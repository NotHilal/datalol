"""
Validation utility functions
"""
from typing import Optional


def validate_pagination(page: int, page_size: int, max_page_size: int = 100) -> Optional[str]:
    """
    Validate pagination parameters
    Returns error message if invalid, None if valid
    """
    if page < 1:
        return "Page must be greater than 0"

    if page_size < 1:
        return "Page size must be greater than 0"

    if page_size > max_page_size:
        return f"Page size must not exceed {max_page_size}"

    return None


def validate_tier(tier: str) -> bool:
    """Validate tier is a valid League of Legends tier"""
    valid_tiers = ['IRON', 'BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'EMERALD', 'DIAMOND', 'MASTER', 'GRANDMASTER', 'CHALLENGER']
    return tier.upper() in valid_tiers


def validate_rank(rank: str) -> bool:
    """Validate rank is a valid division"""
    valid_ranks = ['I', 'II', 'III', 'IV']
    return rank.upper() in valid_ranks
