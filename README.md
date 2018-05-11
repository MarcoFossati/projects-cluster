# PASTA
**P**anel method **A**erodynamic **S**imulation and **T**hermal **A**nalysis

A project to formulate and implement low-fidelity methods to study the aero(thermo)dynamics interaction over subsonic, transonic, supersonic and hypersonic regimes.

**Official repository for all PASTA code and documentation**

## Installation
**WINDOWS (must be Windows 10 or later)**
1. Download setup.exe and setup.msi, ensuring both are saved to the same folder
2. Run setup.exe 
3. Follow the installation wizard to install PASTA to the desired directory

**LINUX**
1. Download and extract the Linux directory
2. Place the directory in any location
3. Run using the PASTA.out program




## Input
**Initialisation**
- Main Directory - Must be the full directory, punctuated using single forward slashes. Must also finish with a single forward slash e.g. C:/Users/Steve/Documents/PASTA/PASTA_1.2/
- On Linux this should be punctuated with forward slashed, e.g. /home/Steve/Location/
- Geometry Directory - Same as for Main Directory
- STL File Name - must exactly match the desired filename located in the specified geometry folder, including the .STL e.g. Orion.STL

**Operational**
- Altitude (km) - Must lie between 0 and 1000km
- Velocity (m/s)
- Angle of Attack (deg)
- Angle of Sideslip (deg)
- Fixed Wall Temperature (K)

**Design**
- Reference Length (m) - e.g. Mean Aerodynamic Chord 
- Reference Cross Section (m^2) - Cross sectional area of the geometry at the specified angle of attack. This can be determined using 3D visualisation software such as Paraview <link>
- Nose Radius (m)

**Model Selection**
- USSA 76 (US Standard Atmosphere 1976)
- NRLMSISE-00 (Naval Research Laboratory Mass Spectrometer Incoherent Scatter Radar Model 2000)

Indicate model selection using either 1 or 0. Only one model can be selected at any one time. 



## Notes
**STL File Format**

The STL geometry must have units of meters, and conform to the following orientation:
  - Front face of geometry - Faces the negative X direction
  - Top surface of geometry - Positive Z direction
  - Starboard side of geometry - Positive Y direction


**STL File Size**

The length of time taken for PASTA to complete one simulation is directly dependant on the number of elements used to represent the geometry. Details of computational time can be found in the documnetation. We recommend the following geometry specifications to acheive the best results using PASTA:
  - Between 10,000 and 20,000 elements
  - Uniform size and distribution (Elements dominated by one particular dimension are not advised)


