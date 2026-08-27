# Data directory

This directory contains the processed hourly daytime datasets used by the MUFASA reproducibility workflow.

## Expected paper dataset

A complete paper-mode run expects six city files:

- `Busan_2016_2020_complete.csv`
- `Daegu_2016_2020_complete.csv`
- `Daejeon_2016_2020_complete.csv`
- `Gwangju_2016_2020_complete.csv`
- `Incheon_2016_2020_complete.csv`
- `Seoul_2016_2020_complete.csv`

Each complete file should contain 20,097 rows = 1,827 days × 11 hourly observations from 08:00 through 18:00.

## Schema

| Field | Meaning |
|---|---|
| `Year` | Calendar year |
| `Month` | Calendar month |
| `Day` | Calendar day |
| `Hour` | Hour of day |
| `Temp` | Air temperature |
| `Humi` | Relative humidity |
| `WS` | Wind speed |
| `WD` | Wind direction |
| `Solar` | Hourly accumulated global solar radiation |

The response variable `Solar` is treated as hourly accumulated global solar radiation in MJ m⁻².

## Integrity rules

The public notebook and `scripts/validate_data.py` verify that:

1. all required columns are present;
2. each day contains exactly the 11 target hours;
3. the chronology covers 2016-01-01 through 2020-12-31;
4. no duplicate date-hour rows exist;
5. no missing required values remain;
6. solar radiation is non-negative;
7. paper mode contains the exact six expected sites.

## Provenance note

The manuscript documents the KMA Meteorological Data Open Portal / ASOS workflow as the source lineage for these processed observations.

The processed derivative files do **not** retain original station identifiers or separate sensor-metadata records. Any city coordinates used in the forecasting code are fixed reference coordinates for solar-geometry calculations and are not reconstructed sensor locations.

Before publicly redistributing processed meteorological data, verify the applicable source-data license, attribution, and redistribution requirements.

## Checksums

`checksums.sha256` records the SHA-256 hash of each supplied CSV. Regenerate the file whenever a dataset is intentionally replaced.
