"""
Core plotting of given folder module
"""
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
from numpy import sin, cos
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
        shadow_loc = QFileDialog.getExistingDirectory(self, "Select shadow_folder")
        aborted_folder = os.path.join(shadow_loc, "csvs_aborted")
        full_folder = os.path.join(shadow_loc, "csvs_full")
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
            filename = os.path.join(csv_loc,elements)
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


def plot_folder(seed_folder, params, dist, show_or_not):
    csv_loc = seed_folder + "/csvs_full/"
    csv_names = os.listdir(csv_loc)
    quad_param_d, mass_d = params
    r_anzeige = 1.1 * dist
    ax = plt.axes(projection='3d')
    ax.set_xlim([-r_anzeige ,r_anzeige])
    ax.set_ylim([-r_anzeige, r_anzeige])
    ax.set_zlim([-r_anzeige, r_anzeige])

    #ax.set_ylim([-1, 1])
    #ax.set_zlim([-1, 1])

    # for elements in csv_names:
    #     filename = os.path.join(csv_loc,elements)
    #     df = pd.read_csv(filename).head(100)
    #     rr = df.loc[0,:]
    #     phi = df.loc[2,:]
    #     theta = df.loc[1,:]
    #     xx = rr * cos(phi) * sin(theta)
    #     yy = rr * sin(phi) * sin(theta)
    #     zz = rr * cos(theta)
    #     ax.plot3D(xx, yy, zz, "b-")
    # ax.legend()
    # sph_make(ax)
    # # print(seed_folder + "/figs/" + f"dist_{dist}_initial.png")
    # plt.savefig(seed_folder + "/figs/" + f"dist_{dist}_initial.png")


    for elements in csv_names:
        filename = os.path.join(csv_loc,elements)
        df = pd.read_csv(filename)
        rr = df.loc[0,:]
        phi = df.loc[2,:]
        theta = df.loc[1,:]
        xx = rr * cos(phi) * sin(theta)
        yy = rr * sin(phi) * sin(theta)
        zz = rr * cos(theta)
        ax.plot3D(xx, yy, zz, "b-")
    ax.legend()
    sph_make(ax)
    print(seed_folder + "/figs/" + f"dist_{dist}_complete.png")
    plt.savefig(seed_folder + "/figs/" + f"dist_{dist}_complete.png")
    if show_or_not:
        plt.show()
    plt.close()


if __name__ == '__main__':
    window()
