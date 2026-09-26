---
parish: christ-the-good-shepherd-oswego
name: Our Lady of Perpetual Help
line1: 2913 State Route 48
line2: ''
city: Minetto
state: NY
postal_code: '13115'
latitude: 43.4074375
longitude: -76.4773125
coordinates_from: gcatholic-plus-code
name_verified: true
address_verified: true
roster: ['gcatholic:17963', 'directory:33066']
evidence:
- url: https://gcatholic.org/churches/usa-02/17963
  seen: 2026-09-25
  quote: W River Rd., Minetto, New York 13115-0236
  note: 'Listed in GCatholic: churches of the Roman Catholic Diocese of Syracuse as ''Our Lady of Perpetual
    Help'', W River Rd., Minetto, NY, 13115; kind: Church'
- url: https://www.syracusediocese.org/parishfinder
  seen: 2026-09-26
  note: Listed in Diocese of Syracuse parish finder (Mass-times map) as 'Our Lady of Perpetual Help',
    2912 NY-48, Minetto, NY, 13115-0236
- url: https://www.church-bulletin.org/bulletin/christ-the-good-shepherd-parish-oswego-ny-13126/2026-09-27.pdf
  seen: 2026-09-26
  quote: 'Saturday: 4:00 pm - Our Lady of Perpetual Help'
  note: 'Page 1 of the 27 September 2026 bulletin. The masthead gives the church''s address as 2913 State
    Route 48, Minetto (the text layer doubles final letters: "29133 Statee Routee 488  Minetto"), and the
    schedule has Saturday 4:00 pm and Sunday 9:00 am here.'
- url: https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=43.4074375&lon=-76.4773125&zoom=18
  seen: 2026-09-26
  quote: 2913, State Route 48
  note: OSM reverse geocode of GCatholic's Plus Code for this church lands on the address point 2913 State
    Route 48, independent of the parish.
---

## Holds Mass

Yes, weekly. The 27 September 2026 Christ the Good Shepherd bulletin (page 1) lists Saturday 4:00 pm
and Sunday 9:00 am at Our Lady of Perpetual Help, and its page-2 intentions have "4:00pm - OLPH" and
"9:00am - OLPH" for 26 and 27 September. It is a mission served from Christ the Good Shepherd, Oswego,
and shares its bulletin.

## Name and address

The name is the same in the bulletin, the diocese directory and GCatholic, so `name_verified` is true.
The address differs:

- 2913 State Route 48, Minetto: the bulletin masthead.
- 2912 NY-48: the diocese directory, whose map pin sits about 1 km south, in Minetto village
  (43.39840, -76.47845, reverse-geocoding to County Route 24), so it is only a town pin.
- W River Rd.: GCatholic, without a number. Its Plus Code (87M5CGW...) reverse-geocodes in OSM to the
  address point "2913, State Route 48", i.e. the same place the bulletin names.

Modelled at 2913 State Route 48, where the bulletin and OSM's address point at GCatholic's Plus Code
agree; `address_verified` is true on that basis. The directory's 2912 is taken as a typo. Postal code
13115 (Minetto) is GCatholic's; OSM puts the point in 13126 (Oswego) because it lies just inside the
city line. Coordinates are GCatholic's Plus Code.
