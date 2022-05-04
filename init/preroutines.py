"""
initial file generations
"""

import os
import csv
from datetime import datetime
from numpy import array
from geodesics.geo import geodesic, backward_raytrace
from initialconditions import space_light_timelike


def init_calculation(mass, quad_param, ort, gesch):
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%H-%M-%S-%f")

    seed_folder = "/home/altin/gr_py/data/" + f"data_{dt_string}"
    make_these_dirs(seed_folder)
    with open(seed_folder + "/inits/" + f"{dt_string}_repr.csv", "w") as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=["date", "qq", "init_ort", "init_vel", "mass"])
        csv_writer.writeheader()
        info = {
            "date": dt_string,
            "qq": quad_param,
            "init_ort": ort,
            "init_vel": gesch,
            "mass": mass
        }
        csv_writer.writerow(info)

    return seed_folder


def data_make(pos, vel, seed_folder, params, steps, forward_backward, delta):
    csv_loc = seed_folder + "/csvs_full/"
    aborted_loc = seed_folder + "/csvs_aborted/"

    now_obj = datetime.now()
    dt_string = now_obj.strftime("%d-%m-%H-%M-%S-%f")

    move_flag = prep_tr(pos, vel, params, steps, dt_string, forward_backward, csv_loc, aborted_loc, delta)

    return move_flag


def prep_tr(pos, vel, params, steps,  dt_string, forward_backward, csv_loc, aborted_loc, delta):
    u_t = space_light_timelike(pos, vel, params)
    vel_four = [u_t, vel[0], vel[1], vel[2]]
    move_flag = 1
    if forward_backward == "forward":
        move_flag = geodesic(dt_string, array(pos), array(vel_four), steps, params, csv_loc,
                             aborted_loc, delta)
    if forward_backward == "backward" or forward_backward == "shadow":
        move_flag = backward_raytrace(dt_string, array(pos), array(vel_four), steps, params, csv_loc,
                                      aborted_loc, delta)
    return move_flag


def make_these_dirs(seed_folder):
    os.mkdir(seed_folder)
    os.mkdir(seed_folder + "/inits")
    os.mkdir(seed_folder + "/csvs_full")
    os.mkdir(seed_folder + "/csvs_aborted")
    os.mkdir(seed_folder + "/figs")
