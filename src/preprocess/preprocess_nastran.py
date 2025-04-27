import pyNastran as nas

from src.utils.time_feat_g_eazy_and_olivver_the_kid import runtime

class preprocess_nastran():
    def __init__(self, program_input):
        with runtime("read openfoam"):
            model = nas.read_bdf(program_input.bdf_filename)