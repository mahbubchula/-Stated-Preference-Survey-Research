---
title: "Module 3 - Experimental Design"
layout: default
nav_order: 12
---

# Module 3: Experimental Design & Efficient Choice Tasks

<div class="alert alert-info">
<strong>Duration:</strong> 2 weeks | <strong>Effort:</strong> 12-14 hours | <strong>Level:</strong> Advanced
</div>

---

## 📋 Overview

With your survey design brief complete, it's time to construct the experimental design—the mathematical foundation that determines which combinations of attribute levels respondents will evaluate. This module moves from conceptual planning to statistical optimization, teaching you how to create choice experiments that maximize information while minimizing respondent burden.

You'll learn to distinguish between orthogonal and efficient designs, work with design generation software (Ngene, R idefix, Python), evaluate design quality using statistical metrics, and create choice cards that are both statistically rigorous and cognitively accessible.

---

## 🎯 Learning Objectives

By completing this module, you will be able to:

1. **Distinguish** between full factorial, fractional factorial, orthogonal, D-efficient, and Bayesian designs and select appropriate approaches for different research contexts
2. **Generate** experimental designs using commercial (Ngene) and open-source (R idefix, Python pylogit) software with appropriate priors and constraints
3. **Evaluate** design quality using D-error, S-efficiency, A-error, level balance, and correlation diagnostics
4. **Implement** pivot designs that personalize choice scenarios based on respondent characteristics
5. **Create** visually effective choice cards using textual, tabular, and graphical presentation formats
6. **Apply** blocking strategies to distribute choice tasks across respondents while maintaining statistical efficiency

---

## 🧮 Experimental Design Fundamentals

### What is an Experimental Design?

An **experimental design** is a systematic plan for constructing choice tasks that specifies:
- Which attribute levels appear together in each alternative
- Which alternatives appear together in each choice task
- Which choice tasks each respondent sees

**Goal:** Estimate preference parameters (β coefficients) with maximum statistical precision given constraints on respondent burden.

### The Design Matrix

A design matrix **X** has dimensions:
- **Rows:** choice tasks × alternatives
- **Columns:** attributes (or dummy-coded levels)

**Example:** 3 attributes, 2 alternatives, 8 tasks = 16 rows

```
Task | Alt | Price | Time | Comfort
-----|-----|-------|------|--------
  1  |  A  |   3   |  30  |   1
  1  |  B  |   4   |  25  |   0
  2  |  A  |   5   |  20  |   1
  2  |  B  |   3   |  35  |   0
 ... | ... |  ...  | ...  |  ...
```

---

## 🔬 Types of Experimental Designs

### 1. Full Factorial Design

**Definition:** Every possible combination of attribute levels appears

**Example:** 3 attributes with 4, 3, 3 levels respectively
- Total combinations: 4 × 3 × 3 = **36 profiles**
- With 2 alternatives per task: 36 × 35 / 2 = **630 possible pairs**

**Advantages:**
- Complete coverage of design space
- No confounding between attributes
- Can estimate all main effects and interactions

**Disadvantages:**
- Becomes enormous quickly (dimensionality curse)
- Respondent burden is prohibitive
- Many combinations are unrealistic or redundant

**When to use:** Very small designs only (≤ 3 attributes, ≤ 3 levels each)

### 2. Fractional Factorial Design

**Definition:** A carefully selected subset of the full factorial

**Example:** 1/6 fractional factorial of above = **6 profiles**

**Construction:**
- Use orthogonal array (OA) designs
- Ensures attribute levels are uncorrelated
- Sacrifices interaction estimation for efficiency

**Common Notation:**
- L₁₈(3⁷): 18 runs, up to 7 attributes with 3 levels each
- L₁₆(4⁵): 16 runs, up to 5 attributes with 4 levels each

**Advantages:**
- Dramatically reduces number of tasks
- Maintains statistical balance
- Standard OA tables readily available

**Disadvantages:**
- Fixed structure, less flexibility
- Cannot estimate interactions
- May include unrealistic combinations
- Not optimized for specific utility functions

**When to use:** Early-stage exploratory studies, baseline comparisons

### 3. Orthogonal Design

**Definition:** Designed so attribute levels are statistically independent (uncorrelated)

**Mathematical Property:**
```
X'X is diagonal (or proportional to identity matrix)
```

**Implications:**
- Attribute effects can be estimated independently
- Variance inflation factors (VIF) = 1
- No multicollinearity

**Construction Methods:**
- Orthogonal arrays (OA)
- Rotation designs
- Fractional factorial generators

**Example Orthogonal Design:**

| Task | Price | Time | Comfort |
|------|-------|------|---------|
| 1    | Low   | Short | High   |
| 2    | Low   | Long  | Low    |
| 3    | High  | Short | Low    |
| 4    | High  | Long  | High   |

Check: Correlation(Price, Time) = 0, Correlation(Price, Comfort) = 0, etc.

**Advantages:**
- Simple interpretation
- Minimum variance for main effects
- No confounding

**Disadvantages:**
- Doesn't account for prior knowledge about parameters
- May require more tasks than efficient designs
- Optimizes for orthogonality, not parameter precision

**When to use:** No prior information, need simple interpretability

### 4. D-Efficient Design

**Definition:** Designed to minimize the determinant of the asymptotic variance-covariance (AVC) matrix

**Statistical Objective:**
```
Minimize: |AVC(β)| = |(X'X)⁻¹|

Equivalently, maximize: D-efficiency = |X'X|^(1/K)
```

Where K = number of parameters

**D-error:**
```
D-error = |AVC|^(1/K) = |(X'X)⁻¹|^(1/K)
```

Lower D-error = better design

**Process:**
1. Specify utility function with prior parameter values (β priors)
2. Use algorithm (coordinate exchange, modified Fedorov) to search design space
3. Find design that minimizes determinant of AVC matrix
4. Iterate to improve

**Advantages:**
- Uses prior knowledge to optimize information
- Requires fewer tasks than orthogonal for same precision
- Flexible: can handle constraints, pivot designs, labeled alternatives
- Industry standard for SP surveys

**Disadvantages:**
- Requires reasonable priors (wrong priors = poor design)
- Computationally intensive
- Results vary across software implementations

**When to use:** You have prior information from literature, focus groups, or pilot data

### 5. Bayesian Efficient Design

**Definition:** Accounts for uncertainty in priors by integrating over a distribution of parameter values

**Objective:**
```
Minimize: DB-error = E[D-error | distribution of β]
```

**Prior Specification:**
- Mean: expected parameter value
- Standard deviation: uncertainty about that value

**Example:**
```
β_price ~ Normal(mean = -0.5, sd = 0.2)
β_time  ~ Normal(mean = -0.3, sd = 0.15)
```

**Advantages:**
- More robust to prior misspecification
- Explicitly models uncertainty
- Better performance when priors are imprecise

**Disadvantages:**
- Requires distributional assumptions
- Computationally expensive (Monte Carlo integration)
- May still perform poorly if prior distribution is wrong

**When to use:** You have prior estimates but are uncertain about them (e.g., from small pilot, transferred from different context)

### 6. Pivot Design

**Definition:** Attributes are defined relative to each respondent's current situation (status quo)

**Mechanism:**
- Respondent reports current alternative (e.g., "I pay $3.50, trip takes 35 min")
- Alternative attribute levels are generated as % changes or absolute shifts
- Creates personalized choice tasks

**Example:**

**Respondent's Status Quo:** $3.50 fare, 35 min travel time

**Generated Alternatives:**
- Alt A: $3.00 (-14%), 30 min (-14%)
- Alt B: $4.00 (+14%), 40 min (+14%)
- Alt C: Status quo ($3.50, 35 min)

**Advantages:**
- Increases realism (scenarios close to respondent's experience)
- Reduces variance in choices (more variation around familiar point)
- Can improve engagement and completion rates

**Disadvantages:**
- Requires warm-up questions to collect status quo
- More complex programming
- Design efficiency depends on variation in population status quo

**When to use:** Evaluating changes to existing service, heterogeneous user base

---

## 🛠️ Design Generation Software

### Ngene (ChoiceMetrics)

**Platform:** Windows standalone application

**Strengths:**
- Industry standard for transport SP studies
- Excellent documentation and examples
- Handles complex designs (pivot, labeled alternatives, priors, constraints)
- Built-in diagnostics (D-error, S-estimate, correlations)

**Basic Syntax:**

```
Design
;alts = alt1, alt2, alt3
;rows = 12
;eff = (mnl, d)
;model:
U(alt1) = b1 * price[2,3,4,5] + b2 * time[20,30,40,50] /
U(alt2) = b1 * price + b2 * time /
U(alt3) = b0
$

```

**Key Commands:**
- `alts`: define alternatives
- `rows`: number of choice tasks
- `eff`: efficiency criterion (mnl, d = D-efficient MNL)
- `model`: utility specifications with priors
- `[levels]`: attribute levels

**Example with Priors:**

```
;model:
U(alt1) = b1[-0.5] * price[2,3,4,5] +
          b2[-0.3] * time[20,30,40,50] +
          b3[0.8] * comfort[0,1] /
U(alt2) = b1 * price + b2 * time + b3 * comfort /
U(alt3) = b0[0]
```

Numbers in square brackets `[-0.5]` are prior parameter values.

**Constraints Example:**

```
;cond:
if(alt1.price > alt2.price, alt1.time < alt2.time)
```

This ensures if Alt 1 is more expensive, it must be faster.

**Academic License:** Free for students/faculty with `.edu` email

### R Package: idefix

**Platform:** Open-source R

**Strengths:**
- Free and open-source
- Integrates with R ecosystem for data analysis
- Adaptive designs (update design during fielding)
- Good for Bayesian designs

**Installation:**
```r
install.packages("idefix")
library(idefix)
```

**Basic Example:**

```r
# Define attributes and levels
attributes <- list(
  price = c(2, 3, 4, 5),
  time = c(20, 30, 40, 50),
  comfort = c(0, 1)
)

# Prior parameter values (β)
priors <- c(-0.5, -0.3, 0.8)

# Generate D-efficient design
design <- Modfed(
  cand.set = attributes,
  n.sets = 12,  # 12 choice tasks
  n.alts = 2,   # 2 alternatives per task
  par.draws = priors,
  no.choice = FALSE
)

# View design
design$design
```

**Bayesian Design:**

```r
# Prior distributions
mu <- c(-0.5, -0.3, 0.8)
sigma <- diag(c(0.1, 0.1, 0.2))  # variance

design.bayesian <- Modfed(
  cand.set = attributes,
  n.sets = 12,
  n.alts = 2,
  par.draws = MASS::mvrnorm(100, mu, sigma),
  no.choice = FALSE
)
```

### Python: pylogit / choice-learn

**Platform:** Open-source Python

**Strengths:**
- Integration with pandas, numpy, scikit-learn
- Good for researchers familiar with Python data science stack
- Can link design generation to estimation pipeline

**Installation:**
```python
pip install pylogit
pip install choice-learn
```

**Example (using choice-learn):**

```python
import numpy as np
from choice_learn.design import create_design

# Define attribute levels
attributes = {
    'price': [2, 3, 4, 5],
    'time': [20, 30, 40, 50],
    'comfort': [0, 1]
}

# Prior parameters
priors = {'price': -0.5, 'time': -0.3, 'comfort': 0.8}

# Generate efficient design
design = create_design(
    attributes=attributes,
    priors=priors,
    n_tasks=12,
    n_alts=2,
    criterion='D-efficiency'
)

print(design)
```

### Comparison Table

| Feature | Ngene | R idefix | Python |
|---------|-------|----------|--------|
| **Cost** | Free (academic) / $495 (commercial) | Free | Free |
| **Ease of Use** | ⭐⭐⭐⭐ GUI + script | ⭐⭐⭐ Code | ⭐⭐⭐ Code |
| **Documentation** | ⭐⭐⭐⭐⭐ Excellent | ⭐⭐⭐ Good | ⭐⭐ Fair |
| **Flexibility** | ⭐⭐⭐⭐⭐ Very high | ⭐⭐⭐⭐ High | ⭐⭐⭐ Moderate |
| **Speed** | ⭐⭐⭐⭐ Fast | ⭐⭐⭐ Moderate | ⭐⭐⭐ Moderate |
| **Bayesian Designs** | ✅ Yes | ✅ Yes | ✅ Yes (limited) |
| **Adaptive Designs** | ❌ No | ✅ Yes | ⚠️ Experimental |
| **Community** | Large (transport) | Moderate (stats) | Growing |

**Recommendation:** Use Ngene for professional/commercial projects; idefix for academic research with adaptive needs; Python for integrated pipelines.

---

## 📊 Design Quality Metrics

### D-Error (Primary Metric)

**Formula:**
```
D-error = |AVC|^(1/K) = |(X'X)⁻¹|^(1/K)
```

**Interpretation:**
- Lower is better
- Typical values: 0.05 to 0.50 for well-designed studies
- Absolute value less important than relative comparison

**What it measures:** Average variance across all parameters

**Use:** Compare alternative designs for same study

**Example:**
- Design A: D-error = 0.18
- Design B: D-error = 0.12
- Design B is more efficient (37% reduction in average parameter variance)

### A-Error (Trace of AVC Matrix)

**Formula:**
```
A-error = trace(AVC) / K
```

**Interpretation:**
- Arithmetic mean of parameter variances
- Lower is better
- More sensitive to poorly estimated individual parameters than D-error

**Use:** When you care about precision of specific parameters (e.g., value of time)

### S-Efficiency (Sample Size Efficiency)

**Definition:** Ratio of sample size needed with orthogonal design vs. efficient design for same precision

**Formula:**
```
S-efficiency = (D-error_orthogonal / D-error_efficient)^2
```

**Interpretation:**
- Values > 1 indicate efficient design is better
- S = 2.0 means you need only 50% sample size vs. orthogonal
- Typical values: 1.5 to 3.0 for well-optimized designs

**Example:**
- Orthogonal design: D-error = 0.20
- Efficient design: D-error = 0.10
- S-efficiency = (0.20/0.10)² = 4.0
- Efficient design needs only 25% of sample (4× improvement)

### Level Balance

**Definition:** How evenly attribute levels appear across the design

**Ideal:** Each level appears equally often

**Example:**

**Balanced:**
| Price | Count |
|-------|-------|
| $2    | 6     |
| $3    | 6     |
| $4    | 6     |
| $5    | 6     |
Total: 24 alternatives across 12 tasks

**Unbalanced:**
| Price | Count |
|-------|-------|
| $2    | 10    |
| $3    | 8     |
| $4    | 4     |
| $5    | 2     |

**Why it matters:**
- Unbalanced designs may struggle to estimate preferences for rare levels
- Can introduce bias if respondents notice imbalance

**Acceptable Deviation:** ±20% from perfect balance

### Correlation Matrix

**Definition:** Correlation between attributes across design

**Ideal (Orthogonal):**
```
         Price   Time   Comfort
Price     1.00   0.00    0.00
Time      0.00   1.00    0.00
Comfort   0.00   0.00    1.00
```

**Acceptable (Efficient):**
```
         Price   Time   Comfort
Price     1.00   0.15   -0.08
Time      0.15   1.00    0.22
Comfort  -0.08   0.22    1.00
```

**Threshold:** Absolute correlations < 0.30 are generally acceptable

**Why it matters:** High correlations inflate standard errors (multicollinearity)

### Overlap

**Definition:** Frequency with which the same level appears in multiple alternatives within a task

**Example:**

**No Overlap (Good):**
```
Task 1:
  Alt A: Price = $3, Time = 30 min
  Alt B: Price = $4, Time = 40 min
```

**Overlap (Poor):**
```
Task 2:
  Alt A: Price = $3, Time = 30 min
  Alt B: Price = $3, Time = 40 min  ← Price overlaps!
```

**Why it matters:**
- Reduces information about attribute importance
- Respondents can't trade off that attribute

**Target:** < 10% overlap across all attributes and tasks

---

## 🎨 Creating Effective Choice Cards

### Design Principles

1. **Clarity:** Respondents instantly understand the task
2. **Consistency:** Same format across all tasks
3. **Simplicity:** Minimize cognitive load
4. **Realism:** Scenarios feel plausible
5. **Neutrality:** No visual bias toward any alternative

### Presentation Formats

#### Format 1: Tabular (Classic)

**Best for:** Quantitative attributes, 2-3 alternatives

**Example:**

```
╔══════════════════════════════════════════════════════╗
║           CHOICE TASK 5 of 12                        ║
╠══════════════════════════════════════════════════════╣
║  Which option would you choose for your commute?     ║
╠══════════════╦════════════╦════════════╦═════════════╣
║              ║  Option A  ║  Option B  ║  Option C   ║
╠══════════════╬════════════╬════════════╬═════════════╣
║ Fare         ║   $3.50    ║   $2.50    ║   $4.00     ║
║ Travel Time  ║   30 min   ║   40 min   ║   25 min    ║
║ Wait Time    ║   8 min    ║   12 min   ║   5 min     ║
║ Comfort      ║  Seated    ║  Standing  ║  Seated     ║
╠══════════════╬════════════╬════════════╬═════════════╣
║ YOUR CHOICE: ║     ☐      ║     ☐      ║     ☐       ║
╚══════════════╩════════════╩════════════╩═════════════╝
```

**Pros:** Clear, compact, easy to scan
**Cons:** Can feel clinical, less engaging

#### Format 2: Graphical/Icon-Based

**Best for:** Mixed attributes, younger/visual audiences, mobile surveys

**Example:**

```
┌────────────────────────────────────┐
│  OPTION A                          │
├────────────────────────────────────┤
│  💵 Cost: $3.50                    │
│  ⏱️ Travel time: 30 minutes         │
│  🚏 Wait: 8 minutes                │
│  💺 Seating: Guaranteed seat       │
│                                    │
│        [ SELECT OPTION A ]         │
└────────────────────────────────────┘

┌────────────────────────────────────┐
│  OPTION B                          │
├────────────────────────────────────┤
│  💵 Cost: $2.50                    │
│  ⏱️ Travel time: 40 minutes         │
│  🚏 Wait: 12 minutes               │
│  🧍 Seating: Might need to stand   │
│                                    │
│        [ SELECT OPTION B ]         │
└────────────────────────────────────┘
```

**Pros:** Engaging, mobile-friendly, reduces text density
**Cons:** Icons must be universally understood, accessibility concerns

#### Format 3: Narrative/Scenario-Based

**Best for:** Complex decisions, policy contexts requiring explanation

**Example:**

```
─────────────────────────────────────────────
Imagine you're planning your morning commute.
You have two transit options available:
─────────────────────────────────────────────

RAPID BUS SERVICE
  ✓ Departs every 8 minutes
  ✓ Gets you to work in 30 minutes
  ✓ Costs $3.50 per trip
  ✓ Clean buses with comfortable seating
  ✓ Free Wi-Fi available

LOCAL BUS SERVICE
  ✓ Departs every 15 minutes
  ✓ Gets you to work in 45 minutes
  ✓ Costs $2.50 per trip
  ✓ Standard buses, seats usually available
  ✓ No Wi-Fi

Which service would you choose?
  ○ Rapid Bus
  ○ Local Bus
  ○ Neither (I'd drive instead)
```

**Pros:** Engaging, provides context, natural language
**Cons:** Longer, harder to scan, takes more time

### Visual Hierarchy Tips

1. **Use white space generously** - Don't cram information
2. **Align elements consistently** - Creates order and predictability
3. **Highlight differences** - Bold or color-code varying attributes
4. **De-emphasize similarities** - Gray out or minimize constant attributes
5. **Group related information** - Keep attribute/value pairs together

### Accessibility Considerations

- **Color blindness:** Don't rely solely on color to convey information
- **Screen readers:** Use semantic HTML (proper table headers, labels)
- **Font size:** Minimum 14pt for body text, 18pt for important info
- **Contrast ratio:** WCAG 2.1 Level AA requires 4.5:1 for normal text
- **Mobile responsiveness:** Test on smartphones (40-50% of respondents)

---

## 🌍 Real-World Applications & Case Studies

### Case Study 1: High-Speed Rail Attribute Optimization (California)

**Challenge:** Design HSR service to compete with air travel between SF and LA

**Attributes (7 total):**
1. Travel time (2h 40min, 3h 00min, 3h 20min, 3h 40min)
2. Fare ($89, $119, $149, $179)
3. Frequency (every 30min, 1hr, 2hr)
4. Stations (2 stops, 4 stops, 6 stops)
5. Seat type (economy, business class)
6. Wi-Fi (yes/no)
7. On-time performance (85%, 90%, 95%)

**Design Approach:**
- **Initial orthogonal design:** 32 tasks required
- **Bayesian efficient design:** 12 tasks achieved S-efficiency = 2.4
- **Priors:** Derived from European HSR studies (France, Spain)
- **Blocking:** 3 blocks of 4 tasks each, randomly assigned

**Design Specifications (Ngene Syntax):**

```
Design
;alts = hsr, air, drive
;rows = 12
;block = 3
;eff = (mnl, d, mean)
;bdraws = sobol(500)
;model:
U(hsr) =
  b1.mean[-0.02] * time[160,180,200,220] +
  b2.mean[-0.01] * fare[89,119,149,179] +
  b3.mean[0.4] * frequency[0.5,1,2] +
  b4.mean[-0.1] * stops[2,4,6] +
  b5.mean[0.6] * business[0,1] +
  b6.mean[0.3] * wifi[0,1] +
  b7.mean[0.02] * ontime[85,90,95] /
U(air) = ... /
U(drive) = b0[0]
$
```

**Results:**
- D-error: 0.094
- All attribute correlations < |0.20|
- Perfect level balance
- Sample size: n=1,200 → precision ±$1.80 for value of time

**Key Insight:** Efficient design reduced survey length by 62%, increasing completion rate from 68% to 84%.

### Case Study 2: Urban Micromobility Pivot Design (Portland)

**Challenge:** Estimate willingness to switch from personal car to e-scooter/e-bike

**Pivot Strategy:**
- Ask respondents about their most recent car trip < 3 miles
- Capture: distance, duration, parking cost
- Generate alternatives as ±20% variations

**Attributes:**
1. Trip time (pivot ±20%, ±40%)
2. Cost (pivot ±30%, ±60%)
3. Weather protection (none, rain gear provided, covered stations)
4. Parking convenience (same as current, 1 block farther, 2 blocks farther)

**Example Respondent Flow:**

**Q: "Your last short car trip was to:"**
- Grocery store
- 1.8 miles away
- Took 12 minutes
- Parking was free but took 3 minutes to find

**Generated Choice Task:**

```
Option A: Continue driving
  • Time: 12 minutes driving + 3 min parking = 15 min
  • Cost: $0 (free parking)
  • Convenience: Park at store entrance

Option B: E-scooter
  • Time: 18 minutes (50% longer, includes walk to scooter)
  • Cost: $2.50
  • Weather: No protection (rain gear not provided)
  • Convenience: Dock located 1 block from store

Which would you choose?
```

**Design Outcomes:**
- 8 tasks per respondent, 2 alternatives each
- Realistic scenarios (personalized to actual trips)
- D-error: 0.11 (comparable to non-pivot design with 50% more tasks)
- Completion rate: 91% (vs. 78% for generic scenarios in pilot)

**Lesson Learned:** Pivot designs require careful programming but dramatically improve engagement.

### Case Study 3: Freight Rail Corridor Pricing (Multi-Attribute Constraints)

**Challenge:** Price rail service for freight shippers; avoid unrealistic combinations

**Attributes:**
1. Shipping cost ($/container)
2. Transit time (days)
3. Reliability (on-time %)
4. Damage rate (% claims)

**Constraint Requirements:**
- Lower cost cannot come with better reliability (physically implausible)
- Faster service must cost more
- Damage rate independent but bounded (0.5% to 3%)

**Ngene Constraint Syntax:**

```
;cond:
if(alt1.cost < alt2.cost, alt1.time >= alt2.time),
if(alt1.time < alt2.time, alt1.cost > alt2.cost),
alt1.damage <= 3 and alt1.damage >= 0.5,
alt2.damage <= 3 and alt2.damage >= 0.5
```

**Challenge Encountered:**
- Initial design had 15% infeasible combinations rejected
- Required 10,000+ iterations to find 12 valid tasks
- Generation time: 45 minutes

**Solution:**
- Relaxed constraints slightly (allowed ties)
- Pre-generated candidate set meeting constraints
- Used restricted candidate set in Fedorov algorithm
- Generation time reduced to 3 minutes

**Result:**
- 12 tasks, D-error = 0.15
- 100% plausible combinations
- Estimated value of time: $180/day (±$22, 95% CI)

---

## ⚙️ Session Breakdown

### Session 1: Design Theory & Evaluation (4 hours)

**Part 1: Lecture - Design Typology (60 min)**
- Full factorial → fractional factorial → orthogonal → efficient
- Mathematical foundations: AVC matrix, determinant, D-error
- When to use each approach
- Prior specification strategies

**Part 2: Interactive Computation Lab (90 min)**

**Exercise 1: Manual D-error Calculation (30 min)**
- Provide small design matrix (4 tasks × 2 alts × 3 attributes)
- Calculate X'X matrix by hand
- Compute determinant
- Calculate D-error
- **Goal:** Demystify "black box" metrics

**Exercise 2: R idefix Walkthrough (30 min)**
```r
# Load library
library(idefix)

# Define candidate set
cand <- Profiles(
  lvls = list(price = c(2,3,4,5),
              time = c(20,30,40,50),
              comfort = c(0,1))
)

# Generate design
des <- Modfed(
  cand.set = cand,
  n.sets = 8,
  n.alts = 2,
  par.draws = c(-0.5, -0.3, 0.8),
  no.choice = FALSE
)

# Examine output
des$design        # Design matrix
des$error.measures  # D-error, A-error
```

**Exercise 3: Compare Designs (30 min)**
- Generate 3 designs: orthogonal, D-efficient (good priors), D-efficient (bad priors)
- Compare D-errors
- Discuss sensitivity to prior misspecification

**Part 3: Design Diagnostics Quiz (30 min)**

Students receive 3 design outputs and must identify issues:

**Design A:**
- D-error: 0.08
- Correlations: all < 0.10
- Level balance: Price level "$5" appears only 2 times out of 24
- **Issue:** Unbalanced levels → poor precision for high price

**Design B:**
- D-error: 0.25
- Correlations: Price-Time = 0.68
- Level balance: Perfect
- **Issue:** High correlation → multicollinearity

**Design C:**
- D-error: 0.12
- Correlations: all < 0.15
- Level balance: Perfect
- Overlap: 40% of tasks have same price in both alternatives
- **Issue:** High overlap → reduced information

**Part 4: Wrap-Up & Assignment Prep (30 min)**

### Session 2: Ngene Workshop & Choice Card Prototyping (4 hours)

**Part 1: Ngene Demonstration (60 min)**

**Live Coding Session:**

```
Design
;alts = bus, rail, drive
;rows = 12
;eff = (mnl, d)
;model:
U(bus) = b1[-0.05] * fare[2.5,3,3.5,4] +
         b2[-0.03] * time[25,30,35,40] +
         b3[0.8] * comfort[0,1] /
U(rail) = b1 * fare + b2 * time + b3 * comfort /
U(drive) = b0[0]
$
```

**Step-by-step:**
1. Define alternatives
2. Set number of rows (tasks)
3. Specify efficiency criterion
4. Write utility functions
5. Add priors in brackets
6. Define attribute levels in brackets
7. Run and interpret output

**Output Interpretation:**
- D-error
- S-estimate (standard errors)
- Correlation matrix
- Level balance table
- Sample size recommendation

**Part 2: Design Lab Rotations (90 min)**

**Scenario:** City Bus Fare Reform

Teams rotate through 3 stations:

**Station 1: Basic Design (30 min)**
- 4 attributes, 3-4 levels each
- Generate orthogonal design
- Generate D-efficient design
- Compare metrics

**Station 2: Constrained Design (30 min)**
- Add constraint: "If fare increases, time must decrease"
- Generate feasible design
- Assess impact on D-error

**Station 3: Pivot Design (30 min)**
- Implement pivot around respondent's current fare ($2.75 ± 20%)
- Test with different baseline values
- Examine level distributions

**Part 3: Choice Card Critique & Redesign (60 min)**

**Activity:**
1. Show poorly designed choice card (cluttered, confusing, biased)
2. Teams identify 5+ problems
3. Redesign using best practices
4. Present to class (5 min per team)
5. Peer voting on best redesign

**Poor Example Issues:**
- Tiny font (9pt)
- 5 alternatives (overwhelming)
- Inconsistent attribute order across alternatives
- Use of jargon ("IVT", "OVT")
- No visual hierarchy
- Green color for "expensive" option (misleading)

**Part 4: Blocking & Randomization (30 min)**

**Lecture:**
- Why block? (Reduce respondent burden, test for order effects)
- How to block in Ngene:
```
;block = 3  # Divides design into 3 blocks
```
- Randomization of task order
- Randomization of alternative position (left/right)

**Exercise:**
Generate 24-task design, block into 4 sets of 6 tasks, assign to respondents

---

## 🔬 Lab Activities

### Activity 1: Design Surgery (90 minutes)

**Objective:** Diagnose and fix a flawed experimental design

**Provided Materials:**
- Design matrix (Excel file) with 16 tasks, 3 alts, 5 attributes
- Summary statistics showing problems
- Brief on original research objectives

**Problems Embedded:**
1. One attribute (parking cost) has 80% overlap
2. Two attributes (time, distance) are correlated at r = 0.72
3. One level (premium service) appears only 3 times
4. D-error is 0.42 (very high)

**Task:**
1. Identify all issues (20 min)
2. Propose fixes (30 min):
   - Regenerate design with better constraints?
   - Drop problematic attribute?
   - Add more tasks?
3. Implement fix using Ngene or R (30 min)
4. Present before/after comparison (10 min)

**Deliverable:**
- Diagnosis memo (1 page)
- Improved design matrix
- Comparison table of metrics

### Activity 2: Design Generation Tournament (60 minutes)

**Challenge:** Generate the most efficient design possible for a given scenario

**Scenario:**
- 5 attributes: fare (4 levels), time (4 levels), frequency (3 levels), comfort (3 levels), reliability (3 levels)
- 2 alternatives + opt-out
- Budget: 8 choice tasks per respondent

**Priors Provided:**
- β_fare = -0.08 (±0.02)
- β_time = -0.05 (±0.015)
- β_frequency = 0.3 (±0.1)
- β_comfort = 0.6 (±0.2)
- β_reliability = 0.04 (±0.01)

**Competition Rules:**
1. Teams have 45 minutes to generate design
2. Can use any software (Ngene, R, Python)
3. Must satisfy constraints:
   - Exactly 8 tasks
   - No more than 20% overlap
   - Level balance within ±15%

**Judging Criteria:**
1. D-error (60%)
2. Level balance (20%)
3. Correlation minimization (20%)

**Winner:** Team with lowest weighted score

**Prize:** Bragging rights + featured in course Hall of Fame

**Debrief:**
- Winning team presents strategy
- Compare approaches across teams
- Discuss trade-offs

---

## 📝 Assignment

### [Module 3 Efficient Design Package](../assignments/03_design_package.md)

**Objective:** Produce a complete experimental design ready for survey implementation

**Deliverables:**

**1. Design Specification Document (3-4 pages)**

Include:
- **Utility function:** Full specification with priors and justification
- **Prior derivation:** Where did priors come from? (literature, pilot, expert opinion)
- **Design parameters:** # tasks, # alternatives, blocking strategy
- **Constraints:** Any logical restrictions on attribute combinations
- **Software & settings:** Ngene syntax or R/Python code (appendix)

**2. Design Matrix (Excel/CSV)**

Columns:
- Task ID
- Block ID (if using blocking)
- Alternative ID
- Attribute 1, Attribute 2, ... Attribute N
- Version (if multiple designs)

**3. Design Diagnostics Report (2 pages)**

Must include:
- **D-error and A-error**
- **S-efficiency** (comparison to orthogonal baseline)
- **Correlation matrix** with interpretation
- **Level balance table** with acceptability assessment
- **Overlap statistics**
- **Sample size recommendation** for target precision

**4. Choice Card Prototypes (3 examples)**

Create visual mockups of 3 choice tasks showing:
- **Format:** Tabular, graphical, or narrative
- **Visual hierarchy:** Highlighting, spacing, typography
- **Mobile responsiveness:** How it looks on phone vs. desktop
- **Accessibility notes:** Color contrast, screen reader compatibility

Use PowerPoint, Figma, Adobe XD, or even hand sketches (photographed).

**5. Justification Memo (1 page)**

Answer:
- Why did you choose this design type (orthogonal vs. efficient vs. Bayesian)?
- How did you handle trade-offs (e.g., tasks vs. precision)?
- What are the 2-3 biggest risks to your design?
- If you could add one more feature (more tasks, attributes, constraints), what would it be?

**Submission Requirements:**
- Combined PDF + separate Excel file for design matrix
- Include all code (Ngene/R/Python) in appendix
- Filename: `M3_design_package_<lastname>.pdf`
- **Due:** End of Week 5

**Evaluation Rubric (100 points):**

| Component | Points | Criteria |
|-----------|--------|----------|
| Design specification | 20 | Clear utility functions, justified priors, appropriate constraints |
| Design quality | 30 | Low D-error, good balance, low correlations, minimal overlap |
| Diagnostics | 20 | Complete metrics, correct interpretation, actionable insights |
| Choice cards | 20 | Professional design, clear hierarchy, accessible, realistic |
| Justification | 10 | Critical thinking, acknowledges trade-offs, realistic about limitations |

---

## 💬 Discussion Prompts

**Post your responses on the course forum (200-250 words each; respond to 2 peers):**

### Prompt 1: Pivot vs. Generic Designs

**Question:**
"When is a pivot design superior to a generic orthogonal or efficient design in transport pricing studies? Provide a specific example and discuss potential drawbacks."

**Consider:**
- Engagement and realism benefits
- Statistical efficiency implications
- Programming complexity
- Population heterogeneity

**Starter:**
"In congestion pricing studies, respondents' current travel costs vary from $0 (transit users) to $15+ (long-distance drivers). A pivot design could..."

### Prompt 2: Prior Sensitivity

**Question:**
"How do you balance attribute level realism with statistical efficiency? What happens when realistic level ranges produce high D-errors?"

**Trade-offs:**
- Wider ranges → more information but less realistic
- Narrow ranges → realistic but may not capture full sensitivity
- Interaction with priors

**Scenario:**
"You're studying EV adoption. Literature suggests β_price ≈ -0.003 ($/dollar). But your budget only allows $10k price increments. Your D-efficient design has D-error = 0.35. What do you do?"

### Prompt 3: The 'Perfect Design' Myth

**Question:**
"Ngene can generate thousands of designs with different random seeds, yielding slightly different D-errors (e.g., 0.082 vs. 0.088). How much effort should you invest in finding the 'optimal' design?"

**Discuss:**
- Diminishing returns of optimization
- Practical vs. theoretical efficiency
- When 'good enough' is actually good enough
- Real constraints (programming time, stakeholder review cycles)

---

## 📖 Recommended Resources

### Core Textbooks

1. **Rose, J. M., & Bliemer, M. C. J. (2014).** *Constructing Efficient Stated Choice Experimental Designs*
   - The definitive guide to efficient designs
   - Step-by-step Ngene tutorials
   - Available as working paper from University of Sydney

2. **Hensher, D. A., Rose, J. M., & Greene, W. H. (2015).** *Applied Choice Analysis* (2nd ed.)
   - Chapters 6-7: Experimental design theory and practice
   - Extensive Ngene examples
   - Companion website with datasets

3. **Kuhfeld, W. F. (2010).** *Marketing Research Methods in SAS: Experimental Design, Choice, Conjoint, and Graphical Techniques*
   - Free PDF (800+ pages) from SAS Institute
   - Chapter 5: Choice-based conjoint designs
   - Orthogonal array tables in appendices

### Journal Articles

- **Bliemer, M. C. J., & Rose, J. M. (2010).** "Construction of experimental designs for mixed logit models allowing for correlation across choice observations." *Transportation Research Part B*, 44(6), 720-734.

- **Ferrini, S., & Scarpa, R. (2007).** "Designs with a-priori information for nonmarket valuation with choice experiments." *Journal of Environmental Economics and Management*, 53(3), 342-363.
  - Bayesian design methods

- **Scarpa, R., & Rose, J. M. (2008).** "Design efficiency for non-market valuation with choice modelling." *Journal of Environmental Economics and Management*, 56(3), 269-281.

- **Bliemer, M. C. J., Rose, J. M., & Hess, S. (2008).** "Approximation of Bayesian efficiency in experimental choice designs." *Journal of Choice Modelling*, 1(1), 98-126.

### Software Documentation

- **Ngene User Manual** (ChoiceMetrics, 2024)
  [http://www.choice-metrics.com/download.html](http://www.choice-metrics.com/download.html)
  - 300+ page manual with examples
  - Syntax reference, case studies

- **R idefix Package Vignette**
  ```r
  vignette("idefix")
  ```
  - Adaptive design workflows
  - Bayesian updating examples

- **Sawtooth Software CBC Technical Paper**
  [https://sawtoothsoftware.com/resources/technical-papers](https://sawtoothsoftware.com/resources/technical-papers)
  - Alternative commercial platform
  - Good conceptual explanations

### Online Tutorials

- **Choice Modelling Centre** (University of Leeds)
  Video tutorials on Ngene, design evaluation
  [https://www.its.leeds.ac.uk/choices/](https://www.its.leeds.ac.uk/choices/)

- **Stated Choice Blog** by John Rose
  Monthly posts on design tips, common mistakes
  [https://statedchoice.wordpress.com/](https://statedchoice.wordpress.com/)

---

## ✅ Module Completion Checklist

Before moving to Module 4, ensure you have:

- [ ] Attended or watched both sessions (8 hours total)
- [ ] Completed D-error calculation exercise by hand
- [ ] Generated at least one design in Ngene or R idefix
- [ ] Participated in design critique activity
- [ ] Posted to all 3 discussion prompts with peer responses
- [ ] Submitted Module 3 Design Package
- [ ] Read Rose & Bliemer (2014) primer
- [ ] Reviewed Ngene syntax reference (key sections)
- [ ] Practiced creating choice card mockups

**Self-Assessment Questions:**

1. **Can you explain the difference** between D-error and S-efficiency to a non-technical stakeholder?
2. **Can you generate a basic efficient design** using Ngene with priors and constraints?
3. **Can you diagnose design quality** issues using correlation matrix, level balance, and overlap statistics?
4. **Can you create a professional choice card** mockup using tables or graphics?
5. **Can you justify your design decisions** (# of tasks, blocking, pivot vs. generic) in writing?

If you answered "yes" to all five—you're ready for Module 4: Implementation & Fieldwork!

---

## 🔗 Navigation

- **Previous:** [Module 2 - Survey Design Essentials](02-survey-design.md)
- **Next:** [Module 4 - Implementation & Fieldwork](04-implementation.md)
- **Related:** [Assignment 3](../assignments/03_design_package.md) | [Syllabus](../syllabus.md) | [Course Home](../index.md)

---

<div class="alert alert-success">
<strong>💡 Pro Tip:</strong> Save all your Ngene syntax files and design matrices in a "Design Library" folder. When starting a new project, you can adapt previous designs rather than starting from scratch. Over time, you'll build a valuable portfolio of design templates for different transport contexts!
</div>

---

**Questions or feedback?** Contact the instructor or post in the course discussion forum.
