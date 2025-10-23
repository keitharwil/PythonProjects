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