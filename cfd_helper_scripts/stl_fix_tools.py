import numpy as np
import trimesh

# I love SolidWorks!
def shift_stl(filepath, x_shift, y_shift, z_shift, output_file):
    # Load STL with no processing
    mesh = trimesh.load_mesh(filepath, process=False)

    # Force vertices to double precision
    mesh.vertices = mesh.vertices.astype(np.float64)

    # Apply precise Y translation
    shift_vec = np.array([x_shift, y_shift, z_shift], dtype=np.float64)
    mesh.apply_translation(shift_vec)

    # Export as binary STL (more precise than ASCII)
    mesh.export(output_file, file_type='stl')  # binary by default

    print(f"Mesh from {filepath} shifted x={x_shift}, y={y_shift}, z={z_shift}, units and saved to {output_file}!")


def scale_stl(filepath, multiplied_scale_factor, output_file):
    # Load STL without automatic processing
    mesh = trimesh.load_mesh(filepath, process=False)

    # Ensure vertices are double precision for accuracy
    mesh.vertices = mesh.vertices.astype(np.float64)

    # Apply uniform scale factor to all coordinates
    mesh.vertices *= multiplied_scale_factor

    # Export the scaled mesh to a new STL file
    mesh.export(output_file)


### NOTE: don't forget to cd into this dir!
original_stl_filepath = r"a2-a000-cfddomain.STL"
scaled_stl_filepath = "tmp-scaled.STL"
shifted_stl_filepath = "A2-final-processed-stl.STL"

scale_stl(original_stl_filepath, (1/1000), scaled_stl_filepath)
shift_stl(scaled_stl_filepath, 3, (-201.4891/1000), (-254.6285 /1000), shifted_stl_filepath)