"""
Core geodesic calculation routine using RK4 forward calculation
"""
import os
import pandas as pd
from rk4.methods import runge_kutta_4_forward, runge_kutta_4_backward, euler_backward, euler_forward


def geodesic(dt_string, position, velocity, steps, params, csv_loc, aborted_loc, delta):
    """

    :param dt_string:
    :param position:
    :param velocity:
    :param steps:
    :param params:
    :param csv_loc:
    :param aborted_loc:
    :return:
    """
    quad_param, mass = params
    filename = csv_loc + f"{dt_string}.csv"
    file_replace = aborted_loc + f"{dt_string}.csv"
    # trajectory, move_flag = runge_kutta_4_forward(velocity, position, steps, params, delta)
    trajectory, move_flag = euler_forward(velocity, position, steps, params, delta)
    df = pd.DataFrame(data=trajectory)
    df.to_csv(filename, index=False)
    if move_flag == 0:
        os.replace(filename, file_replace)
    return move_flag


def backward_raytrace(dt_string, position, velocity, steps, params, csv_loc, aborted_loc, delta):
    """

    :param velocity:
    :param position:
    :param dt_string:
    :param steps:
    :param params:
    :param csv_loc:
    :param aborted_loc:
    :return:
    """
    quad_param, mass = params
    filename = csv_loc + f"{dt_string}.csv"
    file_replace = aborted_loc + f"{dt_string}.csv"
    # trajectory, move_flag = runge_kutta_4_backward(velocity, position, steps, params, delta)
    trajectory, move_flag = euler_backward(velocity, position, steps, params, delta)
    df = pd.DataFrame(data=trajectory)
    df.to_csv(filename, index=False)
    if move_flag == 0:
        os.replace(filename, file_replace)
    return move_flag


if __name__ == '__main__':
    geodesic()
