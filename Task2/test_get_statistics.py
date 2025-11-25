"""
Тест-кейсы для ручки: Получить статистику по item id
TestCase 16-18
"""
import pytest
from api_client import AdsAPIClient


class TestGetStatistics:
    def test_case_16_successful_get_statistics_for_existing_ad(self, api_client, created_ad):
        item_id = created_ad["id"]
        
        response = api_client.get_statistics_by_item_id(item_id)
        
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        response_data = response.json()
        
        assert isinstance(response_data, list), "Ответ должен быть массивом"
        assert len(response_data) > 0, "Массив не должен быть пустым"
        
        stats = response_data[0]
        assert "likes" in stats, "Статистика должна содержать поле likes"
        assert "viewCount" in stats, "Статистика должна содержать поле viewCount"
        assert "contacts" in stats, "Статистика должна содержать поле contacts"
        assert isinstance(stats["likes"], int)
        assert isinstance(stats["viewCount"], int)
        assert isinstance(stats["contacts"], int)
    
    def test_case_17_get_statistics_for_nonexistent_ad(self, api_client):
        nonexistent_id = "00000000-0000-0000-0000-000000000000"
        
        response = api_client.get_statistics_by_item_id(nonexistent_id)
        
        assert response.status_code in [400, 404], f"Ожидался статус 400 или 404, получен {response.status_code}"
        response_data = response.json()
        assert "result" in response_data or "status" in response_data, \
            "Должно быть сообщение об ошибке"
    
    def test_case_18_get_statistics_with_invalid_item_id(self, api_client):
        invalid_id = "abc"
        
        response = api_client.get_statistics_by_item_id(invalid_id)
        
        assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"
        response_data = response.json()
        assert "result" in response_data or "status" in response_data, \
            "Должно быть сообщение об ошибке"

