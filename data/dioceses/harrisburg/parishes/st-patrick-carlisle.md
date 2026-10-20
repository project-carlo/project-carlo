---
name: Saint Patrick Catholic Church
website: https://www.saintpatrickchurch.org/
bulletin_provider: parishes_online
provider_id: st-patrick-church-17013
publication: ['po-org:st-patrick-church-17013', 'lpi:0018000000Qc2KcAAJ', 'po-container:04/0437']
group: ''
evidence:
- url: https://container.parishesonline.com/bulletins/04/0437/20261018B.pdf
  seen: 2026-10-19
  quote: Sunday | 8 am Shrine,9:30 & 11:30 am PAC Gym, 7:30 pm Dickinson
  note: 'Page 1 of the 18 October 2026 issue: "SAINT PATRICK CATHOLIC CHURCH"; Weekend Masses "Saturday
    | 8:30 a.m. Shrine, 5:15 pm PAC Gym; Sunday | 8 am Shrine, 9:30 & 11:30 am PAC Gym, 7:30 pm
    Dickinson"; Weekday Masses Monday and Tuesday 8:30 am Shrine, Wednesday and Thursday 8:30 am PAC
    Classrooms, Friday 8:30 am PAC Gym; "Shrine & Parish Office 152 E. Pomfret Street, Carlisle, PA
    17013"; "Marsh Drive & Parish Activity Ctr. 85 Marsh Drive, Carlisle, PA 17015"; "Dickinson Campus,
    Allison Great Hall, Carlisle, PA".'
- url: https://container.parishesonline.com/bulletins/04/0437/20261018B.pdf
  seen: 2026-10-19
  quote: Adoration Chapel, 140 E. Pomfret Street
  note: Page 3, "Saint Katharine Drexel Perpetual Adoration Chapel" (adoration only).
- url: https://container.parishesonline.com/bulletins/04/0437/20260830B.pdf
  seen: 2026-10-19
  quote: PAC Gym, 11:30 am ERC
  note: 'Page 1 of the 30 August 2026 issue: the summer schedule adds "11:30 am ERC" on Sundays (St.
    Eleanor Regina Chapel); the same line is in the 24 May, 19 July (image), 23 August and 6 September
    issues and not in the 18 October one.'
- url: https://www.saintpatrickchurch.org/bulletins
  seen: 2026-10-19
  note: The parish site's "Weekly Bulletin" page embeds the LPi publication widget
    parishesonline.com/publicationWidget?type=bulletin&id=0018000000Qc2KcAAJ; probe po gives org
    st-patrick-church-17013 ("Saint Patrick Church", 152 E Pomfret St, Carlisle), container 04/0437,
    newest issue 18 October 2026.
---

## Publisher

Saint Patrick, Carlisle publishes one weekly bulletin through LPi/ParishesOnline for all its
worship sites. I read the 18 October 2026 issue: page 1 is the parish's own cover with the
whole Mass schedule, keyed by place ("Shrine", "PAC Gym", "PAC Classrooms", "Dickinson"),
and the addresses of the Shrine and parish office (152 E. Pomfret Street), the Marsh Drive
campus and Parish Activity Center (85 Marsh Drive) and the Dickinson campus (Allison Great
Hall). The LPi footer on its advertising pages reads "St. Patrick Church, Carlisle, PA 04-0437".

## Worship sites

- Marsh Drive church / Parish Activity Center, 85 Marsh Drive (`st-patrick-marsh-drive-carlisle`):
  Saturday 5:15 pm, Sunday 9:30 and 11:30 am in the "PAC Gym", weekday Masses in the PAC.
  The diocese and the parish site call it the "Marsh Drive Church".
- Shrine church, 152 E. Pomfret Street (`st-patrick-shrine-carlisle`, GCatholic's "St.
  Patrick Shrine", gcatholic:23801): the historic downtown church, Saturday 8:30 a.m.,
  Sunday 8 am, Monday and Tuesday 8:30 am.
- Allison Hall, Dickinson College (`allison-hall-dickinson-college-carlisle`): Sunday
  7:30 pm, the Dickinson College Catholic Campus Ministry Mass ("DCCM" in the intentions),
  in "Allison Great Hall" (October) or "Allison Interfaith Chapel" (July, August).
- St. Eleanor Regina Chapel, Pine Grove Furnace State Park
  (`st-eleanor-regina-chapel-pine-grove-furnace`): Sunday 11:30 am from Memorial Day to Labor
  Day only ("ERC" in the summer issues).

The Saint Katharine Drexel Perpetual Adoration Chapel, 140 E. Pomfret Street, has adoration
only and is not a Mass site.

## Website and bulletin provider

saintpatrickchurch.org's Bulletins page embeds the LPi widget for organization id
0018000000Qc2KcAAJ; `probe po` gives the org slug `st-patrick-church-17013` and container
04/0437 with weekly issues through 18 October 2026. Provider `parishes_online` with that
slug. Discover Mass has an empty page for the parish (`st-patrick-parish-carlisle-pa`, no
issues).

Fetch check (2026-10-20, `fetch_check.check_fetch` on a temporary CSV): ok, the 18 October 2026 issue (container 04/0437, 43.8 MB) on the second run; the first run's download came back as a 1,169-byte non-PDF, a transient failure through the proxy.

## Not yet confirmed

- Whether the Sunday Masses are in the gym because a new Marsh Drive church is still being
  built; the bulletin only says "PAC Gym". The address and coordinates are the Marsh Drive
  campus's either way.
- The Dickinson Mass runs in the academic year; the bulletin gives no dates.
