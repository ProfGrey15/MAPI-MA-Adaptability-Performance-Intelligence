# MAPI Model Methodology

## 1. Conceptual Model

MAPI is based on a contextual performance perspective.

The model assumes that employee performance following an M&A event should be interpreted in relation to the degree of organisational disruption experienced.

The conceptual relationship is:

**Disruption Exposure → Performance Response → Adaptation → Intervention**

---

## 2. M&A Disruption Index

For employee *i*, disruption is measured across seven dimensions:

* Role
* Team
* Leadership
* Technology
* Process
* Culture
* Location/Environment

The current prototype assigns equal weight to each dimension.

$$
MDI_i = \frac{R_i + T_i + L_i + Tech_i + P_i + C_i + Loc_i}{7}
$$

where each dimension is measured from 0 to 100.

---

## 3. Baseline Performance

The employee's pre-M&A performance is used to establish an individual baseline.

$$
Baseline_i = Mean(Performance_{pre-M\&A})
$$

This provides an employee-specific reference point rather than comparing all employees against a single organisational average.

---

## 4. Performance Shock

Performance shock represents the immediate decline associated with the M&A event.

$$
Performance\ Shock_i =
Baseline_i - Performance_{M\&A,i}
$$

A larger positive value indicates a larger immediate performance decline.

---

## 5. Recovery Time

Recovery time represents the time required for performance to return toward the employee's baseline.

The prototype examines the post-M&A longitudinal performance period to determine whether and when recovery occurs.

Employees who do not recover within the available observation window receive a lower recovery score.

---

## 6. Recovery Velocity

Recovery velocity represents the rate of performance improvement following the initial shock.

Conceptually:

$$
Recovery\ Velocity =
\frac{Performance_{later}-Performance_{M\&A}}{Time}
$$

Higher positive values indicate faster improvement.

---

## 7. Performance Trajectory

Performance trajectory captures the direction of performance across the longitudinal observation period.

A positive trajectory indicates improving performance, while a negative trajectory indicates declining performance.

---

## 8. Expected Performance Shock

The model estimates expected performance shock based on disruption exposure.

A linear regression is fitted:

$$
Expected\ Shock_i = \beta_0 + \beta_1(MDI_i)
$$

where:

* \(\beta_0\) = regression intercept
* \(\beta_1\) = estimated relationship between MDI and performance shock
* \(MDI_i\) = employee disruption exposure

---

## 9. Adaptation Residual

The central contextual measure is:

$$
Adaptation\ Residual_i =
Expected\ Shock_i - Observed\ Shock_i
$$

Interpretation:

### Positive residual

Observed shock is smaller than expected.

**Interpretation: stronger adaptation relative to disruption.**

### Negative residual

Observed shock is larger than expected.

**Interpretation: weaker adaptation relative to disruption.**

This allows the model to distinguish disruption exposure from employee adaptation.

---

## 10. Component Normalisation

The four MAPI components are converted to a common 0–100 scale.

The current prototype uses min-max normalisation:

$$
X' =
100 \times
\frac{X-X_{min}}
{X_{max}-X_{min}}
$$

For indicators where lower values represent better adaptation, the scoring direction is reversed.

This produces:

* Adaptation Residual Score (ARS)
* Recovery Score (RS)
* Recovery Velocity Score (RVS)
* Trajectory Score (TS)

---

## 11. MAPI Calculation

The current prototype uses:

$$
MAPI =
0.35(ARS)
+
0.30(RS)
+
0.15(RVS)
+
0.20(TS)
$$

Therefore:

| Component                 | Weight |
| ------------------------- | -----: |
| Adaptation Residual Score |    35% |
| Recovery Score            |    30% |
| Recovery Velocity Score   |    15% |
| Trajectory Score          |    20% |

The weighting reflects the conceptual priority given to adaptation relative to disruption and subsequent recovery.

These weights are **prototype design parameters** and should be empirically tested and potentially revised using real-world organisational data.

---

## 12. MAPI Interpretation

|  Score | Interpretation           |
| -----: | ------------------------ |
| 80–100 | Highly Adaptive          |
|  60–79 | Adaptive                 |
|  40–59 | Moderately Adaptive      |
|  20–39 | Low Adaptation           |
|   0–19 | Critical Adaptation Risk |

These categories are intended for prototype interpretation and should not be treated as validated psychological thresholds.

---

## 13. Intervention Logic

The model combines MDI and MAPI to create an intervention matrix.

### High MDI + Low MAPI

High disruption with weaker adaptation.

**Recommended response:** targeted support and change-management intervention.

### High MDI + High MAPI

High disruption with strong adaptation.

**Recommended response:** identify resilience patterns and potential peer/change champions.

### Low MDI + High MAPI

Lower disruption with strong adaptation.

**Recommended response:** monitor and identify transferable adaptive behaviours.

### Low MDI + Low MAPI

Lower disruption with weaker adaptation.

**Recommended response:** investigate contextual factors before intervention.

---

## 14. Model Philosophy

The core principle of MAPI is:

> **Performance should be interpreted in context.**

Instead of treating performance decline as an isolated employee characteristic, the model considers:

**How much disruption occurred?**

**How much did performance change?**

**How quickly did the employee recover?**

**How did the employee perform relative to the disruption they experienced?**

This contextualisation forms the primary innovation of the framework.
