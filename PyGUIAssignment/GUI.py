import tkinter as tk

COLORS = {
    'base': '#1e1e2e',
    'mantle': '#181825',
    'crust': '#11111b',
    'text': '#cdd6f4',
    'subtext': '#bac2de',
    'surface0': '#313244',
    'surface1': '#45475a',
    'surface2': '#585b70',
    'overlay0': '#6c7086',
    'blue': '#89b4fa',
    'lavender': '#b4befe',
    'sapphire': '#74c7ec',
    'sky': '#89dceb',
    'teal': '#94e2d5',
    'green': '#a6e3a1',
    'yellow': '#f9e2af',
    'peach': '#fab387',
    'maroon': '#eba0ac',
    'red': '#f38ba8',
    'mauve': '#cba6f7',
    'pink': '#f5c2e7',
    'flamingo': '#f2cdcd',
    'rosewater': '#f5e0dc'
}

class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OOP Tkinter")
        self.root.geometry("900x900")
        self.root.configure(bg=COLORS['base'])

        self.icon = tk.PhotoImage(file="PyGUIAssignment/logo.png")
        self.root.iconphoto(False, self.icon)


# Run the app
root = tk.Tk()
app = MyApp(root)
root.mainloop()
