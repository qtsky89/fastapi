#!/bin/env python

from typing_extensions import Annotated
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
from enum import Enum


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: float | None = None


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items9/")
async def read_items(
    q: Annotated[
        str | None,
        Query(
            title="Query string",
            description="Query string for the items to search in the database that have a good match",
            min_length=3,
            alias="item-query",
            regex="^fixedquery$",
            deprecated=True,
        ),
    ] = None
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


@app.get("/files/{fp:path}")
def read_file(fp: str):
    return {"file_path": fp}


fake_item_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/items4/")
def read_item4(skip: int = 0, limit: int = 10):
    return fake_item_db[skip: skip + limit]


@app.post("/items/")
async def create_item(item: Item):
    return item


@app.get("/items2/")
async def read_items2(q: Annotated[str | None, Query(max_length=3)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/items3/")
async def read_items3(q: Annotated[list[str] | None, Query()] = None):
    query_items = {"q": q}
    return query_items
