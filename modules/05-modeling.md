---
title: "Module 5 - Modeling"
layout: default
nav_order: 14
---

# Module 5: Discrete Choice Modeling & Estimation

<div class="alert alert-info">
<strong>Duration:</strong> 3 weeks | <strong>Effort:</strong> 14-16 hours | <strong>Level:</strong> Advanced
</div>

---

## 📋 Overview

Your data is collected—now it's time to extract insights. This module teaches you how to transform SP survey responses into policy-relevant choice models. You'll learn to prepare data, specify utility functions, estimate models using industry-standard software (Biogeme/Apollo), interpret coefficients, calculate willingness-to-pay, and select the best model among competing specifications.

This is where your SP study delivers value: turning stated preferences into quantitative predictions that inform real-world decisions.

---

## 🎯 Learning Objectives

By completing this module, you will be able to:

1. **Structure** SP datasets for estimation including wide/long formats, effect coding, dummy coding, and panel identifiers
2. **Estimate** Multinomial Logit (MNL) models using Biogeme (Python) and Apollo (R) with proper syntax and diagnostics
3. **Extend** basic models to Mixed Logit (random parameters), Nested Logit, and Latent Class specifications
4. **Apply** model selection criteria including likelihood ratio tests, AIC/BIC, and predictive accuracy checks
5. **Calculate** policy-relevant outputs: elasticities, marginal willingness-to-pay, value of time, and scenario forecasts
6. **Interpret** parameter estimates for non-technical audiences and translate to actionable recommendations

---

## 📊 Data Preparation Fundamentals

### From Raw Survey to Estimation Dataset

**Typical Data Pipeline:**

```
Raw Survey Export (Qualtrics/SurveyCTO)
  ↓
Cleaning & Quality Filters
  ↓
Reshape to Long Format
  ↓
Code Attributes (dummy/effect coding)
  ↓
Add Alternative-Specific Variables
  ↓
Ready for Estimation
```

### Data Structures

#### Wide Format (Survey Export)

```
RespondentID | Task1_Choice | Task1_Price_A | Task1_Time_A | Task1_Price_B | Task1_Time_B | ...
001          | A            | 3.50          | 30           | 2.50          | 40           | ...
002          | B            | 4.00          | 25           | 3.00          | 35           | ...
```

**Challenges:**
- Each task adds 10+ columns
- Difficult to estimate (software expects long format)
- Hard to add alternative-specific constants

#### Long Format (Estimation-Ready)

```
RespID | TaskID | AltID | Choice | Price | Time | Frequency | Comfort | ASC
001    | 1      | A     | 1      | 3.50  | 30   | 10        | 1       | 1
001    | 1      | B     | 0      | 2.50  | 40   | 15        | 0       | 0
001    | 2      | A     | 0      | 4.00  | 35   | 8         | 0       | 1
001    | 2      | B     | 1      | 2.50  | 40   | 12        | 1       | 0
002    | 1      | A     | 0      | 3.00  | 35   | 12        | 1       | 1
002    | 1      | B     | 1      | 4.00  | 30   | 10        | 0       | 0
```

**Benefits:**
- One row per alternative per task per respondent
- Easy to add variables
- Standard for all estimation software

### Reshaping Data: R Example

```r
library(tidyr)
library(dplyr)

# Wide to long transformation
data_long <- data_wide %>%
  # Create unique observation ID
  mutate(obs_id = row_number()) %>%

  # Pivot tasks to long
  pivot_longer(
    cols = starts_with("Task"),
    names_to = c("task", ".value"),
    names_pattern = "Task(\\d+)_(.*)"
  ) %>%

  # Separate alternative attributes
  pivot_longer(
    cols = matches("_[AB]$"),
    names_to = c("attribute", "alternative"),
    names_pattern = "(.*)_([AB])$",
    values_to = "value"
  ) %>%

  # Pivot alternatives to separate rows
  pivot_wider(
    names_from = attribute,
    values_from = value
  ) %>%

  # Create choice indicator
  mutate(
    chosen = ifelse(alternative == Choice, 1, 0)
  ) %>%

  # Clean up
  select(RespID, task, alternative, chosen, Price, Time, Frequency, Comfort)

# View result
head(data_long, 10)
```

### Reshaping Data: Python Example

```python
import pandas as pd
import numpy as np

# Load wide-format data
data_wide = pd.read_csv("survey_export.csv")

# Extract task columns
task_cols = [col for col in data_wide.columns if col.startswith('Task')]

# Function to reshape one respondent's data
def reshape_respondent(row):
    resp_data = []

    # Number of tasks (assuming attributes: Price, Time, Frequency, Comfort)
    n_tasks = len([c for c in task_cols if 'Price_A' in c])

    for task in range(1, n_tasks + 1):
        for alt in ['A', 'B']:
            resp_data.append({
                'RespID': row['RespID'],
                'TaskID': task,
                'AltID': alt,
                'Choice': 1 if row[f'Task{task}_Choice'] == alt else 0,
                'Price': row[f'Task{task}_Price_{alt}'],
                'Time': row[f'Task{task}_Time_{alt}'],
                'Frequency': row[f'Task{task}_Frequency_{alt}'],
                'Comfort': row[f'Task{task}_Comfort_{alt}']
            })

    return pd.DataFrame(resp_data)

# Apply to all respondents
data_long = pd.concat([reshape_respondent(row) for _, row in data_wide.iterrows()],
                      ignore_index=True)

# Add panel identifiers
data_long['obs_id'] = data_long.groupby('RespID').ngroup()

print(data_long.head(10))
```

### Coding Categorical Variables

#### Dummy Coding (Reference Category)

**Example:** Comfort level (3 categories: Standing, Seated, Premium)

```
Comfort = 0 (Standing) → Comfort_Seated = 0, Comfort_Premium = 0  [Reference]
Comfort = 1 (Seated)   → Comfort_Seated = 1, Comfort_Premium = 0
Comfort = 2 (Premium)  → Comfort_Seated = 0, Comfort_Premium = 1
```

**Interpretation:**
- β_Comfort_Seated = utility difference between Seated and Standing
- β_Comfort_Premium = utility difference between Premium and Standing

**R code:**
```r
data$Comfort_Seated <- ifelse(data$Comfort == 1, 1, 0)
data$Comfort_Premium <- ifelse(data$Comfort == 2, 1, 0)
```

#### Effect Coding (Symmetric Around Zero)

```
Comfort = 0 (Standing) → Comfort_Seated = -1, Comfort_Premium = -1
Comfort = 1 (Seated)   → Comfort_Seated =  1, Comfort_Premium =  0
Comfort = 2 (Premium)  → Comfort_Seated =  0, Comfort_Premium =  1
```

**Interpretation:**
- β_Comfort_Seated = utility difference between Seated and average of all levels
- Preferred when no natural reference category

**When to use which:**
- **Dummy coding:** When one category is a clear baseline (e.g., "No service" vs. service options)
- **Effect coding:** When all categories are equally important (e.g., route colors)

### Panel Data Structure

**Panel:** Multiple observations (tasks) from same respondent

**Key identifier:** `RespID` or `obs_id`

**Why it matters:**
- Error terms are correlated within respondents
- Need to adjust standard errors (cluster by respondent)
- Enables random parameters (taste heterogeneity)

**Biogeme Panel Specification:**
```python
# Indicate panel structure
database = db.Database("data_long", data)
database.panel("RespID")  # Tell Biogeme to cluster by RespID
```

**Apollo Panel Specification:**
```r
# Define panel structure
apollo_control = list(
  modelName = "MNL_Model",
  panelData = TRUE,
  indivID = "RespID"
)
```

---

## 🧮 Multinomial Logit (MNL) Models

### Theory Refresher

**Utility Function:**
```
U_ni = V_ni + ε_ni
     = β'X_ni + ε_ni
```

Where:
- `U_ni` = utility of alternative `i` for person `n`
- `V_ni` = systematic component (observable)
- `ε_ni` = random component (unobservable)

**Choice Probability (Logit Formula):**
```
P_ni = exp(V_ni) / Σ_j exp(V_nj)
```

**Assumptions:**
1. Error terms are IID Gumbel (Type I Extreme Value)
2. Independence of Irrelevant Alternatives (IIA)
3. Homogeneous preferences across population

### Utility Specification Example

**Mode Choice:** Bus, Rail, Drive

```
V_bus  = ASC_bus + β_cost * Cost_bus + β_time * Time_bus + β_freq * Frequency_bus
V_rail = ASC_rail + β_cost * Cost_rail + β_time * Time_rail + β_freq * Frequency_rail
V_drive = 0  [normalized to zero for identification]
```

**Key Principles:**

1. **Alternative-Specific Constants (ASC):**
   - Capture average preference for mode, all else equal
   - One alternative must be normalized to 0 for identification
   - Interpretation: "People prefer bus over driving by X utils, ceteris paribus"

2. **Generic Coefficients:**
   - Same parameter across alternatives (e.g., β_cost)
   - Assumes one dollar costs the same regardless of mode
   - More efficient (fewer parameters)

3. **Alternative-Specific Coefficients:**
   - Different parameters by alternative (e.g., β_time_bus, β_time_rail)
   - Allows flexibility (transit time may be valued differently than drive time)
   - Requires more data

### Biogeme Estimation: Step-by-Step

**Step 1: Import Libraries**

```python
import pandas as pd
import biogeme.database as db
import biogeme.biogeme as bio
import biogeme.models as models
from biogeme.expressions import Beta, Variable
```

**Step 2: Load Data**

```python
# Read dataset
data = pd.read_csv("transit_choice_long.csv")

# Create Biogeme database
database = db.Database("TransitData", data)
database.panel("RespID")  # Panel structure

# Define variables
Choice = Variable('Choice')
Price = Variable('Price')
Time = Variable('Time')
Frequency = Variable('Frequency')
Comfort = Variable('Comfort')
AltID = Variable('AltID')  # 1=Bus, 2=Rail, 3=Drive
```

**Step 3: Define Parameters**

```python
# Parameters to be estimated (name, initial value, lower bound, upper bound, status)
ASC_bus = Beta('ASC_bus', 0, None, None, 0)
ASC_rail = Beta('ASC_rail', 0, None, None, 0)
ASC_drive = Beta('ASC_drive', 0, None, None, 1)  # Fixed to 0 for identification

B_cost = Beta('B_cost', 0, None, None, 0)
B_time = Beta('B_time', 0, None, None, 0)
B_frequency = Beta('B_frequency', 0, None, None, 0)
B_comfort = Beta('B_comfort', 0, None, None, 0)
```

**Parameters:**
- First argument: name (string)
- Second: starting value
- Third/Fourth: bounds (None = no bound)
- Fifth: status (0 = estimate, 1 = fix to starting value)

**Step 4: Specify Utility Functions**

```python
# Utility functions
V_bus = (ASC_bus +
         B_cost * Price +
         B_time * Time +
         B_frequency * Frequency +
         B_comfort * Comfort) * (AltID == 1)

V_rail = (ASC_rail +
          B_cost * Price +
          B_time * Time +
          B_frequency * Frequency +
          B_comfort * Comfort) * (AltID == 2)

V_drive = (ASC_drive +
           B_cost * Price +
           B_time * Time) * (AltID == 3)

# Collect in dictionary
V = {1: V_bus, 2: V_rail, 3: V_drive}

# Availability (all alternatives always available)
av = {1: 1, 2: 1, 3: 1}
```

**Step 5: Define and Estimate Model**

```python
# Logit probability
logprob = models.loglogit(V, av, Choice)

# Create Biogeme object
biogeme = bio.BIOGEME(database, logprob)
biogeme.modelName = "MNL_Transit"

# Estimate
results = biogeme.estimate()

# Display results
print(results.shortSummary())
print(results.getEstimatedParameters())
```

**Step 6: Interpret Output**

```
Results for model MNL_Transit
Number of observations: 4800
Number of individuals: 600
Final log likelihood: -2,847.32
Rho-squared: 0.285
Rho-squared-bar: 0.281

Coefficients:
                  Value   Std err  t-stat  p-value
ASC_bus           0.342    0.156    2.19    0.028
ASC_rail         -0.128    0.142   -0.90    0.367
B_cost           -0.082    0.012   -6.83    0.000
B_time           -0.034    0.006   -5.67    0.000
B_frequency       0.025    0.008    3.13    0.002
B_comfort         0.612    0.089    6.88    0.000
```

**Interpretation:**

- **ASC_bus = 0.342:** People prefer bus over drive by 0.342 utils (all else equal), significant at 5% level
- **ASC_rail = -0.128:** Rail is slightly less preferred than drive, but not significant (p=0.367)
- **B_cost = -0.082:** For every $1 increase in cost, utility decreases by 0.082 utils
- **B_time = -0.034:** For every 1-minute increase in travel time, utility decreases by 0.034 utils
- **B_frequency = 0.025:** More frequent service (shorter headway) increases utility
- **B_comfort = 0.612:** Comfortable seating adds 0.612 utils vs. standing

**Model Fit:**
- **Rho-squared = 0.285:** Analogous to R² in regression; 28.5% of variance explained
- **Rho-squared-bar = 0.281:** Adjusted for number of parameters (penalizes complexity)

### Apollo Estimation: Step-by-Step

**Step 1: Setup**

```r
# Load libraries
library(apollo)

# Load data
database <- read.csv("transit_choice_long.csv")

# Define core settings
apollo_initialise()

apollo_control = list(
  modelName = "MNL_Transit",
  modelDescr = "Transit mode choice MNL",
  indivID = "RespID",
  panelData = TRUE,
  outputDirectory = "output/"
)
```

**Step 2: Define Parameters**

```r
apollo_beta = c(
  asc_bus = 0,
  asc_rail = 0,
  b_cost = 0,
  b_time = 0,
  b_frequency = 0,
  b_comfort = 0
)

# Fix ASC for drive (identification)
apollo_fixed = c("asc_drive")
```

**Step 3: Validate Data**

```r
apollo_inputs = apollo_validateInputs()
```

**Step 4: Define Utility Functions**

```r
apollo_probabilities = function(apollo_beta, apollo_inputs, functionality="estimate") {

  # Attach inputs and parameters
  apollo_attach(apollo_beta, apollo_inputs)
  on.exit(apollo_detach(apollo_beta, apollo_inputs))

  # Create list of probabilities
  P = list()

  # Define utilities
  V = list()
  V[['bus']]  = asc_bus + b_cost * Price + b_time * Time +
                b_frequency * Frequency + b_comfort * Comfort
  V[['rail']] = asc_rail + b_cost * Price + b_time * Time +
                b_frequency * Frequency + b_comfort * Comfort
  V[['drive']] = 0 + b_cost * Price + b_time * Time

  # Define availability (all alternatives available)
  avail = list(bus=1, rail=1, drive=1)

  # Define settings for MNL model
  mnl_settings = list(
    alternatives = c(bus=1, rail=2, drive=3),
    avail = avail,
    choiceVar = Choice,
    V = V
  )

  # Calculate probabilities
  P[['model']] = apollo_mnl(mnl_settings, functionality)

  # Take product across observations for same individual
  P = apollo_panelProd(P, apollo_inputs, functionality)

  # Prepare and return outputs
  P = apollo_prepareProb(P, apollo_inputs, functionality)
  return(P)
}
```

**Step 5: Estimate Model**

```r
# Estimate
model = apollo_estimate(apollo_beta, apollo_fixed, apollo_probabilities, apollo_inputs)

# Print results
apollo_modelOutput(model)

# Save results
apollo_saveOutput(model)
```

**Step 6: Output**

```
Model run by R using Apollo 0.2.8
Model name      : MNL_Transit
Model description : Transit mode choice MNL
Estimation method : bfgs
Number of individuals: 600
Number of observations: 4800

Final log-likelihood: -2847.32
Rho-square: 0.285
Adj.Rho-square: 0.281

Estimates:
              Estimate  s.e.  t.rat.(0)  p(2-sided)
asc_bus         0.342  0.156      2.19      0.0284
asc_rail       -0.128  0.142     -0.90      0.3674
b_cost         -0.082  0.012     -6.83      0.0000
b_time         -0.034  0.006     -5.67      0.0000
b_frequency     0.025  0.008      3.13      0.0018
b_comfort       0.612  0.089      6.88      0.0000
```

---

## 🔄 Advanced Model Specifications

### Mixed Logit (Random Parameters)

**Motivation:** Capture taste heterogeneity

**Idea:** Allow parameters to vary across individuals (random coefficients)

**Specification:**

```
β_n = β_mean + σ * v_n

where:
- β_mean = population mean
- σ = standard deviation
- v_n ~ N(0,1) or other distribution
```

**Example:** Random cost sensitivity

```
β_cost_n ~ Normal(β_cost_mean, σ_cost)
```

**Biogeme Mixed Logit:**

```python
from biogeme.expressions import Beta, bioDraws

# Define parameters
B_cost_mean = Beta('B_cost_mean', 0, None, None, 0)
B_cost_std = Beta('B_cost_std', 1, None, None, 0)

# Define random parameter
B_cost_random = B_cost_mean + B_cost_std * bioDraws('B_cost_random', 'NORMAL')

# Utility with random parameter
V_bus = (ASC_bus +
         B_cost_random * Price +  # Random!
         B_time * Time +
         B_frequency * Frequency +
         B_comfort * Comfort) * (AltID == 1)

# Mixed logit probability
logprob = models.loglogit(V, av, Choice)

# Monte Carlo integration
prob = models.mixedloglogit(logprob, bioDraws('B_cost_random', 'NORMAL'), 1000)

biogeme = bio.BIOGEME(database, prob)
biogeme.modelName = "MixedLogit_Transit"

results = biogeme.estimate()
print(results.shortSummary())
```

**Output Interpretation:**

```
B_cost_mean = -0.082 (s.e. 0.014)  ← Average cost sensitivity
B_cost_std  =  0.045 (s.e. 0.008)  ← Heterogeneity

Interpretation:
- 68% of population has β_cost between -0.127 and -0.037
- 95% of population has β_cost between -0.172 and +0.008
- Some individuals are almost cost-insensitive!
```

**Apollo Mixed Logit:**

```r
# Define random parameters
apollo_randCoeff = function(apollo_beta, apollo_inputs) {
  randcoeff = list()

  # Random cost parameter (normal distribution)
  randcoeff[["b_cost_random"]] = b_cost_mean + b_cost_std * draws_cost

  return(randcoeff)
}

# Modify apollo_probabilities to use random coefficient
V[['bus']] = asc_bus + b_cost_random * Price + b_time * Time + ...

# Set up mixing
apollo_inputs$apollo_draws = list(
  interDrawsType = "mlhs",  # Modified Latin Hypercube Sampling
  interNDraws = 500,  # Number of draws
  interNormDraws = c("draws_cost")
)

# Estimate
model_mixed = apollo_estimate(apollo_beta, apollo_fixed, apollo_probabilities, apollo_inputs)
```

### Nested Logit

**Motivation:** Relax IIA assumption by grouping similar alternatives

**Example:** Motorized (Bus, Rail, Car) vs. Non-Motorized (Bike, Walk)

**Structure:**

```
           Root
          /     \
    Motorized  Non-Motorized
     / | \        /    \
  Bus Rail Car  Bike  Walk
```

**Nesting Parameter (λ):**
- λ = 1: Reduces to MNL (no nesting)
- 0 < λ < 1: Positive correlation within nest
- λ → 0: Perfect correlation (alternatives in nest are identical)

**Biogeme Nested Logit:**

```python
# Define nesting structure
motorized_nest = 1.0, [1, 2, 3]  # (λ, [Bus, Rail, Car])
non_motorized_nest = 1.0, [4, 5]  # (λ, [Bike, Walk])

nests = {0: motorized_nest, 1: non_motorized_nest}

# Nested logit probability
logprob = models.lognested(V, av, nests, Choice)

biogeme = bio.BIOGEME(database, logprob)
results = biogeme.estimate()
```

**Output:**

```
Nesting parameter (motorized): 0.68 (s.e. 0.12)

Interpretation:
- λ < 1 confirms correlation within motorized modes
- Violations of IIA are partially addressed
- Substitution patterns more realistic
```

### Latent Class Models

**Motivation:** Capture discrete heterogeneity (market segments)

**Idea:** Population consists of C latent classes with different preferences

**Specification:**

```
P(choice) = Σ_c π_c * P(choice | class c)

where:
- π_c = probability of belonging to class c
- Σ π_c = 1
```

**Example:** Two classes (Cost-Sensitive vs. Time-Sensitive)

```
Class 1 (Cost-Sensitive): Large β_cost, small β_time
Class 2 (Time-Sensitive): Small β_cost, large β_time
```

**Apollo Latent Class:**

```r
apollo_beta = c(
  # Class 1 parameters
  asc_bus_c1 = 0,
  b_cost_c1 = 0,
  b_time_c1 = 0,

  # Class 2 parameters
  asc_bus_c2 = 0,
  b_cost_c2 = 0,
  b_time_c2 = 0,

  # Class allocation (constant + covariates)
  delta_class2 = 0  # Constant for class 2 membership
)

apollo_lcPars = function(apollo_beta, apollo_inputs) {
  lcpars = list()

  # Class allocation probabilities
  lcpars[["pi_c1"]] = 1 / (1 + exp(delta_class2))
  lcpars[["pi_c2"]] = exp(delta_class2) / (1 + exp(delta_class2))

  # Class-specific parameters
  lcpars[["b_cost"]] = list(b_cost_c1, b_cost_c2)
  lcpars[["b_time"]] = list(b_time_c1, b_time_c2)

  return(lcpars)
}

# Estimate
model_lc = apollo_estimate(apollo_beta, apollo_fixed, apollo_probabilities, apollo_inputs)
```

**Output:**

```
Class Membership:
Class 1: 62% (Cost-Sensitive)
Class 2: 38% (Time-Sensitive)

Parameters:
              Class 1   Class 2
b_cost        -0.142    -0.031
b_time        -0.021    -0.068

Interpretation:
- Class 1 is 4.6x more sensitive to cost
- Class 2 is 3.2x more sensitive to time
- Clear market segmentation
```

---

## 📈 Model Selection & Diagnostics

### Likelihood Ratio Test

**Purpose:** Test if adding parameters significantly improves fit

**Formula:**

```
LR = -2 * (LL_restricted - LL_unrestricted)
LR ~ χ²(df = difference in # parameters)
```

**Example:**

```
Model 1 (MNL): LL = -2,847.32, K = 6 parameters
Model 2 (Mixed Logit): LL = -2,782.15, K = 8 parameters

LR = -2 * (-2847.32 - (-2782.15)) = -2 * (-65.17) = 130.34
df = 8 - 6 = 2

Critical value (α=0.05, df=2): χ²(2) = 5.99

Decision: 130.34 > 5.99 → Reject null → Mixed Logit significantly better
```

**R code:**

```r
lr_test <- function(ll_restricted, ll_unrestricted, df) {
  lr_stat <- -2 * (ll_restricted - ll_unrestricted)
  p_value <- 1 - pchisq(lr_stat, df)

  cat("LR statistic:", lr_stat, "\n")
  cat("Degrees of freedom:", df, "\n")
  cat("p-value:", p_value, "\n")

  if (p_value < 0.05) {
    cat("Result: Reject null hypothesis (unrestricted model is significantly better)\n")
  } else {
    cat("Result: Fail to reject null hypothesis (no significant improvement)\n")
  }
}

lr_test(-2847.32, -2782.15, 2)
```

### Information Criteria

#### AIC (Akaike Information Criterion)

```
AIC = -2 * LL + 2 * K
```

Lower is better. Penalizes model complexity.

#### BIC (Bayesian Information Criterion)

```
BIC = -2 * LL + K * log(N)
```

Lower is better. Stronger penalty for complexity than AIC.

**Example:**

```
Model          LL         K    N      AIC        BIC
MNL         -2847.32    6   4800   5706.64    5747.23
Mixed Logit -2782.15    8   4800   5580.30    5634.22
Nested Logit -2795.48   7   4800   5604.96    5652.21

Best by AIC: Mixed Logit (5580.30)
Best by BIC: Mixed Logit (5634.22)
```

**Rule of Thumb:**
- ΔAIC or ΔBIC < 2: Models are equivalent
- 2-6: Some evidence for better model
- 6-10: Strong evidence
- >10: Very strong evidence

### Predictive Accuracy

**Hit Rate (% Correct Predictions):**

```r
# Apollo: Calculate predictions
predictions <- apollo_prediction(model, apollo_probabilities, apollo_inputs)

# Get predicted choice (highest probability)
predicted_choice <- apply(predictions, 1, which.max)
actual_choice <- database$Choice

# Hit rate
hit_rate <- mean(predicted_choice == actual_choice)
cat("Hit rate:", round(hit_rate * 100, 1), "%\n")
```

**Typical Results:**
- Random guess (3 alternatives): 33.3%
- Constants only: ~45%
- Good MNL: 55-65%
- Excellent Mixed Logit: 65-75%

**Note:** Hit rate alone is not sufficient—can be high even with poor model if one alternative dominates.

### Parameter Sign and Significance

**Expected Signs:**

| Variable | Expected Sign | Rationale |
|----------|---------------|-----------|
| Cost | Negative (-) | Higher cost reduces utility |
| Travel time | Negative (-) | Longer time reduces utility |
| Frequency (headway) | Positive (+) | More frequent = higher utility |
| Comfort | Positive (+) | Better comfort = higher utility |
| Reliability | Positive (+) | On-time performance increases utility |

**T-statistic Interpretation:**

```
|t-stat| < 1.96: Not significant at 5% level
|t-stat| ≥ 1.96: Significant at 5% level (p < 0.05)
|t-stat| ≥ 2.58: Significant at 1% level (p < 0.01)
```

**Warning Signs:**
- Wrong sign (e.g., positive cost coefficient)
- Very large standard errors (estimation problems)
- Counterintuitive magnitudes

---

## 💰 Policy-Relevant Calculations

### Willingness to Pay (WTP)

**Definition:** Amount willing to pay for one-unit improvement in attribute

**Formula:**

```
WTP_attribute = -β_attribute / β_cost
```

**Example:**

From earlier model:
- β_time = -0.034
- β_cost = -0.082

```
WTP_time = -(-0.034) / (-0.082) = 0.034 / 0.082 = $0.41 per minute

Or: $24.60 per hour
```

**Interpretation:** Travelers value a 1-minute time saving at $0.41 (or $24.60/hour).

**Confidence Interval (Delta Method):**

```r
# R code for WTP with standard error
library(msm)

# Define WTP function
wtp_time <- function(params) {
  -params["b_time"] / params["b_cost"]
}

# Calculate WTP and SE
wtp_estimate <- wtp_time(model$estimate)
wtp_se <- deltamethod(~ -x1/x2,
                      coef(model)[c("b_time", "b_cost")],
                      vcov(model)[c("b_time", "b_cost"), c("b_time", "b_cost")])

# 95% CI
wtp_ci_lower <- wtp_estimate - 1.96 * wtp_se
wtp_ci_upper <- wtp_estimate + 1.96 * wtp_se

cat("Value of Time:", round(wtp_estimate * 60, 2), "$/hour\n")
cat("95% CI: [", round(wtp_ci_lower * 60, 2), ",", round(wtp_ci_upper * 60, 2), "] $/hour\n")
```

**Output:**
```
Value of Time: $24.60/hour
95% CI: [$19.20, $30.00] $/hour
```

### Elasticities

**Point Elasticity:**

```
E_ij = (∂P_i / ∂x_j) * (x_j / P_i)
```

Where:
- E_ij = elasticity of choice probability P_i with respect to attribute x_j
- Positive = increase in x_j increases P_i (own-elasticity if i=j)
- Negative = increase in x_j decreases P_i (cross-elasticity if i≠j)

**Logit Elasticity Formula:**

```
E_ij (own) = β_j * x_j * (1 - P_i)
E_ij (cross) = -β_j * x_j * P_j
```

**Example:**

Given:
- β_price = -0.082
- Current price for bus = $3.50
- Current bus probability = 0.42

```
Own-price elasticity (bus):
E_bus,price = -0.082 * 3.50 * (1 - 0.42) = -0.082 * 3.50 * 0.58 = -0.166

Interpretation: 1% increase in bus price → 0.166% decrease in bus choice probability
```

**Python Code:**

```python
def calculate_elasticity(beta, attribute_value, prob_i, own=True):
    """
    Calculate elasticity.

    Parameters:
    beta: coefficient estimate
    attribute_value: current value of attribute
    prob_i: choice probability
    own: True for own-elasticity, False for cross-elasticity
    """
    if own:
        elasticity = beta * attribute_value * (1 - prob_i)
    else:
        elasticity = -beta * attribute_value * prob_i

    return elasticity

# Example
beta_price = -0.082
current_price = 3.50
prob_bus = 0.42

own_elast = calculate_elasticity(beta_price, current_price, prob_bus, own=True)
print(f"Own-price elasticity: {own_elast:.3f}")

# Cross-price elasticity (bus vs. rail)
prob_rail = 0.28
cross_elast = calculate_elasticity(beta_price, current_price, prob_rail, own=False)
print(f"Cross-price elasticity: {cross_elast:.3f}")
```

### Scenario Analysis

**Purpose:** Predict market shares under policy scenarios

**Process:**

1. Estimate model on baseline data
2. Create scenario dataset (modify attribute values)
3. Calculate predicted probabilities
4. Aggregate to market shares

**Example:** Forecast impact of 20% fare reduction

**Apollo Code:**

```r
# Create baseline scenario
baseline <- database

# Create policy scenario (20% fare reduction for bus)
scenario <- baseline
scenario$Price[scenario$AltID == 1] <- scenario$Price[scenario$AltID == 1] * 0.80

# Predict probabilities
predictions_baseline <- apollo_prediction(model, apollo_probabilities,
                                          apollo_inputs, database = baseline)
predictions_scenario <- apollo_prediction(model, apollo_probabilities,
                                          apollo_inputs, database = scenario)

# Calculate market shares
shares_baseline <- colMeans(predictions_baseline)
shares_scenario <- colMeans(predictions_scenario)

# Compare
comparison <- data.frame(
  Alternative = c("Bus", "Rail", "Drive"),
  Baseline = round(shares_baseline * 100, 1),
  Scenario = round(shares_scenario * 100, 1),
  Change_pct = round((shares_scenario - shares_baseline) * 100, 1)
)

print(comparison)
```

**Output:**

```
  Alternative  Baseline  Scenario  Change_pct
1        Bus      42.0      48.5        +6.5
2       Rail      28.0      26.2        -1.8
3      Drive      30.0      25.3        -4.7
```

**Interpretation:**
- 20% bus fare reduction increases bus share from 42% to 48.5%
- Draws riders from both rail (-1.8 pp) and drive (-4.7 pp)
- Total ridership gain: +6.5 percentage points

---

## 🌍 Real-World Case Studies

### Case Study 1: London Crossrail Value of Time Study

**Context:** Estimate time savings benefits for £18 billion rail project

**Data:**
- n = 3,200 commuters
- 8 SP tasks per respondent
- Attributes: Travel time, cost, frequency, crowding, reliability

**Model Specification:**
- Mixed logit with random time and cost parameters
- Segmented by trip purpose (commute vs. business vs. leisure)
- Included current mode as covariate

**Key Results:**

```
Value of Time (£/hour):
  Commute:  £15.20 (95% CI: £13.50 - £16.90)
  Business: £34.80 (95% CI: £31.20 - £38.40)
  Leisure:  £ 8.40 (95% CI: £ 7.10 - £ 9.70)

Value of Reliability (£/hour of saved standard deviation):
  £12.60 (95% CI: £10.80 - £14.40)

Crowding Multiplier:
  Standing vs. Seated: 1.8x time weight
```

**Policy Application:**
- Annual time savings: £850 million (using VoT estimates)
- Reliability benefits: £280 million
- Total benefits justified investment
- Used in cost-benefit analysis submitted to Parliament

**Methodological Innovations:**
- Pivot design around respondent's current trip
- Video-based scenarios (showed crowding levels)
- Validation against revealed preference data (ticket sales)

### Case Study 2: California High-Speed Rail Demand Forecasting

**Context:** Predict ridership for SF-LA high-speed rail

**Data:**
- n = 5,500 inter-city travelers
- Modes: HSR, Air, Drive, Conventional rail
- 12 choice tasks per respondent

**Model Evolution:**

**Model 1: Basic MNL**
- LL = -8,245
- Rho-squared = 0.22
- Predicted HSR share: 28%

**Model 2: Nested Logit (Rail nest)**
- LL = -8,102
- Rho-squared = 0.24
- Nesting parameter: 0.71 (sig.)
- Predicted HSR share: 31%

**Model 3: Mixed Logit (Random time/cost)**
- LL = -7,886
- Rho-squared = 0.29
- Predicted HSR share: 34%

**Model 4: Latent Class (3 classes)**
- LL = -7,720
- Rho-squared = 0.32
- Classes:
  - Cost-sensitive (42%): HSR share 18%
  - Balanced (38%): HSR share 42%
  - Time-sensitive (20%): HSR share 51%
- Weighted HSR share: 33%

**Final Recommendation:** Mixed logit (Model 3)
- Best statistical fit
- Interpretable heterogeneity
- Conservative ridership forecast

**Sensitivity Analysis:**

```
Scenario                          HSR Share
Base case                              34%
+10% fare                              29%
-10% fare                              39%
+15 min travel time                    28%
-15 min travel time                    41%
Frequency: 1/hr → 2/hr                 37%
```

**Lesson Learned:** Small changes in assumptions yield large ridership changes—present range of scenarios rather than single point estimate.

### Case Study 3: E-Scooter Regulation in Portland

**Context:** Design parking and speed regulations for e-scooters

**Data:**
- n = 850 residents
- 3 alternatives per task: Permit scooters, Restrict scooters, Ban scooters
- Attributes:
  - Parking rules (designated racks, sidewalk, anywhere)
  - Speed limit (8 mph, 12 mph, 15 mph)
  - Helmet requirement (yes/no)
  - Operating hours (24/7, daylight only)
  - Monthly fee ($1, $2, $5)

**Model:** MNL with interaction terms

**Key Coefficients:**

```
                                    Coef.   t-stat
ASC_permit (vs. ban)                0.82     3.4
ASC_restrict (vs. ban)              0.45     2.1

Parking: Designated racks           0.54     4.2
Parking: Sidewalk                  -0.31    -2.8

Speed: 15 mph (vs. 8 mph)          -0.68    -5.1
Speed: 12 mph (vs. 8 mph)          -0.22    -1.9

Helmet required                    -0.19    -1.4  (n.s.)
Operating: 24/7 (vs. daylight)      0.33     2.6
Monthly fee ($/month)              -0.14    -6.2

Interaction: Age>55 × ASC_permit   -0.48    -2.3
Interaction: Cyclist × Speed15      0.42     2.1
```

**Insights:**

1. **Strong preference for designated parking:**
   - Reduces sidewalk clutter concerns
   - Increases permit support from 52% to 68%

2. **Speed limits matter:**
   - 15 mph reduces support significantly
   - 8 mph speed limit increases permit support by 12 pp
   - Cyclists more tolerant of higher speeds

3. **Helmet requirement:**
   - Not statistically significant
   - Small negative effect suggests not a dealbreaker

4. **Heterogeneity:**
   - Seniors much less supportive (interaction term = -0.48)
   - Existing cyclists more supportive of liberal rules

**Policy Recommendations Adopted:**
- Designated parking zones (not free-floating)
- 10 mph speed limit in downtown, 15 mph elsewhere
- No helmet requirement (to avoid usage barrier)
- 24/7 operations permitted
- $2/month public space fee

**Outcome:**
- Policy implemented in 2020
- 72% public approval (vs. 52% predicted under alternative design)
- E-scooter usage 3x higher than comparable cities with stricter rules

---

## ⚙️ Session Breakdown

### Session 1: Data Prep & MNL Estimation (4 hours)

**Part 1: Data Wrangling Workshop (90 min)**

**Activity:** Transform wide survey export to long estimation format

**Provided:**
- Sample survey export (n=100, 8 tasks each)
- Data dictionary

**Tasks:**
1. Reshape wide to long (R or Python)
2. Create dummy variables for categorical attributes
3. Add panel identifiers
4. Export estimation-ready CSV

**Troubleshooting Clinic:**
- Common reshaping errors
- Missing data handling
- Variable naming conventions

**Part 2: Biogeme Walkthrough (90 min)**

**Live Coding:**
1. Load data
2. Define variables and parameters
3. Specify utility functions
4. Estimate MNL
5. Interpret output

**Students follow along** in Jupyter notebook or Google Colab

**Part 3: Model Interpretation Exercise (60 min)**

**Scenario:** Transit pricing study

**Output provided:**
```
ASC_bus:    0.45 (s.e. 0.18)
ASC_rail:   0.22 (s.e. 0.16)
b_cost:    -0.09 (s.e. 0.015)
b_time:    -0.04 (s.e. 0.008)
b_frequency: 0.03 (s.e. 0.010)
```

**Questions:**
1. Which coefficients are significant at 5% level?
2. Calculate value of time (VoT)
3. If bus fare increases from $2.50 to $3.00, predict directional change in bus share
4. Is the model economically sensible?

**Group discussion and debrief**

### Session 2: Advanced Models & Policy Analysis (4 hours)

**Part 1: Mixed Logit Demonstration (60 min)**

**Instructor estimates:**
- Base MNL
- Mixed logit with random cost parameter
- Compare LL, AIC, BIC
- Discuss convergence issues

**Part 2: Model Selection Tournament (90 min)**

**Challenge:** Given a dataset, estimate 3+ models and select the best

**Data provided:** Ride-hailing choice (Uber, Lyft, Taxi, Transit)

**Required models:**
1. MNL (baseline)
2. At least one advanced specification (mixed logit, nested logit, or latent class)
3. Model with interaction terms

**Teams present:**
- Model comparison table
- Recommended model with justification
- One policy insight

**Judging criteria:**
- Statistical fit (30%)
- Interpretation clarity (30%)
- Policy relevance (40%)

**Part 3: WTP & Scenario Analysis Lab (90 min)**

**Exercise:** Calculate policy impacts

**Tasks:**

**Task 1: Willingness to Pay (30 min)**
- Calculate VoT with confidence intervals
- Calculate WTP for comfort improvement
- Interpret magnitudes (are they reasonable?)

**Task 2: Elasticities (30 min)**
- Own-price elasticity for each alternative
- Cross-price elasticity matrix
- Identify closest substitutes

**Task 3: Scenario Forecasting (30 min)**
- Baseline market shares
- Policy scenario: +$1 transit fare
- Calculate change in shares
- Revenue impact analysis

**Deliverable:** One-page policy memo with recommendations

---

## 🔬 Lab Activities

### Activity 1: Model Diagnostics Workshop (90 minutes)

**Objective:** Identify and fix common modeling problems

**Provided:** 3 "broken" model outputs (students don't see data or syntax)

**Model A: Sign Problems**
```
b_cost:  0.05 (s.e. 0.02)  ← WRONG SIGN!
b_time: -0.03 (s.e. 0.01)
```

**Diagnosis:**
- Positive cost coefficient is implausible
- Likely coding error (cost entered as negative?) or multicollinearity

**Fix:**
- Check data: Are costs coded correctly?
- Check correlation: Is cost highly correlated with another variable?
- Re-specify or transform variables

**Model B: Non-Convergence**
```
Estimation stopped after 1000 iterations
Final LL = -5,245.32
Gradient norm = 12.5 (threshold: 0.01)
Message: Maximum iterations reached
```

**Diagnosis:**
- Model didn't converge
- Gradient still large

**Fix:**
- Increase max iterations
- Try different starting values
- Simplify model (remove parameters)
- Check for perfect multicollinearity

**Model C: Unrealistic Magnitudes**
```
ASC_bus:  15.2 (s.e. 3.4)
b_cost:   -0.002 (s.e. 0.001)
b_time:   -0.001 (s.e. 0.0005)
```

**Diagnosis:**
- Huge ASC suggests scaling issue
- Tiny coefficients suggest units problem

**Fix:**
- Check units: Are costs in cents instead of dollars?
- Rescale attributes (divide by 100)
- Re-estimate

**Activity:** Students diagnose, propose solutions, then see actual data/syntax to confirm

### Activity 2: Code Review & Debugging (60 minutes)

**Objective:** Debug Biogeme/Apollo syntax errors

**Scenario:** Junior analyst's code won't run

**Task:** Fix the errors and get model to estimate

**Buggy Biogeme Code:**

```python
# ERROR 1: Undefined variable
V_bus = ASC_bus + b_cost * Cost + b_time * TravelTime  # TravelTime not defined in database

# ERROR 2: Wrong availability syntax
av = {1: 1, 2: 1}  # Missing alternative 3

# ERROR 3: Wrong Choice variable
logprob = models.loglogit(V, av, choice)  # Should be Choice (case-sensitive)

# ERROR 4: Panel not specified
# database.panel() not called, but multiple observations per person
```

**Students:**
1. Identify all errors
2. Fix syntax
3. Run model
4. Verify output is reasonable

**Debrief:** Common mistakes and debugging strategies

---

## 📝 Assignment

### [Module 5 Modeling Memo](../assignments/05_modeling_memo.md)

**Objective:** Estimate choice models and deliver policy-ready insights

**Components:**

**1. Data Description (2 pages)**
- Sample characteristics (n, demographics)
- Choice frequencies by alternative
- Descriptive statistics for key attributes
- Missing data and quality filters applied

**2. Model Estimation (5-7 pages)**

Estimate and report:

**a) Base MNL Model**
- Full parameter table (estimates, s.e., t-stats)
- Model fit statistics (LL, Rho-sq, AIC, BIC)
- Interpretation of key coefficients

**b) At Least Two Advanced Models:**
- Mixed logit, nested logit, latent class, or with interactions
- Comparison table across all models
- Likelihood ratio tests or AIC/BIC comparison
- Recommended model with justification

**3. Policy Analysis (3-4 pages)**

Calculate and present:

**a) Willingness to Pay:**
- Value of time ($/hour) with 95% CI
- WTP for other key attributes
- Comparison to literature benchmarks

**b) Elasticities:**
- Own-price elasticities for all alternatives
- At least one cross-price elasticity
- Interpretation for policy

**c) Scenario Analysis:**
- Define 2-3 policy scenarios
- Predict market share changes
- Revenue or welfare impacts (if applicable)

**4. Code Appendix**
- All estimation code (Biogeme or Apollo)
- Data cleaning scripts (R or Python)
- Scenario analysis code
- Well-commented and reproducible

**Submission Requirements:**
- Main report: PDF, 12-15 pages
- Code appendix: .py or .R files + README
- Dataset: CSV file (or link if large)
- Filename: `M5_modeling_memo_<lastname>.pdf`
- **Due:** End of Week 10

**Evaluation Rubric (100 points):**

| Component | Points | Criteria |
|-----------|--------|----------|
| Data description | 15 | Clear summary, appropriate visualizations, quality checks documented |
| Model estimation | 35 | Correct specification, proper syntax, multiple models compared, justified selection |
| Policy analysis | 30 | Accurate WTP/elasticities, realistic scenarios, clear interpretation |
| Code quality | 10 | Reproducible, well-commented, follows best practices |
| Communication | 10 | Professional writing, clear tables/figures, actionable insights |

---

## 💬 Discussion Prompts

**Post your responses on the course forum (200-250 words each; respond to 2 peers):**

### Prompt 1: Model Complexity Trade-off

**Question:**
"When does model complexity hinder communication with non-technical stakeholders? Give an example where you'd choose a simpler model over a statistically superior complex model."

**Consider:**
- Interpretability vs. fit trade-off
- Stakeholder sophistication
- Decision context (exploratory vs. high-stakes)
- Time/resource constraints

**Example:** "A latent class model with 4 classes has better AIC than MNL, but explaining market segments to a city council might be challenging..."

### Prompt 2: RP-SP Data Integration

**Question:**
"How can we combine RP (revealed preference) and SP data to improve predictive accuracy without overfitting? What are the practical challenges?"

**Issues to address:**
- Scale differences between RP and SP
- Data fusion techniques
- Validation strategies
- When RP alone is sufficient

**Cite:** At least one paper on RP-SP integration methods

### Prompt 3: Value of Time Validation

**Question:**
"You estimated a value of time of $45/hour for commuters, but median income in your sample is $28/hour. How do you explain this to a skeptical client? Is the estimate valid?"

**Discuss:**
- Theoretical vs. empirical VoT
- Context-specific variation (work vs. leisure)
- Hypothetical bias in SP
- Comparison to other studies

---

## 📖 Recommended Resources

### Core Textbooks

1. **Train, K. (2009).** *Discrete Choice Methods with Simulation* (2nd ed.)
   - Chapters 3-8: MNL, nested logit, mixed logit, simulation
   - **THE** reference for choice modeling
   - [Free PDF](https://eml.berkeley.edu/books/choice2.html)

2. **Hensher, D. A., Rose, J. M., & Greene, W. H. (2015).** *Applied Choice Analysis* (2nd ed.)
   - Practical focus with software examples
   - Chapters 8-12: Model specification and estimation
   - Companion datasets available

3. **Ben-Akiva, M., & Lerman, S. R. (1985).** *Discrete Choice Analysis*
   - Classic foundational text
   - Mathematical rigor
   - Chapters 5-7 for this module

### Software Documentation

- **Biogeme Documentation**
  [https://biogeme.epfl.ch/](https://biogeme.epfl.ch/)
  - Python package by Michel Bierlaire
  - Excellent examples and tutorials
  - Active development

- **Apollo Package (R)**
  [http://www.apollochoicemodelling.com/](http://www.apollochoicemodelling.com/)
  - Comprehensive choice modeling in R
  - Manual with 200+ pages of examples
  - Supports MNL, mixed logit, nested, latent class, and more

- **PyLogit (Python)**
  [https://github.com/timothyb0912/pylogit](https://github.com/timothyb0912/pylogit)
  - Alternative to Biogeme
  - Good for MNL and nested logit
  - Scikit-learn style API

### Journal Articles

- **McFadden, D. (1974).** "Conditional logit analysis of qualitative choice behavior." In *Frontiers in Econometrics*, 105-142.
  - Foundational paper on logit models

- **Train, K., & Weeks, M. (2005).** "Discrete choice models in preference space and willingness-to-pay space." In *Applications of Simulation Methods in Environmental and Resource Economics*, 1-16.
  - WTP-space models vs. preference-space

- **Hess, S., & Palma, D. (2019).** "Apollo: A flexible, powerful and customisable freeware package for choice model estimation and application." *Journal of Choice Modelling*, 32, 100170.

- **Cherchi, E., & Ortúzar, J. de D. (2011).** "On the use of mixed RP/SP models in prediction: Accounting for systematic and random taste heterogeneity." *Transportation Science*, 45(1), 98-108.

### Online Tutorials

- **Biogeme Tutorial by Tim Hillel**
  Step-by-step notebooks on GitHub
  [https://github.com/JoseAngelMartinB/Biogeme-Python-Tutorial](https://github.com/JoseAngelMartinB/Biogeme-Python-Tutorial)

- **Apollo R Package Examples**
  Vignettes and case studies
  [http://www.apollochoicemodelling.com/examples.html](http://www.apollochoicemodelling.com/examples.html)

- **Choice Modeling YouTube Channel**
  Video walkthroughs of estimation
  Search: "Discrete choice modeling tutorial"

---

## ✅ Module Completion Checklist

Before moving to Module 6, ensure you have:

- [ ] Attended or watched both sessions (8 hours total)
- [ ] Completed data reshaping exercise (wide to long)
- [ ] Estimated at least one MNL model in Biogeme or Apollo
- [ ] Participated in model selection tournament
- [ ] Calculated WTP and elasticities
- [ ] Posted to all 3 discussion prompts with peer responses
- [ ] Submitted Module 5 Modeling Memo
- [ ] Read Train (2009) Chapters 3-5
- [ ] Reviewed Biogeme or Apollo documentation

**Self-Assessment Questions:**

1. **Can you reshape** a wide-format SP dataset to long format for estimation?
2. **Can you estimate** a basic MNL model using Biogeme or Apollo and interpret the output?
3. **Can you calculate** willingness-to-pay from parameter estimates with confidence intervals?
4. **Can you compare** two competing models using likelihood ratio test or AIC/BIC?
5. **Can you forecast** market shares under a policy scenario using your estimated model?
6. **Can you explain** your results to a non-technical audience in plain language?

If you answered "yes" to all six—you're ready for Module 6: Policy Communication!

---

## 🔗 Navigation

- **Previous:** [Module 4 - Implementation & Fieldwork](04-implementation.md)
- **Next:** [Module 6 - Policy Interpretation & Communication](06-policy-communication.md)
- **Related:** [Assignment 5](../assignments/05_modeling_memo.md) | [Syllabus](../syllabus.md) | [Course Home](../index.md)

---

<div class="alert alert-success">
<strong>💡 Pro Tip:</strong> Create a "Model Library" folder with template scripts for common model types (MNL, mixed logit, nested). Include clear comments explaining each section. When starting a new project, you can adapt these templates rather than writing from scratch. Over time, you'll build a valuable toolkit for rapid analysis!
</div>

---

**Questions or feedback?** Contact the instructor or post in the course discussion forum.
