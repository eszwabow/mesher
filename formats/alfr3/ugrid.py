'''
Created on Jun 14, 2018

@author: eszwabowski
'''

import sys
import struct
import numpy as np
from colorama import Fore, init

init(autoreset=True)


from geom import meshtools
    
# --------- Routines for reading a *.ugrid file --------- #
def getformat(filename):
    
    # --- Get the file format from the *.ugrid filename ---
    
    print(Fore.GREEN + 'This machine is %s endian.' % sys.byteorder)
    
    format_str = filename.split('.')[-2]
    
    file_format = {}
    file_format['int_bytesize'] = 0
    file_format['float_bytesize'] = 0
    file_format['int_format'] = ''
    file_format['float_format'] = ''
        
    if format_str == 'b8':
        # Binary double big endian
        file_format['int_bytesize'] = 4
        file_format['float_bytesize'] = 8
        file_format['int_format'] = '>L'
        file_format['float_format'] = '>d'
        print(Fore.GREEN + 'Reading in a binary double big-endian file')
        
    elif format_str == 'b4':
        # Binary float big endian
        file_format['int_bytesize'] = 4
        file_format['float_bytesize'] = 4
        file_format['int_format'] = '>L'
        file_format['float_format'] = '>f'
        print(Fore.GREEN + 'Reading in a binary float big-endian file')
        
    elif format_str == 'lb8':
        # Binary double little endian
        file_format['int_bytesize'] = 4
        file_format['float_bytesize'] = 8
        file_format['int_format'] = '<L'
        file_format['float_format'] = '<d'
        print(Fore.GREEN + 'Reading in a binary double little-endian file')
        
    elif format_str == 'lb4':
        # Binary float little endian
        file_format['int_bytesize'] = 4
        file_format['float_bytesize'] = 4
        file_format['int_format'] = '<L'
        file_format['float_format'] = '<f'
        print(Fore.GREEN + 'Reading in a binary float little-endian file')
        
    elif format_str == 'r8':
        # FORTRAN unformatted real*8 big endian
        # NOT IMPLEMENTED
        print(Fore.RED + 'FORTRAN unformatted real*8 big endian not implemeted')
        exit()
    
    elif format_str == 'r4':
        # FORTRAN unformatted real*4 big endian
        # NOT IMPLEMENTED
        print(Fore.RED + 'FORTRAN unformatted real*4 big endian not implemeted')
        exit()
        
    elif format_str == 'lr8':
        # FORTRAN unformatted real*8 little endian
        # NOT IMPLEMENTED
        print(Fore.RED + 'FORTRAN unformatted real*4 litte-endian not implemeted')
        exit()
        
    elif format_str == 'lr4':
        # FORTRAN unformatted real*4 little endian
        # NOT IMPLEMENTED
        print(Fore.RED + 'FORTRAN unformatted real*4 litte-endian not implemeted')
        exit()
        
    else:
        # ASCII
        # NOT IMPLEMENTED
        print(Fore.RED + 'ASCII not implemented')
        exit()
    
    return file_format
    
def readint(fp, file_format):
    # --- Read an integer value ---    
    record = fp.read(file_format['int_bytesize'])
    n = int(struct.unpack(file_format['int_format'], record)[0])
    return n

def readfloat(fp, file_format):
    # --- Read a float/double ---
    record = fp.read(file_format['float_bytesize'])
    num = float(struct.unpack(file_format['float_format'], record)[0])
    return num

def readheader(fp, file_format):
    # --- Reads in the header data ---
    
    # Go to start of file
    fp.seek(0)

    nnodes = readint(fp, file_format)
    ntrias = readint(fp, file_format)
    nquads = readint(fp, file_format)
    ntetrs = readint(fp, file_format)
    npyrms = readint(fp, file_format)
    nprsms = readint(fp, file_format)
    nhexas = readint(fp, file_format)
    
    print(Fore.GREEN + '  Nodes:    %d' % (nnodes))
    print(Fore.GREEN + '  Tris:     %d' % (ntrias))
    print(Fore.GREEN + '  Quads:    %d' % (nquads))
    print(Fore.GREEN + '  Tets:     %d' % (ntetrs))
    print(Fore.GREEN + '  Pyramids: %d' % (npyrms))
    print(Fore.GREEN + '  Prisms:   %d' % (nprsms))
    print(Fore.GREEN + '  Hexes:    %d' % (nhexas))
    
    return nnodes, ntrias, nquads, ntetrs, npyrms, nprsms, nhexas


def remove_orphans(ugridmesh):   
    
    # Loop over each node and see if it is used
    nodes2keep = np.zeros(len(ugridmesh.nodes), dtype = bool)
    inode = 0
    for node in ugridmesh.nodes:
      if ( (node[0] in ugridmesh.trias[:,1:-1]) or
           (node[0] in ugridmesh.quads[:,1:-1]) or
           (node[0] in ugridmesh.tetrs[:,1:]) or
           (node[0] in ugridmesh.pyrms[:,1:]) or
           (node[0] in ugridmesh.prsms[:,1:]) or
           (node[0] in ugridmesh.hexas[:,1:]) ):
          nodes2keep[inode] = True
          inode += 1
     
    # Remove the orphan nodes with the mask     
    new_nodes = ugridmesh.nodes[nodes2keep]
    
    # Now we will loop through the new nodes and map
    # the old nid to the new one
    old2newids = {}
    for inode in range(len(new_nodes)):
        old2newids[new_nodes[inode,0]] = inode + 1 # 1 based index
        new_nodes[inode,0] = inode + 1 # Renumber it after it is mapped
    
    # Insert the new nodes into the mesh object
    ugridmesh.nodes = new_nodes
    ugridmesh.nnodes = len(new_nodes)
        
    # Now loop through the elements and renumber the nids using the map  
    ugridmesh.trias = meshtools.renumber_elements(ugridmesh.trias, old2newids, nnids=3)
    ugridmesh.quads = meshtools.renumber_elements(ugridmesh.quads, old2newids, nnids=4)
    
    ugridmesh.tetrs = meshtools.renumber_elements(ugridmesh.tetrs, old2newids, nnids=4)
    ugridmesh.pyrms = meshtools.renumber_elements(ugridmesh.pyrms, old2newids, nnids=5)
    ugridmesh.prsms = meshtools.renumber_elements(ugridmesh.prsms, old2newids, nnids=6)
    ugridmesh.hexas = meshtools.renumber_elements(ugridmesh.hexas, old2newids, nnids=8)
    
    return ugridmesh
    
def read(filename, only_surf=False):   
    # --- Reads in an aflr3 formatted grid ---    
    print(Fore.GREEN + 'Reading %s...' % filename) 
    file_format = getformat(filename)
    
    ugridmesh = meshtools.meshclass()
    
    with open(filename, 'rb') as fp:
        
        # Read the header
        ugridmesh.nnodes, ugridmesh.ntrias, ugridmesh.nquads, ugridmesh.ntetrs, ugridmesh.npyrms, ugridmesh.nprsms, ugridmesh.nhexas = readheader(fp, file_format)
        
        ugridmesh.nodes = np.resize(ugridmesh.nodes, (ugridmesh.nnodes, 4))
        ugridmesh.trias = np.resize(ugridmesh.trias, (ugridmesh.ntrias, 5))
        ugridmesh.quads = np.resize(ugridmesh.quads, (ugridmesh.nquads, 6))
        ugridmesh.tetrs = np.resize(ugridmesh.tetrs, (ugridmesh.ntetrs, 5))
        ugridmesh.pyrms = np.resize(ugridmesh.pyrms, (ugridmesh.npyrms, 6))
        ugridmesh.prsms = np.resize(ugridmesh.prsms, (ugridmesh.nprsms, 7))
        ugridmesh.hexas = np.resize(ugridmesh.hexas, (ugridmesh.nhexas, 9))
        
        ielem = 1
        
        # Nodes
        for inode in range(ugridmesh.nnodes):
            ugridmesh.nodes[inode,0] = inode+1
            for i in range(1,4):
                ugridmesh.nodes[inode, i] = readfloat(fp, file_format) # x

        # Tris
        for itria in range(ugridmesh.ntrias):
            ugridmesh.trias[itria, 0] = ielem
            ielem += 1
            for inode in range(1,4):
                ugridmesh.trias[itria, inode] = readint(fp, file_format) # inode1
        
        # Quads
        for iquad in range(ugridmesh.nquads):
            ugridmesh.quads[iquad, 0] = ielem
            ielem += 1
            for inode in range(1,5):
                ugridmesh.quads[iquad, inode] = readint(fp, file_format) # inode1
        
        ## Surface IDs
        for itria in range(ugridmesh.ntrias):
            ugridmesh.trias[itria, -1] = readint(fp, file_format) # Surface ID
        for iquad in range(ugridmesh.nquads):
            ugridmesh.quads[iquad, -1] = readint(fp, file_format) # Surface ID
            
        
        surfs = np.unique(np.concatenate((ugridmesh.trias[:,-1], ugridmesh.quads[:,-1]), axis=None))
        print(Fore.GREEN + '%d Surfaces found.' % (len(surfs)))
        
        if only_surf:
            print(Fore.YELLOW + 'Reading in only surface mesh.')
            # Set the other values to zero
            ugridmesh.ntetrs = 0
            ugridmesh.npyrms = 0
            ugridmesh.nprsms = 0
            ugridmesh.nhexas = 0
            
            print(Fore.YELLOW + '  Removing extra nodes and renumbering.')
            ugridmesh = remove_orphans(ugridmesh)

        else:
            # Tets
            for itetr in range(ugridmesh.ntetrs):
                ugridmesh.tetrs[itetr, 0] = ielem
                ielem += 1
                for inode in range(1,5):
                    ugridmesh.tetrs[itetr, inode] = readint(fp, file_format) # inode1
            
            # Pent5s
            for ipyrm in range(ugridmesh.npyrms):
                ugridmesh.pyrms[ipyrm, 0] = ielem
                ielem += 1
                for inode in range(1,6):
                    ugridmesh.pyrms[ipyrm, inode] = readint(fp, file_format) # inode1
            
            # Pent6s
            for iprsm in range(ugridmesh.nprsms):
                ugridmesh.prsms[iprsm, 0] = ielem
                ielem += 1
                for inode in range(1,7):
                    ugridmesh.prsms[iprsm, inode] = readint(fp, file_format) # inode1

            # Hexes
            for ihexa in range(ugridmesh.nhexas):
                ugridmesh.hexes[ihexa, 0] = ielem
                ielem += 1
                for inode in range(1,9):
                    ugridmesh.hexes[ihexa, inode] = readint(fp, file_format)

    print(Fore.GREEN + 'Done reading %s' % filename)
    
    return ugridmesh
        
    

        
        
        
        
        
        
    