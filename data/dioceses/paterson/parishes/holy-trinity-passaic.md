---
name: Holy Trinity
website: https://holytrinitypassaic.com/
bulletin_provider: parishes_online
provider_id: holy-trinity-church-07055
publication: ['po-org:holy-trinity-church-07055', 'lpi:0018000000Qbz3OAAR', 'po-container:03/0832']
group: ''
evidence:
- url: https://container.parishesonline.com/bulletins/03/0832/20261108B.pdf
  seen: 2026-11-05
  quote: 226 Harrison St., Passaic, NJ 07055
  note: 'Page 1 of the 8 November 2026 bulletin: the Parish Family of Holy Trinity Church welcomes you
    (English, German, Spanish); Rev. Antonio Rodriguez, Pastor; Mass schedule Saturday 7:30 pm (Spanish);
    Sunday 8:30 am (English), 10:00 am (German), 11:30 am, 1:30 pm and 3:30 pm (Spanish); Wed/Fri 7:30
    pm (Spanish). Page 2 heads ''Church of the Holy Trinity Passaic, NJ'' with intentions for 7-11 November.
    Four pages, all with text; a grep for Chapel and Capilla finds none.'
- url: https://parishesonline.com/organization/holy-trinity-church-07055
  seen: 2026-11-05
  note: 'probe po: org Holy Trinity Church, 226 Harrison St, Passaic, website holytrinitypassaic.com,
    lpi 0018000000Qbz3OAAR, container 03/0832; weekly issues 4 October to 8 November 2026.'
- url: https://holytrinitypassaic.com/bulletins
  seen: 2026-11-05
  note: 'eCatholic site 11689 (read with visit.py): the Bulletin page has no issue links, and the site
    menu links no bulletin. issues.py ecatholic:11689 found no Sunday, Saturday or Friday file for the
    last 4-6 weeks (403).'
bulletin_status: available
---

## Publisher

Holy Trinity, Passaic publishes a weekly trilingual bulletin through LPi / ParishesOnline (org `holy-trinity-church-07055`, container 03/0832). Page 1 of the 8 November 2026 issue (`https://container.parishesonline.com/bulletins/03/0832/20261108B.pdf`, read 2026-11-05) reads "the Parish Family of Holy Trinity Church ... Welcomes You", with the rectory at "226 Harrison St., Passaic, NJ 07055" and Rev. Antonio Rodriguez, Pastor. Page 2 is headed "Church of the Holy Trinity Passaic, NJ".

## Worship sites

- `holy-trinity-passaic`: the only church. The page 1 Mass schedule (Saturday 7:30 pm Spanish; Sunday 8:30 English, 10:00 German, 11:30, 1:30 and 3:30 Spanish; Wed/Fri 7:30 pm Spanish) names no other place, and a grep of the issue for Chapel and Capilla finds none.

The diocese's finder (directory:11689) and GCatholic (18992) list this one church.

## Website and bulletin provider

The parish site is eCatholic site 11689, but its Bulletin page lists no issues and its menu links none, and `issues.py` found no file in the eCatholic archive for recent weeks (Sunday, Saturday or Friday names all 403). The bulletin is on ParishesOnline: the org page gives the parish's own website and address, and has weekly issues through 8 November 2026. So the provider is `parishes_online` with the org slug as `provider_id`; `ecatholic:11689` is not recorded, as it carries no issues. `fetch:check` on 2026-11-05 picked `https://container.parishesonline.com/bulletins/03/0832/20261108B.pdf`, next Sunday's issue (freshness `future`, age -3 days), whose masthead was read above.

## Not yet confirmed

Nothing open.
