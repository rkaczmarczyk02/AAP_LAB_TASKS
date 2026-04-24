class Product:
    def __init__(self, name: str, price: float, quantity: int):
        if price < 0 or quantity < 0:
            raise ValueError("Cena i ilość muszą być nieujemne")
        self.name = name
        self.price = price
        self.quantity = quantity

    def add_stock(self, amount: int):
        if amount < 0:
            raise ValueError("Ilość musi być nieujemna")
        self.quantity += amount

    def remove_stock(self, amount: int):
        if amount < 0 or amount > self.quantity:
            raise ValueError("Nieprawidłowa ilość do usunięcia")
        self.quantity -= amount

    def is_available(self) -> bool:
        return self.quantity > 0

    def total_value(self) -> float:
        return self.price * self.quantity

    def apply_discount(self, percent: float):
        """Obniża cenę o podany procent (0-100)."""
        if not (0 <= percent <= 100):
            raise ValueError("Zniżka musi mieścić się w przedziale 0-100")
        self.price = self.price * (1 - percent / 100)