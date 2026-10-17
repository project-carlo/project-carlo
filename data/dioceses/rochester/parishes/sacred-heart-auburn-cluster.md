---
name: Catholic Community of Sacred Heart, St. Alphonsus, St. Ann Parish and Holy Family
website: https://sacredheartauburn.org
bulletin_provider: other
provider_id: ''
publication: ['url:https://www.sacredheartauburn.org/bulletin__trashed/']
group: Sacred Heart cluster (Auburn)
evidence:
- url: https://www.sacredheartauburn.org/wp-content/uploads/Sacred-Heart-092726.pdf.pdf
  seen: 2026-10-02
  quote: The Catholic Community of Holy Family * Sacred Heart * St. Alphonsus * St. Ann
  note: 27 Sep 2026 issue, page 1 masthead (the 4 Oct issue was not posted on 2 Oct). It still names Holy
    Family, closed June 2024.
- url: https://www.sacredheartauburn.org/wp-content/uploads/Sacred-Heart-092726.pdf.pdf
  seen: 2026-10-02
  quote: Sacred Heart Church 90 Melrose Rd St. Alphonsus Church 85 E. Genesee St. St. Ann Church 4890
    Twelve Corners Rd. Holy Family Church 85 North St.
  note: 'Page 1: the church list, with Holy Family still printed.'
- url: https://www.sacredheartauburn.org/wp-content/uploads/Sacred-Heart-092726.pdf.pdf
  seen: 2026-10-02
  quote: Sunday, September 27, 2026 8:30 am Sacred Heart
  note: 'Page 5: Mass intentions at Sacred Heart, St. Alphonsus and St. Ann; none at Holy Family.'
- url: https://www.sacredheartauburn.org/mass-times/
  seen: 2026-10-02
  quote: Saturdays 4:00pm at Sacred Heart 4:30pm at St. Alphonsus
  note: Cluster Mass-times page, read 2 Oct 2026.
- url: https://www.sacredheartauburn.org/bulletin__trashed/
  seen: 2026-10-02
  note: 'Bulletin page (visit.py, 2 Oct 2026): self-hosted WordPress uploads, newest Sacred-Heart-092726.pdf.pdf,
    no publisher id. The page slug "bulletin__trashed" is odd (a WordPress page that was trashed and re-created)
    but it is the live nav target.'
- url: https://ps.dor.org/directory/sacred-heart/
  seen: 2026-10-02
  quote: SACRED HEART, 90 Melrose Rd., Auburn ST. ALPHONSUS, 85 East Genesee St., Auburn ST. ANN, Route
    38A, Owasco
  note: 'Diocesan directory: "Sacred Heart, a cluster community"; a second listing makes St. Ann a "mission
    of Sacred Heart".'
promoted: 2026-10-02
---

## Publisher

The Sacred Heart cluster of Auburn publishes one self-hosted PDF bulletin on sacredheartauburn.org. The 27 September 2026 issue is headed "The Catholic Community of Holy Family * Sacred Heart * St. Alphonsus * St. Ann" and has one Mass-intention list (page 5) for Sacred Heart, St. Alphonsus and St. Ann. It is **separate** from the St. Mary's / Ss. Mary & Martha / Our Lady of the Snow bulletin (ParishesOnline 06/0329): the two clusters have different pastors (Fr. Karani here, Fr. White there), offices (90 Melrose Rd vs 299 Clark St) and mastheads. So the Locator's group "Holy Family" (Sacred Heart, St. Alphonsus, Holy Family, St. Ann) is one row, and Holy Family's name is a different "Holy Family" from Wayland's "Holy Family Catholic Community" (a different row, not mine).

## Worship sites

Sacred Heart (90 Melrose Rd), St. Alphonsus (85 E. Genesee St) and St. Ann (4890 Twelve Corners Rd, Owasco; "a mission of Sacred Heart" in the directory). Holy Family, 85 North St, closed on 16 June 2024 and is `excluded/holy-family-auburn`, even though the masthead and church list still print its name. The Locator lists St. Ann (`directory:290-st-ann`), and GCatholic (`17859`) the same church, both previously unlinked.

## Website and bulletin provider

`website` https://sacredheartauburn.org (redirects to www) links the bulletin page. Provider `other`; the publication is the bulletin page `/bulletin__trashed/`. The Locator's old addresses are dead or unusable: shsarc.com (self-signed certificate), auburnholyfamily.org (403), stalphonsusauburn.org (no DNS).

## Not yet confirmed

- The bulletin page slug "bulletin__trashed" may be changed by the webmaster; if fetch stops finding PDFs, re-run `visit.py --bulletin` on the home page.
- The cluster's Mass-times page still lists a Friday 7:30 am Mass at St. Alphonsus; the 27 Sept bulletin says it was discontinued from 25 Sept 2026.
