"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from homework.models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def other_product():
    return Product("pen", 50, "This is a pen", 300)


@pytest.fixture()
def cart():
    return Cart()


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        # TODO напишите проверки на метод check_quantity
        assert product.check_quantity(product.quantity - 1)

    def test_product_buy(self, product):
        # TODO напишите проверки на метод buy
        assert product.buy(product.quantity)

    def test_product_buy_more_than_available(self, product):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        with pytest.raises(ValueError):
            product.buy(product.quantity + 1)


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    def test_add_product_in_cart(self, product, cart):
        # Проверка на добавление товара в корзину, а также на количество добавленного товара в корзине
        cart.add_product(product)
        assert product in cart.products
        assert cart.products.get(product) == 1
        cart.add_product(product)
        assert cart.products.get(product) == 2

    def test_clear_full_cart_product(self, product, cart):
        # Проверка на очистку корзины при remove_count = None
        cart.add_product(product)
        assert product in cart.products
        cart.remove_product(product)
        assert product not in cart.products

    def test_remove_same_count_cart_product(self, product, cart):
        # Проверка на удаление того же числа продуктов, что и было добавлено
        cart.add_product(product, buy_count=93)
        assert product in cart.products
        cart.remove_product(product, 93)
        assert cart.products == {}

    def test_clear_cart(self, product, cart):
        # Проверка на полную очистку корзины
        cart.add_product(product, buy_count=19)
        assert cart.products.get(product) == 19
        cart.clear()
        assert cart.products == {}

    def test_buy_product_in_cart(self, product, cart):
        # Проверка на покупку quantity продуктов в корзине
        cart.add_product(product, buy_count=7)
        assert cart.products.get(product) == 7
        cart.buy(quantity=5)
        assert cart.products.get(product) == 2

    def test_buy_product_in_cart_ValueError(self, product, cart):
        # Проверка на покупку большего quantity продуктов в корзине, вызывая VallueError
        cart.add_product(product, buy_count=7)
        with pytest.raises(ValueError):
            cart.buy(quantity=9)

    def test_get_total_price(self, product, cart):
        # Проверка на получение фулл стоимости корзины
        cart.add_product(product, buy_count=15)
        assert cart.products.get(product) == 15
        assert cart.get_total_price() == 1500

    def test_cart_get_total_price_with_two_products(self, cart, product, other_product):
        # Проверка на получение фулл стоимости корзины с двумя разными товарами
        cart.add_product(product, 6)
        cart.add_product(other_product, 12)
        assert cart.get_total_price() == 1200

    def test_cart_buy_more_than_available(self, cart, product):
        # Проверка на удаление большего количетсва товаров, чем лежит в корзине
        cart.add_product(product, 10)
        cart.remove_product(product, 11)
        assert cart.products == {}
