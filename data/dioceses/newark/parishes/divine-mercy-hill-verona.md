---
name: Divine Mercy Hill (Salvatorians), Verona
website: https://www.veronasds.com/
bulletin_provider: other
provider_id: page-pdfs https://www.veronasds.com/ filename=Ogloszenia*.pdf
publication: ['url:https://www.veronasds.com/']
group: ''
evidence:
- url: https://www.veronasds.com/word/Ogloszenia%20Listopad%202026%20good.pdf
  seen: 2026-11-03
  quote: Ogłoszenia ze Wzgórza Miłosierdzia
  note: 'November 2026 issue (2 pages, Polish, text layer). Page 1 masthead: ''Posługę duszpasterską na
    Wzgórzu Miłosierdzia w Veronie pełnią SALWATORIANIE, SDS, 23 Crestmont Rd; Verona, NJ 07044''. Page
    2 ''Msze Święte'': ''Weekend: Sobota o godzinie 5:00 pm Niedziela o godzinie 8:00 am i 11:00 am'';
    ''W listopadzie od poniedziałku do piątku Msze św poranne o godzinie 8:00 am''; first Friday 7:00
    pm Mass; All Saints 1 November 8:00 and 11:00 am; 2 November 8:00 am and 7:00 pm.'
- url: https://www.veronasds.com/
  seen: 2026-11-03
  quote: Gazetka na listopad jest dostępna w sekcji
  note: 'Homepage of the Salwatorianie w Veronie, 23 Crestmont Road, Verona: ''Formularze do pobrania''
    lists ''Gazetka na listopad .pub .pdf'' (word/Ogloszenia Listopad 2026 good.pdf) and older forms (Gazetka
    Wielki Post 2026, Nowenna Swiety Jozef 2026, Mass-offering forms). Mass schedule: ''Sobota: 5:00pm
    (z niedzieli) Niedziela: 8:00am i 11:00am'', weekdays Monday-Friday 8:00am.'
revisit: Confirm the December 2026 newsletter is named Ogloszenia* and picked by fetch:check.
revisit_after: 2026-12-07
research:
- method: fetch:check with page-pdfs on the homepage filtered to Ogloszenia*.pdf
  url: https://www.veronasds.com/
  checked: '2026-11-03'
  outcome: found
  next_action: After 1 December 2026, check that the homepage links a December 'Ogloszenia' file and that
    fetch:check picks it rather than an older one
  revisit_after: 2026-12-07
bulletin_status: available
---

## Publisher

The Polish Salvatorian community (Society of the Divine Savior, SDS) at Divine Mercy Hill ('Wzgórze Miłosierdzia'), 23 Crestmont Road, Verona, publishes a monthly two-page newsletter in Polish, 'Ogłoszenia ze Wzgórza Miłosierdzia' (the homepage calls it 'Gazetka na listopad'), with its Mass schedule. I read the November 2026 issue: page 1 masthead names the Salvatorians at Divine Mercy Hill, 23 Crestmont Rd, Verona; page 2 gives Saturday 5:00 pm, Sunday 8:00 and 11:00 am, and Monday-Friday 8:00 am. It is the only bulletin of this place, which is not a canonical parish (GCatholic 47767 lists it as a monastery; the archdiocese's parish directory does not list it), so it is its own row.

## Worship sites

- Divine Mercy Hill, 23 Crestmont Road, Verona (`divine-mercy-hill-verona`): Saturday 5:00 pm; Sunday 8:00, 11:00 am; Monday-Friday 8:00 am; first Friday 7:00 pm (November 2026 newsletter and homepage, both in Polish).

## Website and bulletin provider

https://www.veronasds.com/ (a hand-built static site in Polish) links each month's newsletter from its 'Formularze do pobrania' box, as word/Ogloszenia <Month> <Year> good.pdf beside a .pub copy, together with standing forms (Mass offerings, novenas) and a Lent newsletter named 'Gazetka Wielki Post 2026.pdf'. Provider `other` with `page-pdfs https://www.veronasds.com/ filename=Ogloszenia*.pdf` so only the monthly newsletter is picked.

Fetch check (2026-11-03, headed): transport ok, PDF, resolved `page-pdfs on https://www.veronasds.com/: first-listed` and picked word/Ogloszenia Listopad 2026 good.pdf, the November 2026 issue read above. Issue date and freshness `unknown`: the file name and text give the month in Polish ('Listopad 2026'), which fetch doesn't read. The issue is monthly, so a 14-day freshness window won't fit it.

## Not yet confirmed

Whether the next month's file keeps the 'Ogloszenia' prefix (the Lent issue was named 'Gazetka'); see `revisit_after` 2026-12-07.
