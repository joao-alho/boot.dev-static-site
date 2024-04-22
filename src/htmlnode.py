class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props: dict = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None:
            return ""
        else:
            props_html = map(lambda k: f' {k}="{self.props[k]}"', self.props)
            return "".join(props_html)

    def __eq__(self, o):
        return (
            self.tag == o.tag
            and self.value == o.value
            and self.children == o.children
            and self.props == o.props
        )

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        if value is None:
            raise ValueError("All leaf nodes require a value")
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if not self.tag:
            return f"{self.value}"
        else:
            _props = self.props_to_html()
            return f"<{self.tag}{_props}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("All parent nodes require a tag")
        if not self.children:
            raise ValueError("All parent nodes require children")

        children_html = "".join(map(lambda c: c.to_html(), self.children))
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
