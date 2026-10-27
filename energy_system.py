"""Energy consumption and tariff calculator for Lab 5 static analysis."""

import json
from datetime import datetime
from pathlib import Path

RATE_TIER_1 = 3.5
RATE_TIER_2 = 5.0
RATE_TIER_3 = 7.5
SPIKE_LIMIT = 500
meters: dict[str, int] = {}


def record_reading(meter_id: str, units: int, history: list | None = None) -> list:
    """Record a meter reading, rejecting negative units."""
    if not meter_id.strip():
        raise ValueError("Meter ID must not be empty.")
    if not isinstance(units, int) or isinstance(units, bool):
        raise ValueError("Units must be an integer.")
    if units < 0:
        raise ValueError("Units cannot be negative.")

    if history is None:
        history = []
    history.append((meter_id, units, datetime.now().isoformat(timespec="seconds")))
    meters[meter_id] = meters.get(meter_id, 0) + units
    return history


def compute_bill(meter_id: str, tier_rates: list[float]) -> float:
    """Calculate a bill using three consumption tiers."""
    if meter_id not in meters:
        raise KeyError(f"Unknown meter ID: {meter_id}")
    if len(tier_rates) != 3:
        raise ValueError("Exactly three tier rates are required.")

    units = meters[meter_id]
    if units <= 100:
        return units * tier_rates[0]
    if units <= 300:
        return 100 * tier_rates[0] + (units - 100) * tier_rates[1]
    return (
        100 * tier_rates[0]
        + 200 * tier_rates[1]
        + (units - 300) * tier_rates[2]
    )


def raise_rates(percent: float) -> None:
    """Increase all tariff rates by a percentage."""
    if percent < 0:
        raise ValueError("Rate increase percentage cannot be negative.")
    global RATE_TIER_1, RATE_TIER_2, RATE_TIER_3
    multiplier = 1 + percent / 100
    RATE_TIER_1 *= multiplier
    RATE_TIER_2 *= multiplier
    RATE_TIER_3 *= multiplier


def flag_spikes() -> list[str]:
    """Return meter IDs whose accumulated usage exceeds the spike limit."""
    return [meter_id for meter_id, units in meters.items() if units > SPIKE_LIMIT]


def load_meter_data(file: str = "meters.json") -> None:
    """Load meter totals from a JSON file, using an empty mapping if absent/invalid."""
    global meters
    path = Path(file)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        meters = {}
        return
    except (OSError, json.JSONDecodeError, UnicodeError) as exc:
        raise ValueError(f"Could not load meter data from {path}") from exc

    if not isinstance(data, dict) or not all(
        isinstance(key, str) and isinstance(value, int) and value >= 0
        for key, value in data.items()
    ):
        raise ValueError("Meter data must be a JSON object of non-negative integer totals.")
    meters = data


def save_meter_data(file: str = "meters.json") -> None:
    """Save meter totals to a JSON file."""
    path = Path(file)
    path.write_text(json.dumps(meters, indent=2), encoding="utf-8")


def main() -> None:
    """Run a small demonstration of the tariff calculator."""
    history: list = []
    record_reading("M-01", 120, history)
    record_reading("M-02", 640, history)
    record_reading("M-03", 0, history)
    print(f"Readings stored so far: {len(history)}")
    raise_rates(10)
    rates = [RATE_TIER_1, RATE_TIER_2, RATE_TIER_3]
    print(f"Bill M-01: {compute_bill('M-01', rates):.2f}")
    print(f"Bill M-03: {compute_bill('M-03', rates):.2f}")
    print(f"Spikes: {flag_spikes()}")

    response = input("Extra non-negative integer units for M-01 (Enter for 0): ").strip()
    if response:
        try:
            extra_units = int(response)
            record_reading("M-01", extra_units, history)
        except ValueError as exc:
            print(f"Invalid extra units: {exc}")
            return

    save_meter_data()
    load_meter_data()
    print(f"Bill M-01 after reload: {compute_bill('M-01', rates):.2f}")


if __name__ == "__main__":
    main()
