import math

def growth_requirement(level: int, base: float, rate: float = 1.18, log_weight: float = 0.5) -> float:
    """
    Calculates a gradually increasing requirement using a hybrid exponential-logarithmic growth model.

    This model starts faster than pure exponential growth and slows slightly over time to avoid overly steep difficulty spikes.

    Formula:
        R(n) = base * (rate ** n) + (log_weight * base * log2(n + 1))

    Args:
        level (int): The mission or progression level (e.g. 1, 2, 3...).
        base (float): The base value for the first level (starting score or coin requirement).
        rate (float): The exponential rate (default 1.18). Higher = faster growth.
        log_weight (float): How much the logarithmic component contributes. 
                            Higher = slightly steeper start, slower late growth.

    Returns:
        int: The scaled requirement for the given level rounded to the nearest 10.
    """
    raw_value =  base * (rate ** level) + (log_weight * base * math.log2(level + 1))
    return int(round(raw_value / 10) * 10)

def get_score_requirement(level):
    return growth_requirement(level, base=205, rate=2.18, log_weight=0.5)

def get_vault_balance_requirement(level):
    return growth_requirement(level, base=30, rate=1.50, log_weight=0.3)
