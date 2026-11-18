---
name: St. Malachy (The Actors' Chapel)
website: https://actorschapel.org
bulletin_provider: unsupported
provider_id: ''
publication: ['url:https://us13.campaign-archive.com/home/?u=bfc58786edc4ea7ffd7e38609&id=a9f5c81312',
  'ecatholic:14448']
group: ''
evidence:
- url: https://us13.campaign-archive.com/home/?u=bfc58786edc4ea7ffd7e38609&id=a9f5c81312
  seen: 2026-11-08
  quote: 11/07/2026 - Sunday, November 8th Bulletin
  note: 'Mailchimp campaign archive of St. Malachy''s - The Actors'' Chapel: weekly ''Sunday, ... Bulletin''
    emails on 10/17, 10/24, 10/31 and 11/07/2026, plus event emails. Its address came from the list links
    in the 2024 email linked from actorschapel.org.'
- url: https://us13.campaign-archive.com/?u=bfc58786edc4ea7ffd7e38609&id=03c4fe34f8
  seen: 2026-11-08
  quote: Sunday, November 8th, 2026 Thirty-Second Sunday in Ordinary Time
  note: The 8 November 2026 bulletin email (eepurl.com/JG9_PFaQpW); footer 'Copyright © 2026 St. Malachy's
    - The Actors' Chapel'. Most of its content is images.
- url: https://actorschapel.org
  seen: 2026-11-08
  quote: 'Monday - Friday: 8:00am Daily Mass Saturday Vigil Mass: 5:00pm Sunday: 9:00am & 11:00am'
  note: Homepage Mass times; contact block gives 239 West 49th Street, New York, NY 10019.
- url: https://mailchi.mp/actorschapel/st-malachys-church-sunday-march-22-bulletin-6751554
  seen: 2026-10-08
  note: One of the five E-BULLETINS links on the homepage; dated September 8, 2024 despite the March-22
    slug. The others are August 11 to September 1, 2024 (rechecked 2026-11-08).
research:
- method: probe get of the Mailchimp list archive found via the u= id in a linked 2024 email
  url: https://us13.campaign-archive.com/home/?u=bfc58786edc4ea7ffd7e38609&id=a9f5c81312
  checked: '2026-11-08'
  outcome: unsupported-format
  next_action: Set a real provider once a collector reads Mailchimp HTML campaign archives (see fetch_gap)
  retry_when: A Mailchimp/HTML-newsletter collector lands
bulletin_status: unsupported-format
fetch_gap:
  kind: mailchimp-html-newsletter
  seen: 2026-11-08
  url: https://us13.campaign-archive.com/home/?u=bfc58786edc4ea7ffd7e38609&id=a9f5c81312
  note: The weekly bulletin is an HTML Mailchimp email, 'Sunday, <date> Bulletin', archived on the us13.campaign-archive.com
    list (newest '11/07/2026 - Sunday, November 8th Bulletin' on 2026-11-08, between concert announcements).
    No PDF; the actorschapel.org /bulletins eCatholic archive is empty and the homepage's E-BULLETINS
    links point at 2024 emails.
---

## Publisher

St. Malachy's - The Actors' Chapel publishes a weekly bulletin as a Mailchimp email. Its public campaign archive (https://us13.campaign-archive.com/home/?u=bfc58786edc4ea7ffd7e38609&id=a9f5c81312), read November 8, lists "Sunday, October 18th Bulletin", "October 25th", "November 1st" and "Sunday, November 8th Bulletin" (sent 11/07/2026), among concert and event emails. The November 8 email is headed "Sunday, November 8th, 2026 Thirty-Second Sunday in Ordinary Time" and signed "St. Malachy's - The Actors' Chapel". It names no other church.

## Worship sites

One: St. Malachy, 239 West 49th Street (`churches/st-malachy-new-york-city.md`). The homepage (November 8) gives Monday-Friday 8:00 am, Saturday vigil 5:00 pm, Sunday 9:00 and 11:00 am.

## Website and bulletin provider

No collector reads it: the bulletin is HTML email, mostly images, with no PDF. actorschapel.org is an eCatholic site (14448) whose /bulletins archive is empty, and its E-BULLETINS block still links five 2024 emails (August 11 to September 8, 2024). The current archive was found from the list id in those emails. So the row is `unsupported` with `fetch_gap` kind `mailchimp-html-newsletter`, kept off the site until a collector reads it.

## Not yet confirmed

Whether the email's images carry the Mass schedule; the schedule above is from the homepage.
