import numpy as np
import skfuzzy as fuzz
import pandas as pd
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# The universe of variables and membership functions
velocity = ctrl.Antecedent(np.arange(0, 51, 1), 'velocity')
angle = ctrl.Antecedent(np.arange(-2, 2.5, 0.5), 'angle')
db = ctrl.Consequent(np.arange(0, 1.05, 0.05), 'db')

# Rules

velocity['low'] = fuzz.trapmf(velocity.universe, [0, 0, 10, 20])
velocity['med'] = fuzz.trapmf(velocity.universe, [10, 20, 30, 40])
velocity['high'] = fuzz.trapmf(velocity.universe, [30, 40, 50, 50])

angle['left'] = fuzz.trapmf(angle.universe, [-2,-2, -1, -0.5])
angle['str'] = fuzz.trapmf(angle.universe, [-1, -0.5, 0.5, 1])
angle['right'] = fuzz.trapmf(angle.universe, [0.5, 1, 2,2])

db['aggr'] = fuzz.trapmf(db.universe, [0, 0, 0.3, 0.4])
db['norm'] = fuzz.trapmf(db.universe, [0.3 , 0.4, 0.6, 0.7])
db['over'] = fuzz.trapmf(db.universe, [0.6, 0.7, 1,1])


"""
==================
DECLARE THE RULES
==================
"""

rule1 = ctrl.Rule(velocity['low'] & angle['left'], db['norm'])
rule2 = ctrl.Rule(velocity['low'] & angle['str'], db['norm'])
rule3 = ctrl.Rule(velocity['low'] & angle['right'], db['norm'])

rule4 = ctrl.Rule(velocity['med'] & angle['left'], db['aggr'])
rule5 = ctrl.Rule(velocity['med'] & angle['str'], db['norm'])
rule6 = ctrl.Rule(velocity['med'] & angle['right'], db['over'])

rule7 = ctrl.Rule(velocity['high'] & angle['left'], db['aggr'])
rule8 = ctrl.Rule(velocity['high'] & angle['str'], db['aggr'])
rule9 = ctrl.Rule(velocity['high'] & angle['right'], db['over'])

db_ctrl = ctrl.ControlSystem(
    [rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])


"""
==========
SIMULATION
==========
"""

data_input = pd.read_csv("Tes3.csv", delimiter=',', names=['speed', 'kmh', 'yaw' , 'rad', 'pirad'])
fuzzy_value = [0.0]*len(data_input)
data_input['Fuzzy Value'] = fuzzy_value
for i in range(1, len(data_input)):
    driver = ctrl.ControlSystemSimulation(db_ctrl)
    driver.input['velocity'] = float(data_input['kmh'][i])
    driver.input['angle'] = (float(data_input['pirad'][i]))
    driver.compute()
    data_input['Fuzzy Value'][i] = driver.output['db']


print(data_input['Fuzzy Value'])
print(driver.output['db'])
data_input.to_csv('Output3.csv')
