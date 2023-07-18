from testing import tester # Тесты
from random import randint, choice

from merkle.merkle_tree import MerkleTree


class TestObject:
    def __init__(self, value):
        self.value = value


tester.run() # Запуск тестов
print("#" * 40)
print("Ручной тест")
print("1 - Добавить вершину")
print("2 - Удалить случайную вершину")
print("3 - Удалить всё дерево")
print("4 - Вывести дерево")
print("0 - Закончить")
objs = [TestObject(i) for i in range(1, 10)]
tree = MerkleTree(objs)
flag = 0
while flag != -1:
    flag = input("Введите команду -> ")
    if flag not in ["0", "1", "2", "3", "4"]:
        print("Введите то, что обозначено")
        continue
    else:
        flag = int(flag)
    if flag == 0:
        exit()
    elif flag == 1:
        obj = TestObject(value=randint(1, 100))
        tree.add(obj)
    elif flag == 2:
        obj = choice(tree.elements)
        tree.delete(obj)
    elif flag == 3:
        for i in range(tree.count):
            tree.delete(choice(tree.elements))
    elif flag == 4:
        tree.display()