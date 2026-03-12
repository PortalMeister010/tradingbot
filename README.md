# Wahlbot

A modular Python scaffold for an automated prediction market bot focused on election markets.

## Current strategy coverage

- 5% threshold opportunities using poll/base-rate edge checks.
- Near-even election markets (roughly 50/50 within configurable band) to trigger AI research for high-uncertainty races, e.g. upcoming state elections.
- Both paths are merged into one prefilter pipeline so 5% and close-race candidates are handled consistently.

## Installation (Linux, Python 3.11+)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run CLI

```bash
python -m wahlbot.main
```

## Run GUI (Tkinter)

```bash
python -m wahlbot.gui
```

The GUI provides:
- Configuration fields (bankroll, poll filters, close-race band, max stake, min edge, min EV)
- Start button for `run_once`
- Results table (trade-id, market, proposal, agent assessment, status)
- CSV export button
- Local logs in `data/trade_log.jsonl` and GUI run logs in `data/gui_runs.jsonl`

## Test

```bash
pytest
```
