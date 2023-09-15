import os
from pydantic import BaseModel
from pymongo import MongoClient
from pymongo.collection import Collection

mongo_client = MongoClient(os.environ.get("MONGODB_URL"))


class MongoDataStore:
    """This class is using pymongo to connect to the MongoDB database.

    MongoClient object is directly accessible via the `client` attribute.
    MongoClient uses the Mongo URL set as MONGODB_URL environment variable.
    """

    def __init__(
        self,
        db_name: str,
    ):
        self.client = mongo_client
        self.db = self.client[db_name]

    def collection(self, collection_name: str) -> Collection:
        return self.db[collection_name]

    def collection_for_pydantic(
        self,
        model_cls: BaseModel,
        use_persist_schema_as_name=False,
    ) -> Collection:
        """Create a Collection object based on the pydantic model."""
        if use_persist_schema_as_name:
            schema = model_cls.Config.schema_extra.get("persist_schema")
            if not schema:
                raise ValueError("persist_schema is not set for the model")
            collection_name = schema
        else:
            collection_name = model_cls.__name__.lower()

        return self.db[collection_name]
