---
name: Holy Name of Jesus
website: https://www.hnojchurch.org/bulletin
bulletin_provider: other
provider_id: page-pdfs
publication: ['url:https://www.hnojchurch.org/bulletin']
group: ''
evidence:
- url: https://irp.cdn-website.com/280d9b6c/files/uploaded/Nov+14+15+2026+33rd+Sun+OT.pdf
  seen: 2026-11-12
  note: 'Page 1 of the 14-15 November 2026 issue is an image (rendered with render.py; recheck cannot
    find text there): masthead ''HOLY NAME OF JESUS CATHOLIC CHURCH 1950 Barnum Ave., Stratford, CT 06614'',
    ''November 14-15, 2026 ~33rd Sunday in Ordinary Time'', ''Rev. James DiVasto, Pastor''; MASS SCHEDULE
    Weekend Saturday 4:00pm Vigil, Sunday 7:30am, 10:00am; Weekday Tuesday 7:30am and Thursday 7:30am
    ''in the parish Chapel of Saints Cyril & Methodius, 2 Mary Ave'', Wednesday 5:30pm Mass ''All services
    held in Church''. Names no other parish.'
- url: https://irp.cdn-website.com/280d9b6c/files/uploaded/Nov+14+15+2026+33rd+Sun+OT.pdf
  seen: 2026-11-12
  quote: 095A (PK) - Holy Name of Jesus, Stratford
  note: 'Ad-page footer (the only page with a text layer): printed by Bon Venture Services, account 095A.'
- url: https://www.hnojchurch.org/bulletin
  seen: 2026-11-12
  note: 'probe get: the parish''s Duda bulletin page links weekly PDFs on irp.cdn-website.com/280d9b6c,
    newest first: ''Nov+14+15+2026+33rd+Sun+OT.pdf'', ''Nov+7+8+2026+32+Sun+OT.pdf'', ''Oct+31+Nov+1+2026+All+Saints+.pdf''.'
bulletin_status: available
---

## Publisher

Holy Name of Jesus, Stratford publishes its own weekly bulletin, printed by Bon Venture (account 095A) and posted as PDFs on the parish's Duda site. The 14-15 November 2026 issue (`https://irp.cdn-website.com/280d9b6c/files/uploaded/Nov+14+15+2026+33rd+Sun+OT.pdf`, read 2026-11-12) has the masthead "HOLY NAME OF JESUS CATHOLIC CHURCH 1950 Barnum Ave., Stratford, CT 06614" and "Rev. James DiVasto, Pastor" on page 1, and names no other parish. Page 1 is an image; it was rendered and read by eye.

## Worship sites

- `holy-name-of-jesus-stratford`: the church, 1950 Barnum Ave.: Saturday 4:00pm Vigil, Sunday 7:30 and 10:00am, Wednesday 5:30pm ("All services held in Church").
- `sts-cyril-methodius-chapel-stratford`: Tuesday and Thursday 7:30am Mass "in the parish Chapel of Saints Cyril & Methodius, 2 Mary Ave", a separate building about 90 m from the church.

The directory (directory:1455, mass note "In chapel") and GCatholic (22008) list only the church; the chapel is in no roster.

## Website and bulletin provider

The bulletin is self-hosted: `hnojchurch.org/bulletin` (Duda) links each week's PDF on `irp.cdn-website.com/280d9b6c/files/uploaded/`, named by date ("Nov+14+15+2026+33rd+Sun+OT.pdf"), newest first. Provider `other`. `fetch:check` on 2026-11-12 read the page with recipe `page-pdfs` and picked `https://irp.cdn-website.com/280d9b6c/files/uploaded/Nov+14+15+2026+33rd+Sun+OT.pdf` (url date 2026-11-14, freshness `future`; identity unverified as reported, masthead checked by hand above); the recipe is recorded in `provider_id`. The bulletin's content pages are image-only (only the ad page has text), so the pipeline will need to read them as images.

## Not yet confirmed

Nothing open.
