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


        ## Attribute declaration

     
    def read_and_parse(self):

        ## Read
        with runtime("read bdf"):
            model = BDF()
            model.read_bdf(self.bdf_path)
            
        with runtime("read op2"):
            results = OP2()
            results.read_op2(self.op2_path) #, build_dataframe=True)

            """
            with runtime("read op4"):
                op4 = OP4()
                k_stiff = op4.read_op4(self.op4_path, matrix_names=['KGG'])
                m_mass = op4.read_op4(self.op4_path, matrix_names=['MGG'])
            """
        ## Parse
            """
            print(type(k_stiff))

            for key in k_stiff:
                print("key! ", key)

            print(k_stiff['KGG'].data)
            """

            eig1 = results.eigenvectors[1]
            
            modes = eig1.modes #modes
            nat_freq = eig1.mode_cycles #natural frequencies
            for m in modes:
                print("mode: ", m, nat_freq[m-1])

            print(results.get_op2_stats())


            #TODO: PRINT MODE SHAPES *****, also how to get elem norm vec???
            """
            all_subcases = list(results.eigenvectors.keys())
            isubcase = all_subcases[0]
            eig = results.eigenvectors[isubcase]
            print("mode shapes: \n")
            print(eig)
            """
            for eigenvectors in results:
                print(eigenvectors.shape[1])



        