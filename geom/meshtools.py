import sys
import struct
import numpy as np
from colorama import Fore, init

init(autoreset=True)

#----------------------------------------------------------------------
#
#    Untructured Mesh Class for 3D mesh
#
#----------------------------------------------------------------------
class meshclass(object):
    # --- Empty constructor ---
    def __init__(self, nnodes = None, ntrias = None, nquads = None, ntetrs = None, npyrms = None, nprsms = None, nhexas = None):
        if nnodes is None:
            self.nnodes = 0
        else:
            self.nnodes = nnodes
            
        if ntrias is None:
            self.ntrias = 0
        else:
            self.ntrias = ntrias
            
        if nquads is None:
            self.nquads = 0
        else:
            self.nquads = nquads
            
        if ntetrs is None:
            self.ntetrs = 0
        else:
            self.ntetrs = ntetrs
            
        if npyrms is None:
            self.npyrms = 0
        else:
            self.npyrms = npyrms
            
        if nprsms is None:
            self.nprsms = 0
        else:
            self.nprsms = nprsms
            
        if nhexas is None:
            self.nhexas = 0
        else:
            self.nhexas = nhexas
        
        self.nodes = np.zeros((self.nnodes,            4), dtype = float) # nid, x, y, z
        self.trias = np.zeros((self.ntrias,            5), dtype = int) # eid, nid1, nid2, nid3, surfid
        self.quads = np.zeros((self.nquads,            6), dtype = int) # eid, nid1, nid2, nid3, nid4, surfid     
        self.tetrs = np.zeros((self.ntetrs,            5), dtype = int)
        self.pyrms = np.zeros((self.npyrms,            6), dtype = int)
        self.prsms = np.zeros((self.nprsms,            7), dtype = int)
        self.hexas = np.zeros((self.nhexas,            9), dtype = int)
        # NO LONGER NEEDED self.surfs = np.zeros((self.nquads + self.ntrias), dtype = int)
        
        return
    
    def nodebyid(self, nodeid):
        index = np.where(self.nodes[:,0] == nodeid)
        return self.nodes[index[0][0]]
    
#----------------------------------------------------------------------
#
#    Structured Mesh Class for single block 3D mesh
#
#----------------------------------------------------------------------
class structmeshclass(object):
    def __init__(self, ni = None, nj = None, nk = None, X = None, Y = None, Z = None):
        if ni is None:
            self.ni = 0
        else:
            self.ni = ni
            
        if nj is None:
            self.nj = 0
        else:
            self.nj = nj
        
        if nk is None:
            self.nk = 0
        else:
            self.nk = nk    
            
        if X is None:
            self.X = np.zeros((self.ni, self.nj, self.nk))
        else:
            self.X = X
            
        if Y is None:
            self.Y = np.zeros((self.ni, self.nj, self.nk))
        else:
            self.Y = Y
            
        if Z is None:
            self.Z = np.zeros((self.ni, self.nj, self.nk))
        else:
            self.Z = Z


        return
    def get(self, i, j, k):
        node = np.array([self.X[i,j,k], self.Y[i,j,k], self.Z[i,j,k]])
        
        return node
        
def struct2unstruct(structmesh):
    # If multiblock grab the 1st block and 1st surface
    k = 0
    if isinstance(structmesh, list):
            structmesh = structmesh[0]
    
    unstructmesh = meshclass(nnodes = (structmesh.ni * structmesh.nj), 
                             ntrias = 2*((structmesh.ni - 1) * (structmesh.nj - 1)))
    
    inode = 0
    itria = 0
    for j in range(structmesh.nj):
        for i in range(structmesh.ni):        
            # Store the node
            node = structmesh.get(i,j,k)
            unstructmesh.nodes[inode] = [inode+1, node[0], node[1], node[2]]
            inode += 1
            
            if (i < (structmesh.ni -1)) and (j < (structmesh.nj - 1)):
                # Store the elements
                nij     = j*structmesh.ni + i + 1
                nip1j   = j*structmesh.ni + (i+1) + 1
                nijp1   = (j+1)*structmesh.ni + i + 1
                nip1jp1 = (j+1)*structmesh.ni + (i+1) + 1
                
                #print(' (i,j) = (%d,%d) inode = %d' % (i,j,inode-1))
                #print(' trias: %d, %d, %d, %d' % (nij, nip1j, nijp1, nip1jp1))
                
                unstructmesh.trias[itria] = [itria+1, nij, nijp1, nip1jp1, 1]; itria += 1
                unstructmesh.trias[itria] = [itria+1, nij, nip1jp1, nip1j, 1]; itria += 1
            
            
        
    
    return unstructmesh

def renumber_elements(elements, map, nnids=None):
    if elements.any():
        if nnids is None:
            nnids = len(elements[0]) - 2 # This assumes the last column is a surface id (we do +1 later)
        
        # Now loop through the elements and renumber the nids using the map
        for ielem in range(len(elements)):
            for inid in range(1, nnids + 1): # First column is element id
                newnid = map[elements[ielem, inid]]
                elements[ielem, inid] = newnid
    
    return elements
    