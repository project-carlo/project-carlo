---
name: The Immaculate Heart of Mary Parish
website: https://www.ihmdushore.com/
bulletin_provider: parishes_online
provider_id: immaculate-heart-of-mary-parish-18614
publication: ['po-org:immaculate-heart-of-mary-parish-18614', 'lpi:0018000000Qx8KJAAZ', 'po-container:03/1303']
group: Immaculate Heart of Mary Parish
evidence:
- url: https://container.parishesonline.com/bulletins/03/1303/20261018B.pdf
  seen: 2026-10-16
  quote: THE IMMACULATE HEART OF MARY PARISH … St. Basil the Great, Dushore … St. Francis of Assisi, Mildred
    … St. Francis of Assisi Chapel, Eagles Mere … Sts. Philip and James, St. John Neumann Shrine, Sugar
    Ridge … Rev. Bert S. Kozen, Pastor
  note: Masthead, page 1 of the 18 October 2026 issue.
- url: https://container.parishesonline.com/bulletins/03/1303/20261018B.pdf
  seen: 2026-10-16
  quote: 7:30 AM is at St. Francis of Assisi, Mildred, and 9:30 AM is at St. Basil the Great, Dushore
  note: 'Page 1 "Mass Schedule": daily Mass Monday-Friday 9:00 AM and Saturday vigil 4:00 PM at St. Basil;
    seasonal Eagles Mere chapel (July 4-September 5, 11:30 AM) and three shrine Masses a year.'
- url: https://parishesonline.com/organization/immaculate-heart-of-mary-parish-18614
  seen: 2026-10-16
  note: '`probe po`: 101 Churchill Street, Dushore, LPi id 0018000000Qx8KJAAZ, container 03/1303, weekly
    issues through 2026-10-18. The parish site embeds this issue list (seen in a browser with visit.py
    on 2026-10-16, after Cloudflare challenged the first 18 loads).'
promoted: 2026-10-17
---

## Publisher

Immaculate Heart of Mary Parish, Dushore (Rev. Bert S. Kozen, pastor) publishes one weekly
bulletin through ParishesOnline (container 03/1303). The 18 October 2026 masthead (page 1) names
all four of its worship sites: "St. Basil the Great, Dushore; St. Francis of Assisi, Mildred;
St. Francis of Assisi Chapel, Eagles Mere; Sts. Philip and James, St. John Neumann Shrine, Sugar
Ridge", with each one's address under "Worship Sites". No neighbouring parish shares it.

## Worship sites

Four, all in the 18 October 2026 Mass Schedule:

- `st-basil-the-great-dushore`: daily 9:00 am, Saturday 4:00 pm, Sunday 9:30 am.
- `st-francis-of-assisi-mildred`: Sunday 7:30 am.
- `st-francis-of-assisi-chapel-eagles-mere`: seasonal, Sunday 11:30 am from 4 July to
  5 September (the issue already gives the 2027 season).
- `sts-philip-and-james-st-john-neumann-shrine-sugar-ridge`: three Masses a year (2027: 11
  July, 1 August, 5 September, at 2:30 pm). The diocesan finder mentions the shrine only inside
  Mildred's Mass-times text, and its Find a Mass page lists "Saint John Neumann Shrine, Sugar
  Ridge" with "Please call the office for the Mass schedule"; neither roster has it as an entry.

## Website and bulletin provider

ihmdushore.com is an eCatholic site (site id 10935) behind Cloudflare: `probe url` and plain curl
get the "Just a moment..." page, and visit.py loaded it on its first try only in a later run. The
page embeds the ParishesOnline issue list for `immaculate-heart-of-mary-parish-18614`; the
eCatholic host has no bulletins (`files.ecatholic.com/10935/bulletins/20261018.pdf` answers 403),
so `ecatholic:10935` is the website, not the bulletin, and is not recorded as a publication.
Fetching goes by the ParishesOnline `provider_id`, so the Cloudflare block does not matter.

## Not yet confirmed

Pages 10-11 of the 18 October issue are images (not read). Nothing about structure.
