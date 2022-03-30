"""
Runge kutta method implementation for geodesic and raytracing calculation
"""
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
    fn = init_vel
    yn = init_pos
    quad_param, mass = params
    naked_singularity = 2*mass

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

        r_pos.append(init_pos[1].copy())
        theta_pos.append(init_pos[2].copy())
        phi_pos.append(init_pos[3].copy())

        yn_k1 = init_vel
        fn_k1 = accel(yn, fn, params)

        yn_k2 = init_vel + delta / 2 * accel(yn + delta / 2 * yn_k1, init_vel + delta / 2 * fn_k1, params)
        fn_k2 = accel(yn + delta / 2 * yn_k1, init_vel + delta / 2 * fn_k1, params)

        yn_k3 = init_vel + delta / 2 * accel(yn + delta / 2 * yn_k2, init_vel + delta / 2 * fn_k2, params)
        fn_k3 = accel(yn + delta / 2 * yn_k2, init_vel + delta / 2 * fn_k2, params)

        yn_k4 = init_vel + delta * accel(yn + delta * yn_k3, init_vel + delta * fn_k3, params)
        fn_k4 = accel(yn + delta * yn_k3, init_vel + delta * fn_k3, params)

        new_pos = init_pos + delta / 6 * (yn_k1 + 2 * yn_k2 + 2 * yn_k3 + yn_k4)
        new_velocity = init_vel + delta / 6 * (fn_k1 + 2 * fn_k2 + 2 * fn_k3 + fn_k4)

        init_pos = new_pos
        init_vel = new_velocity

    trajectory.append(r_pos)
    trajectory.append(theta_pos)
    trajectory.append(phi_pos)

    return array(trajectory), move_flag


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
    fn = init_vel
    yn = init_pos
    quad_param, mass = params
    naked_singularity = 2*mass

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
        r_pos.append(init_pos[1].copy())
        theta_pos.append(init_pos[2].copy())
        phi_pos.append(init_pos[3].copy())

        yn_k1 = init_vel
        fn_k1 = accel(yn, fn, params)

        yn_k2 = init_vel + delta / 2 * accel(yn + delta / 2 * yn_k1, init_vel + delta / 2 * fn_k1, params)
        fn_k2 = accel(yn + delta / 2 * yn_k1, init_vel + delta / 2 * fn_k1, params)

        yn_k3 = init_vel + delta / 2 * accel(yn + delta / 2 * yn_k2, init_vel + delta / 2 * fn_k2, params)
        fn_k3 = accel(yn + delta / 2 * yn_k2, init_vel + delta / 2 * fn_k2, params)

        yn_k4 = init_vel + delta * accel(yn + delta * yn_k3, init_vel + delta * fn_k3, params)
        fn_k4 = accel(yn + delta * yn_k3, init_vel + delta * fn_k3, params)

        new_pos = init_pos - delta / 6 * (yn_k1 + yn_k2 + yn_k3 + yn_k4)
        new_velocity = init_vel - delta / 6 * (fn_k1 + fn_k2 + fn_k3 + fn_k4)

        init_pos = new_pos
        init_vel = new_velocity

    trajectory.append(r_pos)
    trajectory.append(theta_pos)
    trajectory.append(phi_pos)

    return array(trajectory), move_flag