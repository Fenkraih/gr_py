import time
from shadows import plot_shadow
from numpy import pi, sqrt, array, arcsin
from init import init_calculation, data_make
from plotting import plot_folder, multi_plot
from initialconditions import lin_comb, eq_plane_grid, angle_calc, shadow_angle_calc


def main(mass, distance, quad_param, steps, grid_steps, delta, angles=None, forward_backward="backward"):
    start = time.time()
    ort = [0, distance, pi / 2, pi]  # t r theta phi
    lower_phi_angle, higher_phi_angle, angle_steps = angle_calc(mass, quad_param, distance)
    if angles is None:
        angles = [pi / 2, pi / 2,
                  lower_phi_angle * 2 * pi / 360, (lower_phi_angle + grid_steps * angle_steps) * 2 * pi / 360]
    geschw, asoc_points_on_square = lin_comb(ort, quad_param, mass, angles, grid_steps)
    seed_folder = init_calculation(mass, quad_param, ort, geschw[0])
    light_or_dark = []
    doomtimer = 0
    upper_angle = lower_phi_angle
    for count, gesch in enumerate(geschw):
        print(f"{count} out of {len(geschw)}")
        move_flag = data_make(ort, gesch, seed_folder, [quad_param, mass], steps, forward_backward, delta)
        light_or_dark.append(move_flag)
        upper_angle += angle_steps
        if move_flag == 0:
            doomtimer += 1
        if doomtimer == 2:
            break
    shadow_angle = shadow_angle_calc(lower_phi_angle, light_or_dark, angle_steps)

    plot_folder(seed_folder, angles, ort, [quad_param, mass], distance,
                show_or_not=True, print_black_geodesics=True, d_plot=False, zoom_plot=True)
    plot_shadow(asoc_points_on_square, light_or_dark, seed_folder)
    print(time.time() - start)


def q_compare(mass, distance, quad_list, steps, grid_steps, delta, angles=None, forward_backward="backward"):
    start = time.time()
    ort = [0, distance, pi / 2, pi]  # t r theta phi
    parent_folders = []
    shadow_angles_list = []
    for quad_param in quad_list:
        lower_phi_angle, high_phi_angle, angle_steps = angle_calc(mass, quad_param, distance, grid_steps)
        angles = [pi / 2, pi / 2,
                  lower_phi_angle * 2 * pi / 360, high_phi_angle * 2 * pi / 360]
        geschw, asoc_points_on_square = lin_comb(ort, quad_param, mass, angles, grid_steps)
        seed_folder = init_calculation(mass, quad_param, ort, geschw[0])
        parent_folders.append(seed_folder)
        light_or_dark = []
        doomtimer = 0
        upper_angle = lower_phi_angle
        for count, gesch in enumerate(geschw):
            print(f"{count + 1} out of {len(geschw)}")
            move_flag = data_make(ort, gesch, seed_folder, [quad_param, mass], steps, forward_backward, delta)
            light_or_dark.append(move_flag)
            upper_angle += angle_steps
            if move_flag == 0:
                doomtimer += 1
            if doomtimer == 2:
                break
        shadow_angle = shadow_angle_calc(lower_phi_angle, light_or_dark, angle_steps)
        shadow_angles_list.append(shadow_angle)

    multi_plot(parent_folders, quad_list, shadow_angles_list)

    print(time.time() - start)


# TODO 1: . Teilchen fliegen sehr weit weg manchmal -> gtt exponential wachstum
#       untersuchen um diese auszusortieren  - fixed durch gut gewähltes koordinatensystem
# TODO 2:   koordinaten der initialen geschwindigkigkeitsvektoren fixen - fixed durch lokal minkowski wahl
# TODO 3: irgendwo ist ein mixup zwischen theta und phi Koordinaten bei den inital conditions -- fixed
# TODO 4: REPULSIVE GRAVITY BEI SCHWARZSCHILD ? GIBBET NICHT WAS IST HIER FALSCH
#  - fixed RK4 war SCHULD wieso ? Gute Frage
# TODO 5: DREHER IM KOORDINATEN SYSTEM: FUNKTIONIERT BISHER NUR RICHTIG WENN AX UND AY VERTAUSCHT SIND


if __name__ == '__main__':
    # main(1, 50, 1, 600, 11, .5)   # angles = [pi/2, pi/2 , 120/360 * pi, 240/360 * pi]  # example
    # main(1, 50, -0.3, 25000, 100, .005)
    q_compare(1, 50, [1, 0.5, 0, -0.25], 100000, 30, .001)
