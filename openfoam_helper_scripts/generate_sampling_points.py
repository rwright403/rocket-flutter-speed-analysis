import numpy as np
import pyvista as pv
import trimesh
from pyNastran.bdf.bdf import BDF

def parse_nas_bdf(bdf_filepath):
    """
    given the filepath to a nastran bdf use pynastran to read the .bdf and return a list of tuples of (x,z)
    
    """
    model = BDF()
    model.read_bdf(bdf_filepath)
    sample_pts_xz = []
    for nid,node in sorted(model.nodes.items()):
        sample_pts_xz.append( (node.xyz[0],node.xyz[2]) )

    return sample_pts_xz

def nudge_inside_bounds(x, z, bounds, epsilon=1e-9):
    """
    Nudges x and z inside the mesh bounds if they are slightly out.

    Args:
        x (float): x-coordinate to check.
        z (float): z-coordinate to check.
        bounds (np.ndarray): mesh.bounds array from trimesh (shape: (2, 3)).
        epsilon (float): small nudge distance.

    Returns:
        (float, float): nudged (x, z)
    """
    x_min, x_max = bounds[0][0], bounds[1][0]
    z_min, z_max = bounds[0][2], bounds[1][2]

    if x < x_min:
        x = x_min + epsilon
    elif x > x_max:
        x = x_max - epsilon

    if z < z_min:
        z = z_min + epsilon
    elif z > z_max:
        z = z_max - epsilon

    return x, z

def project_node_y_direction(mesh_path, nastran_nodes_xz):
    """
    Projects each (x, z) node along ±ŷ to intersect with STL geometry.

    Args:
        mesh_path (str): Path to fin surface STL file.
        nastran_nodes_xz (list of tuple): List of (x, z) nodes.
    
    Returns:
        List of (x, y, z) intersection points (top and bottom per node).
    """
    mesh = trimesh.load_mesh(mesh_path, process=True)


    

    #print("check if mesh is watertight: ", mesh.is_watertight)
    if mesh.is_watertight == False:
        raise ValueError(".STL mesh is not closed")
    #print(mesh.bounds)
    
    directions = [np.array([0, 1, 0]), np.array([0, -1, 0])]  # +y, -y
    sample_points = []

    for x, z in nastran_nodes_xz:
        x_0, z_0 = nudge_inside_bounds(x, z, mesh.bounds, epsilon=1e-9)
        origin = np.array([x_0, 0, z_0])  # start at y = 0
        for dir in directions:
            location, _, _ = mesh.ray.intersects_location(
                ray_origins=[origin],
                ray_directions=[dir]
            )
            if len(location) > 0:
                point = location[-1]
                sample_points.append(tuple(point))
                #print("found y val: ", tuple(point))
            else:
                #print(f"No hit for node ({x:.6f}, {z:.6f}) in direction {dir}")
                raise ValueError(f"No intersection found for node ({x}, {z}) in direction {dir}\n\nSometimes this occurs because of the floating point precision error between nastran small field .bdf files and .STL files. Maybe try exporting the structural model with large field formatting?")
    
    return sample_points


def write_sample_dict(points, output_path):
    """
    Writes a sampleDict file for OpenFOAM with hardcoded fields:
    Pressure (p), Density (rho), Speed of Sound (a), Velocity (U).

    Args:
        points (list of tuple): List of (x, y, z) probe points.
        output_path (str): Path to write the sampleDict file.
    """
    body = ""
    body += "interpolationScheme cellPointFace;\n"
    body += "setFormat raw;\n\n"

    # Sets block
    body += "functions\n{\n"
    body += "    sample\n"
    body += "    {\n"
    body += "        type probes;\n"
    body += "        libs (\"libsampling.so\");\n"
    body += "        interpolationScheme cellPointFace;\n"
    body += "        setFormat raw;\n\n"
    body += "        probeLocations\n"
    body += "        (\n"
    for pt in points:
        body += f"            ({pt[0]} {pt[1]} {pt[2]})\n"
    body += "        );\n"
    body += "        fields\n"
    body += "        (\n"
    body += "            p\n"
    body += "            rho\n"
    body += "            a\n"
    body += "            U\n"
    body += "        );\n"
    body += "    }\n"
    body += "};\n\n"

    # Write to file
    with open(output_path, "w") as f:
        f.write(body)

    print(f"sampleDict written to: {output_path}")



###program start:
#for my ref - remember to cd to this dir
bdf_filepath = r"_80-tc1-coarse.bdf"
stl_filepath = r"_80-tc1-no-le-chamfer.STL"
sample_dict_filename = "sampleDict"

sample_pts_xz = parse_nas_bdf(bdf_filepath)
sample_pts = project_node_y_direction(stl_filepath, sample_pts_xz)
write_sample_dict(sample_pts, sample_dict_filename)


"""debug code to visualize points from project_node_y_direction"""

"""for i in sample_pts_xz:
    print(i)"""
