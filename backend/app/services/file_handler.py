"""
File upload handling service
Manages file uploads, validation, and temporary storage
"""

import os
import uuid
import shutil
from pathlib import Path
from typing import Optional
from fastapi import UploadFile, HTTPException, status
import aiofiles
import logging

from app.config import settings

logger = logging.getLogger(__name__)


class FileHandler:
    """Service for handling file uploads and validation"""
    
    def __init__(self):
        self.upload_dir = Path(settings.upload_dir)
        self.max_size = settings.max_upload_size
        self.allowed_extensions = settings.allowed_extensions_list
    
    def validate_file_extension(self, filename: str) -> bool:
        """
        Validate if file extension is allowed
        
        Args:
            filename: Name of the file
            
        Returns:
            True if extension is allowed, False otherwise
        """
        file_ext = Path(filename).suffix.lower()
        return file_ext in self.allowed_extensions or filename.endswith('.zip')
    
    async def save_upload_file(self, upload_file: UploadFile, subfolder: str = "") -> str:
        """
        Save uploaded file to disk
        
        Args:
            upload_file: FastAPI UploadFile object
            subfolder: Optional subfolder within upload directory
            
        Returns:
            Path to saved file
            
        Raises:
            HTTPException: If file validation fails
        """
        # Validate file extension
        if not self.validate_file_extension(upload_file.filename):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File type not allowed. Allowed extensions: {', '.join(self.allowed_extensions)}"
            )
        
        # Create unique filename to avoid collisions
        file_id = str(uuid.uuid4())
        file_ext = Path(upload_file.filename).suffix
        unique_filename = f"{file_id}{file_ext}"
        
        # Create subfolder if specified
        save_dir = self.upload_dir / subfolder if subfolder else self.upload_dir
        save_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = save_dir / unique_filename
        
        try:
            # Save file asynchronously
            async with aiofiles.open(file_path, 'wb') as f:
                content = await upload_file.read()
                
                # Check file size
                if len(content) > self.max_size:
                    raise HTTPException(
                        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        detail=f"File size exceeds maximum allowed size of {self.max_size / (1024*1024):.2f}MB"
                    )
                
                await f.write(content)
            
            logger.info(f"File saved: {file_path}")
            return str(file_path)
        
        except Exception as e:
            # Clean up file if save failed
            if file_path.exists():
                file_path.unlink()
            logger.error(f"Error saving file: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to save file: {str(e)}"
            )
    
    async def save_multiple_files(self, files: list[UploadFile], subfolder: str = "") -> list[str]:
        """
        Save multiple uploaded files
        
        Args:
            files: List of FastAPI UploadFile objects
            subfolder: Optional subfolder within upload directory
            
        Returns:
            List of paths to saved files
        """
        saved_paths = []
        for file in files:
            path = await self.save_upload_file(file, subfolder)
            saved_paths.append(path)
        return saved_paths
    
    def delete_file(self, file_path: str) -> bool:
        """
        Delete a file from disk
        
        Args:
            file_path: Path to file to delete
            
        Returns:
            True if deleted successfully, False otherwise
        """
        try:
            path = Path(file_path)
            if path.exists():
                path.unlink()
                logger.info(f"File deleted: {file_path}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting file {file_path}: {str(e)}")
            return False
    
    def cleanup_directory(self, subfolder: str = "") -> int:
        """
        Clean up all files in a directory
        
        Args:
            subfolder: Optional subfolder to clean
            
        Returns:
            Number of files deleted
        """
        target_dir = self.upload_dir / subfolder if subfolder else self.upload_dir
        if not target_dir.exists():
            return 0
        
        count = 0
        try:
            for item in target_dir.iterdir():
                if item.is_file():
                    item.unlink()
                    count += 1
                elif item.is_dir():
                    shutil.rmtree(item)
                    count += 1
            logger.info(f"Cleaned up {count} items from {target_dir}")
        except Exception as e:
            logger.error(f"Error cleaning directory {target_dir}: {str(e)}")
        
        return count


# Global file handler instance
file_handler = FileHandler()

# Made with Bob
