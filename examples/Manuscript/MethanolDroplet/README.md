# UCG Modeling of Methanol-Droplet

This folder contains the CG modeling of the methanol-air interface using the UCG-RLE method.
This work is an extention of the previous modeling of liquid-air interface. 

The similarities are:

1. This work is also using a unitary system (methanol molecules only)
2. This work is also to model the interface of a liquid cluster in vaccum
3. This work is also applying UCG-RLE algorithm with defining two sub-states for the methanol CG particles.

The difference are:

1. Instead of a SLAB system (a liquid methanol slab in XY-plane and with two flat surface along Z-axis), this
work is using a droplet model (sphere) in vaccum.
2. While z-axis density profile is used to analyze the model quality with a SLAB system, the radial density
profile (RDF) is used for the spherical system.

The files are organized as:

1. All-atom simulation

topol.top    - Gromacs input files (and the next two) for AA simulation
conf.gro
grompp.mdp
methanol_opls.itp
traj.trr     - AA simulation trajectory
cg.lammpstrj - CG trajectory mapped from AA trajectory 

2. Traditional MSCG work

mscg.py              - Script for MSCG modeling
cg.top               - CGTop file for MSCG model
cg_models.p          - Result of MSCG modeling
Pair_MeOH-MeOH.table - Dumped table for MSCG model
mscg_sim.dcd         - CG simulation trajectory

3. UCG work

ucg.py               - Script for UCG modeling
ucg-top.in           - CGTop file for UCG model
ucg_models.p         - Result of UCG-RLE modeling
Pair_Far-Far.table   - UCG pair tables (with the following two)
Pair_Near-Far.table
Pair_Near-Near.table
ucg_sim.dcd          - UCG simulation trajectory

4. Analysis

density.py           - Plot RDF from AA, MSCG and UCG trajectories
dump-ucg.py          - Dump and plot pairwise tables for MSCG and UCG models

The following trajectories can be downloaded here:

```
wget --no-check-certificate https://software.rcc.uchicago.edu/mscg/downloads/openmscg-examples/Manuscript/MethanolDroplet/cg.lammpstrj
```

```
wget --no-check-certificate https://software.rcc.uchicago.edu/mscg/downloads/openmscg-examples/Manuscript/MethanolDroplet/traj.trr
```

```
wget --no-check-certificate https://software.rcc.uchicago.edu/mscg/downloads/openmscg-examples/Manuscript/MethanolDroplet/mscg_sim.dcd
```

```
wget --no-check-certificate https://software.rcc.uchicago.edu/mscg/downloads/openmscg-examples/Manuscript/MethanolDroplet/ucg_sim.dcd
```