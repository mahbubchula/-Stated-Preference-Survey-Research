---
title: "Module 1 - Foundations"
layout: default
nav_order: 10
---

# Module 1: Foundations of Stated Preference Methods

<div class="alert alert-info">
<strong>Duration:</strong> 1-2 weeks | <strong>Effort:</strong> 8-10 hours | <strong>Level:</strong> Introductory
</div>

---

## 📋 Overview

Welcome to the foundational module of Stated Preference Survey Research! This module positions stated preference (SP) techniques within the broader transportation analytics toolbox. You'll learn why SP methods are essential, when to use them, and how they differ from traditional data sources.

By the end of this module, you'll understand the **theoretical foundations**, **practical applications**, and **limitations** of SP research in transportation planning and policy.

---

## 🎯 Learning Objectives

By completing this module, you will be able to:

1. **Explain** why SP data is collected when revealed preference (RP) data is insufficient or biased
2. **Identify** the theoretical pillars that support SP experiments (random utility theory, choice axioms)
3. **Map** transport policy questions to appropriate SP survey approaches
4. **Evaluate** the strengths and limitations of seminal SP studies in congestion pricing, microtransit, and EV adoption
5. **Apply** utility theory concepts to real-world transportation scenarios

---

## 📚 What is Stated Preference Research?

### Definition

**Stated Preference (SP)** methods are survey techniques that ask respondents to state their preferences among hypothetical alternatives. Unlike revealed preference data (which observes actual behavior), SP allows researchers to:

- Test **non-existent alternatives** (e.g., autonomous shuttles, hyperloop)
- Evaluate **future scenarios** (e.g., climate policies in 2040)
- Control **experimental conditions** precisely
- Separate **confounded attributes** (e.g., price vs. quality)

### Historical Context

| Era | Development |
|-----|-------------|
| **1970s** | Origins in marketing research and environmental economics |
| **1980s** | Formal integration into transportation demand modeling |
| **1990s** | Rise of discrete choice experiments and conjoint analysis |
| **2000s** | Advanced econometric models (mixed logit, latent class) |
| **2010s-Present** | Online platforms, big data integration, AI-assisted design |

---

## 🔄 Revealed Preference vs. Stated Preference

### Comparison Table

| Aspect | Revealed Preference (RP) | Stated Preference (SP) |
|--------|--------------------------|------------------------|
| **Data Source** | Observed actual behavior | Hypothetical scenarios |
| **Realism** | ⭐⭐⭐⭐⭐ Highest | ⭐⭐⭐ Moderate |
| **Control** | ⭐⭐ Limited | ⭐⭐⭐⭐⭐ Excellent |
| **Future Alternatives** | ❌ Cannot test | ✅ Perfect for this |
| **Attribute Correlation** | Often confounded | Orthogonal by design |
| **Sample Size** | Can be massive | Typically smaller |
| **Cost** | Varies widely | Moderate to high |
| **Strategic Bias** | Low | Can be significant |

### When to Use SP Methods

**Choose SP when:**
- New alternatives don't exist yet (e.g., Maglev trains)
- Current data lacks variation (e.g., uniform tolls across network)
- Policy testing requires counterfactuals
- Need to isolate specific attribute effects
- Ethical/practical constraints prevent real experiments

**Choose RP when:**
- Actual behavior data is available and sufficient
- Realism is paramount
- Budget is limited
- Respondent burden must be minimized

**Best Practice:** Combine RP + SP (hybrid models) for optimal reliability!

---

## 🧮 Random Utility Theory (RUT) Fundamentals

### Core Concepts

Stated preference analysis relies on **Random Utility Theory**, which assumes:

1. **Decision-makers are rational:** They choose the alternative with highest utility
2. **Utility is decomposable:** U = V (systematic) + ε (random error)
3. **Probabilistic choices:** Because of ε, we can only predict choice probabilities

### Mathematical Foundation

For individual *n* choosing among alternatives *i* in choice set *C*:

```
U_ni = V_ni + ε_ni
```

Where:
- **U_ni** = Total utility of alternative i for person n
- **V_ni** = Systematic (observable) utility = β₁X₁ + β₂X₂ + ... + βₖXₖ
- **ε_ni** = Random (unobservable) component

**Choice Probability:**
```
P(i|C) = P(U_ni > U_nj for all j ≠ i)
```

If ε follows **Type I Extreme Value distribution** → **Logit Model**

### Example: Commute Mode Choice

Consider three alternatives:
- **Drive alone** (DA)
- **Public transit** (PT)
- **Bike** (BK)

**Utility Functions:**
```
V_DA = β_cost × Cost_DA + β_time × Time_DA + ASC_DA
V_PT = β_cost × Cost_PT + β_time × Time_PT + ASC_PT
V_BK = β_cost × Cost_BK + β_time × Time_BK + ASC_BK
```

If estimated parameters are:
- β_cost = -0.05 ($/unit)
- β_time = -0.03 ($/min)
- ASC_DA = 0 (reference)
- ASC_PT = -0.5
- ASC_BK = -1.2

For a trip with:
- Drive: $8, 25 min → V_DA = -0.05(8) - 0.03(25) + 0 = -1.15
- Transit: $3, 45 min → V_PT = -0.05(3) - 0.03(45) - 0.5 = -2.0
- Bike: $0, 35 min → V_BK = -0.05(0) - 0.03(35) - 1.2 = -2.25

**Multinomial Logit Probabilities:**
```
P(DA) = exp(-1.15) / [exp(-1.15) + exp(-2.0) + exp(-2.25)] = 0.577
P(PT) = exp(-2.0) / [...] = 0.256
P(BK) = exp(-2.25) / [...] = 0.167
```

---

## 🌍 Real-World Applications

### Case Study 1: Singapore Electronic Road Pricing (ERP)

**Challenge:** Design optimal congestion pricing for urban corridors

**SP Approach:**
- Presented commuters with choice sets varying:
  - Toll levels ($0, $1, $2, $3, $5)
  - Peak vs. off-peak timing
  - Alternative routes
  - Transit improvements

**Outcomes:**
- Estimated willingness-to-pay for time savings
- Forecasted traffic diversion rates
- Optimized pricing structure
- Politically informed implementation

**Key Learning:** SP allowed testing price points before costly infrastructure

### Case Study 2: Electric Vehicle (EV) Adoption in Norway

**Challenge:** Predict EV uptake under different policy scenarios

**SP Design:**
- Attributes: purchase price, charging time, range, fuel savings
- Scenarios: varying tax incentives, charging infrastructure
- Sample: 2,500 potential car buyers

**Findings:**
- Range anxiety diminishes above 300 km
- Fast charging (30 min) increases adoption by 40%
- Price subsidies more effective than fuel tax increases

### Case Study 3: On-Demand Microtransit Services

**Challenge:** Design service attributes for suburban areas

**SP Experiment:**
- Wait time: 5, 10, 15, 20 min
- Fare: $2, $4, $6, $8
- Walking distance: 100m, 300m, 500m
- Service hours: peak-only vs. all-day

**Results:**
- Optimal wait time: <10 minutes
- Price elasticity: -0.45
- Service viability thresholds identified

---

## ⚙️ Session Breakdown

### Session 1: RP vs SP Landscape (3 hours)

**Activities:**
1. **Mini-lecture (45 min):** History of travel demand modeling and the rise of SP
2. **Group Exercise (60 min):** Catalog deficiencies in existing agency datasets
   - Break into teams of 3-4
   - Select a local transport agency
   - Identify 5 data gaps that SP could fill
   - Present findings (10 min per team)
3. **Reading Discussion (75 min):**
   - Ben-Akiva & Lerman Chapters 1-2
   - Federal Transit Administration SP case note
   - Facilitated Q&A

**Preparation:**
- Read assigned chapters before class
- Bring examples from your professional context

### Session 2: Utility Theory Refresh (3 hours)

**Activities:**
1. **Lecture (60 min):** Random utility models, behavioral assumptions, error terms, IIA
2. **Mathematical Exercise (45 min):**
   - Derive utility specifications for three-alternative commuter choice
   - Calculate choice probabilities by hand
   - Discuss parameter interpretation
3. **Case Study Spotlight (75 min):** Singapore ERP pricing redesign
   - Video presentation
   - Group discussion on transferability

**Deliverables:**
- Completed utility derivation worksheet
- Discussion post on case applicability

---

## 🔬 Lab Activities

### Activity 1: Concept Mapping (90 minutes)

**Objective:** Create a visual "decision value chain" from planning question to policy

**Steps:**
1. Form teams of 3-4 students
2. Choose a transport challenge:
   - Bike-share expansion
   - Congestion pricing
   - Autonomous vehicle regulation
   - Rural transit redesign
3. Map the flow:
   ```
   Policy Question → Research Objectives → SP Design →
   Data Collection → Modeling → Insights → Implementation
   ```
4. Present on poster board or digital whiteboard
5. Peer critique (2 min per team)

**Rubric:**
- Clarity of connections (30%)
- Depth of SP methodology (30%)
- Creativity and presentation (20%)
- Peer feedback incorporation (20%)

### Activity 2: Tool Familiarization Tour (60 minutes)

**Platforms to Explore:**
1. **Survey Platform:** Qualtrics demo
   - Create a simple 3-alternative choice
   - Add randomization
   - Preview on mobile
2. **Design Software:** Ngene basics
   - Input attributes and levels
   - Generate orthogonal design
   - Review balance statistics
3. **Modeling Environment:** Biogeme walkthrough
   - Load sample dataset
   - Specify MNL model
   - Interpret output

**Note:** No installation required—instructor-led demos with shared screens

---

## 📝 Assignment

### [Module 1 Reflection Memo](../assignments/01_reflection.md)

**Objective:** Analyze when SP evidence would improve one of your ongoing or hypothetical transport programs

**Requirements:**
1. **Context Snapshot (300 words):**
   - Describe transport issue
   - Identify stakeholders
   - Explain existing data limitations
2. **SP Opportunity Matrix:** Minimum 3 research questions mapped to policy levers
3. **Risk/Benefit Commentary (200 words):**
   - Potential biases
   - How SP could influence action
   - Mitigation strategies

**Submission:**
- PDF or Markdown format
- 2-3 pages maximum
- Filename: `M1_reflection_<lastname>.pdf`
- **Due:** End of Week 1

**Evaluation Rubric:**
| Criterion | Weight | Indicators |
|-----------|--------|------------|
| Problem framing | 30% | Clear linkage to objectives, relevant stakeholders |
| SP justification | 40% | Demonstrates why SP > RP for this case |
| Critical thinking | 20% | Identifies risks, limitations, mitigation |
| Clarity & professionalism | 10% | Structure, tone, citations |

---

## 💬 Discussion Prompts

**Post your responses on the course forum (minimum 150 words each):**

1. **RP Preference Paradox:**
   "When is RP data preferable even if SP can be fielded cheaply? Provide a specific example from your domain."

2. **Uncertainty Communication:**
   "How can we communicate uncertainty from SP models to decision-makers who expect deterministic forecasts? What visualization techniques work best?"

3. **Behavioral Realism:**
   "Critics argue SP responses don't match real behavior. How would you defend or acknowledge this limitation in a policy brief?"

**Engagement Expectations:**
- Initial post by Day 3
- Respond to 2 peers by Day 5
- Instructor synthesis on Day 7

---

## 📖 Recommended Resources

### Core Textbooks

1. **Train, K. (2009).** *Discrete Choice Methods with Simulation* (2nd ed.)
   - Chapters 1-2: Introduction to utility theory
   - [Free PDF available from author's website](https://eml.berkeley.edu/books/choice2.html)

2. **Ben-Akiva, M., & Lerman, S. R. (1985).** *Discrete Choice Analysis: Theory and Application to Travel Demand*
   - Foundational reference
   - Chapters 1-3 for this module

3. **Louviere, J. J., Hensher, D. A., & Swait, J. D. (2000).** *Stated Choice Methods: Analysis and Applications*
   - Comprehensive SP methodology
   - Chapter 2: Theoretical foundations

### Journal Articles

- **Chorus, C., Timmermans, H., & Arentze, T. (2020).** "Transportation Research Part B: Special Issue on SP Debiasing"
  - Latest advances in addressing hypothetical bias

- **Hensher, D. A. (2010).** "Hypothetical Bias, Choice Experiments and Willingness to Pay." *Transportation Research Part B*, 44(6), 735-752.

- **Adamowicz, W., et al. (1994).** "Combining Revealed and Stated Preference Methods." *Journal of Environmental Economics and Management*, 26(3), 271-292.

### Reports & Policy Documents

- **ITF/OECD (2019).** *Data-Driven Transport Policy* - Chapter on SP applications
  - [Download link](https://www.itf-oecd.org/data-driven-transport-policy)

- **Federal Transit Administration (2016).** *Stated Preference Research Methods: Case Studies*
  - Real-world applications in US transit
  - [FTA website](https://www.transit.dot.gov/)

### Online Resources

- **Choice Modeling Centre** (University of Leeds)
  Resources, tutorials, software links
  [https://www.its.leeds.ac.uk/choices/](https://www.its.leeds.ac.uk/choices/)

- **Discrete Choice Analysis Blog**
  Monthly updates on methods and applications
  [https://discretechoice.wordpress.com/](https://discretechoice.wordpress.com/)

---

## ✅ Module Completion Checklist

Before moving to Module 2, ensure you have:

- [ ] Attended or watched both sessions
- [ ] Completed the concept mapping activity
- [ ] Participated in tool familiarization lab
- [ ] Posted to all 3 discussion prompts
- [ ] Submitted Module 1 Reflection Memo
- [ ] Read Train (2009) Chapters 1-2
- [ ] Reviewed at least one case study in detail

**Self-Assessment Questions:**
1. Can you explain the difference between RP and SP in one minute?
2. Can you write a simple utility function for a mode choice problem?
3. Can you identify when SP is superior to RP for a given policy question?

If you answered "yes" to all three—you're ready for Module 2!

---

## 🔗 Navigation

- **Previous:** [Course Home](../index.md)
- **Next:** [Module 2 - Survey Design Essentials](02-survey-design.md)
- **Related:** [Assignment 1](../assignments/01_reflection.md) | [Syllabus](../syllabus.md)

---

<div class="alert alert-success">
<strong>🎓 Pro Tip:</strong> Keep a "SP Opportunities Journal" throughout this course. Every time you encounter a transport policy question in your work or news, ask: "Could SP help answer this?" By Module 6, you'll have a portfolio of potential applications!
</div>

---

**Questions or feedback?** Contact Mahbub Hassan at [mahbub.hassan@ieee.org](mailto:mahbub.hassan@ieee.org) or [6870376421@student.chula.ac.th](mailto:6870376421@student.chula.ac.th)
