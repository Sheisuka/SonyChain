from merkle import merkle_tree

import unittest


class _TestObject:
    def __init__(self, value: int):
        self.value = value
    

class TestMerkle(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("#" * 40)
        print("Запуск тестов дерева Меркла")
    
    def test_change_hash_delete(self):
        test_objects = [_TestObject(value=i) for i in range(16)]
        test_object = test_objects[0]
        tree = merkle_tree.MerkleTree(test_objects)
        hash = tree.root.hash
        tree.delete(test_object)
        self.assertNotEqual(tree.root.hash, hash, "Дерево не меняет свою размерность при удалении вершниы")
        print("Тест 5 пройден. Хэш корня меняется при удалении вершины.")

    def test_change_hash_add(self):
        test_objects = [_TestObject(value=i) for i in range(16)]
        extra_test_object = _TestObject(value=120)
        tree = merkle_tree.MerkleTree(test_objects)
        hash = tree.root.hash
        tree.add(extra_test_object)
        self.assertNotEqual(tree.root.hash, hash, "Корень не меняет свой хэш при добавлении вершины")
        print("Тест 4 пройден. Хэш корня меняется при добавлении вершины.")

    def test_delete_tree(self):
        test_objects = [_TestObject(value=i) for i in range(16)]
        tree = merkle_tree.MerkleTree(test_objects)
        for obj in test_objects:
            tree.delete(obj)
        self.assertEqual(tree.root, None, "Дерево не удалилось полностью")
        print("Тест 3 пройден. Удаление дерева полностью.")

    def test_change_size_up(self):
        test_objects = [_TestObject(value=i) for i in range(16)]
        extra_test_object = _TestObject(value=120)
        tree = merkle_tree.MerkleTree(test_objects)
        tree.add(extra_test_object)
        self.assertEqual(len(tree.elements), 32, "Дерево не меняет свою размерность при превышении своей размерности")
        print("Тест 2 пройден. Увеличение размерности дерева. 2^n листьев -> 2^(n+1).")

    def test_change_size_down(self):
        test_objects = [_TestObject(value=i) for i in range(17)]
        tree = merkle_tree.MerkleTree(test_objects)
        tree.delete(test_objects[0])
        self.assertEqual(len(tree.elements), 16, "Дерево не меняет свою размерность при изменении своей размерности")
        print("Тест 1 пройден. Уменьшение размерности дерева. 2^(n+1) листьев -> 2^n.")

    @classmethod
    def tearDownClass(cls):
        print("#" * 40, "\n")
    