"""
visuals for the initial condition stuff
"""
import matplotlib.pyplot as plt
from numpy import sqrt, pi, cos, sin, size, linspace, outer, ones, array, arccos, arctan2


def sph_make(ax):
    """
    visual to print a 3d sphere on a plt plot
    :param ax:
    :return:
    """
    coefs_1 = (0.8, 0.8, 0.8)
    rx_1, ry_1, rz_1 = 1 / sqrt(coefs_1)
    rz_1 = 1/(rx_1*ry_1)

    # Make data
    u_space = linspace(0, 2 * pi, 100)
    v_space= linspace(0, pi, 100)

    x_space = rx_1 * outer(cos(u_space), sin(v_space))
    y_space = ry_1 * outer(sin(u_space), sin(v_space))
    z_space = rz_1 * outer(ones(size(u_space)), cos(v_space))

    # Plot the surface
    surf_1 = ax.plot_surface(x_space, y_space, z_space, alpha=0.8, label='Sphäre')
    surf_1._edgecolors2d = surf_1._edgecolor3d
    surf_1._facecolors2d = surf_1._facecolor3d


def square_to_polar_grid_v2(steps, distance, width):
    karth_quadrat = []
    karth_kugel = []
    sph_kugel = []

    for kk in range(steps):
        karth_quadrat.append([-distance, (-1 * width + 2*width * kk / steps), -1 * width])
        for ll in range(steps):
            karth_quadrat.append([-distance, (-1 * width + 2*width * kk / steps), (-1 * width + 2*width * ll / steps)])

    for elements in karth_quadrat:
        length = sqrt(elements[0] ** 2 + elements[1] ** 2 + elements[2] ** 2)
        karth_kugel.append(array(elements) / length * 0.1)

    if False:
        for elements in karth_kugel:
            xx = elements[0]
            yy = elements[1]
            zz = elements[2]
            # spiegelung an x=-0.1
            xx = -xx - 0.2 - 29.9
            rr = sqrt(xx ** 2 + yy ** 2 + zz ** 2)
            theta = arccos(zz / rr)
            phi = arctan2(yy, xx)
            sph_kugel.append([rr,theta,phi])

    return karth_quadrat, sph_kugel, karth_kugel

def square_to_polar_grid(steps):
    karth_quadrat = []
    karth_kugel = []
    sph_kugel = []

    for kk in range(steps+1):
        karth_quadrat.append([50, (-0.5 + 1 * kk / steps), (-0.5)])
        for ll in range(steps):
            karth_quadrat.append([50, (-0.5 + 1 * kk / steps), (-0.5 + 1 * ll / steps)])

    for elements in karth_quadrat:
        length = sqrt(elements[0] ** 2 + elements[1] ** 2 + elements[2] ** 2)
        karth_kugel.append(array(elements) / length * 0.1)

    for elements in karth_kugel:
        xx = elements[0]
        yy = elements[1]
        zz = elements[2]
        # spiegelung an x=-0.1
        xx = -xx - 0.2 - 29.9
        rr = sqrt(xx ** 2 + yy ** 2 + zz ** 2)
        theta = arccos(zz / rr)
        phi = arctan2(yy, xx)
        sph_kugel.append([rr,theta,phi])

    return karth_quadrat, sph_kugel, karth_kugel


def plot_karth_multi_vel(karth_geschw_multi):
    r_anzeige = 0.2
    ax = plt.axes(projection='3d')
    ax.set_xlim([-r_anzeige, r_anzeige])
    ax.set_ylim([-r_anzeige, r_anzeige])
    ax.set_zlim([-r_anzeige, r_anzeige])
    for karth_geschw in karth_geschw_multi:
        x_coord = []
        y_coord = []
        z_coord = []
        for elements in karth_geschw:
            x_coord.append(elements[0])
            y_coord.append(elements[1])
            z_coord.append(elements[2])
        ax.plot3D(x_coord, y_coord, z_coord, "+")
    plt.show()


def sph_to_karth(geschw):
    geschw_karth = []
    for elements in geschw:
        xx = elements[0] * cos(elements[2]) * sin(elements[1])
        yy = elements[0] * sin(elements[2]) * sin(elements[1])
        zz = elements[0] * cos(elements[1])
        geschw_karth.append([xx,yy,zz])
    return geschw_karth


def square_to_sphere_tester():
    karth_quadrat, sph_kugel, karth_kugel = square_to_polar_grid(40)
    kugel = sph_to_karth(sph_kugel)
    plot_karth_multi_vel([karth_quadrat, kugel])


if __name__ == '__main__':
    square_to_sphere_tester()