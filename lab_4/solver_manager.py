from lab_4.solve import Solve
from lab_4.solve_custom import SolveExpTh
from lab_4.read_data import read_data
from lab_4.presentation import PolynomialBuilderExpTh, PolynomialBuilder

class SolverManager(object):

    def __init__(self,d):
        self.custom_struct = d['custom_struct']
        if d['custom_struct']:
            self.solver = SolveExpTh(d)
        else:
            self.solver = Solve(d)

    def prepare(self, filename):
        self.time, self.data = read_data(filename)

    def fit(self, shift, n):
        self.solver.load_data(self.data[shift:shift + n])
        self.solver.prepare()
        self.presenter = PolynomialBuilderExpTh(self.solver) if self.custom_struct else PolynomialBuilder(self.solver)

    def plot(self, steps):
        if steps > 0:
            self.presenter.plot_graphs_with_prediction(steps)
        else:
            self.presenter.plot_graphs()

    def predict(self, steps):
        pass