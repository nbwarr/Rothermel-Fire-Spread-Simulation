#!/usr/bin/env python
# coding: utf-8

# Basic Rothermel Surface Fire Spread Model
# Source: https://www.fs.usda.gov/rm/pubs_series/rmrs/gtr/rmrs_gtr371.pdf

# 
# $
# \text{Basic Rothermel Surface Fire Spread Model}
# \\
# \\ R=\Large\frac{I_{R}\xi(1+\phi_w+\phi_s)}{\rho_b\epsilon Q_{ig}}
# $
# 

# $
# \text{Model Assuming No Wind or Slope}
# \\R=\Large\frac{I_{R}\xi}{\rho_b\epsilon Q_{ig}}
# $

# In[27]:


# The following script accepts the parameters layed out by the RSFSM explanation and provides
# a rate of fire spread assuming no wind and no slope

import math

# h: low heat content (btu/lb) 
# S_T: total mineral content (lb minerals / lb fuel)
# S_e: effective mineral content ((lb minerals - lb silica) / lb fuel)
# ρ_p: oven dry particle density (lb / ft^3)
# σ: surface area to volume ratio (ft^2 / ft^3)
# w_0: oven dry fuel load (lb / ft^2)
# δ: fuel bed depth (ft)
# M_x: dead fuel moisture of extinction (fraction)
# M_f: moisture content (lb moisture / lb fuel)
# U: wind velocity at midflame height (ft/min)
def rateOfSpread(h, S_T, S_e, ρ_p, σ, w_0, δ, M_x, M_f, U):
    
    # Reaction Intensity
    r_M = M_f / M_x
    η_M = 1.0 - 2.59 * r_M + 5.11 * pow(r_M, 2.0) - 3.52 * pow(r_M, 3.0)
    η_S = 0.174 * pow(S_e, -0.19)
    w_n = w_0 * (1 - S_T)
    A = 133.0 * pow(σ, -0.7913)
    ρ_b = w_0 / δ
    β = ρ_b / ρ_p
    β_op = 3.348 * pow(σ, -0.8189)
    Γ_max = pow(σ, 1.5) * pow((495 + 0.0594 * pow(σ, 1.5)), -1.0)
    Γ = Γ_max * pow(β / β_op, A) * math.exp(A * (1 - (β / β_op)))
    I_R = Γ * w_n * h * η_M * η_S
    # Propagating Flux Ratio
    Ξ = pow(192.0 + 0.2595 * σ, -1.0) * math.exp((0.792 + 0.681 * pow(σ, 0.5)) * (β + 0.1))
    
    # Bulk Density
    ρ_b = w_0 / δ

    # Effective Heating Number
    ϵ = math.exp(-138.0 / σ)

    # Heat of Preignition
    Q_ig = 250.0 + 1116.0 * M_f
    
    numerator = I_R * Ξ
    denominator = ρ_b * ϵ * Q_ig
    
    if I_R <= 0:
        return 0
    else:
        return numerator / denominator


# In[28]:


# Call for Standard High Load, Dry Climate Grass in the Seattle area climate
currentSpreadRate = round(rateOfSpread(8000, 0.0555, 0.010, 32, 2000, 1, 3, 0.15, 0.08, 0), 3)
futureSpreadRate = round(rateOfSpread(8000, 0.0555, 0.010, 32, 2000, 1, 3, 0.15, 0.07, 0), 3)
print(f"Current Seattle Rate of fire spread for dense tall grass(ft/s): {currentSpreadRate}")
print(f"Future(100y) Seattle Rate of fire spread for dense tall grass(ft/s): {futureSpreadRate}")


# In[29]:


# Calculates the area burned given a fire spread rate and a time
def calcArea(spreadRate, hours):
    return spreadRate * 60 * 60 * hours
    


# In[30]:


# Area burned given a burn time

# Give burn time in hours
burnTime = 6
currentBurnArea = round(calcArea(currentSpreadRate, burnTime), 3)
futureBurnArea = round(calcArea(futureSpreadRate, burnTime), 3)
print(f"Current area burned in 6 hours (ft^2): {currentBurnArea}")
print(f"Future area burned in 6 hours (ft^2): {futureBurnArea}")
print(f"Added burn area (ft^2): {round(futureBurnArea - currentBurnArea, 3)}")


# In[ ]:




