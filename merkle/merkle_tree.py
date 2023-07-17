from encoding.sha256 import sha256
from merkle.utils import round_to_2_power, padd_to_2_power

from re import match


class MerkleNode:
    def __init__(self, hash="", r_son=None, l_son=None) -> None:
        self.hash = hash
        self.r_son = r_son
        self.l_son = l_son
    
    
    def __eq__(self, other: object) -> bool: # Реализация сравнения с другим объектом MerkleNode
        if other != None:
            return self.hash == other.hash
        return super().__eq__(other)

    def __repr__(self) -> str:
        return f"{self.hash[0:5]}...{self.hash[-5:]}"


class MerkleTree:    
    def __init__(self, elements: list, sort_attr: str = "") -> None:
        if sort_attr != "": # Опциональный аттрибут, по которому ведется сортировка в возр. порядке
            self.sort_attr: str = sort_attr
            elements = sorted(elements, key=lambda x: getattr(x, sort_attr))
        self.elements = padd_to_2_power(elements)
        self.count: int = len(elements) # Количество объектов
        self.fictive_count: int = round_to_2_power(self.count) # Количество объектов + фиктивные объекты
        self.root: MerkleNode = self.create(self.elements)

    def create(self, elements) -> MerkleNode:
        """Рекурсивно создаёт дерево Меркла, предварительно дополнив количество элементов до степени 2"""
        elements_count = len(elements)
        if elements_count == 1: 
            return MerkleNode(hash=sha256(elements[0])) 
        else:
            cur_node = MerkleNode()
            cur_node.l_son = self.create(elements[0:elements_count // 2])
            cur_node.r_son = self.create(elements[elements_count // 2:])
            cur_node.hash = sha256(cur_node.l_son.hash + cur_node.r_son.hash)
            return cur_node

    def display(self):
        """Выводит дерево на боку"""
        def _display(node: MerkleNode, indent: int = 2):
            if node.l_son != None:
                _display(node.l_son, indent + 8)
            if node != None:
                print(f"{' ' * indent}{node.hash[0:5]}...{node.hash[-5:]}")
            if node.r_son != None:
                _display(node.r_son, indent + 8)
        print(list(map(lambda x: x.value, self.elements)))
        _display(self.root)
        print("#" * 60)
    
    def add(self, element):
        """Добавляет element в дерево. Если включена сортировка, то работает с её учетом. После добавления обновляет хэш соответствующего поддерева"""
        position = self.count
        if hasattr(self, "sort_attr"): # Если задан параметр сортировки, то находим подходящее место для вставки
            try:
                position = 0
                for i in range(self.count):
                    if getattr(element, self.sort_attr) < getattr(self.elements[i], self.sort_attr):
                        break
                    else:
                        position += 1
            except AttributeError:
                print("Добавляемый элемент не имеет указанного аттрибута. Добавление не удалось")
                return
        
        self.count += 1
        if self.count > self.fictive_count:
            self.elements.append(element)
            if position != self.count - 1:
                for i in range(self.count - 1, position, -1):
                    self.elements[i], self.elements[i - 1] = self.elements[i - 1], self.elements[i]
            self.fictive_count = round_to_2_power(self.count)
        else:
            self.elements[self.count - 1] = element
            if position == self.count - 1:
                for i in range(self.count, self.fictive_count):
                    self.elements[i] = element
            else:
                for i in range(self.count - 1, position, -1):
                    self.elements[i], self.elements[i - 1] = self.elements[i - 1], self.elements[i]
        
        if position <= self.fictive_count // 2:
            self.root.l_son = self.create(self.elements[0:self.fictive_count//2])
            self.root.hash = sha256(self.root.l_son.hash + self.root.r_son.hash)
        else:
            self.root.r_son = self.create(self.elements[self.fictive_count//2:])
            self.root.hash = sha256(self.root.l_son.hash + self.root.r_son.hash)

    def _dfs(self, needed):
        """Возвращает путь из вершин до искомого значения(хэша/объекта-нелитерала), либо None, если его нет в дереве"""
        def _dfs_hash(node: MerkleNode, visited: list, needed_hash: str):
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

        dfs_res = _dfs_hash(self.root, [], needed)
        return dfs_res

    def delete(self, element):
        """Каскадно удаляет element если это хэш или объект-нелитерал"""
        if isinstance(element, str):
            if match(r"^[0-9a-fA-F]{64}$", element): # Является ли переданная строка хэшем
                element_hash = element_hash
            else:
                element_hash = sha256(element)
        else:
            element_hash = sha256(element)

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
            print("Такого элемента нет в дереве")

    def verify():
        ...
    