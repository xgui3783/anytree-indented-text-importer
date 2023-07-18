import pytest
from indented_text_importer import EtheralDict, parse_text
from anytree import RenderTree, Node
from anytree.importer import DictImporter

dict_importer = DictImporter(nodecls=Node)

@pytest.fixture
def provide_dict():
    return EtheralDict()

def test_etheraldict_as_dict(provide_dict: EtheralDict):
    assert "foo" not in provide_dict
    provide_dict["foo"] = "bar"
    assert "foo" in provide_dict
    assert provide_dict["foo"] == "bar"

    provide_dict.pop("foo", None)
    assert "foo" not in provide_dict

def test_etheraldict_special(provide_dict: EtheralDict):

    # set int keys
    provide_dict[0] = '0'
    provide_dict[1] = '1'
    provide_dict[2] = '2'

    # check they are valid getters
    assert 0 in provide_dict
    assert 1 in provide_dict
    assert 2 in provide_dict

    # on set of base int, check resets all higher ints
    provide_dict[0] = 'new_0'

    assert 0 in provide_dict
    assert 1 not in provide_dict
    assert 2 not in provide_dict

siblings = {
    "name": "root",
    "children": [{
        "name": "foo",
    }, {
        "name": "bar",
    }]
}

children = {
    "name": "root",
    "children": [{
        "name": "foo",
        "children": [{
            "name": "bar"
        }]
    }]
}
children2 = {
    "name": "root",
    "children": [{
        "name": "foo",
        "children": [{
            "name": "bar"
        },{
            "name": "baz"
        }]
    }]
}
complex = {
    "name": "root",
    "children": [{
        "name": "foo",
        "children": [{
            "name": "bar"
        }]
    },{
        "name": "baz"
    }]
}

args = [
(
    """foo
bar""", siblings
),
(
    """
foo
bar
""", siblings
),
(
    """
foo
    bar
""", children
),
(
    """
foo
\tbar
""", children
),
(
    """
foo
    bar
    baz
""", children2
),
(
    """
foo
    bar
baz
""", complex
),
(
    """
foo
    bar
        baz
foo1
        baz1
""", None
),
]

@pytest.mark.parametrize('input_text,expected_json', args)
def test_parse_text(input_text: str,expected_json):
    if expected_json is None:
        with pytest.raises(Exception):
            actual_tree = parse_text(input_text.split("\n"))        
        return
    expected_tree = dict_importer.import_(expected_json)
    actual_tree = parse_text(input_text.split("\n"))
    assert str(RenderTree(actual_tree)) == str(RenderTree(expected_tree))
    