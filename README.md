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

Initially tried to use NASTRAN:
- MSC NASTRAN did not have flutter accessible in the student version
- Altair Hypermesh (NASTRAN) did not have supersonic aero

Therefore we need to work at a lower level: New approach to use existing aero and structural models and create our own solver.

_old
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




## Mass Model ⚖️

Gmsh???

## Aerodynamic Model ✈️

Using USU Aerolab MachLine: https://github.com/usuaero/MachLine


## Splines ➰



## Other Assumptions and Notes 📝
- want to recreate experimental data to validate our understanding/methods
- likely want to do a mesh convergence study on model
- temperature effects?

## Solver 📝


https://fenicsproject.org/ 


## Postprocessing Tools 🛠️🐍



## Validation ✅

See [4]

Potentially See [3] - seems to use piston theory, ZONA51 is more complicated
This case does not include body shockwaves

[1] also has examples
TODO: try first tutorial to build an understanding of how all the pieces fit together



## Sources and Citations:

_old
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
