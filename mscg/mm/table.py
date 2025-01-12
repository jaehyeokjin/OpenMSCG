#

from mscg import R2D
from ..table import *
import mscg.core.cxx_tables as lib

class ForceTable:
    def __init__(self, params):
        self.tables = {k:Table.load_lammps(v) for k, v in params.items()}
    
    def setup(self, top):
        if self.style == 'pair':
            self._h = lib.create(top.ntype_atom * top.ntype_atom)
        else:
            self._h = lib.create(getattr(top, 'ntype_' + self.style.lower()))
        
        for k, v in self.tables.items():
            ks = k.split('-')
            tid = top.pair_tid(*ks) if self.style == 'pair' else top.bonding_tid(self.style.lower(), ks)
            lib.set_table(self._h, tid, v)
    
    def compute(self, n, types, scalars, U, dU):
        lib.compute(self._h, n, types, scalars, U, dU)


class Pair_Table(ForceTable):
    pass

class Bond_Table(ForceTable):
    pass

class Angle_Table(ForceTable):
    def __init__(self, params):
        super().__init__(params)

        for k, t in self.tables.items():
            t['min']  /= R2D
            t['inc']  /= R2D
            t['ffac'] *= R2D

class Dihedral_Table(ForceTable):
    def __init__(self, params):
        super().__init__(params)

        for k, t in self.tables.items():
            t['min']  /= R2D
            t['inc']  /= R2D
            t['ffac'] *= R2D
