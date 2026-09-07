# MAPI — M&A Adaptability Performance Intelligence

### A data-driven organisational intelligence prototype for measuring employee adaptation during mergers and acquisitions

---

## Overview

**MAPI (M&A Adaptability Performance Index)** is an organisational intelligence prototype designed to help organisations understand how employees adapt to disruption during **mergers and acquisitions (M&A)**.

Traditional performance management primarily evaluates **how well an employee performs**. MAPI introduces a contextual approach by asking:

> **How well did the employee adapt relative to the level of disruption they experienced?**

The system combines disruption exposure, longitudinal performance data, performance-shock modelling, recovery behaviour, and adaptation analytics to generate an individual **MAPI score from 0–100**.

The prototype is intended as a **decision-support tool for HR and organisational leaders**, rather than an automated employee-ranking or termination system.

---

## Organisational Problem

Mergers and acquisitions can substantially disrupt employees through changes in:

* Roles and responsibilities
* Teams and reporting structures
* Leadership
* Technology and systems
* Organisational processes
* Organisational culture
* Work location/environment

These disruptions can temporarily reduce performance and create difficulties in employee adaptation.

A conventional performance rating may interpret reduced performance simply as poor performance. MAPI instead attempts to distinguish between:

**Performance decline caused by organisational disruption**

and

**Performance decline associated with weaker adaptation.**

This allows organisations to identify employees who may require targeted support during organisational change.

---

## Psychological Foundation

MAPI is informed by research on **adaptive performance**, particularly the conceptualisation of adaptability as an employee's ability to modify behaviour and performance in response to changing work demands.

A major theoretical foundation is:

Pulakos, E. D., Arad, S., Donovan, M. A., & Plamondon, K. E. (2000). Adaptability in the workplace: Development of a taxonomy of adaptive performance. *Journal of Applied Psychology, 85*(4), 612–624.

The model translates the broader organisational psychology concept of adaptive performance into a quantitative framework that can be applied to M&A-related organisational disruption.

---

# How MAPI Works

The model follows a multi-stage analytical pipeline:

**M&A Disruption Inputs**

↓

**M&A Disruption Index (MDI)**

↓

**Longitudinal Employee Performance**

↓

**Performance Shock & Recovery Metrics**

↓

**Expected Performance Shock**

↓

**Adaptation Residual**

↓

**MAPI Score**

↓

**Workforce Intelligence Dashboard**

↓

**Targeted HR Intervention**

---

## 1. M&A Disruption Index (MDI)

The **M&A Disruption Index** measures the level of disruption experienced by an employee across seven dimensions:

1. Role change
2. Team change
3. Leadership change
4. Technology change
5. Process change
6. Culture change
7. Location/environment change

Each dimension is represented on a **0–100 scale**.

The current prototype uses equal weighting:

**MDI = (Role + Team + Leadership + Technology + Process + Culture + Location) / 7**

A higher MDI represents greater disruption exposure.

---

## 2. Longitudinal Performance Analysis

Employee performance is examined across a longitudinal window surrounding the M&A event.

The prototype contains:

* Six pre-M&A months
* M&A month (Month 0)
* Six post-M&A months

This allows the system to examine not only an employee's performance at one point in time, but also their response and recovery trajectory following organisational disruption.

---

## 3. Performance Metrics

The model calculates several indicators:

### Performance Shock

Measures the decline in performance associated with the M&A event relative to the employee's pre-M&A baseline.

### Recovery Time

Measures how long the employee takes to return toward their baseline performance.

### Recovery Velocity

Measures the rate at which performance improves following the initial disruption.

### Performance Trajectory

Captures the overall direction of performance across the longitudinal period.

---

## 4. Expected Performance Shock

MAPI does not interpret performance shock in isolation.

A linear regression is fitted between:

**MDI → Performance Shock**

The model estimates:

**Expected Shock = β₀ + β₁(MDI)**

This represents the approximate performance shock expected given the employee's level of organisational disruption.

---

## 5. Adaptation Residual

The key contextual component is the difference between expected and observed performance shock:

**Adaptation Residual = Expected Shock − Observed Shock**

A positive residual indicates that the employee experienced **less performance disruption than expected** given their MDI.

A negative residual indicates that the employee experienced **greater disruption than expected**.

Therefore, the residual provides an indication of adaptation relative to disruption rather than performance in isolation.

---

# 6. MAPI Score

The four analytical components are normalised to a 0–100 scale and combined using the current prototype weights:

| Component                    | Weight |
| ---------------------------- | -----: |
| Adaptation Residual Score    |    35% |
| Recovery Score               |    30% |
| Recovery Velocity Score      |    15% |
| Performance Trajectory Score |    20% |

The resulting formula is:

**MAPI = 0.35(ARS) + 0.30(RS) + 0.15(RVS) + 0.20(TS)**

Higher MAPI scores indicate stronger adaptation.

---

## 7. Adaptation Categories

The prototype currently uses the following interpretation bands:

| MAPI Score | Category                 |
| ---------: | ------------------------ |
|     80–100 | Highly Adaptive          |
|      60–79 | Adaptive                 |
|      40–59 | Moderately Adaptive      |
|      20–39 | Low Adaptation           |
|       0–19 | Critical Adaptation Risk |

These thresholds are **prototype interpretation bands and are not clinically or empirically validated cut-offs**.

---

# 8. Workforce Intelligence

The Streamlit application provides two primary analytical perspectives.

### Workforce Overview

Provides:

* Total workforce size
* Average MAPI
* Average MDI
* Adaptation-risk distribution
* Department-level adaptation patterns
* Employees requiring attention
* High-disruption/high-adaptation employees
* M&A adaptation intervention matrix

### Employee Intelligence

Provides:

* Individual MAPI score
* M&A disruption exposure
* Performance shock
* Recovery time
* Recovery velocity
* Performance trajectory
* Expected vs. observed shock
* Adaptation residual
* MAPI component scores
* HR interpretation

---

# 9. Intervention Framework

MAPI is designed to support targeted organisational interventions.

The prototype identifies four broad employee contexts:

### High Disruption + Low MAPI

**Priority Intervention**

Potential responses include coaching, mentoring, change-management support, training, and wellbeing resources.

### High Disruption + High MAPI

**Resilient Under Pressure**

These employees may provide useful examples of successful adaptation and can potentially contribute to peer support or change implementation.

### Low Disruption + High MAPI

**Strong Adaptor**

These employees demonstrate strong adaptation despite relatively lower disruption exposure.

### Low Disruption + Low MAPI

**Monitor**

Further contextual assessment may be required before determining the appropriate intervention.

---

# 10. Technology Stack

The prototype was developed using:

* **Python** — analytical computation and data processing
* **Pandas** — dataset manipulation and analysis
* **NumPy** — numerical computation
* **Matplotlib** — data visualisation
* **Streamlit** — interactive web application and dashboard
* **CSV** — prototype data storage

---

# 11. Synthetic Dataset

The current prototype uses a **synthetically generated dataset** representing employees undergoing M&A disruption.

The dataset contains:

* 200 employees
* 6 departments
* Multiple employee adaptation profiles
* Seven M&A disruption dimensions
* Longitudinal performance observations
* Pre-M&A and post-M&A performance

The synthetic dataset is used for **prototype development and model testing**.

It does not represent real organisational employee data.

---

# 12. Model Validation

The prototype was tested against a hidden synthetic **Adaptability Ground Truth** generated independently during dataset construction.

The resulting MAPI score demonstrated:

* Pearson correlation with adaptability ground truth: **r = 0.921**
* Spearman correlation: **ρ = 0.919**

Additional relationships included:

* MAPI vs Performance Shock: **r = −0.846**
* MAPI vs Recovery Time: **r = −0.906**
* MAPI vs Recovery Velocity: **r = 0.669**
* MAPI vs Performance Trajectory: **r = 0.821**

These results demonstrate **strong internal criterion validity within the simulated dataset**.

They should not be interpreted as evidence that MAPI has been empirically validated in real organisations.

---

# 13. Running the Prototype

Install the required Python packages:

```bash
pip install -r requirements.txt
```

Run the Streamlit application:

```bash
streamlit run app.py
```

The application will open in a local browser.

---

# 14. Prototype Features

The current prototype includes:

* Workforce-level MAPI dashboard
* Employee-level intelligence
* M&A disruption measurement
* Longitudinal performance analysis
* Expected performance shock modelling
* Adaptation residual analysis
* MAPI scoring
* Adaptation categorisation
* HR intervention matrix
* Department-level analysis
* Add Employee functionality

---

# 15. Current Limitations

MAPI is currently a **proof-of-concept prototype**.

Key limitations include:

* The current dataset is synthetic.
* MDI dimensions currently use equal weighting.
* MAPI component weights require further empirical investigation.
* Regression assumptions require testing using real organisational data.
* Normalisation is dependent on the current dataset.
* Recovery definitions may require refinement for different organisational contexts.
* Fairness and demographic bias require systematic evaluation.
* Real-world longitudinal validation is required before organisational deployment.

---

# 16. Future Development

Future versions could incorporate:

* Real organisational longitudinal data
* Empirically validated MDI measures
* Data-driven component weighting
* Machine-learning prediction models
* Explainable AI
* Organisation-specific benchmarks
* Automated intervention recommendations
* Integration with HR Information Systems
* Privacy-preserving employee analytics
* Fairness and bias auditing
* Real-time change-management monitoring

---

## Intended Use

MAPI is designed as a **decision-support framework** for understanding employee adaptation during organisational change.

It should complement, rather than replace:

* Managerial judgement
* Employee conversations
* HR assessment
* Psychological and organisational context
* Ethical decision-making

**MAPI should not be used as an automatic basis for employee termination, promotion, compensation, or disciplinary action.**

---

## Project

**Organisational Psychology, Innovation & Entrepreneurial Problem-Solving Project**

**Prototype:** MAPI — M&A Adaptability Performance Intelligence

**Technology:** Python + Streamlit

**Application Domain:** Organisational Psychology / Human Resources / M&A Change Management

---
