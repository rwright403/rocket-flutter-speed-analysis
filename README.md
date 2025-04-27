# rocket-flutter-speed-analysis 🚀
A losely coupled flutter speed calculator built using open-source and software available to students (from a student license).

## Required Program Inputs:
### CFD - from Openfoam:
The following files:
- p
- rho
- Ma - or a ??? #TODO:
- U

### Structual Model - from ALTAIR HYPERMESH NASTRAN:
- natural frequencies
- mode shapes


## Running this program:



> python3 -m 



# documentation

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

Therefore we need to work at a lower level: 
New approach "weakly coupled solver" - using [5] as a guide.
This method requires Harmonics and a CFD Simulation

   ## Harmonics Simulation
   - Altair Student edition is easy for me to obtain as a student. It is the least restrictive and NASTRAN files are easy to parse.

   ## CFD Simulation
   - OpenFOAM, see [8],[9],[10]

   ### My toolkit docker setup:
   |-home
      |-rocket-cfd
         |-openfoam-data
         |-openfoam-dockerfiles

   Running the docker container:
   > sudo docker container run -ti --rm -v $HOME/rocket-cfd-toolkit/openfoam-data:/data -w /data openfoam:latest


   ## Flutter Sol:
   This repository
   -Copy results files from Harmonics and CFD Simulations into the correct dir <!-- TODO: DEFINE -->


Using a virtual environment to stop this from interfering w other python projects:
Enter virtual env with 
> source venv/bin/activate
Exit with - deactivate







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


## Interpolation ➰
https://docs.pyvista.org/examples/01-filter/interpolate


## Other Assumptions and Notes 📝
- want to recreate experimental data to validate our understanding/methods
- likely want to do a mesh convergence study on model
- temperature effects?

## Solver 📝


https://fenicsproject.org/ 


## Postprocessing Tools 🛠️🐍



## Validation ✅

See [4]

Potentially See [3] - seems to use piston theory

[1] also has examples
TODO: try first tutorial to build an understanding of how all the pieces fit together



## Sources and Citations:


| Number | Source                            | Contribution / Use Description                 | Link to Source    |
|--------|-----------------------------------|------------------------------------------------|-------------------|
| [1]    | Wright and Cooper Aeroelasticity Textbook | Starting point for learning theory     |                   |
| [2]    | AEROELASTIC INVESTIGATION OF A MISSILE CONFIGURATION | Example of MSC Nastran for flutter analysis of a similar vehicle                   | https://www.foi.se/rest-api/report/FOI-R--0474--SE |
| [3]    | EXPERIMENTAL AND CALCULATED RESULTS OF SUPERSONIC FLUTTER CHARACTERISTICS OF A LOW ASPECT-RATIO FLAT-PLATE SURFACES | Looks Promising for a validation case, no body just fin | https://arc.aiaa.org/doi/10.2514/6.1967-1340 |
| [4]    | A Sensitivity Investigation on the Aeroelastic Dynamic Stability of Slender Spinning Sounding Rockets | shows nastran model setup and validation, basically what we want to do | doi: 10.5028/jatm.v5i1.192 |
| [5]    | Supersonic Flutter Analysis Based on a Local Piston Theory | This paper presents the method we will try to use | https://www.researchgate.net/publication/245426315_Supersonic_Flutter_Analysis_Based_on_a_Local_Piston_Theory |
| [6]    | Piston Theory-A New Aerodynamic Tool for the Aeroelastician | used to understand some of the aero theory in [5] | https://arc.aiaa.org/doi/abs/10.2514/8.3740?journalCode=jans |
| [7]    | Ata engineering flutter tutorial | useful overview | https://www.youtube.com/watch?v=GjBXsR6SSLY&t=165s |
| [8]    | Toolchain for Aerodynamic Characterization of a Rocket During Ascent using OpenFOAM | OpenFOAM toolchain the cfd in this project is built on |https://github.com/WyllDuck/OpenFOAM-ToolChain-for-Rocket-Aerodynamic-Analysis |
| [9]    | OpenFOAM-ToolChain-helperFunctions | Helper functions from the same author as [8] for the toolchain | https://github.com/WyllDuck/OpenFOAM-ToolChain-helperFunctions/tree/30bf81273756a84d419085d8e594a9b08d46e7dd |
| [10]   | Docker instructions for [8],[9] | Setup CFD Toolkit | https://github.com/jakobhaervig/openfoam-dockerfiles |

<!-- This is a comment in a Markdown file (not rendered) --> 
