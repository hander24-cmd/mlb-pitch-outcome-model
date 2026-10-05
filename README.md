# MLB Expected Whiff Model

## Project Overview

This project builds a machine learning model to estimate the probability that an MLB pitch results in a swing and miss.

Using pitch-level Statcast data from the 2025 MLB season, the model evaluates pitch characteristics and game context to calculate an expected whiff probability, or xWhiff, for each pitch.

The model is then used to compare expected and actual whiff rates, allowing individual pitcher-pitch combinations to be evaluated based on how much they outperform or underperform model expectations.

## Research Question

Given the characteristics and context of an MLB pitch, how likely is it to generate a swing and miss, and which pitches outperform that expectation?

## Dataset

The analysis uses 711,897 MLB pitches from the 2025 season.

Pitch-level features include:

- Release velocity
- Spin rate
- Horizontal and vertical pitch movement
- Release extension
- Horizontal and vertical pitch location
- Pitch type
- Ball-strike count
- Pitcher handedness
- Batter handedness
- Pitcher-batter handedness matchup

The target variable is whether the pitch resulted in a whiff.

## Methodology

To simulate prediction on future pitches, the data was split chronologically rather than randomly.

- Training period: March through August 2025
- Test period: September 2025
- Training pitches: 601,559
- Test pitches: 110,338

Numeric variables were median-imputed and standardized, while categorical variables were imputed and one-hot encoded.

Two machine learning models were evaluated:

1. Logistic Regression
2. Histogram-based Gradient Boosting

A constant-probability model was also included as a baseline.

## Model Performance

| Model | ROC-AUC | Log Loss |
| --- | ---: | ---: |
| Constant Baseline | 0.500 | 0.358 |
| Logistic Regression | 0.648 | 0.345 |
| Gradient Boosting | **0.751** | **0.316** |

Gradient Boosting produced the strongest out-of-sample performance with a ROC-AUC of 0.751 and Log Loss of 0.316.

The improvement over Logistic Regression suggests that nonlinear relationships and interactions between pitch characteristics are important when predicting swing-and-miss probability.

## ROC Curve

![ROC Curve](figures/roc_curve.png)

The Gradient Boosting model provides substantially better discrimination between whiffs and non-whiffs than both the Logistic Regression model and a random classifier.

## Expected Whiff Analysis

The Gradient Boosting model was used to generate an expected whiff probability, or xWhiff, for every pitch in the September test set.

Expected and actual whiff rates were then aggregated by pitch type and individual pitcher-pitch combinations.

## Actual vs Expected Whiff Rate

![Actual vs Expected Whiff](figures/actual_vs_expected_whiff.png)

Pitcher-pitch combinations above the diagonal generated more whiffs than predicted by the model, while combinations below the diagonal generated fewer whiffs than expected.

The overall relationship between expected and actual whiff rate indicates that the model captures meaningful differences in pitch quality while still leaving room to identify pitches that outperform their underlying characteristics.

## Whiff Above Expected

Whiff Above Expected is defined as:

**Whiff Above Expected = Actual Whiff Rate - Expected Whiff Rate**

Positive values indicate that a pitch generated more whiffs than predicted by the model.

![Whiff Above Expected](figures/whiff_above_expected.png)

Among qualifying pitcher-pitch combinations in the September test period, several pitches substantially exceeded their expected whiff rates. Clayton Beeter's slider showed the largest positive difference in the sample, followed by sliders from Emmet Sheehan and other high-performing pitcher-pitch combinations.

These results demonstrate how an expected-whiff model can be used not only for prediction, but also for pitcher and pitch evaluation.

## Feature Importance

Permutation importance was used to estimate how strongly each feature contributed to the Gradient Boosting model's predictive performance.

![Feature Importance](figures/feature_importance.png)

Vertical pitch location relative to the strike zone was the most important feature in the model. Pitch type was the second most important predictor, followed by vertical movement, horizontal location, and horizontal movement.

The results suggest that where a pitch is located, what type of pitch is thrown, and how the pitch moves are major factors in determining swing-and-miss probability.

## Key Findings

- Gradient Boosting substantially outperformed Logistic Regression, reaching a test ROC-AUC of 0.751.
- The model improved Log Loss from the constant baseline of 0.358 to 0.316.
- Pitch location was particularly important for predicting whiffs, with normalized vertical location producing the largest permutation importance.
- Pitch type and pitch movement were also major contributors to model performance.
- Comparing actual whiff rate with xWhiff provides a framework for identifying individual pitches that generate more swing-and-miss than their characteristics would predict.
- Several pitcher-pitch combinations substantially exceeded model expectations during the September test period.

## Repository Structure

```text
mlb-pitch-outcome-model/
│
├── data/
├── figures/
│   ├── roc_curve.png
│   ├── actual_vs_expected_whiff.png
│   ├── whiff_above_expected.png
│   └── feature_importance.png
│
├── notebooks/
│   └── final_whiff_model.ipynb
│
├── src/
│   └── download_full_data.py
│
├── .gitignore
├── README.md
└── requirements.txt