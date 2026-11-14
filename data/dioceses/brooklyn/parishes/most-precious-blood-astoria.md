---
name: Most Precious Blood (Astoria)
website: https://www.mpbastoria.com/
bulletin_provider: unsupported
provider_id: ''
publication: []
group: Deanery Q1 (Queens West)
evidence:
- url: https://www.mpbastoria.com/mpb-bulletin
  seen: 2026-11-06
  quote: Read online our newest bulletin
  note: 'Wix page ''Weekly Bulletins'', LATEST BULLETIN slideshow ''1/4'' (rendered with parish-site-access
    visit.py; screenshot). Slide 1 (image 80633a_5ef211c290124a7f95a1df5ad147f642~mv2.jpg) is the cover:
    ''MOST PRECIOUS BLOOD ROMAN CATHOLIC CHURCH'', ''Rectory: 32-23 36th St., NY 11106'', ''Thirty Second
    Sunday in Ordinary Time'', ''November 8, 2026''. The slides are images, so recheck can''t find their
    words.'
- url: https://static.wixstatic.com/media/80633a_0814aaee3f2b4fa9aa1929e3917777c0~mv2.jpg
  seen: 2026-11-06
  note: 'Slide 2 of the 8 November 2026 issue (image): Pastoral Staff, Pastor Father Christopher M. O''Connor;
    Mass Schedule Sunday 8:00 am (English), 9:30 am (Espanol), 11:00 am (Croatian), 12:30 pm (English),
    5:00 pm (English; 1st Sunday Tagalog); Saturday 8:30 am and 5:30 pm; Monday-Friday 8:30 am and 12:15pm,
    7:00pm Espanol Wednesday. Mass intentions for 8-15 November at those times; Weekly Sunday Collection
    November 1, 2026. No other church or chapel is named.'
- url: https://parishesonline.com/organization/most-precious-blood-church-11106
  seen: 2026-11-06
  note: 'probe po: ''Most Precious Blood Church'', 3216 36th St, website mpbastoria.com, lpi 0018000000QxB6cAAF,
    but no issues (''this organization does not publish a bulletin here now''): an empty org, not a publication
    id.'
research:
- method: parish-site-access visit.py and tools/frames-requests.py on the Wix bulletin page; fetch:check
    with page-pdfs and page-images recipes
  url: https://www.mpbastoria.com/mpb-bulletin
  checked: '2026-11-06'
  outcome: unsupported-format
  next_action: When a collector reads a Wix image slideshow as one multi-page issue (or the parish posts
    PDFs), set provider other with its recipe, run fetch:check and clear the fetch_gap
  retry_when: A collector for Wix image slideshows lands, or the page links a PDF
bulletin_status: unsupported-format
fetch_gap:
  kind: wix-image-slideshow
  seen: 2026-11-06
  note: The Wix page /mpb-bulletin shows the current issue only as a slideshow of page JPEGs on static.wixstatic.com
    (80633a_<hash>~mv2.jpg, empty alt, no date or 'bulletin' in name or text), no PDF and no dated links;
    fetch:check with page-pdfs found 'No PDF links found', and page-images would take one undated picture
    per issue, not a 4-page issue. The 'PREVIOUS BULLETINS' section rendered empty.
  url: https://www.mpbastoria.com/mpb-bulletin
---

## Publisher

Most Precious Blood, Astoria (Long Island City postal area) publishes its own weekly bulletin, posted on its Wix site only as page images. The page https://www.mpbastoria.com/mpb-bulletin (rendered 2026-11-06 with parish-site-access) shows LATEST BULLETIN as a 4-slide slideshow; slide 1 is the cover of the 8 November 2026 issue, "MOST PRECIOUS BLOOD ROMAN CATHOLIC CHURCH", "Rectory: 32-23 36th St., NY 11106", "Thirty Second Sunday in Ordinary Time". Slide 2 gives the staff (Pastor Father Christopher M. O'Connor) and the Mass schedule. A ParishesOnline org exists (`most-precious-blood-church-11106`, lpi 0018000000QxB6cAAF) but holds no issues, so it is not a publication id.

## Worship sites

One. Slide 2's "Mass Schedule" gives Sunday 8:00 am (English), 9:30 am (Spanish), 11:00 am (Croatian), 12:30 pm (English), 5:00 pm (English; 1st Sunday Tagalog), Saturday 8:30 am and 5:30 pm, Monday-Friday 8:30 am and 12:15 pm, Wednesday 7:00 pm Spanish, with no other church or chapel; the intentions for 8-15 November are at those times. The directory, the deanery list, GCatholic 16624 and Mass finder 1125 give the one church at 32-23 36th Street.

## Website and bulletin provider

`unsupported`, fetch gap `wix-image-slideshow`. The diocese directory links https://www.mpbastoria.com/ (the job note that the directory gives no website did not match the roster row read on 2026-11-06). The bulletin page has no PDF and no dated link: each page is a `static.wixstatic.com` JPEG with an empty alt and a hash name. `fetch:check` with `page-pdfs` reported "No PDF links found"; `page-images` needs a dated or 'bulletin'-labelled picture and would take one image per issue. No publication id: the issue is self-published and the ParishesOnline org is empty.

## Not yet confirmed

Slides 3 and 4 were not read (slide 2 holds the schedule). Whether past issues are kept anywhere (the PREVIOUS BULLETINS section rendered empty); see research.
