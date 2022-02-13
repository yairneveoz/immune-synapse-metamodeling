# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 15:23:32 2022

@author: yairn

1. Pre process of data.
    1.1 Read raw training data for model1.
    1.2 Crop and scale data, assign values and units for x and y axes.
    1.3 Arange training data in 'pandas' dataFrame.
        1.3.1 Plot training data.
2. Pre modeling (finding initial fit parameters).
    2.1 Define fit equations and parameters.
    2.2 Get fit parameters.
    2.3 Create fitted data.
        2.3.1 Plot fitted data.
3. Create tables for the model.
    3.1 Define class RV.
    3.2  Define class Model.
    3.3 Get untrained model info.
        3.3.1 Display untrained table 
    3.4 Save outputs.    
4. Surrogate model with pymc3.
    4.1 Set untrained pymc3 model.
        4.1.1 Display and save graphviz of untrained model:
    4.2 Set trained pymc3 model.
        4.2.1 Plot trace_plots of the trained model:
    4.3 Set trained pymc3 model
        4.3.1 Display and save graphviz of trained model:        
    4.4 Create a map with trained pymc3 model.
5. Outputs.
    5.1
    5.2
    5.3
"""

import numpy as np
import pandas as pd
import pymc3 as pm
import graphviz as gv
# from IPython.display import display

# 0. Import model1 packages:
import model1.styling
import model1.plotting
import model1.preprocessing
import model1.parametersfitting
import model1.model_info
import model1.modeling
import model1.trainedmodeltomesh

#################################################
# 1. Read and arange data:
# 1.1 Read raw training data for model1:
dep_raw_data = pd.read_csv('model1/dep_raw_data.csv', header=None)

# 1.2 Crop and scale raw data to nanometers,
# assign values and units for x and y axes:
t_array, k_array, dep_training_data_nm =\
    model1.preprocessing.cropAndScaleRawData(dep_raw_data)

# 1.3 Arange training data in pandas dataFrame (df):
df_dep_nm = model1.preprocessing.trainingDataToDataFrame(
    t_array, k_array, dep_training_data_nm)

# 1.4 Plot training data:
nRows = 4

DataToPlot = nRows*[None]
DataToPlot[0] = [[df_dep_nm.columns,
                  df_dep_nm.index],
                 [df_dep_nm.values]]
plotWhat = [True, False, False, False]

model1.plotting.plotData(DataToPlot, plotWhat)
#################################################
# 2. Pre modeling (finding initial fit parameters):
# 2.1 Define fit equations and parameters:
df_trainingData_model1 = pd.read_csv('trainingData_model1.csv')

# 2.2 Get fit parameters:
df_fitParameters_dep = model1.parametersfitting.setFitFunction(
    df_trainingData_model1)

# 2.3 Create fitted data from fit parameters:
df_fitted_dep = model1.parametersfitting.fittedData(
    df_fitParameters_dep, df_trainingData_model1)

# 2.4 Plot fitted data:
DataToPlot[1] = [[df_fitted_dep.columns,
                  df_fitted_dep.index],
                 [df_fitted_dep.values]]
plotWhat = [True, True, False, False]

model1.plotting.plotData(DataToPlot, plotWhat)
#################################################
# 3. Create table for the model:
# 3.1 Define class RV
model1.model_info.RV

# 3.2 Define class Model:
model1.model_info.Model

# 3.3 Get untrained model info:
model1_dep_info = model1.model_info.createModelInfo(df_fitParameters_dep)

df_model1_untrainedTable = model1_dep_info.get_dataframe()
# 3.4 Display untrained table:
df_model1_untrainedTable = df_model1_untrainedTable.set_index('ID')
print(df_model1_untrainedTable)
model1.model_info.displayInfo(df_model1_untrainedTable)

# 3.5 Output (temp)

#################################################
# 4. Modeling with pymc3:
# 4.1 Set untrained pymc3 model:
pm_model1 = model1.modeling.get_pm_model1_untrained(
     df_trainingData_model1, df_model1_untrainedTable)

# 4.1.1 Display and save graphviz of untrained model:
gv1_untrained = pm.model_to_graphviz(pm_model1)
gv1_untrained
gv1_untrained_filename = gv1_untrained.render(filename='gv1_untrained')

# 4.2 Run untrained model:
with pm_model1:
    trace1 = pm.sample(2000, chains=4);

# 4.2.1 Plot trace_plots of the trained model:
pm.traceplot(trace1);

# temp (if untrained model doesn't run):
df_model1_trainedTable = df_model1_untrainedTable

# 4.3 Set trained model:
pm_model1_trained= model1.modeling.get_pm_model1_trained(
        df_model1_trainedTable)

# 4.3.1 Display and save graphviz of trained model:
gv1_trained = pm.model_to_graphviz(pm_model1_trained)
gv1_trained
gv1_trained_filename = gv1_trained.render(filename='gv1_trained')

# 4.4 Trained_mesh:
n_t = 21
max_t = 100.
min_t = 0.

n_k = 20
max_k = 100.
min_k = max_k/n_k

if True:
    deps_mean, deps_std =\
    model1.trainedmodeltomesh.trained_mesh(min_t, max_t, n_t,
                                           min_k, max_k, n_k,
                                           df_model1_trainedTable)
