import time
from shadows import plot_shadow
from numpy import pi, sqrt, array, arcsin
from init import init_calculation, data_make
from plotting import plot_folder
from initialconditions import lin_comb, eq_plane_grid, angle_calc


def main(mass, distance, quad_param, steps, grid_steps, delta, angles=None):
    start = time.time()
    forward_backward = "backward"
    ort = [0, distance, pi/2, pi]                                                  # t r theta phi
    # angles = [60/180 * pi, 120/180 * pi , 120/360 * pi, 240/360 * pi]      # theta low, up same with phi,
    # sample für himmels abrastern
    syng_angle, schwarzschild_angle  = angle_calc(mass, quad_param, distance)

    if forward_backward == "forward":
        angles = [pi/2, pi/2, 250/360 * 2 * pi, 290/360 * 2 * pi]                     # sample for phi raster mit const theta
    else:
        angles = [pi/2, pi/2, 78.315 / 360 * 2 * pi, 78.318 / 360 * 2 * pi]

    angle_intervall = angles[3]-angles[2]
    low_shadow_estimate = (90 - syng_angle)/360 * 2 * pi - 5*angle_intervall
    high_shadow_estimate = (90 - syng_angle)/360 * 2 * pi + 5*angle_intervall
        
    angles[2] = low_shadow_estimate
    angles[3] = high_shadow_estimate
    
    lower_phi_angle = angles[2] * (360/(2*pi))
    angle_steps = (angles[3]-angles[2])/(grid_steps+1) * (360/(2*pi))  
    geschw, asoc_points_on_square = lin_comb(ort, quad_param, mass, angles, grid_steps)
    seed_folder = init_calculation(mass, quad_param, ort, geschw[0])
    light_or_dark = []

    for count, gesch in enumerate(geschw):
        print(f"{count} out of {len(geschw)}")
        move_flag = data_make(ort, gesch, seed_folder, [quad_param, mass], steps, forward_backward, delta)
        light_or_dark.append(move_flag)
    shadow_angle = lower_phi_angle    
    for number in light_or_dark:
        if number==1:
            shadow_angle += angle_steps
    shadow_angle += 0.5 * angle_steps
    shadow_angle = 90 - shadow_angle
    print(f"Numerical value of shadow angle: {shadow_angle}")
            
    plot_folder(seed_folder, angles, ort, [quad_param, mass], distance,
                show_or_not=True, print_black_geodesics=True, d_plot=False, zoom_plot=True)
    plot_shadow(asoc_points_on_square, light_or_dark, seed_folder)
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
    main(1, 50, 0.5, 25000, 50, .005)
    


