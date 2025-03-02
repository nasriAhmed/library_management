import pytest
from bson import ObjectId
from app.utils import serialize_doc

def test_serialize_objectid():
    """ Vérifie la conversion d'un ObjectId en chaîne """
    obj_id = ObjectId()
    assert serialize_doc(obj_id) == str(obj_id)

def test_serialize_list():
    """ Vérifie la conversion d'une liste contenant des ObjectIds """
    obj_id1 = ObjectId()
    obj_id2 = ObjectId()
    data = [obj_id1, obj_id2]
    expected = [str(obj_id1), str(obj_id2)]
    assert serialize_doc(data) == expected

def test_serialize_dict():
    """ Vérifie la conversion d'un dictionnaire contenant des ObjectIds """
    obj_id = ObjectId()
    data = {"_id": obj_id, "name": "Test"}
    expected = {"_id": str(obj_id), "name": "Test"}
    assert serialize_doc(data) == expected

def test_serialize_nested_dict():
    """ Vérifie la conversion d'un dictionnaire imbriqué contenant des ObjectIds """
    obj_id = ObjectId()
    data = {"user": {"id": obj_id, "name": "Alice"}}
    expected = {"user": {"id": str(obj_id), "name": "Alice"}}
    assert serialize_doc(data) == expected

def test_serialize_primitive():
    """ Vérifie que les types primitifs restent inchangés """
    assert serialize_doc(42) == 42
    assert serialize_doc("hello") == "hello"
    assert serialize_doc(3.14) == 3.14
    assert serialize_doc(True) == True
