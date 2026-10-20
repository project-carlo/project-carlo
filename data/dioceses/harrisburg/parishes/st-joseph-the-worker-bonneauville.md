---
name: Saint Joseph the Worker
website: http://stjosephtheworkerpa.org/
bulletin_provider: other
provider_id: dated-post http://stjosephtheworkerpa.org/bulletin/
publication: ['url:http://stjosephtheworkerpa.org/bulletin/']
group: ''
evidence:
- url: http://stjosephtheworkerpa.org/wp-content/uploads/2026/10/10182026.pdf
  seen: 2026-10-19
  quote: Saint Joseph the Worker Bonneauville, Pennsylvania
  note: The 18 October 2026 issue (6 pages). Page 1 cover "World Mission Sunday ... Saint Joseph the Worker
    Bonneauville, Pennsylvania" (a Bon Venture template, "©2018 Bon Venture Services, LLC"); page 2 "ST.
    JOSEPH THE WORKER CHURCH" mission statement and Mass intentions; last page "A53101 (CK) - St. Joseph
    the Worker, Gettysburg ... BON VENTURE, LLC".
- url: http://stjosephtheworkerpa.org/wp-content/uploads/2026/10/10182026.pdf
  seen: 2026-10-19
  quote: Please notify Fr. Benny 717-334-2510
- url: http://stjosephtheworkerpa.org/
  seen: 2026-10-19
  note: The homepage serves a "One moment, please..." page that reloads itself after 5 seconds (a WordPress
    bot check); in a browser left to wait it shows "Bulletins October 18, 2026, October 11, 2026 ..."
    links to /notice/<date>/ posts, each embedding the PDF with PDF Embedder. The PDF files themselves
    download without the check. Found the file names from the site's /wp-json/wp/v2/media listing.
---

## Publisher

St. Joseph the Worker, 12 East Hanover Street, Bonneauville publishes its own weekly
bulletin; Bon Venture prints it (ad pages, client code A53101) and the parish posts the PDF on
its WordPress site. I read the 18 October 2026 issue: the cover names "Saint Joseph the
Worker, Bonneauville, Pennsylvania", page 2 lists the Mass intentions (Saturday 4:30 pm,
Sunday 8:00 and 10:30 am) and asks parishioners to notify "Fr. Benny" (Rev. Benny Jose, the
pastor in the diocesan directory). No partner parish.

## Worship sites

- St. Joseph the Worker, 12 E Hanover St, Bonneauville (postal Gettysburg)
  (`st-joseph-the-worker-bonneauville`).

## Website and bulletin provider

The site posts each issue as a "notice" post (`/notice/october-18-2026/`) that embeds
`wp-content/uploads/<y>/<m>/<MMDDYYYY>.pdf`; the homepage and `/bulletin/` list the posts.
HTML pages sit behind a "One moment, please..." bot check that clears in a real browser
after one reload; the PDFs are not behind it. Bon Venture's sponsor site was not checked
for a copy.

Fetch check (2026-10-20): `dated-post on http://stjosephtheworkerpa.org/bulletin/:
first-listed`, picking `.../2026/10/10182026.pdf`, this week's issue (checked by hand), so
the printed recipe `dated-post http://stjosephtheworkerpa.org/bulletin/` is pinned.

## Not yet confirmed

Nothing.
