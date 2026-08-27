#!/usr/bin/env python3
"""Validate the public MUFASA city CSV files before a paper-mode run."""

from __future__ import annotations

from pathlib import Path
import hashlib
import sys
import pandas as pd

REQUIRED_COLUMNS = {"Year", "Month", "Day", "Hour", "Temp", "Humi", "WS", "WD", "Solar"}
EXPECTED_SITES = {"Busan", "Daegu", "Daejeon", "Gwangju", "Incheon", "Seoul"}
EXPECTED_HOURS = list(range(8, 19))
EXPECTED_DATES = pd.date_range("2016-01-01", "2020-12-31", freq="D")
EXPECTED_ROWS = len(EXPECTED_DATES) * len(EXPECTED_HOURS)


def site_name(path: Path) -> str:
    return path.name.split("_2016_2020_complete")[0]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate(path: Path) -> dict:
    frame = pd.read_csv(path)
    missing_columns = REQUIRED_COLUMNS - set(frame.columns)
    if missing_columns:
        raise ValueError(f"{path.name}: missing columns {sorted(missing_columns)}")

    frame = frame.copy()
    frame["date"] = pd.to_datetime(frame[["Year", "Month", "Day"]], errors="raise")

    if len(frame) != EXPECTED_ROWS:
        raise ValueError(f"{path.name}: expected {EXPECTED_ROWS} rows, found {len(frame)}")

    hours = sorted(frame["Hour"].unique().tolist())
    if hours != EXPECTED_HOURS:
        raise ValueError(f"{path.name}: expected hours {EXPECTED_HOURS}, found {hours}")

    if frame.duplicated(["date", "Hour"]).any():
        raise ValueError(f"{path.name}: duplicate date-hour rows found")

    dates = pd.DatetimeIndex(sorted(frame["date"].unique()))
    if not dates.equals(EXPECTED_DATES):
        missing = len(EXPECTED_DATES.difference(dates))
        extra = len(dates.difference(EXPECTED_DATES))
        raise ValueError(f"{path.name}: date coverage mismatch; missing={missing}, extra={extra}")

    if frame[list(REQUIRED_COLUMNS)].isna().any().any():
        raise ValueError(f"{path.name}: missing required values found")

    if (frame["Solar"] < 0).any():
        raise ValueError(f"{path.name}: negative solar-radiation values found")

    return {
        "site": site_name(path),
        "rows": len(frame),
        "days": len(dates),
        "solar_mean": float(frame["Solar"].mean()),
        "solar_max": float(frame["Solar"].max()),
        "sha256": sha256(path),
    }


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    data_dir = repo_root / "data"
    files = sorted(data_dir.glob("*_2016_2020_complete.csv"))

    if not files:
        print("ERROR: no city CSV files found in data/", file=sys.stderr)
        return 2

    results = []
    failed = False
    for path in files:
        try:
            result = validate(path)
            results.append(result)
            print(
                f"PASS  {result['site']:<8} rows={result['rows']:,} "
                f"days={result['days']:,} solar_mean={result['solar_mean']:.4f}"
            )
        except Exception as exc:
            failed = True
            print(f"FAIL  {path.name}: {exc}", file=sys.stderr)

    found_sites = {item["site"] for item in results}
    missing_sites = sorted(EXPECTED_SITES - found_sites)
    extra_sites = sorted(found_sites - EXPECTED_SITES)

    print()
    print(f"Validated sites: {sorted(found_sites)}")
    if missing_sites:
        print(f"Missing paper sites: {missing_sites}")
    if extra_sites:
        print(f"Unexpected sites: {extra_sites}")

    checksum_path = data_dir / "checksums.sha256"
    checksum_lines = [
        f"{item['sha256']}  {item['site']}_2016_2020_complete.csv"
        for item in sorted(results, key=lambda x: x["site"])
    ]
    checksum_path.write_text("\n".join(checksum_lines) + ("\n" if checksum_lines else ""), encoding="utf-8")
    print(f"Checksums written to {checksum_path.relative_to(repo_root)}")

    if failed or missing_sites or extra_sites:
        print("\nValidation completed with a noncanonical paper dataset.")
        return 1

    print("\nAll six paper datasets passed validation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
