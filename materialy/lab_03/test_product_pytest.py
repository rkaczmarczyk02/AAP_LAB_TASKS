import pytest
from product import Product

@pytest.fixture
def product():
    """Tworzy bazowy produkt do testów: Laptop za 1000 zł, 10 sztuk."""
    return Product("Laptop", 1000.0, 10)

def test_is_available(product):
    assert product.is_available() == True

def test_total_value(product):
    # Sprawdzamy czy 1000 * 10 = 10000
    assert product.total_value() == pytest.approx(10000.0)

@pytest.mark.parametrize("amount, expected_quantity", [
    (5, 15),
    (0, 10),
    (100, 110),
])
def test_add_stock_parametrized(product, amount, expected_quantity):
    product.add_stock(amount)
    assert product.quantity == expected_quantity

# --- Testy Zadania Dodatkowego ---

@pytest.mark.parametrize("percent, expected_price", [
    (0, 1000.0),    # 0% zniżki -> cena bez zmian
    (50, 500.0),    # 50% zniżki -> połowa ceny
    (100, 0.0),     # 100% zniżki -> cena zero
    (20, 800.0),    # 20% zniżki -> 800 zł
])
def test_apply_discount_valid(product, percent, expected_price):
    product.apply_discount(percent)
    assert product.price == pytest.approx(expected_price)

@pytest.mark.parametrize("invalid_percent", [-10, 101, 150])
def test_apply_discount_invalid_raises(product, invalid_percent):
    with pytest.raises(ValueError):
        product.apply_discount(invalid_percent)