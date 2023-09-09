from typing import List


from pydantic import BaseModel
from pybackpack.datastores import RedisDataStore


class ChildModel(BaseModel):
    name: str
    age: int


class ParentModel(BaseModel):
    name: str
    age: int
    children: List[ChildModel]

    class Config:
        schema_extra = {"persist_schema": "parent"}


def test_redis_ping():
    redis = RedisDataStore()
    assert redis.ping() is True


def test_redis_simple_get_set():
    redis = RedisDataStore()

    redis.set_str("key1", "value1")
    assert redis.get_str("key1") == "value1"

    redis.delete("key1")
    assert redis.get_str("key1") is None


def test_redis_json():
    redis = RedisDataStore()

    parent = {
        "name": "parent",
        "age": 50,
        "children": [
            {"name": "child1", "age": 10},
            {"name": "child2", "age": 20},
        ],
    }

    # Set and get the parent
    redis.set_json("p1", parent)
    name = redis.get_json("p1", "$.name")
    assert name == "parent"

    # Update the name of the first child
    redis.set_json("p1", "child1-updated", "$.children[0].name")
    name = redis.get_json("p1", "$.children[0].name")
    assert name == "child1-updated"

    # Update the whole object of the first child
    new_child = {"name": "child1-updated2", "age": 11}
    redis.set_json("p1", new_child, "$.children[0]")
    loaded_child = redis.get_json("p1", "$.children[0]")
    assert loaded_child["name"] == "child1-updated2"

    # Delete the first child
    redis.delete_json("p1", "$.children[0]")
    loaded_parent = redis.get_json("p1")
    assert len(loaded_parent["children"]) == 1

    # Delete the parent
    redis.delete("p1")
    assert redis.get_json("p1") is None


def test_redis_from_pydantic_dict():
    redis = RedisDataStore()

    parent = ParentModel(
        name="parent",
        age=50,
        children=[
            ChildModel(name="child1", age=10),
            ChildModel(name="child2", age=20),
        ],
    )

    # Set the parent and childrens
    redis.set_json("p1", parent.model_dump())
    loaded_parent = ParentModel(**redis.get_json("p1"))
    assert loaded_parent.name == "parent"
    assert len(loaded_parent.children) == 2
    assert loaded_parent.children[0].name == "child1"

    # Update the name of the first child
    redis.set_json("p1", "child1-updated", "$.children[0].name")
    loaded_parent = ParentModel(**redis.get_json("p1"))
    assert loaded_parent.children[0].name == "child1-updated"

    # Update the name using the object of the first child
    loaded_parent.children[0].name = "child1-updated-again"
    redis.set_json(
        "p1", loaded_parent.children[0].model_dump(), "$.children[0]"
    )
    loaded_parent = ParentModel(**redis.get_json("p1"))
    assert loaded_parent.children[0].name == "child1-updated-again"

    # Update the whole object of the first child
    redis.set_json(
        "p1", {"name": "child1-updated", "age": 11}, "$.children[0]"
    )
    loaded_parent = ParentModel(**redis.get_json("p1"))
    assert loaded_parent.children[0].name == "child1-updated"
    assert loaded_parent.children[0].age == 11

    # Update the whole object of the first child using the object
    updated_child = ChildModel(name="child1-updated2", age=12)
    redis.set_json("p1", updated_child.model_dump(), "$.children[0]")
    loaded_parent = ParentModel(**redis.get_json("p1"))
    assert loaded_parent.children[0].name == "child1-updated2"

    # Update the first child and add the third child.
    loaded_parent.children[0] = ChildModel(name="child1-updated3", age=13)
    loaded_parent.children.append(ChildModel(name="child3", age=30))
    redis.set_json("p1", loaded_parent.model_dump(), "$")
    loaded_parent = ParentModel(**redis.get_json("p1"))
    assert loaded_parent.children[0].name == "child1-updated3"
    assert loaded_parent.children[2].name == "child3"

    # Get the second child only
    loaded_child = ChildModel(**redis.get_json("p1", "$.children[1]"))
    assert loaded_child.name == "child2"
    assert loaded_child.age == 20

    # Remove the first child
    redis.delete_json("p1", "$.children[0]")
    loaded_parent = ParentModel(**redis.get_json("p1"))
    assert len(loaded_parent.children) == 2

    # delete the parent
    redis.delete("p1")
    assert redis.get_json("p1") is None


def test_redis_pydantic():
    redis = RedisDataStore()

    parent = ParentModel(
        name="parent",
        age=50,
        children=[
            ChildModel(name="child1", age=10),
            ChildModel(name="child2", age=20),
        ],
    )

    # Set and get the parent
    redis.set_pydantic("p1", parent)
    loaded_parent = redis.get_pydantic("p1", ParentModel)
    assert loaded_parent.name == "parent"
    assert len(loaded_parent.children) == 2

    # Update the name of the first child
    parent.children[0].name = "child1-updated"
    redis.set_pydantic("p1", parent)
    loaded_parent = redis.get_pydantic("p1", ParentModel)
    assert loaded_parent.children[0].name == "child1-updated"

    redis.delete_pydantic("p1", ParentModel)
    assert redis.get_pydantic("p1", ParentModel) is None


def test_redis_create_index():
    root_prefix = "test"
    redis = RedisDataStore(root_prefix=root_prefix)

    schema = [
        {"field": "$.name", "type": "text", "alias": "name"},
        {"field": "$.age", "type": "number", "alias": "age"},
    ]

    index_name = "parents"
    # Get index info
    index_info = redis.get_index_info(index_name)
    if index_info:
        assert index_info["index_name"] == "test:idx:parents"
        print(index_info["index_definition"])
        # Drop the index
        redis.delete_index(index_name)

    # Create the index
    redis.create_index_on_json(
        index_name=index_name,
        key_prefixes_to_index=["parents"],
        schema=schema,
    )
    index_info = redis.get_index_info(index_name)
    assert (
        index_info["index_definition"][3][0].decode("utf-8")
    ) == "test:parents:"
    assert redis.get_index_info(index_name) is not None

    # Delete the index
    redis.delete_index(index_name)
    assert redis.get_index_info(index_name) is None
