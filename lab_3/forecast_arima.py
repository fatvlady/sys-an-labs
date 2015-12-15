__author__ = 'vlad'
from statsmodels.tsa.arima_model import ARIMA
import warnings
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brute

def choose_arima_order(endog):

    def objfunc(order, *params):
        series = params

        try:
            mod = ARIMA(series, order, exog=None)
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                res = mod.fit(disp=0, solver='bfgs', maxiter=5000)
        except:
            return float('inf')
        if math.isnan(res.aic):
            return float('inf')
        return res.aic


    grid = (slice(1, 5, 1), slice(0, 3, 1), slice(0, 5, 1))

    t = brute(objfunc, grid, args=endog, finish=None).astype(int)

    return ARIMA(endog, t, exog=None).fit()


def pos_of_xi_in_x(i, dimensions):
    """defines starting position of i-th coordinate in x"""
    pos_sum = 0
    for j in range(i):
        pos_sum += dimensions[j]
    return pos_sum


def forecast(x, forecast_num):
    mod = choose_arima_order(x[:-forecast_num])

    t = mod.forecast(forecast_num)[0]

    axis = np.arange(1, x.shape[0]+1)

    forecasted = np.zeros(x.shape[0])
    for k in xrange(x.shape[0]-forecast_num):
        forecasted[k] = x[k]
    for k in xrange(x.shape[0]-forecast_num, x.shape[0]):
        forecasted[k] = t[k-x.shape[0]+forecast_num]

    plt.clf()
    plt.plot(axis, map(lambda y: x[y-1], axis), color="b", label = 'X')
    plt.plot(axis, map(lambda y: forecasted[y-1], axis), color="r", label='Restored X')
    plt.xlabel('k')
    plt.ylabel('x')
    plt.legend(loc=0)
    plt.title('Forecast for X' + ' (unnormed)')
    return forecasted