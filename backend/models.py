from pydantic import BaseModel, Field
from typing import List

class TrackedScript(BaseModel):
    symbol: str
    type: str = "index"

class AppConfig(BaseModel):
    tracked_scripts: List[TrackedScript] = Field(default_factory=lambda: [TrackedScript(symbol="NIFTY", type="index")])
    refresh_interval: int = 30
