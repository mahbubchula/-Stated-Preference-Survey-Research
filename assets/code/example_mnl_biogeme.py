"""
Example MNL Model Estimation using Biogeme
Stated Preference Survey Research Course
Author: Mahbub Hassan
Course: https://github.com/mahbubchula/-Stated-Preference-Survey-Research
"""

import pandas as pd
import biogeme.database as db
import biogeme.biogeme as bio
from biogeme import models
from biogeme.expressions import Beta, Variable

# ===========================
# Step 1: Load Data
# ===========================
# Load your SP survey data
df = pd.read_csv('sp_data.csv')

# Create Biogeme database
database = db.Database('SP_Mode_Choice', df)

# ===========================
# Step 2: Define Variables
# ===========================
# Alternative availability (1 if available, 0 otherwise)
av_car = Variable('av_car')
av_transit = Variable('av_transit')
av_bike = Variable('av_bike')

# Attributes
cost_car = Variable('cost_car')
cost_transit = Variable('cost_transit')
cost_bike = Variable('cost_bike')

time_car = Variable('time_car')
time_transit = Variable('time_transit')
time_bike = Variable('time_bike')

# Choice indicator
choice = Variable('choice')  # 1=car, 2=transit, 3=bike

# ===========================
# Step 3: Define Parameters
# ===========================
# Alternative-Specific Constants (ASC)
asc_car = Beta('asc_car', 0, None, None, 0)  # Fixed to 0 (reference)
asc_transit = Beta('asc_transit', 0, None, None, 0)
asc_bike = Beta('asc_bike', 0, None, None, 0)

# Generic coefficients
beta_cost = Beta('beta_cost', 0, None, None, 0)
beta_time = Beta('beta_time', 0, None, None, 0)

# ===========================
# Step 4: Define Utility Functions
# ===========================
V_car = asc_car + beta_cost * cost_car + beta_time * time_car
V_transit = asc_transit + beta_cost * cost_transit + beta_time * time_transit
V_bike = asc_bike + beta_cost * cost_bike + beta_time * time_bike

# Associate utility functions with alternatives
V = {1: V_car, 2: V_transit, 3: V_bike}

# Associate availability conditions with alternatives
av = {1: av_car, 2: av_transit, 3: av_bike}

# ===========================
# Step 5: Define Model
# ===========================
# Multinomial Logit Model
logprob = models.loglogit(V, av, choice)

# Create Biogeme object
biogeme = bio.BIOGEME(database, logprob)
biogeme.modelName = 'SP_MNL_Mode_Choice'

# ===========================
# Step 6: Estimate Model
# ===========================
results = biogeme.estimate()

# ===========================
# Step 7: Display Results
# ===========================
print("\n=== Model Estimation Results ===")
print(results.shortSummary())

# Get parameter estimates
params = results.getBetaValues()
print("\n=== Parameter Estimates ===")
for param, value in params.items():
    print(f"{param}: {value:.4f}")

# Get statistics
stats = results.getGeneralStatistics()
print("\n=== Model Statistics ===")
for stat, value in stats.items():
    print(f"{stat}: {value}")

# ===========================
# Step 8: Calculate Value of Time (VoT)
# ===========================
vot = -params['beta_time'] / params['beta_cost']
print(f"\n=== Value of Time ===")
print(f"VoT: ${vot:.2f} per hour")

# ===========================
# Step 9: Elasticities
# ===========================
# Calculate aggregate elasticities
print("\n=== Elasticities ===")
print("Run biogeme.calculate_elasticities() for detailed elasticity analysis")

# Save results
results.writeHtmlFile('results_mnl.html')
print("\nResults saved to results_mnl.html")
