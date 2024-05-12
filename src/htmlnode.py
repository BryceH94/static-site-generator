class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        return " ".join(map(lambda k: f"{k}={self.props[k]}", self.props))
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag=None, **kwargs):
        value = kwargs.pop('value', None)
        if value is None:
            raise ValueError("value is required for a LeafNode")
        props = kwargs.pop('props', None)
        children = kwargs.pop('children', None)
        if children is not None:
            raise ValueError("LeafNodes cannot have children")
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value:
            if self.tag:
                return f"<{self.tag}>{self.value}</{self.tag}>"
            else:
                return f"{self.value}"
        else:
            raise ValueError("value is required for a LeafNode")