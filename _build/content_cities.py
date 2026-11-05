# -*- coding: utf-8 -*-
# Service-area cities. Each service page gets one variant per city listed here.
# When re-using this template for a client in another region, rewrite these entries AND the
# "cities" text in each service (content_services.py) for the new towns. Keep the text genuinely local.
# "cat" holds one paragraph per service category (power, wiring, repair).
#
# Local details (checked November 2026): Windsor's local electricity distributor is ENWIN Utilities;
# the Windsor area had major basement flooding in August 2016 and August 2017 (Tecumseh was also hit in 2017);
# Oldcastle is a light-industrial community within the Town of Tecumseh. Electrical permits and inspections in
# Ontario are provincial (ESA), not municipal. The utility serving LaSalle and Tecumseh is deliberately not
# named. CLIENT REVIEW: re-check before launch.

CITIES = [
{
"slug": "windsor",
"name": "Windsor",
"municipality": "City of Windsor",
"region": "Essex County",
"short": "Windsor's century homes, post-war bungalows and newer subdivisions mean everything from knob and tube to EV chargers, often on the same street.",
"title": "Electrician in Windsor, ON",
"desc": "Electrician in Windsor, Ontario: panel upgrades, EV chargers, rewiring, knob and tube replacement, pot lights, generators, repairs and inspections.",
"intro": "Windsor has some of the oldest housing in the region, from Walkerville and Olde Sandwich Towne to Ford City, alongside newer east and south end subdivisions. Each era brings its own wiring.",
"hub": [
"Windsor homeowners call us for panel upgrades on 60 and 100 amp services, knob and tube replacement in pre-war homes, EV chargers in detached garages off the alley, and pot lights in plaster ceilings. In older neighbourhoods, much of the job is understanding what previous owners added over the decades before we change anything.",
"Electrical permits and inspections in Windsor go through the province, not the city, and service upgrades are coordinated with ENWIN Utilities. Below you'll find each of our services with information specific to Windsor homes."
],
"cat": {
"power": "Many Windsor homes still run on 60 or 100 amp services with crowded panels, and plenty have detached garages off rear alleys, which makes EV charger and generator installs a matter of planning the route. Service upgrades here are coordinated with ENWIN Utilities for the disconnect and reconnect.",
"wiring": "Windsor's plaster and lath walls, brick exteriors and balloon framing take patience to wire through. Older homes often have knob and tube in the upper floors, ungrounded outlets and decades of add-ons, so we trace what's there before planning new circuits, pot lights or a renovation.",
"repair": "Summer storms, older services and basements that flooded in 2016 and 2017 keep Windsor repair calls varied: loose connections in old boxes, overloaded circuits, storm-damaged masts and water-damaged wiring. Buyers of older homes here often book an electrical inspection before closing."
},
"permits": "Electrical work in Windsor needs a permit (called a notification) filed with the Electrical Safety Authority, and paid work must be done by an ESA Licensed Electrical Contractor. ESA inspects the work and issues a Certificate of Acceptance, which insurers and buyers often ask for. Service upgrades also involve ENWIN Utilities for the disconnect and reconnect. Utility locates are requested before any digging for buried runs."
},
{
"slug": "lasalle",
"name": "LaSalle",
"municipality": "Town of LaSalle",
"region": "Essex County",
"short": "LaSalle grew quickly from the 1990s on, so most calls here are about adding capacity: EV chargers, hot tubs, pools and finished basements.",
"title": "Electrician in LaSalle, ON",
"desc": "Electrician in LaSalle, Ontario: EV chargers, panel upgrades, hot tub and pool wiring, pot lights, basement wiring, generators, repairs and inspections.",
"intro": "LaSalle's subdivisions are newer, larger and full of things that need power: two-car garages, pools, hot tubs and finished basements, plus older homes along the Detroit River and Front Road.",
"hub": [
"LaSalle homeowners call us to add rather than fix: EV chargers in attached garages, hot tub and pool equipment circuits, pot lights in open-concept main floors and full basement finishes. With so much on one panel, many jobs start with a load calculation to see what the service can carry.",
"Electrical permits and inspections in LaSalle are handled by the province through the Electrical Safety Authority. Below you'll find each of our services with information specific to LaSalle homes."
],
"cat": {
"power": "Most LaSalle homes already have 100 or 200 amp services, but EVs, pool heaters, hot tubs and air conditioners can fill them quickly. A load calculation tells you whether a charger fits as is, needs an energy management system, or calls for a bigger service.",
"wiring": "LaSalle's newer drywall construction makes adding pot lights, outlets and basement circuits straightforward. Larger homes mean longer runs to backyards, decks and garages, and plenty of basements to finish with bars, gyms, theatres and guest suites.",
"repair": "Storm damage, GFCI and arc-fault breakers that trip with certain equipment, outdoor outlets that let water in and work added by previous owners without permits are the usual LaSalle repair calls. Inspections here often check what was added after the house was built."
},
"permits": "Electrical work in LaSalle needs a permit (a notification) filed with the Electrical Safety Authority, and paid work must be done by an ESA Licensed Electrical Contractor. ESA inspects the work and issues a Certificate of Acceptance. Hot tubs, pools and EV chargers are all permitted work. Service upgrades also need the local utility for the disconnect and reconnect, and buried runs need utility locates before digging."
},
{
"slug": "tecumseh",
"name": "Tecumseh",
"municipality": "Town of Tecumseh",
"region": "Essex County",
"short": "Tecumseh mixes 1960s and 1970s homes, newer subdivisions, a rural edge and the Oldcastle industrial area, so the work ranges from aluminum wiring to three-phase.",
"title": "Electrician in Tecumseh, ON",
"desc": "Electrician in Tecumseh, Ontario: panel upgrades, aluminum wiring repairs, EV chargers, generators, pot lights, commercial electrical and inspections.",
"intro": "Tecumseh runs from its original core and 1960s and 1970s neighbourhoods to newer subdivisions, rural properties and the Oldcastle industrial area, which gives it the widest mix of electrical work in the area.",
"hub": [
"Tecumseh homeowners call us about original 100 amp panels, aluminum branch wiring in homes from the mid-1960s to the late 1970s, generators and sump pump circuits after the 2017 flooding, and feeds to shops and outbuildings on larger lots. Businesses in Oldcastle call us for equipment circuits and lighting.",
"Electrical permits and inspections in Tecumseh are handled by the province through the Electrical Safety Authority. Below you'll find each of our services with information specific to Tecumseh properties."
],
"cat": {
"power": "Tecumseh's 1960s and 1970s homes often still have their original 100 amp panels, while rural properties may run a house, shop and well pump on one service. Generators are popular here after the 2017 flooding, and long runs to detached garages and shops need careful sizing.",
"wiring": "Aluminum branch wiring is common in Tecumseh homes from the mid-1960s to the late 1970s, so outlet, switch and lighting work here is done with connectors approved for aluminum. Split-levels and bungalows brighten up dramatically with pot lights, and larger lots mean garage and shop circuits.",
"repair": "Tecumseh repair and inspection calls often involve aluminum connections, aging outbuilding feeds and storm damage on the rural edge. In Oldcastle, commercial work centres on machinery, three-phase power and keeping production running."
},
"permits": "Electrical work in Tecumseh needs a permit (a notification) filed with the Electrical Safety Authority, and paid work must be done by an ESA Licensed Electrical Contractor. ESA inspects the work and issues a Certificate of Acceptance. Feeds to shops and outbuildings are permitted work too. Service upgrades also need the local utility for the disconnect and reconnect, and buried runs need utility locates before digging."
},
]
