

def solve_elastic_axis_isotropic_fin():

    """
    for every cross section
        find centroid x_c, z_c

        for each cquad4
            obtain area
            obtain centroid (x_i, z_i)

            EI_xx += E*t*Area*(z_i-z_c)^2
            EI_yy += E*t*Area*(x_i-x_c)^2
    """

    return 1 #RETURN A LIST OF POINTS THAT CAN BE INTERPOLATED BETWEEN


def solve_torsion_axis_isotropic_fin():

    return 1 #RETURN A LIST OF POINTS THAT CAN BE INTERPOLATED BETWEEN