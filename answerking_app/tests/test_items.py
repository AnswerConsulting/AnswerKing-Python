from django.test import TestCase, Client
from answerking_app.models.models import Item

from django.db.models.query import QuerySet
from API_types import NewItemType, ItemType, ItemIDType, ErrorMessage

client = Client()



class ItemTests(TestCase):
    def setUp(self):
        self.test_item_1: Item = Item.objects.create(
            name="Burger", price=1.20, description="desc", stock=100, calories=100
        )
        self.test_item_2: Item = Item.objects.create(
            name="Coke", price=1.50, description="desc", stock=100, calories=100
        )

    def tearDown(self):
        Item.objects.all().delete()

    def test_get_all_without_items_returns_no_content(self):
        # Arrange
        Item.objects.all().delete()

        # Act
        response = client.get("/api/items")

        # Assert
        self.assertEqual(response.status_code, 204)

    def test_get_all_with_items_returns_ok(self):
        # Arrange
        expected: list[ItemType] = [
            {
                "id": self.test_item_1.id,
                "name": self.test_item_1.name,
                "price": f"{self.test_item_1.price:.2f}",
                "description": self.test_item_1.description,
                "stock": self.test_item_1.stock,
                "calories": self.test_item_1.calories,
            },
            {
                "id": self.test_item_2.id,
                "name": self.test_item_2.name,
                "price": f"{self.test_item_2.price:.2f}",
                "description": self.test_item_2.description,
                "stock": self.test_item_2.stock,
                "calories": self.test_item_2.calories,
            },
        ]

        # Act
        response = client.get("/api/items")
        actual = response.json()

        # Assert
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 200)

    def test_get_id_valid_returns_ok(self):
        # Arrange
        expected: ItemType = {
            "id": self.test_item_1.id,
            "name": self.test_item_1.name,
            "price": f"{self.test_item_1.price:.2f}",
            "description": self.test_item_1.description,
            "stock": self.test_item_1.stock,
            "calories": self.test_item_1.calories,
        }

        # Act
        response = client.get(f"/api/items/{self.test_item_1.id}")
        actual = response.json()

        # Assert
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 200)

    def test_get_id_invalid_returns_not_found(self):
        # Arrange
        expected: ErrorMessage = {
            "error": {"message": "Request failed", "details": "Object not found"}
        }

        # Act
        response = client.get("/api/items/f")
        actual = response.json()

        # Assert
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 404)

    def test_post_valid_returns_ok(self):
        # Arrange
        old_list = client.get("/api/items").json()
        post_data: NewItemType = {
            "name": "Whopper",
            "price": "1.50",
            "description": "desc",
            "stock": 100,
            "calories": 100,
        }
        expected_id: ItemIDType = {"id": self.test_item_2.id + 1}
        expected: ItemType = {**expected_id, **post_data}

        # Act
        response = client.post("/api/items", post_data, content_type="application/json")
        actual = response.json()

        created_item: Item = Item.objects.filter(name="Whopper")[0]
        updated_list: QuerySet[Item] = Item.objects.all()

        # Assert
        self.assertNotIn(actual, old_list)
        self.assertIn(created_item, updated_list)
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 200)

    def test_post_invalid_json_returns_bad_request(self):
        # Arrange
        invalid_json_data: str = '{"invalid": }'
        expected_json_error: ErrorMessage = {
            "error": {
                "message": "Failed data validation",
                "details": "Invalid JSON in body. Expecting value",
            }
        }

        # Act
        response = client.post(
            "/api/items", invalid_json_data, content_type="application/json"
        )
        actual = response.json()

        # Assert
        self.assertEqual(expected_json_error, actual)
        self.assertEqual(response.status_code, 400)

    def test_post_invalid_name_returns_bad_request(self):
        # Arrange
        invalid_post_data: NewItemType = {
            "name": "Bad data£",
            "price": "1.50",
            "description": "desc",
            "stock": 100,
            "calories": 100,
        }
        expected_failure_error: ErrorMessage = {
            "error": {
                "message": "Request failed",
                "details": "Object could not be created",
            }
        }

        # Act
        response = client.post(
            "/api/items", invalid_post_data, content_type="application/json"
        )
        actual = response.json()

        # Assert
        self.assertEqual(expected_failure_error, actual)
        self.assertEqual(response.status_code, 400)

    def test_post_invalid_price_returns_bad_request(self):
        # Arrange
        invalid_post_data: NewItemType = {
            "name": "Bad data",
            "price": "1.50f",
            "description": "desc",
            "stock": 100,
            "calories": 100,
        }
        expected_failure_error: ErrorMessage = {
            "error": {
                "message": "Request failed",
                "details": "Object could not be created",
            }
        }

        # Act
        response = client.post(
            "/api/items", invalid_post_data, content_type="application/json"
        )
        actual = response.json()

        # Assert
        self.assertEqual(expected_failure_error, actual)
        self.assertEqual(response.status_code, 400)

    def test_post_invalid_description_returns_bad_request(self):
        # Arrange
        invalid_post_data: NewItemType = {
            "name": "Bad data",
            "price": "1.50",
            "description": "desc&",
            "stock": 100,
            "calories": 100,
        }
        expected_failure_error: ErrorMessage = {
            "error": {
                "message": "Request failed",
                "details": "Object could not be created",
            }
        }

        # Act
        response = client.post(
            "/api/items", invalid_post_data, content_type="application/json"
        )
        actual = response.json()

        # Assert
        self.assertEqual(expected_failure_error, actual)
        self.assertEqual(response.status_code, 400)

    def test_post_invalid_stock_returns_bad_request(self):
        # Arrange
        invalid_post_data: NewItemType = {
            "name": "Bad data",
            "price": "1.50",
            "description": "desc",
            "stock": "f100",
            "calories": 100,
        }
        expected_failure_error: ErrorMessage = {
            "error": {
                "message": "Request failed",
                "details": "Object could not be created",
            }
        }

        # Act
        response = client.post(
            "/api/items", invalid_post_data, content_type="application/json"
        )
        actual = response.json()

        # Assert
        self.assertEqual(expected_failure_error, actual)
        self.assertEqual(response.status_code, 400)

    def test_post_negative_stock_returns_bad_request(self):
        # Arrange
        invalid_post_data: NewItemType = {
            "name": "Bad data",
            "price": "1.50",
            "description": "desc",
            "stock": -100,
            "calories": 100,
        }
        expected_failure_error: ErrorMessage = {
            "error": {
                "message": "Request failed",
                "details": "Object could not be created",
            }
        }

        # Act
        response = client.post(
            "/api/items", invalid_post_data, content_type="application/json"
        )
        actual = response.json()

        # Assert
        self.assertEqual(expected_failure_error, actual)
        self.assertEqual(response.status_code, 400)

    def test_post_invalid_calories_returns_bad_request(self):
        # Arrange
        invalid_post_data: NewItemType = {
            "name": "Bad data",
            "price": "1.50",
            "description": "desc",
            "stock": 100,
            "calories": "100f",
        }
        expected_failure_error: ErrorMessage = {
            "error": {
                "message": "Request failed",
                "details": "Object could not be created",
            }
        }

        # Act
        response = client.post(
            "/api/items", invalid_post_data, content_type="application/json"
        )
        actual = response.json()

        # Assert
        self.assertEqual(expected_failure_error, actual)
        self.assertEqual(response.status_code, 400)

    def test_post_negative_calories_returns_bad_request(self):
        # Arrange
        invalid_post_data: NewItemType = {
            "name": "Bad data",
            "price": "1.50",
            "description": "desc",
            "stock": 100,
            "calories": -100,
        }
        expected_failure_error: ErrorMessage = {
            "error": {
                "message": "Request failed",
                "details": "Object could not be created",
            }
        }

        # Act
        response = client.post(
            "/api/items", invalid_post_data, content_type="application/json"
        )
        actual = response.json()

        # Assert
        self.assertEqual(expected_failure_error, actual)
        self.assertEqual(response.status_code, 400)

    def test_put_valid_returns_ok(self):
        # Arrange
        old_item = client.get(f"/api/items/{self.test_item_1.id}").json()
        post_data: NewItemType = {
            "name": "New Burger",
            "price": "1.75",
            "description": "new desc",
            "stock": 0,
            "calories": 200,
        }
        expected_id: ItemIDType = {"id": self.test_item_1.id}
        expected: ItemType = {**expected_id, **post_data}

        # Act
        response = client.put(
            f"/api/items/{self.test_item_1.id}",
            post_data,
            content_type="application/json",
        )
        actual = response.json()

        updated_item: Item = Item.objects.filter(name="New Burger")[0]
        updated_list: QuerySet[Item] = Item.objects.all()

        # Assert
        self.assertNotEqual(old_item, actual)
        self.assertIn(updated_item, updated_list)
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 200)

    def test_put_invalid_id_returns_bad_request(self):
        # Arrange
        expected: ErrorMessage = {
            "error": {"message": "Request failed", "details": "Object not found"}
        }

        # Act
        response = client.get("/api/items/f")
        actual = response.json()

        # Assert
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 404)

    def test_put_invalid_json_returns_bad_request(self):
        # Arrange
        invalid_json_data: str = '{"invalid": }'
        expected_json_error: ErrorMessage = {
            "error": {
                "message": "Failed data validation",
                "details": "Invalid JSON in body. Expecting value",
            }
        }

        # Act
        response = client.put(
            f"/api/items/{self.test_item_1.id}",
            invalid_json_data,
            content_type="application/json",
        )
        actual = response.json()

        # Assert
        self.assertEqual(expected_json_error, actual)
        self.assertEqual(response.status_code, 400)

    def test_put_invalid_details_returns_bad_request(self):
        # Arrange
        invalid_post_data: NewItemType = {
            "name": "Bad data£",
            "price": "1.50",
            "description": "*",
            "stock": 100,
            "calories": 100,
        }
        expected_failure_error: ErrorMessage = {
            "error": {
                "message": "Request failed",
                "details": "Object could not be updated",
            }
        }

        # Act
        response = client.put(
            f"/api/items/{self.test_item_1.id}",
            invalid_post_data,
            content_type="application/json",
        )
        actual = response.json()

        # Assert
        self.assertEqual(expected_failure_error, actual)
        self.assertEqual(response.status_code, 400)

    def test_delete_valid_returns_ok(self):
        # Arrange
        item: QuerySet[Item] = Item.objects.filter(pk=self.test_item_1.id)

        # Act
        response = client.delete(f"/api/items/{self.test_item_1.id}")
        items: QuerySet[Item] = Item.objects.all()

        # Assert
        self.assertEqual(response.status_code, 204)
        self.assertNotIn(item, items)

    def test_delete_invalid_id_returns_not_found(self):
        # Arrange
        expected: ErrorMessage = {
            "error": {"message": "Request failed", "details": "Object not found"}
        }

        # Act
        response = client.delete("/api/items/f")
        actual = response.json()

        # Assert
        self.assertEqual(expected, actual)
        self.assertEqual(response.status_code, 404)