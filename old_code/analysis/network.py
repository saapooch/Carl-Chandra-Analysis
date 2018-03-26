from sklearn.neural_network import MLPClassifier, MLPRegressor
from analysis.analysis import Analysis
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class Network(analysis.Analysis):
    """

    """

    def __init__(self, portfolio = None):
        super(Network, self).__init__(portfolio = portfolio)
        portfolio = self.portfolio

    def run_network(self):
        mlp = MLPRegressor(solver='sgd', alpha=1e-5, hidden_layer_sizes=(3, 2))

        _10_day, _25_day = self.moving_percent_change()

        result = self.calculate_interday_difference()

        plt.plot()

        # X =  map(list,zip(*[_10_day.iloc[25:250, 0].values, _25_day.iloc[25:250, 0].values]))
        X1 = _10_day.iloc[25:250, 0].values
        X2 = _25_day.iloc[25:250, 0].values
        y = result.iloc[0:225, 0].values

        threedee = plt.figure().gca(projection='3d')
        threedee.scatter(X1, X2, y)
        threedee.set_xlabel('10 day moving percent change')
        threedee.set_ylabel('25 day moving percent change')
        threedee.set_zlabel('25 day post percent change')
        plt.show()



        #
        # X = np.asarray(X, dtype="float64")
        # y = np.asarray(y, dtype="float64")
        #
        #
        # mlp.fit(X, y)
        #
        # ans = mlp.predict([[-4.0123,1.4123], [9,3]])
        #
        # print ans
