# Wahlbot

A modular Python scaffold for an automated prediction market bot focused on election markets.

## Current strategy coverage

- 5% threshold opportunities using poll/base-rate edge checks.
- Near-even election markets (roughly 50/50 within configurable band) to trigger AI research for high-uncertainty races, e.g. upcoming state elections.

## Run

```bash
python -m wahlbot.main
```

## Test

```bash
pytest
```
