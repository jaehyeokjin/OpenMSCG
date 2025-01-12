import numpy as np
import MDAnalysis as mda
import yaml

mapping = yaml.safe_load(open("resolution_edcg.yaml", 'r'))
u = mda.Universe("protein_1microsec.pdb")

def MassCenter(grp, indices):
	ans = np.array([0,0,0], dtype=float)
	tot = 0
	for idx in indices:
		ans += grp.atoms.positions[idx] * grp.atoms[idx].mass
		tot += grp.atoms[idx].mass
	return ans/tot

# Generate CG coordinate
CG_coord = []
for grp in mapping["system"]:
	for repeat in range(grp["repeat"]):
		for site in grp["sites"]:
			tmp = [site[0]]
			tmp2 = [grp["anchor"]+repeat*grp["offset"]+site[1]+idx for idx in mapping["site-types"][site[0]]["index"]]
			tmp = tmp + [str(x) for x in MassCenter(u, tmp2[:])]
			CG_coord.append(tmp[:])

# Write to xyz
OutFile = open("protein_1microsec_CG.xyz", "w")
OutFile.write(str(len(CG_coord))+"\n")
OutFile.write("CG coordinate file generated by Ace Yang\n")
OutFile.write("\n".join(["  ".join(line) for line in CG_coord]))
OutFile.close()