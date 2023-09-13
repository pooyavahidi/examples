import os
import json
from typing import List, Type
import redis
from redis.commands.search.field import (
    TextField,
    NumericField,
    TagField,
    GeoField,
)
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import Query

from pydantic import BaseModel

redis_client = redis.from_url(url=os.environ.get("REDIS_URL"))


class RedisDataStore:
    """This class is a wrapper on top of redis client.
    It provides methods to get and set data, work with indexes and more.
    It also support pydantic models.
    """

    def __init__(
        self,
        root_prefix: str = None,
        prefix_delimiter: str = ":",
        index_prefix: str = "idx",
    ) -> None:
        self.root_prefix = root_prefix
        self.prefix_delimiter = prefix_delimiter
        self.index_prefix = index_prefix

    def _add_prefix(self, key: str, prefixes: List[str] = None) -> str:
        """Returns the key with the prefix.
        If any prefixes are given, they will be added to the key in the order.
        It will use the defined delimiter to join the prefixes and key.
        """

        output = key
        if prefixes:
            # Reverse prefixes to add them from the top level to the bottom.
            prefixes.reverse()
            for prefix in prefixes:
                if prefix is not None:
                    if self.prefix_delimiter is None:
                        output = prefix + output
                    else:
                        output = prefix + self.prefix_delimiter + output

        return output

    def ping(self) -> bool:
        """Returns pong if redis server is running."""
        return redis_client.ping()

    def get_str(self, key: str, decoding="utf-8") -> str:
        """Returns the value for the given key."""

        key = self._add_prefix(key, prefixes=[self.root_prefix])
        res = redis_client.get(key)

        if res and decoding:
            return res.decode(decoding)
        return res

    def set_str(self, key: str, value: str) -> None:
        """Sets the value for the given key."""

        key = self._add_prefix(key, prefixes=[self.root_prefix])
        redis_client.set(key, value)

    def delete(self, key: str) -> None:
        """Deletes the key-value pair for the given key."""

        key = self._add_prefix(key, prefixes=[self.root_prefix])
        redis_client.delete(key)

    def set_json(self, key: str, value: dict, json_path="$") -> None:
        """Using JSON capability of Redis Stack.
        Sets the value for the given key at the given JSONPath."""

        key = self._add_prefix(key, prefixes=[self.root_prefix])
        redis_client.json().set(key, json_path, value)

    def keys(self, pattern: str) -> List[str]:
        """Returns the keys for the given pattern."""

        pattern = self._add_prefix(pattern, prefixes=[self.root_prefix])
        return redis_client.keys(pattern)

    def get_json(self, key: str, json_path="$") -> dict:
        """Using JSON capability of Redis Stack.
        Returns the value for the given key at the given JSONPath."""

        key = self._add_prefix(key, prefixes=[self.root_prefix])
        res = redis_client.json().get(key, json_path)

        if res and len(res) == 1:
            return res[0]

        # The expectation from a JSONPath is to return a list with one item.
        if res and len(res) > 1:
            raise ValueError("Invalid JSON path. Expected only one result.")

        return None

    def delete_json(self, key: str, json_path="$") -> None:
        """Using JSON capability of Redis Stack.
        Deletes the value for the given key at the given JSONPath."""

        key = self._add_prefix(key, prefixes=[self.root_prefix])
        redis_client.json().delete(key, json_path)

    def _get_key_for_pydantic(
        self, key: str, model: BaseModel, use_persist_schema_as_prefix=True
    ) -> str:
        """Returns the key for the given key and model.
        If the model has `persist_schema` attribute, it will be used as prefix.
        """
        if use_persist_schema_as_prefix:
            schema = model.Config.schema_extra.get("persist_schema")
            if not schema:
                raise ValueError("persist_schema is not set in the model")
            return self._add_prefix(key, prefixes=[schema])

        return key

    def set_pydantic(
        self,
        key: str,
        model: BaseModel,
        json_path="$",
        use_persist_schema_as_prefix=True,
    ) -> None:
        """Sets the value for the given key at the given JSONPath."""

        key = self._get_key_for_pydantic(
            key, model, use_persist_schema_as_prefix
        )
        self.set_json(key, model.model_dump(), json_path)

    def get_pydantic(
        self,
        key: str,
        model: Type[BaseModel],
        json_path="$",
        use_persist_schema_as_prefix=True,
    ) -> BaseModel:
        """Returns the value for the given key at the given JSONPath."""

        key = self._get_key_for_pydantic(
            key, model, use_persist_schema_as_prefix
        )

        res = self.get_json(key, json_path)
        if res:
            return model(**res)

        return None

    def delete_pydantic(
        self,
        key: str,
        model: Type[BaseModel],
        json_path="$",
        use_persist_schema_as_prefix=True,
    ) -> None:
        """Deletes the value for the given key at the given JSONPath."""

        key = self._get_key_for_pydantic(
            key, model, use_persist_schema_as_prefix
        )
        self.delete_json(key, json_path)

    def _get_key_for_index(self, index_name: str) -> str:
        """Returns the key for the given index name.
        It will use root_prefix and index_prefix as prefixes.
        """
        return self._add_prefix(
            index_name, prefixes=[self.root_prefix, self.index_prefix]
        )

    def create_index_on_json(
        self,
        index_name: str,
        key_prefixes_to_index: List[str],
        schema: List[dict],
    ) -> None:
        """Creates an JSON index with the given schema.
        It will use all documents with the given prefix to create the index.

        `key_prefixes_to_index` is the list of prefixes for the json documents
        to be indexed. For example, if the documents are stored with the
        following keys:
        "root_prefix:mydocs:1", then key_prefixes_to_index = ["mydocs"]

        No need to include the root prefix. It will be added automatically.

        `schema` is a dict with the following format:
        {
            "field": "$.name",
            "type": "text|number|tag|geo",
            "alias": "name"
        }
        `type` by default is text. More on redis fields here:
        https://redis.io/docs/interact/search-and-query/basic-constructs/field-and-type-options/
        """

        if not schema:
            raise ValueError("schema is required")

        if not key_prefixes_to_index:
            raise ValueError("prefixes is required")

        # Convert the given schema to redis schema
        redis_schema = []
        for item in schema:
            # If type is not given, default to text
            field_type = item.get("type", "text")
            field_name = item["field"]

            if field_type == "text":
                redis_schema.append(
                    TextField(field_name, as_name=item["alias"])
                )
            elif field_type == "number":
                redis_schema.append(
                    NumericField(field_name, as_name=item["alias"])
                )
            elif field_type == "tag":
                redis_schema.append(
                    TagField(field_name, as_name=item["alias"])
                )
            elif field_type == "geo":
                redis_schema.append(
                    GeoField(field_name, as_name=item["alias"])
                )
            else:
                raise ValueError(f"Not supported type: {item['type']}")

        index_key = self._get_key_for_index(index_name)

        rs = redis_client.ft(index_key)

        # Add root prefix to the key prefixes
        for i, prefix in enumerate(key_prefixes_to_index):
            # Add prefixes in this format:
            # root_prefix + delimiter + prefix + delimiter
            key_prefixes_to_index[i] = self._add_prefix(
                "", prefixes=[self.root_prefix, prefix]
            )

        rs.create_index(
            redis_schema,
            definition=IndexDefinition(
                prefix=key_prefixes_to_index, index_type=IndexType.JSON
            ),
        )

    def delete_index(self, index_name: str) -> None:
        """Deletes the index for the given index name."""

        rs = redis_client.ft(self._get_key_for_index(index_name))
        rs.dropindex()

    def get_index_info(self, index_name):
        """Returns the index info for the given index name."""

        rs = redis_client.ft(self._get_key_for_index(index_name))
        try:
            res = rs.info()
            return res
        except redis.exceptions.ResponseError as ex:
            # If the message is "Unknown Index name", it means the index
            # doesn't exist. So, just return None without raising an error.
            if "Unknown Index name" in str(ex):
                return None

            raise ex

    def search_on_json(
        self,
        index_name: str,
        query: str,
        offset: int = 0,
        num: int = 10,
        sort_by_field: str = None,
        sort_asc: bool = True,
    ) -> List:
        """Searches the index for the given query."""

        rs = redis_client.ft(self._get_key_for_index(index_name))

        query_obj = Query(query).paging(offset, num)

        if sort_by_field:
            query_obj.sort_by(sort_by_field, asc=sort_asc)

        res = rs.search(query=query_obj)

        output = []
        if res and res.docs and len(res.docs) > 0:
            for doc in res.docs:
                if hasattr(doc, "json"):
                    output.append(json.loads(doc.json))
                else:
                    output.append(doc.__dict__)
            return output

        return output
