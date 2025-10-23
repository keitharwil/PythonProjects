"""Linked list data structures and operations"""
from .node import Node

class LinkedListManager:
    def __init__(self):
        self.singly_list = []
        self.doubly_head = None
        self.circular_singly_list = []
        self.circular_doubly_head = None
    
    # Singly Linked List Methods
    def singly_insert(self, value, position=None):
        """Insert into singly linked list"""
        if position is not None:
            if position < 0 or position > len(self.singly_list):
                raise ValueError(f"Position must be between 0 and {len(self.singly_list)}")
            self.singly_list.insert(position, value)
            return f"Inserted '{value}' at position {position}"
        else:
            self.singly_list.append(value)
            return f"Inserted '{value}' at end"
    
    def singly_delete(self, position=None):
        """Delete from singly linked list"""
        if not self.singly_list:
            raise ValueError("List is empty!")
        
        if position is None:
            value = self.singly_list.pop()
            return f"Deleted '{value}' from end"
        else:
            if position < 0 or position >= len(self.singly_list):
                raise ValueError(f"Position must be between 0 and {len(self.singly_list)-1}")
            value = self.singly_list.pop(position)
            return f"Deleted '{value}' from position {position}"
    
    def singly_traverse(self):
        """Traverse singly linked list"""
        if not self.singly_list:
            return []
        return [(i, value) for i, value in enumerate(self.singly_list)]
    
    def singly_clear(self):
        """Clear singly linked list"""
        self.singly_list.clear()
    
    def get_singly_list(self):
        """Get singly linked list"""
        return self.singly_list
    
    # Doubly Linked List Methods
    def doubly_insert(self, value, position=None):
        """Insert into doubly linked list"""
        new_node = Node(value)
        
        if not self.doubly_head:
            self.doubly_head = new_node
            return f"Inserted '{value}' as first node"
        
        if position is None:
            # Insert at end
            current = self.doubly_head
            while current.next:
                current = current.next
            current.next = new_node
            new_node.prev = current
            return f"Inserted '{value}' at end"
        
        if position == 0:
            new_node.next = self.doubly_head
            self.doubly_head.prev = new_node
            self.doubly_head = new_node
            return f"Inserted '{value}' at position 0"
        
        current = self.doubly_head
        for i in range(position - 1):
            if not current:
                raise ValueError("Position out of range")
            current = current.next
        
        if not current:
            raise ValueError("Position out of range")
        
        new_node.next = current.next
        new_node.prev = current
        if current.next:
            current.next.prev = new_node
        current.next = new_node
        return f"Inserted '{value}' at position {position}"
    
    def doubly_delete(self, position=None):
        """Delete from doubly linked list"""
        if not self.doubly_head:
            raise ValueError("List is empty!")
        
        if position is None:
            # Delete last node
            if not self.doubly_head.next:
                value = self.doubly_head.data
                self.doubly_head = None
                return f"Deleted '{value}' (last node)"
            
            current = self.doubly_head
            while current.next:
                current = current.next
            value = current.data
            current.prev.next = None
            return f"Deleted '{value}' from end"
        
        if position == 0:
            value = self.doubly_head.data
            self.doubly_head = self.doubly_head.next
            if self.doubly_head:
                self.doubly_head.prev = None
            return f"Deleted '{value}' from position 0"
        
        current = self.doubly_head
        for i in range(position):
            if not current:
                raise ValueError("Position out of range")
            current = current.next
        
        if not current:
            raise ValueError("Position out of range")
        
        value = current.data
        if current.prev:
            current.prev.next = current.next
        if current.next:
            current.next.prev = current.prev
        return f"Deleted '{value}' from position {position}"
    
    def doubly_traverse_forward(self):
        """Traverse doubly linked list forward"""
        if not self.doubly_head:
            return []
        
        result = []
        current = self.doubly_head
        i = 0
        while current:
            result.append((i, current.data))
            current = current.next
            i += 1
        return result
    
    def doubly_traverse_reverse(self):
        """Traverse doubly linked list in reverse"""
        if not self.doubly_head:
            return []
        
        # Go to end
        current = self.doubly_head
        while current.next:
            current = current.next
        
        result = []
        while current:
            result.append(current.data)
            current = current.prev
        return result
    
    def doubly_clear(self):
        """Clear doubly linked list"""
        self.doubly_head = None
    
    def get_doubly_list(self):
        """Get doubly linked list as array"""
        if not self.doubly_head:
            return []
        nodes = []
        current = self.doubly_head
        while current:
            nodes.append(current.data)
            current = current.next
        return nodes
    
    # Circular Singly Linked List Methods
    def circular_singly_insert(self, value, position=None):
        """Insert into circular singly linked list"""
        if position is not None:
            if position < 0 or position > len(self.circular_singly_list):
                raise ValueError(f"Position must be between 0 and {len(self.circular_singly_list)}")
            self.circular_singly_list.insert(position, value)
            return f"Inserted '{value}' at position {position} (circular)"
        else:
            self.circular_singly_list.append(value)
            return f"Inserted '{value}' at end (circular)"
    
    def circular_singly_delete(self, position=None):
        """Delete from circular singly linked list"""
        if not self.circular_singly_list:
            raise ValueError("List is empty!")
        
        if position is None:
            value = self.circular_singly_list.pop()
            return f"Deleted '{value}' from end (circular)"
        
        if position < 0 or position >= len(self.circular_singly_list):
            raise ValueError(f"Position must be between 0 and {len(self.circular_singly_list)-1}")
        value = self.circular_singly_list.pop(position)
        return f"Deleted '{value}' from position {position} (circular)"
    
    def circular_singly_traverse(self, cycles=2):
        """Traverse circular singly linked list"""
        if not self.circular_singly_list:
            return []
        
        result = []
        list_len = len(self.circular_singly_list)
        for i in range(list_len * cycles):
            idx = i % list_len
            result.append((i, self.circular_singly_list[idx], idx))
        return result
    
    def circular_singly_clear(self):
        """Clear circular singly linked list"""
        self.circular_singly_list.clear()
    
    def get_circular_singly_list(self):
        """Get circular singly linked list"""
        return self.circular_singly_list
    
    # Circular Doubly Linked List Methods
    def circular_doubly_insert(self, value, position=None):
        """Insert into circular doubly linked list"""
        new_node = Node(value)
        
        if not self.circular_doubly_head:
            self.circular_doubly_head = new_node
            new_node.next = new_node
            new_node.prev = new_node
            return f"Inserted '{value}' as first node (circular doubly)"
        
        if position is None:
            # Insert at end (before head)
            last = self.circular_doubly_head.prev
            new_node.next = self.circular_doubly_head
            new_node.prev = last
            last.next = new_node
            self.circular_doubly_head.prev = new_node
            return f"Inserted '{value}' at end (circular doubly)"
        
        if position == 0:
            last = self.circular_doubly_head.prev
            new_node.next = self.circular_doubly_head
            new_node.prev = last
            last.next = new_node
            self.circular_doubly_head.prev = new_node
            self.circular_doubly_head = new_node
            return f"Inserted '{value}' at position 0 (circular doubly)"
        
        current = self.circular_doubly_head
        for i in range(position - 1):
            current = current.next
            if current == self.circular_doubly_head:
                raise ValueError("Position out of range")
        
        new_node.next = current.next
        new_node.prev = current
        current.next.prev = new_node
        current.next = new_node
        return f"Inserted '{value}' at position {position} (circular doubly)"
    
    def circular_doubly_delete(self, position=None):
        """Delete from circular doubly linked list"""
        if not self.circular_doubly_head:
            raise ValueError("List is empty!")
        
        if position is None:
            # Delete last node (node before head)
            if self.circular_doubly_head.next == self.circular_doubly_head:
                value = self.circular_doubly_head.data
                self.circular_doubly_head = None
                return f"Deleted '{value}' (last node in circular doubly)"
            
            last = self.circular_doubly_head.prev
            value = last.data
            last.prev.next = self.circular_doubly_head
            self.circular_doubly_head.prev = last.prev
            return f"Deleted '{value}' from end (circular doubly)"
        
        if position == 0:
            value = self.circular_doubly_head.data
            if self.circular_doubly_head.next == self.circular_doubly_head:
                self.circular_doubly_head = None
            else:
                last = self.circular_doubly_head.prev
                self.circular_doubly_head = self.circular_doubly_head.next
                last.next = self.circular_doubly_head
                self.circular_doubly_head.prev = last
            return f"Deleted '{value}' from position 0 (circular doubly)"
        
        current = self.circular_doubly_head
        for i in range(position):
            current = current.next
            if current == self.circular_doubly_head and i < position:
                raise ValueError("Position out of range")
        
        value = current.data
        current.prev.next = current.next
        current.next.prev = current.prev
        return f"Deleted '{value}' from position {position} (circular doubly)"
    
    def circular_doubly_traverse_forward(self, cycles=2):
        """Traverse circular doubly linked list forward"""
        if not self.circular_doubly_head:
            return []
        
        # Count nodes
        temp = self.circular_doubly_head
        list_len = 1
        temp = temp.next
        while temp != self.circular_doubly_head:
            list_len += 1
            temp = temp.next
        
        result = []
        current = self.circular_doubly_head
        for i in range(list_len * cycles):
            result.append((i, current.data))
            current = current.next
        return result
    
    def circular_doubly_traverse_reverse(self, cycles=2):
        """Traverse circular doubly linked list in reverse"""
        if not self.circular_doubly_head:
            return []
        
        # Count nodes
        temp = self.circular_doubly_head
        list_len = 1
        temp = temp.next
        while temp != self.circular_doubly_head:
            list_len += 1
            temp = temp.next
        
        result = []
        current = self.circular_doubly_head.prev
        for i in range(list_len * cycles):
            result.append((i, current.data))
            current = current.prev
        return result
    
    def circular_doubly_clear(self):
        """Clear circular doubly linked list"""
        self.circular_doubly_head = None
    
    def get_circular_doubly_list(self):
        """Get circular doubly linked list as array"""
        if not self.circular_doubly_head:
            return []
        
        nodes = []
        current = self.circular_doubly_head
        nodes.append(current.data)
        current = current.next
        while current != self.circular_doubly_head:
            nodes.append(current.data)
            current = current.next
        return nodes