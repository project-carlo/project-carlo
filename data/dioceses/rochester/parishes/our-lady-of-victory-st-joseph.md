---
name: Our Lady of Victory / St. Joseph
website: https://olvsj.org
bulletin_provider: google_drive
provider_id: drive-folder https://drive.google.com/drive/folders/1GKyckPYyKi9TbK14Qli16e-iV8sJYuhd?usp=sharing
publication:
- url:https://drive.google.com/drive/folders/1GKyckPYyKi9TbK14Qli16e-iV8sJYuhd
group: ''
evidence:
- url: https://drive.google.com/uc?export=download&id=1LdcErV26yow8rjtS18K-yW5DXaoEBnaZ
  seen: '2026-10-02'
  quote: 'Weekend Masses: Saturday: 4:30 P.M. &'
  note: '"Sunday: 10:00 A.M. / Weekday Masses: Mon. - Wed. & Fri. 12:10 P.M." The bulletin is a single
    page, "September 27, 2026", "Our Lady of Victory/St Joseph, 210 Pleasant St." (the file is "Sept.
    27, 2026.pdf" in the parish Drive folder, read via drive.google.com/uc?export=download).'
- url: https://www.olvsj.org/
  seen: '2026-10-02'
  quote: BULLETINS
  note: The home page nav has a "BULLETINS" button that links the shared Google Drive folder https://drive.google.com/drive/folders/1GKyckPYyKi9TbK14Qli16e-iV8sJYuhd
    (read with visit.py --links). The folder lists "Sept. 27, 2026.pdf", "Sept. 20, 2026.pdf", "September
    13, 2026.pdf", "September 6, 2026.pdf" and an Archive folder (read via drive.google.com/embeddedfolderview).
- url: https://www.olvsj.org/
  seen: '2026-10-02'
  quote: 'Weekend Masses: Saturday: 4:30 PM, Sundays 10:00 AM'
- url: https://ps.dor.org/directory/our-lady-of-victory-st-joseph/
  seen: '2026-10-02'
  quote: 'Weekend Masses: Saturday: 4:30 PM, Sundays 10:00 AM'
promoted: 2026-10-02
---

## Publisher

Our Lady of Victory / St. Joseph publishes a one-page bulletin as a PDF dropped into a shared Google Drive folder. The 27 September 2026 file gives the Mass intentions for 26 September to 4 October, the parish address (210 Pleasant St.) and the schedule: Saturday 4:30 pm, Sunday 10:00 am, weekdays Monday to Wednesday and Friday 12:10 pm. Pastor Fr. Ronald Antinarelli. It names no other parish.

## Worship sites

One: `churches/our-lady-of-victory-st-joseph.md` (210 Pleasant Street, "The Little French Church"). The parish was joined with St. Joseph, whose 1843 building at 108 Franklin Street was destroyed in 1974 (GCatholic 38891), recorded in `excluded/st-joseph-franklin-street-rochester.md`. The sacramental-records index lists "St. Joseph, Rochester" under this parish.

## Website and bulletin provider

`olvsj.org` (redirects to `www.olvsj.org`) links the Drive folder from its "BULLETINS" button, which is what the live `google_drive` provider needs (the website has to link the folder). Provider unchanged. Drive does not show the files without a browser; the folder is public.

Fetch recipe `drive-folder https://drive.google.com/drive/folders/1GKyckPYyKi9TbK14Qli16e-iV8sJYuhd?usp=sharing`, pinned 2026-10-03: on the pages recorded in `tests/fixtures/fetch/our-lady-of-victory-st-joseph.json.gz` the resolver found https://drive.google.com/file/d/16rZZ-DBeNg8cYlv7A5OBlZuVWdEIWvGh/view this way, dated that week.

## Not yet confirmed

Nothing.
