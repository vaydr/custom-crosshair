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
            # Inner lines
            'inner_enabled': 'True',
            'inner_length': '15',
            'inner_thickness': '2',
            'inner_offset': '3',
            'inner_color': '#FF0000',
            'inner_outline_enabled': 'True',
            'inner_outline_thickness': '1',
            'inner_outline_color': '#000000',
            
            # Outer lines
            'outer_enabled': 'True',
            'outer_length': '25',
            'outer_thickness': '2',
            'outer_offset': '8',
            'outer_color': '#FF0000',
            'outer_outline_enabled': 'True',
            'outer_outline_thickness': '1',
            'outer_outline_color': '#000000',
            
            # Center dot
            'center_dot_enabled': 'False',
            'center_dot_size': '3',
            'center_dot_color': '#FF0000',
            'center_dot_outline_enabled': 'True',
            'center_dot_outline_thickness': '1',
            'center_dot_outline_color': '#000000',
            
            # General
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
        """Draw the advanced crosshair on the canvas"""
        if not self.overlay_window:
            return
            
        self.canvas.delete("all")
        
        center_x = 50  # Center of 100x100 window
        center_y = 50
        
        # Draw outer lines first (so they appear behind inner lines)
        if self.config.getboolean('crosshair', 'outer_enabled'):
            outer_length = int(self.config.get('crosshair', 'outer_length'))
            outer_thickness = int(self.config.get('crosshair', 'outer_thickness'))
            outer_offset = int(self.config.get('crosshair', 'outer_offset'))
            outer_color = self.config.get('crosshair', 'outer_color')
            
            # Outer line positions (start from offset distance from center)
            outer_start = outer_offset
            outer_end = outer_offset + outer_length
            
            # Draw outer outlines first if enabled
            if self.config.getboolean('crosshair', 'outer_outline_enabled'):
                outline_thickness = int(self.config.get('crosshair', 'outer_outline_thickness'))
                outline_color = self.config.get('crosshair', 'outer_outline_color')
                total_thickness = outer_thickness + (outline_thickness * 2)
                
                # Horizontal outer outlines
                self.canvas.create_line(center_x + outer_start, center_y, center_x + outer_end, center_y, fill=outline_color, width=total_thickness)
                self.canvas.create_line(center_x - outer_start, center_y, center_x - outer_end, center_y, fill=outline_color, width=total_thickness)
                # Vertical outer outlines
                self.canvas.create_line(center_x, center_y + outer_start, center_x, center_y + outer_end, fill=outline_color, width=total_thickness)
                self.canvas.create_line(center_x, center_y - outer_start, center_x, center_y - outer_end, fill=outline_color, width=total_thickness)
            
            # Draw outer lines
            # Horizontal outer lines
            self.canvas.create_line(center_x + outer_start, center_y, center_x + outer_end, center_y, fill=outer_color, width=outer_thickness)
            self.canvas.create_line(center_x - outer_start, center_y, center_x - outer_end, center_y, fill=outer_color, width=outer_thickness)
            # Vertical outer lines
            self.canvas.create_line(center_x, center_y + outer_start, center_x, center_y + outer_end, fill=outer_color, width=outer_thickness)
            self.canvas.create_line(center_x, center_y - outer_start, center_x, center_y - outer_end, fill=outer_color, width=outer_thickness)
        
        # Draw inner lines
        if self.config.getboolean('crosshair', 'inner_enabled'):
            inner_length = int(self.config.get('crosshair', 'inner_length'))
            inner_thickness = int(self.config.get('crosshair', 'inner_thickness'))
            inner_offset = int(self.config.get('crosshair', 'inner_offset'))
            inner_color = self.config.get('crosshair', 'inner_color')
            
            # Inner line positions (start from offset distance from center)
            inner_start = inner_offset
            inner_end = inner_offset + inner_length
            
            # Draw inner outlines first if enabled
            if self.config.getboolean('crosshair', 'inner_outline_enabled'):
                outline_thickness = int(self.config.get('crosshair', 'inner_outline_thickness'))
                outline_color = self.config.get('crosshair', 'inner_outline_color')
                total_thickness = inner_thickness + (outline_thickness * 2)
                
                # Horizontal inner outlines
                self.canvas.create_line(center_x + inner_start, center_y, center_x + inner_end, center_y, fill=outline_color, width=total_thickness)
                self.canvas.create_line(center_x - inner_start, center_y, center_x - inner_end, center_y, fill=outline_color, width=total_thickness)
                # Vertical inner outlines
                self.canvas.create_line(center_x, center_y + inner_start, center_x, center_y + inner_end, fill=outline_color, width=total_thickness)
                self.canvas.create_line(center_x, center_y - inner_start, center_x, center_y - inner_end, fill=outline_color, width=total_thickness)
            
            # Draw inner lines
            # Horizontal inner lines
            self.canvas.create_line(center_x + inner_start, center_y, center_x + inner_end, center_y, fill=inner_color, width=inner_thickness)
            self.canvas.create_line(center_x - inner_start, center_y, center_x - inner_end, center_y, fill=inner_color, width=inner_thickness)
            # Vertical inner lines
            self.canvas.create_line(center_x, center_y + inner_start, center_x, center_y + inner_end, fill=inner_color, width=inner_thickness)
            self.canvas.create_line(center_x, center_y - inner_start, center_x, center_y - inner_end, fill=inner_color, width=inner_thickness)
        
        # Draw center dot last (so it appears on top)
        if self.config.getboolean('crosshair', 'center_dot_enabled'):
            dot_size = int(self.config.get('crosshair', 'center_dot_size'))
            dot_color = self.config.get('crosshair', 'center_dot_color')
            
            # Draw center dot outline first if enabled
            if self.config.getboolean('crosshair', 'center_dot_outline_enabled'):
                outline_thickness = int(self.config.get('crosshair', 'center_dot_outline_thickness'))
                outline_color = self.config.get('crosshair', 'center_dot_outline_color')
                total_size = dot_size + outline_thickness
                
                self.canvas.create_oval(
                    center_x - total_size, center_y - total_size,
                    center_x + total_size, center_y + total_size,
                    fill=outline_color, outline=outline_color
                )
            
            # Draw center dot
            self.canvas.create_oval(
                center_x - dot_size, center_y - dot_size,
                center_x + dot_size, center_y + dot_size,
                fill=dot_color, outline=dot_color
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
        self.root.title("Advanced Crosshair Settings")
        self.root.geometry("600x800")
        
        # Create and show crosshair by default
        self.create_overlay()
        self.is_visible = True
        
        # Create scrollable frame
        canvas = tk.Canvas(self.root)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        frame = ttk.Frame(scrollable_frame, padding="10")
        frame.pack(fill="both", expand=True)
        
        # Initialize all variables
        self.vars = {}
        
        # Define update function
        def update_settings(*args):
            # Update all config values from variables
            for key, var in self.vars.items():
                if isinstance(var, tk.BooleanVar):
                    self.config.set('crosshair', key, str(var.get()))
                elif key.endswith('_color'):
                    # Handle RGB color variables
                    if key.endswith('_color'):
                        base_key = key[:-6]  # Remove '_color'
                        if f"{base_key}_red" in self.vars:
                            r = self.vars[f"{base_key}_red"].get()
                            g = self.vars[f"{base_key}_green"].get()
                            b = self.vars[f"{base_key}_blue"].get()
                            self.config.set('crosshair', key, f"#{r:02x}{g:02x}{b:02x}")
                else:
                    self.config.set('crosshair', key, str(var.get()))
            
            self.save_config()
            if self.overlay_window:
                self.overlay_window.attributes('-alpha', float(self.config.get('crosshair', 'opacity')))
                self.draw_crosshair()
        
        row = 0
        
        # Inner Lines Section
        ttk.Label(frame, text="INNER LINES", font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=(10, 5))
        row += 1
        
        # Inner enabled
        self.vars['inner_enabled'] = tk.BooleanVar(value=self.config.getboolean('crosshair', 'inner_enabled'))
        ttk.Checkbutton(frame, text="Enable Inner Lines", variable=self.vars['inner_enabled']).grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=2)
        self.vars['inner_enabled'].trace_add('write', update_settings)
        row += 1
        
        # Inner length
        ttk.Label(frame, text="Length:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.vars['inner_length'] = tk.IntVar(value=int(self.config.get('crosshair', 'inner_length')))
        ttk.Scale(frame, from_=1, to=50, variable=self.vars['inner_length'], orient=tk.HORIZONTAL, length=200).grid(row=row, column=1, sticky=tk.W, padx=(10, 0))
        ttk.Entry(frame, textvariable=self.vars['inner_length'], width=5).grid(row=row, column=2, sticky=tk.W, padx=(5, 0))
        self.vars['inner_length'].trace_add('write', update_settings)
        row += 1
        
        # Inner thickness
        ttk.Label(frame, text="Thickness:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.vars['inner_thickness'] = tk.IntVar(value=int(self.config.get('crosshair', 'inner_thickness')))
        ttk.Scale(frame, from_=1, to=10, variable=self.vars['inner_thickness'], orient=tk.HORIZONTAL, length=200).grid(row=row, column=1, sticky=tk.W, padx=(10, 0))
        ttk.Entry(frame, textvariable=self.vars['inner_thickness'], width=5).grid(row=row, column=2, sticky=tk.W, padx=(5, 0))
        self.vars['inner_thickness'].trace_add('write', update_settings)
        row += 1
        
        # Inner offset
        ttk.Label(frame, text="Offset:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.vars['inner_offset'] = tk.IntVar(value=int(self.config.get('crosshair', 'inner_offset')))
        ttk.Scale(frame, from_=0, to=20, variable=self.vars['inner_offset'], orient=tk.HORIZONTAL, length=200).grid(row=row, column=1, sticky=tk.W, padx=(10, 0))
        ttk.Entry(frame, textvariable=self.vars['inner_offset'], width=5).grid(row=row, column=2, sticky=tk.W, padx=(5, 0))
        self.vars['inner_offset'].trace_add('write', update_settings)
        row += 1
        
        # Inner color RGB
        r, g, b = self.parse_hex_color(self.config.get('crosshair', 'inner_color'))
        self.vars['inner_red'] = tk.IntVar(value=r)
        self.vars['inner_green'] = tk.IntVar(value=g)
        self.vars['inner_blue'] = tk.IntVar(value=b)
        
        ttk.Label(frame, text="Red:").grid(row=row, column=0, sticky=tk.W, pady=2)
        ttk.Scale(frame, from_=0, to=255, variable=self.vars['inner_red'], orient=tk.HORIZONTAL, length=200).grid(row=row, column=1, sticky=tk.W, padx=(10, 0))
        ttk.Entry(frame, textvariable=self.vars['inner_red'], width=5).grid(row=row, column=2, sticky=tk.W, padx=(5, 0))
        self.vars['inner_red'].trace_add('write', lambda *args: self.update_color_and_settings('inner_color', update_settings))
        row += 1
        
        ttk.Label(frame, text="Green:").grid(row=row, column=0, sticky=tk.W, pady=2)
        ttk.Scale(frame, from_=0, to=255, variable=self.vars['inner_green'], orient=tk.HORIZONTAL, length=200).grid(row=row, column=1, sticky=tk.W, padx=(10, 0))
        ttk.Entry(frame, textvariable=self.vars['inner_green'], width=5).grid(row=row, column=2, sticky=tk.W, padx=(5, 0))
        self.vars['inner_green'].trace_add('write', lambda *args: self.update_color_and_settings('inner_color', update_settings))
        row += 1
        
        ttk.Label(frame, text="Blue:").grid(row=row, column=0, sticky=tk.W, pady=2)
        ttk.Scale(frame, from_=0, to=255, variable=self.vars['inner_blue'], orient=tk.HORIZONTAL, length=200).grid(row=row, column=1, sticky=tk.W, padx=(10, 0))
        ttk.Entry(frame, textvariable=self.vars['inner_blue'], width=5).grid(row=row, column=2, sticky=tk.W, padx=(5, 0))
        self.vars['inner_blue'].trace_add('write', lambda *args: self.update_color_and_settings('inner_color', update_settings))
        row += 1
        
        # Inner outline
        self.vars['inner_outline_enabled'] = tk.BooleanVar(value=self.config.getboolean('crosshair', 'inner_outline_enabled'))
        ttk.Checkbutton(frame, text="Enable Outline", variable=self.vars['inner_outline_enabled']).grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=2)
        self.vars['inner_outline_enabled'].trace_add('write', update_settings)
        row += 1
        
        # Outer Lines Section
        ttk.Label(frame, text="OUTER LINES", font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=(15, 5))
        row += 1
        
        # Outer enabled
        self.vars['outer_enabled'] = tk.BooleanVar(value=self.config.getboolean('crosshair', 'outer_enabled'))
        ttk.Checkbutton(frame, text="Enable Outer Lines", variable=self.vars['outer_enabled']).grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=2)
        self.vars['outer_enabled'].trace_add('write', update_settings)
        row += 1
        
        # Outer length
        ttk.Label(frame, text="Length:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.vars['outer_length'] = tk.IntVar(value=int(self.config.get('crosshair', 'outer_length')))
        ttk.Scale(frame, from_=1, to=50, variable=self.vars['outer_length'], orient=tk.HORIZONTAL, length=200).grid(row=row, column=1, sticky=tk.W, padx=(10, 0))
        ttk.Entry(frame, textvariable=self.vars['outer_length'], width=5).grid(row=row, column=2, sticky=tk.W, padx=(5, 0))
        self.vars['outer_length'].trace_add('write', update_settings)
        row += 1
        
        # Outer thickness
        ttk.Label(frame, text="Thickness:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.vars['outer_thickness'] = tk.IntVar(value=int(self.config.get('crosshair', 'outer_thickness')))
        ttk.Scale(frame, from_=1, to=10, variable=self.vars['outer_thickness'], orient=tk.HORIZONTAL, length=200).grid(row=row, column=1, sticky=tk.W, padx=(10, 0))
        ttk.Entry(frame, textvariable=self.vars['outer_thickness'], width=5).grid(row=row, column=2, sticky=tk.W, padx=(5, 0))
        self.vars['outer_thickness'].trace_add('write', update_settings)
        row += 1
        
        # Outer offset
        ttk.Label(frame, text="Offset:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.vars['outer_offset'] = tk.IntVar(value=int(self.config.get('crosshair', 'outer_offset')))
        ttk.Scale(frame, from_=0, to=30, variable=self.vars['outer_offset'], orient=tk.HORIZONTAL, length=200).grid(row=row, column=1, sticky=tk.W, padx=(10, 0))
        ttk.Entry(frame, textvariable=self.vars['outer_offset'], width=5).grid(row=row, column=2, sticky=tk.W, padx=(5, 0))
        self.vars['outer_offset'].trace_add('write', update_settings)
        row += 1
        
        # Outer color RGB
        r, g, b = self.parse_hex_color(self.config.get('crosshair', 'outer_color'))
        self.vars['outer_red'] = tk.IntVar(value=r)
        self.vars['outer_green'] = tk.IntVar(value=g)
        self.vars['outer_blue'] = tk.IntVar(value=b)
        
        ttk.Label(frame, text="Red:").grid(row=row, column=0, sticky=tk.W, pady=2)
        ttk.Scale(frame, from_=0, to=255, variable=self.vars['outer_red'], orient=tk.HORIZONTAL, length=200).grid(row=row, column=1, sticky=tk.W, padx=(10, 0))
        ttk.Entry(frame, textvariable=self.vars['outer_red'], width=5).grid(row=row, column=2, sticky=tk.W, padx=(5, 0))
        self.vars['outer_red'].trace_add('write', lambda *args: self.update_color_and_settings('outer_color', update_settings))
        row += 1
        
        ttk.Label(frame, text="Green:").grid(row=row, column=0, sticky=tk.W, pady=2)
        ttk.Scale(frame, from_=0, to=255, variable=self.vars['outer_green'], orient=tk.HORIZONTAL, length=200).grid(row=row, column=1, sticky=tk.W, padx=(10, 0))
        ttk.Entry(frame, textvariable=self.vars['outer_green'], width=5).grid(row=row, column=2, sticky=tk.W, padx=(5, 0))
        self.vars['outer_green'].trace_add('write', lambda *args: self.update_color_and_settings('outer_color', update_settings))
        row += 1
        
        ttk.Label(frame, text="Blue:").grid(row=row, column=0, sticky=tk.W, pady=2)
        ttk.Scale(frame, from_=0, to=255, variable=self.vars['outer_blue'], orient=tk.HORIZONTAL, length=200).grid(row=row, column=1, sticky=tk.W, padx=(10, 0))
        ttk.Entry(frame, textvariable=self.vars['outer_blue'], width=5).grid(row=row, column=2, sticky=tk.W, padx=(5, 0))
        self.vars['outer_blue'].trace_add('write', lambda *args: self.update_color_and_settings('outer_color', update_settings))
        row += 1
        
        # Center Dot Section
        ttk.Label(frame, text="CENTER DOT", font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=(15, 5))
        row += 1
        
        # Center dot enabled
        self.vars['center_dot_enabled'] = tk.BooleanVar(value=self.config.getboolean('crosshair', 'center_dot_enabled'))
        ttk.Checkbutton(frame, text="Enable Center Dot", variable=self.vars['center_dot_enabled']).grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=2)
        self.vars['center_dot_enabled'].trace_add('write', update_settings)
        row += 1
        
        # Center dot size
        ttk.Label(frame, text="Size:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.vars['center_dot_size'] = tk.IntVar(value=int(self.config.get('crosshair', 'center_dot_size')))
        ttk.Scale(frame, from_=1, to=10, variable=self.vars['center_dot_size'], orient=tk.HORIZONTAL, length=200).grid(row=row, column=1, sticky=tk.W, padx=(10, 0))
        ttk.Entry(frame, textvariable=self.vars['center_dot_size'], width=5).grid(row=row, column=2, sticky=tk.W, padx=(5, 0))
        self.vars['center_dot_size'].trace_add('write', update_settings)
        row += 1
        
        # General Section
        ttk.Label(frame, text="GENERAL", font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=(15, 5))
        row += 1
        
        # Opacity
        ttk.Label(frame, text="Opacity:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.vars['opacity'] = tk.IntVar(value=int(float(self.config.get('crosshair', 'opacity')) * 100))
        ttk.Scale(frame, from_=10, to=100, variable=self.vars['opacity'], orient=tk.HORIZONTAL, length=200).grid(row=row, column=1, sticky=tk.W, padx=(10, 0))
        ttk.Entry(frame, textvariable=self.vars['opacity'], width=5).grid(row=row, column=2, sticky=tk.W, padx=(5, 0))
        self.vars['opacity'].trace_add('write', lambda *args: self.update_opacity_and_settings(update_settings))
        row += 1
        
        # Apply initial settings to draw crosshair
        update_settings()
        
        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=row, column=0, columnspan=3, pady=20)
        row += 1
        
        ttk.Button(button_frame, text="Toggle Crosshair", command=self.toggle_visibility).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Exit", command=self.quit_app).pack(side=tk.LEFT, padx=5)
        
        # Instructions
        instructions = """
Advanced Crosshair Controls:
• Inner/Outer Lines: Independent control with length, thickness, offset
• Outlines: Black borders around lines for visibility
• Center Dot: Optional dot at crosshair center
• RGB Colors: 0-255 values for precise color control
• Settings apply instantly as you adjust
        """
        ttk.Label(frame, text=instructions, justify=tk.LEFT).grid(row=row, column=0, columnspan=3, pady=10)
        
        self.root.protocol("WM_DELETE_WINDOW", self.quit_app)
        self.root.mainloop()
    
    def update_color_and_settings(self, color_key, update_callback):
        """Update color from RGB values and trigger settings update"""
        try:
            base_key = color_key[:-6]  # Remove '_color'
            r = self.vars[f"{base_key}_red"].get()
            g = self.vars[f"{base_key}_green"].get()
            b = self.vars[f"{base_key}_blue"].get()
            self.config.set('crosshair', color_key, f"#{r:02x}{g:02x}{b:02x}")
            self.save_config()
            if self.overlay_window:
                self.draw_crosshair()
        except:
            pass
    
    def update_opacity_and_settings(self, update_callback):
        """Update opacity and trigger settings update"""
        try:
            opacity_val = self.vars['opacity'].get() / 100
            self.config.set('crosshair', 'opacity', str(opacity_val))
            self.save_config()
            if self.overlay_window:
                self.overlay_window.attributes('-alpha', opacity_val)
                self.draw_crosshair()
        except:
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
