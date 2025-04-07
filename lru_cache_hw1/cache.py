from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int=10) -> None:
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key: str) -> str:
        if key not in self.cache:
            return ''
        else:
            # Перемещаем элемент в конец, так как он был использован (первый пришел, первый ушел)
            self.cache.move_to_end(key)
            return self.cache[key]

    def set(self, key: str, value: str) -> None:
        if key in self.cache:
            # Если ключ уже такой есть в кэше, то перемещаем его назад
            self.cache.move_to_end(key)
        # Записываем в кэш значение
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            # Если кэщ переполнился, то удаляем первый элемент, так как его давно не использовали
            self.cache.popitem(last=False)

    def rem(self, key: str) -> None:
        # Удаляем элемент по ключу, если он существует
        if key in self.cache:
            del self.cache[key]