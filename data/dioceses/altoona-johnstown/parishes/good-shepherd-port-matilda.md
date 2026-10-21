---
name: Good Shepherd Parish, Port Matilda
website: https://www.goodshepherd-sc.org
bulletin_provider: ecatholic
provider_id: '37809'
publication: ['ecatholic:37809']
group: ''
evidence:
- url: https://files.ecatholic.com/37809/bulletins/20261018.pdf
  seen: 2026-10-21
  quote: 'Address: 867 Gray’s Woods Boulevard'
  note: 'Page 1 of the 18 Oct 2026 issue (12 pages): masthead "THE CHURCH OF THE GOOD SHEPHERD", Port Matilda PA 16870, Pastor Father Jozef Kovacik. Page 2 Mass intentions: Sat 5:00 p.m.; Sun 8:30 a.m. and 10:30 a.m.; Mon 8:30; Tue and Wed no Mass or Communion Service; Thu 8:30; Fri 12:00 p.m. It names this church alone.'
- url: https://www.goodshepherd-sc.org/
  seen: 2026-10-21
  note: 'Cloudflare answers curl and `probe url` with 403 (HTTP4XX); headed Chrome (`visit.py --bulletin`) opens it: title "Good Shepherd Catholic Church - Port Matilda, PA", embeds ecatholic:37809, Bulletin link https://www.goodshepherd-sc.org/bulletins.'
- url: https://www.dioceseaj.org/parishes/
  seen: 2026-10-21
  note: 'Directory: Good Shepherd Parish, Port Matilda, 867 Grays Woods Boulevard 16870, homepage goodshepherd-sc.org; Masses Sat 5:00 PM, Sun 8:30 and 10:30 AM, Mon-Thu 8:30 AM (the directory lists Tue and Wed 8:30; the 18 Oct bulletin says no Mass those days that week), Fri 12 noon.'
---

## Publisher

Good Shepherd (Fr. Jozef Kovacik, pastor) publishes its own weekly bulletin through eCatholic site 37809, one PDF per Sunday at `files.ecatholic.com/37809/bulletins/<YYYYMMDD>.pdf`. The 18 October 2026 issue (read 2026-10-21) is headed "THE CHURCH OF THE GOOD SHEPHERD" and carries only this church's Masses.

## Worship sites

One church, 867 Gray's Woods Boulevard, Port Matilda (the postal city; the parish is in the State College area). No other Mass site appears in the bulletin.

## Website and bulletin provider

`ecatholic`, `provider_id: 37809`, website the eCatholic-hosted `www.goodshepherd-sc.org`. `issues.py ecatholic ecatholic:37809` found `20261018.pdf` (200) and 25 Oct not yet posted. `pnpm fetch:check` (2026-10-21) picked `https://files.ecatholic.com/37809/bulletins/20261018.pdf`, status ok.

## Not yet confirmed

Nothing outstanding.
