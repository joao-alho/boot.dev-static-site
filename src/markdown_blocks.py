import re

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"


def markdown_to_blocks(markdown):
    lines = markdown.split("\n\n")

    def clean_up_block_text(text):
        block_lines = text.split("\n")
        if len(block_lines) == 1:
            return block_lines[0].strip()
        else:
            return "\n ".join(map(lambda x: x.strip(), block_lines))
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
        numbered = list(
            map(lambda x: int(re.match(ord_regex, x).group(1)), lines))
        is_ordered = True
        for i in range(len(lines)):
            if numbered[i] == i+1:
                is_ordered = True
            else:
                is_ordered = False
                break

        if is_ordered:
            return block_type_ordered_list

    return block_type_paragraph
