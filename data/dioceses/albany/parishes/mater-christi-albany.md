---
name: Parish of Mater Christi
website: https://www.materchristi.org
bulletin_provider: parishes_online
provider_id: parish-of-mater-christi
publication: ['po-org:parish-of-mater-christi', 'lpi:0018000000Qx7OXAAZ', 'po-container:04/0808']
group: ''
evidence:
- url: https://container.parishesonline.com/bulletins/04/0808/20260927B.pdf
  seen: 2026-09-28
  note: 'Page 1 of the 27 September 2026 issue is an image (no text layer; rendered with
    parish-site-access render.py and read). It reads: "26TH SUNDAY IN ORDINARY TIME - SEPTEMBER 27, 2026
    / PARISH OF MATER CHRISTI / ROMAN CATHOLIC CHURCH / 40 HOPEWELL STREET ALBANY, NY 12208 / WEEKEND
    MASSES / SATURDAY VIGIL MASS - 4:00 PM ... SUNDAY - 8:30 AM ... SUNDAY - 11:00 AM". Mater Christi
    alone.'
- url: https://container.parishesonline.com/bulletins/04/0808/20260927B.pdf
  seen: 2026-09-28
  quote: Mater Christi, Albany, NY 04-0808
  note: LPi ad-page footer (page 6, the only page with text), naming the container.
- url: https://www.materchristi.org
  seen: 2026-09-28
  note: The parish site (Wix; answers 429 to plain fetches, loaded in a browser with visit.py). It
    embeds the ParishesOnline organization parish-of-mater-christi and links a bulletin PDF.
---

## Publisher

The Parish of Mater Christi, 40 Hopewell Street, Albany publishes its own weekly bulletin
through ParishesOnline (LPi container 04/0808). The 27 September 2026 issue's cover (page 1,
an image) names "Parish of Mater Christi" alone, at 40 Hopewell Street, with weekend Masses
Saturday 4 pm and Sunday 8:30 am and 11 am, and weekday Masses Tuesday 8:15 am, Wednesday
5:30 pm and Friday 8:15 am and 5:30 pm. `probe po parish-of-mater-christi` lists weekly
issues through 27 September.

Mater Christi shares its pastor (Fr. Charles Onyeneke) with All Saints, Albany, but All
Saints publishes a separate bulletin on eCatholic (`all-saints-albany`), so this is its own
row.

## Worship sites

One: the church at 40 Hopewell Street (`mater-christi-albany`; GCatholic 18081 at "Hurst Ave.
& Hopewell St.", directory 259). The institutional-records index says Mater Christi holds the
records of St. Catherine of Siena and St. Teresa of Avila (Albany); neither building is in
either roster, so nothing is recorded for them here.

## Website and bulletin provider

materchristi.org is the directory's "Parish Website" link (the directory's detail-page link
itself is the malformed `rcda.org/www.mcalbany.org`; mcalbany.org also answers 429). The
site embeds `po-org:parish-of-mater-christi`; `probe po` gave the LPi id and container.

**The bulletin is image-only**: of six pages in the 27 September issue only the LPi ad page
has a text layer. The pipeline will need to read it as images.

## Not yet confirmed

Nothing.
