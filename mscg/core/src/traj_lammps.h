#ifndef TRAJ_LAMMPS_H
#define TRAJ_LAMMPS_H

#include "traj.h"
#include <cstdio>
#include <cstdlib>
#include <cstring>

class TrajLAMMPS : public Traj
{
  public:
  
    FILE *fp;
    
    TrajLAMMPS(const char*, const char*);
    virtual ~TrajLAMMPS();
    
    virtual int read_next_frame();
    virtual int write_frame();
    virtual void rewind();
    
    int read_head();
    int read_body();
    int parse_columns();
    
    char line[1001];
    char columns[1001];
    Vec boxlo;
    
    int cx, cy, cz, cfx, cvx, cvy, cvz, cfy, cfz, cid, ctype, cq, cxs, cys, czs;
    int _natoms;
    bool xs, ys, zs;
};

#endif
