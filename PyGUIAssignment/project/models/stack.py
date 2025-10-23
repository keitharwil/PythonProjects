"""Stack implementation"""

class StackManager:
    def __init__(self):
        self.linked_list_stack = []
    
    def push(self, value):
        """Push value onto stack"""
        self.linked_list_stack.append(value)
        return f"Pushed node with value: {value}"
    
    def pop(self):
        """Pop value from stack"""
        if not self.linked_list_stack:
            raise ValueError("Stack is empty!")
        value = self.linked_list_stack.pop()
        return f"Popped value: {value}"
    
    def peek(self):
        """Peek at top of stack"""
        if not self.linked_list_stack:
            return None
        return self.linked_list_stack[-1]
    
    def is_empty(self):
        """Check if stack is empty"""
        return len(self.linked_list_stack) == 0
    
    def clear(self):
        """Clear the stack"""
        self.linked_list_stack.clear()
    
    def get_stack(self):
        """Get the stack as list"""
        return self.linked_list_stack
    
    def search(self, value):
        """
        Search for a value in the stack
        Returns the position from top (0-indexed) if found, else -1
        """
        for i in range(len(self.linked_list_stack) - 1, -1, -1):  # Search from top to bottom
            if self.linked_list_stack[i] == value:
                return len(self.linked_list_stack) - 1 - i  # Position from top (0-indexed)
        return -1  # Value not found
    
    def size(self):
        """Return the size of the stack"""
        return len(self.linked_list_stack)