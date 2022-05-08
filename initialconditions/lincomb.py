from numpy import array, pi, sqrt
from coordtransform.coords import sph_to_karth
from metric import q_metric

def lin_comb(ort, quad_param, mass, angles, steps):
    g = q_metric(ort, [quad_param, mass])
    e1 = [1*(1/sqrt(g[1])),0,0]      # forward
    e2 = [0,1*(1/sqrt(g[2])),0]      # upward
    e3 = [0,0,1*(1/sqrt(g[3]))]      # leftward

    theta_low, theta_up, phi_low, phi_up = angles
    coords = []
    square_points = []

    if theta_low == theta_up:
        for ll in range(steps+1):
            sphere = [1, theta_low,
             phi_low + ll * (phi_up-phi_low)/steps]
            # print(sphere)
            sph_karth = sph_to_karth([sphere])
            ax, ay, az = sph_karth
            local_coord = array([ay*e1[0], ax*e2[1], az*e3[2]])                 #  array([[0,1,0], [1,0,0], [0,0,1]])
            square_points.append(.1/local_coord[0] * local_coord)
            coords.append(local_coord)
            # print(local_coord)

    elif phi_low == phi_up:
        for kk in range(steps+1):
            sphere = [1, theta_low + kk * (theta_up-theta_low)/steps, phi_low]
            # print(sphere)
            sph_karth = sph_to_karth([sphere])
            ax, ay, az = sph_karth
            local_coord = array([ay*e1[0], ax*e2[1], az*e3[2]])
            coords.append(local_coord)
            square_points.append(.1/local_coord[0] * local_coord)
            #print(local_coord)

    else:
        for kk in range(steps+1):
            for ll in range(steps+1):
                 sphere = [1, theta_low + kk * (theta_up-theta_low)/steps,
                  phi_low + ll * (phi_up-phi_low)/steps]
                 # print(sphere)
                 sph_karth = sph_to_karth([sphere])
                 ax, ay, az = sph_karth
                 local_coord = array([ay*e1[0], ax*e2[1], az*e3[2]])
                 coords.append(local_coord)
                 square_points.append(.1/local_coord[0] * local_coord)
                 #print(local_coord)

    return coords, square_points        # rotate it for some reason

def lin_comb_2():
    return None
