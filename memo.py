import numpy as np
import pandas as pd

# Importing the dataset
data = pd.read_csv("day_approach_maskedID_timeseries.csv")
essencial_keys = ['nr. sessions', 'total km', 'km Z3-4', 'km Z5-T1-T2', 'km sprinting','strength training', 'hours alternative', 'perceived exertion','perceived trainingSuccess', 'perceived recovery']
model_keys = {
    "Frts":{},
    "days":{}
}
termination = ["."+str(ter) for ter in range(1,7)]
for key in essencial_keys:
    arr = []
    for ter in termination:
        arr.append(key+ter)
    arr.append('injury')
    model_keys['Frts'][key] = arr
for ter in termination:
    arr = [] 
    for key in essencial_keys:
        arr.append(key+ter)
    arr.append('injury')
    model_keys['days'][ter] = arr
print(model_keys['days']['.1'])

termination = ["."+str(ter) for ter in range(1,7)]
for key in essencial_keys:
    arr = []
    for ter in termination:
        arr.append(key+ter)
    arr.append('injury')
    model_keys['Frts'][key] = arr
for ter in termination:
    arr = [] 
    for key in essencial_keys:
        arr.append(key+ter)
    arr.append('injury')
    model_keys['days'][ter] = arr
print(model_keys['days']['.1'])
data[model_keys['Frts']['total km']].head(20)

New_features = {
    "Feature" : {}
} 
statictislb = ["_mean","_std","_total"]
label = [model_keys['days']['.1'][1]]
label.append(model_keys['days']['.1'][4])

for lb in label:
    arr = []
    for stat_lb in statictislb:
        arr.append(lb[:-2]+stat_lb)
    New_features['Feature'][lb[:-2]] = arr
# ["total km_mean","total km_std","total km_total",'km sprinting_mean','km sprinting_std','km sprinting_total','strength training_mode','nr. sessions_mode']
model_stats = pd.DataFrame()

#o  = input(data['injury']==1)
#o = input(data[model_keys['Frts']['total km']].values[0])
print(New_features['Feature'],data.shape[0])
for feature in New_features['Feature']:
    arr = []
    arr1 = []
    stats = []
    for row in range(data.shape[0]):
        arr.append(sum(data[model_keys['Frts'][feature]].values[row]))
        arr1.append(np.std(data[model_keys['Frts'][feature]].values[row]))
        print(row)
    print("aqui")
    n = len(model_keys['Frts'][feature])
    stats.append([suma/n for suma in arr])
    stats.append(arr1)
    stats.append(arr)
    for stat in range(len(stats)):
        print("stat")
        model_stats[New_features['Feature'][feature][stat]]  = stats[stat]
print(model_stats.to_string())