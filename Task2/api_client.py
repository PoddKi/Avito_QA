import requests
from typing import Dict, Any, Optional, List
import random


class AdsAPIClient:  
    BASE_URL = "https://qa-internship.avito.com"
    
    def __init__(self, base_url: str = None):
        self.base_url = base_url or self.BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json"
        })
    
    def generate_unique_seller_id(self) -> int:
        return random.randint(111111, 999999)
    
    def create_ad(self, seller_id: int, name: str, price: int, statistics: Dict[str, int] = None) -> requests.Response:
        """       
        Args:
            seller_id: ID продавца
            name: Название объявления
            price: Цена
            statistics: Статистика (likes, viewCount, contacts)
        
        Returns:
            Response объект
        """
        url = f"{self.base_url}/api/1/item"
        payload = {
            "sellerID": seller_id,
            "name": name,
            "price": price
        }
        
        if statistics:
            payload["statistics"] = statistics
        else:
            payload["statistics"] = {
                "likes": 0,
                "viewCount": 0,
                "contacts": 0
            }
        
        response = self.session.post(url, json=payload)
        
        if response.status_code == 200:
            try:
                response_data = response.json()
                if "status" in response_data and "id" not in response_data:
                    import re
                    status_text = str(response_data.get("status", ""))
                    uuid_match = re.search(r'([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})', status_text, re.IGNORECASE)
                    if uuid_match:
                        item_id = uuid_match.group(1)
                        get_response = self.get_ad_by_id(item_id)
                        if get_response.status_code == 200:
                            get_data = get_response.json()
                            if isinstance(get_data, list) and len(get_data) > 0:
                                class MockResponse:
                                    def __init__(self, data, original_response):
                                        self.status_code = 200
                                        self._json_data = data
                                        self.headers = original_response.headers
                                        self.text = original_response.text
                                    
                                    def json(self):
                                        return self._json_data
                                
                                return MockResponse(get_data[0], response)
            except Exception as e:
                pass  
        
        return response
    
    def get_ad_by_id(self, item_id: str, fields: Optional[str] = None) -> requests.Response:
        """
        Args:
            item_id: ID объявления
            fields: Дополнительные поля (опционально)
        
        Returns:
            Response объект
        """
        url = f"{self.base_url}/api/1/item/{item_id}"
        params = {}
        if fields:
            params["fields"] = fields
        
        return self.session.get(url, params=params)
    
    def get_ads_by_seller_id(self, seller_id: int, page: Optional[int] = None, size: Optional[int] = None) -> requests.Response:
        """        
        Args:
            seller_id: ID продавца
            page: Номер страницы (опционально)
            size: Размер страницы (опционально)
        
        Returns:
            Response объект
        """
        url = f"{self.base_url}/api/1/{seller_id}/item"
        params = {}
        if page is not None:
            params["page"] = page
        if size is not None:
            params["size"] = size
        
        return self.session.get(url, params=params)
    
    def get_statistics_by_item_id(self, item_id: str) -> requests.Response:
        """
        Args:
            item_id: ID объявления
        
        Returns:
            Response объект
        """
        url = f"{self.base_url}/api/1/statistic/{item_id}"
        return self.session.get(url)

