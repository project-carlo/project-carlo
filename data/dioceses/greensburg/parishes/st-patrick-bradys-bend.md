---
name: St. Patrick Parish, Brady's Bend
website: https://www.stpatrickbradysbend.org
bulletin_provider: discover_mass
provider_id: st-patrick-east-brady-pa
publication: ['discovermass:st-patrick-east-brady-pa', 'url:https://www.stpatrickbradysbend.org/bulletin/bulletins/']
group: ''
evidence:
- url: https://discovermass.com/church/st-patrick-east-brady-pa/
  seen: 2026-10-22
  quote: 915 State Rte. 68, East Brady, PA 16028
  note: 'Discover Mass (J.S. Paluch) church page "St Patrick", read once with curl. "Current Bulletin
    Oct 25, 2026"; archive back to Aug 9, 2026, weekly. Cover image class "bulletin-cover X-|2026-10-25|1792712072|3396":
    bulletin number 3396, the number the parish site''s file names end in. The Oct 25 issue (downloaded
    once via its tokenised link, 4 pages) is headed "St. Patrick Parish Brady''s Bend, Pennsylvania ...
    915 State Route 68 East Brady, Pennsylvania 16028 ... Schedule of Masses Saturday Vigil ... 5:00 pm
    Sunday ... 9:30 am ... 30th Sunday in Ordinary Time October 25, 2026" and names no other parish or
    church.'
- url: https://www.stpatrickbradysbend.org/wp-content/uploads/2026/10/10182026-3396.pdf
  seen: 2026-10-22
  quote: 29th Sunday in Ordinary Time October 18, 2026
  note: The parish site's own copy of the 18 Oct 2026 issue (3 pages), linked from its post /weekly-bulletin-october-18-2026/.
    Page 1 masthead "St. Patrick Parish Brady’s Bend, Pennsylvania", "Saturday Vigil ... 5:00 pm", "Sunday
    ... 9:30 am", "The Very Reverend Eric J. Dinga, V.F. Administrator"; page 2 "Masses For The Week"
    lists weekday 9:00 am Masses with no place named other than St. Patrick.
- url: https://www.stpatrickbradysbend.org/bulletin/bulletins/
  seen: 2026-10-22
  quote: Weekly Bulletin – October 18, 2026
  note: Diocese-template WordPress bulletin page (plain curl with a browser User-Agent answers 200), one
    post per issue from August 9 to October 18, 2026. On 2026-10-22 it had not yet posted the Oct 25 issue
    that Discover Mass already carried.
- url: https://parishesonline.com/organization/st-patrick-church-16028
  seen: 2026-10-22
  note: 'LPi organization "St. Patrick Church", 915 State Route 68, East Brady (lpi 0018000000QxC0MAAV):
    `probe po` lists no publications. An empty organization, not a channel; its ids are not recorded.'
promoted: 2026-10-23
---

## Publisher

St. Patrick Parish, Brady's Bend (directory 033, GCatholic 24156) publishes its own weekly bulletin. J.S. Paluch prints it for Discover Mass under the church page `st-patrick-east-brady-pa` (bulletin number 3396), and the parish reposts each issue on its diocese-template site as `wp-content/uploads/<yyyy>/<mm>/<MMDDYYYY>-3396.pdf`. The 25 October 2026 issue (Discover Mass, read 2026-10-22) and the 18 October 2026 issue (parish site) both have the masthead "St. Patrick Parish Brady's Bend, Pennsylvania", 915 State Route 68, East Brady, with Father Eric J. Dinga as administrator. Neither names another parish or worship site.

Batch 16 checked that this parish is in neither the Ford City nor the Kittanning/Yatesboro bulletins. No partner parish is listed in the directory. The Discover Mass page `st-eusebius-east-brady-pa` and the LPi org `st-eusebius-catholic-church` that the LPi geo-search turns up near East Brady are St. Eusebius, East Brady. GCatholic's Greensburg list and the diocese directory do not include St. Eusebius, so it is presumably a Diocese of Erie parish across the Allegheny. It is not modelled here, and this was not checked further.

## Worship sites

One church: St. Patrick, 915 State Route 68 (`st-patrick-bradys-bend`). The 25 Oct 2026 issue lists Saturday Vigil at 5:00 pm, Sunday at 9:30 am and weekday Masses Tuesday to Friday at 9:00 am, and names no other place. GCatholic and the directory list no other site for the parish.

## Website and bulletin provider

`discover_mass`, provider_id `st-patrick-east-brady-pa`. Discover Mass had the 25 Oct issue on 2026-10-22, while the parish's own bulletin page (https://www.stpatrickbradysbend.org/bulletin/bulletins/) still ended at 18 Oct. Both carry the same bulletin number (3396), so both are recorded as publications of this one row. The website is the parish's own site, which is the directory's homepage for it. The LPi organization `st-patrick-church-16028` is empty.

If the Discover Mass download cap gets in the way, a fallback is `other` with `dated-post https://www.stpatrickbradysbend.org/bulletin/bulletins/ filename=[0-9]*.pdf`, which reads the same issue about a week later.

## Not yet confirmed

Discover Mass caps downloads per IP per day, so `fetch:check` may report `not_pdf` on a day the issue was already downloaded.
