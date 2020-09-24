import pytest
from mscg.cli import cgderiv

def test_dimer(datafile):

    mean, var = cgderiv.main(
        top     = datafile("dimer_mixture.top"),
        traj    = datafile("dimer_mixture.lammpstrj"),
        cut     = 12.0,
        pair    = ["model=BSpline,type=1:1,min=3.0,resolution=0.5,order=4",
                   "model=BSpline,type=1:2,min=4.0,resolution=0.5,order=4",
                   "model=BSpline,type=1:3,min=3.0,resolution=0.5,order=4",
                   "model=BSpline,type=1:4,min=4.0,resolution=0.5,order=4",
                   "model=BSpline,type=2:2,min=4.0,resolution=0.5,order=4",
                   "model=BSpline,type=2:3,min=4.5,resolution=0.5,order=4",
                   "model=BSpline,type=2:4,min=4.5,resolution=0.5,order=4",
                   "model=BSpline,type=3:3,min=3.5,resolution=0.5,order=4",
                   "model=BSpline,type=3:4,min=4.5,resolution=0.5,order=4",
                   "model=BSpline,type=4:4,min=5.0,resolution=0.5,order=4",
                  ],
        verbose = 0,
        save    = 'return'
    )

    benchmark = [0.021775,0.068338,0.179148,0.366948,0.534709,0.756651,1.016840,1.318865,1.657591,2.139481,2.617115,3.030731,3.433730,3.880529,4.311300,4.828099,5.385412,5.878595,4.751690,3.324538,1.725302]
    
    coeffs = mean['Pair_1-1']
    print(','.join(["%0.6f" % (i) for i in coeffs]))
    print("")

    for i in range(len(benchmark)):
        diff = (coeffs[i] - benchmark[i]) / benchmark[i]
        print("X=%3d, Y0=%10.3e, Y=%10.3e, dY/Y0=%5.2f%%" %(i+1, benchmark[i], coeffs[i], diff*100))
        assert abs(diff)<0.01
    
    benchmark = [0.980744,3.033537,6.951531,9.963532,9.082668,8.267871,8.006254,8.412228,9.069888,9.357843,9.163096,9.305922,10.004852,10.963591,11.882818,9.517916,6.688733,3.460917]
    
    coeffs = mean['Pair_3-4']
    print(','.join(["%0.6f" % (i) for i in coeffs]))
    print("")

    for i in range(len(benchmark)):
        diff = (coeffs[i] - benchmark[i]) / benchmark[i]
        print("X=%3d, Y0=%10.3e, Y=%10.3e, dY/Y0=%5.2f%%" %(i+1, benchmark[i], coeffs[i], diff*100))
        assert abs(diff)<0.01


"""
1-1
0.014179	0.070982	0.179163	0.366252	0.534130	0.756797	1.017068	1.319161	1.657742	2.139628	
2.617742	3.031314	3.434005	3.880220	4.311505	4.828534	5.384616	5.878121	4.751956	3.323951	
1.724935	

1-2
0.074050	0.300359	0.824718	1.656390	2.256915	2.859712	3.520323	4.315712	5.131604	6.080868	
6.982294	7.848745	8.761923	9.668584	10.646791	11.773806	9.411014	6.580734	3.463959	

1-3
0.002514	0.057777	0.333231	0.977214	1.567562	2.056528	2.628818	3.431917	4.393275	5.473281	
6.558753	7.472532	8.174983	8.734260	9.309070	10.052216	10.955002	11.849095	9.466169	6.660705	
3.438096	

1-4
0.089237	0.591504	1.762546	3.338841	4.008355	4.513766	4.942704	5.544577	6.383056	7.072176	
7.557435	8.116238	8.805310	9.660791	10.639812	11.691358	9.384282	6.568511	3.430000	

2-2
0.001890	0.038315	0.224484	0.681609	1.096656	1.449012	1.855382	2.309375	2.751685	3.123814	
3.489183	3.894985	4.374902	4.845637	5.351964	5.810277	4.679748	3.317560	1.741522	

2-3
0.135301	0.689011	1.928805	3.698360	4.547580	5.186170	5.911250	6.647373	7.326064	7.905998	
8.455508	9.056047	9.863787	10.813184	11.807228	9.473229	6.630291	3.436313	

2-4
0.267236	1.237763	3.039428	4.981537	5.338978	5.567675	5.812738	6.276222	6.748115	7.138680	
7.740872	8.497649	9.458551	10.477793	11.512331	9.326746	6.632630	3.452558	

3-3
0.020836	0.290042	1.208948	2.423842	2.660659	2.748555	2.986411	3.419840	4.048840	4.759418	
5.148420	5.059131	5.045906	5.166702	5.442608	5.810646	6.169990	4.896404	3.385135	1.746167	

3-4
0.677539	3.129819	6.952351	9.964569	9.082199	8.267706	8.006635	8.410913	9.069717	9.358712	
9.162817	9.305760	10.004720	10.964643	11.883221	9.518874	6.688955	3.460350	

4-4
0.992616	3.373607	6.045705	7.169073	5.315829	4.211381	3.836292	3.637522	3.411918	3.439033	
3.887275	4.567946	5.282795	5.929778	4.818834	3.421183	1.775712	
"""