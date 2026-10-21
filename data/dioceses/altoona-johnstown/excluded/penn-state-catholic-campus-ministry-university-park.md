---
name: Nittany Catholic (Penn State Catholic Campus Ministries), Pasquerilla Spiritual Center
reason: no-bulletin
line1: Pasquerilla Spiritual Center, 205A-D
city: University Park
state: PA
postal_code: '16802'
decided: 2026-10-21
roster: ['gcatholic:23887']
evidence:
- url: https://gcatholic.org/churches/usa-03/23887
  seen: 2026-10-21
  quote: 207A Eisenhower Chapel, University Park, Pennsylvania 16802
  note: 'Listed in GCatholic: churches of the Roman Catholic Diocese of Altoona-Johnstown as ''PSU'',
    207A Eisenhower Chapel, University Park, PA, 16802; kind: PSU; group: Penn State Catholic Campus Ministry'
- url: https://nittanycatholic.org/masses/
  seen: 2026-10-21
  quote: ALL ARE WELCOME AT OUR LITURGIES
  note: 'Mass & Sacrament Times page (rendered in headed Chrome; curl gets 406). Semester schedule: Saturday 4pm Vigil, Sunday 9:30am, 11:30am and 8pm in the Worship Hall of Pasquerilla Spiritual Center; Monday-Wednesday 5:05pm Eisenhower Chapel (Pasquerilla) and 9:15pm Holy Family Chapel (Paterno Faith Center); Thursday-Friday 12:15pm Holy Family Chapel and 5:05pm Eisenhower Chapel. Holy Days: "Masses held at Our Lady of Victory and Good Shepherd" on Jan. 1 when the campus is closed.'
- url: https://nittanycatholic.org/
  seen: 2026-10-21
  quote: You are invited to celebrate Mass with us, especially all those visiting the University Park campus!
  note: 'Homepage: "Nittany Catholic - Serving the University Park campus of Penn State"; "Main offices 205A-D Pasquerilla Spiritual Center, University Park PA 16802; Paterno Faith Center, 117 E Park Ave, State College PA 16803"; a "Parish Registration" link. The old psu.edu/catholic and psucatholic.org addresses now redirect here.'
- url: https://discovermass.com/church/penn-state-catholic-campus-ministry-university-park-pa/
  seen: 2026-10-21
  quote: There are currently no bulletins available for Penn State Catholic Campus Ministry.
  note: 'Discover Mass page "Penn State Catholic Campus Ministry", 205A-D Pasquerilla Spiritual Center, (814) 865-4281; lists the same Masses; empty Bulletins tab.'
- url: https://nittanycatholic.org/announcements/
  seen: 2026-10-21
  quote: Mass Announcements
  note: 'The only weekly publication: an HTML page "Week of October 19, 2026" (a few announcements, a Flocknote sign-up). No PDF, no Mass schedule or intentions; not something the fetch pipeline reads. psucatholic.flocknote.com is a sign-up page.'
- url: https://ourladyofvictory.com/wp-content/uploads/2026/10/October-18-2026.pdf
  seen: 2026-10-21
  note: 'Our Lady of Victory''s 17-18 Oct 2026 bulletin and Good Shepherd''s 18 Oct 2026 bulletin (files.ecatholic.com/37809/bulletins/20261018.pdf) were read for a Penn State campus Mass: neither lists one (grep for Penn State, Pasquerilla, Nittany: only "Mount Nittany Medical Center" in OLV).'
---

## Why it is excluded

Penn State's Catholic campus ministry (Nittany Catholic, Catholic Campus Ministries at Penn State, with the Newman Catholic student club) holds **public Mass at a fixed site**: the Worship Hall of the Pasquerilla Spiritual Center, University Park (near the library, NE corner of Allen and Curtin Rds), Saturday 4pm vigil and Sunday 9:30am, 11:30am and 8pm in the semester, with weekday Masses in Eisenhower Chapel (same building, 5:05pm) and the Holy Family Chapel of the Paterno Faith Center. Its own site invites everyone ("You are invited to celebrate Mass with us, especially all those visiting the University Park campus"; "ALL ARE WELCOME AT OUR LITURGIES"; both read 2026-10-21), and it has a Visitors and a Parking page and a "Parish Registration". So unlike the Mount Aloysius and Juniata College Masses (`open/`) this one is settled as public.

It is excluded only because **no bulletin exists the pipeline can read**: Discover Mass has no bulletins for it, the site's "Mass Announcements" page is a few lines of HTML, and neither neighbouring parish bulletin (Our Lady of Victory, 18 Oct; Good Shepherd, 18 Oct) lists it. It was never a parish row of its own (the diocese's parish directory does not list it; GCatholic lists it as "PSU", kind PSU, group "Penn State Catholic Campus Ministry", 207A Eisenhower Chapel). The Mass site is the Pasquerilla Spiritual Center, 205A-D for the offices; GCatholic's point is Eisenhower Chapel in the same building (Plus Code 87G4Q4XM+MC). The weekday chapel at the Paterno Faith Center, 117 E Park Ave, State College, is a second place with public Mass run by the same ministry; it has no record of its own and the same reason applies. During summer the ministry holds Sunday 9:30am in the Worship Hall and weekday Masses at the Paterno Faith Center only.

## What would change this

A readable weekly bulletin or Mass-time page for the ministry (for example a PDF on nittanycatholic.org or a Discover Mass bulletin). Then add a parish row (`other` or `discover_mass`) with churches for the Pasquerilla Spiritual Center and the Paterno Faith Center. Revisit when the 2027 semester starts.
