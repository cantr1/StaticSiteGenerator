"""
Main entry point for static site generation
"""
import logging

from textnode import TextNode, TextType
from block_type import *
from htmlnode import HTMLNode, ParentNode, LeafNode
from helper_functions import *
import argparse
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

def generate_page(from_path: str, template_path: str, to_path: str, base_path: str = "/"):
    logger.info(f"Generating page from {from_path} using template {template_path} and outputting to {to_path}")
    # Open markdown file and read contents
    try:
        with open(from_path, "r") as markdown_file:
            markdown_content = markdown_file.read()
    except Exception as e:
        logger.critical(f"Error reading markdown file: {e}")
        exit(1)

    # Open template file and read contents
    try:
        with open(template_path, "r") as template_file:
            template_content = template_file.read()
    except Exception as e:
        logger.critical(f"Error reading template file: {e}")
        exit(1)

    html: HTMLNode = markdown_to_html_node(markdown_content)

    title = extract_title(markdown_content)

    # Replace title and content in template
    html_output = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html.to_html()).replace("{{ href=\"/ }}", f"{{ href=\"{base_path} }}").replace("{{ src=\"/ }}", f"{{ src=\"{base_path} }}")

    # Write output to file
    try:
        with open(to_path, "w") as output_file:
            output_file.write(html_output)
    except Exception as e:
        logger.critical(f"Error writing output file: {e}")
        exit(1)

def generate_pages_recursive(dir_path_content: str, template_path: str, dir_path_output: str, base_path: str = "/"):
    try:
        for content in os.listdir(dir_path_content):
            content_path = os.path.join(dir_path_content, content)
            output_path = os.path.join(dir_path_output, content.replace(".md", ".html"))
            if os.path.isfile(content_path) and content.endswith(".md"):
                generate_page(content_path, template_path, output_path, base_path)
            elif os.path.isdir(content_path):
                if not os.path.exists(output_path):
                    os.makedirs(output_path)
                generate_pages_recursive(content_path, template_path, output_path, base_path)
    except Exception as e:
        logger.critical(f"Error generating pages recursively: {e}")
        exit(1)

def main() -> None:
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Static Site Generator")
    parser.add_argument("--basepath", "-b", type=str, default="./", help="Base path for root of directory structure")
    args = parser.parse_args()

    public_folder_path = "./docs/"
    static_folder_path = "./static/"

    clear_public_directory(public_folder_path)
    copy_static_folder_to_public(static_folder_path, public_folder_path)

    generate_pages_recursive(
        dir_path_content="./content/",
        template_path="./template.html",
        dir_path_output="./docs/",
        base_path=args.basepath
    )

if __name__ == "__main__":
    main()
    exit(0)
