---
name: St. Mary and Sacred Heart Parishes
website: https://thesmchurch.com
bulletin_provider: parishes_online
provider_id: st-mary-sacred-heart-churches
publication: ['po-org:st-mary-sacred-heart-churches', 'lpi:0018000000Qc2AnAAJ', 'po-container:14/0966']
group: St. Mary and Sacred Heart partnership, St. Marys (decree 2023-09-20)
evidence:
- url: https://container.parishesonline.com/bulletins/14/0966/20261025B.pdf
  seen: 2026-10-23
  quote: Staffed by the Benedictine Monks of Saint Vincent Archabbey
  note: '25 October 2026 issue (8 pages; posted early). Page 2 Mass schedule: ''LORD''S DAY Saturday SM
    4:30PM; Sunday SH 7:00AM SM 9:00AM SH 10:30AM''; ''DAILY MASS SH (Mon-Wed-Fri) 6:15AM, SM (Tues-Thur-Sat)
    8:30AM''; page 3 ''SH & SM MASS INTENTIONS'' tags every Mass (SM)/(SH); page 4 has ''SACRED HEART
    NEWS'' and ''ST. MARY''S NEWS'' columns under one ''SACRED HEART & ST. MARY''S ST. MARYS, PA'' calendar.
    Page 8 footer: ''St. Mary & Sacred Heart Churches, St. Marys, PA 14-0966''.'
- url: https://sacredheartparish.us/bulletins.html
  seen: 2026-10-23
  note: 'Sacred Heart''s own Bulletins page (static HTML, title ''Sacred Heart Church Bulletins: St. Marys,
    PA 15857''): its single ''Current Church Bulletin'' link is https://parishesonline.com/organization/st-mary-sacred-heart-churches,
    i.e. this same bulletin; the only other links are two archived issues (2015 and 2023-05-28, container
    14/0963). The page also embeds a widget.parishesonline.com publications iframe (id 32453635...) that
    returned 502 on 2026-10-23, so it was not read.'
- url: https://parishesonline.com/organization/sacred-heart-church-15857
  seen: 2026-10-23
  note: 'probe po sacred-heart-church-15857 (website www.sacredheartparish.us, container 14/0963, LPi
    0018000000Qc05JAAR): latest issue 2024-02-11, nothing since. Its 11 Feb 2024 issue (md5 aa142576...)
    is a Sacred Heart-only bulletin (''Sacred Heart Church Sunday - 7:00 & 10:30 a.m.'') different from
    St. Mary''s 14/0966 issue of the same date (md5 684a2790...; ''Partnered Parish with Sacred Heart
    Church''). By 14 Apr 2024 the 14/0966 issue carries ''SH & SM'' columns (18 Feb and 3 Mar 2024 do
    not), so the merge into one bulletin happened in March-April 2024.'
- url: https://www.eriercd.org/images/sections/bishop/pdf/Decree%20partnering%20Sacred%20Heart%20and%20St.%20Mary,%20St.%20Marys.pdf
  seen: 2026-10-23
  quote: This decree is effective September 20, 2023.
  note: 'Decree partnering Sacred Heart and St. Mary, St. Marys (images/sections/bishop/pdf/Decree partnering
    Sacred Heart and St. Mary, St. Marys.pdf): ''St. Mary Parish and Sacred Heart Parish, both in St.
    Marys, Pennsylvania, are to be partnered''; Rev. Thomas Curry, O.S.B. pastor of both.'
- url: https://thesmchurch.com/
  seen: 2026-10-23
  note: 'St. Mary''s site (WordPress; probe url finds po-org:st-mary-sacred-heart-churches). Mass times:
    ''Daily Mass: 6:15AM Monday, Wednesday and Friday at Sacred Heart Church; 8:30AM Tuesday, Thursday
    and Saturday at St. Mary''s Church''; ''SM (ST. MARY''S) Saturday 4:30 PM, 315 Church Street St. Marys,
    PA 15857''.'
research:
- method: probe po st-mary-sacred-heart-churches and sacred-heart-church-15857; probe pdf of 14/0966 25
    Oct 2026; md5 and masthead comparison of 14/0963 and 14/0966 for 11 Feb 2024; read sacredheartparish.us/bulletins.html
  url: https://parishesonline.com/organization/st-mary-sacred-heart-churches
  checked: '2026-10-23'
  outcome: found
  next_action: None; Sacred Heart's former separate org (14/0963) is silent since 2024-02-11.
- method: pnpm fetch:check --diocese erie --parish st-mary-sacred-heart-st-marys --expected-identity Mary
    (headed Chrome)
  url: https://container.parishesonline.com/bulletins/14/0966/20261025B.pdf
  checked: '2026-10-23'
  outcome: found
  next_action: None. Transport ok, PDF, 25 Oct 2026 issue; freshness 'future' (posted two days early),
    so overall 'unverified' for that reason only. Page 1 of the issue is an insert with no masthead text
    ('St. Mary's Church Convent Chapel October 27th'), so identity was matched on 'Mary'; the name 'St.
    Mary & Sacred Heart Churches ... 14-0966' is in the page 8 footer.
- method: widget.parishesonline.com/publications?id=32453635... embedded on sacredheartparish.us/bulletins.html
    (curl)
  url: https://sacredheartparish.us/bulletins.html
  checked: '2026-10-23'
  outcome: access-blocked
  next_action: Open the widget in the browser to see which org it lists; expected to be the same org as
    the page's 'Current Church Bulletin' link.
  retry_when: If the sacredheartparish.us widget turns out to list a container other than 14/0966 or 14/0963,
    split Sacred Heart into its own row.
publication_reviews:
- parish: queen-of-the-world-st-marys
  decision: separate
  evidence:
  - url: https://container.parishesonline.com/bulletins/14/1220/20261025B.pdf
    seen: 2026-10-23
    quote: Rev. Jeffery Noble, Pastor
    note: The 25 Oct 2026 Queen of the World issue's masthead names Queen of the World Church, 134 Queens
      Road, with Rev. Jeffery Noble, Pastor, and lists Mass Saturday 5:15 pm, Sunday 7:30 am and 10 am.
  - url: https://container.parishesonline.com/bulletins/14/0966/20261025B.pdf
    seen: 2026-10-23
    quote: Staffed by the Benedictine Monks of Saint Vincent Archabbey
    note: The same-date issue's page 8 masthead footer names St. Mary & Sacred Heart Churches; its page
      2 lists the Benedictine-staffed Sunday rota (SH 7:00, SM 9:00, SH 10:30) and shows no Queen of the
      World Mass schedule, so the two bulletins are different documents.
---

## Publisher

St. Mary Parish and Sacred Heart Parish, St. Marys, were partnered by decree effective 2023-09-20 under one Benedictine pastor (Rev. Thomas P. Curry, O.S.B., per the diocesan clergy list updated 8/7/2026: 'Pastor ... 1) St. Mary, St. Marys; 2) Sacred Heart, St. Marys'). They publish **one** bulletin: ParishesOnline org `st-mary-sacred-heart-churches`, container 14/0966 ('St. Mary & Sacred Heart Churches, St. Marys, PA 14-0966'). The 25 October 2026 issue, read 2026-10-23, carries one Mass schedule for both churches and a shared 'SH & SM' Mass-intentions table. Sacred Heart's own website (sacredheartparish.us) has a bulletins page of its own, but its current-bulletin link goes to the same ParishesOnline org, so the two sites are not two bulletins. Sacred Heart's former separate org (`sacred-heart-church-15857`, container 14/0963) stopped on 2024-02-11; the two were still separate documents that week (different md5) and merged into 14/0966 by April 2024. Hence one row for both parishes (README rule 1), with two churches.

## Worship sites

Two churches, both in the 25 Oct 2026 schedule: St. Mary's (Saturday 4:30 pm, Sunday 9:00 am, Tue/Thu/Sat 8:30 am) and Sacred Heart (Sunday 7:00 and 10:30 am, Mon/Wed/Fri 6:15 am). The bulletin also mentions a one-off event in the 'St. Mary's Church Convent Chapel' on 27 October 6:30-8 pm (RSVP); that is a single event, not a recurring Mass, and is not modelled. Queen of the World, St. Marys has its own pastor and bulletin (separate row).

## Website and bulletin provider

`parishes_online` with org slug `st-mary-sacred-heart-churches` as provider_id; website is St. Mary's thesmchurch.com, which names that org. The directory's own homepage entries are thesmchurch.com (St. Mary) and sacredheartparish.us (Sacred Heart); the latter is not used as a second row website because its bulletin is this one.

## Not yet confirmed

The widget embedded on sacredheartparish.us returned 502 when fetched, so which org it lists was inferred from the page's own link to the combined org (see research).
