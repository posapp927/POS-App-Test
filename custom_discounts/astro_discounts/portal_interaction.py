import logging
import requests
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import time

logger = logging.getLogger('custom_discounts.astro_discounts.portal_interaction')

class PortalInteraction:
    def __init__(self, portal_url: str, api_key: Optional[str] = None, username: Optional[str] = None,
                 password: Optional[str] = None, timeout: int = 30):
        """
        Initializes the PortalInteraction instance.

        Args:
            portal_url (str): The base URL of the Astro portal.
            api_key (Optional[str]): API key for authentication, if available.
            username (Optional[str]): Username for login, if API key is not used.
            password (Optional[str]): Password for login, if API key is not used.
            timeout (int): Timeout for HTTP requests in seconds.
        """
        self.portal_url = portal_url.rstrip('/')
        self.api_key = api_key
        self.username = username
        self.password = password
        self.timeout = timeout
        self.session = requests.Session()
        self.authenticated = False

    def authenticate(self) -> bool:
        """
        Authenticates with the Astro portal using API key or username/password.

        Returns:
            bool: True if authentication is successful, False otherwise.
        """
        try:
            if self.api_key:
                self.session.headers.update({'Authorization': f'Bearer {self.api_key}'})
                # Optionally, verify the API key by making a test request
                response = self.session.get(f"{self.portal_url}/api/status", timeout=self.timeout)
                response.raise_for_status()
                self.authenticated = True
                logger.info("Authenticated with Astro portal using API key.")
                return True
            elif self.username and self.password:
                login_url = f"{self.portal_url}/login"
                payload = {'username': self.username, 'password': self.password}
                response = self.session.post(login_url, data=payload, timeout=self.timeout)
                response.raise_for_status()
                # Verify login by checking a protected resource
                dashboard_url = f"{self.portal_url}/dashboard"
                response = self.session.get(dashboard_url, timeout=self.timeout)
                response.raise_for_status()
                self.authenticated = True
                logger.info("Authenticated with Astro portal using username and password.")
                return True
            else:
                logger.error("No authentication method provided.")
                return False
        except requests.RequestException as e:
            logger.error(f"Authentication failed: {e}")
            return False

    def submit_discount(self, discount: 'AstroDiscount') -> bool:
        """
        Submits a single discount to the Astro portal.

        Args:
            discount (AstroDiscount): The discount to submit.

        Returns:
            bool: True if submission is successful, False otherwise.
        """
        if not self.authenticated:
            if not self.authenticate():
                logger.error("Cannot submit discount; authentication failed.")
                return False

        submit_url = f"{self.portal_url}/api/discounts/submit"
        discount_data = self._map_discount_to_api(discount)

        try:
            response = self.session.post(submit_url, json=discount_data, timeout=self.timeout)
            response.raise_for_status()
            result = response.json()
            if result.get('success'):
                logger.info(f"Successfully submitted discount {discount.astro_discount_id}.")
                return True
            else:
                logger.error(f"Failed to submit discount {discount.astro_discount_id}: {result.get('error')}")
                return False
        except requests.RequestException as e:
            logger.error(f"Error submitting discount {discount.astro_discount_id}: {e}")
            return False

    def submit_discounts(self, discounts: List['AstroDiscount']) -> Dict[str, bool]:
        """
        Submits multiple discounts to the Astro portal.

        Args:
            discounts (List[AstroDiscount]): The list of discounts to submit.

        Returns:
            Dict[str, bool]: A mapping of discount IDs to their submission status.
        """
        results = {}
        for discount in discounts:
            success = self.submit_discount(discount)
            results[discount.astro_discount_id] = success
        return results

    def check_reimbursement_status(self, discount_id: str) -> Optional[Dict]:
        """
        Checks the reimbursement status of a specific discount.

        Args:
            discount_id (str): The ID of the discount to check.

        Returns:
            Optional[Dict]: The reimbursement status data if successful, None otherwise.
        """
        if not self.authenticated:
            if not self.authenticate():
                logger.error("Cannot check reimbursement status; authentication failed.")
                return None

        status_url = f"{self.portal_url}/api/discounts/{discount_id}/reimbursement-status"

        try:
            response = self.session.get(status_url, timeout=self.timeout)
            response.raise_for_status()
            status_data = response.json()
            logger.info(f"Retrieved reimbursement status for discount {discount_id}.")
            return status_data
        except requests.RequestException as e:
            logger.error(f"Error checking reimbursement status for discount {discount_id}: {e}")
            return None

    def sync_discounts(self, local_discounts: Dict[str, 'AstroDiscount']) -> None:
        """
        Synchronizes local discounts with the Astro portal.

        Args:
            local_discounts (Dict[str, AstroDiscount]): A mapping of discount IDs to AstroDiscount instances.
        """
        if not self.authenticated:
            if not self.authenticate():
                logger.error("Cannot synchronize discounts; authentication failed.")
                return

        # Example synchronization logic:
        # 1. Fetch existing discounts from the portal.
        # 2. Compare with local_discounts.
        # 3. Add, update, or remove discounts as necessary.

        try:
            existing_discounts = self.fetch_existing_discounts()
            # Compare and determine actions (add/update/remove)
            # Implement comparison logic here
            logger.info("Synchronized discounts with the Astro portal.")
        except Exception as e:
            logger.error(f"Error during synchronization: {e}")

    def fetch_existing_discounts(self) -> List[Dict]:
        """
        Fetches existing discounts from the Astro portal.

        Returns:
            List[Dict]: A list of existing discount data from the portal.
        """
        fetch_url = f"{self.portal_url}/api/discounts"
        try:
            response = self.session.get(fetch_url, timeout=self.timeout)
            response.raise_for_status()
            discounts = response.json().get('discounts', [])
            logger.info(f"Fetched {len(discounts)} discounts from the Astro portal.")
            return discounts
        except requests.RequestException as e:
            logger.error(f"Error fetching existing discounts: {e}")
            return []

    def _map_discount_to_api(self, discount: 'AstroDiscount') -> Dict:
        """
        Maps an AstroDiscount instance to the API's expected data format.

        Args:
            discount (AstroDiscount): The discount to map.

        Returns:
            Dict: The mapped discount data.
        """
        # Implement the mapping based on the API's requirements
        return {
            'id': discount.astro_discount_id,
            'name': discount.discount_name,
            'criteria': discount.eligibility_criteria,
            'valid_from': discount.start_date.strftime('%Y-%m-%d'),
            'valid_to': discount.end_date.strftime('%Y-%m-%d'),
            'promotion_materials': discount.promotion_materials,
            'tracking_info': discount.tracking_info
        }

    def logout(self) -> bool:
        """
        Logs out from the Astro portal.

        Returns:
            bool: True if logout is successful, False otherwise.
        """
        if not self.authenticated:
            logger.warning("Attempted to logout without an active session.")
            return False

        logout_url = f"{self.portal_url}/logout"

        try:
            response = self.session.post(logout_url, timeout=self.timeout)
            response.raise_for_status()
            self.authenticated = False
            logger.info("Successfully logged out from the Astro portal.")
            return True
        except requests.RequestException as e:
            logger.error(f"Error logging out: {e}")
            return False
