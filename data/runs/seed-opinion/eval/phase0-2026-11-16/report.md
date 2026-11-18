# Seed second opinion, phase 0

gpt-6-luna read each approved seed's newest 2-4 bulletins blind; its schedule is compared with the approved slots (`seeding/opinion.py`). See docs/seed-second-opinion-plan.md.

- Parishes compared: 258; skipped: 8 (1 bulletin(s) with a stored PDF: 8); unparseable: 0
- Cost of these replies: $0.835 (median $0.0029 a parish)

## Differences per parish (grouped: a Mon-Fri difference is one)

| measure | total | median | parishes with none |
|---|---:|---:|---:|
| all kinds | 319 | 0 | 138 |
| all, but a settled R22-R26 exclusion counts as resolved | 317 | 0 | 140 |
| missing | 62 | 0 | 220 |
| extra | 182 | 0 | 172 |
| differs | 49 | 0 | 227 |
| excluded | 26 | 0 | 238 |
| question | 0 | 0 | 258 |

Ungrouped: 403 differences; 3548 of luna's entries agree with a slot (3846 included slots in all).

Distribution (counted differences, R22-R26 exclusions resolved):

- 0: 140 parishes
- 1: 50 parishes
- 2: 27 parishes
- 3: 12 parishes
- 4: 8 parishes
- 5: 7 parishes
- 6: 3 parishes
- 7: 2 parishes
- 8: 5 parishes
- 9: 2 parishes
- 10+: 2 parishes

## Every parish

| parish | bulletins | seed slots | agree | missing | extra | differs | excluded | question | cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| family-of-the-holy-cross-herkimer | 2 | 11 | 1 | 0 | 10 | 0 | 0 | 0 | $0.0007 |
| st-mary-of-the-assumption-oswego | 3 | 27 | 18 | 4 | 4 | 2 | 0 | 0 | $0.0042 |
| st-joseph-the-worker-west-winfield | 4 | 26 | 17 | 0 | 9 | 0 | 0 | 0 | $0.0033 |
| st-patricks-victor | 3 | 20 | 11 | 3 | 4 | 2 | 0 | 0 | $0.0045 |
| eternal-flame-catholic-community | 4 | 58 | 40 | 1 | 5 | 2 | 0 | 0 | $0.0065 |
| holy-spirit-hamilton | 4 | 20 | 13 | 1 | 7 | 0 | 0 | 0 | $0.0045 |
| mater-christi-albany | 2 | 24 | 16 | 0 | 8 | 0 | 0 | 0 | $0.0018 |
| st-anthony-of-padua-buffalo | 2 | 18 | 9 | 3 | 3 | 2 | 0 | 0 | $0.0020 |
| st-anthony-of-padua-syracuse | 2 | 13 | 5 | 0 | 4 | 4 | 0 | 0 | $0.0050 |
| holy-cross-dewitt | 2 | 16 | 12 | 3 | 4 | 0 | 0 | 0 | $0.0021 |
| spirit-of-hope-oneida | 4 | 15 | 14 | 6 | 1 | 0 | 0 | 0 | $0.0042 |
| our-lady-of-hope-whitehall | 4 | 31 | 27 | 2 | 1 | 3 | 0 | 0 | $0.0070 |
| st-mary-cortland | 4 | 19 | 14 | 1 | 5 | 0 | 0 | 0 | $0.0040 |
| transfiguration-syracuse | 2 | 40 | 35 | 1 | 4 | 1 | 0 | 0 | $0.0089 |
| catholic-family-cheektowaga | 4 | 40 | 37 | 0 | 2 | 1 | 2 | 0 | $0.0072 |
| holy-spirit-holy-trinity-gloversville | 4 | 20 | 10 | 1 | 4 | 0 | 0 | 0 | $0.0049 |
| most-holy-name-of-jesus | 3 | 18 | 15 | 2 | 3 | 0 | 0 | 0 | $0.0044 |
| sacred-heart-divine-mercy-cicero | 3 | 20 | 15 | 0 | 5 | 0 | 0 | 0 | $0.0027 |
| our-lady-of-the-lakes | 4 | 14 | 10 | 0 | 3 | 1 | 1 | 0 | $0.0034 |
| prince-of-peace-our-lady-of-good-counsel-endicott | 3 | 12 | 7 | 0 | 4 | 1 | 0 | 0 | $0.0036 |
| st-agnes-paul-rose | 4 | 12 | 9 | 0 | 3 | 0 | 2 | 0 | $0.0035 |
| assumption-syracuse | 2 | 6 | 4 | 2 | 1 | 0 | 1 | 0 | $0.0021 |
| bread-of-life-catholic-community | 4 | 70 | 67 | 1 | 3 | 0 | 0 | 0 | $0.0086 |
| blessed-trinity-st-patrick | 3 | 33 | 25 | 0 | 0 | 4 | 0 | 0 | $0.0041 |
| ss-columba-and-brigid-buffalo | 2 | 5 | 3 | 2 | 2 | 0 | 0 | 0 | $0.0014 |
| st-john-spencerport | 3 | 16 | 13 | 1 | 3 | 0 | 0 | 0 | $0.0033 |
| st-john-the-baptist-greenville | 4 | 14 | 11 | 1 | 2 | 1 | 0 | 0 | $0.0039 |
| st-marys-st-matthew | 3 | 9 | 6 | 2 | 2 | 0 | 0 | 0 | $0.0022 |
| sts-isidore-maria-torribia | 4 | 11 | 9 | 2 | 2 | 0 | 0 | 0 | $0.0027 |
| assumption-resurrection | 3 | 19 | 18 | 0 | 1 | 0 | 2 | 0 | $0.0044 |
| catholic-family-south-buffalo | 4 | 34 | 31 | 0 | 3 | 0 | 0 | 0 | $0.0066 |
| blessed-family-7-west-seneca | 3 | 29 | 27 | 1 | 2 | 0 | 0 | 0 | $0.0054 |
| christ-our-light-family | 4 | 33 | 24 | 0 | 0 | 3 | 0 | 0 | $0.0052 |
| holy-trinity-hudson | 4 | 15 | 12 | 0 | 2 | 1 | 0 | 0 | $0.0032 |
| holy-spirit-st-josephs | 3 | 29 | 28 | 2 | 1 | 0 | 0 | 0 | $0.0036 |
| light-of-christ-kenmore | 4 | 55 | 52 | 0 | 1 | 2 | 0 | 0 | $0.0074 |
| st-daniel-syracuse | 3 | 12 | 10 | 1 | 0 | 2 | 0 | 0 | $0.0039 |
| st-luke-schenectady | 3 | 11 | 9 | 1 | 2 | 0 | 0 | 0 | $0.0027 |
| st-peters-ontario-county | 4 | 16 | 13 | 0 | 0 | 3 | 0 | 0 | $0.0045 |
| twelve-apostles-catholic | 4 | 37 | 34 | 0 | 3 | 0 | 0 | 0 | $0.0053 |
| wheat-family-east-aurora | 4 | 43 | 40 | 0 | 3 | 0 | 0 | 0 | $0.0055 |
| christ-our-hope-boonville | 4 | 22 | 22 | 0 | 0 | 0 | 2 | 0 | $0.0037 |
| catholic-family-holy-rosary | 4 | 21 | 19 | 0 | 2 | 0 | 0 | 0 | $0.0026 |
| enchanted-mountains-catholic | 4 | 25 | 24 | 1 | 1 | 0 | 0 | 0 | $0.0068 |
| chautauqua-family-catholic | 4 | 35 | 33 | 0 | 1 | 1 | 0 | 0 | $0.0061 |
| christ-our-light-st-anne-pulaski | 3 | 16 | 14 | 0 | 2 | 0 | 0 | 0 | $0.0026 |
| good-shepherd-catholic-community | 4 | 16 | 14 | 0 | 1 | 1 | 0 | 0 | $0.0033 |
| hudson-valley-vicariate-west-catskill | 3 | 32 | 32 | 0 | 0 | 0 | 2 | 0 | $0.0040 |
| christ-the-king-albany | 3 | 11 | 9 | 0 | 2 | 0 | 0 | 0 | $0.0019 |
| central-niagara-catholic | 4 | 26 | 26 | 2 | 0 | 0 | 0 | 0 | $0.0056 |
| holy-spirit-sacred-heart-east-greenbush | 4 | 15 | 14 | 0 | 1 | 0 | 1 | 0 | $0.0037 |
| immaculate-heart-of-mary-watervliet | 2 | 6 | 5 | 0 | 1 | 0 | 1 | 0 | $0.0016 |
| our-lady-of-good-counsel-verona | 3 | 16 | 14 | 0 | 1 | 1 | 0 | 0 | $0.0020 |
| our-lady-queen-of-peace-st-thomas-more | 4 | 12 | 10 | 0 | 2 | 0 | 0 | 0 | $0.0029 |
| parish-of-the-holy-family | 2 | 18 | 17 | 0 | 0 | 1 | 1 | 0 | $0.0041 |
| st-augustine-baldwinsville | 3 | 3 | 2 | 1 | 1 | 0 | 0 | 0 | $0.0039 |
| st-clare-christ-our-light-colonie | 3 | 10 | 8 | 0 | 2 | 0 | 0 | 0 | $0.0020 |
| our-lady-of-victory-basilica | 4 | 25 | 24 | 1 | 0 | 1 | 0 | 0 | $0.0113 |
| st-edward-the-confessor-clifton-park | 3 | 13 | 12 | 0 | 1 | 0 | 1 | 0 | $0.0026 |
| our-lady-of-the-snow-saints-mary-and-martha | 4 | 26 | 25 | 1 | 1 | 0 | 0 | 0 | $0.0121 |
| st-joseph-st-patrick-utica | 3 | 2 | 2 | 2 | 0 | 0 | 0 | 0 | $0.0016 |
| st-francis-of-assisi-binghamton | 3 | 8 | 6 | 0 | 2 | 0 | 0 | 0 | $0.0032 |
| st-lawrence-otoole-and-sacred-heart | 3 | 25 | 17 | 0 | 2 | 0 | 0 | 0 | $0.0040 |
| st-kateri-tekakwitha | 4 | 13 | 12 | 0 | 0 | 1 | 1 | 0 | $0.0035 |
| st-malachy-sherburne | 3 | 8 | 8 | 2 | 0 | 0 | 0 | 0 | $0.0022 |
| st-luke-the-evangelist | 4 | 13 | 12 | 1 | 1 | 0 | 0 | 0 | $0.0030 |
| st-mary-nassau | 3 | 4 | 3 | 1 | 1 | 0 | 0 | 0 | $0.0023 |
| transfiguration-troy | 4 | 2 | 2 | 0 | 0 | 0 | 2 | 0 | $0.0022 |
| catholic-community-buffalo-north | 4 | 19 | 19 | 0 | 0 | 0 | 1 | 0 | $0.0057 |
| holy-trinity-webster | 2 | 19 | 18 | 0 | 1 | 0 | 0 | 0 | $0.0027 |
| holy-family-schuylerville | 4 | 18 | 17 | 0 | 1 | 0 | 0 | 0 | $0.0031 |
| beloved-disciples-lancaster | 4 | 45 | 45 | 0 | 0 | 0 | 1 | 0 | $0.0065 |
| holy-family-little-falls | 2 | 19 | 18 | 0 | 1 | 0 | 0 | 0 | $0.0025 |
| cattaraugus-creek-catholic | 4 | 17 | 16 | 0 | 1 | 0 | 0 | 0 | $0.0027 |
| corpus-christi-round-lake | 2 | 14 | 13 | 0 | 0 | 1 | 0 | 0 | $0.0029 |
| cathedral-st-mary-albany | 4 | 23 | 23 | 1 | 0 | 0 | 0 | 0 | $0.0040 |
| all-saints-corning | 2 | 6 | 6 | 0 | 0 | 0 | 1 | 0 | $0.0023 |
| holy-family-catholic-community | 4 | 11 | 10 | 0 | 1 | 0 | 0 | 0 | $0.0034 |
| blessed-trinity-buffalo | 2 | 8 | 7 | 0 | 1 | 0 | 0 | 0 | $0.0010 |
| historic-old-st-johns-utica | 2 | 13 | 12 | 0 | 1 | 0 | 0 | 0 | $0.0021 |
| all-saints-syracuse | 3 | 7 | 6 | 0 | 1 | 0 | 0 | 0 | $0.0029 |
| northern-points-cluster-st-cecilia-chestertown | 4 | 8 | 8 | 1 | 0 | 0 | 0 | 0 | $0.0031 |
| our-lady-of-fatima-shrine-lewiston | 4 | 40 | 39 | 0 | 1 | 0 | 0 | 0 | $0.0043 |
| niagara-frontier-catholic | 4 | 29 | 28 | 0 | 1 | 0 | 0 | 0 | $0.0052 |
| olg-ic-sj-glenville | 4 | 21 | 20 | 0 | 0 | 1 | 0 | 0 | $0.0055 |
| mary-mother-of-mercy | 3 | 9 | 8 | 0 | 1 | 0 | 0 | 0 | $0.0019 |
| liverpool-catholic-community | 4 | 27 | 26 | 0 | 1 | 0 | 0 | 0 | $0.0058 |
| lakeshore-catholic-faith-community | 4 | 39 | 32 | 0 | 1 | 0 | 0 | 0 | $0.0055 |
| niagara-falls-rc-family | 4 | 29 | 28 | 0 | 0 | 1 | 0 | 0 | $0.0044 |
| sacred-heart-stamford | 4 | 6 | 5 | 0 | 1 | 0 | 0 | 0 | $0.0021 |
| our-lady-queen-of-peace-rotterdam | 4 | 9 | 8 | 0 | 0 | 1 | 0 | 0 | $0.0023 |
| st-anthony-st-agnes-utica | 3 | 6 | 5 | 0 | 1 | 0 | 0 | 0 | $0.0015 |
| st-ann-manlius | 2 | 14 | 7 | 0 | 0 | 1 | 0 | 0 | $0.0017 |
| prince-of-peace-north-endicott | 4 | 17 | 16 | 0 | 1 | 0 | 0 | 0 | $0.0054 |
| saints-john-and-andrew-binghamton | 3 | 11 | 11 | 0 | 0 | 0 | 1 | 0 | $0.0039 |
| st-catherine-of-siena-ithaca | 3 | 8 | 7 | 0 | 1 | 0 | 0 | 0 | $0.0029 |
| st-francis-xavier-marcellus | 3 | 12 | 11 | 0 | 0 | 1 | 0 | 0 | $0.0021 |
| st-john-the-baptist-walton | 3 | 15 | 14 | 0 | 1 | 0 | 0 | 0 | $0.0017 |
| st-kateri-latin-mass-community | 2 | 8 | 3 | 0 | 1 | 0 | 0 | 0 | $0.0014 |
| st-jude-st-michael-wynantskill | 3 | 15 | 14 | 0 | 1 | 0 | 0 | 0 | $0.0022 |
| st-kateri-tekakwitha-niskayuna | 3 | 10 | 9 | 0 | 1 | 0 | 0 | 0 | $0.0025 |
| st-joseph-schenectady | 3 | 13 | 12 | 0 | 1 | 0 | 0 | 0 | $0.0029 |
| st-joseph-st-francis-broadalbin | 4 | 14 | 14 | 1 | 0 | 0 | 0 | 0 | $0.0032 |
| st-lawrence | 4 | 12 | 12 | 0 | 0 | 0 | 1 | 0 | $0.0033 |
| st-joseph-university-buffalo | 3 | 19 | 18 | 0 | 1 | 0 | 0 | 0 | $0.0034 |
| st-leo-the-great | 3 | 13 | 13 | 0 | 0 | 0 | 1 | 0 | $0.0034 |
| st-mary-our-mother | 3 | 9 | 9 | 1 | 0 | 0 | 0 | 0 | $0.0025 |
| st-mary-of-the-assumption-baldwinsville | 3 | 8 | 7 | 0 | 1 | 0 | 0 | 0 | $0.0032 |
| st-michael-the-archangel-south-glens-falls | 3 | 12 | 12 | 1 | 0 | 0 | 0 | 0 | $0.0030 |
| st-pauls-webster | 3 | 11 | 10 | 0 | 1 | 0 | 0 | 0 | $0.0047 |
| st-mary-crescent | 3 | 10 | 9 | 0 | 0 | 1 | 0 | 0 | $0.0041 |
| st-theodores-gates | 4 | 15 | 8 | 0 | 1 | 0 | 0 | 0 | $0.0022 |
| st-vincent-de-paul-albany | 3 | 4 | 3 | 0 | 1 | 0 | 0 | 0 | $0.0011 |
| st-paul-st-adalbert-mt-carmel-schenectady | 4 | 8 | 7 | 0 | 1 | 0 | 0 | 0 | $0.0032 |
| st-paul-whitesboro | 4 | 12 | 12 | 0 | 0 | 0 | 1 | 0 | $0.0044 |
| transfiguration-st-catherine-mendon | 3 | 11 | 10 | 0 | 1 | 0 | 0 | 0 | $0.0024 |
| st-rose-of-lima-north-syracuse | 3 | 10 | 10 | 1 | 0 | 0 | 0 | 0 | $0.0035 |
| three-catholic-sisters-foothills | 4 | 21 | 20 | 0 | 0 | 1 | 0 | 0 | $0.0085 |
| tonawanda-catholic | 4 | 37 | 36 | 0 | 1 | 0 | 0 | 0 | $0.0044 |
| the-lords-vineyard | 4 | 31 | 30 | 0 | 1 | 0 | 0 | 0 | $0.0047 |
| christ-the-good-shepherd-oswego | 4 | 16 | 16 | 0 | 0 | 0 | 0 | 0 | $0.0034 |
| ccncc-valatie | 3 | 9 | 9 | 0 | 0 | 0 | 0 | 0 | $0.0031 |
| christ-sun-of-justice-troy | 2 | 6 | 6 | 0 | 0 | 0 | 0 | 0 | $0.0008 |
| blessed-sacrament-albany | 2 | 14 | 14 | 0 | 0 | 0 | 0 | 0 | $0.0019 |
| all-saints-albany | 2 | 12 | 12 | 0 | 0 | 0 | 0 | 0 | $0.0026 |
| holy-trinity-utica | 3 | 14 | 14 | 0 | 0 | 0 | 0 | 0 | $0.0038 |
| cathedral-immaculate-conception-syracuse | 2 | 18 | 18 | 0 | 0 | 0 | 0 | 0 | $0.0020 |
| catholic-communities-of-eastern-broome | 3 | 9 | 9 | 0 | 0 | 0 | 0 | 0 | $0.0036 |
| annunciation-our-lady-queen-of-apostles-ilion | 2 | 16 | 16 | 0 | 0 | 0 | 0 | 0 | $0.0017 |
| holy-mother-and-child-st-joseph-st-paul-greenfield-center | 4 | 11 | 11 | 0 | 0 | 0 | 0 | 0 | $0.0033 |
| holy-trinity-cohoes | 2 | 15 | 15 | 0 | 0 | 0 | 0 | 0 | $0.0016 |
| holy-cross-buffalo | 2 | 11 | 11 | 0 | 0 | 0 | 0 | 0 | $0.0013 |
| holy-family-endwell | 2 | 6 | 6 | 0 | 0 | 0 | 0 | 0 | $0.0018 |
| catholic-parishes-eastern-wayne-county | 4 | 24 | 24 | 0 | 0 | 0 | 0 | 0 | $0.0046 |
| church-of-the-nativity-tully | 4 | 12 | 12 | 0 | 0 | 0 | 0 | 0 | $0.0031 |
| holy-family-st-marianne-cope-syracuse | 4 | 20 | 20 | 0 | 0 | 0 | 0 | 0 | $0.0053 |
| catholic-neighbors-in-faith | 4 | 25 | 25 | 0 | 0 | 0 | 0 | 0 | $0.0051 |
| downtown-family-buffalo | 4 | 22 | 22 | 0 | 0 | 0 | 0 | 0 | $0.0049 |
| holy-cross-utica | 3 | 6 | 6 | 0 | 0 | 0 | 0 | 0 | $0.0018 |
| immaculate-conception-ithaca | 3 | 16 | 16 | 0 | 0 | 0 | 0 | 0 | $0.0031 |
| holy-cross-morris | 3 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | $0.0012 |
| cheektowaga-kaisertown-sloan-catholic | 3 | 17 | 17 | 0 | 0 | 0 | 0 | 0 | $0.0020 |
| immaculate-conception-hoosick-falls | 4 | 9 | 9 | 0 | 0 | 0 | 0 | 0 | $0.0030 |
| greater-east-buffalo-catholic | 3 | 28 | 28 | 0 | 0 | 0 | 0 | 0 | $0.0041 |
| fields-of-grace | 4 | 33 | 33 | 0 | 0 | 0 | 0 | 0 | $0.0042 |
| basilica-sacred-heart-syracuse | 2 | 14 | 14 | 0 | 0 | 0 | 0 | 0 | $0.0018 |
| blessed-sacrament-st-vincent-de-paul-syracuse | 3 | 17 | 17 | 0 | 0 | 0 | 0 | 0 | $0.0030 |
| catholic-community-st-stephen-st-patrick-whitney-point | 3 | 15 | 15 | 0 | 0 | 0 | 0 | 0 | $0.0026 |
| immaculate-conception-greene | 2 | 4 | 4 | 0 | 0 | 0 | 0 | 0 | $0.0011 |
| all-saints-on-the-hudson-mechanicville | 4 | 12 | 12 | 0 | 0 | 0 | 0 | 0 | $0.0025 |
| catholic-family-holy-spirit-alden | 3 | 34 | 34 | 0 | 0 | 0 | 0 | 0 | $0.0042 |
| our-lady-of-fatima-delanson | 2 | 4 | 4 | 0 | 0 | 0 | 0 | 0 | $0.0009 |
| mary-mother-of-our-savior-utica | 2 | 15 | 15 | 0 | 0 | 0 | 0 | 0 | $0.0026 |
| immaculate-conception-st-bridgets | 3 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | $0.0011 |
| net-catholic | 3 | 12 | 12 | 0 | 0 | 0 | 0 | 0 | $0.0023 |
| nativity-seas | 3 | 13 | 13 | 0 | 0 | 0 | 0 | 0 | $0.0030 |
| most-holy-rosary-maine | 2 | 5 | 5 | 0 | 0 | 0 | 0 | 0 | $0.0012 |
| immaculate-conception-fayetteville | 3 | 9 | 9 | 0 | 0 | 0 | 0 | 0 | $0.0025 |
| holy-trinity-st-stephen-fulton | 3 | 12 | 12 | 0 | 0 | 0 | 0 | 0 | $0.0027 |
| our-lady-of-hope-copake-falls | 2 | 3 | 3 | 0 | 0 | 0 | 0 | 0 | $0.0010 |
| our-lady-of-sorrows-vestal | 3 | 9 | 9 | 0 | 0 | 0 | 0 | 0 | $0.0025 |
| our-lady-of-hope-fort-plain | 2 | 3 | 3 | 0 | 0 | 0 | 0 | 0 | $0.0009 |
| our-lady-of-the-annunciation-queensbury | 3 | 8 | 8 | 0 | 0 | 0 | 0 | 0 | $0.0021 |
| our-lady-of-the-americas-albany | 2 | 3 | 3 | 0 | 0 | 0 | 0 | 0 | $0.0011 |
| one-catholic | 4 | 34 | 34 | 0 | 0 | 0 | 0 | 0 | $0.0051 |
| one-catholic-family-east-syracuse | 4 | 10 | 10 | 0 | 0 | 0 | 0 | 0 | $0.0035 |
| our-lady-of-lourdes-st-anne | 3 | 13 | 13 | 0 | 0 | 0 | 0 | 0 | $0.0026 |
| our-lady-of-peace-geneva | 4 | 23 | 23 | 0 | 0 | 0 | 0 | 0 | $0.0049 |
| our-lady-of-the-sacred-heart-orchard-park | 2 | 10 | 10 | 0 | 0 | 0 | 0 | 0 | $0.0021 |
| our-lady-of-the-assumption-latham | 2 | 9 | 9 | 0 | 0 | 0 | 0 | 0 | $0.0021 |
| our-lady-of-the-valley-middleburgh | 2 | 4 | 4 | 0 | 0 | 0 | 0 | 0 | $0.0012 |
| sacred-heart-sidney | 2 | 6 | 6 | 0 | 0 | 0 | 0 | 0 | $0.0010 |
| sacred-heart-lake-george | 2 | 5 | 5 | 0 | 0 | 0 | 0 | 0 | $0.0014 |
| our-lady-of-victory-st-joseph | 2 | 11 | 11 | 0 | 0 | 0 | 0 | 0 | $0.0009 |
| sacred-heart-troy | 2 | 10 | 10 | 0 | 0 | 0 | 0 | 0 | $0.0012 |
| sacred-heart-cathedral | 2 | 16 | 16 | 0 | 0 | 0 | 0 | 0 | $0.0019 |
| sacred-heart-rome | 4 | 13 | 13 | 0 | 0 | 0 | 0 | 0 | $0.0034 |
| our-lady-of-victory-troy | 4 | 8 | 8 | 0 | 0 | 0 | 0 | 0 | $0.0030 |
| sacred-heart-margaretville | 3 | 7 | 7 | 0 | 0 | 0 | 0 | 0 | $0.0023 |
| st-ambrose-latham | 2 | 10 | 10 | 0 | 0 | 0 | 0 | 0 | $0.0016 |
| ss-cyril-methodius-holy-trinity-binghamton | 4 | 9 | 9 | 0 | 0 | 0 | 0 | 0 | $0.0021 |
| our-lady-of-the-valley | 3 | 20 | 20 | 0 | 0 | 0 | 0 | 0 | $0.0037 |
| southeast-rochester-catholic-community | 4 | 12 | 12 | 0 | 0 | 0 | 0 | 0 | $0.0030 |
| our-mother-of-sorrows-holy-cross | 3 | 16 | 16 | 0 | 0 | 0 | 0 | 0 | $0.0040 |
| st-anthony-of-padua-troy | 2 | 10 | 10 | 0 | 0 | 0 | 0 | 0 | $0.0012 |
| st-anthony-schenectady | 3 | 4 | 4 | 0 | 0 | 0 | 0 | 0 | $0.0022 |
| st-bartholomew-norwich | 3 | 5 | 5 | 0 | 0 | 0 | 0 | 0 | $0.0016 |
| st-cecilia-sacred-heart-fonda | 3 | 6 | 6 | 0 | 0 | 0 | 0 | 0 | $0.0016 |
| st-clement-saratoga-springs | 3 | 10 | 10 | 0 | 0 | 0 | 0 | 0 | $0.0053 |
| peace-of-christ | 4 | 15 | 15 | 0 | 0 | 0 | 0 | 0 | $0.0073 |
| st-charles-borromeo | 3 | 11 | 11 | 0 | 0 | 0 | 0 | 0 | $0.0025 |
| st-christopher | 3 | 8 | 8 | 0 | 0 | 0 | 0 | 0 | $0.0020 |
| st-elizabeth-ann-seton-baldwinsville | 3 | 8 | 8 | 0 | 0 | 0 | 0 | 0 | $0.0020 |
| st-charles-st-ann-st-patrick-st-brigid-syracuse | 4 | 10 | 10 | 0 | 0 | 0 | 0 | 0 | $0.0037 |
| sacred-heart-auburn-cluster | 4 | 18 | 18 | 0 | 0 | 0 | 0 | 0 | $0.0082 |
| st-benedict-parish | 4 | 13 | 13 | 0 | 0 | 0 | 0 | 0 | $0.0117 |
| st-francis-and-st-clare | 3 | 13 | 13 | 0 | 0 | 0 | 0 | 0 | $0.0033 |
| st-francis-of-assisi-albany | 4 | 7 | 7 | 0 | 0 | 0 | 0 | 0 | $0.0029 |
| st-jerome | 3 | 11 | 11 | 0 | 0 | 0 | 0 | 0 | $0.0017 |
| st-joan-of-arc-menands | 3 | 9 | 9 | 0 | 0 | 0 | 0 | 0 | $0.0012 |
| shepherd-and-saints-family | 4 | 36 | 36 | 0 | 0 | 0 | 0 | 0 | $0.0131 |
| st-john-the-baptist-holy-trinity-syracuse | 3 | 3 | 3 | 0 | 0 | 0 | 0 | 0 | $0.0014 |
| st-john-greece | 3 | 9 | 9 | 0 | 0 | 0 | 0 | 0 | $0.0030 |
| st-john-the-evangelist-schenectady | 3 | 4 | 4 | 0 | 0 | 0 | 0 | 0 | $0.0023 |
| st-benedicts-st-marys-lake | 4 | 8 | 8 | 0 | 0 | 0 | 0 | 0 | $0.0039 |
| st-john-xxiii-west-seneca | 3 | 8 | 8 | 0 | 0 | 0 | 0 | 0 | $0.0021 |
| st-john-of-rochester | 3 | 17 | 17 | 0 | 0 | 0 | 0 | 0 | $0.0037 |
| st-john-st-joseph-st-mary-rensselaer | 3 | 19 | 19 | 0 | 0 | 0 | 0 | 0 | $0.0027 |
| st-gabriel-elma | 3 | 28 | 28 | 0 | 0 | 0 | 0 | 0 | $0.0040 |
| st-joseph-worcester | 3 | 6 | 6 | 0 | 0 | 0 | 0 | 0 | $0.0013 |
| st-james-johnson-city | 3 | 18 | 18 | 0 | 0 | 0 | 0 | 0 | $0.0035 |
| st-joseph-camillus | 3 | 13 | 13 | 0 | 0 | 0 | 0 | 0 | $0.0031 |
| st-henry-averill-park | 3 | 12 | 12 | 0 | 0 | 0 | 0 | 0 | $0.0025 |
| st-john-the-evangelist-camden | 3 | 7 | 7 | 0 | 0 | 0 | 0 | 0 | $0.0017 |
| st-joseph-cathedral-buffalo | 3 | 11 | 11 | 0 | 0 | 0 | 0 | 0 | $0.0021 |
| st-john-the-evangelist-new-hartford | 3 | 9 | 9 | 0 | 0 | 0 | 0 | 0 | $0.0023 |
| st-lucy-syracuse | 2 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | $0.0013 |
| st-joseph-st-mary-st-paul-fort-edward | 3 | 12 | 12 | 0 | 0 | 0 | 0 | 0 | $0.0022 |
| st-john-vianney | 3 | 16 | 16 | 0 | 0 | 0 | 0 | 0 | $0.0024 |
| st-joseph-troy | 2 | 15 | 15 | 0 | 0 | 0 | 0 | 0 | $0.0024 |
| st-margaret-mattydale | 3 | 8 | 8 | 0 | 0 | 0 | 0 | 0 | $0.0014 |
| st-marks-greece | 3 | 9 | 9 | 0 | 0 | 0 | 0 | 0 | $0.0026 |
| st-mary-clinton | 3 | 5 | 5 | 0 | 0 | 0 | 0 | 0 | $0.0017 |
| st-mary-cooperstown | 3 | 8 | 8 | 0 | 0 | 0 | 0 | 0 | $0.0017 |
| st-marianne-cope | 3 | 9 | 9 | 0 | 0 | 0 | 0 | 0 | $0.0023 |
| st-madeleine-sophie-st-gabriel-schenectady | 3 | 13 | 13 | 0 | 0 | 0 | 0 | 0 | $0.0032 |
| st-mary-glens-falls | 3 | 7 | 7 | 0 | 0 | 0 | 0 | 0 | $0.0023 |
| st-mary-of-mount-carmel-blessed-sacrament-utica | 3 | 4 | 4 | 0 | 0 | 0 | 0 | 0 | $0.0022 |
| st-mary-amsterdam | 2 | 13 | 13 | 0 | 0 | 0 | 0 | 0 | $0.0020 |
| st-martin-de-porres | 4 | 10 | 10 | 0 | 0 | 0 | 0 | 0 | $0.0027 |
| st-mary-oneonta | 3 | 8 | 8 | 0 | 0 | 0 | 0 | 0 | $0.0021 |
| st-mary-of-the-lake-skaneateles | 3 | 9 | 9 | 0 | 0 | 0 | 0 | 0 | $0.0018 |
| st-mary-waterford | 3 | 5 | 5 | 0 | 0 | 0 | 0 | 0 | $0.0015 |
| st-louis-pittsford | 3 | 15 | 15 | 0 | 0 | 0 | 0 | 0 | $0.0040 |
| st-patrick-chittenango | 3 | 5 | 5 | 0 | 0 | 0 | 0 | 0 | $0.0013 |
| st-patrick-st-anthony-chadwicks | 3 | 5 | 5 | 0 | 0 | 0 | 0 | 0 | $0.0013 |
| st-matthew-voorheesville | 3 | 8 | 8 | 0 | 0 | 0 | 0 | 0 | $0.0018 |
| st-mary-ballston-spa | 4 | 13 | 13 | 0 | 0 | 0 | 0 | 0 | $0.0044 |
| st-patricks-family-of-churches | 4 | 13 | 13 | 0 | 0 | 0 | 0 | 0 | $0.0030 |
| st-michael-cohoes | 3 | 13 | 13 | 0 | 0 | 0 | 0 | 0 | $0.0026 |
| st-michael-st-peter-our-lady-of-hope-syracuse | 4 | 12 | 12 | 0 | 0 | 0 | 0 | 0 | $0.0027 |
| st-mary-st-paul-binghamton | 4 | 12 | 12 | 0 | 0 | 0 | 0 | 0 | $0.0031 |
| st-paul-the-apostle-hancock | 3 | 8 | 8 | 0 | 0 | 0 | 0 | 0 | $0.0019 |
| st-peter-saratoga-springs | 3 | 7 | 7 | 0 | 0 | 0 | 0 | 0 | $0.0023 |
| st-stephen-hagaman | 3 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | $0.0012 |
| st-stanislaus-our-lady-of-mount-carmel-amsterdam | 3 | 4 | 4 | 0 | 0 | 0 | 0 | 0 | $0.0022 |
| st-katharine-drexel-st-maximilian-kolbe | 4 | 32 | 32 | 0 | 0 | 0 | 0 | 0 | $0.0062 |
| st-pius-x-chili | 3 | 11 | 11 | 0 | 0 | 0 | 0 | 0 | $0.0033 |
| st-paul-norwich | 3 | 7 | 7 | 0 | 0 | 0 | 0 | 0 | $0.0021 |
| st-vincent-de-paul-blessed-sacrament-vestal | 3 | 7 | 7 | 0 | 0 | 0 | 0 | 0 | $0.0017 |
| st-vincent-de-paul-cobleskill | 2 | 7 | 7 | 0 | 0 | 0 | 0 | 0 | $0.0010 |
| st-theresa-windham | 3 | 4 | 4 | 0 | 0 | 0 | 0 | 0 | $0.0013 |
| st-monica-emmanuel | 3 | 11 | 11 | 0 | 0 | 0 | 0 | 0 | $0.0032 |
| st-thomas-the-apostle-delmar | 3 | 13 | 13 | 0 | 0 | 0 | 0 | 0 | $0.0024 |
| st-rita-webster | 3 | 14 | 14 | 0 | 0 | 0 | 0 | 0 | $0.0036 |
| st-patrick-st-thomas-aquinas-binghamton | 3 | 28 | 28 | 0 | 0 | 0 | 0 | 0 | $0.0035 |
| st-stanislaus-kostka | 3 | 16 | 16 | 0 | 0 | 0 | 0 | 0 | $0.0035 |
| together-in-christ-family | 4 | 35 | 35 | 0 | 0 | 0 | 0 | 0 | $0.0065 |
