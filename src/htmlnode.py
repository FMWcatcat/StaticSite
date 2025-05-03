class HTMLNODE():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError


    def props_to_html(self):
        if self.props is None:
            return ""
        
        props_list = []
        for key, value in self.props.items():
            props_list.append(f'{key}="{value}"')

        return " " + " ".join(props_list) if props_list else ""
    
    def __repr__(self):
        return  f"HTMLNODE(tag={self.tag}, value{self.value}, children{self.children}, props{self.props})"
    

class LeafNode(HTMLNODE):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError(("invalid HTML: no value"))
        if self.tag is None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
class ParentNode(HTMLNODE):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError(("invalid HTML: no tag"))
        if self.children is None:
            raise ValueError(("invalid HTML: no children"))
        else:
            result = f"<{self.tag}{self.props_to_html()}>"
            for child in self.children:
                result += child.to_html()
            result += f"</{self.tag}>"
            return result