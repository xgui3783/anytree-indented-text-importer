from typing import Iterable, Mapping, Any
import re
from anytree import Node

_fuse = 10

class EtheralDict(dict):
    def __setitem__(self, __key: Any, __value: Any) -> None:
        """
        Special implementation. On set an int key, all int key larger will get reset.
        This is so that, in the event user accidentally used double delimiter, an error 
        will be thrown, rather than attaching it to the wrong node.
        """
        if isinstance(__key, int):
            iter_key = __key
            while iter_key in self:
                self.pop(iter_key)
                iter_key = iter_key + 1
        return super().__setitem__(__key, __value)

def parse_text(texts: Iterable[str], delimiter: str=None):
    # if delimiter unset, attempt to find suitable candidate
    if delimiter is None:
        print(f"Delimiter not provided, will attempt to infer")

    root_node = Node("root")
    parent_nodes: Mapping[int, Node] = EtheralDict()

    for text in texts:

        # skip empty lines
        if text.strip() == "":
            continue

        if delimiter is None:
            matched = re.match(r'(\s+)', text)
            if matched:
                delimiter = matched[0]
        
        
        idx = 0
        delimiter_len = len(delimiter or [])
        while all([
            delimiter is not None,
            len(text) > delimiter_len,
            text[:delimiter_len] == delimiter,
        ]):
            idx = idx + 1
            text = text.replace(delimiter, "", 1)
            if idx > _fuse:
                raise Exception(f"{text!r}, {delimiter!r}, something broke")

        new_node = Node(text)
        parent_nodes[idx] = new_node
        try:
            new_node.parent = root_node if idx == 0 else parent_nodes[idx - 1]
        except IndexError as e:
            raise IndexError(f"Parent to {text!r} not found. Did you indent correctly?") from e

    return root_node

__all__ = [
    "parse_text"
]
