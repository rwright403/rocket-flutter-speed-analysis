# rocket-flutter-speed-analysis 🚀

## Project Goal:
Given a supersonic rocket with chosen fin dimensions, solve the flutter speed

## UVic Rocketry Anduril-2 Information:
1) Dimensions:

L/D: 12?

Fin shape:

2) Flight Profile:

Velocity



## Structural Model

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

Connect to fins with RB3? RB2? 

## Aerodynamic Model ✈️
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






## Splines ➰
Surface splines - solutions for uniform plates [1] - several different options and implementations
Rigid Body splines - transfer based only on geometry


## Other Assumptions and Notes

## Solver

### Static aeroelasticity - divergence
- static aeroelastic response DMAP sequence SOL 144
- (both structural and aerodynamic data) provides loads, deflections and stresses

### Dynamic aeroelastic stability - flutter:
3 methods:
- K method
- KE method
- PK method

vibration modal analysis used to reduce number of dof

## Postprocessing Tools

TODO: pynastran graph of flutter speeds per flutter modes
maybe noteworthy: https://github.com/vsdsantos/nastran-aeroelasticity/tree/main


## Validation

See [3] - seems to use piston theory, ZONA51 is more complicated
This case does not include body shockwaves


## Sources and Citations:
| Number | Source                            | Contribution / Use Description                 | Link to Source    |
|--------|-----------------------------------|------------------------------------------------|-------------------|
| [1]    | MSC Nastran Aeroelastic Analysis User Guide | Explains solver                      | https://help-be.hexagonmi.com/bundle/MSC_Nastran_2023.1_Aeroelastic_Analysis_User_Guide/raw/resource/enus/MSC_Nastran_2023.1_Aeroelastic_Analysis_User_Guide.pdf |
| [2]    | AEROELASTIC INVESTIGATION OF A MISSILE CONFIGURATION | Example of MSC Nastran for flutter analysis of a similar vehicle                   | https://www.foi.se/rest-api/report/FOI-R--0474--SE |
| [3]    | EXPERIMENTAL AND CALCULATED RESULTS OF SUPERSONIC FLUTTER CHARACTERISTICS OF A LOW ASPECT-RATIO FLAT-PLATE SURFACES | Looks Promising for a validation case, no body just fin | https://arc.aiaa.org/doi/10.2514/6.1967-1340 |
| [4]    | 


<!-- This is a comment in a Markdown file (not rendered) --> 
