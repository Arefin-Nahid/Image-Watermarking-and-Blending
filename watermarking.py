import cv2
import numpy as np
from PIL import Image
import os
from datetime import datetime


class Watermarking:
    
    def __init__(self):
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
    
    def visible_watermark(self, main_image_path, watermark_image_path, edge_opacity=50, output_path=None):

        try:
            # Load images
            main_img = cv2.imread(main_image_path)
            watermark_img = cv2.imread(watermark_image_path)
            
            if main_img is None or watermark_img is None:
                raise ValueError("Could not load one or both images")
            
            # Resize watermark to match main image dimensions
            watermark_resized = cv2.resize(watermark_img, (main_img.shape[1], main_img.shape[0]))
            
            # Convert to grayscale for edge detection
            watermark_gray = cv2.cvtColor(watermark_resized, cv2.COLOR_BGR2GRAY)
            
            # Apply Canny edge detection
            edges = cv2.Canny(watermark_gray, 50, 150)
            
            # Convert edges to 3-channel image
            edges_3channel = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
            
            # Normalize opacity (0-100 to 0-1)
            alpha = edge_opacity / 100.0
            
            # Apply watermark using cv2.addWeighted
            watermarked = cv2.addWeighted(main_img, 1.0, edges_3channel, alpha, 0)
            
            # Generate output path if not provided
            if output_path is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = f"watermarked_images/visible_watermark_{timestamp}.jpg"
            
            # Save the result
            cv2.imwrite(output_path, watermarked)
            
            return output_path
            
        except Exception as e:
            print(f"Error in visible watermarking: {str(e)}")
            return None
    
    def invisible_watermark(self, main_image_path, watermark_image_path, alpha=0.1, output_path=None):

        try:
            # Load images
            main_img = cv2.imread(main_image_path)
            watermark_img = cv2.imread(watermark_image_path)
            
            if main_img is None or watermark_img is None:
                raise ValueError("Could not load one or both images")
            
            # Resize watermark to match main image dimensions
            watermark_resized = cv2.resize(watermark_img, (main_img.shape[1], main_img.shape[0]))
            
            # Convert to float32 for FFT
            main_float = main_img.astype(np.float32)
            watermark_float = watermark_resized.astype(np.float32)
            
            # Split channels
            main_b, main_g, main_r = cv2.split(main_float)
            watermark_b, watermark_g, watermark_r = cv2.split(watermark_float)
            
            # Apply FFT to each channel
            main_b_fft = np.fft.fft2(main_b)
            main_g_fft = np.fft.fft2(main_g)
            main_r_fft = np.fft.fft2(main_r)
            
            watermark_b_fft = np.fft.fft2(watermark_b)
            watermark_g_fft = np.fft.fft2(watermark_g)
            watermark_r_fft = np.fft.fft2(watermark_r)
            
            # Embed watermark in frequency domain
            watermarked_b_fft = main_b_fft + alpha * watermark_b_fft
            watermarked_g_fft = main_g_fft + alpha * watermark_g_fft
            watermarked_r_fft = main_r_fft + alpha * watermark_r_fft
            
            # Apply inverse FFT
            watermarked_b = np.real(np.fft.ifft2(watermarked_b_fft))
            watermarked_g = np.real(np.fft.ifft2(watermarked_g_fft))
            watermarked_r = np.real(np.fft.ifft2(watermarked_r_fft))
            
            # Merge channels
            watermarked = cv2.merge([watermarked_b, watermarked_g, watermarked_r])
            
            # Clip values to valid range and convert back to uint8
            watermarked = np.clip(watermarked, 0, 255).astype(np.uint8)
            
            # Generate output path if not provided
            if output_path is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = f"watermarked_images/invisible_watermark_{timestamp}.jpg"
            
            # Save the result
            cv2.imwrite(output_path, watermarked)
            
            return output_path
            
        except Exception as e:
            print(f"Error in invisible watermarking: {str(e)}")
            return None
    
    def extract_watermark(self, original_image_path, watermarked_image_path, method='fourier', output_path=None):

        try:
            if method == 'fourier':
                return self._extract_fourier_watermark(original_image_path, watermarked_image_path, output_path)
            elif method == 'edge':
                return self._extract_edge_watermark(original_image_path, watermarked_image_path, output_path)
            else:
                raise ValueError("Method must be 'fourier' or 'edge'")
                
        except Exception as e:
            print(f"Error in watermark extraction: {str(e)}")
            return None
    
    def _extract_fourier_watermark(self, original_path, watermarked_path, output_path):
       
        # Load images
        original = cv2.imread(original_path)
        watermarked = cv2.imread(watermarked_path)
        
        if original is None or watermarked is None:
            raise ValueError("Could not load images")
        
        # Convert to float32
        orig_float = original.astype(np.float32)
        water_float = watermarked.astype(np.float32)
        
        # Split channels
        orig_b, orig_g, orig_r = cv2.split(orig_float)
        water_b, water_g, water_r = cv2.split(water_float)
        
        # Apply FFT
        orig_b_fft = np.fft.fft2(orig_b)
        orig_g_fft = np.fft.fft2(orig_g)
        orig_r_fft = np.fft.fft2(orig_r)
        
        water_b_fft = np.fft.fft2(water_b)
        water_g_fft = np.fft.fft2(water_g)
        water_r_fft = np.fft.fft2(water_r)
        
        # Extract watermark (difference in frequency domain)
        extracted_b_fft = water_b_fft - orig_b_fft
        extracted_g_fft = water_g_fft - orig_g_fft
        extracted_r_fft = water_r_fft - orig_r_fft
        
        # Apply inverse FFT
        extracted_b = np.real(np.fft.ifft2(extracted_b_fft))
        extracted_g = np.real(np.fft.ifft2(extracted_g_fft))
        extracted_r = np.real(np.fft.ifft2(extracted_r_fft))
        
        # Merge channels
        extracted = cv2.merge([extracted_b, extracted_g, extracted_r])
        
        # Normalize and convert to uint8
        extracted = np.clip(extracted, 0, 255).astype(np.uint8)
        
        # Generate output path if not provided
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"results/extracted_watermark_fourier_{timestamp}.jpg"
        
        # Save the result
        cv2.imwrite(output_path, extracted)
        
        return output_path
    
    def _extract_edge_watermark(self, original_path, watermarked_path, output_path):
        
        # Load images
        original = cv2.imread(original_path)
        watermarked = cv2.imread(watermarked_path)
        
        if original is None or watermarked is None:
            raise ValueError("Could not load images")
        
        # Convert to grayscale
        orig_gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
        water_gray = cv2.cvtColor(watermarked, cv2.COLOR_BGR2GRAY)
        
        # Apply Canny edge detection
        orig_edges = cv2.Canny(orig_gray, 50, 150)
        water_edges = cv2.Canny(water_gray, 50, 150)
        
        # Extract difference (watermark edges)
        extracted_edges = cv2.subtract(water_edges, orig_edges)
        
        # Generate output path if not provided
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"results/extracted_watermark_edge_{timestamp}.jpg"
        
        # Save the result
        cv2.imwrite(output_path, extracted_edges)
        
        return output_path
    
    def validate_image(self, image_path):
        if not os.path.exists(image_path):
            return False, "File does not exist"
        
        # Check file extension
        _, ext = os.path.splitext(image_path.lower())
        if ext not in self.supported_formats:
            return False, f"Unsupported format. Supported: {self.supported_formats}"
        
        # Try to load the image
        try:
            img = cv2.imread(image_path)
            if img is None:
                return False, "Could not load image"
            return True, "Valid image"
        except Exception as e:
            return False, f"Error loading image: {str(e)}"
