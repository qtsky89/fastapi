#!/bin/env python

from typing_extensions import Annotated
from fastapi import FastAPI, Query
from pydantic import BaseModel
from enum import Enum


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None


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


# testing comments
@app.get("/items/{item_id}")
def read_items(item_id: int):
    ret = [Item(name="wonzzang", price=20.3, is_offer=True), Item(name="wonzzang2", price=40.3, is_offer=False)]

    return {"data": ret}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


@app.get("/files/{fp:path}")
def read_file(fp: str):
    return {"file_path": fp}


fake_item_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/items/")
def read_item(skip: int = 0, limit: int = 10):
    return fake_item_db[skip: skip + limit]


@app.post("/items/")
async def create_item(item: Item):
    return item


@app.get("/items2/")
async def read_items(q: Annotated[str | None, Query(max_length=3)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/items3/")
async def read_items3(q: Annotated[list[str] | None, Query()] = None):
    query_items = {"q": q}
    return query_items
