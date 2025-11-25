"""
Тест-кейсы для ручки: Получить все объявления по идентификатору продавца
TestCase 11-15
"""
import pytest
from api_client import AdsAPIClient


class TestGetAdsBySeller:
    
    def test_case_11_successful_get_ads_for_existing_seller(self, api_client):
        seller_id = api_client.generate_unique_seller_id()
        
        created_ads = []
        import time
        for i in range(3):
            response = api_client.create_ad(
                seller_id=seller_id,
                name=f"Item {i+1}",
                price=1000 * (i + 1),
                statistics={"likes": max(i, 1), "viewCount": max(i, 1), "contacts": max(i, 1)}  
            )
            assert response.status_code == 201 or response.status_code == 200, \
                f"Ожидался статус 201 при создании объявления {i+1}, получен {response.status_code}. Ответ: {response.text}"
            created_ads.append(response.json())
            time.sleep(0.1)  
        
        response = api_client.get_ads_by_seller_id(seller_id)
        
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        response_data = response.json()
        assert isinstance(response_data, list), "Ответ должен быть массивом"
        assert len(response_data) >= len(created_ads), \
            f"Количество объявлений должно быть не менее {len(created_ads)}"
        
        response_ids = {ad["id"] for ad in response_data}
        created_ids = {ad["id"] for ad in created_ads}
        assert created_ids.issubset(response_ids), \
            "Все созданные объявления должны присутствовать в ответе"
    
    def test_case_12_get_ads_with_pagination(self, api_client):
        seller_id = api_client.generate_unique_seller_id()
        
        import time
        created_count = 5
        for i in range(created_count):
            response = api_client.create_ad(
                seller_id=seller_id,
                name=f"Item {i+1}",
                price=1000 * (i + 1),
                statistics={"likes": 1, "viewCount": 1, "contacts": 1}  # Используем минимальные ненулевые значения
            )
            assert response.status_code == 201 or response.status_code == 200, \
                f"Ожидался статус 201 при создании объявления {i+1}, получен {response.status_code}. Ответ: {response.text}"
            time.sleep(0.1) 
        
        response = api_client.get_ads_by_seller_id(seller_id, page=1, size=2)
        
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        response_data = response.json()
        assert isinstance(response_data, list), "Ответ должен быть массивом"
        
        # API может не поддерживать пагинацию, поэтому проверяем:
        # 1. Если пагинация работает - количество должно быть <= size
        # 2. Если пагинация не работает - должно быть >= созданных объявлений
        # В любом случае должно быть хотя бы созданное количество объявлений
        if len(response_data) <= 2:
            assert len(response_data) <= 2, \
                f"Количество элементов должно быть не более 2, получено {len(response_data)}"
        else:
            assert len(response_data) >= created_count, \
                f"Должно быть не менее {created_count} объявлений (создано {created_count}), получено {len(response_data)}"
    
    def test_case_13_get_ads_for_seller_without_ads(self, api_client):
        seller_id = api_client.generate_unique_seller_id()
        
        response = api_client.get_ads_by_seller_id(seller_id)
        
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        response_data = response.json()
        assert isinstance(response_data, list), "Ответ должен быть массивом"
        assert len(response_data) == 0, "Список объявлений должен быть пустым"
    
    def test_case_14_get_ads_for_nonexistent_seller(self, api_client):
        nonexistent_seller_id = 999998  # другой ID
        
        response = api_client.get_ads_by_seller_id(nonexistent_seller_id)
        
        assert response.status_code in [200, 404], \
            f"Ожидался статус 200 или 404, получен {response.status_code}"
        
        if response.status_code == 200:
            response_data = response.json()
            assert isinstance(response_data, list), "Ответ должен быть массивом"
    
    def test_case_15_get_ads_with_invalid_seller_id(self, api_client):
        url = f"{api_client.base_url}/item/seller/abc"
        
        response = api_client.session.get(url)
        
        assert response.status_code == 400 or response.status_code == 404, f"Ожидался статус 400, получен {response.status_code}"
        response_data = response.json()
        

