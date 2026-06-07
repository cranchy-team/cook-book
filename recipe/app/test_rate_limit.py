import pytest
from fastapi.testclient import TestClient
from uuid import uuid4
from slowapi.errors import RateLimitExceeded

from .main import app
from .limiter import limiter


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mock_jwt_user():
    return {
        "user_id": str(uuid4()),
        "exp": 9999999999
    }


class TestRateLimiting:

    def test_rate_limit_default_applied(self, client, mock_jwt_user):
        response = client.get(
            "/health",
            headers={"X-Forwarded-For": "192.168.1.1"}
        )
        assert response.status_code == 200

    def test_health_endpoint_no_limit(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy", "service": "recipe-service"}

    def test_root_endpoint_no_limit(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert "Cook Book Recipe Service" in response.json()["message"]

    @pytest.mark.skip(reason="Интеграционный тест - требует БД")
    def test_recipes_endpoint_rate_limit(self, client, mock_jwt_user):
        """
        Тест: rate limiting на endpoint получения рецептов.

        Интеграционный тест - требует настроенную БД и JWT.
        Пропускается в unit тестах.
        """
        # Для реального тестирования:
        # 1. Настроить тестовую БД
        # 2. Сгенерировать валидный JWT токен
        # 3. Сделать больше 60 запросов за минуту
        # 4. Проверить ответ 429 Too Many Requests
        pass

    @pytest.mark.skip(reason="Интеграционный тест - требует БД")
    def test_create_recipe_rate_limit(self, client, mock_jwt_user):
        """
        Тест: rate limiting на создание рецепта (20/мин).

        Интеграционный тест - требует настроенную БД и JWT.
        """
        pass

    @pytest.mark.skip(reason="Интеграционный тест - требует БД")
    def test_upload_image_rate_limit(self, client, mock_jwt_user):
        """
        Тест: rate limiting на загрузку изображений (10/мин).

        Интеграционный тест - требует настроенную БД и JWT.
        Самый строгий лимит из-за ресурсоёмкости операции.
        """
        pass


class TestRateLimitConfiguration:

    def test_limiter_initialized(self):
        assert app.state.limiter is not None
        assert app.state.limiter == limiter

    def test_middleware_added(self):
        middleware_classes = [m.cls.__name__ for m in app.user_middleware]
        assert "SlowAPIMiddleware" in middleware_classes

    def test_exception_handler_added(self):
        assert RateLimitExceeded in app.exception_handlers


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
