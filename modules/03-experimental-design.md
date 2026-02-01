---
title: "Module 3 - Experimental Design"
layout: default
nav_order: 12
---

# Module 3 - Experimental Design & Efficient Choice Tasks

## Overview
Move from attribute spreadsheets to optimized experimental designs. Participants compare orthogonal and efficient designs, explore blocking strategies, and prototype choice tasks for a transit fare reform case.

## Learning objectives
- Explain the differences among full factorial, fractional factorial, orthogonal, D-efficient, and Bayesian designs.
- Configure priors and constraints in commercial or open-source design generators.
- Evaluate design quality using D-error, S-efficiency, and level balance diagnostics.
- Create readable, context-rich choice cards (textual, graphical, or tabular forms).

## Session breakdown
### Session 1: Theory & evaluation metrics
- Lecture: algebra of design matrices, priors, and error terms.
- Interactive notebook: compute D-efficiency for sample matrices using R `idefix` or Python `pylogit`.
- Quick quiz: interpret design diagnostics for provided output tables.

### Session 2: Tool demos & prototyping
- Demo: Ngene workflow (attributes -> priors -> constraints -> output).
- Lab rotations: teams generate a pivot design around a real bus fare scenario, then critique each other's choice card layout.
- Mini-lecture: blocking and randomization to manage respondent burden.

## Activities & lab
- **Design surgery:** critique a poor-choice screen and rebuild it with clear formatting, icons, or scenario narratives.
- **Automation challenge:** scripts generate 200 design variants; teams justify the final pick using metrics.

## Assignment
[Module 3 Efficient Design Package](../assignments/03_design_package.md) - submit priors, generator settings, sample choice screens, and a one-page justification memo.

## Discussion prompts
1. When is a pivot design superior to a purely orthogonal design in transport pricing studies?
2. How do you balance attribute level realism with statistical efficiency?

## Recommended resources
- Rose & Bliemer (2014) primer on stated choice experimental designs.
- ChoiceMetrics Ngene user manual (latest edition).
- Scarpa, Thiene, & Train (2008) on Bayesian approaches for SP designs.


