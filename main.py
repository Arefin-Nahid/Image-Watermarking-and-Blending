import tkinter as tk
from tkinter import ttk
import os
import logging

from watermarking import Watermarking
from blending import ImageBlending
from gui_components import GUIComponents
from event_handlers import EventHandlers
from app_utils import AppUtils


class ImageProcessingApp:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processing Application")
        self.root.geometry("1400x850")
        self.root.minsize(1200, 700)
        
        self.bg_color = '#F5F7FA'
        self.root.configure(bg=self.bg_color)
        
        # Initialize processing classes
        self.watermarking = Watermarking()
        self.blending = ImageBlending()
        
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
        
        # Setup logging and directories
        self.logger = AppUtils.setup_logging()
        AppUtils.create_directories()
        
        # Bind event handlers
        self._bind_event_handlers()
        
        # Create GUI
        self.create_widgets()
        
        # Welcome message
        self._show_welcome_message()
    
    def _bind_event_handlers(self):
        # File selection handlers
        self.select_main_image = self.event_handlers.select_main_image
        self.select_watermark_image = self.event_handlers.select_watermark_image
        self.select_first_image = self.event_handlers.select_first_image
        self.select_second_image = self.event_handlers.select_second_image
        self.select_original_image = self.event_handlers.select_original_image
        self.select_watermarked_image = self.event_handlers.select_watermarked_image
        
        # Parameter update handlers
        self.update_edge_opacity_label = self.event_handlers.update_edge_opacity_label
        self.update_watermark_alpha_label = self.event_handlers.update_watermark_alpha_label
        self.update_blend_alpha_label = self.event_handlers.update_blend_alpha_label
        
        # Operation handlers
        self.apply_watermark = self.event_handlers.apply_watermark
        self.blend_images = self.event_handlers.blend_images
        self.extract_watermark = self.event_handlers.extract_watermark
        self.clear_results = self.event_handlers.clear_results
    
    def create_widgets(self):
        # Header
        header_frame = tk.Frame(self.root, bg='#4A90E2', height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, 
                text="Image Processing Application", 
                font=('Segoe UI', 16, 'bold'), 
                fg='white', 
                bg='#4A90E2').pack(side='left', padx=20, pady=15)
        
        tk.Label(header_frame, 
                text="Watermarking & Image Blending", 
                font=('Segoe UI', 10), 
                fg='white', 
                bg='#4A90E2').pack(side='left', padx=10)
        
        # Create notebook for tabs
        self.notebook = self.gui_components.create_notebook()
        
        # Create tabs
        self.gui_components.create_watermarking_tab()
        self.gui_components.create_blending_tab()
        self.gui_components.create_extraction_tab()
        self.gui_components.create_results_tab()
        
        # Status bar
        status_bar = tk.Frame(self.root, bg='#2C3E50', height=25)
        status_bar.pack(side='bottom', fill='x')
        status_bar.pack_propagate(False)
        
        self.status_label = tk.Label(status_bar, 
                                     text="Ready", 
                                     font=('Segoe UI', 9), 
                                     fg='white', 
                                     bg='#2C3E50')
        self.status_label.pack(side='left', padx=15, pady=3)
    
    def _show_welcome_message(self):
        if hasattr(self, 'results_text'):
            self.results_text.insert(tk.END, "Image Processing Application\n")
            self.results_text.insert(tk.END, "=" * 60 + "\n\n")
            self.results_text.insert(tk.END, "Features:\n")
            self.results_text.insert(tk.END, "  • Visible Watermarking\n")
            self.results_text.insert(tk.END, "  • Invisible Watermarking\n")
            self.results_text.insert(tk.END, "  • Image Blending\n")
            self.results_text.insert(tk.END, "  • Watermark Extraction\n\n")
            self.results_text.insert(tk.END, "Ready to process images...\n")
            self.results_text.insert(tk.END, "-" * 60 + "\n\n")
    
    def run(self):
        self.logger.info("Image Processing Application started")
        self.root.mainloop()


def main():
    root = tk.Tk()
    app = ImageProcessingApp(root)
    app.run()


if __name__ == "__main__":
    main()