---
name: St. Luke the Evangelist Parish
website: https://www.stlukelivingstoncounty.org
bulletin_provider: parishes_online
provider_id: st-luke-the-evangelist
publication:
- po-org:st-luke-the-evangelist
- lpi:0018000000Qc2bOAAR
- po-container:06/0103
group: ''
evidence:
- url: https://container.parishesonline.com/bulletins/06/0103/20261004B.pdf
  seen: '2026-10-02'
  quote: St. Luke the Evangelist, Geneseo, NY 06-0103
  note: '4 October 2026 issue, page 6 (the only page with a text layer): LPi container 06-0103, "St. Luke the Evangelist,
    Geneseo, NY". Pages 1-5 are images.'
- url: https://container.parishesonline.com/bulletins/06/0103/20260927B.pdf
  seen: '2026-10-02'
  note: '27 September 2026 issue, page 1 (image, read with render.py). Masthead: "St. Luke the Evangelist Catholic
    Parish Central Office: 13 North Street Geneseo, NY 14454 ... www.stlukelivingstoncounty.org Parochial Administrator:
    Rev. Daniel L. White", then the sites "Holy Angels 45 N Church Street Nunda, NY / St. Lucy 2770 Retsof Avenue
    Retsof, NY / St. Mary 4 Avon Road Geneseo, NY / St. Patrick 46 Stanley Street Mt. Morris, NY / Diocese of Rochester
    Migrant Ministry St. Juan Diego Community 175 Main Street Leicester, NY / Newman Community SUNY Geneseo Interfaith
    Center 11 Franklin Street Geneseo, NY". Page 2 Mass intentions use codes SL, HA, SP, SM, SJDC.'
- url: https://www.stlukelivingstoncounty.org/
  seen: '2026-10-02'
  quote: 'Saturday Vigil: 4:00 pm at St. Lucy 5:45 pm at Holy Angels Sunday: 8:30 am at St. Patrick 10:00am at St.
    Mary Weekdays: Monday - 8:00am at St. Mary Tuesday - 8:00am at St. Patrick Wednesday - 5:30pm at Holy Angels'
  note: Parish home page, Mass Times (also Thursday 8:00am at St. Juan Diego Community).
- url: https://www.stlukelivingstoncounty.org/
  seen: '2026-10-02'
  quote: Bulletin
  note: The home page's Bulletin link goes to https://parishesonline.com/organization/st-luke-the-evangelist. `probe
    url` finds po-org:st-luke-the-evangelist on the page; `probe po` gives lpi:0018000000Qc2bOAAR and container
    06/0103, weekly issues through 2026-10-04.
- url: https://ps.dor.org/directory/st-luke-the-evangelist-parish/
  seen: '2026-10-02'
  quote: a multi-site parish, Geneseo, New York, Livingston County
  note: 'Diocesan Directory of Parishes (updated 1/27/25): one multi-site parish with St. Mary, St. Lucy, Holy Angels,
    St. Patrick and St. Juan Diego Community (formerly St. Thomas Aquinas).'
- url: https://www.dor.org/learning-and-living-your-faith/sacraments/sacramental-records/
  seen: '2026-10-02'
  note: 'Sacramental-records index: Assumption (Mount Morris), Holy Angels (Nunda), Holy Name of Jesus (Groveland),
    St. Lucy (Retsof), St. Mary (Geneseo), St. Patrick (Mount Morris), St. Raphael (Piffard), St. Thomas Aquinas
    (Leicester) and Santa Maria de Mercede (Cuylerville) all keep records at St. Luke the Evangelist, Geneseo. Corporations
    merged, not buildings.'
promoted: 2026-10-02
---

## Publisher

St. Luke the Evangelist Parish, Geneseo, one multi-site parish with one weekly bulletin on ParishesOnline (LPi container 06/0103). The 27 September 2026 masthead (an image page) is headed "St. Luke the Evangelist Catholic Parish", gives the Central Office at 13 North Street, Geneseo, and lists the parish's sites: Holy Angels (Nunda), St. Lucy (Retsof), St. Mary (Geneseo), St. Patrick (Mt. Morris), St. Juan Diego Community (Leicester) and the Newman Community at the SUNY Geneseo Interfaith Center. The diocese groups nothing else with it.

## Worship sites

Five churches, each with a Mass in the current schedule: `st-mary-geneseo` (Sunday 10:00, Monday 8:00), `st-patrick-mount-morris` (Sunday 8:30, Tuesday 8:00), `st-lucy` (Saturday 4:00), `holy-angels` (Saturday 5:45, Wednesday 5:30) and `st-juan-diego-community` (Thursday 8:00; formerly St. Thomas Aquinas, Leicester). The Locator's two "St. Thomas Aquinas" entries (one placed at Geneseo with "No Mass", one at Leicester) are the Leicester church under its old name, linked to `st-juan-diego-community`.

Not here: the Newman Community at the Interfaith Center, 11 Franklin Street (`open/newman-community-suny-geneseo`: a weekly Thursday Mass is claimed by the university's page but by no parish source). The sacramental-records index lists nine more merged corporations (Assumption in Mount Morris, Holy Name of Jesus in Groveland, St. Raphael in Piffard, Santa Maria de Mercede in Cuylerville, ...). None appears in the Mass schedule on the site or the bulletin; I did not look for separate closure sources for them and they are in none of my region's rosters beyond what is recorded here.

## Website and bulletin provider

stlukelivingstoncounty.org is the parish's site (Our Sunday Visitor); its Bulletin link goes to the ParishesOnline organization `st-luke-the-evangelist`, so `provider_id` is that slug and `publication` has all three forms (po-org, lpi, container 06/0103) from `probe po`. Issues are posted a week ahead (4 October 2026 exists on 2 October). **The weekly PDF is mostly images**: pages 1-5 of the 4 October issue have no text layer (only the LPi ad page 6 does), so the pipeline will need to read them as images; the 27 September pages 1-3 were drawn with render.py.

## Not yet confirmed

Whether St. Juan Diego also has a Friday 8am Mass (the diocese directory says Thursday and Friday; the parish site and bulletin say Thursday only). Whether the Newman Thursday Mass is held (see the open record, revisit 2026-11-15).
