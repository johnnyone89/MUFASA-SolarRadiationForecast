# MUFASA

**Reproducible code and six-city hourly solar-radiation benchmark**

![Manuscript](https://img.shields.io/badge/manuscript-under%20review-orange)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Protocol](https://img.shields.io/badge/evaluation-locked%20chronology-brightgreen)

> **Manuscript status:** Under review.  
> This repository corresponds to the current review-stage version of the MUFASA study. Results, labels, and documentation may be updated during peer review.

MUFASA is a simplex-constrained multi-expert forecasting framework for **11-step hourly solar radiation forecasting from 08:00 to 18:00**. The public workflow combines a nonlinear temporal expert with a regularized Ridge expert, uses physically structured meteorological and solar-geometry representations, performs development-only model selection, and evaluates the final system on a chronologically locked 2020 test year.

## Current review-stage result snapshot

Under the controlled oracle-weather protocol, the current manuscript reports a six-site macro RMSE of **0.3431 MJ m⁻²**, macro MAE of **0.2447 MJ m⁻²**, and macro R² of **0.8739**. MUFASA achieved the lowest site-level RMSE at all six sites against 18 benchmark architectures and ranked first in **63 of 66** site–horizon comparisons.

These values are reported for transparency while the manuscript is under review. They should not be treated as final published claims until peer review is complete.

## Repository layout

```text
MUFASA_GitHub_Public_Release/
├── README.md
├── RELEASE_CHECKLIST.md
├── requirements.txt
├── .gitignore
├── data/
│   ├── README.md
│   ├── checksums.sha256
│   └── *_2016_2020_complete.csv
├── notebooks/
│   └── MUFASA_Public_Release.ipynb
├── scripts/
│   └── validate_data.py
└── outputs/
```

The notebook is intentionally organized into short, ordered execution blocks rather than a few very large cells. Each major stage is preceded by a Markdown explanation describing its purpose, dependencies, and run order.

## Experimental contract

The chronology is fixed before evaluation:

- **2016–2018:** primary training
- **2019:** architecture screening, Bayesian hyperparameter optimization, seed policy, and aggregation calibration
- **2020:** locked test year

No 2020 observation is used for hyperparameter search, scaler fitting, seed weighting, or aggregation calibration.

The primary paper experiment uses a **controlled oracle-weather protocol**. Observed target-horizon meteorology is supplied identically to all forecasting architectures and interpreted as a perfectly accurate day-ahead weather forecast. **Target-horizon solar radiation is never used as a predictor.** Therefore, reported oracle-weather performance is a controlled upper-bound result and should not be interpreted as direct operational NWP-driven performance.

## Data

A complete paper reproduction expects the following six files:

```text
Busan_2016_2020_complete.csv
Daegu_2016_2020_complete.csv
Daejeon_2016_2020_complete.csv
Gwangju_2016_2020_complete.csv
Incheon_2016_2020_complete.csv
Seoul_2016_2020_complete.csv
```

Each complete file contains **20,097 hourly daytime observations**, corresponding to **1,827 complete days × 11 forecast hours**.

Required columns are:

| Column | Description |
|---|---|
| `Year` | Calendar year |
| `Month` | Calendar month |
| `Day` | Calendar day |
| `Hour` | Hour of day; expected 08–18 |
| `Temp` | Air temperature |
| `Humi` | Relative humidity |
| `WS` | Wind speed |
| `WD` | Wind direction |
| `Solar` | Hourly accumulated global solar radiation |

The modeled response is hourly accumulated global solar radiation in **MJ m⁻²**.

The processed data lineage follows the KMA Meteorological Data Open Portal / ASOS workflow used in the manuscript. The processed derivative files do not retain original station identifiers or independent sensor metadata. City coordinates used by the notebook are reference coordinates for deterministic solar-geometry calculations and should not be interpreted as reconstructed sensor positions.

Before making the `data/` directory public, confirm the applicable KMA redistribution and attribution requirements.

## Quick start

Create an isolated environment:

```bash
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
# .venv\Scripts\activate       # Windows

python -m pip install --upgrade pip
pip install -r requirements.txt
```

Validate the data before opening the notebook:

```bash
python scripts/validate_data.py
```

Then start Jupyter:

```bash
jupyter lab notebooks/MUFASA_Public_Release.ipynb
```

## Runtime profiles

The public notebook starts in **smoke mode** by default.

| Mode | Purpose | CUDA | Suitable for paper results |
|---|---|---:|---:|
| `smoke` | Data, shape, dependency, and contract checks | Optional | No |
| `paper` + `thorough` | Full HPO, benchmark, inference, and XAI workflow | Recommended/required by guard | Yes |

For the manuscript configuration, restart the kernel and set these variables before running the notebook from the top:

```python
import os

os.environ["MUFASA_RUN_MODE"] = "paper"
os.environ["MUFASA_SPEED_PROFILE"] = "thorough"
os.environ["MUFASA_REQUIRE_CUDA"] = "1"
```

The full configuration is computationally expensive. Do not infer paper-level performance from smoke-mode outputs.

## Notebook execution order

The notebook is divided into ten stages:

1. Runtime and experiment contract
2. Data, chronology, and information boundaries
3. MUFASA nonlinear expert and training objective
4. Development selection and aggregation
5. Locked refit and 2020 evaluation
6. Matched-budget benchmark suite
7. Ablation, diagnostics, inference, and XAI
8. Publication artifacts
9. Oracle-weather manuscript XAI
10. Multi-horizon statistical analysis

Run the notebook **top to bottom** for a clean full reproduction. Individual downstream sections may be rerun only after their upstream objects have been created in the current kernel.

## Reproducibility safeguards

The public notebook includes fail-fast checks for:

- required data columns and exact 08:00–18:00 hourly coverage;
- duplicate or incomplete date–hour rows;
- non-finite or negative solar values;
- chronological split violations;
- target-day solar leakage;
- missing six-site data in paper mode;
- benchmark completeness;
- invalid or non-finite model predictions;
- seed and aggregation decisions that improperly depend on the 2020 test year.

SHA-256 checksums are generated for the supplied data files so that data revisions can be detected explicitly.

## Outputs

Generated artifacts are written under `outputs/`, including:

- data and protocol audits;
- development-screening tables;
- HPO and promoted-configuration records;
- locked 2020 prediction files;
- benchmark provenance and performance tables;
- horizon-wise rankings;
- dependence-aware statistical summaries;
- grouped permutation / XAI outputs;
- manuscript-oriented figures and tables.

Some analysis stages recreate their own output subdirectories. Do not store manually edited files inside generated output folders.

## Statistical interpretation

The repository separates **numerical ranking** from **inferential separation**. The manuscript workflow uses dependence-aware procedures, including HAC-based tests, moving-block bootstrap inference, multiplicity adjustment, and conservative model-set analysis. A lower RMSE is not automatically described as statistically unique superiority.

Likewise, permutation importance is interpreted as **predictive dependence**, not atmospheric causality.

## Citation

A formal article citation will be added after publication.

Until then, if this repository is used in a manuscript, presentation, or derivative analysis, please cite the GitHub repository together with the associated manuscript title and indicate that the paper is **under review**.

## License and redistribution

No code or data license is assigned automatically by this release template. Before publishing the repository, choose an explicit code license and verify that the source-data terms permit redistribution of the processed files. A common approach is to license code and data separately, but the appropriate choice depends on the original data-use terms.

## Contact / issues

For reproducibility questions, open a GitHub issue and include:

- operating system;
- Python and PyTorch versions;
- CUDA version and GPU model, if applicable;
- runtime profile;
- failing notebook stage;
- complete traceback;
- data-file checksums.

Please avoid uploading unpublished review correspondence or confidential manuscript material to public issues.
