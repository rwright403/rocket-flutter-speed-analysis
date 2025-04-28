from pyNastran.bdf.bdf import BDF
from pyNastran.op2.op2 import OP2
from pyNastran.op4.op4 import OP4, read_op4

from src.utils.time_feat_g_eazy_and_olivver_the_kid import runtime

class preprocess_nastran():
    def __init__(self, program_input):

        with runtime("read bdf"):
            model = BDF()
            model.read_bdf(program_input.nastran_bdf_path)
            
        with runtime("read op2"):
            results = OP2()
            results.read_op2(program_input.nastran_op2_path)
            print(results.get_op2_stats())

            print("everything printed is the value! ", results.eigenvectors[1])

    """
        with runtime("read op4"):
            k_stiff = read_op4(program_input.nastran_op4_path, matrix_names=['K'])
            m_mass = read_op4(program_input.nastran_op4_path, matrix_names=['M'])
    """