import re

from src.htmlnode import ParentNode
from src.inline_markdown import text_to_textnodes
from src.textnode import text_node_to_html_node

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"


def markdown_to_blocks(markdown):
    lines = markdown.split("\n\n")

    def clean_up_block_text(text):
        block_lines = text.strip().split("\n")
        if len(block_lines) == 1:
            return block_lines[0].strip()
        else:
            return "\n".join(map(lambda x: x.strip(), block_lines))

    lines = map(clean_up_block_text, lines)
    lines = filter(lambda x: x != "", lines)
    return list(lines)


def block_to_block_type(block):
    lines = block.split("\n")
    ord_regex = r"^(\d)\. "
    if re.match(r"^#{1,6} ", block):
        return block_type_heading
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return block_type_code
    if all(map(lambda x: re.match(r"^>", x), lines)):
        return block_type_quote
    if all(map(lambda x: re.match(r"^[\*|-] ", x), lines)):
        return block_type_unordered_list
    if all(map(lambda x: re.match(ord_regex, x), lines)):
        numbered = list(map(lambda x: int(re.match(ord_regex, x).group(1)), lines))
        is_ordered = True
        for i in range(len(lines)):
            if numbered[i] == i + 1:
                is_ordered = True
            else:
                is_ordered = False
                break

        if is_ordered:
            return block_type_ordered_list

    return block_type_paragraph


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return list(map(lambda x: text_node_to_html_node(x), text_nodes))


def paragraph_block_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode(tag="p", children=children)


def headings_block_to_html_node(block):
    level = len(block.split("#")) - 1
    text = block[level + 1 :]
    children = text_to_children(text)

    return ParentNode(tag=f"h{level}", children=children)


def ordered_list_block_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode(tag="li", children=children))
    return ParentNode(tag="ol", children=html_items)


def unordered_list_block_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode(tag="li", children=children))
    return ParentNode(tag="ul", children=html_items)


def quote_block_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        new_lines.append(line.lstrip(">").strip())
    children = text_to_children(" ".join(new_lines))
    return ParentNode(tag="blockquote", children=children)


def code_block_to_html_node(block):
    text = block[4:-3]
    children = text_to_children(text)
    return ParentNode(tag="pre", children=[ParentNode(tag="code", children=children)])


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        if block_to_block_type(block) == block_type_code:
            html_nodes.append(code_block_to_html_node(block))
        elif block_to_block_type(block) == block_type_quote:
            html_nodes.append(quote_block_to_html_node(block))
        elif block_to_block_type(block) == block_type_ordered_list:
            html_nodes.append(ordered_list_block_to_html_node(block))
        elif block_to_block_type(block) == block_type_heading:
            html_nodes.append(headings_block_to_html_node(block))
        elif block_to_block_type(block) == block_type_unordered_list:
            html_nodes.append(unordered_list_block_to_html_node(block))
        else:
            html_nodes.append(paragraph_block_to_html_node(block))
    return ParentNode(tag="div", children=html_nodes)
