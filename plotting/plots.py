"""
Core plotting of given folder module
"""
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from numpy import sin, cos, pi, around, linspace, sqrt
from PyQt5.QtWidgets import QFileDialog, QApplication, QMainWindow
from initialconditions.visuals import sph_make


class FolderClass(QMainWindow):
    """
    printing a folder class
    """

    def __init__(self):
        super(FolderClass, self).__init__()
        self.setWindowTitle('Anwendung')

    def select_folder(self):
        parent_folder = QFileDialog.getExistingDirectory(self, "Select shadow_folder")
        aborted_folder = os.path.join(parent_folder, "csvs_aborted")
        full_folder = os.path.join(parent_folder, "csvs_full")
        list_aborted = os.listdir(aborted_folder)
        list_full = os.listdir(full_folder)
        complete_list = (list_full + list_aborted).sort()
        return complete_list, list_aborted, list_full

    def plot_folder(self):
        csv_loc = QFileDialog.getExistingDirectory(self, "Select folder")
        csv_names = os.listdir(csv_loc)
        r_anzeige = 1.5 * 80

        ax = plt.axes(projection='3d')
        ax.set_xlim([-r_anzeige, r_anzeige])
        ax.set_ylim([-r_anzeige, r_anzeige])
        ax.set_zlim([-r_anzeige, r_anzeige])

        for elements in csv_names:
            filename = os.path.join(csv_loc, elements)
            df = pd.read_csv(filename)
            df["xx"] = df["rr"] * cos(df["phi"]) * sin(df["theta"])
            df["yy"] = df["rr"] * sin(df["phi"]) * sin(df["theta"])
            df["zz"] = df["rr"] * cos(df["theta"])
            ax.plot3D(df["xx"], df["yy"], df["zz"], "b-")
        sph_make(ax)
        plt.show()
        plt.close()


def window():
    app = QApplication(sys.argv)
    win = FolderClass()
    win.plot_folder()
    sys.exit(app.exec_())


def three_d_plotter(r_anzeige, csv_names, csv_loc, print_black_geodesics, shadow_csv, shadow_loc):
    ax = plt.axes(projection='3d')
    ax.set_xlim([-r_anzeige, r_anzeige])
    ax.set_ylim([-r_anzeige, r_anzeige])
    ax.set_zlim([-r_anzeige, r_anzeige])
    ax.set_xlabel("c=G=M=1")

    for elements in csv_names:
        filename = os.path.join(csv_loc, elements)
        df = pd.read_csv(filename)
        rr = df.loc[0, :]
        phi = df.loc[2, :]
        theta = df.loc[1, :]
        xx = rr * cos(phi) * sin(theta)
        yy = rr * sin(phi) * sin(theta)
        zz = rr * cos(theta)
        ax.plot3D(xx, yy, zz, "b-")
    if print_black_geodesics:
        for elements in shadow_csv:
            filename = os.path.join(shadow_loc, elements)
            df = pd.read_csv(filename)
            rr = df.loc[0, :]
            phi = df.loc[2, :]
            theta = df.loc[1, :]
            xx = rr * cos(phi) * sin(theta)
            yy = rr * sin(phi) * sin(theta)
            zz = rr * cos(theta)
            ax.plot3D(xx, yy, zz, "k-")
    ax.legend()
    sph_make(ax)


def plane_chooser(xx, yy, zz, plane="equatorial"):
    if plane == "equatorial":
        pl_ax_1 = xx
        pl_ax_2 = yy
    elif plane == "meridional":
        pl_ax_1 = xx
        pl_ax_2 = zz
    else:
        pl_ax_1 = xx
        pl_ax_2 = yy
    return pl_ax_1, pl_ax_2


def photon_sphere_indicate(quad_param_d, mass_d, ax):
    equatorial_photon_sphere = (2 * quad_param_d + 3) * mass_d
    xval = linspace(-equatorial_photon_sphere, equatorial_photon_sphere)
    yval = sqrt(equatorial_photon_sphere**2-xval**2)
    ax.plot(xval, yval, "r")
    ax.plot(xval, -yval, "r")


def plot_equatorial_surface_line(ax):
    surface = 2.3
    xval = linspace(-surface, surface)
    yval = sqrt(surface**2-xval**2)
    ax.plot(xval, yval, "c")
    ax.plot(xval, -yval, "c")


def two_d_plotter(dist, mass_d, quad_param_d, phi_low, phi_up, r_anzeige, zoom_plot, csv_names, csv_loc,
                  print_black_geodesics, shadow_csv, shadow_loc, the_low, the_up, seed_folder, show_or_not,
                  plane="equatorial"):
    if plane == "meridional":
        zoom_plot = False
    ax = plt.axes()
    if plane == "equatorial":
        photon_sphere_indicate(quad_param_d, mass_d, ax)
        plot_equatorial_surface_line(ax)
    ax.set_title(f"r = {dist} M= {mass_d} q= {quad_param_d} ϕ = [{phi_low}, {phi_up}] θ = [{the_low}, {the_up}]")
    ax.set_xlim([-r_anzeige, r_anzeige])
    ax.set_ylim([-r_anzeige, r_anzeige])
    if zoom_plot:
        axins = ax.inset_axes([0.7, 0.5, 0.25, 0.25])
    x1, x2, y1, y2 = -.1, .1, 2 * quad_param_d + 3 * mass_d - 0.1, 2 * quad_param_d + 3 * mass_d + 0.1
    if zoom_plot:
        axins.set_xlim(x1, x2)
        axins.set_ylim(y1, y2)
        ax.indicate_inset_zoom(axins, edgecolor="black")
    for elements in csv_names:
        filename = os.path.join(csv_loc, elements)
        df = pd.read_csv(filename)
        rr = df.loc[0, :]
        phi = df.loc[2, :]
        theta = df.loc[1, :]
        xx = rr * cos(phi) * sin(theta)
        yy = rr * sin(phi) * sin(theta)
        zz = rr * cos(theta)
        pl_ax_1, pl_ax_2 = plane_chooser(xx, yy, zz, plane)
        ax.plot(pl_ax_1, pl_ax_2, "b-", label="Light")
        if zoom_plot:
            axins.plot(pl_ax_1, pl_ax_2, "b-", label="Light")
            if plane == "equatorial":
                photon_sphere_indicate(quad_param_d, mass_d, axins)
    if print_black_geodesics:
        for elements in shadow_csv:
            filename = os.path.join(shadow_loc, elements)
            df = pd.read_csv(filename)
            rr = df.loc[0, :]
            phi = df.loc[2, :]
            theta = df.loc[1, :]
            xx = rr * cos(phi) * sin(theta)
            yy = rr * sin(phi) * sin(theta)
            zz = rr * cos(theta)
            pl_ax_1, pl_ax_2 = plane_chooser(xx, yy, zz, plane)
            ax.plot(pl_ax_1, pl_ax_2, "k-", label="Shadow")
            if zoom_plot:
                axins.plot(pl_ax_1, pl_ax_2, "k-", label="Shadow")
    black_patch = mpatches.Patch(color='black', label='Shadow geodesics')
    blue_patch = mpatches.Patch(color='blue', label='Light geodesics')
    red_patch = mpatches.Patch(color='red', label='photon circle')
    cyan_patch = mpatches.Patch(color='cyan', label='body surface')
    ax.set_xlabel("c=G=M=1")
    if plane == "equatorial":
        ax.legend(handles=[blue_patch, black_patch, red_patch, cyan_patch])
    else:
        ax.legend(handles=[blue_patch, black_patch])
    print(seed_folder + "/figs/" + f"dist_{dist}_complete.png")
    plt.savefig(seed_folder + "/figs/" + f"dist_{dist}_complete.png")
    if show_or_not:
        plt.show()
    plt.close()


def plot_folder(seed_folder, angles, ort, params, dist, show_or_not, print_black_geodesics, d_plot, zoom_plot,
                plane="equatorial"):
    csv_loc = seed_folder + "/csvs_full/"
    shadow_loc = seed_folder + "/csvs_aborted/"
    csv_names = os.listdir(csv_loc)
    shadow_csv = os.listdir(shadow_loc)
    quad_param_d, mass_d = params
    phi_low = around(angles[2] * (360 / (2 * pi)), decimals=4)
    phi_up = around(angles[3] * (360 / (2 * pi)), decimals=4)
    the_low = around(angles[0] * (180 / (pi)), decimals=4)
    the_up = around(angles[1] * (180 / (pi)), decimals=4)
    r_anzeige = 1.1 * dist
    if d_plot:
        three_d_plotter(r_anzeige, csv_names, csv_loc, print_black_geodesics, shadow_csv, shadow_loc)
    else:
        two_d_plotter(dist, mass_d, quad_param_d, phi_low, phi_up, r_anzeige, zoom_plot, csv_names, csv_loc,
                      print_black_geodesics, shadow_csv, shadow_loc, the_low, the_up, seed_folder, show_or_not,
                      plane)


def subfolders(parent_folder):
    shadow_loc = os.path.join(parent_folder, "csvs_aborted")
    csv_loc = os.path.join(parent_folder, "csvs_full")
    csv_names = os.listdir(csv_loc)
    shadow_csv = os.listdir(shadow_loc)
    return shadow_csv, csv_names, shadow_loc, csv_loc


def part_plot(ax, parent_folder, quad, shadow_angle):
    shadow_csv, csv_names, shadow_loc, csv_loc = subfolders(parent_folder)
    mass = 1
    r_anzeige = 50
    ax.set_xlim([-r_anzeige, r_anzeige])
    ax.set_ylim([-r_anzeige, r_anzeige])
    ax.set_title(f"q = {quad}, α = {around(shadow_angle, 3)}")
    axins = ax.inset_axes([0.65, 0.65, 0.25, 0.25])
    x1, x2, y1, y2 = -.1, .1, 2 * quad + 3 * mass - 0.1, 2 * quad + 3 * mass + 0.1
    axins.set_xlim(x1, x2)
    axins.set_ylim(y1, y2)
    ax.indicate_inset_zoom(axins, edgecolor="black")

    for elements in csv_names:
        filename = os.path.join(csv_loc, elements)
        df = pd.read_csv(filename)
        rr = df.loc[0, :]
        phi = df.loc[2, :]
        theta = df.loc[1, :]
        xx = rr * cos(phi) * sin(theta)
        yy = rr * sin(phi) * sin(theta)
        ax.plot(xx, yy, "b-", label="Light")
        axins.plot(xx, yy, "b-", label="Light")
    for elements in shadow_csv:
        filename = os.path.join(shadow_loc, elements)
        df = pd.read_csv(filename)
        rr = df.loc[0, :]
        phi = df.loc[2, :]
        theta = df.loc[1, :]
        xx = rr * cos(phi) * sin(theta)
        yy = rr * sin(phi) * sin(theta)
        ax.plot(xx, yy, "k-", label="Shadow")
        axins.plot(xx, yy, "k-", label="Shadow")


def multi_plot(parent_folders, quad_list, shadow_list):
    fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(18, 5))
    axis_objects = [ax[0, 0], ax[0, 1], ax[1, 0], ax[1, 1]]
    for num, parent_folder in enumerate(parent_folders):
        part_plot(axis_objects[num], parent_folder, quad_list[num], shadow_list[num])
    plt.tight_layout()
    plt.savefig(parent_folders[-1] + "/figs/" + f"q_compare.png")


if __name__ == '__main__':
    window()
