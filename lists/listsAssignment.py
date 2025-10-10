# ============================================
# 1. SINGLY LINKED LIST
# ============================================

class SingleNode:
    def __init__(self, data):
        self.data = data
        self.next = None


class SinglyLinkLis:
    def __init__(self):
        self.head = None
    
    def insert(self, data):
        new_node = SingleNode(data)
        if self.head is None:
            self.head = new_node
        else:
            temp = self.head
            while temp.next:
                temp = temp.next
            temp.next = new_node
    
    def delete(self, data):
        if self.head is None:
            return
        
        if self.head.data == data:
            self.head = self.head.next
            return
        
        temp = self.head
        while temp.next:
            if temp.next.data == data:
                temp.next = temp.next.next
                return
            temp = temp.next
    
    def display(self):
        if self.head is None:
            print("List is empty")
            return
        
        temp = self.head
        while temp:
            print(temp.data, end=" -> ")
            temp = temp.next
        print("None")


# ============================================
# 2. DOUBLY LINKED LIST
# ============================================

class DoubleNode:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None


class DoublyLinkLis:
    def __init__(self):
        self.head = None
    
    def insert(self, data):
        new_node = DoubleNode(data)
        if self.head is None:
            self.head = new_node
        else:
            temp = self.head
            while temp.next:
                temp = temp.next
            temp.next = new_node
            new_node.prev = temp
    
    def delete(self, data):
        if self.head is None:
            return
        
        temp = self.head
        
        # If head needs to be deleted
        if temp.data == data:
            self.head = temp.next
            if self.head:
                self.head.prev = None
            return
        
        # Search for the node
        while temp and temp.data != data:
            temp = temp.next
        
        if temp is None:
            return
        
        if temp.next:
            temp.next.prev = temp.prev
        if temp.prev:
            temp.prev.next = temp.next
    
    def display(self):
        if self.head is None:
            print("List is empty")
            return
        
        temp = self.head
        print("Forward: ", end="")
        while temp:
            print(temp.data, end=" <-> ")
            temp = temp.next
        print("None")


# ============================================
# 3. CIRCULAR LINKED LIST
# ============================================

class CircularNode:
    def __init__(self, data):
        self.data = data
        self.next = None


class CircLinkLis:
    def __init__(self):
        self.head = None
    
    def insert(self, data):
        new_node = CircularNode(data)
        if self.head is None:
            self.head = new_node
            new_node.next = self.head
        else:
            temp = self.head
            while temp.next != self.head:
                temp = temp.next
            temp.next = new_node
            new_node.next = self.head
    
    def delete(self, data):
        if self.head is None:
            return
        
        # If head needs to be deleted
        if self.head.data == data:
            if self.head.next == self.head:
                self.head = None
                return
            
            temp = self.head
            while temp.next != self.head:
                temp = temp.next
            temp.next = self.head.next
            self.head = self.head.next
            return
        
        # Search for the node
        temp = self.head
        while temp.next != self.head and temp.next.data != data:
            temp = temp.next
        
        if temp.next.data == data:
            temp.next = temp.next.next
    
    def display(self):
        if self.head is None:
            print("List is empty")
            return
        
        temp = self.head
        print(temp.data, end=" -> ")
        temp = temp.next
        while temp != self.head:
            print(temp.data, end=" -> ")
            temp = temp.next
        print(f"(back to {self.head.data})")


# ============================================
# MAIN PROGRAM
# ============================================

print("=" * 50)
print("LINKED LISTS")
print("=" * 50)

# Demo 1: Singly Linked List
print("\n1. SINGLY LINKED LIST")
print("-" * 50)
sll = SinglyLinkLis()
sll.insert(10)
sll.insert(20)
sll.insert(30)
sll.insert(40)
print("After inserting 10, 20, 30, 40:")
sll.display()

sll.delete(20)
print("\nAfter deleting 20:")
sll.display()

# Demo 2: Doubly Linked List
print("\n2. DOUBLY LINKED LIST")
print("-" * 50)
dll = DoublyLinkLis()
dll.insert(100)
dll.insert(200)
dll.insert(300)
dll.insert(400)
print("After inserting 100, 200, 300, 400:")
dll.display()

dll.delete(200)
print("\nAfter deleting 200:")
dll.display()

# Demo 3: Circular Linked List
print("\n3. CIRCULAR LINKED LIST")
print("-" * 50)
cll = CircLinkLis()
cll.insert(5)
cll.insert(10)
cll.insert(15)
cll.insert(20)
print("After inserting 5, 10, 15, 20:")
cll.display()

cll.delete(10)
print("\nAfter deleting 10:")
cll.display()

print("\n" + "=" * 50)
print("SUMMARY")
print("=" * 50)
print("Singly Linked List: One-way connection (->)")
print("Doubly Linked List: Two-way connection (<->)")
print("Circular Linked List: Last connects to first (circular)")
print("=" * 50)