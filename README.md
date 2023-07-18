# Indented text importer

Somewhat monkey patched indent parser in [anytree](https://github.com/c0fec0de/anytree) node, seeing how it was [removed from anytree since 2.5.0](https://github.com/c0fec0de/anytree/commit/9279e1136f1144de86e894af733f27cf5750dd69)

## Usage

```python
input_str = """
foo
    bar
        baz
hello
    world
    amy
        bob
"""

expected_json_equivalent = {
    "name": "root",
    "children": [
        {
            "name": "foo",
            "children": [
                {
                    "name": "bar",
                    "children": [
                        {
                            "name": "baz"
                        }
                    ]
                }
            ]
        },
        {
            "name": "hello",
            "children": [
                {
                    "name": "world"
                },
                {
                    "name": "amy",
                    "children": [
                        {
                            "name": "bob"
                        }
                    ]
                }
            ]
        }
    ]
}

from indented_text_importer import EtheralDict, parse_text
from anytree import RenderTree, Node
from anytree.importer import DictImporter

dict_importer = DictImporter(nodecls=Node)

actual = parse_text(input_str.split("\n"))
expected = dict_importer.import_(expected_json_equivalent)
assert str(RenderNode(actual)) == str(RenderNode(expected))
```

## License

MIT