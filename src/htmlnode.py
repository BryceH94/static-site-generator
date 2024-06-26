class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        return " ".join(map(lambda k: f'{k}="{self.props[k]}"', self.props))
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def __eq__(self, OtherHTMLNode):
        if (self.tag == OtherHTMLNode.tag and self.value == OtherHTMLNode.value
            and self.value == OtherHTMLNode.value and self.props == OtherHTMLNode.props):
            return True
        return False

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, children=None, props=None):
        if value is None:
            raise ValueError("value is required for a LeafNode")
        if props is not None and props is None:
            raise ValueError("Cannot have properties without a tag")
        if children is not None:
            raise ValueError("LeafNodes cannot have children")
        super().__init__(tag=tag, value=value, props=props)

    def __eq__(self, OtherLeafNode):
        if self.tag == OtherLeafNode.tag and self.value == OtherLeafNode.value and self.props == OtherLeafNode.props:
            return True
        return False

    def to_html(self):
        if self.value is not None:
            if self.tag:
                if self.props:
                    return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"
                else:
                    return f"<{self.tag}>{self.value}</{self.tag}>"
            else:
                return f"{self.value}"
        else:
            raise ValueError("value is required for a LeafNode")
        
class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        if tag is None:
            raise ValueError("tag is required for a ParentNode")
        if children is None:
            raise ValueError("children are required for a ParentNode")
        super().__init__(tag=tag, children=children, props=props)

    def __eq__(self, OtherHTMLNode):
        if (self.tag == OtherHTMLNode.tag and self.value == OtherHTMLNode.value
            and self.value == OtherHTMLNode.value and self.props == OtherHTMLNode.props):
            return True
        return False

    def to_html(self):
        current_text = f'<{self.tag}>' if self.props is None else f'<{self.tag} {self.props_to_html()}>'
        for node in self.children:
            current_text += node.to_html()
        current_text += f'</{self.tag}>'
        return current_text