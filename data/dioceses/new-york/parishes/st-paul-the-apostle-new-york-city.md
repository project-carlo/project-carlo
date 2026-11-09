---
name: St. Paul the Apostle
website: https://stpaultheapostle.org/about/newsletter/
bulletin_provider: unsupported
provider_id: ''
publication: ['url:https://stpaultheapostle.org/about/newsletter/']
group: ''
evidence:
- url: https://stpaultheapostle.org/about/newsletter/
  seen: 2026-11-08
  quote: An example of our virtual parish bulletin, which includes information regarding upcoming events,
    articles on current affairs, and reflections from our priests!
  note: Newsletter page; its archive lists weekly issues, newest 'August 6th, 2026' (conta.cc/4bsBNgr),
    same as on 2026-10-08.
- url: https://myemail.constantcontact.com/Summer-at-St--Paul-s--Priestly-Pool-Time--Community-Events-and-More---.html?soid=1103685264260&aid=idbXv9uBmOo
  seen: 2026-11-08
  quote: August 6th, 2026 The Nineteenth Sunday in Ordinary Time The Pastor's Column
  note: The newest archived issue, an HTML email from The Church of St. Paul the Apostle.
- url: https://www.stpaultheapostle.org/
  seen: 2026-11-08
  quote: Saturday 8:30 AM 5:00 PM Sunday 8:00 AM 10:00 AM (Choir) 12:30 PM (Spanish; Coro Hispano) 5:00
    PM (Young Adult Mass & OSP) Monday-Friday 7:30 AM 12:10 PM
  note: Homepage Mass schedule; footer '405 W. 59th St., NYC Columbus & 60th'.
revisit: Check /about/newsletter/ for issues after August 6, 2026; if the archive stays frozen, look for
  a Constant Contact account archive from the soid=1103685264260 emails.
revisit_after: 2026-12-08
research:
- method: probe get of /about/newsletter/, the homepage, and the WordPress search API for 'bulletin'
  url: https://stpaultheapostle.org/about/newsletter/
  checked: '2026-11-08'
  outcome: unsupported-format
  next_action: Look for issues after August 6, 2026 on the newsletter page or a Constant Contact archive;
    set a real provider once a collector reads HTML newsletters
  retry_when: The newsletter archive adds an issue after August 6, 2026, or an HTML-newsletter collector
    lands
bulletin_status: unsupported-format
fetch_gap:
  kind: constant-contact-html-newsletter
  seen: 2026-11-08
  url: https://stpaultheapostle.org/about/newsletter/
  note: The parish calls its weekly Constant Contact email newsletter its 'virtual parish bulletin' and
    archives it as conta.cc / myemail.constantcontact.com links on /about/newsletter/; no PDF. The hand-kept
    archive still ends at 'August 6th, 2026' on 2026-11-08, so even an HTML collector would need a current
    archive.
---

## Publisher

The Paulist parish of St. Paul the Apostle publishes its bulletin as a weekly Constant Contact email. Its newsletter page (https://stpaultheapostle.org/about/newsletter/, read November 8, 2026) calls it "our virtual parish bulletin" and keeps a short archive of links; the newest is "August 6th, 2026", an HTML email headed "August 6th, 2026 The Nineteenth Sunday in Ordinary Time" with the pastor's column. No PDF bulletin is linked anywhere on the site (the WordPress search for "bulletin" finds only the newsletter page). It names only this church.

## Worship sites

One: St. Paul the Apostle, 405 West 59th Street at Columbus Avenue (`churches/st-paul-the-apostle-new-york-city.md`). The homepage (November 8) gives Saturday 8:30 AM and 5:00 PM; Sunday 8:00 AM, 10:00 AM (choir), 12:30 PM (Spanish) and 5:00 PM; Monday-Friday 7:30 AM and 12:10 PM.

## Website and bulletin provider

The website is the newsletter page. No collector reads HTML email, so the row is `unsupported` with `fetch_gap` kind `constant-contact-html-newsletter`. The archive has not moved since August 6 (also the newest on October 8), so whether the emails still go out weekly is not visible publicly; see revisit.

## Not yet confirmed

Whether newsletter issues after August 6, 2026 exist publicly.
