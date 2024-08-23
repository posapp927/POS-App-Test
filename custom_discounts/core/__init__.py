"""
Core module for the CustomDiscounts system. This module contains the fundamental classes and
logic for handling discounts, promotions, strategies, and more.

Modules:
    discount.py: Contains the Discount, DiscountStrategy, Promotion, DiscountApplicationContext, DiscountLogger, and DiscountValidator classes.
    discounts.py: Contains the Discounts class which manages multiple Discount instances.
    industry_specific_base.py: Provides the base class for industry-specific discounts.
    promotion_material_manager.py: Manages promotional materials associated with discounts.
    notification_system.py: Handles notifications related to discount activities.
"""

# Import key classes for easy access when importing the core module
from .discount import Discount, DiscountStrategy, Promotion, DiscountApplicationContext, DiscountLogger, DiscountValidator
from .discounts import Discounts
from .industry_specific_base import IndustrySpecificDiscountBase
from .promotion_material_manager import PromotionMaterialManager
from .notification_system import NotificationSystem

__all__ = [
    "Discount",
    "DiscountStrategy",
    "Promotion",
    "DiscountApplicationContext",
    "DiscountLogger",
    "DiscountValidator",
    "Discounts",
    "IndustrySpecificDiscountBase",
    "PromotionMaterialManager",
    "NotificationSystem",
]
