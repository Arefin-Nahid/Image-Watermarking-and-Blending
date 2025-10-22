"""
File management utilities for the Image Processing application.
"""

import os
import shutil
from datetime import datetime
import logging


class FileManager:
    """Class for managing files and directories in the application."""
    
    def __init__(self):
        self.base_dirs = {
            'images': 'images',
            'watermarked': 'watermarked_images',
            'blended': 'blended_images',
            'results': 'results',
            'logs': 'logs'
        }
        
        # Create directories if they don't exist
        self.create_directories()
    
    def create_directories(self):
        """Create necessary directories for the application."""
        for dir_name, dir_path in self.base_dirs.items():
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
                logging.info(f"Created directory: {dir_path}")
    
    def organize_result(self, file_path, operation_type, timestamp=None):
        """
        Organize result files into appropriate directories.
        
        Args:
            file_path (str): Path to the result file
            operation_type (str): Type of operation ('watermark', 'blend', 'extract')
            timestamp (str): Timestamp for organization
            
        Returns:
            str: New organized path
        """
        if timestamp is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        filename = os.path.basename(file_path)
        name, ext = os.path.splitext(filename)
        
        if operation_type == 'watermark':
            target_dir = self.base_dirs['watermarked']
        elif operation_type == 'blend':
            target_dir = self.base_dirs['blended']
        elif operation_type == 'extract':
            target_dir = self.base_dirs['results']
        else:
            target_dir = self.base_dirs['results']
        
        # Create organized filename
        organized_filename = f"{operation_type}_{timestamp}_{name}{ext}"
        organized_path = os.path.join(target_dir, organized_filename)
        
        # Copy file to organized location
        try:
            shutil.copy2(file_path, organized_path)
            logging.info(f"Organized file: {file_path} -> {organized_path}")
            return organized_path
        except Exception as e:
            logging.error(f"Error organizing file: {str(e)}")
            return file_path
    
    def cleanup_old_files(self, days=30):
        """
        Clean up old files from result directories.
        
        Args:
            days (int): Number of days to keep files
        """
        current_time = datetime.now().timestamp()
        cutoff_time = current_time - (days * 24 * 60 * 60)
        
        for dir_name, dir_path in self.base_dirs.items():
            if os.path.exists(dir_path):
                for filename in os.listdir(dir_path):
                    file_path = os.path.join(dir_path, filename)
                    if os.path.isfile(file_path):
                        file_time = os.path.getmtime(file_path)
                        if file_time < cutoff_time:
                            try:
                                os.remove(file_path)
                                logging.info(f"Cleaned up old file: {file_path}")
                            except Exception as e:
                                logging.error(f"Error cleaning up file {file_path}: {str(e)}")
    
    def get_file_info(self, file_path):
        """
        Get information about a file.
        
        Args:
            file_path (str): Path to the file
            
        Returns:
            dict: File information
        """
        if not os.path.exists(file_path):
            return None
        
        stat = os.stat(file_path)
        return {
            'name': os.path.basename(file_path),
            'size': stat.st_size,
            'created': datetime.fromtimestamp(stat.st_ctime),
            'modified': datetime.fromtimestamp(stat.st_mtime),
            'path': file_path
        }
    
    def list_results(self, operation_type=None):
        """
        List result files.
        
        Args:
            operation_type (str): Type of operation to filter by
            
        Returns:
            list: List of result files
        """
        results = []
        
        for dir_name, dir_path in self.base_dirs.items():
            if operation_type and dir_name != operation_type:
                continue
                
            if os.path.exists(dir_path):
                for filename in os.listdir(dir_path):
                    file_path = os.path.join(dir_path, filename)
                    if os.path.isfile(file_path):
                        file_info = self.get_file_info(file_path)
                        if file_info:
                            results.append(file_info)
        
        # Sort by modification time (newest first)
        results.sort(key=lambda x: x['modified'], reverse=True)
        return results
    
    def create_backup(self, file_path, backup_dir=None):
        """
        Create a backup of a file.
        
        Args:
            file_path (str): Path to the file to backup
            backup_dir (str): Directory to store backup
            
        Returns:
            str: Path to backup file
        """
        if not os.path.exists(file_path):
            return None
        
        if backup_dir is None:
            backup_dir = os.path.join(self.base_dirs['results'], 'backups')
        
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.basename(file_path)
        name, ext = os.path.splitext(filename)
        backup_filename = f"{name}_backup_{timestamp}{ext}"
        backup_path = os.path.join(backup_dir, backup_filename)
        
        try:
            shutil.copy2(file_path, backup_path)
            logging.info(f"Created backup: {file_path} -> {backup_path}")
            return backup_path
        except Exception as e:
            logging.error(f"Error creating backup: {str(e)}")
            return None
    
    def get_directory_size(self, dir_path):
        """
        Get the total size of a directory.
        
        Args:
            dir_path (str): Path to the directory
            
        Returns:
            int: Total size in bytes
        """
        total_size = 0
        if os.path.exists(dir_path):
            for dirpath, dirnames, filenames in os.walk(dir_path):
                for filename in filenames:
                    file_path = os.path.join(dirpath, filename)
                    if os.path.exists(file_path):
                        total_size += os.path.getsize(file_path)
        return total_size
    
    def get_storage_info(self):
        """
        Get storage information for all directories.
        
        Returns:
            dict: Storage information
        """
        storage_info = {}
        total_size = 0
        
        for dir_name, dir_path in self.base_dirs.items():
            if os.path.exists(dir_path):
                size = self.get_directory_size(dir_path)
                storage_info[dir_name] = {
                    'path': dir_path,
                    'size': size,
                    'size_mb': size / (1024 * 1024)
                }
                total_size += size
        
        storage_info['total'] = {
            'size': total_size,
            'size_mb': total_size / (1024 * 1024)
        }
        
        return storage_info
