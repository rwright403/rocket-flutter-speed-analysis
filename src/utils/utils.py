import time
from contextlib import contextmanager
import numpy as np
from scipy.sparse import csr_matrix
import re

def _print_stars():
    print("\n" + "*" * 20 + "\n")

def _print_figma():
    print("\n         			                _______\n	UVic Rocketry Fin Flutter Solver       /       \~\n      				   	      /         \~\n_____________________________________________/           \~\n")


""" 
runtime
Record and print the runtime of a section of code
"""
@contextmanager
def runtime(name="Block"):
    print(f"[{name} - starting]")
    start = time.time()
    yield
    end = time.time()
    print(f"[{name}] - finished, elapsed {end - start:.3f} seconds")



def get_fin_const_thickness(model):
    """
    Extract the total thickness of the fin (assumed constant)
    from the first CQUAD4 element in a pyNastran BDF model.

    Parameters
    ----------
    model : pyNastran.bdf.bdf.BDF
        Parsed NASTRAN model.

    Returns
    -------
    thickness : float
        Total thickness of the fin.
    """
    for eid, elem in model.elements.items():
        if elem.type == 'CQUAD4':
            prop = model.properties[elem.Pid()]
            if prop.type == 'PSHELL':
                return float(prop.t)
            elif prop.type == 'PCOMP':
                return float(sum(ply.t for ply in prop.plies))
            else:
                raise ValueError(f"Unsupported property type {prop.type} for element {eid}")




"""
given a string of the desired datastructure and the filepath to a sparse full.mat file, read it into python 
return:
    the matrices as a scipy .csr matrix 
    or
    the DOF map as a dict
"""
def read_and_parse_full_matrix(mat_str, filepath):
    
    with open(filepath, 'r') as f:
        lines = f.readlines()

    # Find the start of the desired matrix block
    row_idx = None
    for idx, line in enumerate(lines):
        if line.strip().startswith(mat_str):
            row_idx = idx
            break

    print(f"\nthe row found is {row_idx}\n")

    # Parse header line
    header = lines[row_idx].split()

    data = []
    data_row_idx = []
    data_col_idx = []

    shape = ( int(header[4]), int(header[5]) )

    if mat_str != 'DOFS':
        if int(header[3]) == 1:
            raise NotImplementedError(
                "Dense Matrix read/process not implemented yet, add 'OUTPUT,MATRIX,FULL,SPARSE' to hypermesh .fem file before case ctrl."
            )
    
    row_idx += 1

    if mat_str == 'DOFS':
        
        # Parse the index row
        index_parts = list(map(int, lines[row_idx].strip().split()))
        num_dofs = index_parts[2]

        node_ids = []
        while len(node_ids) <= num_dofs:
            node_ids.extend(map(int, lines[row_idx].strip().split()))
            row_idx+=1

        row_idx+=1

        dofs = []
        while len(dofs) <= num_dofs:
            dofs.extend(map(int, lines[row_idx].strip().split()))
            row_idx+=1 # this looks like bad code and it probably is but dont change the algo w/out looking at the DOFS format

        # Convert to numpy array: first row node_ids, second row dofs
        grid_to_dof_mapping_mat = np.array([node_ids[:num_dofs], dofs[:num_dofs]])

        return grid_to_dof_mapping_mat


        """
        below is the regular case for a global matrix. Above is for the DOF MAP
        """
    else:
        # Parse sparse global matrix (STIFFNESS, MASS, etc.)
        while not lines[row_idx].strip().startswith("0"):
            # Parse the index row: col, row_start, row_end
            index_parts = list(map(int, lines[row_idx].strip().split()))
            col = index_parts[0] - 1       # convert to 0-based
            row_start = index_parts[1] - 1
            row_end   = index_parts[2] - 1
            n = row_end - row_start + 1
            row_idx += 1

            # Collect n values (may span multiple lines)
            values = []
            while len(values) < n:
                vals = re.findall(r'[+-]?\d+\.\d+(?:[Ee][+-]?\d+)?', lines[row_idx])
                values.extend(map(float, vals))
                row_idx += 1

            # Assign entries to sparse COO storage
            for i, val in enumerate(values[:n]):
                data_row_idx.append(row_start + i)
                data_col_idx.append(col)
                data.append(val)

        return csr_matrix((data, (np.array(data_row_idx), np.array(data_col_idx))), shape=shape)


import numpy as np

def reduce_phi(phi_full, grid_to_dof_mapping_mat, all_grid_ids=None):
    """
    Reduce eigenvectors to match the active DOFs in .full.mat.

    Parameters
    ----------
    phi_full : ndarray (n_full_dofs, n_modes)
        Eigenvectors from solver, including constrained DOFs (zeros).
    grid_to_dof_mapping_mat : ndarray (2, n_active_dofs)
        Parsed from DOFS block. Row 0 = GRID IDs, Row 1 = DOF IDs (1–6).
    all_grid_ids : list or ndarray, optional
        List of grid IDs in the order they appear in phi_full.
        If None, assumes phi_full is ordered as [sorted unique IDs].

    Returns
    -------
    phi_reduced : ndarray (n_active_dofs, n_modes)
        Reduced eigenvectors aligned with KGG/MGG.
    """
    grid_ids = grid_to_dof_mapping_mat[0, :]
    dof_ids  = grid_to_dof_mapping_mat[1, :]

    # If not provided, assume phi_full rows are ordered by sorted node IDs
    if all_grid_ids is None:
        # Guess ordering from unique grid IDs present in mapping
        all_grid_ids = np.unique(grid_ids)

    # Build lookup: (grid, dof_id) -> row index in phi_full
    node_dof_order = {}
    for i, gid in enumerate(all_grid_ids):
        base = i * 6
        for dof_id in range(1, 7):  # 1=Tx,2=Ty,3=Tz,4=Rx,5=Ry,6=Rz
            node_dof_order[(gid, dof_id)] = base + (dof_id - 1)

    # Collect row indices to keep
    keep_idx = [node_dof_order[(gid, did)] for gid, did in zip(grid_ids, dof_ids)]

    return phi_full[keep_idx, :]


"""def redimensionalize(A_star, B_star, rho, V, c_ref, S_ref):
    q_inf = 0.5 * rho * V**2

    # copy to avoid modifying in place
    A = A_star.copy()
    B = B_star.copy()

    # Force rows (0:3) → multiply by q_inf * S
    A[0:3, :] *= q_inf * S_ref
    B[0:3, :] *= q_inf * S_ref

    # Moment rows (3:6) → multiply by q_inf * S * c_ref
    A[3:6, :] *= q_inf * S_ref * c_ref
    B[3:6, :] *= q_inf * S_ref * c_ref

    return A, B"""
