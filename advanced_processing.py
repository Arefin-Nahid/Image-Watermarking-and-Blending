import cv2
import numpy as np
from PIL import Image
import os
from datetime import datetime
import logging


class AdvancedImageProcessing:
    
    def __init__(self):
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
        self.logger = logging.getLogger(__name__)
    
    # CONVOLUTION OPERATIONS 
    
    def apply_convolution_filter(self, image_path, filter_type='gaussian', kernel_size=5, output_path=None):

        try:
            # Load image
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError("Could not load image")
            
            # Ensure kernel size is odd
            if kernel_size % 2 == 0:
                kernel_size += 1
            
            # Define kernels
            kernels = self._get_convolution_kernels(kernel_size)
            
            if filter_type not in kernels:
                raise ValueError(f"Unsupported filter type: {filter_type}")
            
            kernel = kernels[filter_type]
            
            # Apply convolution
            if filter_type in ['gaussian', 'sharpen', 'edge_detect']:
                filtered_img = cv2.filter2D(img, -1, kernel)
            elif filter_type in ['sobel_x', 'sobel_y']:
                # Convert to grayscale for Sobel
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                filtered = cv2.filter2D(gray, -1, kernel)
                filtered_img = cv2.cvtColor(filtered, cv2.COLOR_GRAY2BGR)
            elif filter_type == 'laplacian':
                # Convert to grayscale for Laplacian
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                filtered = cv2.filter2D(gray, -1, kernel)
                filtered_img = cv2.cvtColor(filtered, cv2.COLOR_GRAY2BGR)
            
            # Generate output path if not provided
            if output_path is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = f"results/convolution_{filter_type}_{timestamp}.jpg"
            
            # Save result
            cv2.imwrite(output_path, filtered_img)
            self.logger.info(f"Convolution filter applied: {filter_type}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error in convolution filtering: {str(e)}")
            return None
    
    def _get_convolution_kernels(self, kernel_size):
        """Get predefined convolution kernels."""
        kernels = {}
        
        # Gaussian kernel
        kernels['gaussian'] = cv2.getGaussianKernel(kernel_size, 0)
        kernels['gaussian'] = np.outer(kernels['gaussian'], kernels['gaussian'])
        
        # Sobel kernels
        kernels['sobel_x'] = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float32)
        kernels['sobel_y'] = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=np.float32)
        
        # Laplacian kernel
        kernels['laplacian'] = np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]], dtype=np.float32)
        
        # Sharpen kernel
        kernels['sharpen'] = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], dtype=np.float32)
        
        # Edge detection kernel
        kernels['edge_detect'] = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]], dtype=np.float32)
        
        return kernels
    
    #  IMAGE SEGMENTATION 
    
    def segment_image(self, image_path, method='edge', threshold_value=127, output_path=None):

        try:
            # Load image
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError("Could not load image")
            
            # Convert to grayscale for segmentation
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            if method == 'edge':
                # Canny edge detection
                edges = cv2.Canny(gray, 50, 150)
                segmented = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
                
            elif method == 'threshold':
                # Simple thresholding
                _, thresh = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)
                segmented = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
                
            elif method == 'otsu':
                # Otsu's thresholding
                _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                segmented = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
                
            elif method == 'adaptive':
                # Adaptive thresholding
                thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
                segmented = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
            
            # Generate output path if not provided
            if output_path is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = f"results/segmentation_{method}_{timestamp}.jpg"
            
            # Save result
            cv2.imwrite(output_path, segmented)
            self.logger.info(f"Image segmentation completed: {method}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error in image segmentation: {str(e)}")
            return None
    
    def find_contours(self, image_path, output_path=None):

        try:
            # Load image
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError("Could not load image")
            
            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Apply threshold
            _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            
            # Find contours
            contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Draw contours
            contour_img = img.copy()
            cv2.drawContours(contour_img, contours, -1, (0, 255, 0), 2)
            
            # Generate output path if not provided
            if output_path is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = f"results/contours_{timestamp}.jpg"
            
            # Save result
            cv2.imwrite(output_path, contour_img)
            
            # Prepare contour data
            contour_data = []
            for i, contour in enumerate(contours):
                area = cv2.contourArea(contour)
                perimeter = cv2.arcLength(contour, True)
                if area > 100:  # Filter small contours
                    contour_data.append({
                        'id': i,
                        'area': area,
                        'perimeter': perimeter,
                        'points': len(contour)
                    })
            
            self.logger.info(f"Found {len(contour_data)} contours")
            return output_path, contour_data
            
        except Exception as e:
            self.logger.error(f"Error in contour detection: {str(e)}")
            return None, None
    
    #  HISTOGRAM OPERATIONS 
    
    def equalize_histogram(self, image_path, method='global', output_path=None):

        try:
            # Load image
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError("Could not load image")
            
            if method == 'global':
                # Global histogram equalization
                # Convert to YUV for better color preservation
                yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
                yuv[:, :, 0] = cv2.equalizeHist(yuv[:, :, 0])
                equalized = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)
                
            elif method == 'clahe':
                # CLAHE (Contrast Limited Adaptive Histogram Equalization)
                lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
                clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
                lab[:, :, 0] = clahe.apply(lab[:, :, 0])
                equalized = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
            
            # Generate output path if not provided
            if output_path is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = f"results/histogram_equalized_{method}_{timestamp}.jpg"
            
            # Save result
            cv2.imwrite(output_path, equalized)
            self.logger.info(f"Histogram equalization completed: {method}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error in histogram equalization: {str(e)}")
            return None
    
    def match_histogram(self, source_path, reference_path, output_path=None):

        try:
            # Load images
            source = cv2.imread(source_path)
            reference = cv2.imread(reference_path)
            
            if source is None or reference is None:
                raise ValueError("Could not load one or both images")
            
            # Resize reference to match source dimensions
            reference = cv2.resize(reference, (source.shape[1], source.shape[0]))
            
            # Convert to LAB color space
            source_lab = cv2.cvtColor(source, cv2.COLOR_BGR2LAB)
            reference_lab = cv2.cvtColor(reference, cv2.COLOR_BGR2LAB)
            
            # Match histograms for each channel
            matched_lab = source_lab.copy()
            for i in range(3):
                matched_lab[:, :, i] = self._match_channel_histogram(
                    source_lab[:, :, i], reference_lab[:, :, i]
                )
            
            # Convert back to BGR
            matched = cv2.cvtColor(matched_lab, cv2.COLOR_LAB2BGR)
            
            # Generate output path if not provided
            if output_path is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = f"results/histogram_matched_{timestamp}.jpg"
            
            # Save result
            cv2.imwrite(output_path, matched)
            self.logger.info("Histogram matching completed")
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error in histogram matching: {str(e)}")
            return None
    
    def _match_channel_histogram(self, source, reference):
        """Match histogram of a single channel."""
        # Calculate histograms
        source_hist, _ = np.histogram(source.flatten(), 256, [0, 256])
        reference_hist, _ = np.histogram(reference.flatten(), 256, [0, 256])
        
        # Calculate cumulative distributions
        source_cdf = source_hist.cumsum()
        reference_cdf = reference_hist.cumsum()
        
        # Normalize
        source_cdf = source_cdf / source_cdf[-1]
        reference_cdf = reference_cdf / reference_cdf[-1]
        
        # Create mapping
        mapping = np.zeros(256, dtype=np.uint8)
        for i in range(256):
            # Find closest reference value
            diff = np.abs(reference_cdf - source_cdf[i])
            mapping[i] = np.argmin(diff)
        
        # Apply mapping
        return mapping[source]
    
    def calculate_histogram(self, image_path):

        try:
            # Load image
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError("Could not load image")
            
            # Calculate histograms for each channel
            hist_data = {}
            colors = ['blue', 'green', 'red']
            
            for i, color in enumerate(colors):
                hist = cv2.calcHist([img], [i], None, [256], [0, 256])
                hist_data[color] = hist.flatten()
            
            # Calculate statistics
            hist_data['statistics'] = {
                'mean': np.mean(img),
                'std': np.std(img),
                'min': np.min(img),
                'max': np.max(img)
            }
            
            return hist_data
            
        except Exception as e:
            self.logger.error(f"Error calculating histogram: {str(e)}")
            return None
    
    # FREQUENCY DOMAIN FILTERING 
    
    def apply_frequency_filter(self, image_path, filter_type='lowpass', cutoff_freq=30, output_path=None):

        try:
            # Load image
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError("Could not load image")
            
            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Apply DFT
            dft = cv2.dft(np.float32(gray), flags=cv2.DFT_COMPLEX_OUTPUT)
            dft_shift = np.fft.fftshift(dft)
            
            # Create frequency filter
            rows, cols = gray.shape
            crow, ccol = rows // 2, cols // 2
            
            # Create mask
            mask = np.zeros((rows, cols, 2), np.float32)
            
            if filter_type == 'lowpass':
                # Low-pass filter
                y, x = np.ogrid[:rows, :cols]
                mask = np.sqrt((x - ccol)**2 + (y - crow)**2) <= cutoff_freq
                mask = np.stack([mask, mask], axis=2)
                
            elif filter_type == 'highpass':
                # High-pass filter
                y, x = np.ogrid[:rows, :cols]
                mask = np.sqrt((x - ccol)**2 + (y - crow)**2) > cutoff_freq
                mask = np.stack([mask, mask], axis=2)
                
            elif filter_type == 'bandpass':
                # Band-pass filter
                y, x = np.ogrid[:rows, :cols]
                dist = np.sqrt((x - ccol)**2 + (y - crow)**2)
                mask = (dist >= cutoff_freq - 10) & (dist <= cutoff_freq + 10)
                mask = np.stack([mask, mask], axis=2)
            
            # Apply filter
            fshift = dft_shift * mask
            
            # Apply inverse DFT
            f_ishift = np.fft.ifftshift(fshift)
            img_back = cv2.idft(f_ishift)
            img_back = cv2.magnitude(img_back[:, :, 0], img_back[:, :, 1])
            
            # Normalize
            img_back = cv2.normalize(img_back, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
            
            # Convert back to 3-channel
            filtered_img = cv2.cvtColor(img_back, cv2.COLOR_GRAY2BGR)
            
            # Generate output path if not provided
            if output_path is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = f"results/frequency_filtered_{filter_type}_{timestamp}.jpg"
            
            # Save result
            cv2.imwrite(output_path, filtered_img)
            self.logger.info(f"Frequency filtering completed: {filter_type}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error in frequency filtering: {str(e)}")
            return None
    
    # REGION DESCRIPTORS 
    
    def extract_region_descriptors(self, image_path, output_path=None):

        try:
            # Load image
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError("Could not load image")
            
            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Find contours
            _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            descriptors = {
                'shape_features': [],
                'texture_features': [],
                'statistical_features': []
            }
            
            # Analyze each contour
            for i, contour in enumerate(contours):
                if cv2.contourArea(contour) < 100:  # Skip small contours
                    continue
                
                # Shape features
                area = cv2.contourArea(contour)
                perimeter = cv2.arcLength(contour, True)
                if perimeter == 0:
                    continue
                
                # Hu moments
                moments = cv2.moments(contour)
                hu_moments = cv2.HuMoments(moments).flatten()
                
                # Bounding rectangle
                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = float(w) / h
                
                # Convex hull
                hull = cv2.convexHull(contour)
                hull_area = cv2.contourArea(hull)
                solidity = float(area) / hull_area if hull_area > 0 else 0
                
                # Shape features
                shape_features = {
                    'contour_id': i,
                    'area': area,
                    'perimeter': perimeter,
                    'aspect_ratio': aspect_ratio,
                    'solidity': solidity,
                    'hu_moments': hu_moments.tolist()
                }
                descriptors['shape_features'].append(shape_features)
                
                # Texture features (using LBP-like approach)
                mask = np.zeros(gray.shape, np.uint8)
                cv2.drawContours(mask, [contour], -1, 255, -1)
                
                # Calculate texture features within the contour
                mean_val = cv2.mean(gray, mask)[0]
                std_val = cv2.meanStdDev(gray, mask)[1][0][0]
                
                texture_features = {
                    'contour_id': i,
                    'mean_intensity': mean_val,
                    'std_intensity': std_val,
                    'energy': np.sum(gray[mask > 0] ** 2),
                    'entropy': self._calculate_entropy(gray, mask)
                }
                descriptors['texture_features'].append(texture_features)
                
                # Statistical features
                contour_pixels = gray[mask > 0]
                if len(contour_pixels) > 0:
                    statistical_features = {
                        'contour_id': i,
                        'mean': np.mean(contour_pixels),
                        'std': np.std(contour_pixels),
                        'min': np.min(contour_pixels),
                        'max': np.max(contour_pixels),
                        'median': np.median(contour_pixels),
                        'skewness': self._calculate_skewness(contour_pixels),
                        'kurtosis': self._calculate_kurtosis(contour_pixels)
                    }
                    descriptors['statistical_features'].append(statistical_features)
            
            # Create visualization
            if output_path:
                vis_img = img.copy()
                for i, contour in enumerate(contours):
                    if cv2.contourArea(contour) >= 100:
                        cv2.drawContours(vis_img, [contour], -1, (0, 255, 0), 2)
                        # Add contour ID
                        M = cv2.moments(contour)
                        if M['m00'] != 0:
                            cx = int(M['m10'] / M['m00'])
                            cy = int(M['m01'] / M['m00'])
                            cv2.putText(vis_img, str(i), (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
                
                cv2.imwrite(output_path, vis_img)
            
            self.logger.info(f"Extracted descriptors for {len(descriptors['shape_features'])} regions")
            return descriptors
            
        except Exception as e:
            self.logger.error(f"Error extracting region descriptors: {str(e)}")
            return None
    
    def _calculate_entropy(self, image, mask):
        """Calculate entropy of image region."""
        pixels = image[mask > 0]
        if len(pixels) == 0:
            return 0
        
        hist, _ = np.histogram(pixels, bins=256, range=(0, 256))
        hist = hist / hist.sum()
        hist = hist[hist > 0]  # Remove zero probabilities
        return -np.sum(hist * np.log2(hist))
    
    def _calculate_skewness(self, data):
        """Calculate skewness of data."""
        if len(data) == 0:
            return 0
        mean = np.mean(data)
        std = np.std(data)
        if std == 0:
            return 0
        return np.mean(((data - mean) / std) ** 3)
    
    def _calculate_kurtosis(self, data):
        """Calculate kurtosis of data."""
        if len(data) == 0:
            return 0
        mean = np.mean(data)
        std = np.std(data)
        if std == 0:
            return 0
        return np.mean(((data - mean) / std) ** 4) - 3
    
    # UTILITY FUNCTIONS 
    
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
    
    def get_image_info(self, image_path):
        """Get detailed information about an image."""
        try:
            img = cv2.imread(image_path)
            if img is None:
                return None
            
            info = {
                'dimensions': img.shape,
                'height': img.shape[0],
                'width': img.shape[1],
                'channels': img.shape[2] if len(img.shape) == 3 else 1,
                'dtype': str(img.dtype),
                'size_bytes': img.nbytes,
                'mean_intensity': np.mean(img),
                'std_intensity': np.std(img)
            }
            
            return info
            
        except Exception as e:
            self.logger.error(f"Error getting image info: {str(e)}")
            return None
