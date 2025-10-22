"""
GUI Components for the Image Processing Application.
Contains all GUI creation methods and UI components.
"""

import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext


class GUIComponents:
    """Class containing all GUI creation methods."""
    
    def __init__(self, parent_app):
        """Initialize with reference to parent application."""
        self.app = parent_app
        self.root = parent_app.root
        self.notebook = None
        
    def create_notebook(self):
        """Create the main notebook widget."""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        return self.notebook
    
    def create_watermarking_tab(self):
        """Create the watermarking tab."""
        watermarking_frame = ttk.Frame(self.notebook)
        self.notebook.add(watermarking_frame, text="Watermarking")
        
        # Main image selection
        main_frame = ttk.LabelFrame(watermarking_frame, text="Image Selection", padding=10)
        main_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(main_frame, text="Select Main Image", 
                  command=self.app.select_main_image).pack(side='left', padx=5)
        self.app.main_image_label = ttk.Label(main_frame, text="No image selected")
        self.app.main_image_label.pack(side='left', padx=10)
        
        # Watermark image selection
        watermark_frame = ttk.LabelFrame(watermarking_frame, text="Watermark Selection", padding=10)
        watermark_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(watermark_frame, text="Select Watermark Image", 
                  command=self.app.select_watermark_image).pack(side='left', padx=5)
        self.app.watermark_image_label = ttk.Label(watermark_frame, text="No watermark selected")
        self.app.watermark_image_label.pack(side='left', padx=10)
        
        # Watermarking options
        options_frame = ttk.LabelFrame(watermarking_frame, text="Watermarking Options", padding=10)
        options_frame.pack(fill='x', padx=10, pady=5)
        
        # Watermark type
        ttk.Label(options_frame, text="Watermark Type:").grid(row=0, column=0, sticky='w', padx=5)
        ttk.Radiobutton(options_frame, text="Visible (Edge Detection)", 
                       variable=self.app.watermark_type, value='visible').grid(row=0, column=1, sticky='w', padx=5)
        ttk.Radiobutton(options_frame, text="Invisible (Fourier Transform)", 
                       variable=self.app.watermark_type, value='invisible').grid(row=0, column=2, sticky='w', padx=5)
        
        # Edge opacity for visible watermarking
        ttk.Label(options_frame, text="Edge Opacity (0-100):").grid(row=1, column=0, sticky='w', padx=5)
        self.app.edge_opacity_scale = ttk.Scale(options_frame, from_=0, to=100, 
                                           variable=self.app.edge_opacity, orient='horizontal')
        self.app.edge_opacity_scale.grid(row=1, column=1, sticky='ew', padx=5)
        self.app.edge_opacity_label = ttk.Label(options_frame, text="50")
        self.app.edge_opacity_label.grid(row=1, column=2, padx=5)
        
        # Watermark alpha for invisible watermarking
        ttk.Label(options_frame, text="Watermark Alpha (0.0-1.0):").grid(row=2, column=0, sticky='w', padx=5)
        self.app.watermark_alpha_scale = ttk.Scale(options_frame, from_=0.0, to=1.0, 
                                              variable=self.app.watermark_alpha, orient='horizontal')
        self.app.watermark_alpha_scale.grid(row=2, column=1, sticky='ew', padx=5)
        self.app.watermark_alpha_label = ttk.Label(options_frame, text="0.1")
        self.app.watermark_alpha_label.grid(row=2, column=2, padx=5)
        
        # Update labels when scales change
        self.app.edge_opacity_scale.configure(command=self.app.update_edge_opacity_label)
        self.app.watermark_alpha_scale.configure(command=self.app.update_watermark_alpha_label)
        
        # Process button
        process_frame = ttk.Frame(watermarking_frame)
        process_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(process_frame, text="Apply Watermark", 
                  command=self.app.apply_watermark, style='Accent.TButton').pack(side='left', padx=5)
        
        # Preview frame
        preview_frame = ttk.LabelFrame(watermarking_frame, text="Preview", padding=10)
        preview_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Create canvas for image preview
        self.app.preview_canvas = tk.Canvas(preview_frame, bg='white', height=300)
        self.app.preview_canvas.pack(fill='both', expand=True)
    
    def create_blending_tab(self):
        """Create the blending tab."""
        blending_frame = ttk.Frame(self.notebook)
        self.notebook.add(blending_frame, text="Image Blending")
        
        # Image selection
        selection_frame = ttk.LabelFrame(blending_frame, text="Image Selection", padding=10)
        selection_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(selection_frame, text="Select First Image", 
                  command=self.app.select_first_image).pack(side='left', padx=5)
        self.app.first_image_label = ttk.Label(selection_frame, text="No image selected")
        self.app.first_image_label.pack(side='left', padx=10)
        
        ttk.Button(selection_frame, text="Select Second Image", 
                  command=self.app.select_second_image).pack(side='left', padx=5)
        self.app.second_image_label = ttk.Label(selection_frame, text="No image selected")
        self.app.second_image_label.pack(side='left', padx=10)
        
        # Blending options
        blend_options_frame = ttk.LabelFrame(blending_frame, text="Blending Options", padding=10)
        blend_options_frame.pack(fill='x', padx=10, pady=5)
        
        # Blend direction
        ttk.Label(blend_options_frame, text="Blend Direction:").grid(row=0, column=0, sticky='w', padx=5)
        direction_frame = ttk.Frame(blend_options_frame)
        direction_frame.grid(row=0, column=1, sticky='w', padx=5)
        
        ttk.Radiobutton(direction_frame, text="Left to Right", 
                       variable=self.app.blend_direction, value='horizontal').pack(side='left', padx=5)
        ttk.Radiobutton(direction_frame, text="Top to Bottom", 
                       variable=self.app.blend_direction, value='vertical').pack(side='left', padx=5)
        ttk.Radiobutton(direction_frame, text="Diagonal", 
                       variable=self.app.blend_direction, value='diagonal').pack(side='left', padx=5)
        
        # Blend alpha
        ttk.Label(blend_options_frame, text="Blend Alpha (0.0-1.0):").grid(row=1, column=0, sticky='w', padx=5)
        self.app.blend_alpha_scale = ttk.Scale(blend_options_frame, from_=0.0, to=1.0, 
                                          variable=self.app.blend_alpha, orient='horizontal')
        self.app.blend_alpha_scale.grid(row=1, column=1, sticky='ew', padx=5)
        self.app.blend_alpha_label = ttk.Label(blend_options_frame, text="0.5")
        self.app.blend_alpha_label.grid(row=1, column=2, padx=5)
        
        # Update label when scale changes
        self.app.blend_alpha_scale.configure(command=self.app.update_blend_alpha_label)
        
        # Process button
        process_frame = ttk.Frame(blending_frame)
        process_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(process_frame, text="Blend Images", 
                  command=self.app.blend_images, style='Accent.TButton').pack(side='left', padx=5)
        
        # Preview frame
        preview_frame = ttk.LabelFrame(blending_frame, text="Preview", padding=10)
        preview_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Create canvas for image preview
        self.app.blend_preview_canvas = tk.Canvas(preview_frame, bg='white', height=300)
        self.app.blend_preview_canvas.pack(fill='both', expand=True)
    
    def create_extraction_tab(self):
        """Create the watermark extraction tab."""
        extraction_frame = ttk.Frame(self.notebook)
        self.notebook.add(extraction_frame, text="Watermark Extraction")
        
        # Image selection
        selection_frame = ttk.LabelFrame(extraction_frame, text="Image Selection", padding=10)
        selection_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(selection_frame, text="Select Original Image", 
                  command=self.app.select_original_image).pack(side='left', padx=5)
        self.app.original_image_label = ttk.Label(selection_frame, text="No original image selected")
        self.app.original_image_label.pack(side='left', padx=10)
        
        ttk.Button(selection_frame, text="Select Watermarked Image", 
                  command=self.app.select_watermarked_image).pack(side='left', padx=5)
        self.app.watermarked_image_label = ttk.Label(selection_frame, text="No watermarked image selected")
        self.app.watermarked_image_label.pack(side='left', padx=10)
        
        # Extraction options
        extraction_options_frame = ttk.LabelFrame(extraction_frame, text="Extraction Options", padding=10)
        extraction_options_frame.pack(fill='x', padx=10, pady=5)
        
        # Extraction method
        ttk.Label(extraction_options_frame, text="Extraction Method:").grid(row=0, column=0, sticky='w', padx=5)
        ttk.Radiobutton(extraction_options_frame, text="Fourier Transform", 
                       variable=self.app.extraction_method, value='fourier').grid(row=0, column=1, sticky='w', padx=5)
        ttk.Radiobutton(extraction_options_frame, text="Edge Detection", 
                       variable=self.app.extraction_method, value='edge').grid(row=0, column=2, sticky='w', padx=5)
        
        # Process button
        process_frame = ttk.Frame(extraction_frame)
        process_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(process_frame, text="Extract Watermark", 
                  command=self.app.extract_watermark, style='Accent.TButton').pack(side='left', padx=5)
        
        # Preview frame
        preview_frame = ttk.LabelFrame(extraction_frame, text="Preview", padding=10)
        preview_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Create canvas for image preview
        self.app.extract_preview_canvas = tk.Canvas(preview_frame, bg='white', height=300)
        self.app.extract_preview_canvas.pack(fill='both', expand=True)
    
    def create_preprocessing_tab(self):
        """Create the preprocessing tab."""
        preprocessing_frame = ttk.Frame(self.notebook)
        self.notebook.add(preprocessing_frame, text="Preprocessing")
        
        # Image selection
        selection_frame = ttk.LabelFrame(preprocessing_frame, text="Image Selection", padding=10)
        selection_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(selection_frame, text="Select Image", 
                  command=self.app.select_preprocessing_image).pack(side='left', padx=5)
        self.app.preprocessing_image_label = ttk.Label(selection_frame, text="No image selected")
        self.app.preprocessing_image_label.pack(side='left', padx=10)
        
        # Convolution filters
        convolution_frame = ttk.LabelFrame(preprocessing_frame, text="Convolution Filters", padding=10)
        convolution_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(convolution_frame, text="Filter Type:").grid(row=0, column=0, sticky='w', padx=5)
        self.app.convolution_filter = tk.StringVar(value='gaussian')
        convolution_combo = ttk.Combobox(convolution_frame, textvariable=self.app.convolution_filter,
                                        values=['gaussian', 'sobel_x', 'sobel_y', 'laplacian', 'sharpen', 'edge_detect'])
        convolution_combo.grid(row=0, column=1, sticky='ew', padx=5)
        
        ttk.Label(convolution_frame, text="Kernel Size:").grid(row=1, column=0, sticky='w', padx=5)
        self.app.kernel_size = tk.IntVar(value=5)
        kernel_scale = ttk.Scale(convolution_frame, from_=3, to=15, variable=self.app.kernel_size, orient='horizontal')
        kernel_scale.grid(row=1, column=1, sticky='ew', padx=5)
        self.app.kernel_size_label = ttk.Label(convolution_frame, text="5")
        self.app.kernel_size_label.grid(row=1, column=2, padx=5)
        kernel_scale.configure(command=self.app.update_kernel_size_label)
        
        ttk.Button(convolution_frame, text="Apply Convolution", 
                  command=self.app.apply_convolution).grid(row=2, column=0, columnspan=2, pady=5)
        
        # Histogram operations
        histogram_frame = ttk.LabelFrame(preprocessing_frame, text="Histogram Operations", padding=10)
        histogram_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(histogram_frame, text="Operation:").grid(row=0, column=0, sticky='w', padx=5)
        self.app.histogram_operation = tk.StringVar(value='equalize')
        histogram_combo = ttk.Combobox(histogram_frame, textvariable=self.app.histogram_operation,
                                     values=['equalize', 'match'])
        histogram_combo.grid(row=0, column=1, sticky='ew', padx=5)
        
        ttk.Label(histogram_frame, text="Method:").grid(row=1, column=0, sticky='w', padx=5)
        self.app.histogram_method = tk.StringVar(value='global')
        method_combo = ttk.Combobox(histogram_frame, textvariable=self.app.histogram_method,
                                  values=['global', 'clahe'])
        method_combo.grid(row=1, column=1, sticky='ew', padx=5)
        
        ttk.Button(histogram_frame, text="Apply Histogram Operation", 
                  command=self.app.apply_histogram_operation).grid(row=2, column=0, columnspan=2, pady=5)
        
        # Frequency filtering
        frequency_frame = ttk.LabelFrame(preprocessing_frame, text="Frequency Domain Filtering", padding=10)
        frequency_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(frequency_frame, text="Filter Type:").grid(row=0, column=0, sticky='w', padx=5)
        self.app.frequency_filter = tk.StringVar(value='lowpass')
        frequency_combo = ttk.Combobox(frequency_frame, textvariable=self.app.frequency_filter,
                                      values=['lowpass', 'highpass', 'bandpass'])
        frequency_combo.grid(row=0, column=1, sticky='ew', padx=5)
        
        ttk.Label(frequency_frame, text="Cutoff Frequency:").grid(row=1, column=0, sticky='w', padx=5)
        self.app.cutoff_freq = tk.IntVar(value=30)
        freq_scale = ttk.Scale(frequency_frame, from_=10, to=100, variable=self.app.cutoff_freq, orient='horizontal')
        freq_scale.grid(row=1, column=1, sticky='ew', padx=5)
        self.app.cutoff_freq_label = ttk.Label(frequency_frame, text="30")
        self.app.cutoff_freq_label.grid(row=1, column=2, padx=5)
        freq_scale.configure(command=self.app.update_cutoff_freq_label)
        
        ttk.Button(frequency_frame, text="Apply Frequency Filter", 
                  command=self.app.apply_frequency_filter).grid(row=2, column=0, columnspan=2, pady=5)
        
        # Preview frame
        preview_frame = ttk.LabelFrame(preprocessing_frame, text="Preview", padding=10)
        preview_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.app.preprocessing_preview_canvas = tk.Canvas(preview_frame, bg='white', height=300)
        self.app.preprocessing_preview_canvas.pack(fill='both', expand=True)
    
    def create_analysis_tab(self):
        """Create the analysis tab."""
        analysis_frame = ttk.Frame(self.notebook)
        self.notebook.add(analysis_frame, text="Analysis")
        
        # Image selection
        selection_frame = ttk.LabelFrame(analysis_frame, text="Image Selection", padding=10)
        selection_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(selection_frame, text="Select Image", 
                  command=self.app.select_analysis_image).pack(side='left', padx=5)
        self.app.analysis_image_label = ttk.Label(selection_frame, text="No image selected")
        self.app.analysis_image_label.pack(side='left', padx=10)
        
        # Segmentation
        segmentation_frame = ttk.LabelFrame(analysis_frame, text="Image Segmentation", padding=10)
        segmentation_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(segmentation_frame, text="Method:").grid(row=0, column=0, sticky='w', padx=5)
        self.app.segmentation_method = tk.StringVar(value='edge')
        seg_combo = ttk.Combobox(segmentation_frame, textvariable=self.app.segmentation_method,
                               values=['edge', 'threshold', 'otsu', 'adaptive'])
        seg_combo.grid(row=0, column=1, sticky='ew', padx=5)
        
        ttk.Label(segmentation_frame, text="Threshold:").grid(row=1, column=0, sticky='w', padx=5)
        self.app.threshold_value = tk.IntVar(value=127)
        thresh_scale = ttk.Scale(segmentation_frame, from_=0, to=255, variable=self.app.threshold_value, orient='horizontal')
        thresh_scale.grid(row=1, column=1, sticky='ew', padx=5)
        self.app.threshold_label = ttk.Label(segmentation_frame, text="127")
        self.app.threshold_label.grid(row=1, column=2, padx=5)
        thresh_scale.configure(command=self.app.update_threshold_label)
        
        ttk.Button(segmentation_frame, text="Segment Image", 
                  command=self.app.segment_image).grid(row=2, column=0, columnspan=2, pady=5)
        
        # Region descriptors
        descriptors_frame = ttk.LabelFrame(analysis_frame, text="Region Descriptors", padding=10)
        descriptors_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(descriptors_frame, text="Extract Descriptors", 
                  command=self.app.extract_descriptors).pack(side='left', padx=5)
        ttk.Button(descriptors_frame, text="Find Contours", 
                  command=self.app.find_contours).pack(side='left', padx=5)
        
        # Analysis results
        results_frame = ttk.LabelFrame(analysis_frame, text="Analysis Results", padding=10)
        results_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.app.analysis_results = scrolledtext.ScrolledText(results_frame, height=15)
        self.app.analysis_results.pack(fill='both', expand=True)
        
        # Preview frame
        preview_frame = ttk.LabelFrame(analysis_frame, text="Preview", padding=10)
        preview_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.app.analysis_preview_canvas = tk.Canvas(preview_frame, bg='white', height=200)
        self.app.analysis_preview_canvas.pack(fill='both', expand=True)
    
    def create_results_tab(self):
        """Create the results and logs tab."""
        results_frame = ttk.Frame(self.notebook)
        self.notebook.add(results_frame, text="Results & Logs")
        
        # Results display
        results_display_frame = ttk.LabelFrame(results_frame, text="Operation Results", padding=10)
        results_display_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Text widget for results
        self.app.results_text = scrolledtext.ScrolledText(results_display_frame, height=20)
        self.app.results_text.pack(fill='both', expand=True)
        
        # Clear button
        ttk.Button(results_display_frame, text="Clear Results", 
                  command=self.app.clear_results).pack(pady=5)
