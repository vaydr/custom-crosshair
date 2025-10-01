import tkinter as tk
from tkinter import ttk, messagebox
import configparser
import os
import sys

class CrosshairOverlay:
    def __init__(self):
        self.root = None
        self.overlay_window = None
        self.is_visible = False
        self.config = configparser.ConfigParser()
        self.load_config()
        
    def load_config(self):
        """Load configuration from config.ini file"""
        self.config.read('config.ini')
        
        # Default settings
        if not self.config.has_section('crosshair'):
            self.config.add_section('crosshair')
            
        # Set defaults if not present
        defaults = {
            'size': '20',
            'thickness': '2',
            'color': '#FF0000',
            'style': 'cross',
            'opacity': '0.8',
            'hotkey_toggle': 'F1'
        }
        
        for key, value in defaults.items():
            if not self.config.has_option('crosshair', key):
                self.config.set('crosshair', key, value)
                
        self.save_config()
    
    def save_config(self):
        """Save configuration to config.ini file"""
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)
    
    def create_overlay(self):
        """Create the transparent overlay window"""
        if self.overlay_window:
            return
            
        self.overlay_window = tk.Toplevel()
        self.overlay_window.title("Crosshair Overlay")
        
        # Make window transparent and always on top
        self.overlay_window.attributes('-alpha', float(self.config.get('crosshair', 'opacity')))
        self.overlay_window.attributes('-topmost', True)
        self.overlay_window.overrideredirect(True)  # Remove window decorations
        
        # Position window in center of screen
        screen_width = self.overlay_window.winfo_screenwidth()
        screen_height = self.overlay_window.winfo_screenheight()
        window_size = 100  # Size of the overlay window
        
        x = (screen_width - window_size) // 2
        y = (screen_height - window_size) // 2
        
        self.overlay_window.geometry(f"{window_size}x{window_size}+{x}+{y}")
        
        # Create canvas for drawing crosshair
        self.canvas = tk.Canvas(
            self.overlay_window,
            width=window_size,
            height=window_size,
            bg='black',
            highlightthickness=0
        )
        self.canvas.pack()
        
        # Make canvas transparent
        self.overlay_window.attributes('-transparentcolor', 'black')
        
        self.draw_crosshair()
    
    def draw_crosshair(self):
        """Draw the crosshair on the canvas"""
        if not self.overlay_window:
            return
            
        self.canvas.delete("all")
        
        size = int(self.config.get('crosshair', 'size'))
        thickness = int(self.config.get('crosshair', 'thickness'))
        color = self.config.get('crosshair', 'color')
        style = self.config.get('crosshair', 'style')
        
        center_x = 50  # Center of 100x100 window
        center_y = 50
        
        if style == 'cross':
            # Draw cross
            self.canvas.create_line(
                center_x - size//2, center_y, center_x + size//2, center_y,
                fill=color, width=thickness
            )
            self.canvas.create_line(
                center_x, center_y - size//2, center_x, center_y + size//2,
                fill=color, width=thickness
            )
        elif style == 'dot':
            # Draw dot
            self.canvas.create_oval(
                center_x - size//4, center_y - size//4,
                center_x + size//4, center_y + size//4,
                fill=color, outline=color
            )
        elif style == 'circle':
            # Draw circle
            self.canvas.create_oval(
                center_x - size//2, center_y - size//2,
                center_x + size//2, center_y + size//2,
                fill='', outline=color, width=thickness
            )
    
    def toggle_visibility(self):
        """Toggle crosshair visibility"""
        if not self.overlay_window:
            self.create_overlay()
        
        self.is_visible = not self.is_visible
        
        if self.is_visible:
            self.overlay_window.deiconify()
            self.overlay_window.lift()
        else:
            self.overlay_window.withdraw()
    
    def show_settings(self):
        """Show settings window"""
        if self.root:
            return
            
        self.root = tk.Tk()
        self.root.title("Crosshair Settings")
        self.root.geometry("400x300")
        
        # Create and show crosshair by default
        self.create_overlay()
        self.is_visible = True
        
        # Create settings frame
        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Size setting
        ttk.Label(frame, text="Size:").grid(row=0, column=0, sticky=tk.W, pady=5)
        size_var = tk.StringVar(value=self.config.get('crosshair', 'size'))
        size_entry = ttk.Entry(frame, textvariable=size_var, width=10)
        size_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
        size_var.trace('w', lambda *args: self.apply_settings(size_var.get(), thickness_var.get(), color_var.get(), style_var.get(), opacity_var.get()))
        
        # Thickness setting
        ttk.Label(frame, text="Thickness:").grid(row=1, column=0, sticky=tk.W, pady=5)
        thickness_var = tk.StringVar(value=self.config.get('crosshair', 'thickness'))
        thickness_entry = ttk.Entry(frame, textvariable=thickness_var, width=10)
        thickness_entry.grid(row=1, column=1, sticky=tk.W, pady=5)
        thickness_var.trace('w', lambda *args: self.apply_settings(size_var.get(), thickness_var.get(), color_var.get(), style_var.get(), opacity_var.get()))
        
        # Color setting
        ttk.Label(frame, text="Color (hex):").grid(row=2, column=0, sticky=tk.W, pady=5)
        color_var = tk.StringVar(value=self.config.get('crosshair', 'color'))
        color_entry = ttk.Entry(frame, textvariable=color_var, width=10)
        color_entry.grid(row=2, column=1, sticky=tk.W, pady=5)
        color_var.trace('w', lambda *args: self.apply_settings(size_var.get(), thickness_var.get(), color_var.get(), style_var.get(), opacity_var.get()))
        
        # Style setting
        ttk.Label(frame, text="Style:").grid(row=3, column=0, sticky=tk.W, pady=5)
        style_var = tk.StringVar(value=self.config.get('crosshair', 'style'))
        style_combo = ttk.Combobox(frame, textvariable=style_var, values=['cross', 'dot', 'circle'])
        style_combo.grid(row=3, column=1, sticky=tk.W, pady=5)
        style_var.trace('w', lambda *args: self.apply_settings(size_var.get(), thickness_var.get(), color_var.get(), style_var.get(), opacity_var.get()))
        
        # Opacity setting
        ttk.Label(frame, text="Opacity (0.1-1.0):").grid(row=4, column=0, sticky=tk.W, pady=5)
        opacity_var = tk.StringVar(value=self.config.get('crosshair', 'opacity'))
        opacity_entry = ttk.Entry(frame, textvariable=opacity_var, width=10)
        opacity_entry.grid(row=4, column=1, sticky=tk.W, pady=5)
        opacity_var.trace('w', lambda *args: self.apply_settings(size_var.get(), thickness_var.get(), color_var.get(), style_var.get(), opacity_var.get()))
        
        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Toggle Crosshair", command=self.toggle_visibility).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Exit", command=self.quit_app).pack(side=tk.LEFT, padx=5)
        
        # Instructions
        instructions = """
Controls:
- Crosshair is ON by default when app starts
- Settings apply instantly as you type
- Click 'Toggle Crosshair' to show/hide
        """
        ttk.Label(frame, text=instructions, justify=tk.LEFT).grid(row=6, column=0, columnspan=2, pady=10)
        
        self.root.protocol("WM_DELETE_WINDOW", self.quit_app)
        self.root.mainloop()
    
    def apply_settings(self, size, thickness, color, style, opacity):
        """Apply new settings"""
        try:
            self.config.set('crosshair', 'size', size)
            self.config.set('crosshair', 'thickness', thickness)
            self.config.set('crosshair', 'color', color)
            self.config.set('crosshair', 'style', style)
            self.config.set('crosshair', 'opacity', opacity)
            
            self.save_config()
            
            if self.overlay_window:
                self.overlay_window.attributes('-alpha', float(opacity))
                self.draw_crosshair()
                
        except Exception as e:
            # Silently handle errors - just don't apply invalid settings
            pass
    
    def quit_app(self):
        """Quit the application"""
        if self.overlay_window:
            self.overlay_window.destroy()
        if self.root:
            self.root.destroy()
        sys.exit()

def main():
    """Main function"""
    app = CrosshairOverlay()
    
    # Create settings window
    app.show_settings()

if __name__ == "__main__":
    main()
