--top system.data
--traj dump.lammpstrj
--cut 7.0
--names SL
--pair model=BSpline,type=SL:SL,min=2.4,resolution=0.2,order=4
--save return
--verbose 0
