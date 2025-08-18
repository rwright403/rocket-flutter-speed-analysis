import numpy as np
from collections import Counter

class iso_fin_structural_axis:
    """
    Assumptions:
    - isotropic material
    - each cross section is rectangular - neglecting machined taper
    - bending axis is the vector between the inbd le and the trailing le
    - torision axis is between the root centroid to the tip centroid
    
    """
    def __init__(self, cquad4_panels):

        ### need the corner nodes. Know the corner nodes of the fin will only have 2 connected nodes and the others will have 3-4.
        all_node_ids = []
        node_positions = {}

        for panel in cquad4_panels:
            for nid, node in panel.nodes.items():
                all_node_ids.append(nid)
                node_positions[nid] = node.r_  # store the 3D position

        # count number of times each node is connected to a cquad4 panel --> the corner nodes will only appear in one cquad4 panel 
        node_counts = Counter(all_node_ids)
        corner_node_ids = [nid for nid, count in node_counts.items() if count == 1]
        corner_node_positions = np.array([node_positions[nid] for nid in corner_node_ids])

        # now we need to sort the corners:
        # inbd leading edge coords will have smallest vector magnitude
        self.inbd_le = min(corner_node_positions.values(), key=lambda p: np.linalg.norm(p))

        # outbd leading edge: smallest x out of remaining 3
        remaining = [p for p in corner_node_positions.values() if not np.allclose(p, self.inbd_le)]
        outbd_le = min(remaining, key=lambda p: p[0])

        # Trailing edge inboard: smallest z out of remaining 3
        remaining = [p for p in remaining if not np.allclose(p, outbd_le)]
        inbd_te = min(remaining, key=lambda p: p[2])

        # Trailing edge outboard: leftover
        outbd_te = [p for p in remaining if not np.allclose(p, inbd_te)][0]

        #find centroids of outbd and inbd (assuming const thickness rectangles)
        self.r_inbd_centroid = 0.5 * (self.inbd_le + inbd_te)
        self.r_outbd_centroid = 0.5 * (outbd_le + outbd_te)

        self.torision_axis = self.r_inbd_centroid - self.r_outbd_centroid

        self.bending_axis = self.inbd_te - self.outbd_le

    def bending_arm(self, pt):
        #Project point P onto bending axis to get param line eqn and thus location along axis, then sol and return bending moment arm
        t = np.dot( (pt - self.inbd_le), self.bending_axis ) / np.dot(self.bending_axis, self.bending_axis)
        return np.array(pt) - (self.inbd_le + t * self.bending_axis)

    def torision_arm(self, pt):
        #Project point P onto torision axis to get param line eqn and thus location along axis, then sol and return torision moment arm
        t = np.dot( (pt - self.r_inbd_centroid), self.torision_axis) / np.dot(self.torision_axis, self.torision_axis)
        return np.array(pt) - (self.r_inbd_centroid + t * self.torision_axis)
