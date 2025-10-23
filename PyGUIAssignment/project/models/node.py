"""Node class for doubly linked list"""

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None