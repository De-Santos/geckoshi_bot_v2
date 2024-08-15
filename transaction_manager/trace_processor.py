from enum import Enum
from typing import Any


class TraceType(Enum):
    SLOTS_BET = 1


def generate_trace(trace_t: TraceType, connector: str | int) -> dict[int, Any]:
    return {trace_t.value: connector}
