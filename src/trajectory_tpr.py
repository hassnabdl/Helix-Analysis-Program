from parse import parse
from tpr import tpr
from dssp import *
from axis import principal_axis


def trajectory_tpr(trajectory_file):
    """
    Get tpr list for each frame

    ---
    Parameters:
    trajectory_file: concatenation of pdb files

    ---
    Return:
    list_thetas: list of lists of tprs. 
    Each sub-list corresponds to a frame and each item of the sub-list to a helix

    """

    backbones = parse(trajectory_file)
    list_thetas = []
    for i, backbone in enumerate(backbones):
        dssp = DSSP(backbone)
        list_helices = dssp.get_ca()
        ithetas = []
        for helix in list_helices:
            orig, axis = principal_axis(helix)
            theta = tpr(helix, axis, orig)
            thetas.append(theta)
        list_thetas.append(thetas)
    return list_thetas


def test_traj_tpr(filename):
    import math
    list_thetas = trajectory_tpr(filename)
    print(list_thetas[0][1]*180/math.pi)
    print(list_thetas[1][1]*180/math.pi)
    print(list_thetas[2][1]*180/math.pi)
    print(list_thetas[3][1]*180/math.pi)
    print(list_thetas[4][1]*180/math.pi)
    print(list_thetas[5][1]*180/math.pi)


# test_traj_tpr("TSPO_traj.pdb")
