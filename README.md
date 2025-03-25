# rocket-flutter-speed-analysis 🚀

## Project Goal:
Given a supersonic rocket with chosen fin dimensions, solve the divergence and flutter speed

## UVic Rocketry Anduril-2 Information:
1) Dimensions:

   Fuselage outer diameter: 5.75 in
   Total rocket length: 97.64 in
   Span: 5 in
   Root chord: 13 in
   Tip chord: 3.5 in
   Sweep distance: 8.5 in
   Fin thickness: 0.255 in
   Fin count: 4
   

L/D ratio: 12?

Fin shape:
Trapezoidal profile w/ hexagonal airfoil


Fin attachment to fuselage/boat tail:
Loctite EA E-120-HP Epoxy

2) Flight Profile:

Velocity



## Workflow Notes

1) Start with flight path and fin geometry from flight sim / analysis
2) Build Structural/aero model
3) Run a SOL 103 


## Structural Model🗼

### Fuselage and Nosecone 
???
modeled as rigid - aluminum tube

### Fin 
is being loaded in:
- Out of plane bending
- Torision
- Shear

Assuming small deformations (linear) to start

Element: 
(likely) Combination of linear CQUAD4 and CTRIG3



## Mass Model ⚖️
Non structural mass:
- Propulsion/Solid Motor
- Recovery
- Avionics
- Sat Club Payload

(likely) a single CONM2 element - mass changes through flight with motor burn
### CONM2 Inputs: 
- Mass
- cg (x,y,z)
- I (xx, yy, zz, xy, xz, yz)

Connect to fins with RB1? RB2? --> question of dof
- rb2 - rigid load transfer to fuselage
- rb1 - flexible load transfer to fuselage --> this would be used if we were modelling fin feet or attachment to high detail (might be worth???)


## Aerodynamic Model ✈️

AEROS --> static
AERO --> dynamic
and a rectangular csys where flow defined along + x dir and // to aero elements

See [4]

- Want to account for supersonic shock waves
- low aoa (5 degree from vertical worst case)

For supersonic flow, msc nastran has Mach Box and ZONA51 implemented.



### Selecting ZONA51 --> See [4]
- Panel Method:
    - inviscid flow (no viscosity effects), does not model boundary layer (poor drag force accuracy)
    - more precise shock wave handling
    - better for complex geometries - better for slender bodies
    - Better for transonic - high supersonic (Ma 1.0 - 5.0)
- Correction for fin thickness in ZONA51  is important for Ma > 1.2 [4]
- One plane symmetry supported (y=0) [1]

Bulk Data --> CAERO1 --> see [1] pdf page 120 for setup guide, some attention to detail required here
Entries --> PAERO1 --> this defines which panels interfere with each other




## Splines ➰

ZONA51 interconnection to structure via box centres [1]

Surface splines - solutions for uniform plates [1] - several different options and implementations
Rigid Body splines - transfer based only on geometry



## Other Assumptions and Notes 📝
- want to recreate experimental data to validate our understanding/methods
- likely want to do a mesh convergence study on model
- temperature effects?

## Solver 📝

### Static aeroelasticity - divergence
- static aeroelastic response DMAP sequence SOL 144
- (both structural and aerodynamic data) provides loads, deflections and stresses

### Dynamic aeroelastic stability - flutter:
3 methods:
- K method
- KE method
- PK method --> i think this is most common?


## Postprocessing Tools 🛠️🐍

maybe noteworthy: https://github.com/vsdsantos/nastran-aeroelasticity/tree/main
TODO: pynastran graph of flutter speeds per flutter modes

have heard people usually make these libs themselves - not much experience we just need the flutter plots

## Validation ✅

See [4]

Potentially See [3] - seems to use piston theory, ZONA51 is more complicated
This case does not include body shockwaves

[1] also has examples
TODO: try first tutorial to build an understanding of how all the pieces fit together



## Sources and Citations:
| Number | Source                            | Contribution / Use Description                 | Link to Source    |
|--------|-----------------------------------|------------------------------------------------|-------------------|
| [1]    | MSC Nastran Aeroelastic Analysis User Guide | Explains solver                      | https://help-be.hexagonmi.com/bundle/MSC_Nastran_2023.1_Aeroelastic_Analysis_User_Guide/raw/resource/enus/MSC_Nastran_2023.1_Aeroelastic_Analysis_User_Guide.pdf |
| [2]    | AEROELASTIC INVESTIGATION OF A MISSILE CONFIGURATION | Example of MSC Nastran for flutter analysis of a similar vehicle                   | https://www.foi.se/rest-api/report/FOI-R--0474--SE |
| [3]    | EXPERIMENTAL AND CALCULATED RESULTS OF SUPERSONIC FLUTTER CHARACTERISTICS OF A LOW ASPECT-RATIO FLAT-PLATE SURFACES | Looks Promising for a validation case, no body just fin | https://arc.aiaa.org/doi/10.2514/6.1967-1340 |
| [4]    | A Sensitivity Investigation on the Aeroelastic Dynamic Stability of Slender Spinning Sounding Rockets | shows nastran model setup and validation, basically what we want to do | doi: 10.5028/jatm.v5i1.192 |
| [5]    | MSC Nastran online card desc | Understanding model setup | https://nexus.hexagon.com/documentationcenter/en-US/bundle/MSC_Nastran_2021/page/Nastran_Combined_Book/qrg/bulk_data/TOC.Bulk.Data.Entry.xhtml |
| [6]    | Ata engineering flutter tutorial | useful overview | https://www.youtube.com/watch?v=GjBXsR6SSLY&t=165s |
| [7]    | Introduction to aircraft aeroelasticity and loads | good resource for learning flutter | book |
| [8]    | Pynastran github | library likely useful for pre/postprocessing but also has an example model library | https://github.com/SteveDoyle2/pyNastran/tree/main/models |


<!-- This is a comment in a Markdown file (not rendered) --> 
