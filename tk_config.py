from tkinter import ttk

def style(window):
        """
        Customizes widgets and frames. 

        More on: https://www.tcl-lang.org/man/tcl8.7/TkCmd/index.html
        """
        
        style = ttk.Style()
        
        style.theme_use("alt")

        bg = "#000000"     # near-black
        fg = "#39FF14"     # neon green
        

        style.configure("Treeview.Heading", 
                        font=("Flexi IBM VGA True", 20, "bold"),
                        foreground=fg,
                        background=bg) 
        style.configure("Treeview", 
                        font=("Flexi IBM VGA True", 17), 
                        background=bg, 
                        foreground=fg, 
                        fieldbackground="#1F731FC6")
        style.configure("TCombobox",
                        fieldbackground=fg,
                        background=bg,   
                        foreground=bg,) 
        style.configure("TEntry",
                        fieldbackground=fg,   
                        foreground=bg)   
        
        style.configure("TLabel.Frame",
                        fieldbackground=fg,   
                        foreground=bg,
                        background=bg)   
        