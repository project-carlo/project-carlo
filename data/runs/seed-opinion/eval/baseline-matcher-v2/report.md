# Seed second opinion

gpt-6-luna read each approved seed's newest 2-4 bulletins blind; its schedule is compared with the approved slots (`seeding/opinion.py`). See docs/seed-second-opinion-plan.md.

- Parishes compared: 258; skipped: 8 (1 bulletin(s) with a stored PDF: 8); unparseable: 0
- Cost of these replies: $0.835 (median $0.0029, mean $0.0032 a parish); spent this run: $0.0000
- Output tokens a parish: median 5174, mean 6037 (reasoning: median 2588)
- Luna entries: 3739; church slugs mapped to a listed one: 3

## Counted differences (grouped: a Mon-Fri difference is one; resolved excluded)

| measure | total | median | parishes with none | parishes with 3 or fewer |
|---|---:|---:|---:|---:|
| all kinds | 204 | 0 | 156 | 244 |
| missing | 26 | 0 | 240 | 257 |
| extra | 96 | 0 | 194 | 255 |
| differs | 52 | 0 | 230 | 253 |
| excluded | 30 | 0 | 235 | 258 |
| question | 0 | 0 | 258 | 258 |

- Agreements: 3581 of luna's entries agree with a slot (3846 included slots in all).
- Ungrouped counted differences: 255.
- Resolved groups (not counted): policy-exclusion 4, unseen-bulletins 5, website 52.
- Dropped as no difference: cancels-nothing 5, covered-by-weekly 24.

Distribution of counted differences:

- 0: 156 parishes
- 1: 55 parishes
- 2: 24 parishes
- 3: 9 parishes
- 4: 4 parishes
- 5: 6 parishes
- 6: 1 parishes
- 7: 2 parishes
- 8: 1 parishes

## Every parish (counted differences)

| parish | bulletins | seed slots | agree | missing | extra | differs | excluded | question | resolved | cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| mater-christi-albany | 2 | 24 | 16 | 0 | 8 | 0 | 0 | 0 | 0 | $0.0018 |
| spirit-of-hope-oneida | 4 | 15 | 14 | 4 | 1 | 0 | 2 | 0 | 0 | $0.0042 |
| st-anthony-of-padua-syracuse | 2 | 13 | 5 | 0 | 3 | 4 | 0 | 0 | 1 | $0.0050 |
| our-lady-of-hope-whitehall | 4 | 31 | 27 | 2 | 1 | 3 | 0 | 0 | 0 | $0.0070 |
| catholic-family-cheektowaga | 4 | 40 | 37 | 0 | 2 | 1 | 2 | 0 | 0 | $0.0072 |
| our-lady-of-the-lakes | 4 | 14 | 10 | 0 | 3 | 1 | 1 | 0 | 0 | $0.0034 |
| st-anthony-of-padua-buffalo | 2 | 18 | 9 | 0 | 0 | 5 | 0 | 0 | 0 | $0.0020 |
| st-mary-of-the-assumption-oswego | 3 | 27 | 18 | 0 | 0 | 5 | 0 | 0 | 0 | $0.0042 |
| st-patricks-victor | 3 | 20 | 11 | 0 | 1 | 4 | 0 | 0 | 0 | $0.0045 |
| transfiguration-syracuse | 2 | 40 | 35 | 1 | 3 | 1 | 0 | 0 | 0 | $0.0089 |
| blessed-trinity-st-patrick | 3 | 33 | 25 | 0 | 0 | 4 | 0 | 0 | 0 | $0.0041 |
| prince-of-peace-our-lady-of-good-counsel-endicott | 3 | 12 | 7 | 0 | 4 | 0 | 0 | 0 | 1 | $0.0036 |
| st-john-spencerport | 3 | 16 | 13 | 1 | 3 | 0 | 0 | 0 | 0 | $0.0033 |
| st-joseph-the-worker-west-winfield | 4 | 26 | 18 | 0 | 4 | 0 | 0 | 0 | 5 | $0.0033 |
| bread-of-life-catholic-community | 4 | 70 | 67 | 0 | 2 | 1 | 0 | 0 | 0 | $0.0086 |
| holy-spirit-st-josephs | 3 | 29 | 28 | 2 | 1 | 0 | 0 | 0 | 0 | $0.0036 |
| light-of-christ-kenmore | 4 | 55 | 52 | 0 | 1 | 2 | 0 | 0 | 0 | $0.0074 |
| st-daniel-syracuse | 3 | 12 | 10 | 0 | 1 | 1 | 1 | 0 | 0 | $0.0039 |
| st-john-the-baptist-greenville | 4 | 14 | 11 | 0 | 1 | 2 | 0 | 0 | 0 | $0.0039 |
| st-mary-cortland | 4 | 19 | 14 | 1 | 2 | 0 | 0 | 0 | 3 | $0.0040 |
| st-peters-ontario-county | 4 | 16 | 13 | 0 | 0 | 3 | 0 | 0 | 0 | $0.0045 |
| twelve-apostles-catholic | 4 | 37 | 34 | 0 | 3 | 0 | 0 | 0 | 0 | $0.0053 |
| wheat-family-east-aurora | 4 | 43 | 41 | 0 | 3 | 0 | 0 | 0 | 0 | $0.0055 |
| assumption-resurrection | 3 | 19 | 18 | 0 | 0 | 0 | 2 | 0 | 1 | $0.0044 |
| assumption-syracuse | 2 | 6 | 4 | 0 | 1 | 0 | 1 | 0 | 0 | $0.0021 |
| blessed-family-7-west-seneca | 3 | 29 | 27 | 1 | 1 | 0 | 0 | 0 | 2 | $0.0054 |
| catholic-family-holy-rosary | 4 | 21 | 19 | 0 | 2 | 0 | 0 | 0 | 0 | $0.0026 |
| chautauqua-family-catholic | 4 | 35 | 33 | 0 | 1 | 1 | 0 | 0 | 0 | $0.0061 |
| christ-our-hope-boonville | 4 | 22 | 22 | 0 | 0 | 0 | 2 | 0 | 0 | $0.0037 |
| christ-our-light-st-anne-pulaski | 3 | 16 | 14 | 0 | 2 | 0 | 0 | 0 | 0 | $0.0026 |
| christ-the-king-albany | 3 | 11 | 9 | 0 | 2 | 0 | 0 | 0 | 0 | $0.0019 |
| good-shepherd-catholic-community | 4 | 16 | 14 | 0 | 1 | 1 | 0 | 0 | 0 | $0.0033 |
| holy-spirit-holy-trinity-gloversville | 4 | 20 | 10 | 1 | 1 | 0 | 0 | 0 | 0 | $0.0049 |
| hudson-valley-vicariate-west-catskill | 3 | 32 | 32 | 0 | 0 | 0 | 2 | 0 | 0 | $0.0040 |
| most-holy-name-of-jesus | 3 | 18 | 15 | 2 | 0 | 0 | 0 | 0 | 0 | $0.0044 |
| our-lady-of-good-counsel-verona | 3 | 16 | 14 | 0 | 1 | 1 | 0 | 0 | 0 | $0.0020 |
| parish-of-the-holy-family | 2 | 18 | 17 | 0 | 0 | 1 | 1 | 0 | 0 | $0.0041 |
| ss-columba-and-brigid-buffalo | 2 | 5 | 3 | 0 | 0 | 2 | 0 | 0 | 0 | $0.0014 |
| st-agnes-paul-rose | 4 | 12 | 9 | 0 | 0 | 0 | 2 | 0 | 1 | $0.0035 |
| st-clare-christ-our-light-colonie | 3 | 10 | 8 | 0 | 2 | 0 | 0 | 0 | 0 | $0.0020 |
| st-edward-the-confessor-clifton-park | 3 | 13 | 12 | 0 | 1 | 0 | 1 | 0 | 0 | $0.0026 |
| st-joseph-st-patrick-utica | 3 | 2 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | $0.0016 |
| st-kateri-tekakwitha | 4 | 13 | 12 | 0 | 0 | 1 | 1 | 0 | 0 | $0.0035 |
| st-luke-schenectady | 3 | 11 | 9 | 0 | 1 | 1 | 0 | 0 | 0 | $0.0027 |
| st-mary-nassau | 3 | 4 | 3 | 1 | 1 | 0 | 0 | 0 | 0 | $0.0023 |
| sts-isidore-maria-torribia | 4 | 11 | 9 | 2 | 0 | 0 | 0 | 0 | 0 | $0.0027 |
| transfiguration-troy | 4 | 2 | 2 | 0 | 0 | 0 | 2 | 0 | 0 | $0.0022 |
| all-saints-corning | 2 | 6 | 6 | 0 | 0 | 0 | 1 | 0 | 0 | $0.0023 |
| all-saints-syracuse | 3 | 7 | 6 | 0 | 1 | 0 | 0 | 0 | 0 | $0.0029 |
| blessed-trinity-buffalo | 2 | 8 | 7 | 0 | 1 | 0 | 0 | 0 | 0 | $0.0010 |
| catholic-family-south-buffalo | 4 | 34 | 31 | 0 | 1 | 0 | 0 | 0 | 2 | $0.0066 |
| cattaraugus-creek-catholic | 4 | 17 | 16 | 0 | 1 | 0 | 0 | 0 | 0 | $0.0027 |
| central-niagara-catholic | 4 | 26 | 26 | 0 | 0 | 0 | 1 | 0 | 0 | $0.0056 |
| corpus-christi-round-lake | 2 | 14 | 13 | 0 | 0 | 1 | 0 | 0 | 0 | $0.0029 |
| enchanted-mountains-catholic | 4 | 25 | 24 | 1 | 0 | 0 | 0 | 0 | 1 | $0.0068 |
| family-of-the-holy-cross-herkimer | 2 | 11 | 1 | 0 | 1 | 0 | 0 | 0 | 9 | $0.0007 |
| historic-old-st-johns-utica | 2 | 13 | 12 | 0 | 1 | 0 | 0 | 0 | 0 | $0.0021 |
| holy-cross-dewitt | 2 | 16 | 12 | 0 | 1 | 0 | 0 | 0 | 3 | $0.0021 |
| holy-family-little-falls | 2 | 19 | 18 | 0 | 1 | 0 | 0 | 0 | 0 | $0.0025 |
| holy-family-schuylerville | 4 | 18 | 17 | 0 | 1 | 0 | 0 | 0 | 0 | $0.0031 |
| holy-spirit-hamilton | 4 | 20 | 13 | 0 | 1 | 0 | 0 | 0 | 6 | $0.0045 |
| holy-spirit-sacred-heart-east-greenbush | 4 | 15 | 14 | 0 | 0 | 0 | 1 | 0 | 0 | $0.0037 |
| holy-trinity-webster | 2 | 19 | 18 | 0 | 1 | 0 | 0 | 0 | 0 | $0.0027 |
| immaculate-heart-of-mary-watervliet | 2 | 6 | 5 | 0 | 0 | 0 | 1 | 0 | 0 | $0.0016 |
| lakeshore-catholic-faith-community | 4 | 39 | 32 | 0 | 1 | 0 | 0 | 0 | 0 | $0.0055 |
| liverpool-catholic-community | 4 | 27 | 26 | 0 | 1 | 0 | 0 | 0 | 0 | $0.0058 |
| niagara-falls-rc-family | 4 | 29 | 28 | 0 | 0 | 1 | 0 | 0 | 0 | $0.0044 |
| niagara-frontier-catholic | 4 | 29 | 28 | 0 | 1 | 0 | 0 | 0 | 0 | $0.0052 |
| northern-points-cluster-st-cecilia-chestertown | 4 | 8 | 8 | 1 | 0 | 0 | 0 | 0 | 0 | $0.0031 |
| olg-ic-sj-glenville | 4 | 21 | 20 | 0 | 0 | 1 | 0 | 0 | 0 | $0.0055 |
| our-lady-of-fatima-shrine-lewiston | 4 | 40 | 39 | 0 | 1 | 0 | 0 | 0 | 0 | $0.0043 |
| our-lady-of-the-snow-saints-mary-and-martha | 4 | 26 | 25 | 0 | 1 | 0 | 0 | 0 | 0 | $0.0121 |
| our-lady-of-victory-basilica | 4 | 25 | 24 | 0 | 0 | 0 | 1 | 0 | 1 | $0.0113 |
| our-lady-queen-of-peace-rotterdam | 4 | 9 | 8 | 0 | 0 | 1 | 0 | 0 | 0 | $0.0023 |
| sacred-heart-stamford | 4 | 6 | 5 | 0 | 1 | 0 | 0 | 0 | 0 | $0.0021 |
| saints-john-and-andrew-binghamton | 3 | 11 | 11 | 0 | 0 | 0 | 1 | 0 | 0 | $0.0039 |
| st-anthony-st-agnes-utica | 3 | 6 | 5 | 0 | 1 | 0 | 0 | 0 | 0 | $0.0015 |
| st-augustine-baldwinsville | 3 | 3 | 2 | 1 | 0 | 0 | 0 | 0 | 0 | $0.0039 |
| st-catherine-of-siena-ithaca | 3 | 8 | 7 | 0 | 1 | 0 | 0 | 0 | 0 | $0.0029 |
| st-francis-xavier-marcellus | 3 | 12 | 11 | 0 | 0 | 1 | 0 | 0 | 0 | $0.0021 |
| st-john-the-baptist-walton | 3 | 15 | 14 | 0 | 1 | 0 | 0 | 0 | 0 | $0.0017 |
| st-joseph-schenectady | 3 | 13 | 12 | 0 | 1 | 0 | 0 | 0 | 0 | $0.0029 |
| st-joseph-st-francis-broadalbin | 4 | 14 | 14 | 0 | 0 | 0 | 1 | 0 | 0 | $0.0032 |
| st-joseph-university-buffalo | 3 | 19 | 18 | 0 | 1 | 0 | 0 | 0 | 0 | $0.0034 |
| st-jude-st-michael-wynantskill | 3 | 15 | 14 | 0 | 1 | 0 | 0 | 0 | 0 | $0.0022 |
| st-kateri-tekakwitha-niskayuna | 3 | 10 | 9 | 0 | 1 | 0 | 0 | 0 | 0 | $0.0025 |
| st-lawrence | 4 | 12 | 12 | 0 | 0 | 0 | 1 | 0 | 0 | $0.0033 |
| st-leo-the-great | 3 | 13 | 13 | 0 | 0 | 0 | 1 | 0 | 0 | $0.0034 |
| st-mary-crescent | 3 | 10 | 9 | 0 | 0 | 1 | 0 | 0 | 0 | $0.0041 |
| st-mary-of-the-assumption-baldwinsville | 3 | 8 | 7 | 0 | 1 | 0 | 0 | 0 | 0 | $0.0032 |
| st-mary-our-mother | 3 | 9 | 9 | 1 | 0 | 0 | 0 | 0 | 0 | $0.0025 |
| st-michael-the-archangel-south-glens-falls | 3 | 12 | 12 | 1 | 0 | 0 | 0 | 0 | 0 | $0.0030 |
| st-paul-st-adalbert-mt-carmel-schenectady | 4 | 8 | 7 | 0 | 1 | 0 | 0 | 0 | 0 | $0.0032 |
| st-paul-whitesboro | 4 | 12 | 12 | 0 | 0 | 0 | 1 | 0 | 0 | $0.0044 |
| st-pauls-webster | 3 | 11 | 10 | 0 | 1 | 0 | 0 | 0 | 0 | $0.0047 |
| st-rose-of-lima-north-syracuse | 3 | 10 | 10 | 1 | 0 | 0 | 0 | 0 | 0 | $0.0035 |
| st-theodores-gates | 4 | 15 | 8 | 0 | 1 | 0 | 0 | 0 | 0 | $0.0022 |
| st-vincent-de-paul-albany | 3 | 4 | 3 | 0 | 1 | 0 | 0 | 0 | 0 | $0.0011 |
| the-lords-vineyard | 4 | 31 | 30 | 0 | 1 | 0 | 0 | 0 | 0 | $0.0047 |
| three-catholic-sisters-foothills | 4 | 21 | 20 | 0 | 0 | 1 | 0 | 0 | 0 | $0.0085 |
| tonawanda-catholic | 4 | 37 | 36 | 0 | 1 | 0 | 0 | 0 | 0 | $0.0044 |
| transfiguration-st-catherine-mendon | 3 | 11 | 10 | 0 | 1 | 0 | 0 | 0 | 0 | $0.0024 |
| all-saints-albany | 2 | 12 | 12 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0026 |
| all-saints-on-the-hudson-mechanicville | 4 | 12 | 12 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0025 |
| annunciation-our-lady-queen-of-apostles-ilion | 2 | 16 | 16 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0017 |
| basilica-sacred-heart-syracuse | 2 | 14 | 14 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0018 |
| beloved-disciples-lancaster | 4 | 45 | 45 | 0 | 0 | 0 | 0 | 0 | 1 | $0.0065 |
| blessed-sacrament-albany | 2 | 14 | 14 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0019 |
| blessed-sacrament-st-vincent-de-paul-syracuse | 3 | 17 | 17 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0030 |
| cathedral-immaculate-conception-syracuse | 2 | 18 | 18 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0020 |
| cathedral-st-mary-albany | 4 | 23 | 23 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0040 |
| catholic-communities-of-eastern-broome | 3 | 9 | 9 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0036 |
| catholic-community-buffalo-north | 4 | 19 | 19 | 0 | 0 | 0 | 0 | 0 | 1 | $0.0057 |
| catholic-community-st-stephen-st-patrick-whitney-point | 3 | 15 | 15 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0026 |
| catholic-family-holy-spirit-alden | 3 | 34 | 34 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0042 |
| catholic-neighbors-in-faith | 4 | 25 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0051 |
| catholic-parishes-eastern-wayne-county | 4 | 24 | 24 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0046 |
| ccncc-valatie | 3 | 9 | 9 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0031 |
| cheektowaga-kaisertown-sloan-catholic | 3 | 17 | 17 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0020 |
| christ-our-light-family | 4 | 33 | 31 | 0 | 0 | 0 | 0 | 0 | 2 | $0.0052 |
| christ-sun-of-justice-troy | 2 | 6 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0008 |
| christ-the-good-shepherd-oswego | 4 | 16 | 16 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0034 |
| church-of-the-nativity-tully | 4 | 12 | 12 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0031 |
| downtown-family-buffalo | 4 | 22 | 22 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0049 |
| eternal-flame-catholic-community | 4 | 58 | 54 | 0 | 0 | 0 | 0 | 0 | 4 | $0.0065 |
| fields-of-grace | 4 | 33 | 33 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0042 |
| greater-east-buffalo-catholic | 3 | 28 | 28 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0041 |
| holy-cross-buffalo | 2 | 11 | 11 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0013 |
| holy-cross-morris | 3 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0012 |
| holy-cross-utica | 3 | 6 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0018 |
| holy-family-catholic-community | 4 | 11 | 10 | 0 | 0 | 0 | 0 | 0 | 1 | $0.0034 |
| holy-family-endwell | 2 | 6 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0018 |
| holy-family-st-marianne-cope-syracuse | 4 | 20 | 20 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0053 |
| holy-mother-and-child-st-joseph-st-paul-greenfield-center | 4 | 11 | 11 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0033 |
| holy-trinity-cohoes | 2 | 15 | 15 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0016 |
| holy-trinity-hudson | 4 | 15 | 12 | 0 | 0 | 0 | 0 | 0 | 3 | $0.0032 |
| holy-trinity-st-stephen-fulton | 3 | 12 | 12 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0027 |
| holy-trinity-utica | 3 | 14 | 14 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0038 |
| immaculate-conception-fayetteville | 3 | 9 | 9 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0025 |
| immaculate-conception-greene | 2 | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0011 |
| immaculate-conception-hoosick-falls | 4 | 9 | 9 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0030 |
| immaculate-conception-ithaca | 3 | 16 | 16 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0031 |
| immaculate-conception-st-bridgets | 3 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0011 |
| mary-mother-of-mercy | 3 | 9 | 8 | 0 | 0 | 0 | 0 | 0 | 1 | $0.0019 |
| mary-mother-of-our-savior-utica | 2 | 15 | 15 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0026 |
| most-holy-rosary-maine | 2 | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0012 |
| nativity-seas | 3 | 13 | 13 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0030 |
| net-catholic | 3 | 12 | 12 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0023 |
| one-catholic | 4 | 34 | 34 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0051 |
| one-catholic-family-east-syracuse | 4 | 10 | 10 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0035 |
| our-lady-of-fatima-delanson | 2 | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0009 |
| our-lady-of-hope-copake-falls | 2 | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0010 |
| our-lady-of-hope-fort-plain | 2 | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0009 |
| our-lady-of-lourdes-st-anne | 3 | 13 | 13 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0026 |
| our-lady-of-peace-geneva | 4 | 23 | 23 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0049 |
| our-lady-of-sorrows-vestal | 3 | 9 | 9 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0025 |
| our-lady-of-the-americas-albany | 2 | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0011 |
| our-lady-of-the-annunciation-queensbury | 3 | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0021 |
| our-lady-of-the-assumption-latham | 2 | 9 | 9 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0021 |
| our-lady-of-the-sacred-heart-orchard-park | 2 | 10 | 10 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0021 |
| our-lady-of-the-valley | 3 | 20 | 20 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0037 |
| our-lady-of-the-valley-middleburgh | 2 | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0012 |
| our-lady-of-victory-st-joseph | 2 | 11 | 11 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0009 |
| our-lady-of-victory-troy | 4 | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0030 |
| our-lady-queen-of-peace-st-thomas-more | 4 | 12 | 10 | 0 | 0 | 0 | 0 | 0 | 2 | $0.0029 |
| our-mother-of-sorrows-holy-cross | 3 | 16 | 16 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0040 |
| peace-of-christ | 4 | 15 | 15 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0073 |
| prince-of-peace-north-endicott | 4 | 17 | 16 | 0 | 0 | 0 | 0 | 0 | 1 | $0.0054 |
| sacred-heart-auburn-cluster | 4 | 18 | 18 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0082 |
| sacred-heart-cathedral | 2 | 16 | 16 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0019 |
| sacred-heart-divine-mercy-cicero | 3 | 20 | 15 | 0 | 0 | 0 | 0 | 0 | 5 | $0.0027 |
| sacred-heart-lake-george | 2 | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0014 |
| sacred-heart-margaretville | 3 | 7 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0023 |
| sacred-heart-rome | 4 | 13 | 13 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0034 |
| sacred-heart-sidney | 2 | 6 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0010 |
| sacred-heart-troy | 2 | 10 | 10 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0012 |
| shepherd-and-saints-family | 4 | 36 | 36 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0131 |
| southeast-rochester-catholic-community | 4 | 12 | 12 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0030 |
| ss-cyril-methodius-holy-trinity-binghamton | 4 | 9 | 9 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0021 |
| st-ambrose-latham | 2 | 10 | 10 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0016 |
| st-ann-manlius | 2 | 14 | 14 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0017 |
| st-anthony-of-padua-troy | 2 | 10 | 10 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0012 |
| st-anthony-schenectady | 3 | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0022 |
| st-bartholomew-norwich | 3 | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0016 |
| st-benedict-parish | 4 | 13 | 13 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0117 |
| st-benedicts-st-marys-lake | 4 | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0039 |
| st-cecilia-sacred-heart-fonda | 3 | 6 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0016 |
| st-charles-borromeo | 3 | 11 | 11 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0025 |
| st-charles-st-ann-st-patrick-st-brigid-syracuse | 4 | 10 | 10 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0037 |
| st-christopher | 3 | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0020 |
| st-clement-saratoga-springs | 3 | 10 | 10 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0053 |
| st-elizabeth-ann-seton-baldwinsville | 3 | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0020 |
| st-francis-and-st-clare | 3 | 13 | 13 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0033 |
| st-francis-of-assisi-albany | 4 | 7 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0029 |
| st-francis-of-assisi-binghamton | 3 | 8 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0032 |
| st-gabriel-elma | 3 | 28 | 28 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0040 |
| st-henry-averill-park | 3 | 12 | 12 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0025 |
| st-james-johnson-city | 3 | 18 | 18 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0035 |
| st-jerome | 3 | 11 | 11 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0017 |
| st-joan-of-arc-menands | 3 | 9 | 9 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0012 |
| st-john-greece | 3 | 9 | 9 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0030 |
| st-john-of-rochester | 3 | 17 | 17 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0037 |
| st-john-st-joseph-st-mary-rensselaer | 3 | 19 | 19 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0027 |
| st-john-the-baptist-holy-trinity-syracuse | 3 | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0014 |
| st-john-the-evangelist-camden | 3 | 7 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0017 |
| st-john-the-evangelist-new-hartford | 3 | 9 | 9 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0023 |
| st-john-the-evangelist-schenectady | 3 | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0023 |
| st-john-vianney | 3 | 16 | 16 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0024 |
| st-john-xxiii-west-seneca | 3 | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0021 |
| st-joseph-camillus | 3 | 13 | 13 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0031 |
| st-joseph-cathedral-buffalo | 3 | 11 | 11 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0021 |
| st-joseph-st-mary-st-paul-fort-edward | 3 | 12 | 12 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0022 |
| st-joseph-troy | 2 | 15 | 15 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0024 |
| st-joseph-worcester | 3 | 6 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0013 |
| st-kateri-latin-mass-community | 2 | 8 | 3 | 0 | 0 | 0 | 0 | 0 | 1 | $0.0014 |
| st-katharine-drexel-st-maximilian-kolbe | 4 | 32 | 32 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0062 |
| st-lawrence-otoole-and-sacred-heart | 3 | 25 | 17 | 0 | 0 | 0 | 0 | 0 | 2 | $0.0040 |
| st-louis-pittsford | 3 | 15 | 15 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0040 |
| st-lucy-syracuse | 2 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0013 |
| st-luke-the-evangelist | 4 | 13 | 12 | 0 | 0 | 0 | 0 | 0 | 1 | $0.0030 |
| st-madeleine-sophie-st-gabriel-schenectady | 3 | 13 | 13 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0032 |
| st-malachy-sherburne | 3 | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0022 |
| st-margaret-mattydale | 3 | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0014 |
| st-marianne-cope | 3 | 9 | 9 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0023 |
| st-marks-greece | 3 | 9 | 9 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0026 |
| st-martin-de-porres | 4 | 10 | 10 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0027 |
| st-mary-amsterdam | 2 | 13 | 13 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0020 |
| st-mary-ballston-spa | 4 | 13 | 13 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0044 |
| st-mary-clinton | 3 | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0017 |
| st-mary-cooperstown | 3 | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0017 |
| st-mary-glens-falls | 3 | 7 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0023 |
| st-mary-of-mount-carmel-blessed-sacrament-utica | 3 | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0022 |
| st-mary-of-the-lake-skaneateles | 3 | 9 | 9 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0018 |
| st-mary-oneonta | 3 | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0021 |
| st-mary-st-paul-binghamton | 4 | 12 | 12 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0031 |
| st-mary-waterford | 3 | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0015 |
| st-marys-st-matthew | 3 | 9 | 9 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0022 |
| st-matthew-voorheesville | 3 | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0018 |
| st-michael-cohoes | 3 | 13 | 13 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0026 |
| st-michael-st-peter-our-lady-of-hope-syracuse | 4 | 12 | 12 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0027 |
| st-monica-emmanuel | 3 | 11 | 11 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0032 |
| st-patrick-chittenango | 3 | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0013 |
| st-patrick-st-anthony-chadwicks | 3 | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0013 |
| st-patrick-st-thomas-aquinas-binghamton | 3 | 28 | 28 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0035 |
| st-patricks-family-of-churches | 4 | 13 | 13 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0030 |
| st-paul-norwich | 3 | 7 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0021 |
| st-paul-the-apostle-hancock | 3 | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0019 |
| st-peter-saratoga-springs | 3 | 7 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0023 |
| st-pius-x-chili | 3 | 11 | 11 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0033 |
| st-rita-webster | 3 | 14 | 14 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0036 |
| st-stanislaus-kostka | 3 | 16 | 16 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0035 |
| st-stanislaus-our-lady-of-mount-carmel-amsterdam | 3 | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0022 |
| st-stephen-hagaman | 3 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0012 |
| st-theresa-windham | 3 | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0013 |
| st-thomas-the-apostle-delmar | 3 | 13 | 13 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0024 |
| st-vincent-de-paul-blessed-sacrament-vestal | 3 | 7 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0017 |
| st-vincent-de-paul-cobleskill | 2 | 7 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0010 |
| together-in-christ-family | 4 | 35 | 35 | 0 | 0 | 0 | 0 | 0 | 0 | $0.0065 |
