from numpy import array, pi, sqrt
from coordtransform.coords import sph_to_karth

def lin_comb(basis_set, angles, steps):
    e1, e2, e3 = basis_set      #forward upward left
    theta_low, theta_up, phi_low, phi_up = angles
    coords = []

    if theta_low == theta_up:
        for ll in range(steps+1):
            sphere = [1, theta_low,
             phi_low + ll * (phi_up-phi_low)/steps]
            # print(sphere)
            sph_karth = sph_to_karth([sphere])
            ax, ay, az = sph_karth
            local_coord = array([ax*e1[0], ay*e2[1], az*e3[2]])
            coords.append(local_coord)

    elif phi_low == phi_up:
        for kk in range(steps+1):
            sphere = [1, theta_low + kk * (theta_up-theta_low)/steps, phi_low]
            print(sphere)
            sph_karth = sph_to_karth([sphere])
            ax, ay, az = sph_karth
            local_coord = array([ax*e1[0], ay*e2[1], az*e3[2]])
            coords.append(local_coord)

    else:
        for kk in range(steps+1):
            for ll in range(steps+1):
                 sphere = [1, theta_low + kk * (theta_up-theta_low)/steps,
                  phi_low + ll * (phi_up-phi_low)/steps]
                 # print(sphere)
                 sph_karth = sph_to_karth([sphere])
                 ax, ay, az = sph_karth
                 local_coord = array([ax*e1[0], ay*e2[1], az*e3[2]])
                 coords.append(local_coord)

    return coords

def lin_comb_2():
    return None
