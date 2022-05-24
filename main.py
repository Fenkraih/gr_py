import time
from shadows import plot_shadow
from numpy import pi, sqrt, array
from init import init_calculation, data_make
from plotting import plot_folder
from initialconditions import lin_comb


def main(mass, distance, quad_param, steps, grid_steps, delta):
    start = time.time()
    forward_backward = "backward"
    ort = [0, distance, pi/2, pi]                                                  # t r theta phi
    # angles = [60/180 * pi, 120/180 * pi , 120/360 * pi, 240/360 * pi]      # theta low, up same with phi, sample für himmels abrastern

    if forward_backward == "forward":
        angles = [pi/2, pi/2, 240/360 * 2 * pi, 300/360 * 2 * pi]                     # sample for phi raster mit const theta
    else:
        angles = [pi / 2, pi / 2, 50 / 360 * 2 * pi, 130 / 360 * 2 * pi]

    geschw, asoc_points_on_square = lin_comb(ort, quad_param, mass, angles, grid_steps)
    seed_folder = init_calculation(mass, quad_param, ort, geschw[0])
    light_or_dark = []

    for count, gesch in enumerate(geschw):
        print(f"{count} out of {len(geschw)}")
        move_flag = data_make(ort, gesch, seed_folder, [quad_param, mass], steps, forward_backward, delta)
        light_or_dark.append(move_flag)
    plot_folder(seed_folder, angles, ort, [quad_param, mass], distance,
                show_or_not=True, print_black_geodesics=True, d_plot=False)
    plot_shadow(asoc_points_on_square, light_or_dark, seed_folder)
    print(time.time() - start)

# TODO 1: . Teilchen fliegen sehr weit weg manchmal -> gtt exponential wachstum
#       untersuchen um diese auszusortieren  - fixed durch gut gewähltes koordinatensystem
# TODO 2:   koordinaten der initialen geschwindigkigkeitsvektoren fixen - fixed durch lokal minkowski wahl
# TODO 3: irgendwo ist ein mixup zwischen theta und phi Koordinaten bei den inital conditions -- fixed
# TODO 4: REPULSIVE GRAVITY BEI SCHWARZSCHILD ? GIBBET NICHT WAS IST HIER FALSCH


if __name__ == '__main__':
    # main(1, 50, 1, 600, 11, .5)   # angles = [pi/2, pi/2 , 120/360 * pi, 240/360 * pi]  # example
    main(1, 50, 0, 1000, 50, .1)
    #main(1, 50, 1, 2000, 1)
    #main(1, 50, 0.5, 2000, 1)
    #main(1, 50, 0.75, 2000, 1)
