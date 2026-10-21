---
name: Our Lady of the Alleghenies Parish, Lilly
website: https://www.oloalilly.org
bulletin_provider: parishes_online
provider_id: our-lady-of-the-alleghenies-church
publication: ['po-org:our-lady-of-the-alleghenies-church', 'lpi:0018000000QxAmWAAV', 'po-container:14/1731']
group: Rev. Matthew Reese (Lilly)
evidence:
- url: https://container.parishesonline.com/bulletins/14/1731/20261018B.pdf
  seen: 2026-10-21
  quote: 608 MAIN STREET LILLY, PA 15938
  note: 'Page 1 masthead of the 18 October 2026 issue (the issue fetch:check picked): names Our Lady of the Alleghenies alone; "Saturday | 4:00pm (Vigil)", Sunday 8:00am and 10:00am, "FATHER MATTHEW REESE, PASTOR". The same text (probe pdf --grep) finds no mention of Dysart or Frugality, so it carries this parish only.'
- url: https://parishesonline.com/organization/our-lady-of-the-alleghenies-church
  seen: 2026-10-21
  note: 'probe po 0018000000QxAmWAAV: org "Our Lady of the Alleghenies Church", 608 Main St, Lilly, website https://www.oloalilly.org, publication ids po-org:our-lady-of-the-alleghenies-church, lpi:0018000000QxAmWAAV, po-container:14/1731, latest issue 2026-10-18 and weekly back to at least 2026-09-13.'
- url: https://www.oloalilly.org/bulletins
  seen: 2026-10-21
  note: 'probe url https://oloalilly.org: HTTP 200, final URL https://www.oloalilly.org/ (Duda site), embeds lpi:0018000000QxAmWAAV and links /bulletins. The parish site and ParishesOnline are one bulletin.'
- url: https://www.dioceseaj.org/clergy/
  seen: 2026-10-21
  quote: Reese, Rev. Matthew
  note: 'Clergy page lists him with Our Lady of the Alleghenies Parish, Lilly - Pastor, and no other parish (Rev. Robert Reese, a different priest, has Dysart and Frugality). So Lilly has no pastor-sharing neighbour whose bulletin could carry it.'
---

## Publisher

Our Lady of the Alleghenies Parish, Lilly publishes its own weekly bulletin through ParishesOnline (container 14/1731). The 18 October 2026 issue (page 1) is headed "OUR LADY OF THE ALLEGHENIES ROMAN CATHOLIC PARISH, 608 MAIN STREET LILLY, PA 15938", with "Saturday | 4:00pm (Vigil)", Sunday 8:00am and 10:00am, Monday to Saturday 8:00am, and "FATHER MATTHEW REESE, PASTOR". It names no other church, and a text search finds no Dysart or Frugality in it. The pastor is Fr. Matthew Reese; the similarly named Fr. Robert Reese is a different priest who serves Dysart and Frugality (clergy page), whose parishes are in separate rows.

## Worship sites

One church, Our Lady of the Alleghenies, 608 Main St, Lilly (churches/our-lady-of-the-alleghenies-lilly), from the masthead, the directory and GCatholic 23857. The diocese lists no second church for this parish.

## Website and bulletin provider

`parishes_online`, `provider_id: our-lady-of-the-alleghenies-church`. The parish's Duda site www.oloalilly.org embeds the same ParishesOnline organization (lpi:0018000000QxAmWAAV) and links its bulletins page. `pnpm fetch:check` (2026-10-21) picked https://container.parishesonline.com/bulletins/14/1731/20261018B.pdf, the 18 October 2026 issue: ok. `probe container 14/1731` showed a 25 October 2026 issue already posted on 21 October.

## Not yet confirmed

Nothing.
