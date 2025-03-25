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