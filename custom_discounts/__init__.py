# custom_discounts/__init__.py

from .core.discount import Discount, DiscountStrategy, Promotion, DiscountApplicationContext, DiscountLogger, DiscountValidator
from .core.discounts import Discounts
from .core.industry_specific_base import IndustrySpecificDiscountBase
from .core.promotion_material_manager import PromotionMaterialManager
from .core.notification_system import NotificationSystem

from .astro_discounts.astro_discount import AstroDiscount, AstroDiscountManager
from .astro_discounts.astro_scraper import AstroDiscountScraper

from .factories.discount_factory import DiscountFactory
from .factories.promotion_factory import PromotionFactory
from .factories.strategy_factory import StrategyFactory
from .factories.industry_discount_factory import IndustrySpecificDiscountFactory

class CustomDiscounts:
    def __init__(self, discount_factory=None, promotion_factory=None, strategy_factory=None, industry_discount_factory=None, logger=None, notification_system=None):
        """
        Initialize the CustomDiscounts manager with all necessary factories and managers.

        Args:
            discount_factory (DiscountFactory): Factory to create Discount instances.
            promotion_factory (PromotionFactory): Factory to create Promotion instances.
            strategy_factory (StrategyFactory): Factory to create DiscountStrategy instances.
            industry_discount_factory (IndustrySpecificDiscountFactory): Factory to create industry-specific discounts.
            logger (DiscountLogger): Logger to handle logging within the discount system.
            notification_system (NotificationSystem): Handles notifications related to discounts and promotions.
        """
        self.discount_factory = discount_factory if discount_factory else DiscountFactory()
        self.promotion_factory = promotion_factory if promotion_factory else PromotionFactory()
        self.strategy_factory = strategy_factory if strategy_factory else StrategyFactory()
        self.industry_discount_factory = industry_discount_factory if industry_discount_factory else IndustrySpecificDiscountFactory()
        self.logger = logger if logger else DiscountLogger(log_level='INFO')
        self.notification_system = notification_system if notification_system else NotificationSystem()

        self.discounts = Discounts()  # Manages multiple Discount instances
        self.promotions = {}
        self.strategies = {}

        # Initialize AstroDiscount Manager if industry-specific discounts are used
        self.astro_manager = AstroDiscountManager(scraper=AstroDiscountScraper(), logger=self.logger, notification_system=self.notification_system)

    def add_discount(self, discount_id, discount_type=None, **kwargs):
        discount = self.discount_factory.create_discount(discount_id, discount_type, **kwargs)
        self.discounts.add_discount(discount_id, discount_type=discount_type, **kwargs)
        self.logger.log(f"Added discount with ID: {discount_id}")

    def add_promotion(self, promotion_name, discount_ids=None, **kwargs):
        promotion = self.promotion_factory.create_promotion(promotion_name, discount_ids, **kwargs)
        self.promotions[promotion_name] = promotion
        self.logger.log(f"Added promotion: {promotion_name}")

    def add_strategy(self, strategy_name, **kwargs):
        strategy = self.strategy_factory.create_strategy(strategy_name, **kwargs)
        self.strategies[strategy_name] = strategy
        self.logger.log(f"Added strategy: {strategy_name}")

    def add_industry_discount(self, industry_type, **kwargs):
        industry_discount = self.industry_discount_factory.create_industry_discount(industry_type, **kwargs)
        self.discounts.add_discount(industry_discount.discount_id, discount_type=industry_type, **kwargs)
        self.logger.log(f"Added industry-specific discount of type: {industry_type}")

    def apply_discounts(self, cart):
        """
        Apply all discounts to the items in the cart.

        Args:
            cart (Cart): The shopping cart to which discounts will be applied.
        """
        self.logger.log("Applying discounts to the cart.")
        total_discount = self.discounts.apply_discounts(cart)
        self.logger.log(f"Total discount applied: {total_discount}")

    def manage_astro_discounts(self):
        """
        Manage the lifecycle and application of Astro discounts.
        This includes scraping updates, notifying users, and interacting with the portal.
        """
        self.astro_manager.update_discounts()
        self.astro_manager.notify_users()
        self.astro_manager.check_reimbursement_status()
        self.logger.log("Managed Astro discounts.")

# Initialize the main custom discounts handler
custom_discounts_handler = CustomDiscounts()
