import time
from metric import q_metric
from shadows import plot_shadow
from numpy import pi, sqrt, array
from init import init_calculation, data_make
from plotting import plot_folder
from initialconditions import lin_comb


def main(mass, distance, quad_param, steps, grid_steps, delta):
    start = time.time()
    forward_backward = "backward"
    ort = [0, distance, pi/2, pi]                                                  # t r theta phi
    g = q_metric(ort, [quad_param, mass])
    e1 = [1*(1/sqrt(g[1])),0,0]      # forward
    e2 = [0,1*(1/sqrt(g[2])),0]      # upward
    e3 = [0,0,1*(1/sqrt(g[3]))]      # leftward
    angles = [4*pi/10, 6*pi/10, 4*pi/10, 6*pi/10]      # theta low, up same with phi
    # NOTE

    geschw = lin_comb([e1, e2, e3], angles, grid_steps)
    # geschw = [e1,e2,e3]           # tetrade Demo
    seed_folder = init_calculation(mass, quad_param, ort, geschw[0])
    light_or_dark = []

    for count, gesch in enumerate(geschw):
        print(f"{count} out of {len(geschw)}")
        move_flag = data_make(ort, gesch, seed_folder, [quad_param, mass], steps, forward_backward, delta)
        light_or_dark.append(move_flag)
    plot_folder(seed_folder, [quad_param, mass], distance, show_or_not=True)
    #plot_shadow(karth_quadrat, light_or_dark, seed_folder)
    print(time.time() - start)

# TODO 1: . Teilchen fliegen sehr weit weg manchmal -> gtt exponential wachstum
#       untersuchen um diese auszusortieren  ?
# TODO 2:   koordinaten der initialen geschwindigkigkeitsvektoren fixen
# TODO 3: irgendwo ist ein mixup zwischen theta und phi Koordinaten bei den inital conditions


if __name__ == '__main__':
    main(1, 50, 1, 200, 21, .5)
    #main(1, 50, 1, 2000, 1)
    #main(1, 50, 0.5, 2000, 1)
    #main(1, 50, 0.75, 2000, 1)
