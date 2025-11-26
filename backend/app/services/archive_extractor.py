import zipfile
import tarfile
import os
from typing import List, Tuple
from pathlib import Path
import tempfile

class ArchiveExtractor:
    """Handles extraction of tar and zip archives"""
    
    SUPPORTED_EXTENSIONS = {'.zip', '.tar', '.tar.gz', '.tgz', '.tar.bz2', '.tbz2'}
    
    @staticmethod
    def is_archive(filename: str) -> bool:
        """Check if file is a supported archive"""
        path = Path(filename)
        # Check for compound extensions like .tar.gz
        if path.suffix == '.gz' and path.stem.endswith('.tar'):
            return True
        if path.suffix == '.bz2' and path.stem.endswith('.tar'):
            return True
        return path.suffix in ArchiveExtractor.SUPPORTED_EXTENSIONS
    
    @staticmethod
    def extract_archive(archive_path: str, extract_to: str = None) -> List[str]:
        """
        Extract archive and return list of extracted file paths
        
        Args:
            archive_path: Path to the archive file
            extract_to: Directory to extract to (creates temp dir if None)
            
        Returns:
            List of paths to extracted files
        """
        if extract_to is None:
            extract_to = tempfile.mkdtemp()
        
        extracted_files = []
        path = Path(archive_path)
        
        try:
            if path.suffix == '.zip':
                with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_to)
                    extracted_files = [
                        os.path.join(extract_to, name) 
                        for name in zip_ref.namelist() 
                        if not name.endswith('/')
                    ]
            
            elif '.tar' in path.name:
                # Handles .tar, .tar.gz, .tar.bz2, etc.
                mode = 'r:*'  # Auto-detect compression
                with tarfile.open(archive_path, mode) as tar_ref:
                    tar_ref.extractall(extract_to)
                    extracted_files = [
                        os.path.join(extract_to, member.name) 
                        for member in tar_ref.getmembers() 
                        if member.isfile()
                    ]
        except Exception as e:
            print(f"Error extracting archive {archive_path}: {e}")
            raise
        
        return extracted_files
    
    @staticmethod
    def extract_and_filter(archive_path: str, allowed_extensions: List[str] = None) -> List[Tuple[str, str]]:
        """
        Extract archive and filter files by extension
        
        Args:
            archive_path: Path to archive
            allowed_extensions: List of allowed extensions (e.g., ['.txt', '.pdf'])
            
        Returns:
            List of tuples (original_filename, extracted_path)
        """
        extracted_files = ArchiveExtractor.extract_archive(archive_path)
        
        if allowed_extensions:
            filtered = []
            for fpath in extracted_files:
                ext = Path(fpath).suffix.lower()
                if ext in allowed_extensions:
                    filtered.append((Path(fpath).name, fpath))
            return filtered
        
        return [(Path(fpath).name, fpath) for fpath in extracted_files]
