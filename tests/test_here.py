import time
from numpy import pi
from init import init_calculation, data_make
from plotting import plot_folder


def test_trajectory():
    """
    If integrator works this shows a ring around the object with radius (3+2q)*m
    :return:
    """
    start = time.time()
    mass = 1
    distance = 3
    quad_param = 0
    steps = 300
    gesch = [0, 0, 0.1]                       # u_r, u_theta, u_phi
    geschw =[gesch]
    forward_backward = "forward"
    ort = [0, distance, pi/2, 0]                                                  # t r theta phi
    seed_folder = init_calculation(mass, quad_param, ort, gesch)
    light_or_dark = []
    for gesch in geschw:
        move_flag = data_make(ort, gesch, seed_folder, [quad_param, mass], steps, forward_backward)
        light_or_dark.append(move_flag)
    plot_folder(seed_folder, [quad_param, mass], distance)
    print(time.time() - start)

def test_raytrace():
    """
    If this test is passed this should produce a clockwise moving particle around the central object. This is a test
    to determine if the backwards method is really going backwards
    :return:
    """
    start = time.time()
    mass = 1
    distance = 3
    quad_param = 0
    steps = 300
    gesch = [0, 0, 0.01]                       # u_r, u_theta, u_phi
    geschw =[gesch]
    forward_backward = "backward"
    ort = [0, distance, pi/2, 0]                                                  # t r theta phi
    seed_folder = init_calculation(mass, quad_param, ort, gesch)
    light_or_dark = []
    for gesch in geschw:
        move_flag = data_make(ort, gesch, seed_folder, [quad_param, mass], steps, forward_backward)
        light_or_dark.append(move_flag)
    plot_folder(seed_folder, [quad_param, mass], distance, show_or_not=False)
    print(time.time() - start)