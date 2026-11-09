---
name: St. Augustine
website: https://staugustinehighland.org
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:11044']
group: ''
evidence:
- url: https://staugustinehighland.org/bulletins
  seen: 2026-10-08
  quote: August 16, 2026
  note: Latest 2026 archive link in the rendered parish page on October 8. This states the observed archive
    endpoint, not cessation of publishing or Mass.
- url: https://files.ecatholic.com/11044/bulletins/20260816.pdf?t=1786582214000
  seen: 2026-10-07
  quote: "Baptisms/Weddings Anointing of the sick Eucharistic Adoration\r\nBaptism: 3rd Saturday of the\
    \ Month. \r\nCome to the Parish Office to schedule.\r\nWeddings: Call the Parish Office at \r\nleast\
    \ 6 months prior for appointment.\r\n \r\n The Priests and Eucharistic\r\n ministers bring Holy Communion\r\
    \n to the homebound. \r\n \r\n \r\n Call for Anointing of the Sick. \r\n \r\n \r\n All Fridays: Adoration\
    \ - 3 to 6PM\r\n Rosary at 5:15 PM\r\n \r\n Spanish Charismatic Prayer \r\n \r\n Healing Mass: Thursday\
    \ - 7 pm \r\n Divine Mercy Chaplet: After Mass \r\nSaturday Vigil: 5 pm\r\nSunday: 7:30 am, 9 am,\
    \ 11:15 am \r\nSpanish Mass: 1 pm\r\nHoly Day Masses - See inside bulletin \r\n Monday – Friday: 8:00\
    \ am\r\n National Holidays - 8 am\r\n \r\n First Fridays: 8:00 am \r\n \r\n Saturdays: 4 pm - 4:45\
    \ pm\r\n \r\n Anytime by appointment.\r\n55 Main Street, Highland, NY 12528 Phone: (845) 691-7673\
    \ \r\nWebsite: www.staugustinehighland.org\r\nPASTOR: Rev. John W. Lynch ASSOCIATE PASTOR: Rev. Charles\
    \ Wiredu Arkorful \r\nDEACON: Marc Fanelli Trustees: Sam Mercier & Gerri Kilpatrick \r\nAugust 16,\
    \ 2026\r\n20th Sunday in Ordinary Time\r\nMass Schedule/Holy Days Daily Mass Sacrament"
  note: Actual bulletin text, page 1, read October 7, 2026. If a future Sunday is printed, it was already
    publicly posted; no future event is inferred as completed.
- url: https://staugustinehighland.org/
  seen: 2026-10-07
  quote: "Mass Schedule \nSATURDAY:\n5:00 PM \nSUNDAY:\n7:30 AM \n9:00 AM \n11:15 AM \n1:00 PM Spanish \n\
    6:00 PM \n \nConfessions \nSUNDAY:\n7:00 PM to 7:25 PM or by appointment\nSATURDAY:\n4:00 PM to 4:45\
    \ PM\nThis Week on FORMED\nOur Parish has Formed!\n\nWebmaster\n\nIf you would like to have something\
    \ posted to the St Augustine Highland website, please email your request to:  staweb33@gmail.com\n\
    \nBecoming Catholic - OCIA\n\nSaint Augustine Church in Highland, NY,  is a Catholic Community committed\
    \ to spreading the Gospel of Jesus Christ, and welcoming others to our Parish Family..  Be sure to\
    \ check our site for Mass and Liturgy schedules, Food Pantry, Thrift Shop, Bazaar "
  note: Current parish site, read in headed Chrome during October 7 research; exact public schedule, not
    canonical directory name.
- url: https://files.ecatholic.com/11044/bulletins/20261108.pdf
  seen: 2026-11-08
  note: November 8, 2026 issue, image-only (page 1 read from a rendering). Masthead 'St. Augustine Parish,
    55 Main Street, Highland, NY 12528', Rev. John W. Lynch, pastor; 'November 8, 2026, 32nd Sunday in
    Ordinary Time'; Mass schedule Saturday Vigil 5 pm, Sunday 7:30 am, 9:00 am, 11:15 am, 1:00 pm (Spanish),
    daily 8:00 am. No other church is named on page 1.
revisit: Re-run fetch:check in late November; the archive went quiet from August 16 to November 8, 2026,
  so a further silence would leave the row without a current issue.
revisit_after: 2026-11-29
promoted: 2026-11-09
research:
- method: issues.py ecatholic:11044 --weeks 14 and headed-Chrome visit of the Bulletins page
  url: https://staugustinehighland.org/bulletins
  checked: '2026-11-08'
  outcome: found
  next_action: None; the archive resumed with the November 8 issue after nothing between August 16 and
    November 1 (every Sunday in between answered 403).
- method: PLAYWRIGHT_BROWSER_CHANNEL=chrome xvfb-run -a pnpm fetch:check --parish st-augustine-highland
  url: https://staugustinehighland.org
  checked: '2026-11-08'
  outcome: found
  next_action: Re-run if a later week picks an old issue
bulletin_status: available
---

## Publisher

St. Augustine Parish, 55 Main Street, Highland, publishes its own weekly bulletin on eCatholic (site 11044). The November 8, 2026 issue (image-only; page 1 read from a rendering on 2026-11-08) has that masthead, the date and 32nd Sunday, and its own Mass schedule: Saturday Vigil 5 pm; Sunday 7:30, 9:00, 11:15 am and 1:00 pm (Spanish); daily 8:00 am. The archive had nothing between August 16 and November 1, 2026 (each Sunday answered 403); it resumed with November 8.

## Worship sites

[St. Augustine, Highland](../churches/st-augustine-highland.md): the schedule above. Page 1 names no other church. St. Cecilia is not merged into this publisher on the strength of an August decree; no shared issue has been read.

## Website and bulletin provider

The parish site staugustinehighland.org is eCatholic-hosted (publication ecatholic:11044), so the `ecatholic` reader takes it from `website`. The issues are scanned images. The October 2026 hold (`no_bulletin`, because the archive then ended August 16) is lifted: fetch:check on 2026-11-08 picked the November 8 issue. The connector question `open/st-augustine-highland-fetch-connector` is closed and deleted.

## Recheck

On October 8, 2026 the archive still ended August 16. On November 8 the November 8 issue was posted. Watch for another gap.

## Automatic fetch safeguard

None now: the provider is `ecatholic` again.
