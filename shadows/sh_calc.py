import matplotlib.pyplot as plt


def plot_shadow(asoc_points_on_square, light_or_dark, seed_folder):
    x_coord = []
    y_coord = []
    z_coord = []
    for elements in asoc_points_on_square:
        x_coord.append(elements[0])
        y_coord.append(elements[1])
        z_coord.append(elements[2])

    for kk in range(len(light_or_dark)):
        if light_or_dark[kk]==1:
            plt.plot(y_coord[kk], z_coord[kk], "b+")
        if light_or_dark[kk]==0:
            plt.plot(y_coord[kk], z_coord[kk], "k+")
    plt.savefig(seed_folder + "\\figs\\" + f"computed_shadow.png")