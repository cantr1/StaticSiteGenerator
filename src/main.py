"""
Main entry point for static site generation
"""
from textnode import TextNode, TextType
import logging
import shutil
import os

# Basic logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

logger = logging.getLogger(__name__)

def clear_public_directory(file_path: str) -> bool:
    """Clear the public directory of all files and folders"""
    try:
        logger.info(f"Beginning file removal in {file_path}")
        if os.path.exists(file_path):
            files = os.listdir(file_path)
            for content in files:
                if os.path.isfile(os.path.join(file_path, content)):
                    logger.warning(f"Removing the following file: {file_path}{content}")
                    os.remove(os.path.join(file_path, content))
                elif os.path.isdir(os.path.join(file_path, content)):
                    logger.warning(f"Removing the following directory: {file_path}{content}/")
                    shutil.rmtree(os.path.join(file_path, content))
    except Exception as e:
        logger.critical(f"Error clearing public directory: {e}")
        exit(1)

def copy_static_folder_to_public(static_folder_path: str, public_folder_path: str) -> bool:
    """Copy all files from the static folder to the public folder"""
    try:
        logger.info(f"Beginning file copy from {static_folder_path} to {public_folder_path}")
        if os.path.exists(static_folder_path) and os.path.exists(public_folder_path):
            static_folder_contents = os.listdir(static_folder_path)
            for content in static_folder_contents:
                if os.path.isfile(os.path.join(static_folder_path, content)):
                    logger.info(f"Copying file {static_folder_path}{content} -> {public_folder_path}")
                    shutil.copy(os.path.join(static_folder_path, content), public_folder_path)
                elif os.path.isdir(os.path.join(static_folder_path, content)):
                    logger.info(f"Copying directory {static_folder_path}{content}/ -> {public_folder_path}{content}/")
                    shutil.copytree(os.path.join(static_folder_path, content), os.path.join(public_folder_path, content))
        else:
            logger.critical("One or more destination folders do not exist")
            exit(1)
    except Exception as e:
        logger.critical(f"Error copying static folder to public: {e}")
        exit(1)

def main() -> None:
    public_folder_path = "./public/"
    static_folder_path = "./static/"

    clear_public_directory(public_folder_path)
    copy_static_folder_to_public(static_folder_path, public_folder_path)

if __name__ == "__main__":
    main()
    exit(0)
