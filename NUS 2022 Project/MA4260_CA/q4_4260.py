# -*- coding: utf-8 -*-
"""q4-4260.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1k1SOnfsMxdCh3WtJ322efAhVFANxbmsA
"""

# Commented out IPython magic to ensure Python compatibility.
# %pip install -i https://pypi.gurobi.com gurobipy

import gurobipy as gp
from gurobipy import GRB

farm = ['wheat', 'corn', 'sugarbeets']
sell = ['wheat_bad', 'corn_bad', 'sugarbeets_highprice_bad', 'sugarbeets_lowprice_bad', 
        'wheat_aver', 'corn_aver', 'sugarbeets_highprice_aver', 'sugarbeets_lowprice_aver',
        'wheat_good', 'corn_good', 'sugarbeets_highprice_good', 'sugarbeets_lowprice_good']
buy = ['wheat_bad', 'corn_bad',
       'wheat_aver', 'corn_aver',
       'wheat_good', 'corn_good']

cropyield = {'wheat_aver': 2.5, 'corn_aver': 3.0, 'sugarbeets_aver': 20.0, 
             'wheat_good': 3, 'corn_good': 3.6, 'sugarbeets_good': 24.0, 
             'wheat_bad': 2, 'corn_bad': 2.4, 'sugarbeets_bad': 16.0}

cropcost = {'wheat': 150, 'corn': 230, 'sugarbeets': 260}
cropconstraint = { 'wheat_bad': 200, 'wheat_aver': 200, 'wheat_good': 200,
                  'corn_bad': 240, 'corn_aver': 240, 'corn_good': 240}

cropsellprice = {'wheat_bad' : 170, 'wheat_aver' : 170, 'wheat_good' : 170,
                 'corn_bad' : 150, 'corn_aver' : 150, 'corn_good' : 150,
                 'sugarbeets_highprice_bad': 36, 'sugarbeets_highprice_aver': 36, 'sugarbeets_highprice_good': 36,
                 'sugarbeets_lowprice_bad': 10, 'sugarbeets_lowprice_aver': 10, 'sugarbeets_lowprice_good': 10}
cropbuyprice = {'wheat_bad' : 238, 'wheat_aver' : 238, 'wheat_good' : 238,
                'corn_bad' : 210, 'corn_aver' : 210, 'corn_good' : 210}

bad = 0.5
aver = 0
good = 0.5

totalland = 500
maxhighbeets = 6000

model = gp.Model('StochasticProgram')

# Variables
landvar = model.addVars(farm, name="landvar")
sellvar = model.addVars(sell, name="sellvar")
buyvar = model.addVars(buy, name="buyvar")

# Capacity constraint.
model.addConstrs( (landvar[f] >= 0 for f in farm) )
model.addConstrs( (sellvar[f] >= 0 for f in sell) )
model.addConstrs( (buyvar[f] >= 0 for f in buy) )
model.addConstrs( (landvar['wheat']*cropyield[f]+buyvar[f]-sellvar[f]>=cropconstraint[f] for f in buy[0:6:2]) )
model.addConstrs( (landvar['corn']*cropyield[f]+buyvar[f]-sellvar[f]>=cropconstraint[f] for f in buy[1:6:2]) )

model.addConstr(sellvar['sugarbeets_highprice_bad']+sellvar['sugarbeets_lowprice_bad']-landvar['sugarbeets']*cropyield['sugarbeets_bad']<=0)
model.addConstr(sellvar['sugarbeets_highprice_aver']+sellvar['sugarbeets_lowprice_aver']-landvar['sugarbeets']*cropyield['sugarbeets_aver']<=0)
model.addConstr(sellvar['sugarbeets_highprice_good']+sellvar['sugarbeets_lowprice_good']-landvar['sugarbeets']*cropyield['sugarbeets_good']<=0)
model.addConstr(sellvar['sugarbeets_highprice_bad']<= maxhighbeets)
model.addConstr(sellvar['sugarbeets_highprice_aver']<= maxhighbeets)
model.addConstr(sellvar['sugarbeets_highprice_good']<= maxhighbeets)
model.addConstr(gp.quicksum(landvar[f] for f in farm) <= totalland)

obj = gp.quicksum(cropcost[f]*landvar[f] for f in farm) - bad*gp.quicksum(cropsellprice[f]*sellvar[f] for f in sell[0:4]) - aver*gp.quicksum(cropsellprice[f]*sellvar[f] for f in sell[4:8]) - good*gp.quicksum(cropsellprice[f]*sellvar[f] for f in sell[8:12]) + bad*gp.quicksum(cropbuyprice[f]*buyvar[f] for f in buy[0:2]) + aver*gp.quicksum(cropbuyprice[f]*buyvar[f] for f in buy[2:4]) + good*gp.quicksum(cropbuyprice[f]*buyvar[f] for f in buy[4:6])
model.setObjective(obj, GRB.MINIMIZE)

# Verify model formulation

model.write('StochasticProgram.lp')

# Run optimization engine

model.optimize()

print(landvar)

print(sellvar)

print(buyvar)