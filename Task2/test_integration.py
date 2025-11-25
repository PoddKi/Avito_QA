"""
Интеграционные тест-кейсы
TestCase 19-20
"""
import pytest
from api_client import AdsAPIClient


class TestIntegration:
    def test_case_19_full_cycle_create_and_get_ad(self, api_client):
        seller_id = api_client.generate_unique_seller_id()
        ad_data = {
            "seller_id": seller_id,
            "name": "Integration Test Item",
            "price": 15000,
            "statistics": {
                "likes": 50,
                "viewCount": 100,
                "contacts": 25
            }
        }
        
        create_response = api_client.create_ad(
            seller_id=ad_data["seller_id"],
            name=ad_data["name"],
            price=ad_data["price"],
            statistics=ad_data["statistics"]
        )
        
        assert create_response.status_code == 200, \
            f"Ожидался статус 200 при создании, получен {create_response.status_code}"
        created_ad = create_response.json()
        item_id = created_ad["id"]
        
        get_response = api_client.get_ad_by_id(item_id)
        assert get_response.status_code == 200, f"Ожидался статус 200 при получении, получен {get_response.status_code}"
        get_response_data = get_response.json()
        assert isinstance(get_response_data, list) and len(get_response_data) > 0
        retrieved_ad = get_response_data[0]
        assert retrieved_ad["id"] == item_id
        assert retrieved_ad["sellerId"] == ad_data["seller_id"]
        assert retrieved_ad["name"] == ad_data["name"]
        assert retrieved_ad["price"] == ad_data["price"]
        
        seller_ads_response = api_client.get_ads_by_seller_id(seller_id)
        assert seller_ads_response.status_code == 200, \
            f"Ожидался статус 200 при получении по sellerId, получен {seller_ads_response.status_code}"
        seller_ads = seller_ads_response.json()
        assert isinstance(seller_ads, list)

        seller_ad_ids = [ad["id"] for ad in seller_ads]
        assert item_id in seller_ad_ids, \
            "Созданное объявление должно присутствовать в списке объявлений продавца"
        
        stats_response = api_client.get_statistics_by_item_id(item_id)
        assert stats_response.status_code == 200, \
            f"Ожидался статус 200 при получении статистики, получен {stats_response.status_code}"
        stats_data = stats_response.json()
        assert isinstance(stats_data, list) and len(stats_data) > 0
        stats = stats_data[0]
        assert "likes" in stats and "viewCount" in stats and "contacts" in stats
    
    def test_case_20_create_and_get_multiple_ads_for_one_seller(self, api_client):
        seller_id = api_client.generate_unique_seller_id()
        
        created_ads = []
        for i in range(3):
            response = api_client.create_ad(
                seller_id=seller_id,
                name=f"Item {i+1}",
                price=1000 * (i + 1),
                statistics={
                    "likes": 10 * (i + 1),
                    "viewCount": 20 * (i + 1),
                    "contacts": 5 * (i + 1)
                }
            )
            assert response.status_code == 200, \
                f"Ожидался статус 200 при создании объявления {i+1}, получен {response.status_code}"
            created_ads.append(response.json())
        
        assert len(created_ads) == 3, "Должно быть создано 3 объявления"
        
        seller_ads_response = api_client.get_ads_by_seller_id(seller_id)
        assert seller_ads_response.status_code == 200, \
            f"Ожидался статус 200, получен {seller_ads_response.status_code}"
        seller_ads = seller_ads_response.json()
        assert isinstance(seller_ads, list)
        assert len(seller_ads) >= 3, \
            f"Список должен содержать не менее 3 объявлений, получено {len(seller_ads)}"
        
        created_ids = {ad["id"] for ad in created_ads}
        seller_ad_ids = {ad["id"] for ad in seller_ads}
        
        assert created_ids.issubset(seller_ad_ids), \
            "Все созданные объявления должны присутствовать в списке"
        
        for created_ad in created_ads:
            item_id = created_ad["id"]
            get_response = api_client.get_ad_by_id(item_id)
            assert get_response.status_code == 200, \
                f"Ожидался статус 200 при получении объявления {item_id}, получен {get_response.status_code}"
            
            get_response_data = get_response.json()
            assert isinstance(get_response_data, list) and len(get_response_data) > 0
            retrieved_ad = get_response_data[0]
            
            assert retrieved_ad["id"] == created_ad["id"]
            assert retrieved_ad["sellerId"] == created_ad["sellerId"]
            assert retrieved_ad["name"] == created_ad["name"]
            assert retrieved_ad["price"] == created_ad["price"]
            assert retrieved_ad["statistics"]["likes"] == created_ad["statistics"]["likes"]
            assert retrieved_ad["statistics"]["viewCount"] == created_ad["statistics"]["viewCount"]
            assert retrieved_ad["statistics"]["contacts"] == created_ad["statistics"]["contacts"]

