from dataclasses import dataclass
@dataclass
class InventoryParams:
    D: float
    T_total: int
    LD: int
    T: int
    Q: float
    initial_ioh: float
    sigma: float = 0
    S: float = 0
    H: float = 0
    