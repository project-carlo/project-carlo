---
name: St. Joseph (Jamaica)
website: https://www.stjjamaica.org/
bulletin_provider: no_bulletin
provider_id: ''
publication: []
group: Deanery Q9 (Queens East)
evidence:
- url: https://www.stjjamaica.org/_files/ugd/9b1f99_065444f914a24996afefdbe4bd88df1f.pdf
  seen: 2026-11-06
  quote: AUGUST 2026
  note: 'English bulletin linked from /bulletin, 4 pages, text. Page 1 ''Mary, Assumed into Heaven, Pray
    for US AUGUST 2026''; page 2: 10843 Sutphin Blvd., Jamaica, NY 11435, www.stjjamaica.org, PASTOR Fr.
    Cezariusz Jastrzębski; ''SUNDAY MASS TIMES 9:00 AM in English 10:45 AM in Polish''; intentions for
    Sundays July 26 to August 30, 2026. No publisher footer: in-house monthly issue.'
- url: https://www.stjjamaica.org/_files/ugd/9b1f99_097cead6a80b4037b326d5775947d817.pdf
  seen: 2026-11-06
  quote: SIERPIEŃ  2026
  note: Polish edition of the same monthly bulletin (2 pages), August 2026, 108-43 Sutphin Blvd.
- url: https://www.stjjamaica.org/bulletin
  seen: 2026-11-06
  quote: Here you can read our weekly Bulletin
  note: 'Wix bulletin page (read with visit.py): ''BULLETIN IN ENGLISH August 2026'', ''BIULETYN PO POLSKU
    Sierpień 2026'', each linking one /_files/ugd/ PDF; nothing for September to November 2026.'
revisit: Check stjjamaica.org/bulletin for an issue after August 2026; if it is kept current, record other
  and run fetch:check (Wix /_files/ugd/ PDFs have no date in the file name; English and Polish editions
  share the page)
revisit_after: 2027-01-15
research:
- method: probe url (Wix site, bulletin link /bulletin); visit.py --text on the homepage and /bulletin;
    probe pdf of both linked PDFs
  url: https://www.stjjamaica.org/bulletin
  checked: '2026-11-06'
  outcome: not-found
  next_action: Re-read /bulletin for an issue later than August 2026; if found, set bulletin_provider
    other and run fetch:check, pinning the English edition if the resolver picks the Polish one
  retry_when: The /bulletin page lists a month after August 2026, or after 2027-01-15
- method: Discover Mass church page
  url: https://discovermass.com/church/st-joseph-jamaica-ny/
  checked: '2026-11-06'
  outcome: not-found
  next_action: Check the parish's weekly e-newsletter (Mailchimp sign-up on the homepage) and YouTube
    for a bulletin channel
  retry_when: After 2027-01-15
bulletin_status: not-found
---

## Publisher

St. Joseph prints its own monthly bulletin in English and Polish and posts it on its Wix site. The English August 2026 issue (read 2026-11-06) has on page 2 "10843 Sutphin Blvd.", Jamaica, NY 11435, www.stjjamaica.org, Pastor Fr. Cezariusz Jastrzębski, and no publisher footer; the Polish edition is "Sierpień 2026". On 6 November 2026 the /bulletin page still offers only the August 2026 issues, so no current bulletin is posted and the row is `no_bulletin`.

## Worship sites

One church. The August 2026 issue gives "SUNDAY MASS TIMES 9:00 AM in English 10:45 AM in Polish", and the homepage (read 2026-11-06) the same Sunday Masses plus Holy Days 6:30 PM English and 7:30 PM Polish, at the church on Sutphin Blvd. The diocese's parish and deanery directories, GCatholic 16728 and Mass finder place 1147 list only this church.

## Website and bulletin provider

`no_bulletin`. www.stjjamaica.org is the directory's and GCatholic's link and the bulletin's website; its /bulletin page links each month's English and Polish PDFs from Wix's /_files/ugd/ store (hashed names, no dates). Discover Mass says no bulletins are available. The homepage offers a weekly e-newsletter by email sign-up, which was not read.

## Not yet confirmed

Whether the September to November 2026 issues exist and are posted elsewhere (the e-newsletter, social media). See research for the retry.
