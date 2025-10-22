"""
Event Handlers for the Image Processing Application.
Contains all event handling methods and callbacks.
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import os
import threading
from datetime import datetime
import logging


class EventHandlers:
    """Class containing all event handling methods."""
    
    def __init__(self, parent_app):
        """Initialize with reference to parent application."""
        self.app = parent_app
        self.logger = logging.getLogger(__name__)
    
    # ==================== FILE SELECTION HANDLERS ====================
    
    def select_main_image(self):
        """Select the main image for watermarking."""
        file_path = filedialog.askopenfilename(
            title="Select Main Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
        )
        if file_path:
            self.app.main_image_path = file_path
            self.app.main_image_label.config(text=os.path.basename(file_path))
            self.logger.info(f"Main image selected: {file_path}")
    
    def select_watermark_image(self):
        """Select the watermark image."""
        file_path = filedialog.askopenfilename(
            title="Select Watermark Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
        )
        if file_path:
            self.app.watermark_image_path = file_path
            self.app.watermark_image_label.config(text=os.path.basename(file_path))
            self.logger.info(f"Watermark image selected: {file_path}")
    
    def select_first_image(self):
        """Select the first image for blending."""
        file_path = filedialog.askopenfilename(
            title="Select First Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
        )
        if file_path:
            self.app.main_image_path = file_path
            self.app.first_image_label.config(text=os.path.basename(file_path))
            self.logger.info(f"First image selected: {file_path}")
    
    def select_second_image(self):
        """Select the second image for blending."""
        file_path = filedialog.askopenfilename(
            title="Select Second Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
        )
        if file_path:
            self.app.second_image_path = file_path
            self.app.second_image_label.config(text=os.path.basename(file_path))
            self.logger.info(f"Second image selected: {file_path}")
    
    def select_original_image(self):
        """Select the original image for extraction."""
        file_path = filedialog.askopenfilename(
            title="Select Original Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
        )
        if file_path:
            self.app.main_image_path = file_path
            self.app.original_image_label.config(text=os.path.basename(file_path))
            self.logger.info(f"Original image selected: {file_path}")
    
    def select_watermarked_image(self):
        """Select the watermarked image for extraction."""
        file_path = filedialog.askopenfilename(
            title="Select Watermarked Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
        )
        if file_path:
            self.app.watermark_image_path = file_path
            self.app.watermarked_image_label.config(text=os.path.basename(file_path))
            self.logger.info(f"Watermarked image selected: {file_path}")
    
    def select_preprocessing_image(self):
        """Select image for preprocessing."""
        file_path = filedialog.askopenfilename(
            title="Select Image for Preprocessing",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
        )
        if file_path:
            self.app.main_image_path = file_path
            self.app.preprocessing_image_label.config(text=os.path.basename(file_path))
            self.logger.info(f"Preprocessing image selected: {file_path}")
    
    def select_analysis_image(self):
        """Select image for analysis."""
        file_path = filedialog.askopenfilename(
            title="Select Image for Analysis",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
        )
        if file_path:
            self.app.main_image_path = file_path
            self.app.analysis_image_label.config(text=os.path.basename(file_path))
            self.logger.info(f"Analysis image selected: {file_path}")
    
    # ==================== PARAMETER UPDATE HANDLERS ====================
    
    def update_edge_opacity_label(self, value):
        """Update the edge opacity label."""
        self.app.edge_opacity_label.config(text=str(int(float(value))))
    
    def update_watermark_alpha_label(self, value):
        """Update the watermark alpha label."""
        self.app.watermark_alpha_label.config(text=f"{float(value):.2f}")
    
    def update_blend_alpha_label(self, value):
        """Update the blend alpha label."""
        self.app.blend_alpha_label.config(text=f"{float(value):.2f}")
    
    def update_kernel_size_label(self, value):
        """Update kernel size label."""
        self.app.kernel_size_label.config(text=str(int(float(value))))
    
    def update_cutoff_freq_label(self, value):
        """Update cutoff frequency label."""
        self.app.cutoff_freq_label.config(text=str(int(float(value))))
    
    def update_threshold_label(self, value):
        """Update threshold label."""
        self.app.threshold_label.config(text=str(int(float(value))))
    
    # ==================== WATERMARKING HANDLERS ====================
    
    def apply_watermark(self):
        """Apply watermarking to the selected images."""
        if not self.app.main_image_path or not self.app.watermark_image_path:
            messagebox.showerror("Error", "Please select both main and watermark images.")
            return
        
        # Validate images
        main_valid, main_msg = self.app.watermarking.validate_image(self.app.main_image_path)
        watermark_valid, watermark_msg = self.app.watermarking.validate_image(self.app.watermark_image_path)
        
        if not main_valid:
            messagebox.showerror("Error", f"Main image error: {main_msg}")
            return
        if not watermark_valid:
            messagebox.showerror("Error", f"Watermark image error: {watermark_msg}")
            return
        
        # Run watermarking in a separate thread
        threading.Thread(target=self._apply_watermark_thread, daemon=True).start()
    
    def _apply_watermark_thread(self):
        """Apply watermarking in a separate thread."""
        try:
            watermark_type = self.app.watermark_type.get()
            
            if watermark_type == 'visible':
                edge_opacity = self.app.edge_opacity.get()
                result_path = self.app.watermarking.visible_watermark(
                    self.app.main_image_path, 
                    self.app.watermark_image_path, 
                    edge_opacity
                )
            else:  # invisible
                watermark_alpha = self.app.watermark_alpha.get()
                result_path = self.app.watermarking.invisible_watermark(
                    self.app.main_image_path, 
                    self.app.watermark_image_path, 
                    watermark_alpha
                )
            
            if result_path:
                self.app.root.after(0, self._watermark_success, result_path)
            else:
                self.app.root.after(0, self._watermark_error)
                
        except Exception as e:
            self.app.root.after(0, self._watermark_error, str(e))
    
    def _watermark_success(self, result_path):
        """Handle successful watermarking."""
        self.logger.info(f"Watermarking completed successfully: {result_path}")
        self.app.results_text.insert(tk.END, f"Watermarking completed: {result_path}\n")
        self.app.results_text.see(tk.END)
        messagebox.showinfo("Success", f"Watermarking completed successfully!\nSaved to: {result_path}")
    
    def _watermark_error(self, error_msg=None):
        """Handle watermarking error."""
        error_text = f"Watermarking failed: {error_msg}" if error_msg else "Watermarking failed"
        self.logger.error(error_text)
        self.app.results_text.insert(tk.END, f"{error_text}\n")
        self.app.results_text.see(tk.END)
        messagebox.showerror("Error", error_text)
    
    # ==================== BLENDING HANDLERS ====================
    
    def blend_images(self):
        """Blend the selected images."""
        if not self.app.main_image_path or not self.app.second_image_path:
            messagebox.showerror("Error", "Please select both images to blend.")
            return
        
        # Validate images
        main_valid, main_msg = self.app.blending.validate_image(self.app.main_image_path)
        second_valid, second_msg = self.app.blending.validate_image(self.app.second_image_path)
        
        if not main_valid:
            messagebox.showerror("Error", f"First image error: {main_msg}")
            return
        if not second_valid:
            messagebox.showerror("Error", f"Second image error: {second_msg}")
            return
        
        # Run blending in a separate thread
        threading.Thread(target=self._blend_images_thread, daemon=True).start()
    
    def _blend_images_thread(self):
        """Blend images in a separate thread."""
        try:
            direction = self.app.blend_direction.get()
            alpha = self.app.blend_alpha.get()
            
            result_path = self.app.blending.blend_images(
                self.app.main_image_path,
                self.app.second_image_path,
                direction,
                alpha
            )
            
            if result_path:
                self.app.root.after(0, self._blend_success, result_path)
            else:
                self.app.root.after(0, self._blend_error)
                
        except Exception as e:
            self.app.root.after(0, self._blend_error, str(e))
    
    def _blend_success(self, result_path):
        """Handle successful blending."""
        self.logger.info(f"Blending completed successfully: {result_path}")
        self.app.results_text.insert(tk.END, f"Blending completed: {result_path}\n")
        self.app.results_text.see(tk.END)
        messagebox.showinfo("Success", f"Blending completed successfully!\nSaved to: {result_path}")
    
    def _blend_error(self, error_msg=None):
        """Handle blending error."""
        error_text = f"Blending failed: {error_msg}" if error_msg else "Blending failed"
        self.logger.error(error_text)
        self.app.results_text.insert(tk.END, f"{error_text}\n")
        self.app.results_text.see(tk.END)
        messagebox.showerror("Error", error_text)
    
    # ==================== EXTRACTION HANDLERS ====================
    
    def extract_watermark(self):
        """Extract watermark from the selected images."""
        if not self.app.main_image_path or not self.app.watermark_image_path:
            messagebox.showerror("Error", "Please select both original and watermarked images.")
            return
        
        # Validate images
        main_valid, main_msg = self.app.watermarking.validate_image(self.app.main_image_path)
        watermark_valid, watermark_msg = self.app.watermarking.validate_image(self.app.watermark_image_path)
        
        if not main_valid:
            messagebox.showerror("Error", f"Original image error: {main_msg}")
            return
        if not watermark_valid:
            messagebox.showerror("Error", f"Watermarked image error: {watermark_msg}")
            return
        
        # Run extraction in a separate thread
        threading.Thread(target=self._extract_watermark_thread, daemon=True).start()
    
    def _extract_watermark_thread(self):
        """Extract watermark in a separate thread."""
        try:
            method = self.app.extraction_method.get()
            
            result_path = self.app.watermarking.extract_watermark(
                self.app.main_image_path,
                self.app.watermark_image_path,
                method
            )
            
            if result_path:
                self.app.root.after(0, self._extract_success, result_path)
            else:
                self.app.root.after(0, self._extract_error)
                
        except Exception as e:
            self.app.root.after(0, self._extract_error, str(e))
    
    def _extract_success(self, result_path):
        """Handle successful extraction."""
        self.logger.info(f"Watermark extraction completed successfully: {result_path}")
        self.app.results_text.insert(tk.END, f"Watermark extraction completed: {result_path}\n")
        self.app.results_text.see(tk.END)
        messagebox.showinfo("Success", f"Watermark extraction completed successfully!\nSaved to: {result_path}")
    
    def _extract_error(self, error_msg=None):
        """Handle extraction error."""
        error_text = f"Watermark extraction failed: {error_msg}" if error_msg else "Watermark extraction failed"
        self.logger.error(error_text)
        self.app.results_text.insert(tk.END, f"{error_text}\n")
        self.app.results_text.see(tk.END)
        messagebox.showerror("Error", error_text)
    
    # ==================== PREPROCESSING HANDLERS ====================
    
    def apply_convolution(self):
        """Apply convolution filter."""
        if not self.app.main_image_path:
            messagebox.showerror("Error", "Please select an image.")
            return
        
        threading.Thread(target=self._apply_convolution_thread, daemon=True).start()
    
    def _apply_convolution_thread(self):
        """Apply convolution in a separate thread."""
        try:
            filter_type = self.app.convolution_filter.get()
            kernel_size = self.app.kernel_size.get()
            
            result_path = self.app.advanced_processing.apply_convolution_filter(
                self.app.main_image_path, filter_type, kernel_size
            )
            
            if result_path:
                self.app.root.after(0, self._convolution_success, result_path)
            else:
                self.app.root.after(0, self._convolution_error)
                
        except Exception as e:
            self.app.root.after(0, self._convolution_error, str(e))
    
    def _convolution_success(self, result_path):
        """Handle successful convolution."""
        self.logger.info(f"Convolution completed: {result_path}")
        self.app.results_text.insert(tk.END, f"Convolution completed: {result_path}\n")
        self.app.results_text.see(tk.END)
        messagebox.showinfo("Success", f"Convolution filter applied successfully!\nSaved to: {result_path}")
    
    def _convolution_error(self, error_msg=None):
        """Handle convolution error."""
        error_text = f"Convolution failed: {error_msg}" if error_msg else "Convolution failed"
        self.logger.error(error_text)
        self.app.results_text.insert(tk.END, f"{error_text}\n")
        self.app.results_text.see(tk.END)
        messagebox.showerror("Error", error_text)
    
    def apply_histogram_operation(self):
        """Apply histogram operation."""
        if not self.app.main_image_path:
            messagebox.showerror("Error", "Please select an image.")
            return
        
        operation = self.app.histogram_operation.get()
        if operation == 'match':
            # Need reference image for matching
            ref_path = filedialog.askopenfilename(
                title="Select Reference Image",
                filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
            )
            if not ref_path:
                return
            threading.Thread(target=self._apply_histogram_matching_thread, args=(ref_path,), daemon=True).start()
        else:
            threading.Thread(target=self._apply_histogram_equalization_thread, daemon=True).start()
    
    def _apply_histogram_equalization_thread(self):
        """Apply histogram equalization in a separate thread."""
        try:
            method = self.app.histogram_method.get()
            
            result_path = self.app.advanced_processing.equalize_histogram(
                self.app.main_image_path, method
            )
            
            if result_path:
                self.app.root.after(0, self._histogram_success, result_path)
            else:
                self.app.root.after(0, self._histogram_error)
                
        except Exception as e:
            self.app.root.after(0, self._histogram_error, str(e))
    
    def _apply_histogram_matching_thread(self, ref_path):
        """Apply histogram matching in a separate thread."""
        try:
            result_path = self.app.advanced_processing.match_histogram(
                self.app.main_image_path, ref_path
            )
            
            if result_path:
                self.app.root.after(0, self._histogram_success, result_path)
            else:
                self.app.root.after(0, self._histogram_error)
                
        except Exception as e:
            self.app.root.after(0, self._histogram_error, str(e))
    
    def _histogram_success(self, result_path):
        """Handle successful histogram operation."""
        self.logger.info(f"Histogram operation completed: {result_path}")
        self.app.results_text.insert(tk.END, f"Histogram operation completed: {result_path}\n")
        self.app.results_text.see(tk.END)
        messagebox.showinfo("Success", f"Histogram operation completed successfully!\nSaved to: {result_path}")
    
    def _histogram_error(self, error_msg=None):
        """Handle histogram error."""
        error_text = f"Histogram operation failed: {error_msg}" if error_msg else "Histogram operation failed"
        self.logger.error(error_text)
        self.app.results_text.insert(tk.END, f"{error_text}\n")
        self.app.results_text.see(tk.END)
        messagebox.showerror("Error", error_text)
    
    def apply_frequency_filter(self):
        """Apply frequency domain filter."""
        if not self.app.main_image_path:
            messagebox.showerror("Error", "Please select an image.")
            return
        
        threading.Thread(target=self._apply_frequency_filter_thread, daemon=True).start()
    
    def _apply_frequency_filter_thread(self):
        """Apply frequency filter in a separate thread."""
        try:
            filter_type = self.app.frequency_filter.get()
            cutoff_freq = self.app.cutoff_freq.get()
            
            result_path = self.app.advanced_processing.apply_frequency_filter(
                self.app.main_image_path, filter_type, cutoff_freq
            )
            
            if result_path:
                self.app.root.after(0, self._frequency_success, result_path)
            else:
                self.app.root.after(0, self._frequency_error)
                
        except Exception as e:
            self.app.root.after(0, self._frequency_error, str(e))
    
    def _frequency_success(self, result_path):
        """Handle successful frequency filtering."""
        self.logger.info(f"Frequency filtering completed: {result_path}")
        self.app.results_text.insert(tk.END, f"Frequency filtering completed: {result_path}\n")
        self.app.results_text.see(tk.END)
        messagebox.showinfo("Success", f"Frequency filter applied successfully!\nSaved to: {result_path}")
    
    def _frequency_error(self, error_msg=None):
        """Handle frequency filtering error."""
        error_text = f"Frequency filtering failed: {error_msg}" if error_msg else "Frequency filtering failed"
        self.logger.error(error_text)
        self.app.results_text.insert(tk.END, f"{error_text}\n")
        self.app.results_text.see(tk.END)
        messagebox.showerror("Error", error_text)
    
    # ==================== ANALYSIS HANDLERS ====================
    
    def segment_image(self):
        """Segment image."""
        if not self.app.main_image_path:
            messagebox.showerror("Error", "Please select an image.")
            return
        
        threading.Thread(target=self._segment_image_thread, daemon=True).start()
    
    def _segment_image_thread(self):
        """Segment image in a separate thread."""
        try:
            method = self.app.segmentation_method.get()
            threshold_value = self.app.threshold_value.get()
            
            result_path = self.app.advanced_processing.segment_image(
                self.app.main_image_path, method, threshold_value
            )
            
            if result_path:
                self.app.root.after(0, self._segmentation_success, result_path)
            else:
                self.app.root.after(0, self._segmentation_error)
                
        except Exception as e:
            self.app.root.after(0, self._segmentation_error, str(e))
    
    def _segmentation_success(self, result_path):
        """Handle successful segmentation."""
        self.logger.info(f"Segmentation completed: {result_path}")
        self.app.results_text.insert(tk.END, f"Segmentation completed: {result_path}\n")
        self.app.results_text.see(tk.END)
        messagebox.showinfo("Success", f"Image segmentation completed successfully!\nSaved to: {result_path}")
    
    def _segmentation_error(self, error_msg=None):
        """Handle segmentation error."""
        error_text = f"Segmentation failed: {error_msg}" if error_msg else "Segmentation failed"
        self.logger.error(error_text)
        self.app.results_text.insert(tk.END, f"{error_text}\n")
        self.app.results_text.see(tk.END)
        messagebox.showerror("Error", error_text)
    
    def extract_descriptors(self):
        """Extract region descriptors."""
        if not self.app.main_image_path:
            messagebox.showerror("Error", "Please select an image.")
            return
        
        threading.Thread(target=self._extract_descriptors_thread, daemon=True).start()
    
    def _extract_descriptors_thread(self):
        """Extract descriptors in a separate thread."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"results/descriptors_{timestamp}.jpg"
            
            descriptors = self.app.advanced_processing.extract_region_descriptors(
                self.app.main_image_path, output_path
            )
            
            if descriptors:
                self.app.root.after(0, self._descriptors_success, descriptors, output_path)
            else:
                self.app.root.after(0, self._descriptors_error)
                
        except Exception as e:
            self.app.root.after(0, self._descriptors_error, str(e))
    
    def _descriptors_success(self, descriptors, output_path):
        """Handle successful descriptor extraction."""
        self.logger.info(f"Descriptors extracted: {output_path}")
        
        # Display results in analysis tab
        self.app.analysis_results.delete(1.0, tk.END)
        self.app.analysis_results.insert(tk.END, "Region Descriptors Analysis:\n")
        self.app.analysis_results.insert(tk.END, "=" * 40 + "\n\n")
        
        # Shape features
        self.app.analysis_results.insert(tk.END, f"Shape Features ({len(descriptors['shape_features'])} regions):\n")
        for i, feature in enumerate(descriptors['shape_features'][:5]):  # Show first 5
            self.app.analysis_results.insert(tk.END, f"Region {i+1}: Area={feature['area']:.1f}, "
                                               f"Perimeter={feature['perimeter']:.1f}, "
                                               f"Aspect Ratio={feature['aspect_ratio']:.2f}\n")
        
        # Texture features
        self.app.analysis_results.insert(tk.END, f"\nTexture Features ({len(descriptors['texture_features'])} regions):\n")
        for i, feature in enumerate(descriptors['texture_features'][:5]):  # Show first 5
            self.app.analysis_results.insert(tk.END, f"Region {i+1}: Mean={feature['mean_intensity']:.1f}, "
                                               f"Std={feature['std_intensity']:.1f}, "
                                               f"Entropy={feature['entropy']:.2f}\n")
        
        self.app.results_text.insert(tk.END, f"Descriptors extracted: {output_path}\n")
        self.app.results_text.see(tk.END)
        messagebox.showinfo("Success", f"Region descriptors extracted successfully!\nSaved to: {output_path}")
    
    def _descriptors_error(self, error_msg=None):
        """Handle descriptor extraction error."""
        error_text = f"Descriptor extraction failed: {error_msg}" if error_msg else "Descriptor extraction failed"
        self.logger.error(error_text)
        self.app.results_text.insert(tk.END, f"{error_text}\n")
        self.app.results_text.see(tk.END)
        messagebox.showerror("Error", error_text)
    
    def find_contours(self):
        """Find contours in image."""
        if not self.app.main_image_path:
            messagebox.showerror("Error", "Please select an image.")
            return
        
        threading.Thread(target=self._find_contours_thread, daemon=True).start()
    
    def _find_contours_thread(self):
        """Find contours in a separate thread."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"results/contours_{timestamp}.jpg"
            
            contour_path, contour_data = self.app.advanced_processing.find_contours(
                self.app.main_image_path, output_path
            )
            
            if contour_path and contour_data:
                self.app.root.after(0, self._contours_success, contour_data, contour_path)
            else:
                self.app.root.after(0, self._contours_error)
                
        except Exception as e:
            self.app.root.after(0, self._contours_error, str(e))
    
    def _contours_success(self, contour_data, contour_path):
        """Handle successful contour detection."""
        self.logger.info(f"Contours found: {contour_path}")
        
        # Display results in analysis tab
        self.app.analysis_results.delete(1.0, tk.END)
        self.app.analysis_results.insert(tk.END, "Contour Analysis:\n")
        self.app.analysis_results.insert(tk.END, "=" * 20 + "\n\n")
        self.app.analysis_results.insert(tk.END, f"Found {len(contour_data)} contours:\n\n")
        
        for i, contour in enumerate(contour_data[:10]):  # Show first 10
            self.app.analysis_results.insert(tk.END, f"Contour {i+1}: Area={contour['area']:.1f}, "
                                               f"Perimeter={contour['perimeter']:.1f}, "
                                               f"Points={contour['points']}\n")
        
        self.app.results_text.insert(tk.END, f"Contours found: {contour_path}\n")
        self.app.results_text.see(tk.END)
        messagebox.showinfo("Success", f"Contour detection completed successfully!\nFound {len(contour_data)} contours\nSaved to: {contour_path}")
    
    def _contours_error(self, error_msg=None):
        """Handle contour detection error."""
        error_text = f"Contour detection failed: {error_msg}" if error_msg else "Contour detection failed"
        self.logger.error(error_text)
        self.app.results_text.insert(tk.END, f"{error_text}\n")
        self.app.results_text.see(tk.END)
        messagebox.showerror("Error", error_text)
    
    # ==================== UTILITY HANDLERS ====================
    
    def clear_results(self):
        """Clear the results text."""
        self.app.results_text.delete(1.0, tk.END)
