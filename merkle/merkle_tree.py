from encoding.sha256 import sha256
from merkle.utils import round_to_2_power, padd_to_2_power, is_sha256

from typing import List
from math import floor


class MerkleNode:
    """Класс, представляющий собой вершину дерева Меркла"""
    def __init__(self, hash: str = "", r_son: "MerkleNode" = None, l_son: "MerkleNode" = None) -> None:
        self.hash = hash
        self.r_son = r_son
        self.l_son = l_son
    
    
    def __eq__(self, other: object) -> bool: # Реализация сравнения с другим объектом MerkleNode
        if not (other is None):
            return self.hash == other.hash
        return super().__eq__(other)

    def __str__(self) -> str: # Реализация неподробного отображения объекта
        return f"{self.hash[0:5]}...{self.hash[-5:]}"

    def __repr__(self) -> str: # Реализация подробного отображения объекта
        return f"{self.hash[0:10]}...{self.hash[-10:]}"


class MerkleTree:    
    """Класс, представляющий собой дерево Меркла в целом"""
    def __init__(self, elements: list, sort_attr: str = "") -> None:
        if sort_attr: # Опциональный аттрибут, по которому ведется сортировка в возр. порядке
            self.sort_attr: str = sort_attr
            elements = sorted(elements, key=lambda x: getattr(x, sort_attr)) # Сортируем по аттрибуту
        self.elements = padd_to_2_power(elements) # Дополняем элементы фиктивными
        self.count: int = len(elements) # Количество объектов
        self.fictive_count: int = round_to_2_power(self.count) # Количество объектов + фиктивные объекты
        self.root: MerkleNode = self.create(self.elements)

    def create(self, elements: list) -> MerkleNode:
        """Рекурсивно создаёт дерево Меркла, предварительно дополнив количество элементов до степени 2"""
        def _create(elements: list) -> MerkleNode:
            elements_count = len(elements)
            if elements_count == 1: 
                return MerkleNode(hash=sha256(elements[0])) 
            else:
                cur_node = MerkleNode()
                cur_node.l_son = _create(elements[0:elements_count // 2])
                cur_node.r_son = _create(elements[elements_count // 2:])
                cur_node.hash = sha256(cur_node.l_son.hash + cur_node.r_son.hash) # Значение внутренней вершины определяется как хэш от рез-та конкатенации хэшей его детей
                return cur_node

        if len(elements) != 0:
            return _create(elements)
        else:
            self.root = None


    def display(self) -> None:
        """Выводит дерево на боку"""
        def _display(node: MerkleNode, indent: int = 2):
            if node.l_son != None:
                _display(node.l_son, indent + 8)
            print(f"{' ' * indent}{node.hash[0:5]}...{node.hash[-5:]}")
            if node.r_son != None:
                _display(node.r_son, indent + 8)
        print(list(map(lambda x: x.value, self.elements)))
        if self.root is None:
            print("Дерево пусто")
        else:
            _display(self.root)
        print("#" * 60)
    
    def add(self, element) -> None:
        """Добавляет element в дерево. Если включена сортировка, то работает с её учетом. После добавления обновляет хэш соответствующего поддерева"""
        position = self.count
        if hasattr(self, "sort_attr"): # Если задан параметр сортировки, то находим подходящее место для вставки
            try:
                position = 0
                for i in range(self.count): # Поиск позиции для вставки с учетом порядка
                    if getattr(element, self.sort_attr) < getattr(self.elements[i], self.sort_attr):
                        break
                    else:
                        position += 1
            except AttributeError:
                print("Добавляемый элемент не имеет указанного аттрибута. Добавление не удалось")
                return
        
        self.count += 1
        if self.count > self.fictive_count: # Количество элементов вышло за "текущую" степень двойки
            self.elements.append(element)
            if position != self.count - 1:
                for i in range(self.count - 1, position, -1): # Транспозициями перемещаем новый элемент на его место 
                    self.elements[i], self.elements[i - 1] = self.elements[i - 1], self.elements[i]
            self.fictive_count = round_to_2_power(self.count)
            self.elements = padd_to_2_power(self.elements)
        else:
            self.elements[self.count - 1] = element
            if position == self.count - 1:
                for i in range(self.count, self.fictive_count): # Фиктивные элементы должны быть копиями последнего элемента
                    self.elements[i] = element
            else:
                for i in range(self.count - 1, position, -1): # Транспозициями перемещаем новый элемент на его место 
                    self.elements[i], self.elements[i - 1] = self.elements[i - 1], self.elements[i]
        
        self._update_root_add(position)
    
    def _update_root_add(self, position: int) -> None:
        if position <= self.fictive_count // 2:
            self.root.l_son = self.create(self.elements[0:self.fictive_count//2])
            self.root.hash = sha256(self.root.l_son.hash + self.root.r_son.hash)
        else:
            self.root.r_son = self.create(self.elements[self.fictive_count//2:])
            self.root.hash = sha256(self.root.l_son.hash + self.root.r_son.hash)
    
    def _update_root_delete(self, position: int) -> None:
        if self.count == floor(self.fictive_count / 2):
            self.elements = self.elements[:self.count]
            self.fictive_count = self.count
            self.root = self.create(self.elements)
        elif position == (self.fictive_count // 2) - 1:
            self.root = self.create(self.elements)
        else:
            if position <= self.fictive_count // 2 - 1: # Обновляем хэш левого поддерева
                self.root.l_son = self.create(self.elements[0:self.fictive_count//2])
            else: # Обновляем хэш правого поддерева
                self.root.r_son = self.create(self.elements[self.fictive_count//2:])
            self.root.hash = sha256(self.root.hash)

    def _dfs(self, needed) -> tuple:
        """Возвращает путь из вершин до искомого значения(хэша/объекта-нелитерала)"""
        def _dfs_hash(node: MerkleNode, visited: list, needed_hash: str) -> tuple:
            current_path = visited.copy()
            current_path.append(node)

            if node.hash == needed_hash:
                return (True, current_path)
            
            if (node.r_son != None) and not (node.r_son in current_path):
                result = _dfs_hash(node.r_son, current_path, needed_hash)
                if result[0]:
                    return result
            if (node.l_son != None) and not (node.l_son in current_path):
                result = _dfs_hash(node.l_son, current_path, needed_hash)
                if result[0]:
                    return result
            return False,
    
        if sha256(needed):
            dfs_res = _dfs_hash(self.root, [], needed)
        else:
            dfs_res = _dfs_hash(self.root, [], sha256(needed))

        return dfs_res

    def delete(self, element) -> None:
        """Каскадно удаляет element если это хэш или объект-нелитерал"""
        def _delete_hash(element_hash) -> None:
            dfs_res = self._dfs(element_hash)
            if dfs_res[0] == True:
                path = dfs_res[1]
                if len(path) >= 2:
                    element_parent = dfs_res[-2]
                    if element_parent.r_son == element_hash:
                        element_parent.r_son = None
                    elif element_parent.l_son == element_hash:
                        element_parent.l_son = None
                else:
                    element = None
            else:
                print("Такого хэша нет в дереве")
        
        def _delete_element(element) -> None:
            position = self.elements.index(element)
            if position != self.count - 1:
                self.elements.pop(position)
                self.elements.append(self.elements[-1])
            else:
                new_last = self.elements[position - 1]
                for i in range(position, self.fictive_count):
                    self.elements[i] = new_last
            self.count -= 1
            if self.count == 0:
                self.root = None
            self._update_root_delete(position)

        if is_sha256(element):
            _delete_hash(element)
        else:
            _delete_element(element)

    def verify(self, element) -> None:
        """Выполняет проверку того, что хэш входит корректно в дерево"""
        def _get_brothers(path: List[MerkleNode]) -> List[MerkleNode]:
            """Получает на вход путь от корня до элемента и ищет брата каждого узла, если брата нет, то отдает копию элемента"""
            brothers = []
            for i in range(1, len(path)):
                if (path[i - 1].r_son == path[i]) and not (path[i - 1].l_son is None):
                    brothers.append(("l", path[i - 1].l_son)) # Указываем положение брата относительно родителя, чтобы корректно конкатенировать хэши
                else:
                    brothers.append(("r", path[i - 1].r_son))
            return brothers
        
        def _hash_brothers(element: object, brothers) -> str:
            hash = element
            for i in range(len(brothers) - 1, -1, -1): # Проходимся по братьям снизу вверх, строя новый хэш корня
                brother_side, brother = brothers[i][0], brothers[i][1]
                if brother_side == "l":
                    hash = sha256(brother.hash + hash)
                else:
                    hash = sha256(hash + brother.hash)
            return hash
        
        dfs_res = self._dfs(element)
        if dfs_res[0]:
            path = dfs_res[1]
            brothers = _get_brothers(path)

            if is_sha256(element):
                element_hash = element
            else:
                element_hash = sha256(element)

            new_root_hash = _hash_brothers(element_hash, brothers)
            verify_res = new_root_hash == self.root.hash
            print("Элемент входит корректно") if verify_res else print("Элемент входит некорректно")
        else:
            print("Такой элемент вовсе не входит в дерево")

    