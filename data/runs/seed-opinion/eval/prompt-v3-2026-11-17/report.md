# Seed second opinion

gpt-6-luna read each approved seed's newest 2-4 bulletins blind; its schedule is compared with the approved slots (`seeding/opinion.py`). See docs/seed-second-opinion-plan.md.

- Parishes compared: 258; skipped: 8 (1 bulletin(s) with a stored PDF: 8); unparseable: 0
- Cost of these replies: $0.983 (median $0.0032, mean $0.0038 a parish); spent this run: $0.2712
- Output tokens a parish: median 5674, mean 6622 (reasoning: median 3302)
- Luna entries: 3778; church slugs mapped to a listed one: 0

## Counted differences (grouped: a Mon-Fri difference is one; resolved excluded)

| measure | total | median | parishes with none | parishes with 3 or fewer |
|---|---:|---:|---:|---:|
| all kinds | 185 | 0 | 167 | 247 |
| missing | 32 | 0 | 236 | 257 |
| extra | 89 | 0 | 205 | 253 |
| differs | 40 | 0 | 232 | 257 |
| excluded | 24 | 0 | 240 | 258 |
| question | 0 | 0 | 258 | 258 |

- Agreements: 3622 of luna's entries agree with a slot (3846 included slots in all).
- Ungrouped counted differences: 239.
- Resolved groups (not counted): policy-exclusion 2, unseen-bulletins 5, website 52.
- Dropped as no difference: cancels-nothing 3, covered-by-weekly 15.

Distribution of counted differences:

- 0: 167 parishes
- 1: 47 parishes
- 2: 23 parishes
- 3: 10 parishes
- 4: 3 parishes
- 5: 5 parishes
- 6: 1 parishes
- 8: 1 parishes
- 10+: 1 parishes

## Every parish (counted differences)

| parish | bulletins | seed slots | agree | missing | extra | differs | excluded | question | resolved | cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| catholic-family-holy-spirit-alden | 3 | 34 | 29 | 6 | 5 | 0 | 0 | 0 | 0 | $0.0036 |
| st-anthony-of-padua-syracuse | 2 | 13 | 3 | 0 | 5 | 3 | 0 | 0 | 1 | $0.0021 |
| st-mary-of-the-assumption-oswego | 3 | 27 | 17 | 0 | 1 | 5 | 0 | 0 | 0 | $0.0035 |
| holy-spirit-holy-trinity-gloversville | 4 | 20 | 16 | 0 | 4 | 0 | 1 | 0 | 0 | $0.0036 |
| prince-of-peace-our-lady-of-good-counsel-endicott | 3 | 12 | 7 | 0 | 5 | 0 | 0 | 0 | 0 | $0.0071 |
| st-john-spencerport | 3 | 16 | 12 | 1 | 2 | 2 | 0 | 0 | 0 | $0.0076 |
| st-patricks-victor | 3 | 20 | 11 | 0 | 2 | 3 | 0 | 0 | 0 | $0.0049 |
| twelve-apostles-catholic | 4 | 37 | 32 | 0 | 5 | 0 | 0 | 0 | 0 | $0.0055 |
| blessed-family-7-west-seneca | 3 | 29 | 26 | 2 | 2 | 0 | 0 | 0 | 0 | $0.0100 |
| our-lady-of-the-lakes | 4 | 14 | 10 | 0 | 3 | 1 | 0 | 0 | 0 | $0.0036 |
| st-john-the-baptist-greenville | 4 | 14 | 10 | 0 | 2 | 2 | 0 | 0 | 0 | $0.0039 |
| assumption-resurrection | 3 | 19 | 18 | 0 | 0 | 0 | 3 | 0 | 1 | $0.0043 |
| blessed-trinity-st-patrick | 3 | 33 | 30 | 2 | 0 | 1 | 0 | 0 | 0 | $0.0133 |
| enchanted-mountains-catholic | 4 | 25 | 23 | 2 | 1 | 0 | 0 | 0 | 1 | $0.0062 |
| holy-trinity-hudson | 4 | 15 | 6 | 0 | 3 | 0 | 0 | 0 | 3 | $0.0024 |
| st-daniel-syracuse | 3 | 12 | 10 | 0 | 1 | 1 | 1 | 0 | 0 | $0.0091 |
| st-joseph-st-patrick-utica | 3 | 2 | 2 | 3 | 0 | 0 | 0 | 0 | 1 | $0.0019 |
| st-joseph-the-worker-west-winfield | 4 | 26 | 19 | 0 | 3 | 0 | 0 | 0 | 5 | $0.0040 |
| st-mary-cortland | 4 | 19 | 14 | 1 | 2 | 0 | 0 | 0 | 3 | $0.0041 |
| st-peters-ontario-county | 4 | 16 | 13 | 0 | 0 | 3 | 0 | 0 | 0 | $0.0044 |
| wheat-family-east-aurora | 4 | 43 | 41 | 0 | 3 | 0 | 0 | 0 | 0 | $0.0076 |
| assumption-syracuse | 2 | 6 | 6 | 0 | 0 | 0 | 2 | 0 | 0 | $0.0030 |
| catholic-family-cheektowaga | 4 | 40 | 39 | 1 | 0 | 1 | 0 | 0 | 0 | $0.0066 |
| catholic-family-holy-rosary | 4 | 21 | 19 | 0 | 2 | 0 | 0 | 0 | 0 | $0.0033 |
| chautauqua-family-catholic | 4 | 35 | 35 | 1 | 0 | 0 | 1 | 0 | 0 | $0.0076 |
| christ-our-light-st-anne-pulaski | 3 | 16 | 14 | 0 | 2 | 0 | 0 | 0 | 0 | $0.0035 |
| good-shepherd-catholic-community | 4 | 16 | 14 | 0 | 1 | 1 | 0 | 0 | 0 | $0.0034 |
| hudson-valley-vicariate-west-catskill | 3 | 32 | 32 | 0 | 0 | 0 | 2 | 0 | 0 | $0.0039 |
| liverpool-catholic-community | 4 | 27 | 25 | 0 | 1 | 1 | 0 | 0 | 0 | $0.0064 |
| niagara-frontier-catholic | 4 | 29 | 27 | 0 | 1 | 1 | 0 | 0 | 0 | $0.0057 |
| northern-points-cluster-st-cecilia-chestertown | 4 | 8 | 6 | 0 | 2 | 0 | 0 | 0 | 0 | $0.0022 |
| olg-ic-sj-glenville | 4 | 21 | 19 | 0 | 1 | 1 | 0 | 0 | 0 | $0.0059 |
| our-lady-of-the-assumption-latham | 2 | 9 | 9 | 1 | 0 | 0 | 1 | 0 | 0 | $0.0027 |
| parish-of-the-holy-family | 2 | 18 | 17 | 0 | 0 | 1 | 1 | 0 | 0 | $0.0034 |
| sacred-heart-troy | 2 | 10 | 9 | 1 | 0 | 1 | 0 | 0 | 0 | $0.0017 |
| spirit-of-hope-oneida | 4 | 15 | 15 | 0 | 0 | 0 | 2 | 0 | 0 | $0.0056 |
| st-clare-christ-our-light-colonie | 3 | 10 | 8 | 0 | 2 | 0 | 0 | 0 | 0 | $0.0046 |
| st-john-the-baptist-walton | 3 | 15 | 14 | 1 | 1 | 0 | 0 | 0 | 0 | $0.0023 |
| st-john-vianney | 3 | 16 | 12 | 0 | 0 | 2 | 0 | 0 | 0 | $0.0060 |
| st-kateri-tekakwitha | 4 | 13 | 12 | 0 | 0 | 1 | 1 | 0 | 0 | $0.0038 |
| st-rose-of-lima-north-syracuse | 3 | 10 | 10 | 1 | 0 | 0 | 1 | 0 | 0 | $0.0046 |
| three-catholic-sisters-foothills | 4 | 21 | 19 | 0 | 0 | 2 | 0 | 0 | 0 | $0.0181 |
| transfiguration-syracuse | 2 | 40 | 38 | 1 | 0 | 1 | 0 | 0 | 0 | $0.0060 |
| transfiguration-troy | 4 | 2 | 2 | 0 | 0 | 0 | 2 | 0 | 0 | $0.0022 |
| all-saints-corning | 2 | 6 | 6 | 0 | 0 | 0 | 1 | 0 | 0 | $0.0026 |
| bread-of-life-catholic-community | 4 | 70 | 69 | 0 | 1 | 0 | 0 | 0 | 0 | $0.0175 |
| catholic-family-south-buffalo | 4 | 34 | 31 | 0 | 1 | 0 | 0 | 0 | 2 | $0.0125 |
| christ-the-king-albany | 3 | 11 | 10 | 0 | 1 | 0 | 0 | 0 | 0 | $0.0024 |
| corpus-christi-round-lake | 2 | 14 | 13 | 0 | 1 | 0 | 0 | 0 | 0 | $0.0023 |
| historic-old-st-johns-utica | 2 | 13 | 12 | 0 | 1 | 0 | 0 | 0 | 0 | $0.0024 |
| holy-cross-dewitt | 2 | 16 | 12 | 0 | 1 | 0 | 0 | 0 | 3 | $0.0024 |
| holy-family-little-falls | 2 | 19 | 18 | 0 | 1 | 0 | 0 | 0 | 0 | $0.0049 |
| holy-family-schuylerville | 4 | 18 | 17 | 0 | 1 | 0 | 0 | 0 | 0 | $0.0032 |
| holy-family-st-marianne-cope-syracuse | 4 | 20 | 20 | 1 | 0 | 0 | 0 | 0 | 0 | $0.0121 |
| holy-spirit-hamilton | 4 | 20 | 13 | 0 | 0 | 1 | 0 | 0 | 6 | $0.0050 |
| holy-spirit-sacred-heart-east-greenbush | 4 | 15 | 14 | 0 | 0 | 0 | 1 | 0 | 0 | $0.0045 |
| holy-spirit-st-josephs | 3 | 29 | 28 | 0 | 0 | 1 | 0 | 0 | 0 | $0.0036 |
| holy-trinity-webster | 2 | 19 | 18 | 0 | 1 | 0 | 0 | 0 | 0 | $0.0025 |
| immaculate-conception-ithaca | 3 | 16 | 15 | 0 | 1 | 0 | 0 | 0 | 0 | $0.0032 |
| immaculate-heart-of-mary-watervliet | 2 | 6 | 5 | 0 | 0 | 0 | 1 | 0 | 0 | $0.0018 |
| mary-mother-of-our-savior-utica | 2 | 15 | 14 | 0 | 1 | 0 | 0 | 0 | 0 | $0.0026 |
| niagara-falls-rc-family | 4 | 29 | 28 | 0 | 0 | 1 | 0 | 0 | 0 | $0.0046 |
| our-lady-of-fatima-shrine-lewiston | 4 | 40 | 39 | 0 | 1 | 0 | 0 | 0 | 0 | $0.0045 |
| our-lady-of-good-counsel-verona | 3 | 16 | 15 | 0 | 1 | 0 | 0 | 0 | 0 | $0.0024 |
| our-lady-of-peace-geneva | 4 | 23 | 22 | 0 | 1 | 0 | 0 | 0 | 0 | $0.0057 |
| our-lady-of-the-snow-saints-mary-and-martha | 4 | 26 | 25 | 0 | 0 | 1 | 0 | 0 | 0 | $0.0050 |
| our-lady-queen-of-peace-rotterdam | 4 | 9 | 8 | 0 | 0 | 1 | 0 | 0 | 0 | $0.0024 |
| saints-john-and-andrew-binghamton | 3 | 11 | 11 | 0 | 0 | 0 | 1 | 0 | 0 | $0.0046 |
| st-anthony-st-agnes-utica | 3 | 6 | 5 | 0 | 1 | 0 | 0 | 0 | 0 | $0.0016 |
| st-catherine-of-siena-ithaca | 3 | 8 | 8 | 1 | 0 | 0 | 0 | 0 | 0 | $0.0027 |
| st-charles-st-ann-st-patrick-st-brigid-syracuse | 4 | 10 | 9 | 0 | 0 | 1 | 0 | 0 | 0 | $0.0087 |
| st-edward-the-confessor-clifton-park | 3 | 13 | 13 | 0 | 0 | 0 | 1 | 0 | 0 | $0.0035 |
| st-john-greece | 3 | 9 | 8 | 0 | 1 | 0 | 0 | 0 | 0 | $0.0030 |
| st-joseph-schenectady | 3 | 13 | 12 | 0 | 1 | 0 | 0 | 0 | 0 | $0.0028 |
| st-joseph-university-buffalo | 3 | 19 | 16 | 0 | 1 | 0 | 0 | 0 | 0 | $0.0034 |
| st-jude-st-michael-wynantskill | 3 | 15 | 14 | 0 | 1 | 0 | 0 | 0 | 0 | $0.0022 |
| st-kateri-latin-mass-community | 2 | 8 | 2 | 0 | 1 | 0 | 0 | 0 | 1 | $0.0012 |
| st-luke-schenectady | 3 | 11 | 9 | 0 | 1 | 0 | 0 | 0 | 1 | $0.0029 |
| st-mary-crescent | 3 | 10 | 9 | 0 | 1 | 0 | 0 | 0 | 0 | $0.0033 |
| st-mary-nassau | 3 | 4 | 4 | 1 | 0 | 0 | 0 | 0 | 0 | $0.0028 |
| st-mary-of-the-assumption-baldwinsville | 3 | 8 | 7 | 0 | 1 | 0 | 0 | 0 | 0 | $0.0034 |
| st-mary-our-mother | 3 | 9 | 9 | 1 | 0 | 0 | 0 | 0 | 0 | $0.0025 |
| st-michael-the-archangel-south-glens-falls | 3 | 12 | 12 | 1 | 0 | 0 | 0 | 0 | 0 | $0.0035 |
| st-patrick-st-thomas-aquinas-binghamton | 3 | 28 | 28 | 1 | 0 | 0 | 0 | 0 | 0 | $0.0043 |
| st-paul-whitesboro | 4 | 12 | 12 | 0 | 0 | 0 | 1 | 0 | 0 | $0.0039 |
| st-pauls-webster | 3 | 11 | 11 | 1 | 0 | 0 | 0 | 0 | 0 | $0.0024 |
| st-pius-x-chili | 3 | 11 | 10 | 0 | 1 | 0 | 0 | 0 | 0 | $0.0038 |
| st-theodores-gates | 4 | 15 | 8 | 0 | 1 | 0 | 0 | 0 | 0 | $0.0023 |
| together-in-christ-family | 4 | 35 | 35 | 1 | 0 | 0 | 0 | 0 | 0 | $0.0066 |
| tonawanda-catholic | 4 | 37 | 36 | 0 | 1 | 0 | 0 | 0 | 0 | $0.0045 |
| transfiguration-st-catherine-mendon | 3 | 11 | 10 | 0 | 1 | 0 | 0 | 0 | 0 | $0.0028 |
| all-saints-albany | 2 | 12 | 12 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0023 |
| all-saints-on-the-hudson-mechanicville | 4 | 12 | 12 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0026 |
| all-saints-syracuse | 3 | 7 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0028 |
| annunciation-our-lady-queen-of-apostles-ilion | 2 | 16 | 16 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0017 |
| basilica-sacred-heart-syracuse | 2 | 14 | 14 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0046 |
| beloved-disciples-lancaster | 4 | 45 | 45 | 0 | 0 | 0 | 0 | 0 | 1 | $0.0064 |
| blessed-sacrament-albany | 2 | 14 | 14 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0023 |
| blessed-sacrament-st-vincent-de-paul-syracuse | 3 | 17 | 17 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0030 |
| blessed-trinity-buffalo | 2 | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0022 |
| cathedral-immaculate-conception-syracuse | 2 | 18 | 18 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0020 |
| cathedral-st-mary-albany | 4 | 23 | 23 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0044 |
| catholic-communities-of-eastern-broome | 3 | 9 | 9 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0075 |
| catholic-community-buffalo-north | 4 | 19 | 19 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0059 |
| catholic-community-st-stephen-st-patrick-whitney-point | 3 | 15 | 15 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0026 |
| catholic-neighbors-in-faith | 4 | 25 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0057 |
| catholic-parishes-eastern-wayne-county | 4 | 24 | 24 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0055 |
| cattaraugus-creek-catholic | 4 | 17 | 17 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0054 |
| ccncc-valatie | 3 | 9 | 9 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0059 |
| central-niagara-catholic | 4 | 26 | 26 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0059 |
| cheektowaga-kaisertown-sloan-catholic | 3 | 17 | 17 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0023 |
| christ-our-hope-boonville | 4 | 22 | 22 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0038 |
| christ-our-light-family | 4 | 33 | 31 | 0 | 0 | 0 | 0 | 0 | 2 | $0.0050 |
| christ-sun-of-justice-troy | 2 | 6 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0009 |
| christ-the-good-shepherd-oswego | 4 | 16 | 16 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0067 |
| church-of-the-nativity-tully | 4 | 12 | 12 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0032 |
| downtown-family-buffalo | 4 | 22 | 22 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0054 |
| eternal-flame-catholic-community | 4 | 58 | 54 | 0 | 0 | 0 | 0 | 0 | 4 | $0.0066 |
| family-of-the-holy-cross-herkimer | 2 | 11 | 2 | 0 | 0 | 0 | 0 | 0 | 9 | $0.0011 |
| fields-of-grace | 4 | 33 | 33 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0044 |
| greater-east-buffalo-catholic | 3 | 28 | 28 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0045 |
| holy-cross-buffalo | 2 | 11 | 11 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0015 |
| holy-cross-morris | 3 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0011 |
| holy-cross-utica | 3 | 6 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0020 |
| holy-family-catholic-community | 4 | 11 | 10 | 0 | 0 | 0 | 0 | 0 | 1 | $0.0028 |
| holy-family-endwell | 2 | 6 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0038 |
| holy-mother-and-child-st-joseph-st-paul-greenfield-center | 4 | 11 | 11 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0032 |
| holy-trinity-cohoes | 2 | 15 | 15 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0018 |
| holy-trinity-st-stephen-fulton | 3 | 12 | 12 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0027 |
| holy-trinity-utica | 3 | 14 | 14 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0036 |
| immaculate-conception-fayetteville | 3 | 9 | 9 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0023 |
| immaculate-conception-greene | 2 | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0012 |
| immaculate-conception-hoosick-falls | 4 | 9 | 9 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0029 |
| immaculate-conception-st-bridgets | 3 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0010 |
| lakeshore-catholic-faith-community | 4 | 39 | 39 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0058 |
| light-of-christ-kenmore | 4 | 55 | 55 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0079 |
| mary-mother-of-mercy | 3 | 9 | 8 | 0 | 0 | 0 | 0 | 0 | 1 | $0.0019 |
| mater-christi-albany | 2 | 24 | 24 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0031 |
| most-holy-name-of-jesus | 3 | 18 | 18 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0037 |
| most-holy-rosary-maine | 2 | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0015 |
| nativity-seas | 3 | 13 | 13 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0036 |
| net-catholic | 3 | 12 | 12 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0026 |
| one-catholic | 4 | 34 | 34 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0061 |
| one-catholic-family-east-syracuse | 4 | 10 | 10 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0037 |
| our-lady-of-fatima-delanson | 2 | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0009 |
| our-lady-of-hope-copake-falls | 2 | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0011 |
| our-lady-of-hope-fort-plain | 2 | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0009 |
| our-lady-of-hope-whitehall | 4 | 31 | 31 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0069 |
| our-lady-of-lourdes-st-anne | 3 | 13 | 13 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0027 |
| our-lady-of-sorrows-vestal | 3 | 9 | 9 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0030 |
| our-lady-of-the-americas-albany | 2 | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0012 |
| our-lady-of-the-annunciation-queensbury | 3 | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0024 |
| our-lady-of-the-sacred-heart-orchard-park | 2 | 10 | 10 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0027 |
| our-lady-of-the-valley | 3 | 20 | 20 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0040 |
| our-lady-of-the-valley-middleburgh | 2 | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0012 |
| our-lady-of-victory-basilica | 4 | 25 | 24 | 0 | 0 | 0 | 0 | 0 | 1 | $0.0112 |
| our-lady-of-victory-st-joseph | 2 | 11 | 11 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0008 |
| our-lady-of-victory-troy | 4 | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0028 |
| our-lady-queen-of-peace-st-thomas-more | 4 | 12 | 10 | 0 | 0 | 0 | 0 | 0 | 2 | $0.0061 |
| our-mother-of-sorrows-holy-cross | 3 | 16 | 16 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0040 |
| peace-of-christ | 4 | 15 | 15 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0039 |
| prince-of-peace-north-endicott | 4 | 17 | 16 | 0 | 0 | 0 | 0 | 0 | 1 | $0.0095 |
| sacred-heart-auburn-cluster | 4 | 18 | 18 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0042 |
| sacred-heart-cathedral | 2 | 16 | 16 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0038 |
| sacred-heart-divine-mercy-cicero | 3 | 20 | 15 | 0 | 0 | 0 | 0 | 0 | 5 | $0.0052 |
| sacred-heart-lake-george | 2 | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0014 |
| sacred-heart-margaretville | 3 | 7 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0033 |
| sacred-heart-rome | 4 | 13 | 13 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0036 |
| sacred-heart-sidney | 2 | 6 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0011 |
| sacred-heart-stamford | 4 | 6 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0052 |
| shepherd-and-saints-family | 4 | 36 | 36 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0059 |
| southeast-rochester-catholic-community | 4 | 12 | 12 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0028 |
| ss-columba-and-brigid-buffalo | 2 | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0023 |
| ss-cyril-methodius-holy-trinity-binghamton | 4 | 9 | 9 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0026 |
| st-agnes-paul-rose | 4 | 12 | 11 | 0 | 0 | 0 | 0 | 0 | 1 | $0.0039 |
| st-ambrose-latham | 2 | 10 | 10 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0031 |
| st-ann-manlius | 2 | 14 | 14 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0016 |
| st-anthony-of-padua-buffalo | 2 | 18 | 18 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0038 |
| st-anthony-of-padua-troy | 2 | 10 | 10 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0013 |
| st-anthony-schenectady | 3 | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0045 |
| st-augustine-baldwinsville | 3 | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0020 |
| st-bartholomew-norwich | 3 | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0023 |
| st-benedict-parish | 4 | 13 | 13 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0124 |
| st-benedicts-st-marys-lake | 4 | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0037 |
| st-cecilia-sacred-heart-fonda | 3 | 6 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0021 |
| st-charles-borromeo | 3 | 11 | 11 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0049 |
| st-christopher | 3 | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0019 |
| st-clement-saratoga-springs | 3 | 10 | 10 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0054 |
| st-elizabeth-ann-seton-baldwinsville | 3 | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0041 |
| st-francis-and-st-clare | 3 | 13 | 13 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0036 |
| st-francis-of-assisi-albany | 4 | 7 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0033 |
| st-francis-of-assisi-binghamton | 3 | 8 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0026 |
| st-francis-xavier-marcellus | 3 | 12 | 12 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0025 |
| st-gabriel-elma | 3 | 28 | 28 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0043 |
| st-henry-averill-park | 3 | 12 | 12 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0050 |
| st-james-johnson-city | 3 | 18 | 18 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0079 |
| st-jerome | 3 | 11 | 11 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0032 |
| st-joan-of-arc-menands | 3 | 9 | 9 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0012 |
| st-john-of-rochester | 3 | 17 | 17 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0090 |
| st-john-st-joseph-st-mary-rensselaer | 3 | 19 | 19 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0064 |
| st-john-the-baptist-holy-trinity-syracuse | 3 | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0015 |
| st-john-the-evangelist-camden | 3 | 7 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0015 |
| st-john-the-evangelist-new-hartford | 3 | 9 | 9 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0026 |
| st-john-the-evangelist-schenectady | 3 | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0048 |
| st-john-xxiii-west-seneca | 3 | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0021 |
| st-joseph-camillus | 3 | 13 | 13 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0031 |
| st-joseph-cathedral-buffalo | 3 | 11 | 11 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0020 |
| st-joseph-st-francis-broadalbin | 4 | 14 | 14 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0029 |
| st-joseph-st-mary-st-paul-fort-edward | 3 | 12 | 12 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0026 |
| st-joseph-troy | 2 | 15 | 15 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0023 |
| st-joseph-worcester | 3 | 6 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0013 |
| st-kateri-tekakwitha-niskayuna | 3 | 10 | 10 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0031 |
| st-katharine-drexel-st-maximilian-kolbe | 4 | 32 | 32 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0060 |
| st-lawrence | 4 | 12 | 12 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0035 |
| st-lawrence-otoole-and-sacred-heart | 3 | 25 | 17 | 0 | 0 | 0 | 0 | 0 | 2 | $0.0040 |
| st-leo-the-great | 3 | 13 | 13 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0031 |
| st-louis-pittsford | 3 | 15 | 15 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0038 |
| st-lucy-syracuse | 2 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0030 |
| st-luke-the-evangelist | 4 | 13 | 12 | 0 | 0 | 0 | 0 | 0 | 1 | $0.0034 |
| st-madeleine-sophie-st-gabriel-schenectady | 3 | 13 | 13 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0029 |
| st-malachy-sherburne | 3 | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0020 |
| st-margaret-mattydale | 3 | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0015 |
| st-marianne-cope | 3 | 9 | 9 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0024 |
| st-marks-greece | 3 | 9 | 9 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0050 |
| st-martin-de-porres | 4 | 10 | 10 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0026 |
| st-mary-amsterdam | 2 | 13 | 13 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0024 |
| st-mary-ballston-spa | 4 | 13 | 13 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0042 |
| st-mary-clinton | 3 | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0018 |
| st-mary-cooperstown | 3 | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0017 |
| st-mary-glens-falls | 3 | 7 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0024 |
| st-mary-of-mount-carmel-blessed-sacrament-utica | 3 | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0021 |
| st-mary-of-the-lake-skaneateles | 3 | 9 | 9 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0019 |
| st-mary-oneonta | 3 | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0022 |
| st-mary-st-paul-binghamton | 4 | 12 | 12 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0031 |
| st-mary-waterford | 3 | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0014 |
| st-marys-st-matthew | 3 | 9 | 9 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0025 |
| st-matthew-voorheesville | 3 | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0019 |
| st-michael-cohoes | 3 | 13 | 13 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0026 |
| st-michael-st-peter-our-lady-of-hope-syracuse | 4 | 12 | 12 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0032 |
| st-monica-emmanuel | 3 | 11 | 11 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0029 |
| st-patrick-chittenango | 3 | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0013 |
| st-patrick-st-anthony-chadwicks | 3 | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0014 |
| st-patricks-family-of-churches | 4 | 13 | 13 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0034 |
| st-paul-norwich | 3 | 7 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0019 |
| st-paul-st-adalbert-mt-carmel-schenectady | 4 | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0034 |
| st-paul-the-apostle-hancock | 3 | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0019 |
| st-peter-saratoga-springs | 3 | 7 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0022 |
| st-rita-webster | 3 | 14 | 14 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0071 |
| st-stanislaus-kostka | 3 | 16 | 16 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0037 |
| st-stanislaus-our-lady-of-mount-carmel-amsterdam | 3 | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0021 |
| st-stephen-hagaman | 3 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0012 |
| st-theresa-windham | 3 | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0016 |
| st-thomas-the-apostle-delmar | 3 | 13 | 13 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0027 |
| st-vincent-de-paul-albany | 3 | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0011 |
| st-vincent-de-paul-blessed-sacrament-vestal | 3 | 7 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0017 |
| st-vincent-de-paul-cobleskill | 2 | 7 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0011 |
| sts-isidore-maria-torribia | 4 | 11 | 11 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0027 |
| the-lords-vineyard | 4 | 31 | 31 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0099 |
