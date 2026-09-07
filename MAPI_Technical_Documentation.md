# MAPI Technical Documentation

## 1. Development Environment

MAPI was developed as a Python-based analytical prototype with an interactive Streamlit interface.

### Core Technologies

* Python
* Pandas
* NumPy
* Matplotlib
* Streamlit

The analytical calculations are separated from the user interface so that the underlying model can be modified independently of the dashboard.

---

## 2. System Architecture

The prototype follows the following architecture:

**Input Data**

↓

**Employee Analysis Engine**

↓

**MDI Calculation**

↓

**Longitudinal Performance Metrics**

↓

**Expected Shock Regression**

↓

**Adaptation Residual**

↓

**Normalised MAPI Components**

↓

**MAPI Score & Category**

↓

**Streamlit Dashboard**

↓

**HR Intervention Insights**

---

## 3. Data Structure

The prototype dataset contains longitudinal employee observations.

Each employee is represented across:

* Months −6 to −1: pre-M&A period
* Month 0: M&A event
* Months +1 to +6: post-M&A period

The prototype contains 200 synthetic employees across six departments.

---

## 4. Synthetic Data Generation

Synthetic employee profiles were created to simulate different adaptation patterns.

The profiles include:

* Resilient
* Rapid Adaptor
* Stable Specialist
* Delayed Adaptor
* Vulnerable
* Declining

Each profile is associated with a different simulated adaptability level.

M&A disruption was independently generated across seven dimensions.

Performance was then generated longitudinally using:

* Individual baseline performance
* M&A disruption
* Performance shock
* Adaptability-related response
* Recovery rate
* Random variation

This design creates a controlled environment for testing whether the analytical framework can recover known relationships.

---

## 5. Regression Model

The expected-shock model uses linear regression:

$$
Y = \beta_0 + \beta_1X
$$

where:

$$
X = MDI
$$

and:

$$
Y = Performance\ Shock
$$

The model estimates the expected level of performance disruption given the employee's MDI.

---

## 6. Validation

An independent synthetic adaptability variable, referred to as **Adaptability Ground Truth**, was retained for validation purposes.

This variable is **not used in the MAPI calculation**.

The final MAPI score was compared with this independent simulated criterion.

Results:

### Pearson correlation

$$
r = 0.921
$$

### Spearman correlation

$$
\rho = 0.919
$$

The strong relationship indicates that the prototype successfully recovers the intended adaptability pattern within the simulated dataset.

This represents **internal criterion validity within the simulation**, not empirical validation of MAPI as a psychological or organisational assessment instrument.

---

## 7. Additional Model Relationships

The prototype produced the following relationships:

| Variable               | Correlation with MAPI |
| ---------------------- | --------------------: |
| Performance Shock      |                −0.846 |
| Recovery Time          |                −0.906 |
| Recovery Velocity      |                 0.669 |
| Performance Trajectory |                 0.821 |

These relationships are directionally consistent with the intended interpretation of MAPI:

* Higher shock → lower MAPI
* Longer recovery → lower MAPI
* Faster recovery → higher MAPI
* Stronger trajectory → higher MAPI

---

## 8. Stress Testing

The model was additionally examined under different simulated conditions.

### Disruption Sensitivity

Employees with high MDI were not automatically assigned low MAPI.

This is important because MAPI is intended to measure **adaptation relative to disruption**, rather than simply rewarding employees who experience less disruption.

### Extreme Adaptation

Highly adaptive synthetic profiles generally produced higher MAPI values, while declining profiles generally produced lower scores.

### Department Analysis

Department-level differences were examined to identify whether MAPI patterns were being driven by substantial differences in disruption exposure or by differences in the simulated composition of employee adaptation profiles.

---

## 9. Current Prototype Performance

The current simulation produced:

* Mean MAPI: **43.67**
* Standard deviation: **22.20**
* Minimum: **2.99**
* Maximum: **86.11**

The prototype therefore produces meaningful variation across employees rather than clustering all employees around a single score.

---

## 10. Technical Limitations

The current system should be regarded as a proof of concept.

### Synthetic Data

Real organisational data may produce relationships that differ from the simulated dataset.

### MDI Weighting

The current MDI uses equal weights across seven disruption dimensions. Future research should investigate whether certain forms of disruption have greater psychological or performance impact.

### MAPI Weighting

The 35/30/15/20 weighting structure is a prototype design decision and requires empirical investigation.

### Regression Assumptions

Real-world implementation would require testing assumptions such as linearity, independence, residual behaviour, and robustness to outliers.

### Normalisation

Min-max normalisation depends on the observed dataset. Production implementation would require stable organisational benchmarks.

### Recovery Definition

Recovery may not be identical across employees, roles, departments, or industries. Future versions should establish empirically justified recovery criteria.

### Fairness

Real-world implementation must investigate whether the model produces systematically different outcomes across demographic or organisational groups.

### Ethical Use

MAPI should be used as decision support and should not independently determine employment decisions.

---

## 11. Future Technical Development

A production version could incorporate:

* Real-time HRIS integration
* Longitudinal organisational data
* Machine-learning models
* Explainable AI
* Organisation-specific calibration
* Dynamic weighting
* Fairness monitoring
* Privacy-preserving analytics
* Automated intervention recommendation
* Role-specific adaptation benchmarks
* API-based deployment
* Cloud-based dashboards

---

## 12. Intended Product Model

MAPI can be conceptualised as a **B2B organisational intelligence service**.

A potential enterprise implementation could provide:

### Data Layer

Integration with HRIS, performance-management, engagement, and organisational-change data.

### Analytics Layer

MDI calculation, longitudinal performance analysis, adaptation modelling, and MAPI scoring.

### Intelligence Layer

Employee, team, and department-level adaptation patterns.

### Intervention Layer

Targeted HR recommendations and change-management insights.

### Monitoring Layer

Longitudinal tracking of workforce adaptation throughout the M&A integration process.

The long-term objective would be to help organisations shift from reactive performance management toward **context-sensitive, predictive, and intervention-oriented change management**.
