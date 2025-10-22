import os
import logging
from datetime import datetime


class AppUtils:
    @staticmethod
    def setup_logging():
        """Setup logging for the application."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/app.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
    
    @staticmethod
    def create_directories():
        """Create necessary directories for the application."""
        directories = ['images', 'watermarked_images', 'blended_images', 'logs', 'results']
        
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)
                logging.info(f"Created directory: {directory}")
    
    @staticmethod
    def validate_image_path(image_path):
        """Validate if the image path exists and is readable."""
        if not image_path:
            return False, "No image path provided"
        
        if not os.path.exists(image_path):
            return False, "File does not exist"
        
        # Check file extension
        _, ext = os.path.splitext(image_path.lower())
        supported_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
        
        if ext not in supported_formats:
            return False, f"Unsupported format. Supported: {supported_formats}"
        
        return True, "Valid image"
    
    @staticmethod
    def get_timestamp():
        """Get current timestamp in format YYYYMMDD_HHMMSS."""
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    @staticmethod
    def format_file_size(size_bytes):
        """Format file size in human readable format."""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f} {size_names[i]}"
    
    @staticmethod
    def get_image_info(image_path):
        """Get basic information about an image file."""
        if not os.path.exists(image_path):
            return None
        
        try:
            stat = os.stat(image_path)
            return {
                'name': os.path.basename(image_path),
                'size': stat.st_size,
                'size_formatted': AppUtils.format_file_size(stat.st_size),
                'created': datetime.fromtimestamp(stat.st_ctime),
                'modified': datetime.fromtimestamp(stat.st_mtime),
                'path': image_path
            }
        except Exception as e:
            logging.error(f"Error getting image info: {str(e)}")
            return None
    
    @staticmethod
    def safe_filename(filename):
        """Create a safe filename by removing invalid characters."""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename
    
    @staticmethod
    def ensure_directory_exists(file_path):
        """Ensure the directory for a file path exists."""
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            logging.info(f"Created directory: {directory}")
    
    @staticmethod
    def log_operation(operation_name, success, result_path=None, error_msg=None):
        """Log operation results."""
        if success:
            logging.info(f"{operation_name} completed successfully: {result_path}")
        else:
            logging.error(f"{operation_name} failed: {error_msg}")
    
    @staticmethod
    def validate_parameters(params_dict):
        """Validate a dictionary of parameters."""
        for param_name, param_value in params_dict.items():
            if param_value is None:
                return False, f"Parameter {param_name} is None"
            if isinstance(param_value, str) and not param_value.strip():
                return False, f"Parameter {param_name} is empty"
        return True, "All parameters valid"
    
    @staticmethod
    def get_supported_image_formats():
        """Get list of supported image formats."""
        return ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
    
    @staticmethod
    def get_file_dialog_filters():
        """Get file dialog filters for image files."""
        return [("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff"), ("All files", "*.*")]
    
    @staticmethod
    def truncate_text(text, max_length=50):
        """Truncate text to specified length with ellipsis."""
        if len(text) <= max_length:
            return text
        return text[:max_length-3] + "..."
    
    @staticmethod
    def format_float(value, decimals=2):
        """Format float value to specified decimal places."""
        return f"{float(value):.{decimals}f}"
    
    @staticmethod
    def format_int(value):
        """Format integer value."""
        return str(int(float(value)))
    
    @staticmethod
    def get_operation_status_message(operation, success, result_path=None, error_msg=None):
        """Get formatted status message for operations."""
        if success:
            return f"{operation} completed successfully!\nSaved to: {result_path}"
        else:
            return f"{operation} failed: {error_msg}" if error_msg else f"{operation} failed"
    
    @staticmethod
    def create_result_filename(operation_type, timestamp=None):
        """Create standardized result filename."""
        if timestamp is None:
            timestamp = AppUtils.get_timestamp()
        
        return f"{operation_type}_{timestamp}.jpg"
    
    @staticmethod
    def get_operation_types():
        """Get list of available operation types."""
        return [
            'watermarking',
            'blending', 
            'extraction',
            'convolution',
            'histogram',
            'frequency',
            'segmentation',
            'descriptors',
            'contours'
        ]
    
    @staticmethod
    def get_default_parameters():
        """Get default parameters for the application."""
        return {
            'edge_opacity': 50,
            'watermark_alpha': 0.1,
            'blend_alpha': 0.5,
            'kernel_size': 5,
            'cutoff_freq': 30,
            'threshold_value': 127
        }
    
    @staticmethod
    def validate_parameter_range(value, min_val, max_val, param_name):
        """Validate parameter is within specified range."""
        try:
            num_value = float(value)
            if min_val <= num_value <= max_val:
                return True, "Valid"
            else:
                return False, f"{param_name} must be between {min_val} and {max_val}"
        except (ValueError, TypeError):
            return False, f"{param_name} must be a number"
    
    @staticmethod
    def get_parameter_ranges():
        """Get valid ranges for all parameters."""
        return {
            'edge_opacity': (0, 100),
            'watermark_alpha': (0.0, 1.0),
            'blend_alpha': (0.0, 1.0),
            'kernel_size': (3, 15),
            'cutoff_freq': (10, 100),
            'threshold_value': (0, 255)
        }
