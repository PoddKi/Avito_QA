"""
Тест-кейсы для ручки: Создать объявление
TestCase 1-6
"""
import pytest
from api_client import AdsAPIClient


class TestCreateAd:
    def test_case_1_successful_creation_with_valid_data(self, api_client):
        seller_id = api_client.generate_unique_seller_id()
        ad_data = {
            "seller_id": seller_id,
            "name": "Test Item",
            "price": 9900,
            "statistics": {
                "likes": 21,
                "viewCount": 11,
                "contacts": 43
            }
        }
        
        response = api_client.create_ad(
            seller_id=ad_data["seller_id"],
            name=ad_data["name"],
            price=ad_data["price"],
            statistics=ad_data["statistics"]
        )
        
        assert response.status_code == 201 or response.status_code == 200, f"Ожидался статус 201, получен {response.status_code}"
        response_data = response.json()
        
        assert "id" in response_data, "В ответе должно быть поле id"
        assert response_data["sellerId"] == ad_data["seller_id"]
        assert response_data["name"] == ad_data["name"]
        assert response_data["price"] == ad_data["price"]
        assert response_data["statistics"]["likes"] == ad_data["statistics"]["likes"]
        assert response_data["statistics"]["viewCount"] == ad_data["statistics"]["viewCount"]
        assert response_data["statistics"]["contacts"] == ad_data["statistics"]["contacts"]
    
    def test_case_2_create_ad_with_minimal_data(self, api_client):
        seller_id = api_client.generate_unique_seller_id()
        
        response = api_client.create_ad(
            seller_id=seller_id,
            name="Minimal Item",
            price=1000,
            statistics={
                "likes": 1,  
                "viewCount": 1,
                "contacts": 1
            }
        )
        
        assert response.status_code == 201 or response.status_code == 200, f"Ожидался статус 201, получен {response.status_code}. Ответ: {response.text}"
        response_data = response.json()
        assert "id" in response_data, "Объявление должно быть создано с ID"
    
    def test_case_3_create_multiple_ads_with_different_seller_ids(self, api_client):
        seller_ids = [api_client.generate_unique_seller_id() for _ in range(3)]
        responses = []
        
        for seller_id in seller_ids:
            response = api_client.create_ad(
                seller_id=seller_id,
                name=f"Item for seller {seller_id}",
                price=5000,
                statistics={"likes": 10, "viewCount": 5, "contacts": 2}
            )
            responses.append(response)
        
        for response in responses:
            assert response.status_code == 201 or response.status_code == 200, f"Ожидался статус 201, получен {response.status_code}"
            response_data = response.json()
            assert "id" in response_data, "Каждое объявление должно быть создано успешно"
    
    def test_case_4_create_ad_without_required_fields(self, api_client):
        url = f"{api_client.base_url}/item"
        payload = {
            "name": "Test Item",
            "price": 9900,
            "statistics": {
                "likes": 0,
                "viewCount": 0,
                "contacts": 0
            }
        }
        
        response = api_client.session.post(url, json=payload)
        
        assert response.status_code == 400 or response.status_code == 404, f"Ожидался статус 400, получен {response.status_code}"
        response_data = response.json()
        assert "result" in response_data or "message" in response_data or "status" in response_data, \
            "Должно быть сообщение об ошибке"
    
    def test_case_5_create_ad_with_invalid_data_type(self, api_client):
        url = f"{api_client.base_url}/item"
        payload = {
            "sellerID": "invalid_string",
            "name": "Test Item",
            "price": 9900,
            "statistics": {
                "likes": 0,
                "viewCount": 0,
                "contacts": 0
            }
        }
        
        response = api_client.session.post(url, json=payload)
        
        assert response.status_code == 400 or response.status_code == 404, f"Ожидался статус 400, получен {response.status_code}"
        response_data = response.json()
        assert "result" in response_data or "message" in response_data or "status" in response_data, \
            "Должно быть сообщение об ошибке"
    
    def test_case_6_create_ad_with_empty_body(self, api_client):
        url = f"{api_client.base_url}/item"
        
        response = api_client.session.post(url, json={})
        
        assert response.status_code == 400 or response.status_code == 404, f"Ожидался статус 400, получен {response.status_code}"
        response_data = response.json()
        assert "result" in response_data or "message" in response_data or "status" in response_data, \
            "Должно быть сообщение об ошибке"

