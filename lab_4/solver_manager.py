# -*- encoding: utf-8 -*-


from lab_4.solve import *
from lab_4.solve_custom import SolveExpTh
from lab_4.read_data import read_data
from lab_4.presentation import PolynomialBuilderExpTh, PolynomialBuilder
#from lab_4.operator_view import OperatorViewWindow


def prob(x, xmax, xmin):
    res = np.fabs((x - xmax) / (xmax - xmin))
    r = np.ma.array(res, mask = np.array(x >= xmax), fill_value= 0)
    return r.filled()

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
    Y_C = np.array([950, 12100, 5000000])  # warning value
    Y_D = np.array([0.0, 0, 0])  # failure value

    def __init__(self, d):
        self.custom_struct = d['custom_struct']
        d['dimensions'][3] = 1
        if d['custom_struct']:
            self.solver = SolveExpTh(d)
        else:
            self.solver = Solve(d)
        self.data_window = None
        #self.operator_view = OperatorViewWindow()
        self.current_iter = 1 # for what??

    def prepare(self, filename):
        self.time, self.data = read_data(filename)
        self.N_all_iter = len(self.time)
        #self.operator_view.show()

    def fit(self, shift, n):
        self.data_window = self.data[shift:shift + n]
        self.solver.load_data(self.data_window[:, :-2]) #y2 and y3 not used
        self.solver.prepare()
        y_forecast = self.predict()
        # self.risk() # really suspicious realisation
        self.presenter = PolynomialBuilderExpTh(self.solver) if self.custom_struct else PolynomialBuilder(self.solver)

    def risk(self):
        self.p = prob(self.solver.YF, self.Y_C, self.Y_D)
        self.f = 1 - (1 - self.p[:, 0]) * (1 - self.p[:, 1]) * (1 - self.p[:, 2])
        self.danger_rate = [classify_danger_rating(i) for i in self.f]
        print(self.f)

    def plot(self, steps):
        if steps > 0:
            self.presenter.plot_graphs_with_prediction(steps)
        else:
            self.presenter.plot_graphs()

    def predict(self):
        y_f = [self.solver.YF, self.solver.XF[0][3], self.solver.XF[1][2]]
        return y_f

