---
name: Saint Anne Parish, Davidsville
website: https://www.stannedavidsvillepa.org
bulletin_provider: other
provider_id: page-images https://www.stannedavidsvillepa.org/services
publication: ['url:https://www.stannedavidsvillepa.org/services']
group: ''
evidence:
- url: https://www.stannedavidsvillepa.org/services
  seen: 2026-10-21
  note: 'Wix page titled "Bulletin" (nav "Calendar / Bulletin / Server Schedules / Visit Us"; footer "Proudly created with Wix.com"). The only content is one JPEG (static.wixstatic.com/media/d147db_3e320d8812d94528a7de3f02ef366c56~mv2.jpg, alt text "10112026.jpg", 801,095 bytes), read as an image: header "ST. ANNE CHURCH 205 Woodstown Highway Davidsville, PA 15928-0500 ... Fr. Karl Kolodziejski, OFM Conv.- Administrator", "MASSES FOR THE WEEK: MON. OCT. 12 8:00AM ... THURS. OCT. 15 6:30PM ... SAT. OCT. 17 8:00AM / 4:00PM ... SUN. OCT. 18 8:30AM", "TWENTY-EIGHTH SUNDAY IN ORDINARY TIME". It is the bulletin for the week of 12-18 October 2026 (screenshot via visit.py). There is no text layer, so no quote.'
- url: https://discovermass.com/church/st-anne-davidsville-pa/
  seen: 2026-10-21
  quote: There are currently no bulletins available for St. Anne.
  note: 'Discover Mass page exists (814-479-2664) but its Bulletins tab is empty: not a live channel.'
- url: https://www.dioceseaj.org/parishes/
  seen: 2026-10-21
  note: 'Diocese directory lists Saint Anne Parish, Davidsville, one church, 205 Woodstown Highway, homepage https://www.stannedavidsvillepa.org, Masses Sat 4:00 PM, Sun 8:30 AM, Mon-Wed and Fri 8:00 AM, Thu 12:00 PM.'
---

## Publisher

St. Anne Parish, Davidsville posts its own weekly bulletin on the Bulletin page of its Wix
site, https://www.stannedavidsvillepa.org/services, as one JPEG of the printed sheet. Read as
an image on 2026-10-21 (screenshot with visit.py), it is headed "ST. ANNE CHURCH 205 Woodstown
Highway Davidsville, PA 15928-0500", lists Fr. Karl Kolodziejski, OFM Conv. as Administrator,
and gives "MASSES FOR THE WEEK" Mon. Oct. 12 to Sun. Oct. 18: weekdays 8:00 AM, Thursday 6:30 PM,
Saturday 8:00 AM and 4:00 PM, Sunday 8:30 AM. It names this church alone. It is the bulletin for
the week of 12-18 October 2026, so it is current.

## Worship sites

One church, St. Anne (churches/st-anne-davidsville). The directory also lists one church and no
linked parish. Thursday differs by source: the directory says 12:00 PM, the bulletin's header
says "Weekdays: 7:30am, except Thursday 6:00pm", and the 15 October line says 6:30 PM. The
bulletin is the newest; the schedule is not settled to the minute.

## Website and bulletin provider

`bulletin_provider: other`, recipe `page-images https://www.stannedavidsvillepa.org/services`.
The Wix Bulletin page shows each week's sheet as one JPEG whose alt text is its date as
MMDDYYYY ("10112026.jpg") and whose URL is a hash. The first `fetch:check` on 2026-10-21 failed
(`NoBulletin`): the image collector keeps an image only when its address or alt text names a
bulletin or a date, and the date parser did not read an unseparated MMDDYYYY. The parser now
reads it (for a year next to the reference date). Rerun the same day: `ok`, "page-images on
https://www.stannedavidsvillepa.org/services: first-listed, dated 2026-10-11", the 600×988 Wix
rendition of `10112026.jpg` (the 12–18 October sheet). The image is small; whether the pipeline
reads its Mass times well is to be seen on its first run.

## Not yet confirmed

Whether the bulletin image is replaced every week on the same page (the 11 October file name
suggests it is). Check the page again after 25 October.
