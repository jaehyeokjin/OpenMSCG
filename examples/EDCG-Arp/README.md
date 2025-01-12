Example of EDCG for Arp2/3 Protein
======================================================

0. (Optional) Principal Component Analysis (PCA)

  * data.data -- LAMMPS data   
  * GC.dcd -- protein trajectory. Download here: 
  ```
  wget --no-check-certificate https://software.rcc.uchicago.edu/mscg/downloads/tutorial_trajectories/example_EDCG/GC.dcd
  ```
  * pca_ca_com.py -- python script to conduct PCA. Note: this script requires MDAnalysis. This step can be skipped, as the resulting files outputted from this script are already provided.

Run PCA via 'python pca_ca_com.py'.

1. Essential Dynamics Coarse-Graining (EDCG)

  * pc.npy -- PCA eigenvectors. Download here if Step 0 is skipped: 
  ```
  wget --no-check-certificate https://software.rcc.uchicago.edu/mscg/downloads/tutorial_trajectories/example_EDCG/pc.npy
  ```
  * ev.npy -- PCA eigenvalues

We will obtain an optimal mapping of 523 CG sites via EDCG using the 24 largest principal components. This can be accomplished via: 'cged --pc pc.npy --ev ev.npy --npc 24 --sites 523'.

2. Convert EDCG output to mapping file

  * map.txt -- EDCG output file
  * protein_1microsec.pdb -- all-atom PDB of Arp2/3 protein 
  * edcg_resolution_map.py -- python script to convert cged output to a YAML file for cgmap
  * resolution_edcg.yaml -- outputted yaml from edcg_resolution_map.py

To create a YAML file for use in the cgmap module of OpenMSCG, run 'python edcg_resolution_map.py'.
