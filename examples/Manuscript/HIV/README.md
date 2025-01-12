#######################################################################
#### The following is a step-by-step tutorial on how to prepare
#### a bottom-up CG protein model (example: HIV-1 CASP1 protein)
#### Created by Alex Pak (Colorado School of Mines, Aug 2023)

#### CG workflow tested using:
#### openmscg 0.7.1 (see note below)
#### numpy 1.24.3
#### scikit-learn 1.2.2
#### scipy 1.10.1
#######################################################################

#### In each of the following folders, you will see
#### - inputs - contains all the input files needed for the process
#### - outputs - contains the outputs of "run_me.bash" 

#### Step 0 - AAMD #### 
````
Download: wget --no-check-certificate https://software.rcc.uchicago.edu/mscg/downloads/openmscg-examples/Manuscript/HIV/part0_aamd
````
#### look in part0_aamd to see the final AAMD trajectory+topology files
#### - merge.trr - protein trajectory of 18-mer
#### - protein.pdb - PDB file of 18-mer

#### Step 1 - EDCG (mapping) ####
````
Download: wget --no-check-certificate https://software.rcc.uchicago.edu/mscg/downloads/openmscg-examples/Manuscript/HIV/part1_edcg
````
cd part1_edcg
bash run_me.bash

#### Step 2 - hENM (intra-protein bond network) ####
````
Download: wget --no-check-certificate https://software.rcc.uchicago.edu/mscg/downloads/openmscg-examples/Manuscript/HIV/part2_henm
````
cd ../part2_henm
bash run_me.bash

#### Step 3 - Analyze CG-mapped AAMD traj ####
````
Download: wget --no-check-certificate https://software.rcc.uchicago.edu/mscg/downloads/openmscg-examples/Manuscript/HIV/part3_aa_analysis
````
cd ../part3_aa_analysis
bash run_me.bash

#### Step 4 - REM (inter-protein interactions) ####
````
Download: wget --no-check-certificate https://software.rcc.uchicago.edu/mscg/downloads/openmscg-examples/Manuscript/HIV/part4_rem
````
cd ../part4_rem
bash run_me.bash

#### Step 5 - Compare CG vs AA traj ####
````
Download: wget --no-check-certificate https://software.rcc.uchicago.edu/mscg/downloads/openmscg-examples/Manuscript/HIV/part5_analysis
````
cd ../part5_analysis
bash run_me.bash

#######################################################################
#### NOTE :
#### I modified cgib to handle detection of pairs with zero
#### data (pair distances) within the given cutoff distance
#### (the modified code is in this directory)
#######################################################################
