---
name: St. James Parish
website: https://sjredbank.org/
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/saint-james-parish-red-bank-nj-07701
publication: ['url:https://www.church-bulletin.org/saint-james-parish-red-bank-nj-07701']
group: Cohort 16 (Red Bank, Rumson, Fair Haven)
evidence:
- url: https://www.church-bulletin.org/bulletin/saint-james-parish-red-bank-nj-07701/2026-11-01.pdf
  seen: 2026-10-30
  quote: A Catholic Community on the Pilgrimage of Holiness
  note: '12-page issue dated 1 November 2026 (Feast of All Saints), text layer. Page 1: ''Saint James
    Parish'', 94 Broad Street, Red Bank, NJ 07701, with the parish office hours, Saint James Elementary
    School, Mount Olivet Cemetery and Red Bank Catholic High School; ''A Message from Msgr. Joe''. Page
    3 ''This Week, Worship'': ''Saturday Evening Mass: 5:30 pm'', Sunday 7:30 am, 9:00 am, 10:30 am, 12:00
    pm and 5:30 pm, weekday Monday to Friday 6:30 am and 8:15 am, Saturday 8:15 am. It names St. James
    alone.'
- url: https://www.church-bulletin.org/saint-james-parish-red-bank-nj-07701
  seen: 2026-10-30
  note: John Patrick Publishing listing 618 ('Saint James Parish, Red Bank, NJ 07701'); latest edition
    1 November 2026 (links the 2026-11-01 and 2026-10-25 PDFs).
- url: https://sjredbank.org/
  seen: 2026-10-30
  note: The parish site (Joomla; probe url reads it) links https://www.jppc.net/onlinebulletins/618template.pdf,
    the listing 618 redirect, as its bulletin. It embeds no other publication.
research:
- method: pnpm fetch:check --diocese trenton --parish st-james-red-bank (headed Chrome); page-pdfs on
    the John Patrick listing
  url: https://www.church-bulletin.org/saint-james-parish-red-bank-nj-07701
  checked: '2026-10-30'
  outcome: found
  next_action: 'None; transport ok, document_type pdf, picks the 2026-11-01 issue (freshness ''future'':
    the coming Sunday''s issue, posted early, which the playbook treats as current)'
bulletin_status: available
---

## Publisher

St. James Parish, Red Bank publishes its own weekly bulletin through John Patrick Publishing (listing 618 on church-bulletin.org), which the parish site links as `jppc.net/onlinebulletins/618template.pdf`. The 1 November 2026 issue's masthead on page 1 reads "Saint James Parish ... 94 Broad Street, Red Bank, New Jersey 07701" with "A Message from Msgr. Joe" (the bulletin does not label the writer; presumably the pastor, an inference); it names St. James alone, with its school (Saint James Elementary), its Mount Olivet Cemetery and Red Bank Catholic High School, 112 Broad Street. No Cohort 16 neighbour (the Oratory, Nativity, Holy Cross) appears in it.

## Worship sites

One church, 94 Broad Street (see `st-james-red-bank`). The bulletin mentions "Masses of Remembrance at 12 noon in the Masoleum Chaple of Mount Olivet Cemetery, our parish cemetery" on All Souls Day (2 November 2026): a one-off cemetery Mass at 100 Chapel Hill Road, Middletown, not a regular Mass site, so no church row. The site's Liturgical Schedule lists the same Masses as the bulletin.

## Website and bulletin provider

GCatholic lists no website for St. James; the finder's `sjredbank.org` is live. The bulletin is the John Patrick listing, so the row is `other` with `page-pdfs` on the listing.

## Not yet confirmed

Nothing outstanding. Whether the cemetery chapel has a regular Mass is not stated; revisit if a later bulletin lists it.
