import numpy as np
import pyNastran
from pathlib import Path
from pyNastran.bdf.bdf import BDF
from pyNastran.op2.op2 import OP2
from pyNastran.op4.op4 import OP4

from src.utils.utils import runtime



#phi = np.column_stack(mode_shapes)



class preprocess_nastran():
    def __init__(self, program_input):

        ## I/O
        if not Path(program_input.nastran_bdf_path).exists():
            raise FileNotFoundError(f"Input BDF file not found: {program_input.nastran_bdf_path}")
        self.bdf_path = program_input.nastran_bdf_path

        if not Path(program_input.nastran_op2_path).exists():
            raise FileNotFoundError(f"Input BDF file not found: {program_input.nastran_op2_path}")
        self.op2_path = program_input.nastran_op2_path

        if not Path(program_input.nastran_op2_path).exists():
            raise FileNotFoundError(f"Input BDF file not found: {program_input.nastran_op2_path}")
        self.op2_path = program_input.nastran_op2_path


        ## Read
        with runtime("read bdf"):
            self.model = BDF()
            self.model.read_bdf(self.bdf_path)
            
        with runtime("read op2"):
            self.results = OP2()
            self.results.read_op2(self.op2_path) #, build_dataframe=True)

            """
            with runtime("read op4"):
                op4 = OP4()
                self.k_stiff = op4.read_op4(self.op4_path, matrix_names=['KGG'])
                self.m_mass = op4.read_op4(self.op4_path, matrix_names=['MGG'])
            """


        