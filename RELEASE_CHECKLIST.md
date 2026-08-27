# Pre-release checklist

Complete this list before making the repository public.

- [ ] Add the complete six-site dataset, including `Busan_2016_2020_complete.csv`.
- [ ] Run `python scripts/validate_data.py` and confirm all six sites pass.
- [ ] Regenerate `data/checksums.sha256` after the final data files are frozen.
- [ ] Run the notebook once in smoke mode from a clean kernel.
- [ ] Run the full paper configuration from a clean environment.
- [ ] Confirm that no 2020 observation enters tuning, scaling, seed weighting, or aggregation calibration.
- [ ] Confirm that target-day `Solar` is never used as a predictor.
- [ ] Confirm that oracle-weather results are clearly labeled as controlled upper-bound results.
- [ ] Verify all benchmark implementations and repository references.
- [ ] Remove local paths, tokens, credentials, temporary files, and unpublished review correspondence.
- [ ] Confirm that figures/tables in the repository match the current manuscript version.
- [ ] Choose an explicit code license.
- [ ] Verify KMA data redistribution / attribution requirements before publishing processed data.
- [ ] Add the final article citation after acceptance/publication.
- [ ] Tag the reproducibility snapshot used for the accepted manuscript.
