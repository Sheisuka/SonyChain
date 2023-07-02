from encoding.sha256 import sha256

from typing import List
from math import log2

class Transaction:
    ...


class MerkleNode:
    """A class that represents Merkle tree node"""
    def __init__(self, hash="", r_son=None, l_son=None) -> None:
        self.hash = hash
        self.r_son = r_son
        self.l_son = l_son


class MerkleTree:
    """A class that represents Merkle tree structure and has functions to work with it"""
    
    def __init__(self, txs: List[Transaction]) -> None:
        self.root = self.create_tree(self.complete_txs(txs))
    
    def __str__(self) -> str:
        return f"Merkle tree with {self.root.hash[0:5]}...{self.root.hash[-5:]} as root hash"
    
    def create_tree(self, txs: List[Transaction]) -> MerkleNode:
        """Recursively creates Merkle tree"""
        tx_count = len(txs)
        if tx_count == 1:
            return MerkleNode(hash=sha256(txs[0]))
        else:
            cur_node = MerkleNode()
            cur_node.l_son = self.create_tree(txs[0:tx_count // 2])
            cur_node.r_son = self.create_tree(txs[tx_count // 2:])
            cur_node.hash = sha256(cur_node.l_son.hash + cur_node.r_son.hash)
            return cur_node
    
    def complete_txs(self, txs: List[Transaction]) -> List[Transaction]:
        """Adds the last element of txs to list to make its length power of 2"""
        tx_count = len(txs)
        tx_last = txs[tx_count - 1]
        tx_log = log2(tx_count)
        tx_round = round(tx_log + 0.5)
        if tx_log != tx_round:
            for i in range(2 ** tx_round - tx_count):
                txs.append(tx_last)
        print(txs)
        return txs

    def display_tree(self, node: MerkleNode, indent=2):
        """Complactly displays the tree"""
        if node.l_son != None:
            self.display_tree(node.l_son, indent + 4)
        if node != None:
            print(f"{' ' * indent}{node.hash[0:5]}...{node.hash[-5:]}")
        if node.r_son != None:
            self.display_tree(node.r_son, indent + 4)
    