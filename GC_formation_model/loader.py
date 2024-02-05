# Licensed under BSD-3-Clause License - see LICENSE

import h5py
import symlib
import os
import pickle
import numpy as np

def load_merger_tree(base, hid_root, fields=None):

    res = {}

    if fields is None:
        fields = ['SubhaloMass', 'FirstProgenitorID', 'SubhaloID', 'SnapNum', 
            'MainLeafProgenitorID', 'NextProgenitorID', 'DescendantID', 
            'SubfindID', 'SubhaloPos', 'LastProgenitorID']

    filename = base + 'merger_tree_%d.hdf5'%hid_root

    with h5py.File(filename, 'r') as f:
        for field in fields:
            res[field] = f[field][:]

    return res

def getLastProgID(aux, base, hid_root, hid):
    # spoofed readLastProgID function

    dfid = symlib.read_tree(os.path.join(base, hid_root), ['dfid'])
    
    filename = os.path.join(aux, f"last_prog_id_{hid_root}.pkl")
    last_prog_id = None

    with open(filename, 'rb') as f:
        last_prog_id_list = pickle.load(f)
        dfid_idx = np.where(dfid == hid)[0][0]
        last_prog_id = last_prog_id_list[dfid_idx]
    
    return last_prog_id



def load_halo(base, hid_root, hid, snap, parttype, fields=None):
    # spoofed load_halo function
    res = {}

    symphony_fields = {
            'Coordinates': 'x',
            'Velocities': 'v',
            'ParticleIDs': 'id',
        }

    mode = "current"
    
    gal_halo = symlib.DWARF_GALAXY_HALO_MODEL

    if parttype == "stars":
        mode = "stars"

    part = symlib.Particles(os.path.join(base, hid_root))
    p = part.read(snap, mode=mode, halo=hid)

    for i, field in enumerate(list(symphony_fields.keys())):
        res[field] = p[symphony_fields[field]]

    if parttype == "stars":
        stars, gals, ranks = symlib.tag_stars(base, gal_halo, target_subs=[hid])
        res['GFM_StellarFormationTime'] = stars['a_form']
    
    res['count'] = len(res['Coordinates'])

    return res