from geom import meshtools
from geom import edge
import matplotlib.pyplot as plt
import numpy as np

def test():
    ds = 0.4
    npts = 9

    edges = []
    nodes = []
    nodes.append(np.array([0.0, 0.0, 0.0]))
    nodes.append(np.array([1.0, 0.0, 0.0]))
    nodes.append(np.array([2.0, 0.0, 0.0]))
    nodes.append(np.array([3.0, 0.0, 0.0]))
    nodes.append(np.array([4.0, 0.0, 0.0]))
    nodes.append(np.array([4.0, 1.0, 0.0]))
    nodes.append(np.array([4.0, 2.0, 0.0]))
    nodes.append(np.array([4.0, 3.0, 0.0]))
    nodes.append(np.array([4.0, 4.0, 0.0]))
    nodes.append(np.array([3.0, 4.0, 0.0]))
    nodes.append(np.array([2.0, 4.0, 0.0]))
    nodes.append(np.array([1.0, 4.0, 0.0]))
    nodes.append(np.array([0.0, 4.0, 0.0]))
    nodes.append(np.array([0.0, 3.0, 0.0]))
    nodes.append(np.array([0.0, 2.0, 0.0]))
    nodes.append(np.array([0.0, 1.0, 0.0]))

    edges.append(edge.edgeclass(1, nodes[0], 2,  nodes[1],  -1))
    edges.append(edge.edgeclass(2, nodes[1], 3,  nodes[2],  -1))
    edges.append(edge.edgeclass(3, nodes[2], 4,  nodes[3],  -1))
    edges.append(edge.edgeclass(4, nodes[3], 5,  nodes[4],  -1))
    edges.append(edge.edgeclass(5, nodes[4], 6,  nodes[5],  -1))
    edges.append(edge.edgeclass(6, nodes[5], 7,  nodes[6],  -1))
    edges.append(edge.edgeclass(7, nodes[6], 8,  nodes[7],  -1))
    edges.append(edge.edgeclass(8, nodes[7], 9,  nodes[8],  -1))
    edges.append(edge.edgeclass(9, nodes[8], 10, nodes[9],  -1))
    edges.append(edge.edgeclass(10,nodes[9], 11, nodes[10], -1))
    edges.append(edge.edgeclass(11,nodes[10],12, nodes[11], -1))
    edges.append(edge.edgeclass(12,nodes[11],13, nodes[12], -1))
    edges.append(edge.edgeclass(13,nodes[12],14, nodes[13], -1))
    edges.append(edge.edgeclass(14,nodes[13],15, nodes[14], -1))
    edges.append(edge.edgeclass(15,nodes[14],16, nodes[15], -1))
    edges.append(edge.edgeclass(16,nodes[15], 1, nodes[0],  -1))

    fig = plt.figure()
    for i, iedge in enumerate(edges):
        iedge.plot2d(fig)

        normal = 0.5*(iedge.normal + edges[i-1].normal)

        for ipt in range(npts):
            newpt = normal*ds*1.2**(ipt) + iedge.node1
            plt.plot(newpt[0], newpt[1], 'o')

    

    plt.show()
    return

if __name__ == "__main__":
        test()

