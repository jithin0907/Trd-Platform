from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class Signal:
    """
    Standard trading signal produced by any strategy.
    """

    strategy: str
    symbol: str
    timeframe: str

    signal: bool = False          # True if a trade is found
    direction: Optional[str] = None   # BUY / SELL

    entry: Optional[float] = None
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None

    confidence: float = 0.0

    reasons: List[str] = field(default_factory=list)

    timestamp: datetime = field(default_factory=datetime.now)