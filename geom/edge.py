import numpy as np
import matplotlib.pyplot as plt

#----------------------------------------------------------------------
#
#    Untructured Mesh Class for 3D mesh
#
#----------------------------------------------------------------------
class edgeclass(object):
    def __init__(self, nid1, node1, nid2, node2, right_face=None, left_face=None):

        if right_face is None:
            self.right_face = 0
        else:
            self.right_face = right_face

        if left_face is None:
            self.left_face = 0
        else:
            self.left_face = left_face

        self.node1 = node1
        self.node2 = node2

        edge_vector = np.array([(node2[i] - node1[i]) for i in range(3)])
        self.edge_length = np.linalg.norm(edge_vector)
        self.edge = edge_vector / self.edge_length

        khat = np.array([0.0, 0.0, 1.0])
        self.normal = np.cross(khat, self.edge)

        return

    def my_nodes(self):
        return nid1, nid2

    def is_member(self, nid):
        if (nid == nid1):
            return True
        elif (nid  == nid2):
            return True
        else:
            return False

    def is_boundary(self):
        if (right_face == -1):
            return True
        else:
            return False

    def is_front(self):
        if (left_face == 0):
            return True
        else:
            return False

    def plot2d(self, fig):
        plt.figure(fig.number)
        plt.plot([self.node1[0], self.node2[0]],  [self.node1[1], self.node2[1]], 'x-')
#----------------------------------------------------------------------



