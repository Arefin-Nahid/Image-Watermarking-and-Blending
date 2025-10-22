# Image Processing Application - Setup Guide

## Quick Start

### Method 1: Windows (Easiest)
1. Double-click `run_app.bat`
2. Follow the prompts

### Method 2: Python Command Line
1. Install dependencies: `pip install opencv-python numpy Pillow`
2. Run: `python main.py`

### Method 3: Anaconda/Spyder
1. Open Anaconda Navigator
2. Launch Spyder
3. Open `main.py` in Spyder
4. Install dependencies: `conda install opencv numpy pillow`
5. Press F5 to run

## Features

- **Watermarking**: Visible and invisible watermarking
- **Image Blending**: Gradient-based blending  
- **Preprocessing**: Convolution filters, histogram operations
- **Analysis**: Segmentation, region descriptors, contours
- **GUI**: User-friendly interface with 6 tabs

## Usage

1. **Select Images**: Use file selection buttons
2. **Adjust Parameters**: Use sliders and dropdowns  
3. **Apply Operations**: Click operation buttons
4. **View Results**: Check the Results tab
5. **Save Files**: Results are automatically saved

## Troubleshooting

- **Import Errors**: Install missing packages (`pip install opencv-python numpy Pillow`)
- **GUI Issues**: Check console for error messages
- **Performance**: Use smaller images for testing
- **Logs**: Check `logs/app.log` for details
