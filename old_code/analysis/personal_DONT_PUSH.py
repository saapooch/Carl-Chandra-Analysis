from analysis import Analysis
import pandas as pd
from optlang import Model, Variable, Constraint, Objective
import numpy


anal = Analysis(portfolio = ['AAPL', 'SQ', 'GWPH', 'EA'])
diff =  anal.calculate_interday_difference()
mean, vol = anal.volitility_analysis(30)
diff['sum'] = diff.sum(1)

# print diff, vol


w1 = Variable('w1', lb=500)
w2 = Variable('w2', lb=500)
w3 = Variable('w3', lb=500)
w4 = Variable('w4', lb=500)

r1 = 1.34
r2 = 1.20
r3 = 2.33
r4 = 0.57


const1 = Constraint(w1+w2+w3+w4, ub=5000)
const2 = Constraint((w1/5000)*r1 + (w2/5000)*r2 + (w3/5000)*r3+ (w4/5000)*r4 , ub=3)



ans = []
initial = 5000
for index, row in diff.iterrows():

    c1 = row['Change AAPL']/100
    c2 = row['Change SQ']/100
    c3 = row['Change GWPH']/100
    c4 = row['Change EA']/100


    obj = Objective( w1*c1+w2*c2+w3*c3+w4*c4 , direction='max')


    model = Model(name='Simple model')
    model.objective = obj
    model.add([const1, const2])

    status = model.optimize()

    weights = []
    for var_name, var in model.variables.iteritems():
        weights.append(var.primal)

    print(model.objective.value, weights[0], weights[1], weights[2], weights[3])

# print ans
