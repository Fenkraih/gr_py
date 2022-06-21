class MetricDefinitions:
    def __init__(self, position, params, velocity=None):
        self.position = position
        self.params = params
        self.velocity = velocity

    def q_metric(self):
        """
        returns the metric
        """
        from numpy import sin, array, float64
        tt, r, theta, phi = self.position
        q, M = self.params
        g00 = -(1. - 2. * M / r) ** (1 + q)
        g11 = (1. - 2. * M / r) ** (- q - 1) * (1 + (M ** 2 * sin(theta) ** 2) / (r ** 2 - 2 * M * r)) ** (-q * (2 + q))
        g22 = (1. - 2. * M / r) ** (-q) * (1 + (M ** 2 * sin(theta) ** 2) / (r ** 2 - 2 * M * r)) ** (
                -q * (2 + q)) * r ** 2
        g33 = (1. - 2. * M / r) ** (-q) * r ** 2 * sin(theta) ** 2
        g = array([float64(g00), g11, g22, g33])
        return g

    def christoffel_precalculated(self):
        """
        Copy pasted the results of the sympy based gamma() function here to save computation time
        """
        from numpy import sin, cos, tan, zeros
        tt, r, theta, phi = self.position
        q, M = self.params
        gam = zeros([4, 4, 4])

        gam[0][0][1] = -1.0 * M * (q + 1) / (r * (2 * M - r))
        gam[0][1][0] = -1.0 * M * (q + 1) / (r * (2 * M - r))
        gam[1][0][0] = -1.0 * M * (-(2 * M - r) / r) ** (2 * q + 2) * (
                -(M ** 2 * sin(theta) ** 2 / r - 2 * M + r) / (2 * M - r)) ** (q * (q + 2)) * (q + 1) / (
                               r * (2 * M - r))
        gam[1][1][1] = 1.0 * M * (-M * q * (M - r) * (q + 2) * sin(theta) ** 2 + (q + 1) * (
                -M ** 2 * sin(theta) ** 2 + 2 * M * r - r ** 2)) / (
                               r * (2 * M - r) * (-M ** 2 * sin(theta) ** 2 + 2 * M * r - r ** 2))
        gam[1][1][2] = 1.0 * M ** 2 * q * (q + 2) * sin(2 * theta) / (
                M ** 2 * cos(2 * theta) - M ** 2 + 4 * M * r - 2 * r ** 2)
        gam[1][2][1] = 1.0 * M ** 2 * q * (q + 2) * sin(2 * theta) / (
                M ** 2 * cos(2 * theta) - M ** 2 + 4 * M * r - 2 * r ** 2)
        gam[1][2][2] = (-2 * M + r) * (M ** 2 * q * (M - r) * (q + 2) * sin(theta) ** 2 - 1.0 * M * q * (
                -M ** 2 * sin(theta) ** 2 + 2 * M * r - r ** 2) + (-2.0 * M + 1.0 * r) * (
                                               -M ** 2 * sin(theta) ** 2 + 2 * M * r - r ** 2)) / (
                               (2 * M - r) * (-M ** 2 * sin(theta) ** 2 + 2 * M * r - r ** 2))
        gam[1][3][3] = 1.0 * ((-M ** 2 * sin(theta) ** 2 / r + 2 * M - r) / (2 * M - r)) ** (q * (q + 2)) * (
                -2 * M + r) * (-M * q - 2 * M + r) * sin(theta) ** 2 / (2 * M - r)
        gam[2][1][1] = 1.0 * M ** 2 * q * (q + 2) * sin(2 * theta) / (
                r * (-2 * M + r) * (-M ** 2 * cos(2 * theta) + M ** 2 - 4 * M * r + 2 * r ** 2))
        gam[2][1][2] = 1.0 * (-M ** 2 * q * (M - r) * (q + 2) * sin(theta) ** 2 + M * q * (
                -M ** 2 * sin(theta) ** 2 + 2 * M * r - r ** 2) + (2 * M - r) * (
                                      -M ** 2 * sin(theta) ** 2 + 2 * M * r - r ** 2)) / (
                               r * (2 * M - r) * (-M ** 2 * sin(theta) ** 2 + 2 * M * r - r ** 2))
        gam[2][2][1] = 1.0 * (-M ** 2 * q * (M - r) * (q + 2) * sin(theta) ** 2 + M * q * (
                -M ** 2 * sin(theta) ** 2 + 2 * M * r - r ** 2) + (2 * M - r) * (
                                      -M ** 2 * sin(theta) ** 2 + 2 * M * r - r ** 2)) / (
                               r * (2 * M - r) * (-M ** 2 * sin(theta) ** 2 + 2 * M * r - r ** 2))
        gam[2][2][2] = 1.0 * M ** 2 * q * (q + 2) * sin(2 * theta) / (
                M ** 2 * cos(2 * theta) - M ** 2 + 4 * M * r - 2 * r ** 2)
        gam[2][3][3] = -0.5 * ((M ** 2 * cos(2 * theta) / (2 * r) - M ** 2 / (2 * r) + 2 * M - r) / (2 * M - r)) ** (
                q * (q + 2)) * sin(2 * theta)
        gam[3][1][3] = 1.0 * (M * q + 2 * M - r) / (r * (2 * M - r))
        gam[3][2][3] = 1.0 / tan(theta)
        gam[3][3][1] = 1.0 * (M * q + 2 * M - r) / (r * (2 * M - r))
        gam[3][3][2] = 1.0 / tan(theta)
        return gam

    def normalisation(self):
        """
        Checks sum of the trajectory with -+++ signature and computes the needed tt component
        """
        from numpy import sqrt
        if self.velocity is not None:
            vv = self.velocity
            g = self.q_metric()
            u_t = sqrt(-(vv[0] ** 2 * g[1] + vv[1] ** 2 * g[2] + vv[2] ** 2 * g[3]) * g[0] ** (-1))
        else:
            raise TypeError("Velocity is None")
        return u_t


class SymbolicMetricDefinitions:
    def __init__(self):
        pass

    def g(self, ii, jj):
        """
        returns the metric coefficient ij
        :param ii: 1. coord
        :param jj: 2. coord
        :return:
        """
        from sympy import symbols, sin
        M, t, r, theta, phi, q = symbols(" M t r theta phi q")
        coords = [t, r, theta, phi]

        g00 = -(1 - 2 * M / r) ** (1 + q)
        g01 = g02 = g03 = g10 = 0
        g11 = (1 - 2 * M / r) ** (-q - 1) * (1 + (M ** 2 * sin(theta) ** 2) / (r ** 2 - 2 * M * r)) ** (
                -q * (2 + q))
        g12 = g13 = g20 = g21 = 0
        g22 = (1 - 2 * M / r) ** (-q) * (1 + (M ** 2 * sin(theta) ** 2) / (r ** 2 - 2 * M * r)) ** (
                -q * (2 + q)) * r ** 2
        g23 = g30 = g31 = g32 = 0
        g33 = (1 - 2 * M / r) ** (-q) * r ** 2 * sin(theta) ** 2

        return ([[g00, g01, g02, g03],
                 [g10, g11, g12, g13],
                 [g20, g21, g22, g23],
                 [g30, g31, g32, g33]])[ii][jj]

    def d_g(self, ii, jj, kk, name):
        """
        :param name: name of the metric to chose the right coefficients
        :param ii: 1. coord
        :param jj: 2. coord
        :param kk: - coord after which the derivation is taking place
        :return: k-derivative of the metric coefficient ii,j
        """
        from sympy import diff, symbols
        M, t, r, theta, phi, q = symbols(" M t r theta phi q")
        coords = [t, r, theta, phi]
        return diff(self.g(ii, jj), coords[kk])

    def inv_g(self, ii, jj, name):
        """
        :param name: name of the metric to chose the right coefficients
        :param ii: 1. coord
        :param jj: 2. coord
        :return: ij coefficient of the inverse metric
        """
        from sympy import Matrix
        g = self.g
        K = Matrix([[g(0, 0), g(0, 1), g(0, 2), g(0, 3)],
                    [g(1, 0), g(1, 1), g(1, 2), g(1, 3)],
                    [g(2, 0), g(2, 1), g(2, 2), g(2, 3)],
                    [g(3, 0), g(3, 1), g(3, 2), g(3, 3)]])
        return K.inv(method="LU")[ii, jj]

    def gamma(self, ii, jj, kk, name):
        """
        :param name: name of the metric to chose the right coefficients
        :param ii: 1. coord upper
        :param jj: 2. coord lower
        :param kk: - coord after which the derivation is taking place lower
        :param name:
        :return:
        """
        from sympy import simplify
        s = 0
        for ll in range(4):
            s += 0.5 * self.inv_g(ii, ll, name) * (
                        self.d_g(kk, ll, jj, name) + self.d_g(ll, jj, kk, name) - self.d_g(jj, kk, ll, name))
        return simplify(s)
