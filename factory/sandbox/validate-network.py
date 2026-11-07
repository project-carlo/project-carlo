"""Exercise production proxy DNS/redirect policy with isolated DNS/HTTP fixtures.

Uses a documentation-only public-classified address on a private test bridge; no
public server or authoritative DNS changes are needed. Never starts a dispatcher.
Run: uv run python factory/sandbox/validate-network.py
"""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
from pathlib import Path

from pdf_extract.factory import sandbox

ROOT = Path(__file__).resolve().parents[2]
IMAGE = 'docker.io/library/python:3.13-alpine'

FIXTURE = r'''
import json, socketserver, struct, threading, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs

def record(kind, **fields):
    with open('/state/events.jsonl', 'a') as out:
        out.write(json.dumps({'kind': kind, 'at': time.time(), **fields})+'\n')

counts = {}
class DNS(socketserver.BaseRequestHandler):
    def handle(self):
        data, sock = self.request
        end, names = 12, []
        while data[end]:
            size = data[end]
            names.append(data[end+1:end+1+size].decode())
            end += size+1
        end += 1
        qtype, qclass = struct.unpack('!HH', data[end:end+4])
        domain = '.'.join(names)
        phase = Path('/state/phase').read_text().strip()
        ip = '10.231.184.10' if domain.startswith('rebind.') and phase == 'private' else '203.0.113.10'
        if domain.startswith('rebind.') and phase.startswith('flip-') and qtype == 1:
            counts[phase] = counts.get(phase, 0) + 1
            ip = '203.0.113.10' if counts[phase] == 1 else '10.231.184.10'
        record('dns', domain=domain, qtype=qtype, phase=phase, ip=ip if qtype==1 else None)
        answer = b''
        if qtype == 1:
            answer = b'\xc0\x0c'+struct.pack('!HHIH',1,1,0,4)+bytes(map(int,ip.split('.')))
        reply = data[:2]+struct.pack('!HHHHH',0x8180,1,bool(answer),0,0)+data[12:end+4]+answer
        sock.sendto(reply,self.client_address)

class HTTP(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'
    def do_GET(self):
        address = self.connection.getsockname()[0]
        record('http', address=address, path=self.path, host=self.headers.get('Host'))
        target = parse_qs(urlparse(self.path).query).get('target', [None])[0]
        if urlparse(self.path).path == '/redirect' and target:
            self.send_response(302)
            self.send_header('Location',target)
            body=b'redirect'
        else:
            self.send_response(200)
            body=b'PUBLIC_FIXTURE_OK' if address=='203.0.113.10' else b'PRIVATE_FIXTURE_REACHED'
        self.send_header('Content-Length',str(len(body)))
        self.send_header('Connection','close')
        self.end_headers()
        self.wfile.write(body)
    def log_message(self,*args): pass

threading.Thread(target=socketserver.ThreadingUDPServer(('0.0.0.0',5353),DNS).serve_forever,daemon=True).start()
ThreadingHTTPServer(('0.0.0.0',8080),HTTP).serve_forever()
'''

CLIENT = r'''
import http.client, json, os, socket, urllib.request, urllib.error
from urllib.parse import quote

proxy = os.environ['PROXY_HOST']
mode = os.environ['MODE']
rows=[]
def get(url):
    opener=urllib.request.build_opener(urllib.request.ProxyHandler({'http':f'http://{proxy}:4750'}))
    try:
        with opener.open(url,timeout=15) as response:
            return {'status':response.status,'body':response.read().decode(),'final_url':response.url}
    except urllib.error.HTTPError as error:
        return {'status':error.code,'body':error.read().decode(),'final_url':error.url}

def connect(host):
    with socket.create_connection((proxy,4750),timeout=15) as sock:
        sock.sendall(f'CONNECT {host}:8080 HTTP/1.1\r\nHost: {host}:8080\r\n\r\n'.encode())
        data=b''
        while b'\r\n\r\n' not in data:
            data+=sock.recv(4096)
        status=int(data.split(b' ',2)[1])
        if status==200:
            sock.sendall(f'GET /connect-ok HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n'.encode())
            body=b''
            while chunk:=sock.recv(4096): body+=chunk
            assert b'PUBLIC_FIXTURE_OK' in body,body
        return {'status':status,'headers':data.decode()}

if mode=='redirects':
    good=get('http://stable.validation.test:8080/ok')
    assert good['status']==200 and good['body']=='PUBLIC_FIXTURE_OK',good
    rows.append({'case':'public-http','result':good})
    public='http://stable.validation.test:8080/ok'
    good=get('http://redirect.validation.test:8080/redirect?target='+quote(public,safe=''))
    assert good['status']==200 and good['body']=='PUBLIC_FIXTURE_OK',good
    rows.append({'case':'public-redirect','result':good})
    for host in ('127.0.0.1','10.231.184.10','169.254.169.254','192.168.1.1','[::1]'):
        target=f'http://{host}:8080/private-canary'
        blocked=get('http://redirect.validation.test:8080/redirect?target='+quote(target,safe=''))
        assert blocked['status']==407 and 'denied' in blocked['body'].lower(),blocked
        rows.append({'case':'private-redirect','target':target,'result':blocked})
elif mode == 'flip-http':
    result=get('http://rebind.validation.test:8080/flip-http')
    assert result['status']==200 and result['body']=='PUBLIC_FIXTURE_OK',result
    rows.append({'case':mode,'result':result})
elif mode == 'flip-connect':
    result=connect('rebind.validation.test')
    assert result['status']==200,result
    rows.append({'case':mode,'result':result})
elif mode in ('public','private','public-again'):
    http=get('http://rebind.validation.test:8080/rebind-'+mode)
    tunnel=connect('rebind.validation.test')
    if mode=='private':
        assert http['status']==407 and 'denied' in http['body'].lower(),http
        assert tunnel['status']==407 and 'denied' in tunnel['headers'].lower(),tunnel
    else:
        assert http['status']==200 and http['body']=='PUBLIC_FIXTURE_OK',http
        assert tunnel['status']==200,tunnel
    rows.append({'case':'dns-'+mode,'http':http,'connect':tunnel})
print(json.dumps(rows),flush=True)
'''


def main() -> int:
    os.umask(0o077)
    output = Path(tempfile.mkdtemp(prefix='carlo-pr184-network-'))
    print(f'Private artifacts: {output}', flush=True)
    suffix = str(os.getpid())
    private, public = f'carlo-net-private-{suffix}', f'carlo-net-public-{suffix}'
    fixture, proxy = f'carlo-net-fixture-{suffix}', f'carlo-net-proxy-{suffix}'
    client = f'carlo-net-client-{suffix}'
    sandbox.NETWORK, sandbox.PROXY = private, proxy
    (output / 'fixture.py').write_text(FIXTURE)
    (output / 'client.py').write_text(CLIENT)
    (output / 'phase').write_text('public')
    report = {'fixture_public_ip': '203.0.113.10', 'fixture_private_ip': '10.231.184.10',
              'results': [], 'topology': 'isolated RFC5737 public-classified fixture; production deny policy'}

    def podman(*args, check=True):
        result = subprocess.run(['podman', *args], capture_output=True, text=True, timeout=120)
        if check and result.returncode:
            raise RuntimeError(f'podman {args[:2]}: {result.stderr}')
        return result

    try:
        podman('network', 'create', '--internal', '--subnet', '10.231.184.0/24', private)
        podman('network', 'create', '--internal', '--subnet', '203.0.113.0/24', public)
        podman('run', '-d', '--name', fixture,
               '--network', f'{private}:ip=10.231.184.10',
               '--network', f'{public}:ip=203.0.113.10', '--read-only', '--cap-drop=ALL',
               '--security-opt', 'no-new-privileges', '--userns=keep-id',
               '-v', f'{output}:/state:rw', IMAGE, 'python', '/state/fixture.py')
        files = sandbox.main_files(ROOT, 'HEAD', (sandbox.PROXY_FILE,))
        tag = sandbox.image_tag(files, sandbox.PROXY_IMAGE)
        sandbox.PodmanBackend(ROOT, 'HEAD').build_image(files, tag, 'Proxy.Containerfile')
        argv = sandbox.proxy_argv(sandbox.host_addresses(), tag, '10.231.184.10:5353')
        # The fixture bridge replaces normal external egress for this controlled test.
        argv[argv.index('podman')] = public
        podman(*argv)
        report['proxy_image'] = tag
        report['proxy_argv'] = argv
        # Synchronize readiness without relying on a sleep or fixed boot timing.
        ready = podman('run', '--rm', '--network', private, IMAGE, 'python', '-c',
                       'import socket,time\n'
                       f'for host,port in [({fixture!r},8080),({proxy!r},4750)]:\n'
                       ' for attempt in range(100):\n'
                       '  try:\n'
                       '   socket.create_connection((host,port),timeout=1).close(); break\n'
                       '  except OSError: time.sleep(.1)\n'
                       ' else: raise RuntimeError("fixture/proxy not ready")')
        assert ready.returncode == 0
        for mode in ('redirects', 'public', 'private', 'public-again', 'flip-http', 'flip-connect'):
            (output / 'phase').write_text(mode if mode.startswith('flip-') or mode == 'private'
                                          else 'public')
            result = podman('run', '--rm', '--name', client, '--network', private,
                            '--read-only', '--cap-drop=ALL', '--security-opt', 'no-new-privileges',
                            '-v', f'{output / "client.py"}:/client.py:ro',
                            '-e', f'PROXY_HOST={proxy}', '-e', f'MODE={mode}',
                            '-e', 'no_proxy=', '-e', 'NO_PROXY=', IMAGE, 'python', '/client.py',
                            check=False)
            (output / f'{mode}.stdout').write_text(result.stdout)
            (output / f'{mode}.stderr').write_text(result.stderr)
            assert result.returncode == 0, result.stderr
            report['results'].extend(json.loads(result.stdout))
            print(f'{mode}: passed', flush=True)
        events = [json.loads(line) for line in (output / 'events.jsonl').read_text().splitlines()]
        assert any(e['kind'] == 'dns' and e.get('phase') == 'private' and
                   e.get('ip') == '10.231.184.10' for e in events)
        assert not any(e['kind'] == 'http' and e['address'] == '10.231.184.10' for e in events)
        for mode in ('flip-http', 'flip-connect'):
            answers = [e for e in events if e['kind'] == 'dns' and e['phase'] == mode
                       and e.get('qtype') == 1 and e['domain'].startswith('rebind.')]
            assert len(answers) == 1 and answers[0]['ip'] == '203.0.113.10', answers
        report['validated_address_pinned_for_http_and_connect'] = True
        report['private_fixture_requests'] = 0
        report['passed'] = True
        return 0
    finally:
        (output / 'proxy.log').write_text(podman('logs', proxy, check=False).stderr)
        for name in (client, proxy, fixture):
            podman('rm', '-f', name, check=False)
        for network in (private, public):
            podman('network', 'rm', network, check=False)
        (output / 'report.json').write_text(json.dumps(report, indent=2))
        print(f'Report: {output / "report.json"}', flush=True)


if __name__ == '__main__':
    raise SystemExit(main())
