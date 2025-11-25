"""
Тест-кейсы для ручки: Получить объявление по идентификатору
TestCase 7-10
"""
import pytest
from api_client import AdsAPIClient


class TestGetAdById:

    def test_case_7_successful_get_existing_ad(self, api_client, created_ad):
        item_id = created_ad["id"]
        
        response = api_client.get_ad_by_id(item_id)
        
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        response_data = response.json()
        
        assert isinstance(response_data, list), "Ответ должен быть массивом"
        assert len(response_data) > 0, "Массив не должен быть пустым"
        
        ad = response_data[0]
        assert ad["id"] == created_ad["id"]
        assert ad["sellerId"] == created_ad["sellerId"]
        assert ad["name"] == created_ad["name"]
        assert ad["price"] == created_ad["price"]
    
    def test_case_8_get_ad_with_additional_parameters(self, api_client, created_ad):
        item_id = created_ad["id"]
        
        response = api_client.get_ad_by_id(item_id, fields="additional_field")
        
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        response_data = response.json()
        assert isinstance(response_data, list), "Ответ должен быть массивом"
        assert len(response_data) > 0, "Массив не должен быть пустым"
    
    def test_case_9_get_nonexistent_ad(self, api_client):
        nonexistent_id = "00000000-0000-0000-0000-000000000000"
        
        response = api_client.get_ad_by_id(nonexistent_id)
        
        assert response.status_code in [400, 404], f"Ожидался статус 400 или 404, получен {response.status_code}"
        response_data = response.json()
        assert "result" in response_data or "status" in response_data, \
            "Должно быть сообщение об ошибке"
    
    def test_case_10_get_ad_with_invalid_id(self, api_client):
        invalid_id = "abc"
        
        response = api_client.get_ad_by_id(invalid_id)
        
        assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"
        response_data = response.json()
        assert "result" in response_data or "status" in response_data, \
            "Должно быть сообщение об ошибке"

