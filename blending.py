import cv2
import numpy as np
from datetime import datetime
import os


class ImageBlending:
    
    def __init__(self):
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
    
    def create_gradient_mask(self, height, width, direction='horizontal', alpha=0.5):

        mask = np.zeros((height, width), dtype=np.float32)
        
        if direction == 'horizontal':
            # Left to right gradient
            for i in range(width):
                mask[:, i] = i / (width - 1)
                
        elif direction == 'vertical':
            # Top to bottom gradient
            for i in range(height):
                mask[i, :] = i / (height - 1)
                
        elif direction == 'diagonal':
            # Diagonal gradient (top-left to bottom-right)
            for i in range(height):
                for j in range(width):
                    mask[i, j] = (i + j) / (height + width - 2)
        
        # Apply alpha scaling
        mask = mask * alpha
        
        return mask
    
    def blend_images(self, image1_path, image2_path, direction='horizontal', alpha=0.5, output_path=None):

        try:
            # Load images
            img1 = cv2.imread(image1_path)
            img2 = cv2.imread(image2_path)
            
            if img1 is None or img2 is None:
                raise ValueError("Could not load one or both images")
            
            # Resize images to the same dimensions (use the smaller dimensions)
            h1, w1 = img1.shape[:2]
            h2, w2 = img2.shape[:2]
            
            target_height = min(h1, h2)
            target_width = min(w1, w2)
            
            img1_resized = cv2.resize(img1, (target_width, target_height))
            img2_resized = cv2.resize(img2, (target_width, target_height))
            
            # Create gradient mask
            mask = self.create_gradient_mask(target_height, target_width, direction, alpha)
            
            # Convert mask to 3-channel
            mask_3channel = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
            
            # Apply blending
            # For each pixel: result = img1 * (1 - mask) + img2 * mask
            blended = img1_resized.astype(np.float32) * (1 - mask_3channel) + img2_resized.astype(np.float32) * mask_3channel
            
            # Convert back to uint8
            blended = np.clip(blended, 0, 255).astype(np.uint8)
            
            # Generate output path if not provided
            if output_path is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = f"blended_images/blended_{direction}_{timestamp}.jpg"
            
            # Save the result
            cv2.imwrite(output_path, blended)
            
            return output_path
            
        except Exception as e:
            print(f"Error in image blending: {str(e)}")
            return None
    
    def advanced_blend(self, image1_path, image2_path, blend_type='linear', alpha=0.5, output_path=None):

        try:
            # Load images
            img1 = cv2.imread(image1_path)
            img2 = cv2.imread(image2_path)
            
            if img1 is None or img2 is None:
                raise ValueError("Could not load one or both images")
            
            # Resize images to the same dimensions
            h1, w1 = img1.shape[:2]
            h2, w2 = img2.shape[:2]
            
            target_height = min(h1, h2)
            target_width = min(w1, w2)
            
            img1_resized = cv2.resize(img1, (target_width, target_height))
            img2_resized = cv2.resize(img2, (target_width, target_height))
            
            # Create advanced gradient mask
            mask = self._create_advanced_mask(target_height, target_width, blend_type, alpha)
            
            # Convert mask to 3-channel
            mask_3channel = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
            
            # Apply blending
            blended = img1_resized.astype(np.float32) * (1 - mask_3channel) + img2_resized.astype(np.float32) * mask_3channel
            
            # Convert back to uint8
            blended = np.clip(blended, 0, 255).astype(np.uint8)
            
            # Generate output path if not provided
            if output_path is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = f"blended_images/advanced_blend_{blend_type}_{timestamp}.jpg"
            
            # Save the result
            cv2.imwrite(output_path, blended)
            
            return output_path
            
        except Exception as e:
            print(f"Error in advanced blending: {str(e)}")
            return None
    
    def _create_advanced_mask(self, height, width, blend_type, alpha):
        mask = np.zeros((height, width), dtype=np.float32)
        
        if blend_type == 'linear':
            # Linear gradient (same as basic horizontal)
            for i in range(width):
                mask[:, i] = i / (width - 1)
                
        elif blend_type == 'sigmoid':
            # Sigmoid gradient for smoother transitions
            for i in range(width):
                x = (i / (width - 1)) * 10 - 5  # Scale to [-5, 5]
                mask[:, i] = 1 / (1 + np.exp(-x))
                
        elif blend_type == 'cosine':
            # Cosine gradient for smooth transitions
            for i in range(width):
                mask[:, i] = (1 - np.cos(np.pi * i / (width - 1))) / 2
        
        # Apply alpha scaling
        mask = mask * alpha
        
        return mask
    
    def create_custom_mask(self, height, width, mask_points, output_path=None):

        try:
            # Create base mask
            mask = np.zeros((height, width), dtype=np.float32)
            
            # Apply custom points (simplified implementation)
            for x, y, value in mask_points:
                if 0 <= x < width and 0 <= y < height:
                    mask[y, x] = value

            # Generate output path if not provided
            if output_path is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = f"results/custom_mask_{timestamp}.jpg"
            
            # Save the mask
            mask_uint8 = (mask * 255).astype(np.uint8)
            cv2.imwrite(output_path, mask_uint8)
            
            return mask, output_path
            
        except Exception as e:
            print(f"Error creating custom mask: {str(e)}")
            return None, None
    
    def validate_image(self, image_path):
        """Validate if the image file is supported and readable."""
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
