'''Distribution and Boltzmann inversion analysis

Description
-----------

The ``cgib`` command is used to analyze the MD trajectoris and calculate the distribution histograms for targeted structural variables: **pairs, bonds, angles and dihedral torsions**. The function can be used to find the ranges of these variables, which can be used for the force-matching method later. This command also calculates the **Boltzmann-Inversed (IB)** free energy profiles for the given variables.


Usage
-----

Syntax of running ``cgib`` command ::

    usage: cgib [-h] [-v] --top file [--names] [--traj file[,args]] [--cut]
            [--temp] [--pair types,args] [--bond types,args]
            [--angle types,args] [--plot U or N]

    General arguments:
      -h, --help          show this help message and exit
      -v , --verbose      screen verbose level (default: 0)

    Required arguments:
      --top file          topology file (default: None)

    Optional arguments:
      --names             comma separated atom type names (needed when using
                          LAMMPS data file for topology) (default: None)
      --traj file[,args]  reader for a trajectory file, multiple fields separated
                          by commas, the first field is the file name, while
                          others define the skip, every and frames (default args:
                          file,skip=0,every=1,frames=0) (default: [])
      --cut               cut-off for pair interactions (default: 10.0)
      --exclude           exclude 1-2, 1-3, 1-4 bonding neighbors in the pair-
                          ist (default: 111)
      --temp              temperature (K) for IB (default: 298.15)
      --pair types,args   define new pair analysis with format: type1,type2,args;
                          args and default values are: min=0,max=10,bins=10
                          (default: [])
      --bond types,args   define new bond analysis with format: type1,type2,args;
                          args and default values are: min=0,max=10,bins=10
                          (default: [])
      --angle types,args  define new angle analysis with format:
                          type1,type2,type3,args; args and default values are:
                          min=0,max=10,bins=10 (default: [])
      --dihed types,args  define new dihedral torsion analysis with format:
                          type1,type2,type3,type4,args; args and default values are:
                          min=0,max=10,bins=10 (default: [])
      --plot U or n       plot the results of U (potential) or n (distribition)
                          (default: U)

'''

import numpy as np
from mscg import *


class Histogram:
    def __init__(self, n, name, args):
        self.ntype = n
        self.types = None
        self.name  = name
        
        self.min   = 0
        self.max   = 10
        self.bins  = 10
        
        self.id    = None
        self.x     = None
        self.n     = None
        self.U     = None
        self.range = None
        
        segs = args.split(",")
        if len(segs) != self.ntype + 3:
            raise Exception('incorrect number of fields for option --' + self.name + ' ' + args)
        
        self.types = segs[:n]
        self.name = "-".join(self.types)
        
        for i in range(n, len(segs)):
            w = segs[i].split('=')
            if w[0] == "min":
                self.min = float(w[1])
            elif w[0] == "max":
                self.max = float(w[1])
            elif w[0] == "bins":
                self.bins = int(w[1])
            else:
                raise Exception('incorrect format of value for option --' + self.name + ' ' + segs[i])
        

def BuildHistAction(n, arg_name):
    class HistAction(argparse.Action):
        nbody = n
        name = arg_name
        
        def __call__(self, parser, namespace, values, option_string=None):
            
            getattr(namespace, self.dest).append(Histogram(HistAction.nbody, HistAction.name, values))
            return
        
        def help():
            msg = "define new " + HistAction.name + " analysis with format: "
            msg += ",".join(["type" + str(i+1) for i in range(HistAction.nbody)]) 
            msg += ",args; args and default values are: min=0,max=10,bins=10"
            return msg
            
    return HistAction



def main(*args, **kwargs):
    
    # parse argument
    
    desc = 'Run MSCG Range-finder, RDF Calculations, or Inversed-boltzmann method. For detailed instructions please read ' + doc_root + 'commands/cgib.html'
    
    parser = CLIParser(description=desc, formatter_class=argparse.ArgumentDefaultsHelpFormatter, fromfile_prefix_chars='@', add_help=False)
    
    group = parser.add_argument_group('General arguments')
    group.add_argument("-h", "--help", action="help", help="show this help message and exit")
    group.add_argument("-v", "--verbose", metavar='', type=int, default=0, help="screen verbose level")
    
    group = parser.add_argument_group('Required arguments')
    group.add_argument("--top",  metavar='file', action=TopAction, help=TopAction.help, required=True)
    
    group = parser.add_argument_group('Optional arguments')
    group.add_argument("--names",  metavar='', type=str, help="comma separated atom type names (needed when using LAMMPS data file for topology)")
    group.add_argument("--traj", metavar='file[,args]', action=TrajReaderAction, help=TrajReaderAction.help, default=[])
    group.add_argument("--cut",  metavar='', type=float, default=10.0, help="cut-off for pair interactions")
    group.add_argument("--exclude", metavar='', type=str, default="111", help="exclude 1-2, 1-3, 1-4 bonding neighbors in the pair-list")
    
    group.add_argument("--temp", metavar='', type=float, default=298.15, help="temperature (K) for IB")
    
    PairAction = BuildHistAction(2, "pair")
    group.add_argument("--pair", metavar='types,args', action=PairAction, help=PairAction.help(), default=[])
    
    BondAction = BuildHistAction(2, "bond")
    group.add_argument("--bond", metavar='types,args', action=BondAction, help=BondAction.help(), default=[])
    
    AngleAction = BuildHistAction(3, "angle")
    group.add_argument("--angle", metavar='types,args', action=AngleAction, help=AngleAction.help(), default=[])
    
    DihedAction = BuildHistAction(4, "dihedral")
    group.add_argument("--dihedral", metavar='types,args', action=DihedAction, help=DihedAction.help(), default=[])
    
    group.add_argument("--plot", metavar='U or N', type=str, default='U', help="plot the results of U (potential) or n (distribition)")
    
    group.add_argument("--save", metavar='prefix or return', default='noname', type=str)
    
    if len(args)>0 or len(kwargs)>0:
        args = parser.parse_inline_args(*args, **kwargs)
    else:
        args = parser.parse_args()
    
    screen.verbose = args.verbose
    screen.info("OpenMSCG CLI Command: " + __name__)
    
    # load topology
    
    screen.info("Check topology ... ")
    
    if args.names is not None:
        args.top.reset_names(args.names.split(','))
    
    # prepare lists
    
    screen.info("Build pair and bonding list-based algorithm ...")
    plist = PairList(cut = args.cut, binsize = args.cut * 0.5)
    plist.init(args.top.types_atom, args.top.linking_map(*([bit=='1' for bit in args.exclude[:3]])))
    blist = BondList(
        args.top.types_bond, args.top.bond_atoms, 
        args.top.types_angle, args.top.angle_atoms, 
        args.top.types_dihedral, args.top.dihedral_atoms)
        
    # prepare plots
    
    names_atom = args.top.names_atom

    if args.pair is not None:
        for pair in args.pair:
            screen.info("Add pair plot: " + pair.name)
            pair.id = args.top.pair_tid(pair.types[0], pair.types[1])
            
    if args.bond is not None:
        for bond in args.bond:
            screen.info("Add bond plot: " + bond.name)
            bond.id = args.top.bonding_tid('bond', bond.types)

    if args.angle is not None:
        for angle in args.angle:
            screen.info("Add angle plot: " + angle.name)
            angle.id = args.top.bonding_tid('angle', angle.types)
    
    if args.dihedral is not None:
        for dihed in args.dihedral:
            screen.info("Add dihedral plot: " + dihed.name)
            dihed.id = args.top.bonding_tid('dihedral', dihed.types)
    
    # start processing trajectory
    
    TIMER.reset()
    last = TIMER.last
    
    vol = 0.0

    for reader in TrajBatch(args.traj, natoms = args.top.n_atom, cut = plist.cut):

        if reader.nread == 1:
            plist.setup_bins(reader.traj.box)
            vol = np.prod(reader.traj.box)

        TIMER.click('io')
        
        # process pair styles
        
        if len(args.pair)>0: 
            plist.build(reader.traj.x)
            
            for pair in args.pair:
                
                for page in plist.pages(pair.id):
                    hist, edges = np.histogram(page.r, bins=pair.bins, range=(pair.min, pair.max))
                    
                    if pair.n is None:
                        pair.n, pair.x = hist, edges[:-1] + np.diff(edges) * 0.5
                        pair.range = [page.r.min(), page.r.max()]
                    else:
                        pair.n += hist
                        pair.range[0] = min(pair.range[0], page.r.min())
                        pair.range[1] = max(pair.range[1], page.r.max())
            
            TIMER.click('pair')
        
        # process bonding styles

        if len(args.bond)>0 or len(args.angle)>0 or len(args.dihedral)>0:
            blist.build(reader.traj.box, reader.traj.x)
            
            def process_hist(one, types, vals):
                vals = vals[types==one.id]
                hist, edges = np.histogram(vals, bins=one.bins, range=(one.min, one.max))

                if one.n is None:
                    one.n, one.x = hist, edges[:-1] + np.diff(edges) * 0.5
                    one.range = [vals.min(), vals.max()]
                else:
                    one.n += hist
                    one.range[0] = min(one.range[0], vals.min())
                    one.range[1] = max(one.range[1], vals.max())

            for one in args.bond:
                z = blist.get_scalar('bond')
                types = args.top.types_bond
                process_hist(one, types, z)

            for one in args.angle:
                z = blist.get_scalar('angle') * R2D
                types = args.top.types_angle
                process_hist(one, types, z)
            
            for one in args.dihedral:
                z = blist.get_scalar('dihedral') * R2D
                types = args.top.types_dihedral
                process_hist(one, types, z)

            TIMER.click('bond')
        
        # end of one trajectory
        
    if screen.verbose > 0:
        screen.info([""] + TIMER.report(False) + [""])
        
    # end of processing trajectories
    
    # dump results
    
    def post_process(d, prefix):
        valid = d.n > 1.0E-40
        d.x = d.x[valid]
        d.n = d.n[valid]
        d.U = -0.0019872041 * args.temp *np.log(d.n)
        
        return {
            'name': prefix + '-' + d.name,
            'data': np.vstack([d.x, d.n, d.U]).T
        }

    results = []

    for pair in args.pair:
        N1 = np.count_nonzero(args.top.types_atom == names_atom.index(pair.types[0]))
        #double count pair histogram for like types, density normalization
        if pair.types[0] ==  pair.types[1]:                               
            pair.n = 2.0*np.divide(pair.n,  ((N1 - 1.0) * N1 / vol))
        else:
            N2 = np.count_nonzero(args.top.types_atom == names_atom.index(pair.types[1]))
            pair.n = np.divide(pair.n,  (N1 * N2 / vol))
        #shell normalization
        pair.n = np.divide(pair.n, 4.0 * np.pi * np.square(pair.x) * (pair.x[1] - pair.x[0]))
        #frame normalization
        pair.n = np.divide(pair.n, reader.nread)
        results.append(post_process(pair, 'Pair'))
        screen.info("Pair: " + pair.name + " " + str(pair.range))
        
    for bond in args.bond:
        bond.n = np.divide(bond.n, bond.n.max())
        results.append(post_process(bond, 'Bond'))
        screen.info("Bond: " + bond.name + " " + str(bond.range))
        
    for angle in args.angle:
        angle.n = np.divide(angle.n, angle.n.max())
        results.append(post_process(angle, 'Angle'))
        screen.info("Angle: " + angle.name + " " + str(angle.range))
    
    for dihed in args.dihedral:
        dihed.n = np.divide(dihed.n, dihed.n.max())
        results.append(post_process(dihed, 'Dihedral'))
        screen.info("Dihedral: " + dihed.name + " " + str(dihed.range))
        
    if args.save == 'return':
        return results
    else:
        for res in results:
            np.savetxt(args.save + "_" + res['name'] + '.dat', res['data'])

    if args.plot != 'none':
        import matplotlib.pyplot as plt

        for pair in args.pair:
            plt.plot(pair.x, getattr(pair, args.plot), label='Pair ' + pair.name)
        
        for bond in args.bond:
            plt.plot(bond.x, getattr(bond, args.plot), label='Bond ' + bond.name)
        
        for angle in args.angle:
            plt.plot(angle.x, getattr(angle, args.plot), label='Angle ' + angle.name)
        
        for dihed in args.dihedral:
            plt.plot(dihed.x, getattr(dihed, args.plot), label='Dihedral ' + dihed.name)
            
        plt.legend(loc='upper right')
        plt.show()
    
    screen.info("Processing is finished.")



if __name__ == '__main__':
    main()
