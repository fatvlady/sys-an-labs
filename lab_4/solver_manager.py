# -*- encoding: utf-8 -*-


from lab_4.solve import *
from lab_4.solve_custom import SolveExpTh
from lab_4.read_data import read_data
from lab_4.presentation import PolynomialBuilderExpTh, PolynomialBuilder


def prob(x, xmax, xmin):
    return np.fabs((x - xmax) / (xmax - xmin))


def classify_danger_rating(level):
    if 0 <= level <= 0.125:
        return 0, u"Безпечна ситуація"
    elif 0.125 < level <= 0.25:
        return 1, u"Нештатна ситуація по одному параметру"
    elif 0.25 < level <= 0.375:
        return 2, u"Нештатна ситуація по декількох параметрах"
    elif 0.375 < level <= 0.5:
        return 3, u"Спостерігається загроза аварії"
    elif 0.5 < level <= 0.625:
        return 4, u"Висока загроза аварії"
    elif 0.625 < level <= 0.75:
        return 5, u"Критична ситуація"
    elif 0.75 < level <= 0.875:
        return 6, u"Шанс уникнути аварії дуже малий"
    elif 0.875 < level <= 1:
        return 7, u"Аварія"


class SolverManager(object):
    Y_C = np.array([9400.0, 20000, 2e+007])  # contingency value
    Y_D = np.array([9350.0, 10000, 1e+007])  # danger value

    def __init__(self, d):
        self.custom_struct = d['custom_struct']
        if d['custom_struct']:
            self.solver = SolveExpTh(d)
        else:
            self.solver = Solve(d)
        self.current_iter = 1

    def prepare(self, filename):
        self.time, self.data = read_data(filename)
        self.N_all_iter = len(self.time)

    def fit(self, shift, n):
        self.solver.load_data(self.data[shift:shift + n])
        self.solver.prepare()
        self.risk()
        self.presenter = PolynomialBuilderExpTh(self.solver) if self.custom_struct else PolynomialBuilder(self.solver)

    def risk(self):
        self.p = prob(self.solver.YF, self.Y_C, self.Y_D)
        self.f = 1 - (1 - self.p[:, 0]) * (1 - self.p[:, 1]) * (1 - self.p[:, 2])
        self.danger_rate = [classify_danger_rating(i) for i in self.f]

    def plot(self, steps):
        if steps > 0:
            self.presenter.plot_graphs_with_prediction(steps)
        else:
            self.presenter.plot_graphs()

    def predict(self, steps):
        pass
