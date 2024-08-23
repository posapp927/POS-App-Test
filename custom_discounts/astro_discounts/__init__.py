import logging
from .astro_discount import AstroDiscount, AstroDiscountManager, AstroDiscountScraper
from .astro_scraper import AstroScraper
from .portal_interaction import PortalInteraction
from .astro_discount_notification import AstroDiscountNotificationSystem

# Initialize logging for the astro_discounts package
logger = logging.getLogger('custom_discounts.astro_discounts')
logger.setLevel(logging.DEBUG)

# Initialize necessary classes and objects for Astro discounts
def initialize_astro_discounts(api_key=None, scraping_interval=None, notification_settings=None):
    """
    Initialize the Astro discounts system.

    Args:
        api_key (str): API key for interacting with the Astro portal.
        scraping_interval (str): Interval for scraping new discounts (e.g., "daily", "weekly").
        notification_settings (dict): Settings for notifications (e.g., methods, frequency).
    """
    logger.info("Initializing Astro discounts system.")

    # Initialize AstroDiscountManager with API key
    astro_discount_manager = AstroDiscountManager(api_key=api_key)

    # Initialize the scraper with the given interval
    astro_scraper = AstroDiscountScraper(scraping_interval=scraping_interval)
    astro_discount_manager.set_scraper(astro_scraper)

    # Initialize portal interaction
    portal_interaction = PortalInteraction(api_key=api_key)
    astro_discount_manager.set_portal_interaction(portal_interaction)

    # Initialize the notification system
    notification_system = AstroDiscountNotificationSystem(settings=notification_settings)
    astro_discount_manager.set_notification_system(notification_system)

    logger.info("Astro discounts system initialized successfully.")
    return astro_discount_manager

# Expose key classes and functions to make them easily accessible
__all__ = [
    'AstroDiscount',
    'AstroDiscountManager',
    'AstroDiscountScraper',
    'AstroScraper',
    'PortalInteraction',
    'AstroDiscountNotificationSystem',
    'initialize_astro_discounts'
]
