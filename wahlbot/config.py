from dataclasses import dataclass, field
from datetime import timedelta


@dataclass(frozen=True)
class Config:
    scan_interval_hours: int = 6
    pre_election_interval_hours: int = 1
    poll_window_min_pct: float = 3.0
    poll_window_max_pct: float = 7.0
    min_edge_pct: float = 10.0
    min_ev: float = 0.05
    kelly_fraction: float = 0.25
    max_stake_usd: float = 25.0
    max_open_positions: int = 10
    approval_timeout_hours: int = 2
    order_fill_timeout_min: int = 30
    min_volume_usd: float = 5000.0
    market_prob_min: float = 0.10
    market_prob_max: float = 0.80
    resolution_min_days: int = 3
    resolution_max_days: int = 365
    close_race_research_enabled: bool = True
    close_race_band_pct: float = 8.0
    election_keywords: tuple[str, ...] = field(
        default_factory=lambda: (
            "election",
            "party",
            "threshold",
            "parliament",
            "landtagswahl",
            "state election",
            "ministerpraesident",
            "ministerpräsident",
            "rheinland-pfalz",
            "rlp",
            "afd",
            "fdp",
            "linke",
            "gruene",
            "spd",
            "cdu",
            "csu",
        )
    )

    @property
    def approval_timeout(self) -> timedelta:
        return timedelta(hours=self.approval_timeout_hours)


DEFAULT_CONFIG = Config()
