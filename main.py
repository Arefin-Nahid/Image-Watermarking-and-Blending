"""
Main GUI application for Image Processing with Watermarking and Blending.
Refactored version with modular components.
"""

import tkinter as tk
from tkinter import ttk
import os
import logging

from watermarking import Watermarking
from blending import ImageBlending
from advanced_processing import AdvancedImageProcessing
from gui_components import GUIComponents
from event_handlers import EventHandlers
from app_utils import AppUtils


class ImageProcessingApp:
    """Main application class for the Image Processing GUI."""
    
    def __init__(self, root):
        """Initialize the application."""
        self.root = root
        self.root.title("Image Processing - Watermarking & Blending")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize processing classes
        self.watermarking = Watermarking()
        self.blending = ImageBlending()
        self.advanced_processing = AdvancedImageProcessing()
        
        # Initialize GUI components and event handlers
        self.gui_components = GUIComponents(self)
        self.event_handlers = EventHandlers(self)
        
        # Variables for file paths
        self.main_image_path = None
        self.watermark_image_path = None
        self.second_image_path = None
        
        # Variables for parameters
        self.edge_opacity = tk.IntVar(value=50)
        self.watermark_alpha = tk.DoubleVar(value=0.1)
        self.blend_alpha = tk.DoubleVar(value=0.5)
        self.blend_direction = tk.StringVar(value='horizontal')
        self.watermark_type = tk.StringVar(value='visible')
        self.extraction_method = tk.StringVar(value='fourier')
        
        # Advanced processing variables
        self.convolution_filter = tk.StringVar(value='gaussian')
        self.kernel_size = tk.IntVar(value=5)
        self.histogram_operation = tk.StringVar(value='equalize')
        self.histogram_method = tk.StringVar(value='global')
        self.frequency_filter = tk.StringVar(value='lowpass')
        self.cutoff_freq = tk.IntVar(value=30)
        self.segmentation_method = tk.StringVar(value='edge')
        self.threshold_value = tk.IntVar(value=127)
        
        # Setup logging and directories
        self.logger = AppUtils.setup_logging()
        AppUtils.create_directories()
        
        # Bind event handlers to self for easy access
        self._bind_event_handlers()
        
        # Create GUI
        self.create_widgets()
    
    def _bind_event_handlers(self):
        """Bind event handlers to the application instance."""
        # File selection handlers
        self.select_main_image = self.event_handlers.select_main_image
        self.select_watermark_image = self.event_handlers.select_watermark_image
        self.select_first_image = self.event_handlers.select_first_image
        self.select_second_image = self.event_handlers.select_second_image
        self.select_original_image = self.event_handlers.select_original_image
        self.select_watermarked_image = self.event_handlers.select_watermarked_image
        self.select_preprocessing_image = self.event_handlers.select_preprocessing_image
        self.select_analysis_image = self.event_handlers.select_analysis_image
        
        # Parameter update handlers
        self.update_edge_opacity_label = self.event_handlers.update_edge_opacity_label
        self.update_watermark_alpha_label = self.event_handlers.update_watermark_alpha_label
        self.update_blend_alpha_label = self.event_handlers.update_blend_alpha_label
        self.update_kernel_size_label = self.event_handlers.update_kernel_size_label
        self.update_cutoff_freq_label = self.event_handlers.update_cutoff_freq_label
        self.update_threshold_label = self.event_handlers.update_threshold_label
        
        # Operation handlers
        self.apply_watermark = self.event_handlers.apply_watermark
        self.blend_images = self.event_handlers.blend_images
        self.extract_watermark = self.event_handlers.extract_watermark
        self.apply_convolution = self.event_handlers.apply_convolution
        self.apply_histogram_operation = self.event_handlers.apply_histogram_operation
        self.apply_frequency_filter = self.event_handlers.apply_frequency_filter
        self.segment_image = self.event_handlers.segment_image
        self.extract_descriptors = self.event_handlers.extract_descriptors
        self.find_contours = self.event_handlers.find_contours
        self.clear_results = self.event_handlers.clear_results
    
    def create_widgets(self):
        """Create the main GUI widgets."""
        # Create notebook for tabs
        self.notebook = self.gui_components.create_notebook()
        
        # Create all tabs
        self.gui_components.create_watermarking_tab()
        self.gui_components.create_blending_tab()
        self.gui_components.create_extraction_tab()
        self.gui_components.create_preprocessing_tab()
        self.gui_components.create_analysis_tab()
        self.gui_components.create_results_tab()
    
    def run(self):
        """Run the application."""
        self.logger.info("Image Processing Application started")
        self.root.mainloop()


def main():
    """Main function to run the application."""
    root = tk.Tk()
    app = ImageProcessingApp(root)
    app.run()


if __name__ == "__main__":
    main()
