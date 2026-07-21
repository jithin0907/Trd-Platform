from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Trade:
    """
    Represents an executed or simulated trade.
    """

    strategy: str
    symbol: str
    timeframe: str

    direction: str

    entry_price: float
    stop_loss: float
    take_profit: float

    lot_size: float

    status: str = "OPEN"        # OPEN / CLOSED

    ticket: Optional[int] = None

    open_time: datetime = field(default_factory=datetime.now)
    close_time: Optional[datetime] = None

    exit_price: Optional[float] = None

    profit: float = 0.0

    exit_reason: Optional[str] = None