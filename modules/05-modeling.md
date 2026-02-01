---
title: "Module 5 - Modeling"
layout: default
nav_order: 14
---

# Module 5 - Discrete Choice Modeling & Estimation

## Overview
Analyze SP datasets using logit-family models. Learners clean pilot data, specify utilities, run models in Biogeme or Apollo, and interpret elasticities, value-of-time, and heterogeneity diagnostics.

## Learning objectives
- Structure SP datasets for estimation (wide/long formats, effect coding, panel identifiers).
- Estimate MNL models and extend to mixed logit, latent class, or nested structures as needed.
- Use likelihood-ratio tests, information criteria, and predictive checks to select models.
- Translate coefficients into interpretable insights (marginal willingness-to-pay, policy uptake curves).

## Session breakdown
### Session 1: Data prep & base models
- Walkthrough: cleaning raw survey exports, coding attributes, merging metadata.
- Notebook lab: run a baseline MNL in Biogeme or Apollo; inspect statistics, significance, and correlations.
- Mini-lecture: identification issues, scale, and confounding between attribute levels.

### Session 2: Advanced models & interpretation
- Workshop: build mixed logit with random parameters; run 500+ draws and discuss convergence.
- Exercise: compute elasticities and scenario-specific willingness-to-pay from estimated models.
- Demo: packaging model outputs into policy-friendly visuals (fan charts, tornado plots).

## Activities & lab
- **Code review circle:** peers review each other's notebooks for documentation, reproducibility, and defensive coding.
- **Diagnostics dash:** teams create a simple dashboard (Jupyter, RMarkdown, Power BI) summarizing fit measures and alternative shares.

## Assignment
[Module 5 Modeling Memo](../assignments/05_modeling_memo.md) - submit cleaned dataset description, scripts/notebooks, model comparison table, and narrative insights.

## Discussion prompts
1. When does model complexity hinder communication with non-technical stakeholders?
2. How can we combine RP and SP data to improve predictive accuracy without overfitting?

## Recommended resources
- Bierlaire, M. (2020) *Python Biogeme* documentation.
- Hess & Palma (2019) papers on estimating advanced discrete choice models.
- R Apollo package tutorials (2023+).


