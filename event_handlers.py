import tkinter as tk
from tkinter import filedialog, messagebox
import os
import threading
from datetime import datetime
import logging


class EventHandlers:
    
    def __init__(self, parent_app):
        self.app = parent_app
        self.logger = logging.getLogger(__name__)

    # === FILE SELECTION ===
    
    def select_main_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Main Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
        )
        if file_path:
            self.app.main_image_path = file_path
            filename = os.path.basename(file_path)
            self.app.main_image_label.config(text=filename)
            self.logger.info(f"Main image selected: {file_path}")
            
            if hasattr(self.app, 'watermark_main_canvas'):
                self.app.root.after(100, lambda: self.app.gui_components.display_image_preview(
                    self.app.watermark_main_canvas, file_path
                ))
    
    def select_watermark_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Watermark Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
        )
        if file_path:
            self.app.watermark_image_path = file_path
            filename = os.path.basename(file_path)
            self.app.watermark_image_label.config(text=filename)
            self.logger.info(f"Watermark image selected: {file_path}")
            
            if hasattr(self.app, 'watermark_wm_canvas'):
                self.app.root.after(100, lambda: self.app.gui_components.display_image_preview(
                    self.app.watermark_wm_canvas, file_path
                ))
    
    def select_first_image(self):
        file_path = filedialog.askopenfilename(
            title="Select First Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
        )
        if file_path:
            self.app.main_image_path = file_path
            filename = os.path.basename(file_path)
            self.app.first_image_label.config(text=filename)
            self.logger.info(f"First image selected: {file_path}")
            
            if hasattr(self.app, 'blend_img1_canvas'):
                self.app.root.after(100, lambda: self.app.gui_components.display_image_preview(
                    self.app.blend_img1_canvas, file_path
                ))
    
    def select_second_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Second Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
        )
        if file_path:
            self.app.second_image_path = file_path
            filename = os.path.basename(file_path)
            self.app.second_image_label.config(text=filename)
            self.logger.info(f"Second image selected: {file_path}")
            
            if hasattr(self.app, 'blend_img2_canvas'):
                self.app.root.after(100, lambda: self.app.gui_components.display_image_preview(
                    self.app.blend_img2_canvas, file_path
                ))
    
    def select_original_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Original Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
        )
        if file_path:
            self.app.main_image_path = file_path
            filename = os.path.basename(file_path)
            self.app.original_image_label.config(text=filename)
            self.logger.info(f"Original image selected: {file_path}")
            
            if hasattr(self.app, 'extract_orig_canvas'):
                self.app.root.after(100, lambda: self.app.gui_components.display_image_preview(
                    self.app.extract_orig_canvas, file_path
                ))
    
    def select_watermarked_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Watermarked Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
        )
        if file_path:
            self.app.watermark_image_path = file_path
            filename = os.path.basename(file_path)
            self.app.watermarked_image_label.config(text=filename)
            self.logger.info(f"Watermarked image selected: {file_path}")
            
            if hasattr(self.app, 'extract_water_canvas'):
                self.app.root.after(100, lambda: self.app.gui_components.display_image_preview(
                    self.app.extract_water_canvas, file_path
                ))

    # === PARAMETER UPDATES ===
    
    def update_edge_opacity_label(self, value):
        self.app.edge_opacity_label.config(text=str(int(float(value))))
    
    def update_watermark_alpha_label(self, value):
        self.app.watermark_alpha_label.config(text=f"{float(value):.2f}")
    
    def update_blend_alpha_label(self, value):
        self.app.blend_alpha_label.config(text=f"{float(value):.2f}")

    # === WATERMARKING ===
    
    def apply_watermark(self):
        if not self.app.main_image_path or not self.app.watermark_image_path:
            messagebox.showerror("Error", "Please select both main and watermark images.")
            return
        
        main_valid, main_msg = self.app.watermarking.validate_image(self.app.main_image_path)
        watermark_valid, watermark_msg = self.app.watermarking.validate_image(self.app.watermark_image_path)
        
        if not main_valid:
            messagebox.showerror("Error", f"Main image error: {main_msg}")
            return
        if not watermark_valid:
            messagebox.showerror("Error", f"Watermark image error: {watermark_msg}")
            return
        
        if hasattr(self.app, 'watermark_status'):
            self.app.watermark_status.config(text="Processing...", 
                                            fg=self.app.gui_components.colors['warning'])
        
        threading.Thread(target=self._apply_watermark_thread, daemon=True).start()
    
    def _apply_watermark_thread(self):
        try:
            watermark_type = self.app.watermark_type.get()
            
            if watermark_type == 'visible':
                edge_opacity = self.app.edge_opacity.get()
                result_path = self.app.watermarking.visible_watermark(
                    self.app.main_image_path, 
                    self.app.watermark_image_path, 
                    edge_opacity
                )
            else:
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
        self.logger.info(f"Watermarking completed: {result_path}")
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.app.results_text.insert(tk.END, 
            f"[{timestamp}] SUCCESS: Watermarking completed\n")
        self.app.results_text.insert(tk.END, f"  Output: {result_path}\n\n")
        self.app.results_text.see(tk.END)
        
        if hasattr(self.app, 'watermark_result_canvas'):
            self.app.gui_components.display_image_preview(
                self.app.watermark_result_canvas, 
                result_path
            )
        
        if hasattr(self.app, 'watermark_status'):
            self.app.watermark_status.config(text="Watermark applied successfully", 
                                            fg=self.app.gui_components.colors['success'])
        
        messagebox.showinfo("Success", 
            f"Watermarking completed successfully!\n\nSaved to:\n{result_path}")
    
    def _watermark_error(self, error_msg=None):
        error_text = f"Watermarking failed: {error_msg}" if error_msg else "Watermarking failed"
        self.logger.error(error_text)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.app.results_text.insert(tk.END, f"[{timestamp}] ERROR: {error_text}\n\n")
        self.app.results_text.see(tk.END)
        
        if hasattr(self.app, 'watermark_status'):
            self.app.watermark_status.config(text="Failed to apply watermark", 
                                            fg=self.app.gui_components.colors['danger'])
        
        messagebox.showerror("Error", error_text)

    # === IMAGE BLENDING ===
    
    def blend_images(self):
        if not self.app.main_image_path or not self.app.second_image_path:
            messagebox.showerror("Error", "Please select both images to blend.")
            return
        
        if hasattr(self.app, 'blending_status'):
            self.app.blending_status.config(text="Blending images...", 
                                           fg=self.app.gui_components.colors['warning'])
        
        threading.Thread(target=self._blend_images_thread, daemon=True).start()
    
    def _blend_images_thread(self):
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
        self.logger.info(f"Blending completed: {result_path}")
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.app.results_text.insert(tk.END, 
            f"[{timestamp}] SUCCESS: Image blending completed\n")
        self.app.results_text.insert(tk.END, f"  Output: {result_path}\n\n")
        self.app.results_text.see(tk.END)
        
        if hasattr(self.app, 'blend_result_canvas'):
            self.app.gui_components.display_image_preview(
                self.app.blend_result_canvas, 
                result_path
            )
        
        if hasattr(self.app, 'blending_status'):
            self.app.blending_status.config(text="Images blended successfully", 
                                           fg=self.app.gui_components.colors['success'])
        
        messagebox.showinfo("Success", 
            f"Image blending completed successfully!\n\nSaved to:\n{result_path}")
    
    def _blend_error(self, error_msg=None):
        error_text = f"Blending failed: {error_msg}" if error_msg else "Blending failed"
        self.logger.error(error_text)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.app.results_text.insert(tk.END, f"[{timestamp}] ERROR: {error_text}\n\n")
        self.app.results_text.see(tk.END)
        
        if hasattr(self.app, 'blending_status'):
            self.app.blending_status.config(text="Failed to blend images", 
                                           fg=self.app.gui_components.colors['danger'])
        
        messagebox.showerror("Error", error_text)

    # === WATERMARK EXTRACTION ===
    
    def extract_watermark(self):
        if not self.app.main_image_path or not self.app.watermark_image_path:
            messagebox.showerror("Error", "Please select both original and watermarked images.")
            return
        
        if hasattr(self.app, 'extraction_status'):
            self.app.extraction_status.config(text="Extracting watermark...", 
                                             fg=self.app.gui_components.colors['warning'])
        
        threading.Thread(target=self._extract_watermark_thread, daemon=True).start()
    
    def _extract_watermark_thread(self):
        try:
            method = self.app.extraction_method.get()
            
            result_path = self.app.watermarking.extract_watermark(
                self.app.main_image_path,
                self.app.watermark_image_path,
                method
            )
            
            if result_path:
                self.app.root.after(0, self._extraction_success, result_path)
            else:
                self.app.root.after(0, self._extraction_error)
                
        except Exception as e:
            self.app.root.after(0, self._extraction_error, str(e))
    
    def _extraction_success(self, result_path):
        self.logger.info(f"Extraction completed: {result_path}")
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.app.results_text.insert(tk.END, 
            f"[{timestamp}] SUCCESS: Watermark extraction completed\n")
        self.app.results_text.insert(tk.END, f"  Output: {result_path}\n\n")
        self.app.results_text.see(tk.END)
        
        if hasattr(self.app, 'extract_result_canvas'):
            self.app.gui_components.display_image_preview(
                self.app.extract_result_canvas, 
                result_path
            )
        
        if hasattr(self.app, 'extraction_status'):
            self.app.extraction_status.config(text="Watermark extracted successfully", 
                                             fg=self.app.gui_components.colors['success'])
        
        messagebox.showinfo("Success", 
            f"Watermark extraction completed successfully!\n\nSaved to:\n{result_path}")
    
    def _extraction_error(self, error_msg=None):
        error_text = f"Extraction failed: {error_msg}" if error_msg else "Extraction failed"
        self.logger.error(error_text)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.app.results_text.insert(tk.END, f"[{timestamp}] ERROR: {error_text}\n\n")
        self.app.results_text.see(tk.END)
        
        if hasattr(self.app, 'extraction_status'):
            self.app.extraction_status.config(text="Failed to extract watermark", 
                                             fg=self.app.gui_components.colors['danger'])
        
        messagebox.showerror("Error", error_text)
    
    def clear_results(self):
        self.app.results_text.delete(1.0, tk.END)
        self.logger.info("Results cleared")
        
        self.app.results_text.insert(tk.END, "Image Processing Application\n")
        self.app.results_text.insert(tk.END, "=" * 60 + "\n\n")
        self.app.results_text.insert(tk.END, "Ready to process images.\n\n")