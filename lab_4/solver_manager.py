# -*- encoding: utf-8 -*-


from lab_4.solve import *
from lab_4.solve_custom import SolveExpTh
from lab_4.read_data import read_data
from lab_4.operator_view import OperatorViewWindow


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
        self.first_launch = True
        self.batch_size = d['samples']
        self.forecast_size = d['pred_steps']
        self.operator_view = OperatorViewWindow(warn=self.Y_C, fail=self.Y_D, callback=self,
                                                descriptions=[u'прибыль\ от\ перевозки,\ грн', u'запас\ хода,\ м',
                                                              u'Запасенная\ в\ АБ\ энергия,\ Дж'])
        self.current_iter = 1

    def prepare(self, filename):
        self.time, self.data = read_data(filename)
        increment = self.time[-1] - self.time[-2]
        self.time = np.append(self.time, np.arange(1, 1 + self.forecast_size) * increment + self.time[-1])
        self.N_all_iter = len(self.time)
        self.operator_view.show()

    def start_machine(self):
        self.operator_view.start_process()

    def launch(self):
        if self.current_iter + self.batch_size < len(self.data):
            self.fit(self.current_iter, self.batch_size)
            self.current_iter += 1
        else:
            self.operator_view.timer.stop()

    def fit(self, shift, n):
        data_window = self.data[shift:shift + n]
        self.solver.load_data(data_window[:, :-2])  # y2 and y3 not used
        self.solver.prepare()
        y_forecast = self.predict()
        if self.first_launch:
            self.operator_view.initial_graphics_fill(real_values=data_window[:, -3:], predicted_values=y_forecast,
                                                     risk_values=y_forecast,
                                                     time_ticks=self.time[shift:shift + n + self.forecast_size])
            self.first_launch = False
        else:
            self.operator_view.update_graphics(data_window[-1, -3:], y_forecast, y_forecast,
                                               self.time[shift + n - 1:shift + n + self.forecast_size])
        # self.risk() # really suspicious realisation

    def risk(self):
        self.p = prob(self.solver.YF, self.Y_C, self.Y_D)
        self.f = 1 - (1 - self.p[:, 0]) * (1 - self.p[:, 1]) * (1 - self.p[:, 2])
        self.danger_rate = [classify_danger_rating(i) for i in self.f]
        print(self.f)

    def predict(self):
        y_f = [self.solver.YF, self.solver.XF[0][3], self.solver.XF[1][2]]
        return y_f

    def table_data(self):
        return