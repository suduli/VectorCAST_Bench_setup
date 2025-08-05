#!/usr/bin/env python3
"""
Automated Test Bench Setup Tool for VectorCAST Unit Testing

This tool automates the creation and setup of test bench environments for 
unit testing projects using VectorCAST with Tasking Tricore TC297TA T32 Simulator.

Author: Suduli Kumar
Version: 1.0.0
"""

import os
import os.path
import shutil
import sys
import time
import logging
from pathlib import Path
from zipfile import ZipFile
from typing import Optional


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test_bench_setup.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


class TestBenchSetup:
    """
    Automated Test Bench Setup for VectorCAST Unit Testing Environment
    
    This class handles the creation of project directories and setup of
    necessary files for automated unit testing with VectorCAST.
    """
    
    def __init__(self):
        """Initialize the TestBenchSetup with default configurations."""
        self.project_path: Optional[str] = None
        self.project_name: Optional[str] = None
        
        # Network paths for source files
        self.network_base = r"Enter File Path"
        self.source_files = {
            'launch_package': 'Launch_VC_Tricore_AURIX_TC23x_t32sim.zip',
            'source_code': 'SourceCode.zip',
            'config_file': 'CCAST_.cfg'
        }
    
    def get_user_inputs(self) -> tuple[str, str]:
        """
        Get user inputs for destination path and project name.
        
        Returns:
            tuple: (destination_path, project_name)
        """
        try:
            # Set console color (Windows only)
            if os.name == 'nt':
                os.system("color A")
            
            destination_path = input("Enter the destination folder path: ").strip()
            if not destination_path:
                raise ValueError("Destination path cannot be empty")
            
            project_name = input("Enter Project Name: ").strip()
            if not project_name:
                raise ValueError("Project name cannot be empty")
            
            return destination_path, project_name
            
        except KeyboardInterrupt:
            logger.info("Setup cancelled by user")
            sys.exit(0)
        except ValueError as e:
            logger.error(f"Input validation error: {e}")
            sys.exit(1)
    
    def create_project_structure(self, destination_path: str, project_name: str) -> None:
        """
        Create the project directory structure.
        
        Args:
            destination_path (str): Base path where project will be created
            project_name (str): Name of the project
        """
        try:
            self.project_path = os.path.join(destination_path, project_name)
            self.project_name = project_name
            
            # Create main project directory
            Path(self.project_path).mkdir(parents=True, exist_ok=True)
            logger.info(f"Created project directory: {self.project_path}")
            
            # Define subdirectories
            subdirectories = {
                'test_path': os.path.join(self.project_path, "VCAST_UT"),
                'launch_path': os.path.join(self.project_path, "VectorCAST_patch_for_Tasking_Tricore_TC297TA_T32_Simulator"),
                'source_path': os.path.join(self.project_path, "SourceCode"),
                'config_path': os.path.join(self.project_path, "Master_CFG")
            }
            
            # Create subdirectories
            for dir_name, dir_path in subdirectories.items():
                Path(dir_path).mkdir(parents=True, exist_ok=True)
                logger.info(f"Created {dir_name}: {dir_path}")
            
            # Store paths for later use
            self.subdirectories = subdirectories
            
        except OSError as e:
            logger.error(f"Failed to create directory structure: {e}")
            raise
    
    def copy_and_extract_files(self) -> None:
        """Copy and extract necessary files from network location."""
        try:
            logger.info("Starting file copy and extraction process...")
            
            # Copy and extract launch package
            self._copy_and_extract_zip(
                filename=self.source_files['launch_package'],
                destination=self.subdirectories['launch_path'],
                description="VectorCAST launch package"
            )
            
            # Copy and extract source code
            self._copy_and_extract_zip(
                filename=self.source_files['source_code'],
                destination=self.subdirectories['source_path'],
                description="Source code package"
            )
            
            # Copy configuration file
            self._copy_config_file()
            
            logger.info("All files copied and extracted successfully!")
            
        except Exception as e:
            logger.error(f"File operation failed: {e}")
            raise
    
    def _copy_and_extract_zip(self, filename: str, destination: str, description: str) -> None:
        """
        Copy and extract a zip file from network location.
        
        Args:
            filename (str): Name of the zip file
            destination (str): Destination directory
            description (str): Description for logging
        """
        source_path = os.path.join(self.network_base, filename)
        
        logger.info(f"Copying {description}...")
        copied_file = shutil.copy(source_path, destination)
        logger.info(f"Copied to: {copied_file}")
        
        logger.info(f"Extracting {description}...")
        with ZipFile(copied_file, 'r') as zip_file:
            zip_file.extractall(destination)
        
        logger.info(f"Extracted {description} successfully")
    
    def _copy_config_file(self) -> None:
        """Copy the configuration file."""
        source_path = os.path.join(self.network_base, self.source_files['config_file'])
        
        logger.info("Copying configuration file...")
        copied_file = shutil.copy(source_path, self.subdirectories['config_path'])
        logger.info(f"Configuration file copied to: {copied_file}")
    
    def run_setup(self) -> None:
        """Run the complete test bench setup process."""
        try:
            logger.info("Starting Automated Test Bench Setup")
            logger.info("=" * 50)
            
            # Get user inputs
            destination_path, project_name = self.get_user_inputs()
            
            # Create project structure
            logger.info("Creating project directory structure...")
            self.create_project_structure(destination_path, project_name)
            
            # Add delay for system stability
            logger.info("Waiting for system stability...")
            time.sleep(2)  # Reduced from 30 seconds for better UX
            
            # Copy and extract files
            self.copy_and_extract_files()
            
            logger.info("=" * 50)
            logger.info("✅ Test bench setup completed successfully!")
            logger.info(f"Project created at: {self.project_path}")
            
        except Exception as e:
            logger.error(f"Setup failed: {e}")
            sys.exit(1)


def main():
    """Main entry point of the application."""
    try:
        setup_tool = TestBenchSetup()
        setup_tool.run_setup()
    except KeyboardInterrupt:
        logger.info("Setup interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
