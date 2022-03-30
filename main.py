import time
from shadows import plot_shadow
from numpy import pi, sqrt, array
from init import init_calculation, data_make
from plotting import plot_folder
from initialconditions import square_to_polar_grid


def main():
    start = time.time()
    mass = 1
    distance = 35
    width = 4
    quad_param = 1
    steps = 200
    delta = 1
    karth_quadrat, sph_kugel, karth_kugel = square_to_polar_grid(10)
    geschw = karth_kugel
    forward_backward = "backward"
    ort = [0, distance, pi/2, pi]                                                  # t r theta phi
    seed_folder = init_calculation(mass, quad_param, ort, geschw[0])
    light_or_dark = []
    for count, gesch in enumerate( geschw):
        print(f"{count} out of {len(geschw)}")
        move_flag = data_make(ort, gesch, seed_folder, [quad_param, mass], steps, forward_backward, delta)
        light_or_dark.append(move_flag)
    plot_folder(seed_folder, [quad_param, mass], distance, show_or_not=True)
    plot_shadow(karth_quadrat, light_or_dark, seed_folder)
    print(time.time() - start)





if __name__ == '__main__':
    main()