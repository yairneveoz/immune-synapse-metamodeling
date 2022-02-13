# -*- coding: utf-8 -*-
"""
Created on Sun "Feb  6 15:32:05 2022

@author: yairn
"""

import pymc3 as pm

# Untrained model:


def get_pm_model1_untrained(df_trainingData_model1,
                            df_model1_untrainedTable):

    pm_model1 = pm.Model()
    
    with pm_model1:

        dfRV = df_model1_untrainedTable
        DP = 'Distribution parameters'

        t_KSEG1_obs = df_trainingData_model1.loc[:, 'time_sec'].values
        k_KSEG1_obs = df_trainingData_model1.loc[:, 'k0_kTnm2'].values
        dep_KSEG1_obs = df_trainingData_model1.loc[:, 'dep_nm'].values

        print(dep_KSEG1_obs)

        # rv_t
        ID = 'fp_t_dep_KSEG1'
        rv_t = pm.Uniform('rv_t',
                          0.,
                          100.,
                          observed=t_KSEG1_obs)

        # rv_k
        ID = 'fp_k_dep_KSEG1'
        rv_k = pm.Uniform('rv_k',
                          lower=dfRV.loc[ID, DP]['lower'],
                          upper=dfRV.loc[ID, DP]['upper'],
                          observed=k_KSEG1_obs)

        # dep_KSEG
        """TODO: read parameters values from RV table"""
        # rv_intercept_dep_KSEG1
        ID = 'rv_intercept_dep_KSEG1'
        rv_intercept_dep_KSEG1 = pm.Normal(ID,
                                           mu=eval(dfRV.loc[ID, DP]['mu']),
                                           sd=eval(dfRV.loc[ID, DP]['sd']))

        # rv_tSlope_dep_KSEG1
        ID = 'rv_tSlope_dep_KSEG1'
        rv_tSlope_dep_KSEG1 = pm.Normal(ID,
                                        mu=eval(dfRV.loc[ID, DP]['mu']),
                                        sd=eval(dfRV.loc[ID, DP]['sd']))

        # rv_kSlope_dep_KSEG1
        ID = 'rv_kSlope_dep_KSEG1'
        rv_kSlope_dep_KSEG1 = pm.Normal(ID,
                                        mu=eval(dfRV.loc[ID, DP]['mu']),
                                        sd=eval(dfRV.loc[ID, DP]['sd']))

        ID = 'rv_output_dep_KSEG1'
        rv_output_dep_KSEG1 = pm.Normal(ID,
                                        mu=rv_intercept_dep_KSEG1 +
                                        rv_tSlope_dep_KSEG1*rv_t +
                                        rv_kSlope_dep_KSEG1*rv_k,
                                        sd=eval(dfRV.loc[ID, DP]['sd']),
                                        observed=dep_KSEG1_obs)

    return pm_model1
#################################################

#@title Build trained model (with updated parameter estimates through their posteriors)
def get_pm_model1_trained(df_model1_trainedTable, 
                          observed_t = None, 
                          observed_k = None):
    
    ''' 
    return model1 trained based on trace1.
    If observed_t and/or observed_k are specified,
    return the model conditioned on those values
    '''
    
    pm_model1_trained = pm.Model()
    with pm_model1_trained:
        dfRV = df_model1_trainedTable
        DP = 'Distribution parameters'
        ### model1 - KS (kinetic segregation) ###########################    
        #  #####################################################
        
        rv_t = pm.Normal('rv_t', mu=70, sd=30, observed= observed_t)
        rv_k = pm.Normal('rv_k', mu=50, sd=20, observed= observed_k)

        # dep_KSEG ####################################################
        """TODO: read parameters values from RV table"""
        # rv_intercept_dep_KSEG1
        ID = 'rv_intercept_dep_KSEG1'
        rv_intercept_dep_KSEG1 = pm.Normal(ID, 
            mu = eval(dfRV.loc[ID,DP]['mu']), 
            sd = eval(dfRV.loc[ID,DP]['sd']))
        
        # rv_tSlope_dep_KSEG1
        ID = 'rv_tSlope_dep_KSEG1'
        rv_tSlope_dep_KSEG1 = pm.Normal(ID, 
            mu = eval(dfRV.loc[ID,DP]['mu']), 
            sd = eval(dfRV.loc[ID,DP]['sd'])) 
        
        # rv_kSlope_dep_KSEG1
        ID = 'rv_kSlope_dep_KSEG1'
        rv_kSlope_dep_KSEG1 = pm.Normal(ID, 
            mu = eval(dfRV.loc[ID,DP]['mu']), 
            sd = eval(dfRV.loc[ID,DP]['sd'])) 
        
        # rv_output_dep_KSEG1, equation:
        """
        eq = b + a1*x1 + a2*x2
        b = rv_intercept_dep_KSEG1
        a1 = rv_tSlope_dep_KSEG1
        x1 = rv_t
        a2 = rv_kSlope_dep_KSEG1
        x2 = rv_k
        """
        ID = 'rv_output_dep_KSEG1'
        rv_output_dep_KSEG1 = pm.Normal(ID, 
            mu = rv_intercept_dep_KSEG1 +\
            rv_tSlope_dep_KSEG1*rv_t +\
            rv_kSlope_dep_KSEG1*rv_k,
            sd = eval(dfRV.loc[ID,DP]['sd'])) #

    return pm_model1_trained
            