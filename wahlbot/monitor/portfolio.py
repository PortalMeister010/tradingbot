from dataclasses import dataclass


@dataclass
class Position:
    market_id: str
    contracts: int
    average_price_cents: int


class Portfolio:
    def __init__(self) -> None:
        self.positions: dict[str, Position] = {}

    def upsert(self, position: Position) -> None:
        self.positions[position.market_id] = position

    def open_positions(self) -> list[Position]:
        return list(self.positions.values())
