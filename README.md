# Custom Crosshair Overlay

A lightweight, configurable crosshair overlay application for Windows. Perfect for gaming or any application where you need a precise center-screen reference point.

## Features

- **Transparent overlay** - Always stays on top of other applications
- **Configurable settings** - Size, thickness, color, style, and opacity
- **Multiple styles** - Cross, dot, and circle crosshairs
- **Easy toggling** - Simple interface to show/hide crosshair
- **Lightweight** - Minimal resource usage

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/custom-crosshair.git
cd custom-crosshair
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python main.py
```

2. Configure your crosshair using the settings window:
   - **Size**: Adjust the overall size of the crosshair
   - **Thickness**: Control line thickness
   - **Color**: Set color using hex codes (e.g., #FF0000 for red)
   - **Style**: Choose between cross, dot, or circle
   - **Opacity**: Set transparency (0.1 to 1.0)

3. Click "Toggle Crosshair" to show/hide the overlay

## Configuration

Settings are automatically saved to `config.ini` and will persist between sessions.

## Future Plans

- C++ version for even better performance
- Global hotkey support
- System tray integration
- More crosshair styles and customization options
