"""
Main entry point for static site generation
"""
from textnode import TextNode, TextType

def main() -> None:
    node = TextNode("Hello, World!", TextType.text, "https://www.bootdev.com")
    print(node)

if __name__ == "__main__":
    main()
    exit(0)
