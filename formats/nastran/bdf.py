'''
Created on Jun 19, 2018

@author: eszwabowski
'''

from colorama import Fore, init
import numpy as np

init(autoreset=True)

from geom import meshtools

def write(mesh, filename):
    # --- Exports mesh object to a bdf
    
    print('Writing: %s' % filename)
    
    with open(filename, 'w') as fp:
        writeheader(fp)
        
        # The nodes
        for inode in range(mesh.nnodes):
            writegrid(mesh.nodes[inode,:], fp)
            
        # The tris
        for itria in range(mesh.ntrias):
            writectria3(mesh.trias[itria,:], fp)
            
        # The quads
        for iquad in range(mesh.nquads):
            writecquad4(mesh.quads[iquad,:], fp)
            
        # The tets
        for itetr in range(mesh.ntetrs):
            writectetra(mesh.tetrs[itetr,:], fp)
            
        # The pyramids
        for ipyrm in range(mesh.npyrms):
            writecpyram(mesh.pyrms[ipyrm,:], fp)
            
        # The prisms
        for iprsm in range(mesh.nprsms):
            writecpenta(mesh.prsms[iprsm,:], fp)
            
        # The hexes
        for ihexas in range(mesh.nhexas):
            writechexa(mesh.hexas[ihexas,:], fp)
            
        for surf in np.unique(np.concatenate((mesh.trias[:,-1], mesh.quads[:,-1]), axis=None)):
            writepshell(surf, fp)
        writepsolid(fp)
        writemat1(fp)
    
    return

def read(nastran_mesh_file):
    nids = []
    nodes = []
    trias = []
    quads = []
    
    print(Fore.GREEN + 'Reading %s...' % nastran_mesh_file) 
    
    with open(nastran_mesh_file, 'r') as fp:
        lines = fp.readlines()
        
    for line in lines:
        fields = line.split(',')
        
        if 'GRID' in fields[0]:
            nid = int(fields[1])
            x = float(fields[3])
            y = float(fields[4])
            z = float(fields[5])
            
            nids.append(nid)
            nodes.append([nid, x, y, z])
        elif 'CTRIA3' in fields[0]:
            eid = int(fields[1])
            nd1 = int(fields[3])
            nd2 = int(fields[4])
            nd3 = int(fields[5])
            
            sid = int(fields[2])
            
            trias.append([eid, nd1, nd2, nd3, sid])
            #surfs.append(sid)
        elif 'CQUAD4' in fields[0]:
            eid = int(fields[1])
            nd1 = int(fields[3])
            nd2 = int(fields[4])
            nd3 = int(fields[5])
            nd4 = int(fields[6])
            
            sid = int(fields[2])
            
            quads.append([eid, nd1, nd2, nd3, nd4, sid])
            #surfs.append(sid)
            
    # Put the data into the mesh class
    bdfmesh = meshtools.meshclass()
    
    bdfmesh.nnodes = len(nodes)
    bdfmesh.ntrias = len(trias)
    bdfmesh.nquads = len(quads)
    
    bdfmesh.nodes = np.array(nodes)
    bdfmesh.trias = np.array(trias)
    bdfmesh.quads = np.array(quads)
    # bdfmesh.surfs = np.array(surfs)


    print(Fore.GREEN + '  Nodes:    %d' % (bdfmesh.nnodes))
    print(Fore.GREEN + '  Tris:     %d' % (bdfmesh.ntrias))
    print(Fore.GREEN + '  Quads:    %d' % (bdfmesh.nquads))
    print(Fore.GREEN + '  Tets:     %d' % (bdfmesh.ntetrs))
    print(Fore.GREEN + '  Pyramids: %d' % (bdfmesh.npyrms))
    print(Fore.GREEN + '  Prisms:   %d' % (bdfmesh.nprsms))
    print(Fore.GREEN + '  Hexes:    %d' % (bdfmesh.nhexas))
    print(Fore.GREEN + 'Done reading %s' % nastran_mesh_file)
    return bdfmesh

def writegrid(node, fp):
    fp.write('%-6s,%7d, ,%7f,%7f,%7f\n' % ('GRID', node[0], node[1], node[2], node[3]))
    return

def writectria3(tria, fp):
    fp.write('%-6s,%7d,%3d,%7d,%7d,%7d\n' % ('CTRIA3', tria[0], tria[4], tria[1], tria[2], tria[3]))
    return

def writecquad4(quad, fp):
    fp.write('%-6s,%7d,%3d,%7d,%7d,%7d,%7d\n' % ('CQUAD4', quad[0], quad[5], quad[1], quad[2], quad[3], quad[4]))
    return

def writectetra(tetr, fp):
    fp.write('%-6s,%7d,99,%7d,%7d,%7d,%7d\n' % ('CTETRA', tetr[0], tetr[1], tetr[2], tetr[3], tetr[4]))
    return

def writecpyram(pyrm, fp):
    fp.write('%-6s,%7d,99,%7d,%7d,%7d,%7d,%7d\n' % ('CPYRAM', pyrm[0], pyrm[1], pyrm[2], pyrm[3], pyrm[4], pyrm[5]))
    return

def writecpenta(prsm, fp):
    fp.write('%-6s,%7d,99,%7d,%7d,%7d,%7d,%7d,%7d\n' % ('CPENTA', prsm[0], prsm[1], prsm[2], prsm[3], prsm[4], prsm[5], prsm[6]))
    return

def writechexa(hexa, fp):
    fp.write('%-6s,%7d,99,%7d,%7d,%7d,%7d,%7d,%7d,%7d,%7d\n' % ('CHEXA', hexa[0], hexa[1], hexa[2], hexa[3], hexa[4], hexa[5], hexa[6], hexa[7], hexa[8]))
    return

def writepshell(surfid, fp):      #PSHELL   PID MID CORDM
    fp.write('%-6s,%3d,%3d,%3g\n' % ('PSHELL', surfid,  1,  1.5))
    return

def writemat1(fp):                          #MAT1   MID    E  NU  RHO     A       TREF GE
    fp.write('%-6s,%3d,%7g, ,%7g,%7g,%7g,%7g,%7g\n' % ('MAT1', 1, 3.5e7, .3, 1.2225, 6.53-6, 273.5, .2))
    return

def writepsolid(fp):              #PSOLID   PID MID CORDM
    fp.write('%-6s,%3d,%3d,%3d\n' % ('PSOLID', 99,  1,  0))
    return

def writepload2(fp, p, eid):
    fp.write('%-6s,%7d,%7f,%7d\n' % ('PLOAD2', 1, p, eid))
    return

def writepload4(fp, p, eid):
    fp.write('%-6s,%7d,%7d,%7f,%7f,%7f,%7f\n' % ('PLOAD4', 1, eid, p[0], p[1], p[2], p[3]))
    return

def writeheader(fp):
    fp.write('CEND\n')
    fp.write('BEGIN BULK\n')
    return
