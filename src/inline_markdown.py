from src.textnode import TextNode
import re

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

delimiters = {
    "`": text_type_code,
    "**": text_type_bold,
    "*": text_type_italic,
}


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type == text_type_text:
            split_nodes = []
            blocks = node.text.split(delimiter)
            if len(blocks) % 2 == 0:
                raise Exception(
                    f"Invalid Markdown syntax, section not closed: {node.text}"
                )
            for i in range(len(blocks)):
                if blocks[i] == "":
                    continue
                if i % 2 == 0:
                    split_nodes.append(TextNode(blocks[i], text_type_text))
                else:
                    split_nodes.append(TextNode(blocks[i], text_type))

            new_nodes.extend(split_nodes)
        else:
            new_nodes.append(node)
    return new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches


def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if len(links) > 0:
            text_to_split = node.text
            for link in links:
                link_text = f"[{link[0]}]({link[1]})"
                splits = text_to_split.split(link_text, 1)
                text_to_split = splits[-1]
                if splits[0] != "":
                    new_nodes.append(TextNode(splits[0], text_type_text))
                new_nodes.append(TextNode(link[0], text_type_link, link[1]))
            if text_to_split != "":
                new_nodes.append(TextNode(text_to_split, text_type_text))
        else:
            new_nodes.append(node)
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        images = extract_markdown_images(node.text)
        if len(images) > 0:
            text_to_split = node.text
            for image in images:
                image_text = f"![{image[0]}]({image[1]})"
                splits = text_to_split.split(image_text, 1)
                text_to_split = splits[-1]
                if splits[0] != "":
                    new_nodes.append(TextNode(splits[0], text_type_text))
                new_nodes.append(TextNode(image[0], text_type_image, image[1]))
            if text_to_split != "":
                new_nodes.append(TextNode(text_to_split, text_type_text))
        else:
            new_nodes.append(node)
    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, text_type_text)]
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
