from dataclasses import dataclass, field
from typing import List, Tuple

Pos = Tuple[int, int]


@dataclass
class SearchResult:
    found: bool
    algorithm: str
    path: List[Pos] = field(default_factory=list)
    actions: List[str] = field(default_factory=list)
    cost: float = float("inf")
    generated: int = 0
    expanded: int = 0
    peak_frontier = max(peak_frontier, len(frontier))
    peak_stored = max(peak_stored, len(frontier_states | explored))

    @property
    def steps(self) -> int:
        return len(self.actions)
