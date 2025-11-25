import pytest
from api_client import AdsAPIClient


@pytest.fixture
def api_client():
    return AdsAPIClient()


@pytest.fixture
def test_ad_data():
    return {
        "seller_id": 123456,
        "name": "Test Item",
        "price": 9900,
        "statistics": {
            "likes": 21,
            "viewCount": 11,
            "contacts": 43
        }
    }


@pytest.fixture
def created_ad(api_client, test_ad_data):
    response = api_client.create_ad(
        seller_id=test_ad_data["seller_id"],
        name=test_ad_data["name"],
        price=test_ad_data["price"],
        statistics=test_ad_data["statistics"]
    )
    
    if response.status_code == 200:
        ad_data = response.json()
        yield ad_data
    else:
        pytest.skip(f"Не удалось создать тестовое объявление: {response.status_code}")

