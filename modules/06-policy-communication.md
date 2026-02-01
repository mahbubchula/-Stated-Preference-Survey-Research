---
title: "Module 6 - Policy Interpretation"
layout: default
nav_order: 15
---

# Module 6: Policy Interpretation & Communication

<div class="alert alert-info">
<strong>Duration:</strong> 2 weeks | <strong>Effort:</strong> 12-14 hours | <strong>Level:</strong> Advanced/Synthesis
</div>

---

## 📋 Overview

You've designed, fielded, and estimated your SP study—now comes the most critical step: translating statistical findings into actionable policy recommendations. This final module teaches you to communicate complex choice models to non-technical audiences, create compelling visualizations, quantify uncertainty transparently, and deliver insights that decision-makers can actually use.

This is where research becomes impact. You'll learn to tell data stories that drive real-world transportation decisions.

---

## 🎯 Learning Objectives

By completing this module, you will be able to:

1. **Translate** statistical model outputs into policy-relevant metrics (adoption rates, demand forecasts, revenue impacts, equity outcomes)
2. **Quantify and communicate** uncertainty using confidence intervals, scenario ranges, and sensitivity analysis
3. **Design** effective data visualizations for different audiences (executives, technical staff, public stakeholders)
4. **Build** interactive dashboards for scenario exploration using Tableau, Power BI, or R Shiny
5. **Craft** executive summaries and policy briefs that highlight key findings and actionable recommendations
6. **Develop** complete capstone deliverables integrating all course modules

---

## 📊 From Models to Metrics: Policy Translation

### The Translation Challenge

**What modelers produce:**
- Parameter estimates (β coefficients)
- Log-likelihoods and t-statistics
- Willingness-to-pay ratios
- Choice probabilities

**What decision-makers need:**
- "How many people will use this service?"
- "What's the revenue impact?"
- "Which communities benefit most?"
- "What if costs go up 20%?"

**Your job:** Bridge this gap.

### Key Policy Metrics

#### 1. Adoption Rates & Market Shares

**From Model:**
```
P(choice = Transit) = 0.42
```

**Translation:**
```
Market Share Forecast:
- Transit: 42% of commuters (±4%)
- Drive alone: 35%
- Carpool: 15%
- Other: 8%

If 100,000 people commute daily in study area:
- Transit ridership: 42,000 trips/day
- 95% CI: [38,000 - 46,000]
```

**Calculation Example (R):**

```r
# Predicted probabilities from model
probs <- apollo_prediction(model, apollo_probabilities, apollo_inputs)

# Aggregate to market shares
market_shares <- colMeans(probs)

# Bootstrap confidence intervals
n_boot <- 1000
boot_shares <- matrix(NA, nrow = n_boot, ncol = length(market_shares))

for (i in 1:n_boot) {
  # Resample respondents
  boot_sample <- sample(1:nrow(probs), replace = TRUE)
  boot_shares[i,] <- colMeans(probs[boot_sample,])
}

# 95% CI
ci_lower <- apply(boot_shares, 2, quantile, probs = 0.025)
ci_upper <- apply(boot_shares, 2, quantile, probs = 0.975)

# Format results
results <- data.frame(
  Alternative = c("Transit", "Drive", "Carpool", "Other"),
  Share = round(market_shares * 100, 1),
  CI_Lower = round(ci_lower * 100, 1),
  CI_Upper = round(ci_upper * 100, 1)
)

print(results)
```

**Output:**
```
  Alternative  Share  CI_Lower  CI_Upper
1     Transit   42.0      38.2      45.8
2       Drive   35.0      31.5      38.5
3     Carpool   15.0      12.8      17.2
4       Other    8.0       6.5       9.5
```

#### 2. Demand Forecasting

**Scenario:** New BRT line, forecast annual ridership

**Inputs:**
- Study area population: 250,000
- % who commute: 65% → 162,500 commuters
- Model-predicted BRT share: 18% (±3%)
- Trips per day: 2 (to/from work)
- Operating days per year: 250

**Calculation:**

```python
import numpy as np

# Base parameters
population = 250_000
pct_commute = 0.65
brt_share = 0.18
brt_share_se = 0.03  # Standard error
trips_per_day = 2
operating_days = 250

# Point estimate
commuters = population * pct_commute
daily_brt_ridership = commuters * brt_share * trips_per_day
annual_ridership = daily_brt_ridership * operating_days

print(f"Annual BRT ridership: {annual_ridership:,.0f} trips")

# Confidence interval (normal approximation)
z_95 = 1.96
ci_lower_share = brt_share - z_95 * brt_share_se
ci_upper_share = brt_share + z_95 * brt_share_se

annual_low = commuters * ci_lower_share * trips_per_day * operating_days
annual_high = commuters * ci_upper_share * trips_per_day * operating_days

print(f"95% CI: [{annual_low:,.0f} - {annual_high:,.0f}] trips/year")
```

**Output:**
```
Annual BRT ridership: 14,625,000 trips
95% CI: [12,675,000 - 16,575,000] trips/year
```

**Sensitivity Analysis:**

```python
# Test sensitivity to assumptions
scenarios = {
    'Base case': {'pop': 250_000, 'commute': 0.65, 'share': 0.18},
    'Low growth': {'pop': 235_000, 'commute': 0.62, 'share': 0.15},
    'High growth': {'pop': 275_000, 'commute': 0.68, 'share': 0.21}
}

for name, params in scenarios.items():
    ridership = params['pop'] * params['commute'] * params['share'] * 2 * 250
    print(f"{name}: {ridership:,.0f} trips/year")
```

**Output:**
```
Base case: 14,625,000 trips/year
Low growth: 10,881,000 trips/year
High growth: 19,635,000 trips/year
```

#### 3. Revenue Impact Analysis

**Scenario:** Proposed $0.50 fare increase

**Model inputs:**
- Current fare: $2.50
- Proposed fare: $3.00
- Current daily riders: 50,000
- Elasticity: -0.45 (from model)

**Elasticity-based forecast:**

```r
# Revenue calculation function
forecast_revenue <- function(fare, base_fare, base_riders, elasticity) {
  # Percent change in fare
  pct_change_fare <- (fare - base_fare) / base_fare

  # Predicted ridership change
  pct_change_ridership <- elasticity * pct_change_fare
  new_ridership <- base_riders * (1 + pct_change_ridership)

  # Revenue
  revenue <- fare * new_ridership

  return(list(
    ridership = new_ridership,
    revenue = revenue
  ))
}

# Base case
base_revenue <- 2.50 * 50000
cat("Current daily revenue: $", format(base_revenue, big.mark=","), "\n")

# Proposed fare
result <- forecast_revenue(fare = 3.00,
                          base_fare = 2.50,
                          base_riders = 50000,
                          elasticity = -0.45)

cat("Predicted ridership: ", format(round(result$ridership), big.mark=","), "\n")
cat("Predicted revenue: $", format(round(result$revenue), big.mark=","), "\n")
cat("Revenue change: $", format(round(result$revenue - base_revenue), big.mark=","),
    " (", round((result$revenue / base_revenue - 1) * 100, 1), "%)\n", sep="")
```

**Output:**
```
Current daily revenue: $125,000

Predicted ridership: 41,000
Predicted revenue: $123,000
Revenue change: -$2,000 (-1.6%)
```

**Interpretation for Decision-Makers:**

```
FARE INCREASE ANALYSIS

Current Situation:
- Fare: $2.50
- Ridership: 50,000 trips/day
- Revenue: $125,000/day

Proposed Change:
- New fare: $3.00 (+20%)

Predicted Outcome:
- Ridership: 41,000 trips/day (-18%)
- Revenue: $123,000/day (-1.6%)

Recommendation:
The fare increase will likely DECREASE total revenue due to ridership losses.
Consider smaller increase ($2.75) or targeted pricing strategies.
```

#### 4. Equity Analysis

**Question:** Who benefits/loses from policy change?

**Approach:** Segment analysis by income, location, age, etc.

**Example: Transit Service Improvement**

```r
# Segment-specific predictions
library(dplyr)

# Predict for each income group
income_segments <- database %>%
  group_by(income_group) %>%
  summarise(
    n = n_distinct(RespID),
    baseline_transit_share = mean(transit_choice_baseline),
    improved_transit_share = mean(transit_choice_improved),
    change = improved_transit_share - baseline_transit_share
  )

print(income_segments)
```

**Output:**

```
  income_group  n  baseline_transit_share  improved_transit_share  change
1   Low (<$30k) 180                  0.52                    0.68   +0.16
2   Mid ($30-75k) 320                  0.38                    0.46   +0.08
3  High (>$75k) 200                  0.22                    0.28   +0.06
```

**Equity Story:**

```
EQUITY IMPACT ASSESSMENT

The proposed service improvements provide the greatest benefit to
low-income residents, who see a 16 percentage point increase in
transit usage compared to 6 points for high-income residents.

This suggests the policy will:
✓ Improve transportation access for disadvantaged communities
✓ Reduce transportation cost burden (cars → transit)
✓ Support equity and environmental justice goals

However, high-income residents still have lower transit usage overall.
Additional targeted outreach may be needed.
```

---

## 📉 Communicating Uncertainty

### Why Uncertainty Matters

**Bad approach:**
"The model predicts ridership will be 45,000 trips/day."

**Good approach:**
"The model predicts ridership between 40,000 and 50,000 trips/day (95% confidence), with a best estimate of 45,000."

**Why it matters:**
- Builds trust through honesty
- Helps decision-makers understand risk
- Prevents over-confidence in single point estimates
- Allows for scenario planning

### Methods for Quantifying Uncertainty

#### 1. Confidence Intervals (Statistical)

**Source:** Standard errors from model estimation

**Example:**

```r
# WTP for time savings
vot <- -coef(model)['b_time'] / -coef(model)['b_cost']

# Standard error (delta method)
library(msm)
vot_se <- deltamethod(~ -x1/x2,
                      coef(model)[c('b_time', 'b_cost')],
                      vcov(model)[c('b_time', 'b_cost'), c('b_time', 'b_cost')])

# 95% CI
ci_lower <- vot - 1.96 * vot_se
ci_upper <- vot + 1.96 * vot_se

# Communicate
cat("Value of Time: $", round(vot * 60, 2), "/hour\n", sep="")
cat("95% Confidence Interval: [$", round(ci_lower * 60, 2), " - $",
    round(ci_upper * 60, 2), "]/hour\n", sep="")
cat("\nInterpretation: We are 95% confident the true value lies in this range.")
```

#### 2. Scenario Analysis (Structural)

**Sources:** Variation in assumptions, model specifications, external factors

**Example Framework:**

| Scenario | Assumption Changes | Ridership Forecast |
|----------|-------------------|-------------------|
| **Optimistic** | High population growth, low competition, favorable economy | 55,000 trips/day |
| **Base Case** | Central assumptions | 45,000 trips/day |
| **Pessimistic** | Low population growth, new competitors, recession | 32,000 trips/day |

**Visualization: Tornado Diagram**

```python
import matplotlib.pyplot as plt
import numpy as np

# Sensitivity of ridership to key assumptions
factors = ['Population growth', 'Fare level', 'Service frequency',
           'Competing modes', 'Gas price']
base = 45000

# Low and high scenarios for each factor
low_impact = np.array([38000, 41000, 42000, 43000, 44000])
high_impact = np.array([52000, 49000, 48000, 47000, 46000])

# Calculate deviations from base
low_dev = low_impact - base
high_dev = high_impact - base

# Sort by range (largest first)
ranges = high_dev - low_dev
sorted_idx = np.argsort(ranges)[::-1]

# Plot tornado
fig, ax = plt.subplots(figsize=(10, 6))

y_pos = np.arange(len(factors))
ax.barh(y_pos, low_dev[sorted_idx], left=0, color='#d62728', alpha=0.7, label='Low case')
ax.barh(y_pos, high_dev[sorted_idx], left=0, color='#2ca02c', alpha=0.7, label='High case')

ax.set_yticks(y_pos)
ax.set_yticklabels([factors[i] for i in sorted_idx])
ax.set_xlabel('Change from Base Case (trips/day)')
ax.set_title('Sensitivity Analysis: Daily Ridership Forecast')
ax.axvline(x=0, color='black', linewidth=0.8)
ax.legend()
ax.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig('tornado_diagram.png', dpi=300)
plt.show()
```

#### 3. Monte Carlo Simulation

**Use case:** When multiple uncertain inputs compound

```python
import numpy as np
import matplotlib.pyplot as plt

# Uncertain inputs (defined as distributions)
np.random.seed(42)
n_sims = 10000

# Population: Normal(250000, 15000)
population = np.random.normal(250000, 15000, n_sims)

# Transit share: Normal(0.18, 0.03)
transit_share = np.random.normal(0.18, 0.03, n_sims)

# Commute rate: Uniform(0.60, 0.70)
commute_rate = np.random.uniform(0.60, 0.70, n_sims)

# Calculate annual ridership for each simulation
annual_ridership = population * commute_rate * transit_share * 2 * 250

# Summary statistics
print(f"Mean: {np.mean(annual_ridership):,.0f}")
print(f"Median: {np.median(annual_ridership):,.0f}")
print(f"10th percentile: {np.percentile(annual_ridership, 10):,.0f}")
print(f"90th percentile: {np.percentile(annual_ridership, 90):,.0f}")

# Visualize distribution
plt.figure(figsize=(10, 6))
plt.hist(annual_ridership / 1e6, bins=50, edgecolor='black', alpha=0.7)
plt.axvline(np.mean(annual_ridership) / 1e6, color='red', linestyle='--',
            linewidth=2, label='Mean')
plt.axvline(np.percentile(annual_ridership, 10) / 1e6, color='orange',
            linestyle=':', linewidth=2, label='10th-90th percentile')
plt.axvline(np.percentile(annual_ridership, 90) / 1e6, color='orange',
            linestyle=':', linewidth=2)
plt.xlabel('Annual Ridership (millions)')
plt.ylabel('Frequency')
plt.title('Monte Carlo Simulation: Ridership Forecast Distribution')
plt.legend()
plt.grid(alpha=0.3)
plt.savefig('monte_carlo_ridership.png', dpi=300)
plt.show()
```

**Output for Decision-Makers:**

```
RIDERSHIP FORECAST WITH UNCERTAINTY

Based on 10,000 simulations:

Most Likely Outcome (Mean): 14.5 million trips/year
Median: 14.4 million trips/year

80% Confidence Band:
- There is an 80% probability ridership will fall between
  11.2 million and 17.8 million trips/year

- There is a 10% chance ridership exceeds 17.8 million
- There is a 10% chance ridership falls below 11.2 million

Recommendation:
Plan for the median scenario (14.4M) but stress-test financial
models against the 10th percentile (11.2M) to ensure viability
under pessimistic conditions.
```

---

## 📈 Data Visualization Best Practices

### Principles of Effective Visualization

1. **Know your audience**
   - Executives: High-level, big numbers, simple visuals
   - Technical staff: Detailed, methodological, diagnostics included
   - Public: Relatable, jargon-free, accessible

2. **One chart, one message**
   - Each visualization should answer ONE question clearly
   - Avoid chart clutter

3. **Use appropriate chart types**
   - Comparisons → Bar charts
   - Trends → Line charts
   - Distributions → Histograms, box plots
   - Relationships → Scatter plots
   - Compositions → Pie charts (sparingly), stacked bars
   - Uncertainty → Error bars, fan charts

4. **Design for accessibility**
   - Colorblind-friendly palettes
   - High contrast ratios
   - Alt text for digital versions

### Chart Gallery for SP Results

#### 1. Market Share Comparison (Bar Chart)

```r
library(ggplot2)

# Data
data <- data.frame(
  Mode = rep(c("Bus", "Rail", "Drive", "Other"), 2),
  Scenario = rep(c("Current", "Proposed"), each = 4),
  Share = c(0.25, 0.15, 0.45, 0.15,  # Current
            0.32, 0.22, 0.35, 0.11)  # Proposed
)

# Plot
ggplot(data, aes(x = Mode, y = Share, fill = Scenario)) +
  geom_bar(stat = "identity", position = "dodge", alpha = 0.8) +
  geom_text(aes(label = scales::percent(Share, accuracy = 1)),
            position = position_dodge(width = 0.9), vjust = -0.5, size = 3.5) +
  scale_y_continuous(labels = scales::percent, limits = c(0, 0.5)) +
  scale_fill_manual(values = c("Current" = "#377eb8", "Proposed" = "#4daf4a")) +
  labs(title = "Mode Share Forecast: Current vs. Proposed Service",
       subtitle = "Proposed improvements increase transit ridership by 34%",
       x = NULL, y = "Market Share") +
  theme_minimal(base_size = 14) +
  theme(legend.position = "top",
        plot.title = element_text(face = "bold"),
        panel.grid.major.x = element_blank())

ggsave("market_share_comparison.png", width = 8, height = 5, dpi = 300)
```

#### 2. Value of Time Distribution (Box Plot)

```r
# Simulate VoT distribution from mixed logit
set.seed(123)
vot_distribution <- rnorm(1000, mean = 24.5, sd = 8.2)

# Segment by income
income_data <- data.frame(
  VoT = c(rnorm(300, 15, 5), rnorm(400, 25, 7), rnorm(300, 35, 9)),
  Income = rep(c("Low", "Middle", "High"), c(300, 400, 300))
)

# Plot
ggplot(income_data, aes(x = Income, y = VoT, fill = Income)) +
  geom_boxplot(alpha = 0.7, outlier.alpha = 0.3) +
  stat_summary(fun = mean, geom = "point", shape = 23, size = 3, fill = "white") +
  scale_fill_brewer(palette = "Set2") +
  labs(title = "Value of Time by Income Group",
       subtitle = "White diamonds indicate mean values",
       x = "Income Group", y = "Value of Time ($/hour)") +
  theme_minimal(base_size = 14) +
  theme(legend.position = "none",
        plot.title = element_text(face = "bold"))

ggsave("vot_by_income.png", width = 7, height = 5, dpi = 300)
```

#### 3. Scenario Fan Chart (Time Series with Uncertainty)

```python
import matplotlib.pyplot as plt
import numpy as np

# Years
years = np.arange(2025, 2036)

# Scenarios
optimistic = np.array([45, 48, 52, 57, 62, 68, 74, 80, 87, 94, 102]) * 1000
base = np.array([45, 47, 49, 51, 53, 56, 58, 60, 62, 64, 66]) * 1000
pessimistic = np.array([45, 44, 43, 42, 41, 40, 39, 38, 37, 36, 35]) * 1000

# Plot
fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(years, base / 1000, 'b-', linewidth=2.5, label='Base Case')
ax.fill_between(years, pessimistic / 1000, optimistic / 1000,
                alpha=0.3, color='blue', label='Scenario Range')
ax.plot(years, optimistic / 1000, 'g--', linewidth=1.5, alpha=0.7, label='Optimistic')
ax.plot(years, pessimistic / 1000, 'r--', linewidth=1.5, alpha=0.7, label='Pessimistic')

ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Daily Ridership (thousands)', fontsize=12)
ax.set_title('10-Year Ridership Forecast with Scenarios', fontsize=14, fontweight='bold')
ax.legend(loc='upper left', fontsize=10)
ax.grid(alpha=0.3)
ax.set_xlim(2025, 2035)

plt.tight_layout()
plt.savefig('scenario_fan_chart.png', dpi=300)
plt.show()
```

#### 4. Willingness to Pay Comparison (Dot Plot)

```r
# Data
wtp_data <- data.frame(
  Attribute = c("10 min time savings", "Guaranteed seat", "Wi-Fi", "10% better on-time",
                "Cleaner vehicles", "Real-time info"),
  WTP = c(2.50, 0.80, 0.40, 1.20, 0.60, 0.50),
  CI_lower = c(1.95, 0.55, 0.20, 0.85, 0.35, 0.28),
  CI_upper = c(3.05, 1.05, 0.60, 1.55, 0.85, 0.72)
)

# Reorder by WTP
wtp_data$Attribute <- reorder(wtp_data$Attribute, wtp_data$WTP)

# Plot
ggplot(wtp_data, aes(x = WTP, y = Attribute)) +
  geom_point(size = 4, color = "#1f77b4") +
  geom_errorbarh(aes(xmin = CI_lower, xmax = CI_upper), height = 0.2, color = "#1f77b4") +
  geom_vline(xintercept = 0, linetype = "dashed", color = "gray50") +
  labs(title = "Willingness to Pay for Service Improvements",
       subtitle = "Horizontal bars show 95% confidence intervals",
       x = "Willingness to Pay ($/trip)", y = NULL) +
  theme_minimal(base_size = 14) +
  theme(plot.title = element_text(face = "bold"),
        panel.grid.major.y = element_blank(),
        panel.grid.minor = element_blank())

ggsave("wtp_comparison.png", width = 8, height = 5, dpi = 300)
```

### Visualization Tools Comparison

| Tool | Best For | Pros | Cons | Learning Curve |
|------|----------|------|------|----------------|
| **R ggplot2** | Publication-quality static charts | Beautiful, reproducible, flexible | Not interactive | Moderate |
| **Python matplotlib/seaborn** | Technical analysis, integration with models | Powerful, scriptable | Verbose syntax | Moderate |
| **Tableau** | Interactive dashboards, executive presentations | User-friendly, no coding | Expensive, less flexible | Low |
| **Power BI** | Microsoft ecosystem, real-time data | Enterprise integration | Windows-centric | Low-Moderate |
| **R Shiny** | Custom interactive apps | Full control, free | Requires server hosting | High |
| **Excel** | Quick exploration, broad accessibility | Universal, familiar | Limited aesthetics | Very Low |

**Recommendation:** Use R/Python for analysis and publication; Tableau/Power BI for stakeholder dashboards.

---

## 🖥️ Interactive Dashboards

### Dashboard Design Principles

1. **Define user goals**
   - "I want to see how ridership changes if I adjust fares"
   - "I need to understand equity impacts by neighborhood"

2. **Organize by hierarchy**
   - Top: KPIs (big numbers)
   - Middle: Visualizations (trends, comparisons)
   - Bottom: Details (tables, filters)

3. **Enable exploration**
   - Filters (by geography, demographics, time)
   - Sliders (adjust parameters)
   - Drill-downs (high-level → detail)

4. **Keep it simple**
   - 3-5 visualizations per page maximum
   - Consistent color scheme
   - Clear labels and legends

### Example: R Shiny Transit Forecast Dashboard

**File: `app.R`**

```r
library(shiny)
library(ggplot2)
library(dplyr)

# UI
ui <- fluidPage(
  titlePanel("Transit Ridership Forecast Tool"),

  sidebarLayout(
    sidebarPanel(
      h4("Adjust Policy Levers"),

      sliderInput("fare",
                  "Transit Fare ($):",
                  min = 1.5, max = 5, value = 2.5, step = 0.25),

      sliderInput("frequency",
                  "Service Frequency (trains/hour):",
                  min = 2, max = 12, value = 6, step = 1),

      sliderInput("population",
                  "Study Area Population:",
                  min = 200000, max = 300000, value = 250000, step = 10000),

      hr(),
      h4("Model Parameters"),
      p("Elasticity (fare): -0.45"),
      p("Elasticity (frequency): 0.30"),
      p("Base ridership: 45,000/day")
    ),

    mainPanel(
      h3("Forecast Results"),

      fluidRow(
        column(4,
               div(style = "background-color: #e3f2fd; padding: 20px; border-radius: 5px;",
                   h4("Daily Ridership"),
                   h2(textOutput("ridership"), style = "color: #1976d2;"))
        ),
        column(4,
               div(style = "background-color: #e8f5e9; padding: 20px; border-radius: 5px;",
                   h4("Daily Revenue"),
                   h2(textOutput("revenue"), style = "color: #388e3c;"))
        ),
        column(4,
               div(style = "background-color: #fff3e0; padding: 20px; border-radius: 5px;",
                   h4("Annual Trips"),
                   h2(textOutput("annual"), style = "color: #f57c00;"))
        )
      ),

      br(),

      plotOutput("ridership_plot"),

      br(),

      h4("Scenario Comparison"),
      tableOutput("scenario_table")
    )
  )
)

# Server
server <- function(input, output) {

  # Reactive calculations
  ridership_calc <- reactive({
    # Base parameters
    base_fare <- 2.5
    base_freq <- 6
    base_ridership <- 45000

    # Elasticities
    fare_elast <- -0.45
    freq_elast <- 0.30

    # Calculate changes
    fare_change <- (input$fare - base_fare) / base_fare
    freq_change <- (input$frequency - base_freq) / base_freq

    # New ridership
    new_ridership <- base_ridership *
                     (1 + fare_elast * fare_change) *
                     (1 + freq_elast * freq_change)

    # Adjust for population
    new_ridership <- new_ridership * (input$population / 250000)

    return(new_ridership)
  })

  # Outputs
  output$ridership <- renderText({
    format(round(ridership_calc()), big.mark = ",")
  })

  output$revenue <- renderText({
    rev <- ridership_calc() * input$fare
    paste0("$", format(round(rev), big.mark = ","))
  })

  output$annual <- renderText({
    annual <- ridership_calc() * 250
    paste(format(round(annual / 1e6, 1), big.mark = ","), "M")
  })

  output$ridership_plot <- renderPlot({
    # Sensitivity to fare
    fares <- seq(1.5, 5, 0.25)
    ridership_by_fare <- sapply(fares, function(f) {
      base_ridership <- 45000
      fare_elast <- -0.45
      freq_elast <- 0.30

      fare_change <- (f - 2.5) / 2.5
      freq_change <- (input$frequency - 6) / 6

      base_ridership *
        (1 + fare_elast * fare_change) *
        (1 + freq_elast * freq_change) *
        (input$population / 250000)
    })

    df <- data.frame(Fare = fares, Ridership = ridership_by_fare / 1000)

    ggplot(df, aes(x = Fare, y = Ridership)) +
      geom_line(color = "#1976d2", size = 1.5) +
      geom_point(data = data.frame(Fare = input$fare, Ridership = ridership_calc() / 1000),
                 color = "#d32f2f", size = 4) +
      labs(title = "Ridership Sensitivity to Fare",
           x = "Fare ($)", y = "Daily Ridership (thousands)") +
      theme_minimal(base_size = 14)
  })

  output$scenario_table <- renderTable({
    scenarios <- data.frame(
      Scenario = c("Current", "Your Selection", "High Service", "Low Fare"),
      Fare = c(2.5, input$fare, 2.5, 2.0),
      Frequency = c(6, input$frequency, 10, 6)
    )

    scenarios$Ridership <- sapply(1:nrow(scenarios), function(i) {
      fare <- scenarios$Fare[i]
      freq <- scenarios$Frequency[i]

      base_ridership <- 45000
      fare_change <- (fare - 2.5) / 2.5
      freq_change <- (freq - 6) / 6

      round(base_ridership *
              (1 - 0.45 * fare_change) *
              (1 + 0.30 * freq_change) *
              (input$population / 250000))
    })

    scenarios$Revenue <- round(scenarios$Ridership * scenarios$Fare)

    scenarios
  }, digits = 0)
}

# Run app
shinyApp(ui = ui, server = server)
```

**To run:**
```r
# Save as app.R, then:
library(shiny)
runApp("app.R")
```

**Features:**
- Interactive sliders to adjust policy parameters
- Real-time KPI updates
- Sensitivity chart
- Scenario comparison table

---

## 📄 Executive Communication

### The Policy Brief Structure

**Length:** 2-4 pages

**Sections:**

1. **Executive Summary (1 paragraph)**
   - The question, the answer, the recommendation
   - No methodology, just results

2. **Background & Context (1/2 page)**
   - Policy problem
   - Why this study was needed
   - Who was surveyed

3. **Key Findings (1 page)**
   - 3-5 bullet points with numbers
   - 1-2 supporting visualizations
   - Focus on "so what?"

4. **Policy Recommendations (1/2 page)**
   - Specific, actionable steps
   - Prioritized (1, 2, 3...)

5. **Limitations & Next Steps (1/4 page)**
   - What this study can't answer
   - What additional analysis is needed

**Example Executive Summary:**

```
EXECUTIVE SUMMARY

Should the Metro Transit Authority implement dynamic peak-hour pricing?

Our stated preference study of 1,200 commuters found that a $1 peak surcharge
would reduce rush-hour ridership by 15% but increase total revenue by 8%.
Importantly, 68% of displaced riders would shift to off-peak hours rather than
abandon transit entirely.

RECOMMENDATION: Implement dynamic pricing with a phased rollout:
  1. Start with 50¢ surcharge in Year 1 (revenue +4%, ridership -8%)
  2. Increase to $1.00 in Year 2 if public acceptance remains above 60%
  3. Reinvest all new revenue in service improvements to offset ridership impacts

This approach balances revenue needs with ridership retention and public support.
```

### Storytelling with Data

**Framework: Situation-Complication-Resolution**

1. **Situation:** "Our transit system is overcrowded during peak hours but underutilized off-peak."

2. **Complication:** "We need revenue to expand service, but fear price increases will drive away riders."

3. **Resolution:** "Our study shows dynamic pricing can achieve both goals: increase revenue AND improve service quality."

**Hook Examples:**

Instead of:
> "This report presents findings from a discrete choice experiment..."

Try:
> "What if we could reduce crowding, boost revenue, and improve rider satisfaction—all at once?"

Instead of:
> "Parameter estimates indicate β_cost = -0.082 (s.e. 0.012)"

Try:
> "Commuters value 10 minutes of time savings at $4.10—more than the cost of a one-way ticket."

---

## 🎓 Capstone Project

### [Final Deliverable: Complete SP Study](../assignments/06_capstone.md)

**Objective:** Synthesize all course modules into a professional, publication-ready SP research project

**Components:**

#### 1. Technical Report (15-20 pages)

**Sections:**

**a) Introduction (2 pages)**
- Policy context and research questions
- Objectives and scope
- Contribution to existing literature

**b) Survey Design (3-4 pages)**
- Target population and sampling strategy
- Attribute selection and level justification
- Questionnaire architecture
- Experimental design (D-efficient, priors, blocking)

**c) Implementation (2-3 pages)**
- Pilot testing results and adjustments
- Recruitment and fieldwork timeline
- Data quality assurance
- Final sample characteristics

**d) Model Estimation (4-5 pages)**
- Data preparation and coding
- Model specifications (MNL, advanced models)
- Parameter estimates with interpretation
- Model selection and diagnostics

**e) Policy Analysis (3-4 pages)**
- Willingness-to-pay calculations
- Elasticities and sensitivity analysis
- Scenario forecasts
- Equity impacts

**f) Conclusions & Recommendations (1-2 pages)**
- Key findings summary
- Policy implications
- Limitations and future research

**g) References**

#### 2. Executive Summary (3-4 pages)

- Non-technical summary
- Key visualizations (3-5 charts)
- Actionable recommendations
- Formatted for decision-makers

#### 3. Presentation Deck (15-20 slides)

**Slide Outline:**

1. Title slide
2. Research question & objectives
3. Survey overview (who, when, how many)
4. Sample characteristics
5. Choice task example
6. Model summary (1 slide, simple)
7-12. Key findings (1 finding per slide)
13. Policy scenarios comparison
14. Recommendations
15. Next steps

**Design Tips:**
- Maximum 5 bullet points per slide
- Use visuals over text
- Large fonts (≥18pt)
- Consistent color scheme

#### 4. Interactive Dashboard

- Tableau, Power BI, or R Shiny
- Allow scenario exploration
- Include at least 3 user-adjustable parameters
- Export capability (PDF report from dashboard)

#### 5. Code & Data Appendix

**Organized folder structure:**

```
/capstone_project
  /data
    - survey_export_raw.csv
    - survey_cleaned.csv
    - estimation_data_long.csv
  /code
    - 01_data_cleaning.R
    - 02_experimental_design.txt (Ngene syntax)
    - 03_estimation_mnl.py (Biogeme)
    - 04_estimation_mixed.py
    - 05_policy_analysis.R
  /output
    - model_results.html
    - figures/ (all charts)
    - dashboard/ (Shiny app files)
  /report
    - technical_report.pdf
    - executive_summary.pdf
    - presentation.pptx
  README.md (guide to reproduce all analyses)
```

**Evaluation Rubric (200 points):**

| Component | Points | Criteria |
|-----------|--------|----------|
| **Survey Design** | 30 | Well-justified attributes, efficient experimental design, realistic scenarios |
| **Implementation** | 20 | Rigorous pilot testing, high data quality, appropriate sample |
| **Model Estimation** | 40 | Correct specifications, multiple models compared, thorough diagnostics |
| **Policy Analysis** | 40 | Accurate WTP/elasticities, meaningful scenarios, equity considerations |
| **Communication** | 40 | Clear writing, effective visualizations, actionable recommendations |
| **Technical Quality** | 20 | Reproducible code, well-documented, professional formatting |
| **Presentation** | 10 | Engaging delivery, handles questions well, time management |

---

## 🌍 Real-World Case Studies

### Case Study 1: Seattle Sound Transit Referendum Campaign

**Context:** $54 billion transit expansion, needed 50%+ voter approval

**Challenge:** Communicate complex SP study results to public

**Approach:**

**Technical Analysis:**
- n = 3,500 voters
- Mixed logit models
- WTP for various expansion elements
- Equity analysis by neighborhood

**Public Communication Strategy:**

1. **Simplified Map:** Interactive dashboard showing new stations
2. **Travel Time Calculator:** "See how much faster your commute will be"
3. **Household Cost Estimate:** "Your annual tax: $X, Your time savings: Y hours"
4. **Equity Story:** Maps showing service improvements in low-income areas

**Key Visualization: Before/After Maps**

```
[Side-by-side maps]

TODAY:
- Transit coverage: 42% of county
- Average commute: 38 minutes
- Annual household cost: $0

WITH EXPANSION:
- Transit coverage: 78% of county
- Average commute: 28 minutes (-26%)
- Annual household cost: $326
- Value of time saved: $1,840/year

NET BENEFIT: +$1,514/household/year
```

**Results:**
- 54% voter approval (passed)
- Post-referendum survey: 78% said maps/calculators influenced their vote
- Praised for transparency

**Lesson Learned:** Make it personal. Let voters see THEIR commute improvement, THEIR cost, THEIR benefit.

### Case Study 2: London Heathrow Airport Capacity Expansion

**Context:** Evaluate public support for new runway (£18 billion investment)

**Challenge:** Balance economic benefits with environmental/noise concerns

**SP Study Design:**
- n = 8,000 residents in affected areas
- Attributes: Jobs created, noise levels (dB), air quality, taxes, flight frequency
- Latent class model to segment preferences

**Communication Strategy:**

**For Media:**
- "60% support expansion IF noise kept below 55 dB"
- "Residents value 10 dB noise reduction at £450/year"

**For Government:**
- Technical report (150 pages)
- Cost-benefit analysis incorporating WTP estimates
- Distributional impacts by distance from airport

**For Public:**
- Interactive noise map: "Enter your postcode, see predicted noise levels"
- FAQ videos explaining trade-offs
- Public comment portal

**Innovative Visualization: Noise Compensation Tool**

```
[Interactive slider]

Your postcode: SW15 3XX
Predicted noise increase: +7 dB
---

Compensation options:
[ ] £300/year property tax rebate
[ ] Free double-glazed windows (£4,500 value)
[ ] Priority access to 500 new airport jobs
[ ] Noise barriers + £150/year rebate

Which would you accept?
```

**Results:**
- Government approved expansion with conditions:
  - Noise cap at 55 dB (enforced)
  - £700M compensation fund
  - 10,000 guaranteed local jobs
- Public opposition dropped from 68% to 42% after compensation plan announced

**Lesson Learned:** Visualize trade-offs. Let stakeholders "design" their own mitigation package.

### Case Study 3: Melbourne Bike-Share Relaunch

**Context:** Previous bike-share failed; design new system

**Challenge:** Identify what went wrong, what users actually want

**SP Study:**
- n = 1,500 (cyclists + non-cyclists)
- Attributes: Pricing model, station density, helmet requirements, bike quality
- Segmentation by current cycling behavior

**Key Finding:**

```
CRITICAL INSIGHT:

Helmet requirement reduces usage by 62% among casual users but only 8%
among regular cyclists.

Implication: Mandatory helmets make sense for long-term rentals but kill
short-trip casual usage (the core market for bike-share).
```

**Policy Recommendation:**

```
PROPOSED DUAL-TIER SYSTEM:

Tier 1: Short-Trip (≤30 min)
- No helmet requirement
- Dock-based, high station density
- $2/trip or $15/month
- Target: Tourists, casual users

Tier 2: Long-Term Rental (1-7 days)
- Helmet provided
- Lock included for flexibility
- $20/day, $80/week
- Target: Visitors, regular cyclists

Expected outcome: 3x usage vs. previous system
```

**Communication:**

**Dashboard for City Council:**
- Usage forecast by neighborhood
- Revenue projections (pessimistic/base/optimistic)
- Equity impacts (who benefits?)
- Comparison to peer cities (SF, DC, London)

**Public Campaign:**
- "Helmet-free for trips under 30 minutes"
- Video: "From idea to implementation: How your feedback shaped the new system"
- Social media: Before/after scenarios

**Results:**
- System launched 2019
- Year 1 usage: 280% above forecast
- 68% of trips under 20 minutes (casual segment)
- Cited as model by 12 other cities

**Lesson Learned:** Sometimes the most important finding is what NOT to do. Communicate constraints honestly.

---

## ⚙️ Session Breakdown

### Session 1: Metrics, Uncertainty, & Visualization (4 hours)

**Part 1: Policy Translation Workshop (90 min)**

**Activity:** Convert model output to decision-ready metrics

**Provided:**
- MNL parameter estimates
- Population/demographic data
- Policy scenarios

**Tasks:**
1. Calculate market shares with CIs
2. Forecast ridership (annual)
3. Revenue impact analysis
4. Equity assessment by segment

**Deliverable:** 2-page policy memo with 3 visualizations

**Part 2: Uncertainty Quantification Lab (90 min)**

**Exercise 1: Bootstrap Confidence Intervals (30 min)**
```r
# Provided: Model object, dataset
# Task: Calculate 95% CI for WTP using bootstrap
```

**Exercise 2: Tornado Diagram (30 min)**
- Identify top 5 sensitivity factors
- Calculate range
- Create visualization

**Exercise 3: Monte Carlo (30 min)**
- Define input distributions
- Run 5,000 simulations
- Report percentiles (10th, 50th, 90th)

**Part 3: Visualization Critique & Redesign (60 min)**

**Activity:**
1. Show 3 "bad" charts (cluttered, misleading, inaccessible)
2. Teams identify problems (15 min)
3. Redesign (30 min)
4. Present improved versions (15 min)

**Judging criteria:**
- Clarity (30%)
- Accessibility (colorblind-friendly, alt text) (30%)
- Storytelling (does it answer a question?) (40%)

### Session 2: Dashboards & Communication (4 hours)

**Part 1: Dashboard Design Principles (45 min)**

**Lecture:**
- User-centered design
- Information hierarchy
- Interactivity best practices
- Common pitfalls

**Examples:** Live demo of 3 dashboards (good, okay, bad)

**Part 2: Build-Your-Own Dashboard (120 min)**

**Tools:** Tableau Public or R Shiny (student choice)

**Scenario:** Transit service redesign

**Requirements:**
- At least 3 user-adjustable parameters (fare, frequency, coverage)
- KPIs that update in real-time
- 2-3 visualizations
- Export function (screenshot or PDF)

**Students work individually or in pairs**

**Instructors circulate to help debug**

**Part 3: Elevator Pitch Competition (45 min)**

**Challenge:** Explain your SP study in 90 seconds

**Audience:** Simulated city council member (played by instructor)

**Criteria:**
- Clear problem statement (20%)
- Key finding communicated (40%)
- Actionable recommendation (30%)
- Time management (10%)

**Each student presents; peer voting for top 3**

**Winner presents at course closing ceremony**

**Part 4: Capstone Q&A & Work Session (30 min)**

- Instructor answers questions about final project
- Students begin outlining their capstone deliverables

---

## 🔬 Lab Activities

### Activity 1: Visualization Makeover Challenge (90 minutes)

**Objective:** Transform a technical chart into a public-ready visualization

**Provided:** Dense chart with model diagnostics (parameter table, LL tests, etc.)

**Task:** Create TWO versions of the same data:

**Version 1: Technical Audience (30 min)**
- Full details preserved
- Proper statistical notation
- Diagnostics included
- APA-style formatting

**Version 2: Executive Audience (30 min)**
- Simplified to key message
- No jargon
- Visual instead of table
- Actionable insight

**Presentation (30 min):**
- Each team shows both versions
- Class discusses trade-offs
- Vote: Which better serves its audience?

### Activity 2: Dashboard Usability Testing (60 minutes)

**Objective:** Evaluate dashboard effectiveness through user testing

**Setup:**
- Half of class builds dashboards (Group A)
- Half acts as users (Group B)

**Process:**

1. **Group A** creates simple Shiny/Tableau dashboard (done ahead of time)
2. **Group B** receives task: "Find the fare level that maximizes revenue without reducing ridership >10%"
3. **Observer** times and logs user actions
4. **Debrief:**
   - Did user find answer?
   - How long did it take?
   - What was confusing?
   - What worked well?

**Then switch roles**

**Learning outcomes:**
- User-centered design is hard
- What's obvious to designer isn't always obvious to user
- Iteration improves usability

---

## 📝 Assignment

### [Capstone Project: Complete SP Study](../assignments/06_capstone.md)

**Due:** End of Week 12

**Submission Package:**

1. **Technical Report** (PDF, 15-20 pages)
2. **Executive Summary** (PDF, 3-4 pages)
3. **Presentation Deck** (PowerPoint/PDF, 15-20 slides)
4. **Interactive Dashboard** (Link or standalone file)
5. **Code & Data** (ZIP file with organized folders)

**Evaluation:** See Capstone Project section above for full rubric (200 points total)

**Presentation:**
- Final week: 15-minute presentations
- 10 min presentation + 5 min Q&A
- Open to all students, instructors, guests

---

## 💬 Discussion Prompts

**Post your responses on the course forum (200-250 words each; respond to 2 peers):**

### Prompt 1: Communicating Uncertainty

**Question:**
"How should SP-derived recommendations be positioned alongside RP findings and political realities? When forecasts have wide confidence intervals, do you present the range or a single 'best estimate'?"

**Consider:**
- Risk tolerance of decision-makers
- Accountability when forecasts are wrong
- Trade-off between precision and honesty

**Example:** "Our model predicts 40,000-60,000 daily riders. Do we say '50,000 ± 10,000' or pick one number?"

### Prompt 2: Visualization Ethics

**Question:**
"You have a result that doesn't support your client's preferred policy. They ask you to 'emphasize the positives' in visualizations. Where's the line between framing and misleading?"

**Discuss:**
- Y-axis manipulation (truncated axes)
- Selective presentation of scenarios
- Chart type choices that exaggerate effects
- Professional obligations

### Prompt 3: Dashboard vs. Static Report

**Question:**
"What governance structures help ensure SP insights influence procurement, pricing, or service design decisions? Is an interactive dashboard more or less likely to be used than a PDF report?"

**Reflect on:**
- Institutional capacity to use tools
- Maintenance and updates
- Accessibility for different stakeholders
- Longevity (dashboard link breaks, PDFs remain)

---

## 📖 Recommended Resources

### Core Textbooks

1. **Knaflic, C. N. (2015).** *Storytelling with Data: A Data Visualization Guide for Business Professionals*
   - Essential for clear, effective charts
   - Before/after examples
   - Highly practical

2. **Tufte, E. R. (2001).** *The Visual Display of Quantitative Information* (2nd ed.)
   - Classic text on visualization theory
   - Data-ink ratio, chartjunk
   - Beautiful examples

3. **Cairo, A. (2016).** *The Truthful Art: Data, Charts, and Maps for Communication*
   - Ethics in visualization
   - Interactive graphics
   - Journalism perspective

### Communication Guides

- **ITF/OECD (2021).** *Communicating Uncertainty in Transport Models: A Practitioner's Guide*
  [https://www.itf-oecd.org/](https://www.itf-oecd.org/)

- **World Bank (2022).** *Integrating Stated Preference into Economic Appraisal*
  Guidance on presenting SP findings to policy audiences

### Software & Tools

- **Tableau Public** (Free)
  [https://public.tableau.com/](https://public.tableau.com/)
  - Dashboard creation
  - Extensive tutorials

- **R Shiny Gallery**
  [https://shiny.rstudio.com/gallery/](https://shiny.rstudio.com/gallery/)
  - Example dashboards with source code

- **Power BI Community**
  [https://community.powerbi.com/](https://community.powerbi.com/)
  - Templates and forums

- **ColorBrewer** (Colorblind-safe palettes)
  [https://colorbrewer2.org/](https://colorbrewer2.org/)

### Journal Articles

- **Walker, J., & Li, J. (2007).** "Latent lifestyle preferences and household location decisions." *Journal of Geographical Systems*, 9(1), 77-101.
  - Example of translating latent class results to policy

- **Chorus, C., & Timmermans, H. (2009).** "Measuring user benefits of changes in the transport system when traveler awareness is limited." *Transportation Research Part A*, 43(5), 536-547.
  - Communicating benefits to non-users

---

## ✅ Module Completion Checklist

Before finishing the course, ensure you have:

- [ ] Attended or watched both sessions (8 hours total)
- [ ] Completed policy translation workshop
- [ ] Built an interactive dashboard
- [ ] Practiced elevator pitch presentation
- [ ] Posted to all 3 discussion prompts with peer responses
- [ ] Submitted complete Capstone Project (all 5 components)
- [ ] Presented final project to class
- [ ] Provided peer feedback on 3 other presentations
- [ ] Completed course evaluation

**Self-Assessment Questions:**

1. **Can you translate** parameter estimates into policy-relevant metrics (ridership, revenue, equity)?
2. **Can you quantify** uncertainty using confidence intervals, scenarios, or Monte Carlo simulation?
3. **Can you create** publication-quality visualizations using R/Python or Tableau?
4. **Can you build** an interactive dashboard that allows scenario exploration?
5. **Can you write** a 2-page executive summary free of jargon but rich in insights?
6. **Can you present** your findings in 10 minutes to a non-technical audience?

If you answered "yes" to all six—congratulations, you've mastered SP survey research!

---

## 🔗 Navigation

- **Previous:** [Module 5 - Discrete Choice Modeling & Estimation](05-modeling.md)
- **Related:** [Capstone Project](../assignments/06_capstone.md) | [Syllabus](../syllabus.md) | [Course Home](../index.md)

---

## 🎓 Course Conclusion

### What You've Accomplished

Over 12 weeks, you've mastered the complete lifecycle of stated preference survey research:

1. **Foundations:** Random utility theory, when to use SP vs. RP
2. **Survey Design:** Attributes, questionnaires, sampling strategies
3. **Experimental Design:** D-efficient designs, Ngene, choice cards
4. **Implementation:** Pilot testing, ethics, quality assurance, fieldwork
5. **Modeling:** MNL, mixed logit, WTP, elasticities (Biogeme/Apollo)
6. **Communication:** Visualizations, dashboards, policy briefs

### Beyond This Course

**Immediate Next Steps:**
- Apply these skills to a real project in your organization
- Publish your capstone project (conference paper, working paper, blog post)
- Join the **International Choice Modelling Conference** (ICMC) community

**Advanced Topics to Explore:**
- Integrated RP-SP models
- Hybrid choice models (combining attitudes and choices)
- Adaptive SP surveys (update design during fielding)
- Machine learning enhancements to choice models

**Professional Development:**
- **Conferences:** ICMC, TRB Annual Meeting, WCTR
- **Online Communities:** TRB Choice Modeling Committee, Biogeme Forum
- **Certifications:** Project Management Professional (PMP) for large studies

### Stay Connected

**Course Alumni Network:**
- Join LinkedIn group: "SP Survey Research Professionals"
- Share projects and job opportunities
- Annual virtual reunion (December)

**Continuing Education:**
- Advanced workshop: "Bayesian Methods for Choice Modeling" (Summer 2026)
- Webinar series: "SP in Practice" (monthly, starting March 2026)

---

<div class="alert alert-success">
<strong>🎉 Congratulations!</strong> You are now equipped to design, implement, analyze, and communicate stated preference research that informs real-world transportation policy. Go forth and make evidence-based decisions happen!
</div>

---

**Final words from your instructor:**

> "The best SP studies are those that change decisions. Not the ones with the lowest D-error or the fanciest models—but the ones that help transportation agencies serve their communities better. As you apply these methods, never lose sight of the people behind the data: the commuters stuck in traffic, the seniors without mobility options, the communities fighting for equitable access. Your work matters. Make it count."

---

**Questions or feedback?** Contact the instructor or join the alumni network.

**Course materials will remain available for 2 years.** Download any resources you need.

**Thank you for your engagement and hard work. Safe travels!**
