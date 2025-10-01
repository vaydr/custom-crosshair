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
        
    def parse_hex_color(self, hex_color):
        """Parse hex color to RGB values"""
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 6:
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            return r, g, b
        return 255, 0, 0  # Default red
    
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
        
        # Initialize all variables first
        size_var = tk.IntVar(value=int(self.config.get('crosshair', 'size')))
        thickness_var = tk.IntVar(value=int(self.config.get('crosshair', 'thickness')))
        r, g, b = self.parse_hex_color(self.config.get('crosshair', 'color'))
        red_var = tk.IntVar(value=r)
        green_var = tk.IntVar(value=g)
        blue_var = tk.IntVar(value=b)
        style_var = tk.StringVar(value=self.config.get('crosshair', 'style'))
        opacity_var = tk.IntVar(value=int(float(self.config.get('crosshair', 'opacity')) * 100))
        
        # Define update function
        def update_settings(*args):
            self.apply_settings(
                str(size_var.get()), 
                str(thickness_var.get()), 
                f"#{red_var.get():02x}{green_var.get():02x}{blue_var.get():02x}", 
                style_var.get(), 
                str(opacity_var.get()/100)
            )
        
        # Size setting
        ttk.Label(frame, text="Size:").grid(row=0, column=0, sticky=tk.W, pady=5)
        size_slider = ttk.Scale(frame, from_=5, to=100, variable=size_var, orient=tk.HORIZONTAL, length=200)
        size_slider.grid(row=0, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        size_entry = ttk.Entry(frame, textvariable=size_var, width=5)
        size_entry.grid(row=0, column=2, sticky=tk.W, pady=5, padx=(5, 0))
        size_var.trace_add('write', update_settings)
        
        # Thickness setting
        ttk.Label(frame, text="Thickness:").grid(row=1, column=0, sticky=tk.W, pady=5)
        thickness_slider = ttk.Scale(frame, from_=1, to=20, variable=thickness_var, orient=tk.HORIZONTAL, length=200)
        thickness_slider.grid(row=1, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        thickness_entry = ttk.Entry(frame, textvariable=thickness_var, width=5)
        thickness_entry.grid(row=1, column=2, sticky=tk.W, pady=5, padx=(5, 0))
        thickness_var.trace_add('write', update_settings)
        
        # RGB Color settings
        ttk.Label(frame, text="Red:").grid(row=2, column=0, sticky=tk.W, pady=5)
        red_slider = ttk.Scale(frame, from_=0, to=255, variable=red_var, orient=tk.HORIZONTAL, length=200)
        red_slider.grid(row=2, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        red_entry = ttk.Entry(frame, textvariable=red_var, width=5)
        red_entry.grid(row=2, column=2, sticky=tk.W, pady=5, padx=(5, 0))
        red_var.trace_add('write', update_settings)
        
        ttk.Label(frame, text="Green:").grid(row=3, column=0, sticky=tk.W, pady=5)
        green_slider = ttk.Scale(frame, from_=0, to=255, variable=green_var, orient=tk.HORIZONTAL, length=200)
        green_slider.grid(row=3, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        green_entry = ttk.Entry(frame, textvariable=green_var, width=5)
        green_entry.grid(row=3, column=2, sticky=tk.W, pady=5, padx=(5, 0))
        green_var.trace_add('write', update_settings)
        
        ttk.Label(frame, text="Blue:").grid(row=4, column=0, sticky=tk.W, pady=5)
        blue_slider = ttk.Scale(frame, from_=0, to=255, variable=blue_var, orient=tk.HORIZONTAL, length=200)
        blue_slider.grid(row=4, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        blue_entry = ttk.Entry(frame, textvariable=blue_var, width=5)
        blue_entry.grid(row=4, column=2, sticky=tk.W, pady=5, padx=(5, 0))
        blue_var.trace_add('write', update_settings)
        
        # Style setting
        ttk.Label(frame, text="Style:").grid(row=5, column=0, sticky=tk.W, pady=5)
        style_combo = ttk.Combobox(frame, textvariable=style_var, values=['cross', 'dot', 'circle'])
        style_combo.grid(row=5, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        style_var.trace_add('write', update_settings)
        
        # Opacity setting
        ttk.Label(frame, text="Opacity:").grid(row=6, column=0, sticky=tk.W, pady=5)
        opacity_slider = ttk.Scale(frame, from_=10, to=100, variable=opacity_var, orient=tk.HORIZONTAL, length=200)
        opacity_slider.grid(row=6, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        opacity_entry = ttk.Entry(frame, textvariable=opacity_var, width=5)
        opacity_entry.grid(row=6, column=2, sticky=tk.W, pady=5, padx=(5, 0))
        opacity_var.trace_add('write', update_settings)
        
        # Apply initial settings to draw crosshair
        update_settings()
        
        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=7, column=0, columnspan=3, pady=20)
        
        ttk.Button(button_frame, text="Toggle Crosshair", command=self.toggle_visibility).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Exit", command=self.quit_app).pack(side=tk.LEFT, padx=5)
        
        # Instructions
        instructions = """
Controls:
- Crosshair is ON by default when app starts
- Use sliders or type exact values
- Settings apply instantly as you adjust
- RGB sliders: 0-255 for each color
        """
        ttk.Label(frame, text=instructions, justify=tk.LEFT).grid(row=8, column=0, columnspan=3, pady=10)
        
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
