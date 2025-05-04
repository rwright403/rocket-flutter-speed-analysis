# rocket-flutter-speed-analysis 🚀
A loosely coupled flutter speed calculator built using open-source and software available to students (from a student license).
Based on the method created by [5]

## Required Program Inputs:

### Structual Model - from ALTAIR OPTISTRUCT NASTRAN:
The following data from ALTAIR OPTISTRUCT in the following NASTRAN Format:
(note: either file works, this is just what I think gets output from each type)

#### .OP2 Outputs:
- natural frequencies
- mode shapes
(below are nice to have)
- element centroids
- element normal vectors

#### .OP4 Outputs:
- Global Mass Matrix
- Global Stiffness Matrix
   - Order of nodes along matrix diagonals


### CFD - from Openfoam:
The following freestream and local (at NASTRAN element centroids) flow data:
- pressure (p)
- density (rho)
- speed of sound (a) 
- flow velocity (U)

Try to use OPENFOAM Sampling (postprocessing) tool to get flow data at NASTRAN element centroids https://www.openfoam.com/documentation/guides/latest/doc/guide-fos-sampling-sets.html


## Running this program:
This file takes input in the form of a python module file. 

In the directory this file is in:  #python3 -m src <filename of a desired python module file without the .py>

The inputs folder contains the input files where the user can update the inputs the program uses.



# Documentation

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
- Altair Hypermesh (NASTRAN) did not have a supersonic aero model available

Therefore we need to work at a lower level and build the flutter solver ourselves: 
New approach "weakly coupled solver" - using [5] as a guide.
This method requires a Harmonics and a CFD Simulation


## Inputs:

   ## Harmonics Simulation
   - Altair Student edition is easy for me to obtain as a student. It is the least restrictive and NASTRAN files are easy to parse.
   - (also can get the mass and stiffness matrices from the same program)

   ## CFD Simulation
   - OpenFOAM, see [8],[9],[10] for toolkit used to assist with setting up simulations



<!-- Using a virtual environment to stop this from interfering w other python projects:
Enter virtual env with 
> source venv/bin/activate
Exit with - deactivate -->


## Structural Model🗼
From OPTISTRUCT

### Fuselage and Nosecone 
???
can we treat as rigid?

### Fin 
is being loaded in:
- Out of plane bending
- Torision
- Shear

Assuming small deformations (linear) to start




## Mass Model ⚖️
From OPTISTRUCT


## Aerodynamic Model ✈️ - See [5]
Unsteady Aerodynamic Model created with local piston theory and steady CFD results from method in [5]

First Try: First Order Local Piston Theory, from [5] looks like we will likely want a higher order model
Assumptions:
- Small peturbations
- thin airfoil

## Interpolation ➰
Need to interpolate the pressure field to the locations of the structural element nodes. 

For element normal vectors and deflections, taken at element level. Need to solve aero at element node center and interpolate to structural model
- We can likely use this library https://docs.pyvista.org/examples/01-filter/interpolate
Note!!!! we are interpolating unsteady pressure --> complex numbers. 
This cannot interpolate complex numbers directly, but we can split and interpolate real and complex parts separately.



## Other Assumptions and Notes 📝
- want to recreate experimental data to validate our understanding/methods
- likely want to do a mesh convergence study on model
- temperature effects? - probably out of scope given ideal timeline but an understanding of the level of impact and how that would impact the flutter speed would be useful

## Solver 📝


potentially ~ https://fenicsproject.org/ 



## Postprocessing 🛠️🐍
none - if it has a gui are you really innovating?



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
| [11]   | OS-T: 1110 Modal Analysis Setup | Altair Modal Analysis Setup |https://2021.help.altair.com/2021/hwsolvers/os/topics/solvers/os/modal_analysis_setup_r.htm
| [12]   | Altair community fourum "How do i export stiffness and mass matrices from Optistruct?" | | https://community.altair.com/discussion/25732/how-do-i-export-stiffness-and-mass-matrices-from-optistruct|


<!-- modal superposition formula det. if useful https://docs.software.vt.edu/abaqusv2023/English/SIMACAEGSARefMap/simagsa-c-dynmodsuperpos.htm -->

<!-- This is a comment in a Markdown file (not rendered) --> 
