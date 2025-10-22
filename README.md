# Image Processing Application

A modular Python application for advanced image processing with watermarking, blending, and analysis capabilities. Features visible and invisible watermarking, gradient-based image blending, and advanced processing including convolution operations, segmentation, histogram operations, frequency domain filtering, and region descriptor analysis.

## Features

### Watermarking
- **Visible Watermarking**: Uses Canny edge detection to create visible watermarks with adjustable opacity
- **Invisible Watermarking**: Uses Fourier Transform to embed watermarks in the frequency domain
- **Watermark Extraction**: Extract watermarks using both Fourier Transform and edge detection methods

### Image Blending
- **Gradient-based Blending**: Blend images with smooth transitions
- **Multiple Directions**: Left-to-right, top-to-bottom, and diagonal blending
- **Adjustable Parameters**: Control blend ratio and direction

### Advanced Image Processing
- **Convolution Operations**: Apply various filters (Gaussian, Sobel, Laplacian, Sharpen, Edge Detection)
- **Image Segmentation**: Edge detection, thresholding, Otsu's method, and adaptive thresholding
- **Histogram Operations**: Histogram equalization and histogram matching
- **Frequency Domain Filtering**: Low-pass, high-pass, and band-pass filters
- **Region Descriptors**: Shape, texture, and statistical feature analysis
- **Contour Detection**: Automatic contour detection and analysis

### User Interface
- **Enhanced GUI**: Multi-tab interface with preprocessing and analysis capabilities
- **Real-time Preview**: See results before saving
- **File Management**: Organized output with automatic directory structure
- **Logging**: Comprehensive logging for all operations
- **Advanced Controls**: Sliders, dropdowns, and parameter adjustment for all features

## Installation

### Prerequisites
- Python 3.7 or higher
- Windows, macOS, or Linux

### Setup
1. Clone or download this repository
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Dependencies
- opencv-python==4.8.1.78
- numpy==1.24.3
- Pillow==10.0.1
- tkinter (usually included with Python)

## Usage

### Running the Application
```bash
python main.py
```

### Directory Structure
The application automatically creates the following directories:
- `images/` - Store input images
- `watermarked_images/` - Store watermarked results
- `blended_images/` - Store blended results
- `results/` - Store extracted watermarks and other results
- `logs/` - Store application logs

### Watermarking

#### Visible Watermarking
1. Select "Watermarking" tab
2. Choose main image and watermark image
3. Select "Visible (Edge Detection)" option
4. Adjust edge opacity (0-100)
5. Click "Apply Watermark"

#### Invisible Watermarking
1. Select "Watermarking" tab
2. Choose main image and watermark image
3. Select "Invisible (Fourier Transform)" option
4. Adjust watermark alpha (0.0-1.0)
5. Click "Apply Watermark"

### Image Blending
1. Select "Image Blending" tab
2. Choose two images to blend
3. Select blending direction:
   - Left to Right (horizontal)
   - Top to Bottom (vertical)
   - Diagonal
4. Adjust blend alpha (0.0-1.0)
5. Click "Blend Images"

### Watermark Extraction
1. Select "Watermark Extraction" tab
2. Choose original and watermarked images
3. Select extraction method:
   - Fourier Transform
   - Edge Detection
4. Click "Extract Watermark"

### Advanced Preprocessing
1. Select "Preprocessing" tab
2. Choose image for preprocessing
3. Apply convolution filters:
   - Select filter type (Gaussian, Sobel, Laplacian, etc.)
   - Adjust kernel size
   - Click "Apply Convolution"
4. Apply histogram operations:
   - Choose operation (equalize or match)
   - Select method (global or CLAHE)
   - Click "Apply Histogram Operation"
5. Apply frequency domain filtering:
   - Select filter type (low-pass, high-pass, band-pass)
   - Adjust cutoff frequency
   - Click "Apply Frequency Filter"

### Image Analysis
1. Select "Analysis" tab
2. Choose image for analysis
3. Perform segmentation:
   - Select method (edge, threshold, Otsu, adaptive)
   - Adjust threshold value
   - Click "Segment Image"
4. Extract region descriptors:
   - Click "Extract Descriptors" for shape, texture, and statistical analysis
   - Click "Find Contours" for contour detection and analysis

## Technical Details

### Visible Watermarking Algorithm
1. Load main image and watermark image
2. Resize watermark to match main image dimensions
3. Apply Canny edge detection to watermark
4. Overlay edges onto main image with adjustable opacity
5. Save result

### Invisible Watermarking Algorithm
1. Load main image and watermark image
2. Resize watermark to match main image dimensions
3. Split RGB channels
4. Apply Fourier Transform to each channel
5. Embed watermark in frequency domain
6. Apply inverse Fourier Transform
7. Merge channels and save result

### Image Blending Algorithm
1. Load two images
2. Resize to common dimensions
3. Create gradient mask based on direction
4. Apply blending using weighted combination
5. Save result

### Advanced Processing Algorithms

#### Convolution Operations
1. Define convolution kernels (Gaussian, Sobel, Laplacian, etc.)
2. Apply cv2.filter2D() with custom kernels
3. Handle different filter types and kernel sizes
4. Save filtered results

#### Image Segmentation
1. Convert to grayscale for processing
2. Apply segmentation method (Canny, threshold, Otsu, adaptive)
3. Generate binary or edge maps
4. Save segmented results

#### Histogram Operations
1. Calculate image histograms
2. Apply equalization (global or CLAHE)
3. Match histograms between images
4. Preserve color information in LAB/YUV space

#### Frequency Domain Filtering
1. Apply Discrete Fourier Transform (DFT)
2. Create frequency masks (low-pass, high-pass, band-pass)
3. Apply filters in frequency domain
4. Inverse DFT to get filtered image

#### Region Descriptors
1. Find contours using cv2.findContours()
2. Calculate shape features (area, perimeter, aspect ratio, Hu moments)
3. Extract texture features (mean, std, energy, entropy)
4. Compute statistical features (skewness, kurtosis, etc.)
5. Visualize and analyze results

## File Management

The application includes automatic file organization:
- Results are saved with timestamps
- Files are organized by operation type
- Automatic cleanup of old files (configurable)
- Backup functionality for important files

## Error Handling

The application includes comprehensive error handling:
- Image format validation
- File existence checks
- Memory management for large images
- User-friendly error messages

## Performance Considerations

- Optimized for various image sizes
- Memory-efficient processing
- Threaded operations to prevent UI freezing
- Automatic cleanup of temporary files

## Troubleshooting

### Common Issues
1. **"Could not load image"**: Check file format and path
2. **Memory errors**: Reduce image size or close other applications
3. **Permission errors**: Ensure write permissions for output directories

### Logs
Check the `logs/app.log` file for detailed error information.

## Development

### Project Structure
```
IPCV/
├── main.py                 # Main application (refactored)
├── gui_components.py       # GUI creation and layout
├── event_handlers.py        # Event handling and user interactions
├── app_utils.py            # Utility functions and helpers
├── watermarking.py         # Watermarking functionality
├── blending.py            # Image blending functionality
├── advanced_processing.py  # Advanced image processing features
├── file_manager.py        # File management utilities
├── requirements.txt       # Python dependencies
├── run_app.bat           # Windows launcher
├── images/               # Input images directory
├── watermarked_images/   # Watermarked results
├── blended_images/       # Blended results
├── results/              # Analysis results
└── logs/                 # Application logs
```

### Adding New Features
1. **GUI Components**: Add new tabs/controls in `gui_components.py`
2. **Event Handlers**: Add new interactions in `event_handlers.py`
3. **Processing**: Add new algorithms in `watermarking.py`, `blending.py`, or `advanced_processing.py`
4. **Utilities**: Add helper functions in `app_utils.py`

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## Support

For support and questions, please check the logs directory for error details or create an issue in the project repository.
