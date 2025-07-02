import numpy as np
import trimesh

# I love SolidWorks!
def shift_stl_in_y(filepath, abs_val_magnitude_to_shift, output_file="out.STL"):
    # Load STL with no processing
    mesh = trimesh.load_mesh(filepath, process=False)

    # Force vertices to double precision
    mesh.vertices = mesh.vertices.astype(np.float64)

    # Apply precise Y translation
    shift_vec = np.array([0.0, -abs_val_magnitude_to_shift, 0.0], dtype=np.float64)
    mesh.apply_translation(shift_vec)

    # Export as binary STL (more precise than ASCII)
    mesh.export(output_file, file_type='stl')  # binary by default

    print(f"Mesh from {filepath} shifted -{abs_val_magnitude_to_shift} units in Y and saved to {output_file}!")


### NOTE: don't forget to cd into this dir!
stl_filepath = r"_80-tc1-no-le-chamfer.STL"
shift_stl_in_y(stl_filepath, 0.001000000000)