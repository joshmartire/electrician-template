# -*- coding: utf-8 -*-
# Electrical services. Each entry becomes a service page (500-600 words of main content together with its
# COSTS entry and FAQs) plus one page per city in content_cities.py.
#
# Tokens: {biz} = business name, {phone} = phone number, {esa} = the inspection authority's short name from
# site.config.json ("inspection_short", ESA in Ontario), [[slug|anchor text]] = link to another service (or
# [[contact|...]], [[estimate|...]], [[area:windsor|...]]). Links to services the client does not offer become
# plain text and are listed in _build/removed-service-mentions.txt for rewording.
#
# "cities" holds one short paragraph per city slug. It must be genuinely about that town, not a
# find-and-replace of the city name.
#
# Facts used in the copy (Ontario, checked November 2026): electrical work done for pay must be done by an
# ESA Licensed Electrical Contractor, who files the permit (a "notification") with the Electrical Safety
# Authority; ESA inspects the work and issues a Certificate of Acceptance; homeowners can check a contractor's
# licence on ESA's website. Work must meet the Ontario Electrical Safety Code. A generator connected to a home
# needs an interlock or transfer switch so it can't feed power back into the utility lines. An EV energy
# management system can let an EV charger share capacity on a smaller service. Re-check these if the template
# is used outside Ontario (US clients: local permit office, NEC, state contractor licence).

SERVICES = [
# ------------------------------------------------------------------ POWER & PANELS
{
"slug": "panel-upgrades",
"name": "Panel Upgrades",
"cat": "power",
"icon": "panel",
"short": "New breaker panels and service upgrades from 60 or 100 amps to 200 amps or more, coordinated with your utility and inspected.",
"title": "Electrical Panel Upgrades | 100 A to 200 A Service",
"desc": "Electrical panel replacement and service upgrades from 60 or 100 amps to 200 amps, with utility coordination, an ESA permit and inspection.",
"h1": "Panel Upgrades",
"lead": "The panel is the heart of the house. When it's full, outdated or too small for an EV, a heat pump or a hot tub, we replace it and size the service for what's next.",
"body": """
<p>Most homes built before the 1980s were wired for 60 or 100 amps, with a fuse box or a panel that has no free spaces left. Add central air, an induction range, a hot tub or an electric car and the numbers stop working. {biz} replaces panels and upgrades services so the house has the capacity it needs, with every circuit labelled and room to grow.</p>
<h2>What's included</h2>
<ul>
<li><strong>Load calculation</strong> — we add up what the house uses now and what you're planning, so the new service is sized properly, not guessed.</li>
<li><strong>Utility coordination</strong> — we arrange the disconnect and reconnect with your local utility, so power is off for as little time as possible.</li>
<li><strong>New panel and breakers</strong> — a quality panel with free spaces, new breakers, and arc-fault and ground-fault protection where the code requires it.</li>
<li><strong>Meter base and mast</strong> — replaced when the service size goes up, along with the service entrance cable.</li>
<li><strong>Grounding and bonding</strong> — brought up to current requirements, including water and gas piping bonds.</li>
<li><strong>Permit and inspection</strong> — we file the {esa} permit and the work is inspected before the job is closed out.</li>
</ul>
<h2>How the job runs</h2>
<ol>
<li><strong>Site visit.</strong> We look at the panel, the meter, the service drop and your plans for the next few years.</li>
<li><strong>Written quote.</strong> Panel size, service work, any extra circuits and what isn't included, spelled out.</li>
<li><strong>Upgrade day.</strong> Most panel swaps take one day. Power is off for part of it, and we tell you when.</li>
<li><strong>Inspection and labels.</strong> Every breaker is labelled, and you get the paperwork for your records and your insurer.</li>
</ol>
<h2>Signs it's time</h2>
<p>Breakers that trip often, a panel that's warm to the touch, fuses, double-tapped breakers or no room for new circuits all point to an upgrade. Planning a charger? Pair the upgrade with [[ev-charger-installation|EV charger installation]], or check a ballpark in the [[estimate|instant electrical estimate]].</p>
""",
"faqs": [
("How long does a panel upgrade take?", "Most residential panel replacements and 200 amp upgrades are done in one day. Your power is off for part of that day, and the utility reconnects the service once the work is ready."),
("Do I need 200 amps?", "Not always. Many homes do fine on 100 amps. A load calculation tells you for sure, especially if you're adding an EV charger, a heat pump, a hot tub or electric heat."),
("Will my insurance company want to know?", "Often, yes. Insurers commonly ask about panel age and fuses. The inspection paperwork from the upgrade is what they usually want to see."),
("Can you move my panel?", "Yes. Panels are often moved out of closets, bathrooms or finished spaces during an upgrade. Moving it adds work, so it's priced in the quote."),
],
"related": ["ev-charger-installation", "surge-protection", "home-rewiring"],
"cities": {
"windsor": "Windsor has thousands of pre-war and post-war homes still on 60 or 100 amp services, many with the panel tucked into a basement corner beside the old fuse box. ENWIN Utilities handles the disconnect and reconnect for Windsor service upgrades, and we book that with them so your power is back on the same day.",
"lasalle": "Most LaSalle homes already have 100 or 200 amp services, so upgrades here are usually about capacity: a second EV, a pool heater, a hot tub and a finished basement all on one panel. A load calculation often shows whether a bigger service or a smarter layout is the right answer.",
"tecumseh": "Tecumseh's 1960s and 1970s homes are prime candidates: original 100 amp panels, full of breakers, sometimes with aluminum branch wiring behind them. We check the condition of those connections during the upgrade, since a new panel is the right time to deal with them."
}
},
{
"slug": "ev-charger-installation",
"name": "EV Charger Installation",
"cat": "power",
"icon": "ev",
"short": "Level 2 home EV chargers installed on a dedicated 240 V circuit, with a load calculation and an energy management option for smaller panels.",
"title": "EV Charger Installation | Level 2 Home Charging",
"desc": "Level 2 EV charger installation at home: dedicated 240 V circuit, load calculation, EV energy management for smaller panels, ESA permit and inspection.",
"h1": "EV Charger Installation",
"lead": "Plug in at night, wake up full. A Level 2 charger on its own 240 V circuit, installed so it charges at full speed without overloading the house.",
"body": """
<p>A regular outlet adds only a few kilometres of range an hour. A Level 2 charger on a dedicated 240 V circuit adds most of a day's driving in a couple of hours, which is why nearly every EV owner ends up wanting one. The charger itself is the easy part. The real work is making sure your panel can carry the load and running the circuit cleanly to where you park.</p>
<h2>What's included</h2>
<ul>
<li><strong>Load calculation</strong> — we check what your panel can spare before anything is installed, so the charger and the air conditioner can run at the same time.</li>
<li><strong>Dedicated 240 V circuit</strong> — sized for your charger, with the right breaker and wire for a continuous load.</li>
<li><strong>Clean wire run</strong> — through the basement and garage, in conduit where it's exposed, to the spot that suits your car's charging port.</li>
<li><strong>Charger mounting</strong> — hard-wired or a 240 V receptacle, depending on the charger, indoors or weatherproof outdoors.</li>
<li><strong>Energy management option</strong> — for smaller services, a device that shares capacity so the charger slows down when the house is busy.</li>
<li><strong>Permit and inspection</strong> — the {esa} permit is filed and the installation is inspected.</li>
</ul>
<h2>Which charger should I buy?</h2>
<p>Buy a charger certified for use in Canada (look for a CSA, cUL or cETL mark), sized to what your car can actually take. Many cars charge at about 32 amps, which needs a 40 amp circuit. Faster cars benefit from a 60 amp circuit. If you're not sure, we'll recommend one before you buy, or supply it with the installation.</p>
<h2>When the panel is too small</h2>
<p>An older 100 amp panel doesn't automatically mean an upgrade. An EV energy management system can let the charger share capacity safely. If the house needs more power anyway, we'll quote a [[panel-upgrades|panel upgrade]] alongside it. Price yours in the [[estimate|instant electrical estimate]].</p>
""",
"faqs": [
("How long does an EV charger installation take?", "Most installations take half a day to a day once the permit is filed. Longer runs, detached garages and panel work take longer."),
("Can I install the charger myself?", "Charger wiring connects to your panel, so in Ontario it needs a permit and inspection, and paid work must be done by a licensed electrical contractor."),
("Do I need a 200 amp panel for an EV charger?", "No. Many 100 amp homes can add a charger with a load calculation, or with an energy management system that shares capacity with the rest of the house."),
("Can the charger go outside?", "Yes. Outdoor chargers need a weatherproof rating and a weatherproof connection. We mount them where the cable reaches your port without crossing a walkway."),
],
"related": ["panel-upgrades", "surge-protection", "outlets-switches"],
"cities": {
"windsor": "Plenty of Windsor homes have a detached garage off a rear alley, so the charger often goes in the garage on a feed buried from the house, or on the house wall facing the driveway. Older Windsor services make the load calculation especially important here, and an energy management system often saves a full upgrade.",
"lasalle": "LaSalle's attached two-car garages make for some of the simplest EV installs in the region: a short run from the basement panel, straight up into the garage. With many families on their second electric vehicle, we often plan the circuit and the panel space so a second charger can follow.",
"tecumseh": "In Tecumseh we install everything from garage chargers in newer subdivisions to outdoor units on long driveways closer to Oldcastle, where the run from the panel can be long. Longer runs need heavier wire to keep the voltage up, which is why we measure the route before we price it."
}
},
{
"slug": "generator-installation",
"name": "Generator Installation",
"cat": "power",
"icon": "generator",
"short": "Generator inlets, interlocks, transfer switches and standby generator hookups, so the fridge, furnace and sump pump keep running in an outage.",
"title": "Generator Installation | Inlets, Interlocks & Transfer Switches",
"desc": "Home generator installation: inlet boxes, panel interlocks, transfer switches and standby generator hookups, wired safely with an ESA permit.",
"h1": "Generator Installation",
"lead": "Keep the sump pump, furnace and fridge running when the grid goes down, with a hookup that's safe for you and for the line crews working outside.",
"body": """
<p>Running extension cords from a generator through a window works for a lamp. It doesn't run a furnace or a sump pump, and back-feeding a panel through a homemade cord can energize the utility lines and seriously hurt a line worker. A proper generator connection lets you power the circuits you choose from one safe connection point. {biz} installs connections for portable generators and hooks up permanent standby units.</p>
<h2>What's included</h2>
<ul>
<li><strong>Circuit planning</strong> — we match what you want to keep running (sump pump, furnace, fridge, a few lights) to what your generator can actually supply.</li>
<li><strong>Inlet box</strong> — a weatherproof outdoor inlet so the generator cord plugs in outside the house, away from windows and doors.</li>
<li><strong>Interlock or transfer switch</strong> — the device that makes it impossible to feed power back into the utility lines.</li>
<li><strong>Standby hookups</strong> — wiring and transfer equipment for a permanent natural gas generator, with the gas line run by a licensed gas fitter.</li>
<li><strong>Permit and inspection</strong> — the {esa} permit is filed and the work is inspected.</li>
<li><strong>Walk-through</strong> — we show you how to switch over safely, in the right order, before you ever need to.</li>
</ul>
<h2>Portable or standby?</h2>
<p>A portable generator with an inlet and interlock is the most affordable way to ride out an outage, but you have to be home to start it and you'll be refuelling it. A standby generator starts on its own within seconds and runs on natural gas, which matters most when nobody is home to start the sump pump in a storm. For both, a [[surge-protection|whole-home surge protector]] protects electronics when the power comes back.</p>
<p>Want a ballpark first? Price a generator hookup in the [[estimate|instant electrical estimate]].</p>
""",
"faqs": [
("Why can't I just plug the generator into an outlet?", "A cord with two male ends can back-feed the utility lines, which can seriously injure line workers and damage your equipment. An interlock or transfer switch prevents that."),
("What size generator do I need?", "It depends on what you want to run. A sump pump, furnace fan, fridge and some lights are well within the reach of many portable units. We help you size it before you buy."),
("Where can the generator sit?", "Outdoors, away from windows, doors and vents, because of carbon monoxide. Standby units have clearance requirements from the manufacturer that we follow."),
("Does a standby generator need a gas permit too?", "Yes. The gas connection is separate work done by a licensed gas fitter. We coordinate with them so the electrical side is ready when they are."),
],
"related": ["surge-protection", "panel-upgrades", "electrical-repair"],
"cities": {
"windsor": "Windsor's August 2016 and 2017 rainstorms flooded thousands of basements, and many of those homes lost their sump pumps when they needed them most. That's why so many Windsor generator calls start with the sump pump circuit, and why we often add a dedicated circuit for it during the installation.",
"lasalle": "LaSalle homes with finished basements, pools and well-equipped kitchens have a lot to protect when the power goes out. A transfer switch lets you pick exactly which circuits the generator feeds, and many LaSalle homeowners choose a standby unit so the house switches over even when they're away.",
"tecumseh": "Tecumseh saw serious basement flooding in the 2017 storms, and homes on the town's rural edge can wait longer for power to come back after an outage. Generator hookups here usually cover the sump pump, the furnace and the fridge, and sometimes a well pump or a shop on the property."
}
},
{
"slug": "surge-protection",
"name": "Surge Protection",
"cat": "power",
"icon": "surge",
"short": "Whole-home surge protectors installed at the panel to shield furnaces, appliances, chargers and electronics from voltage spikes.",
"title": "Whole-Home Surge Protection | Panel Surge Protectors",
"desc": "Whole-home surge protector installation at your electrical panel, protecting furnaces, appliances, EV chargers and electronics from voltage spikes.",
"h1": "Surge Protection",
"lead": "One device at the panel that protects everything plugged into the house, from the furnace board to the TV, when the voltage spikes.",
"body": """
<p>Today's homes are full of circuit boards: furnaces, air conditioners, fridges, washers, ranges, chargers, TVs and routers. A surge from lightning, a utility switching event or the power coming back after an outage can damage them all at once. Power bars protect the few things plugged into them. A whole-home surge protector at the panel protects every circuit in the house.</p>
<h2>What's included</h2>
<ul>
<li><strong>Panel assessment</strong> — we check the panel, its grounding and whether there's a free space for the protector.</li>
<li><strong>Surge protector</strong> — a quality whole-home device rated for residential panels, mounted at or in the panel.</li>
<li><strong>Short, clean connections</strong> — a surge protector performs better with short leads, so we place it as close to the breaker as possible.</li>
<li><strong>Grounding check</strong> — the protector is only as good as the ground it drains to, so we confirm the grounding and bonding.</li>
<li><strong>Permit and inspection</strong> — the {esa} permit is filed for the installation.</li>
</ul>
<h2>How it works with power bars</h2>
<p>Think of it as two layers. The panel protector takes the big hits coming in from outside, and good power bars at the TV and computer handle the smaller spikes made inside the house by motors and appliances. Together they cover far more than either one alone.</p>
<h2>When to add one</h2>
<p>The easiest time is during other panel work, so it's often added with a [[panel-upgrades|panel upgrade]], an [[ev-charger-installation|EV charger]] or a [[generator-installation|generator hookup]]. It can also be installed on its own in an hour or two on most panels.</p>
<p>Not sure your panel has room? [[contact|Send us a photo]] of it with the door open and we'll tell you.</p>
""",
"faqs": [
("Does a surge protector stop lightning?", "No device stops a direct lightning strike. A whole-home protector greatly reduces the damage from surges, which are far more common than direct strikes."),
("How long does a surge protector last?", "Surge protectors wear out as they absorb surges. Most have an indicator light that shows they're still protecting. When it goes out, the device is replaced."),
("Do I still need power bars?", "Yes, for sensitive electronics. The panel protector handles surges from outside, and good power bars handle the smaller ones made inside the house."),
("Will it work with an older panel?", "Usually. Some older panels have no free space or poor grounding, which we'd point out and fix as part of the job."),
],
"related": ["panel-upgrades", "generator-installation", "electrical-inspections"],
"cities": {
"windsor": "Windsor's summer thunderstorms bring plenty of lightning and short outages, and every outage ends with the power snapping back on. In older Windsor homes we pay particular attention to the grounding, since a surge protector on an old water-pipe ground can't do its job properly.",
"lasalle": "LaSalle homes tend to be full of electronics worth protecting: smart thermostats, high-efficiency furnaces, pool equipment, home offices and EV chargers. A whole-home protector is an inexpensive layer of insurance for all of it, and it's often added when a charger or hot tub goes in.",
"tecumseh": "Homes on Tecumseh's rural edge sit at the end of long overhead lines, where storms and switching on the utility side are felt more. We often recommend protection there for well pumps and shop equipment as well as the house itself."
}
},
# ------------------------------------------------------------------ WIRING & LIGHTING
{
"slug": "home-rewiring",
"name": "Home Rewiring",
"cat": "wiring",
"icon": "wire",
"short": "Full and partial rewiring of older homes, including aluminum wiring repairs, ungrounded outlets and overloaded circuits.",
"title": "Home Rewiring | Older Homes & Aluminum Wiring",
"desc": "Full and partial home rewiring for older houses: new circuits, grounded outlets, aluminum wiring repairs and updated panels, with an ESA permit.",
"h1": "Home Rewiring",
"lead": "Old wiring wasn't built for today's homes. We replace it room by room or all at once, with as little damage to your walls as the house allows.",
"body": """
<p>Two-prong outlets, cloth-covered cable, aluminum branch wiring and circuits that trip when the kettle and toaster run together are all signs of a wiring system built for a different era. Rewiring sounds disruptive, but it usually isn't a gut job. {biz} plans each run to use attics, basements and closets, so most of the new wire travels behind finished walls with small, patchable openings.</p>
<h2>What's included</h2>
<ul>
<li><strong>Wiring assessment</strong> — we open boxes, test circuits and map what's there, so the quote is based on the house, not a guess.</li>
<li><strong>New circuits</strong> — copper wiring with a ground, sized for today's loads, with kitchens and laundry on their own circuits.</li>
<li><strong>Grounded, modern outlets</strong> — tamper-resistant receptacles, and GFCI and arc-fault protection where the code calls for it.</li>
<li><strong>Aluminum wiring repairs</strong> — every connection made with connectors approved for aluminum, or the circuit replaced.</li>
<li><strong>Careful access</strong> — small openings, dust control and protected floors, with the holes we make patched and ready for paint.</li>
<li><strong>Permit and inspection</strong> — the {esa} permit is filed and the work is inspected.</li>
</ul>
<h2>Partial or full rewire?</h2>
<p>Not every house needs everything replaced. Sometimes the right job is the kitchen, the bedrooms and the basement, leaving newer circuits alone. We show you what we found and let you choose the scope. Older homes with original wiring often need [[knob-and-tube-replacement|knob and tube replacement]] as well, and a rewire is the right time for a [[panel-upgrades|panel upgrade]].</p>
<h2>Aluminum wiring</h2>
<p>Aluminum branch wiring, common in homes built in the mid-1960s to the late 1970s, can overheat at loose or incompatible connections. The usual fix is to remake every connection with approved connectors, which is often far less work than a full rewire.</p>
""",
"faqs": [
("Do we have to move out during a rewire?", "Usually not. We work room by room and keep power on to the rest of the house at the end of each day."),
("How long does rewiring take?", "A partial rewire can take a few days. A full rewire of a typical house takes one to three weeks, depending on size, access and how much is replaced."),
("Will my walls be torn apart?", "No. We use attics, basements and closets wherever we can, and make small openings elsewhere. The openings we make are patched, ready for paint."),
("Is aluminum wiring dangerous?", "It can be, at connections that loosen or use the wrong devices. Remaking those connections with approved connectors is the standard fix."),
],
"related": ["knob-and-tube-replacement", "panel-upgrades", "electrical-inspections"],
"cities": {
"windsor": "Windsor's plaster and lath walls, brick exteriors and balloon-framed century homes make rewiring a careful job: routes that use the original chases, basement ceilings and attic floors save a lot of patching. Walkerville, Olde Sandwich Towne and the older parts of the east end are full of homes where we find two or three generations of wiring in one house.",
"lasalle": "LaSalle's newer homes rarely need full rewiring. What we do here is partial: an older riverfront home, a basement wired by a previous owner without a permit, or circuits that can't keep up with a renovated kitchen. We test and fix what's needed and leave sound wiring alone.",
"tecumseh": "Tecumseh has a lot of homes built in the mid-1960s to the late 1970s, which is exactly when aluminum branch wiring was used. Before quoting a rewire there, we check whether remaking the connections with approved connectors will do the job, since it often will."
}
},
{
"slug": "knob-and-tube-replacement",
"name": "Knob & Tube Replacement",
"cat": "wiring",
"icon": "knob",
"short": "Removal and replacement of knob and tube wiring in older homes, with documentation for insurance and home sales.",
"title": "Knob and Tube Wiring Replacement | Older Homes",
"desc": "Knob and tube wiring replacement for older homes: live circuits found and replaced with grounded wiring, plus inspection paperwork for insurers.",
"h1": "Knob & Tube Replacement",
"lead": "The wiring that came with your century home has done its time. We find every live run, replace it with grounded circuits and give you the paperwork your insurer wants.",
"body": """
<p>Knob and tube wiring was standard in homes built before about 1950: single wires run on ceramic knobs and through ceramic tubes, with no ground. Much of it still works, but its insulation is now brittle, it was never meant to be buried in insulation, and decades of add-ons have often been spliced into it. Many insurers won't cover a home with live knob and tube, or charge more until it's gone.</p>
<h2>What's included</h2>
<ul>
<li><strong>Tracing every circuit</strong> — we find what's still live and what's been abandoned, in the attic, the basement and the walls.</li>
<li><strong>New grounded wiring</strong> — each knob and tube run replaced with modern copper cable, with grounded, tamper-resistant outlets.</li>
<li><strong>Disconnecting the old system</strong> — live knob and tube is disconnected at the source, so nothing old is left energized.</li>
<li><strong>Careful access</strong> — attic floors, basement ceilings and closets used first, with small openings elsewhere and patching included.</li>
<li><strong>Paperwork</strong> — the {esa} permit and inspection, and a letter for your insurance company listing what was replaced.</li>
</ul>
<h2>How the job runs</h2>
<ol>
<li><strong>Assessment.</strong> We trace the system and show you how much knob and tube is still live.</li>
<li><strong>Written quote.</strong> Every circuit, the access plan and the patching, in writing.</li>
<li><strong>Replacement.</strong> Room by room, with power restored at the end of each day.</li>
<li><strong>Inspection and paperwork.</strong> You get the documents your insurer and any future buyer will ask for.</li>
</ol>
<p>Knob and tube homes usually have small, older services too, so this work is often paired with a [[panel-upgrades|panel upgrade]] or a broader [[home-rewiring|rewire]]. Buying a home that has it? An [[electrical-inspections|electrical inspection]] tells you what you're dealing with before you close.</p>
""",
"faqs": [
("Is knob and tube wiring illegal?", "Existing knob and tube isn't illegal in itself, but it can't be extended, and many insurers restrict coverage on homes where it's still live."),
("How do I know if I have knob and tube?", "Look in the basement and attic for single wires on white ceramic knobs or passing through ceramic tubes. We can confirm it and tell you how much is live."),
("How much of my house will be opened up?", "As little as possible. Most runs are reached from the attic and basement. Small openings elsewhere are patched, ready for paint."),
("Will my insurance company accept the work?", "That's what the paperwork is for. Most insurers ask for proof that the knob and tube was replaced and inspected, which you'll have when we finish."),
],
"related": ["home-rewiring", "panel-upgrades", "electrical-inspections"],
"cities": {
"windsor": "Windsor has one of the region's largest stocks of pre-1950 homes, from Walkerville and Olde Sandwich Towne to the streets around Ottawa Street and Ford City. We regularly find knob and tube still live in their upper floors, often spliced into newer cable by a previous owner, and we trace every run before we quote.",
"lasalle": "Knob and tube is rare in LaSalle's newer subdivisions, but older homes along the river and in the town's original core can still have it. Buyers moving into those homes often call us after an insurer asks the question, and the paperwork from the replacement answers it.",
"tecumseh": "Tecumseh's oldest homes, around the original town core and older farmhouses on its rural edge, are where we find knob and tube in this area. Farmhouses often have it in the attic alongside wiring added for outbuildings, so we trace both before we plan the replacement."
}
},
{
"slug": "pot-lights",
"name": "Pot Lights & Lighting",
"cat": "wiring",
"icon": "potlight",
"short": "Slim LED pot lights, dimmers, under-cabinet and exterior lighting, laid out properly and installed with minimal patching.",
"title": "Pot Light Installation | LED Pot Lights & Dimmers",
"desc": "Slim LED pot light installation with dimmers, plus under-cabinet, feature and exterior lighting, laid out properly and installed with minimal patching.",
"h1": "Pot Lights & Lighting",
"lead": "Even, bright light that makes a room feel bigger, with slim LED pot lights laid out on a plan instead of guessed, and dimmers so you can set the mood.",
"body": """
<p>Pot lights are the most requested lighting upgrade we do, and the difference between good and bad pot lights is mostly the layout. Too few and the room has dark corners; too many in a grid and it looks like an office. {biz} plans spacing around how you use the room: where the furniture goes, where you cook, where the art hangs.</p>
<h2>What's included</h2>
<ul>
<li><strong>Lighting layout</strong> — spacing and placement planned for the room, marked on the ceiling for your approval before we cut.</li>
<li><strong>Slim LED pot lights</strong> — thin, energy-efficient fixtures rated for the ceiling they go in, in the colour temperature you choose.</li>
<li><strong>Wiring and switching</strong> — fished through finished ceilings or run through open joists, on the switches and dimmers you want.</li>
<li><strong>Dimmers that match</strong> — dimmers compatible with LED fixtures, so the lights dim smoothly without flicker or buzz.</li>
<li><strong>Minimal patching</strong> — access holes kept small and patched, ready for paint.</li>
<li><strong>Permit and inspection</strong> — the {esa} permit is filed and the work is inspected.</li>
</ul>
<h2>Beyond pot lights</h2>
<p>We also install under-cabinet lighting, pendants over islands, chandeliers, stair and step lights, and exterior soffit, landscape and security lighting. In a renovation, lighting is easiest to add before the drywall goes up, so it's often part of [[renovation-wiring|renovation and basement wiring]].</p>
<h2>Choosing a colour</h2>
<p>Warm white (around 2700 to 3000 K) suits living rooms and bedrooms. Kitchens and bathrooms often suit a slightly cooler light. Colour-selectable fixtures let you pick after they're in. Want a number before we visit? Price your pot lights in the [[estimate|instant electrical estimate]].</p>
""",
"faqs": [
("How many pot lights do I need?", "It depends on the room size, ceiling height and how bright you like it. A typical living room takes six to ten. We lay them out on the ceiling before we cut."),
("Can you install pot lights without opening the ceiling?", "Mostly, yes. Wires are fished between the fixture holes, with a few small access holes where joists get in the way. Those holes are patched."),
("Can pot lights go under an insulated attic?", "Yes, using fixtures rated for contact with insulation and sealed against air leaks, so you don't lose heat into the attic."),
("Why do my LED lights flicker on the dimmer?", "Usually the dimmer isn't compatible with the LEDs. Replacing it with an LED-rated dimmer usually fixes the flicker."),
],
"related": ["renovation-wiring", "outlets-switches", "home-rewiring"],
"cities": {
"windsor": "Windsor's older homes often have one ceiling fixture per room and plaster ceilings that crack if they're cut carelessly. We cut plaster with the right tools, fish carefully between joists and lay the lights out around the room's original features, like crown moulding and archways.",
"lasalle": "In LaSalle we install a lot of pot lights in open-concept main floors, kitchens with islands and finished basements, often with separate dimmer zones for cooking, eating and relaxing. Soffit lighting for the front of the house and the backyard is a popular add-on here too.",
"tecumseh": "Tecumseh's 1970s split-levels and bungalows tend to have low, dark living rooms that brighten dramatically with pot lights. Slim fixtures need very little depth, so they fit under the main floor in basements and in ceilings with little room above."
}
},
{
"slug": "outlets-switches",
"name": "Outlets & Switches",
"cat": "wiring",
"icon": "outlet",
"short": "New outlets and circuits, GFCI and USB outlets, smart switches and dedicated circuits for appliances, workshops and home offices.",
"title": "Outlets, Switches & New Circuits | GFCI & USB",
"desc": "New outlets and dedicated circuits, GFCI, USB and tamper-resistant outlets, smart switches and dimmers, installed properly with an ESA permit.",
"h1": "Outlets & Switches",
"lead": "More outlets where you actually need them, safer outlets where the code says you should have them, and switches that do what you want.",
"body": """
<p>Most homes don't have enough outlets in the right places, and many still have two-prong or worn-out outlets that don't hold a plug. Extension cords and power bars daisy-chained across a room are a fire risk. {biz} adds outlets and circuits properly, from the panel or from a circuit that has the capacity, and upgrades old devices to the safer ones the code now expects.</p>
<h2>What's included</h2>
<ul>
<li><strong>New outlets</strong> — added where you need them, on a circuit with room to spare.</li>
<li><strong>Dedicated circuits</strong> — for freezers, microwaves, space heaters, workshops, home gyms and offices, so one appliance can't trip the rest.</li>
<li><strong>GFCI protection</strong> — in kitchens, bathrooms, laundry rooms, garages and outdoors, where water and electricity meet.</li>
<li><strong>Tamper-resistant and USB outlets</strong> — child-safe receptacles, and USB-C outlets by the bed or the counter.</li>
<li><strong>Switches and dimmers</strong> — three-way switching for stairs and hallways, smart switches and LED-compatible dimmers.</li>
<li><strong>Permit and inspection</strong> — the {esa} permit is filed and the work is inspected.</li>
</ul>
<h2>Two-prong outlets</h2>
<p>Two-prong outlets mean the circuit has no ground. Swapping in a three-prong outlet without a ground is unsafe and misleading. The right fixes are running a new grounded circuit, or GFCI protection labelled as having no equipment ground, which the code allows in some cases. We'll explain which suits your house. Lots of ungrounded outlets usually point to [[home-rewiring|rewiring]].</p>
<p>Adding outlets outdoors, in a garage or for a hot tub? See [[hot-tub-wiring|hot tub wiring]], or get a ballpark in the [[estimate|instant electrical estimate]].</p>
""",
"faqs": [
("Can you add an outlet anywhere?", "Almost. We check what's in the wall and which circuit can supply it. Exterior walls, tile and old plaster take a little more care."),
("Why does my bathroom outlet keep tripping?", "GFCI outlets trip when they sense current leaking, which can mean a faulty appliance, moisture in an outdoor outlet on the same circuit, or a worn-out GFCI."),
("What's a dedicated circuit?", "A circuit that feeds one appliance or outlet only, with its own breaker. Freezers, microwaves and workshop tools are common examples."),
("Are USB outlets worth it?", "They're convenient by the bed, the kitchen counter and the desk. Choose models with USB-C and good charging power."),
],
"related": ["pot-lights", "renovation-wiring", "electrical-repair"],
"cities": {
"windsor": "Windsor's century homes often have one outlet per wall, many of them two-prong, in rooms that now hold a TV, a computer and a dozen chargers. Fishing new grounded runs through plaster and brick is slower work, so we plan routes from the basement or attic to keep openings to a minimum.",
"lasalle": "LaSalle homeowners mostly call for additions rather than fixes: outlets for an island, a dedicated circuit for a basement bar fridge or a gym, outdoor outlets on the deck and pool equipment. Garage outlets for tools and freezers are another common request here.",
"tecumseh": "In Tecumseh we see both: two-prong and aluminum-wired outlets in older homes that need proper fixes, and requests for new garage, shop and outdoor circuits on larger lots. On aluminum circuits, every device we install is connected with approved connectors."
}
},
{
"slug": "renovation-wiring",
"name": "Renovation & Basement Wiring",
"cat": "wiring",
"icon": "reno",
"short": "Electrical for kitchen, bathroom and basement renovations and additions, from layout to rough-in and final inspection.",
"title": "Renovation & Basement Electrical | Kitchens, Baths, Additions",
"desc": "Electrical for renovations: kitchen, bathroom and basement wiring, additions and garages, from layout and rough-in to the final ESA inspection.",
"h1": "Renovation & Basement Wiring",
"lead": "Get the electrical right while the walls are open. Kitchens, bathrooms, basements and additions, planned with you, roughed in on schedule and inspected.",
"body": """
<p>A renovation is the least expensive time to fix and add electrical work, because the walls are already open. It's also when mistakes get buried behind new drywall. {biz} works with homeowners and contractors on kitchen, bathroom and basement renovations, additions and garages, and plans the electrical before the framing is finished.</p>
<h2>What's included</h2>
<ul>
<li><strong>Electrical layout</strong> — outlets, lighting, switches and appliance circuits planned around your design and the code.</li>
<li><strong>Load check</strong> — confirming the panel can handle the new circuits, with options if it can't.</li>
<li><strong>Rough-in</strong> — boxes, cable and circuits installed while the walls are open, on your contractor's schedule.</li>
<li><strong>Rough-in inspection</strong> — inspected before insulation and drywall, so nothing is covered up unseen.</li>
<li><strong>Finishing</strong> — devices, fixtures, pot lights and appliance connections once the walls are painted.</li>
<li><strong>Final inspection</strong> — the {esa} permit closed out, with paperwork for your records.</li>
</ul>
<h2>Kitchens, bathrooms and basements</h2>
<p>Kitchens need dedicated circuits for the fridge, microwave and dishwasher, counter outlets with GFCI protection, and often a new range circuit for induction. Bathrooms need GFCI protection and an exhaust fan that actually vents outside. Basements need lighting, smoke alarms, outlets every few feet and often a bedroom with arc-fault protection. We'll walk you through what applies to your project.</p>
<h2>Working with your contractor</h2>
<p>We coordinate with your general contractor, plumber and HVAC trade so the electrical arrives on time and inspections don't hold up drywall. Most renovations include [[pot-lights|pot lights]] and new [[outlets-switches|outlets and circuits]], and bigger ones often need a [[panel-upgrades|panel upgrade]].</p>
""",
"faqs": [
("Do I need a permit for basement wiring?", "Yes. New electrical work in Ontario needs a permit, and the rough-in is inspected before the walls are closed."),
("When should the electrician start on a renovation?", "Before the framing is finished. That's when the layout is easiest to change and the rough-in fits the contractor's schedule."),
("Can you work with my general contractor?", "Yes. We regularly work as the electrical trade on renovation projects and keep to the project schedule."),
("Will my panel handle the renovation?", "We check before rough-in. If it can't, the options include rearranging circuits, a subpanel or a panel upgrade."),
],
"related": ["pot-lights", "outlets-switches", "panel-upgrades"],
"cities": {
"windsor": "Windsor renovations often mean updating a century home's kitchen or finishing a basement that took on water years ago. Opening those walls usually uncovers older wiring that needs replacing too, so we leave room in the plan and the quote for what we might find.",
"lasalle": "LaSalle's larger homes see a lot of basement finishing: rec rooms, bars, home gyms, theatres and guest suites with bathrooms. Those basements add up to a lot of circuits, so we check the panel's capacity early in the design rather than at rough-in.",
"tecumseh": "Tecumseh renovations range from updating 1970s kitchens and bathrooms to building additions and detached garages on larger lots. Garages and shops often need a subpanel fed from the house, which we size for the tools and heaters you plan to run."
}
},
{
"slug": "hot-tub-wiring",
"name": "Hot Tub & Pool Wiring",
"cat": "wiring",
"icon": "hottub",
"short": "Dedicated circuits, GFCI disconnects and bonding for hot tubs, swim spas, pool pumps and heaters, done to code.",
"title": "Hot Tub & Pool Wiring | GFCI Disconnects & Bonding",
"desc": "Hot tub, swim spa and pool electrical: dedicated 240 V circuits, GFCI-protected disconnects, bonding and pool equipment wiring, permitted and inspected.",
"h1": "Hot Tub & Pool Wiring",
"lead": "Water and electricity need to be wired with care. Dedicated circuits, GFCI protection and proper bonding for hot tubs, swim spas and pool equipment.",
"body": """
<p>A hot tub needs its own 240 V circuit, a disconnect within sight of the tub and ground-fault protection, and the metal around it needs to be bonded. Pools add pumps, heaters, lights and bonding of everything metal near the water. These are among the most carefully inspected installations in a home, for good reason. {biz} wires them properly the first time.</p>
<h2>What's included</h2>
<ul>
<li><strong>Load check</strong> — confirming your panel can handle the tub or pool equipment, which can be a large load.</li>
<li><strong>Dedicated circuit</strong> — sized for your tub's rating, from a breaker in the panel to the tub.</li>
<li><strong>GFCI-protected disconnect</strong> — a weatherproof disconnect at the required distance from the water, so the tub can be shut off safely.</li>
<li><strong>Proper wire route</strong> — along the house or buried in conduit at the right depth, with locates before we dig.</li>
<li><strong>Bonding</strong> — metal parts, pool equipment and nearby metal bonded together, as the code requires.</li>
<li><strong>Permit and inspection</strong> — the {esa} permit is filed and the work is inspected before the tub is filled.</li>
</ul>
<h2>Before the tub arrives</h2>
<p>Book the electrical when you order the tub. Send us its spec sheet (the amperage is what matters) and tell us where it will sit. Plug-in "plug and play" tubs run on a regular outlet but heat slowly. Most full-size tubs and swim spas need a 40 to 60 amp circuit. If the panel is full, a [[panel-upgrades|panel upgrade]] may come first.</p>
<p>Adding lights and outlets on the deck while we're there? See [[outlets-switches|outlets and switches]] and [[pot-lights|lighting]]. For a ballpark price, use the [[estimate|instant electrical estimate]].</p>
""",
"faqs": [
("Do I need an electrician for a hot tub?", "Full-size hot tubs need a dedicated 240 V circuit, a GFCI-protected disconnect and an inspection. In Ontario that's work for a licensed electrical contractor with a permit."),
("How far does the disconnect have to be from the tub?", "Close enough to see the tub, but not closer than the code allows. We place it to meet the code and still be handy."),
("Can the wire be buried?", "Yes, in conduit at the depth the code requires. Utility locates are requested before any digging."),
("What does bonding mean?", "Connecting nearby metal parts together so they stay at the same voltage. It reduces the risk of shock around water."),
],
"related": ["outlets-switches", "panel-upgrades", "pot-lights"],
"cities": {
"windsor": "Many Windsor backyards are narrow and long, with the hot tub at the back by a detached garage, so the wire run is often long. We measure the route along the house and garage before we quote, and bury the run in conduit where it has to cross the yard.",
"lasalle": "LaSalle has one of the area's highest counts of backyard pools and hot tubs, often on the same panel along with an EV charger. Pool equipment, heaters, lighting and bonding are common jobs here, and we make sure the panel can carry it all.",
"tecumseh": "On Tecumseh's larger lots, hot tubs and swim spas are sometimes set well away from the house, by a pool house or a shop. Long runs need heavier wire, and a subpanel near the tub is sometimes the neater option."
}
},
# ------------------------------------------------------------------ REPAIR, SAFETY & COMMERCIAL
{
"slug": "electrical-repair",
"name": "Electrical Repair",
"cat": "repair",
"icon": "repair",
"short": "Troubleshooting and repairs for tripping breakers, dead outlets, flickering lights, buzzing panels and other electrical problems.",
"title": "Electrical Repair & Troubleshooting | Residential",
"desc": "Electrical repair and troubleshooting: tripping breakers, dead outlets, flickering lights, warm outlets and buzzing panels, found and fixed properly.",
"h1": "Electrical Repair",
"lead": "Breakers that trip, outlets that died, lights that flicker. We find the cause, not just the symptom, and fix it so it stays fixed.",
"body": """
<p>Electrical problems rarely fix themselves, and the cause is often somewhere other than where the symptom shows up. A dead outlet can be a tripped GFCI two rooms away. Flickering lights can be a loose connection in a box, or a problem at the service. {biz} troubleshoots methodically, explains what we found and fixes the cause.</p>
<h2>What we fix</h2>
<ul>
<li><strong>Tripping breakers</strong> — overloaded circuits, damaged cable, failing appliances or worn-out breakers.</li>
<li><strong>Dead outlets and lights</strong> — tripped GFCIs, loose connections, failed devices and broken circuits.</li>
<li><strong>Flickering and dimming</strong> — loose connections, overloaded circuits or problems at the service and meter.</li>
<li><strong>Warm or scorched outlets</strong> — loose or failing connections that can overheat, made safe the same visit.</li>
<li><strong>Buzzing and humming</strong> — from panels, switches and fixtures, traced and fixed.</li>
<li><strong>Damage after storms or floods</strong> — wiring, outlets and equipment that got wet, checked before power is restored.</li>
</ul>
<h2>How a repair call runs</h2>
<ol>
<li><strong>Tell us the symptoms.</strong> When it happens, what's affected and anything that changed recently.</li>
<li><strong>Diagnosis.</strong> We test, trace and find the cause, then tell you what it is and what the fix costs before we do it.</li>
<li><strong>Repair.</strong> Fixed properly, with a permit filed where the work requires one.</li>
</ol>
<h2>When it's urgent</h2>
<p>A burning smell, sparks, a scorched outlet, a hot panel or a breaker that won't stay on are not wait-and-see problems. Turn off the affected circuit if you safely can and call us at {phone}, or see [[emergency-electrician|emergency electrician]] service. Repeated problems across the house often point to deeper issues, and an [[electrical-inspections|electrical inspection]] or [[home-rewiring|rewiring]] can solve them for good.</p>
""",
"faqs": [
("Why does my breaker keep tripping?", "Usually too much on one circuit, a faulty appliance, or damaged wiring. A breaker that trips immediately when reset often means a short, which needs a professional."),
("Is a warm outlet dangerous?", "Yes. An outlet or switch plate that's warm to the touch usually means a loose or failing connection. Stop using it and have it checked."),
("Why do my lights flicker?", "One flickering light is often the bulb or a loose connection. Lights flickering across the house can point to a problem at the panel or service, which needs checking soon."),
("Can I reset a breaker myself?", "Once, yes. If it trips again, leave it off and call an electrician. Repeatedly resetting a tripping breaker can be dangerous."),
],
"related": ["emergency-electrician", "electrical-inspections", "outlets-switches"],
"cities": {
"windsor": "In Windsor's older homes, many repair calls come down to decades of add-ons: circuits extended by previous owners, loose connections in old boxes and devices worn out from years of use. Old wiring is unforgiving of loose connections, so we check the whole circuit, not just the outlet that failed.",
"lasalle": "In LaSalle, repair calls often involve newer equipment: GFCI and arc-fault breakers that trip with certain appliances, outdoor outlets that let water in, and circuits overloaded by basement finishes. We find what's tripping and why, and fix the circuit properly.",
"tecumseh": "Tecumseh repair calls often lead to aluminum wiring connections in 1960s and 1970s homes, or to outbuildings fed by long, old runs from the house. Both need careful testing, and every aluminum connection we touch is made with approved connectors."
}
},
{
"slug": "emergency-electrician",
"name": "Emergency Electrician",
"cat": "repair",
"icon": "bolt",
"short": "Urgent electrical help for sparks, burning smells, power loss, storm damage and flooded electrical, made safe fast.",
"title": "Emergency Electrician | Sparks, Burning Smells, No Power",
"desc": "Emergency electrician for sparks, burning smells, partial power loss, storm damage and flooded electrical. Call for urgent help making it safe.",
"h1": "Emergency Electrician",
"lead": "Sparks, a burning smell, half the house dark or water near the panel. Call us. We'll tell you what to do right now and get someone there to make it safe.",
"body": """
<p>Some electrical problems can't wait until Monday. When something is sparking, smells like it's burning or has lost power for no clear reason, the first job is making it safe, and the second is finding out why. {biz} answers emergency calls and gets a licensed electrician to you to isolate the problem, make the system safe and restore power when it's safe to do so.</p>
<h2>Call right away for</h2>
<ul>
<li><strong>Burning smell or smoke</strong> — from an outlet, switch, fixture or the panel. If there is smoke or fire, call 911 first.</li>
<li><strong>Sparks or arcing</strong> — at outlets, switches, the panel or the meter.</li>
<li><strong>Partial power loss</strong> — half the house dark, lights unusually bright or dim, often a service problem.</li>
<li><strong>Water and electricity</strong> — flooding near the panel, outlets or equipment, or water coming through light fixtures.</li>
<li><strong>Storm damage</strong> — a pulled-down service mast, damaged meter base or tree on the service wires.</li>
<li><strong>Hot panel or breaker</strong> — a panel or breaker that's hot, buzzing loudly or won't reset.</li>
</ul>
<h2>What to do while you wait</h2>
<ol>
<li><strong>Stay safe.</strong> Never touch anything electrical while standing in water. Stay away from downed wires and call the utility.</li>
<li><strong>Shut it off if you can.</strong> Turn off the affected breaker, or the main, only if you can reach the panel safely and dry.</li>
<li><strong>Call us at {phone}.</strong> Describe what you see and hear, and we'll talk you through the next step.</li>
</ol>
<h2>After the emergency</h2>
<p>Once it's safe, we explain the cause and the permanent fix. A pulled-down service may need [[panel-upgrades|service work]], flooded circuits may need [[electrical-repair|repairs]] and some homes benefit from a [[generator-installation|generator hookup]] for the next storm.</p>
<!-- CLIENT REVIEW: confirm the client takes after-hours calls and how quickly they can usually respond. Don't promise response times. -->
""",
"faqs": [
("What counts as an electrical emergency?", "Smoke, a burning smell, sparks, partial power loss, water near electrical equipment and storm damage to the service. When in doubt, call and ask."),
("Should I call the utility or an electrician?", "Call the utility for downed lines and power out on the whole street. Call an electrician when the problem is in or on your home, including the meter base and mast."),
("What if water reached my panel?", "Stay out of the water and don't touch the panel. The utility can disconnect the power, and an electrician must check the equipment before it's turned back on."),
("Can you restore power the same day?", "Often, once it's safe. Some problems, like a damaged service, also need the utility to reconnect, which we coordinate."),
],
"related": ["electrical-repair", "generator-installation", "panel-upgrades"],
"cities": {
"windsor": "Windsor's summer storms and older services make for a steady run of emergencies: service masts pulled off by branches, overloaded connections that finally give out, and basements taking on water near the panel. For a damaged service, we make it safe and coordinate the reconnect with ENWIN Utilities.",
"lasalle": "LaSalle's emergencies are often storm-related: trees on service wires, lightning damage, and flooded basements where finished walls hide wet wiring. Water damage behind drywall needs careful checking before circuits go back on, and we test them one at a time.",
"tecumseh": "Tecumseh's 2017 flooding showed how quickly water can reach basement panels and equipment. Emergency calls here also come from rural properties after storms, where long overhead runs to barns and shops take damage, and we make those safe as well."
}
},
{
"slug": "electrical-inspections",
"name": "Electrical Inspections",
"cat": "repair",
"icon": "inspect",
"short": "Electrical safety inspections for older homes, home buyers, insurance requests and before renovations, with a written report.",
"title": "Home Electrical Inspections | Buyers & Insurance",
"desc": "Home electrical safety inspections for buyers, insurers and older homes: panel, wiring, grounding, GFCI and outlets checked, with a written report.",
"h1": "Electrical Inspections",
"lead": "Know what's behind the walls. A licensed electrician's inspection of your panel, wiring and devices, with a plain-language report of what's fine, what to watch and what to fix.",
"body": """
<p>A general home inspection looks at the electrical system from the outside. An electrician's inspection goes further: opening the panel, testing circuits and checking the connections that cause most electrical fires. {biz} inspects homes for buyers, owners of older houses, insurance requests and anyone planning a renovation, and puts the findings in writing.</p>
<h2>What we check</h2>
<ul>
<li><strong>Service and panel</strong> — size, condition, breakers, double taps, signs of overheating and labelling.</li>
<li><strong>Wiring type</strong> — knob and tube, aluminum branch wiring, ungrounded circuits and wiring added without a permit.</li>
<li><strong>Grounding and bonding</strong> — the grounding electrode, water and gas bonding, and grounded outlets.</li>
<li><strong>Protection</strong> — GFCI in wet locations, arc-fault protection, and smoke and carbon monoxide alarm locations.</li>
<li><strong>Devices and fixtures</strong> — a sample of outlets, switches and fixtures tested for polarity, ground and wear.</li>
<li><strong>Written report</strong> — findings ranked by priority, with photos and repair costs on request.</li>
</ul>
<h2>When to book one</h2>
<p>Before you buy an older home, when your insurer asks about your wiring, before a major renovation, when you've moved into a house with unknown work done by a previous owner, or when something just doesn't feel right. If we find problems, you can have us fix them or take the report to anyone you like. Common follow-ups are [[knob-and-tube-replacement|knob and tube replacement]], [[home-rewiring|rewiring]] and [[panel-upgrades|panel upgrades]].</p>
<h2>Inspection or {esa} inspection?</h2>
<p>Our inspection is a safety assessment of the house as it is. The {esa} inspection is the official check of new work done under a permit. Both matter, and new work we do always gets the official one.</p>
""",
"faqs": [
("How long does an electrical inspection take?", "Most houses take one to two hours, depending on size and how much is accessible."),
("Will you fix what you find?", "If you'd like us to. The report lists each item, and you can choose who does the work."),
("Will the report satisfy my insurance company?", "It usually answers their questions about wiring type, panel and condition. Some insurers also want proof of specific repairs, which the inspection paperwork from that work provides."),
("Is this the same as a home inspection?", "No. A home inspector looks at the whole house. An electrician opens the panel and tests circuits, which goes deeper on electrical."),
],
"related": ["knob-and-tube-replacement", "home-rewiring", "electrical-repair"],
"cities": {
"windsor": "Windsor's housing stock spans more than a century, so we find a bit of everything: knob and tube, ungrounded outlets, fuse panels and generations of DIY wiring. Buyers of older Windsor homes often book an inspection during their conditional period, before they firm up the deal.",
"lasalle": "LaSalle inspections usually focus on what previous owners added: finished basements, hot tubs, pool equipment and garage circuits, sometimes done without a permit. Unpermitted work can be a problem when you sell, so it's worth knowing about early.",
"tecumseh": "In Tecumseh, inspections often focus on aluminum branch wiring in homes built in the mid-1960s to late 1970s, and on outbuilding feeds on larger lots. Insurers frequently ask about aluminum wiring, and our report documents what's there and its condition."
}
},
{
"slug": "commercial-electrical",
"name": "Commercial Electrical",
"cat": "repair",
"icon": "commercial",
"short": "Electrical for shops, offices, restaurants and light industrial spaces: fit-outs, LED retrofits, equipment circuits and service work.",
"title": "Commercial Electrician | Fit-Outs, LED & Equipment",
"desc": "Commercial electrical for shops, offices, restaurants and industrial units: tenant fit-outs, LED lighting retrofits, equipment circuits and service work.",
"h1": "Commercial Electrical",
"lead": "Electrical for businesses that can't afford to be dark. Fit-outs, lighting, equipment and repairs, scheduled around your hours.",
"body": """
<p>Commercial electrical work has tighter schedules, larger loads and more people depending on it. {biz} works with business owners, property managers and contractors on retail, office, restaurant and light industrial spaces, and schedules disruptive work outside business hours where we can.</p>
<h2>What we do</h2>
<ul>
<li><strong>Tenant fit-outs</strong> — new layouts for offices, shops and restaurants, from panel to lighting, coordinated with the other trades.</li>
<li><strong>LED lighting retrofits</strong> — interior, warehouse and parking lot lighting upgraded to LED to cut energy use and maintenance.</li>
<li><strong>Equipment circuits</strong> — dedicated and three-phase circuits for kitchen equipment, compressors, machinery and EV chargers.</li>
<li><strong>Service and panel work</strong> — new services, subpanels and capacity upgrades for growing businesses.</li>
<li><strong>Emergency and exit lighting</strong> — installation, repairs and testing support.</li>
<li><strong>Maintenance and repairs</strong> — troubleshooting and service calls so the business stays open.</li>
</ul>
<h2>How we work with businesses</h2>
<ol>
<li><strong>Walk-through.</strong> We see the space, the panel and the equipment, and understand your hours and deadlines.</li>
<li><strong>Written quote.</strong> Scope, schedule, exclusions and any after-hours work, in writing.</li>
<li><strong>Scheduled work.</strong> Shutdowns planned in advance and kept as short as possible.</li>
<li><strong>Permits and close-out.</strong> The {esa} permit, inspection and documentation for your landlord or insurer.</li>
</ol>
<h2>One electrician for the whole property</h2>
<p>From a single storefront to a multi-unit building, we handle repairs, upgrades and new work. Business owners often call us for their homes too, from [[panel-upgrades|panel upgrades]] to [[ev-charger-installation|EV chargers]]. For a quote, [[contact|tell us about the project]].</p>
<!-- CLIENT REVIEW: confirm the client does commercial work, three-phase and after-hours scheduling before launch. -->
""",
"faqs": [
("Do you work after hours?", "Where the work would disrupt your business, we schedule shutdowns and noisy work outside your opening hours when possible."),
("Can you work with our general contractor?", "Yes. On fit-outs we work as the electrical trade and coordinate with the general contractor and the other trades."),
("Do LED retrofits pay for themselves?", "Often, through lower energy and maintenance costs, especially for lights that run long hours. The payback depends on your hours and your current fixtures."),
("Do you install commercial EV chargers?", "Yes, for staff, fleet and customer parking, including load planning for multiple chargers."),
],
"related": ["panel-upgrades", "ev-charger-installation", "electrical-repair"],
"cities": {
"windsor": "Windsor's commercial work spans downtown storefronts, Walkerville and Ottawa Street restaurants, and industrial units supporting the auto sector. Older commercial buildings here often need panel and lighting upgrades before a new tenant can move in, which we plan into the fit-out schedule.",
"lasalle": "LaSalle's commercial strips along Malden Road and Front Road hold restaurants, clinics, offices and shops. Fit-outs, signage circuits, LED upgrades and EV chargers for customer parking are common requests here.",
"tecumseh": "Tecumseh's Oldcastle area is home to much of the region's light industrial and manufacturing space, with machinery, compressors and three-phase power. We also work on retail and offices along Tecumseh Road, scheduling shutdowns around production and business hours."
}
},
]

# ------------------------------------------------------------------ extra sections (appended to each body)
EXTRA = {
"panel-upgrades": "",
"ev-charger-installation": "",
"generator-installation": """<h2>Before the next outage</h2>
<p>Install the hookup before you need it. In a storm, nobody can get a permit, an inspection or parts quickly, and that's exactly when the sump pump has to run.</p>""",
"surge-protection": """<h2>What a surge looks like</h2>
<p>Most surges are small and frequent: a motor starting, a compressor cycling, the power returning after a flicker. They don't trip a breaker, but over time they wear out the electronics in furnaces, fridges and chargers. A whole-home protector absorbs them at the panel before they reach those circuit boards, and it's especially worth it once you own an EV charger or a heat pump.</p>""",
"home-rewiring": """<h2>Living in the house during a rewire</h2>
<p>We plan the work so the kitchen and bathroom stay usable, keep dust contained with drop sheets and barriers, and tell you each morning which rooms will be without power that day.</p>""",
"knob-and-tube-replacement": """<h2>Why it matters now</h2>
<p>Knob and tube relied on air around the wires to stay cool. Decades later, attics have been insulated over it and its insulation has cracked, which is why insurers and inspectors take it seriously.</p>""",
"pot-lights": """<h2>Ceilings we work with</h2>
<p>Drywall, plaster and lath, textured ceilings and basement joists all take a different approach. We cut plaster with the right tools so it doesn't crack, fish wires through finished ceilings between joists, and keep the access holes we make small. In basements with open joists, the wiring goes in before the ceiling does, so there's nothing to patch at all.</p>""",
"outlets-switches": """<h2>Smart switches and dimmers</h2>
<p>Many smart switches need a neutral wire in the switch box, which older homes often don't have. We check before you buy, and run a neutral or recommend a switch that works without one. For LED lights, choose dimmers made for LEDs so the lights dim smoothly without flicker. Three-way and four-way switching lets you control stairs and long hallways from either end. Timers and motion sensors are handy for porches, closets and garages.</p>""",
"renovation-wiring": """<h2>Additions, garages and workshops</h2>
<p>Additions and detached garages often need their own subpanel, sized for heaters, tools, an EV charger or a workshop. We plan the feed from the main panel, the route (overhead, along the house or buried) and the circuits inside, so the new space has enough power from day one instead of extension cords. Buried feeds get utility locates before any digging. Lighting and outlets are laid out around how you'll use the space.</p>""",
"hot-tub-wiring": """<h2>Swim spas and pool equipment</h2>
<p>Swim spas often draw 50 or 60 amps, sometimes on two circuits. Pools add a pump, filter, heater and lights, each on its own circuit with timers or controls. We wire the equipment pad, bond the pool and equipment, and add GFCI protection everywhere the code calls for it.</p>""",
"electrical-repair": """<h2>Repair or replace?</h2>
<p>If the cause is one worn device or a loose connection, we fix it. If repairs keep coming back to the same panel or the same old wiring, we'll show you what a lasting fix costs, and let you decide. Either way, you'll know the cause before you pay for the fix, and nothing is replaced that doesn't need to be.</p>""",
"emergency-electrician": """<h2>Insurance claims</h2>
<p>After storm or water damage, we can document what we found and what was repaired, which helps with insurance claims. We can also quote the permanent repairs in writing for your adjuster, and work with the restoration company drying out the house.</p>""",
"electrical-inspections": """<h2>What the report looks like</h2>
<p>Each finding is listed in plain language, ranked as urgent, recommended or worth watching, with photos where they help. You can hand it to your insurer, your real estate agent or any electrician you choose. Most buyers use it to negotiate repairs or a price adjustment before their conditional period ends. Owners use it to plan work in order, starting with what matters most for safety.</p>""",
"commercial-electrical": """<h2>Restaurants, retail and industrial</h2>
<p>Restaurants need dedicated circuits for cooking equipment, coolers and hood fans, and often a panel upgrade when the menu changes. Retail spaces need display and track lighting, signage circuits and plenty of outlets. Industrial units need three-phase power for machinery, welders and compressors, with lockout points and clear labelling. Offices need circuits for workstations, server closets and break rooms. Whatever the space, we plan the load before the work starts so the business isn't tripping breakers on opening day.</p>
<h2>Energy savings</h2>
<p>LED retrofits, occupancy sensors and lighting controls cut energy and maintenance costs, especially in spaces lit for long hours. We can quote a retrofit fixture by fixture so you can see the change before you commit.</p>""",
}
for _s in SERVICES:
    _s["body"] += EXTRA.get(_s["slug"], "")
