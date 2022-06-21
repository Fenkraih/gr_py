"""
Runge kutta method implementation for geodesic and raytracing calculation
"""
from numba import jit
from numpy import array
from metric.mets import accel


def runge_kutta_4_forward(init_vel, init_pos, steps, params, delta):
    """
    Forward method for calculating next step of trajectory
    :param init_vel:
    :param init_pos:
    :param steps:
    :param params:
    :param delta:
    :return:
    """
    u = init_vel
    y = init_pos
    h = delta

    quad_param, mass = params
    naked_singularity = 2 * mass

    trajectory = []
    r_pos = []
    theta_pos = []
    phi_pos = []
    move_flag = 1

    for kk in range(steps):
        if abs(init_pos[1]) < naked_singularity + 0.3:
            move_flag = 0
            print("Teilchen stürzt auf nackte Singularität zu ... breche ab")
            break
        r_pos.append(y[1])
        theta_pos.append(y[2])
        phi_pos.append(y[3])

        m1 = h * u
        k1 = h * accel(y, u, params)

        m2 = h * (u + 0.5 * k1)
        k2 = h * accel(y + 0.5 * m1, u + 0.5 * k1, params)

        m3 = h * (u + 0.5 * k2)
        k3 = h * accel(y + 0.5 * m2, u + 0.5 * k2, params)

        m4 = h * (u + k3)
        k4 = h * accel(y + m3, u + k3, params)

        y += (m1 + 2 * m2 + 2 * m3 + m4) / 6
        u += (k1 + 2 * k2 + 2 * k3 + k4) / 6

    trajectory.append(r_pos)
    trajectory.append(theta_pos)
    trajectory.append(phi_pos)

    return array(trajectory), move_flag


# @jit(nopython=True)
def runge_kutta_4_backward(init_vel, init_pos, steps, params, delta):
    """
    Forward method for calculating next step of trajectory
    :param init_vel:
    :param init_pos:
    :param steps:
    :param params:
    :param delta:
    :return:
    """
    u = init_vel
    y = init_pos
    h = delta

    quad_param, mass = params
    naked_singularity = 2 * mass

    trajectory = []
    r_pos = []
    theta_pos = []
    phi_pos = []
    move_flag = 1

    for kk in range(steps):
        if abs(init_pos[1]) < naked_singularity + 0.3:
            move_flag = 0
            print("Teilchen stürzt auf nackte Singularität zu ... breche ab")
            break
        r_pos.append(y[1])
        theta_pos.append(y[2])
        phi_pos.append(y[3])

        m1 = h * u
        k1 = h * accel(y, u, params)

        m2 = h * (u + 0.5 * k1)
        k2 = h * accel(y + 0.5 * m1, u + 0.5 * k1, params)

        m3 = h * (u + 0.5 * k2)
        k3 = h * accel(y + 0.5 * m2, u + 0.5 * k2, params)

        m4 = h * (u + k3)
        k4 = h * accel(y + m3, u + k3, params)

        y -= (m1 + 2 * m2 + 2 * m3 + m4) / 6
        u -= (k1 + 2 * k2 + 2 * k3 + k4) / 6

    trajectory.append(r_pos)
    trajectory.append(theta_pos)
    trajectory.append(phi_pos)

    return array(trajectory), move_flag


def euler_forward(vel, pos, steps, params, delta):
    quad_param, mass = params
    naked_singularity = 2 * mass + 0.3
    move_flag = 1
    trajectory = []
    r_pos = []
    theta_pos = []
    phi_pos = []
    for kk in range(steps):
        if abs(pos[1]) < naked_singularity:
            print("Teilchen stürzt auf nackte Singularität zu ... breche ab")
            move_flag = 0
            break
        r_pos.append(pos[1])
        theta_pos.append(pos[2])
        phi_pos.append(pos[3])
        pos = pos + delta * vel
        vel = vel + accel(pos, vel, params) * delta
    trajectory.append(r_pos)
    trajectory.append(theta_pos)
    trajectory.append(phi_pos)
    return array(trajectory), move_flag


def euler_backward(vel, pos, steps, params, delta):
    quad_param, mass = params
    naked_singularity = 2 * mass + 0.3
    move_flag = 1
    trajectory = []
    r_pos = []
    theta_pos = []
    phi_pos = []
    for kk in range(steps):
        if abs(pos[1]) < naked_singularity:
            print("Teilchen stürzt auf nackte Singularität zu ... breche ab")
            move_flag = 0
            break
        r_pos.append(pos[1])
        theta_pos.append(pos[2])
        phi_pos.append(pos[3])
        pos = pos - delta * vel
        vel = vel - accel(pos, vel, params) * delta
    trajectory.append(r_pos)
    trajectory.append(theta_pos)
    trajectory.append(phi_pos)
    return array(trajectory), move_flag
