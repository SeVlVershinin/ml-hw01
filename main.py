import io
import os, csv
from io import BytesIO
from tempfile import NamedTemporaryFile

import uvicorn
from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
from typing import List
import pandas as pd
from starlette.background import BackgroundTask

from api.models import Item, Items
from models.model import Model

app = FastAPI()

model = Model()


@app.post("/predict_item")
def predict_item(item: Item) -> float:
    """Предсказывает цену одного автомобиля"""
    return model.predict(Items(objects=[item]))[0]


@app.post("/predict_items")
def predict_items(items: List[Item]) -> List[float]:
    """Предсказывает цену для автомобилей из списка"""
    return model.predict(Items(objects=items))


@app.post('/predict_items_from_csv_file')
def predict_items_from_uploaded_csv(file: UploadFile) -> FileResponse:
    """Позволяет загрузить CSV-файл c признаками автомобилей и возвращает CSV-файл,
    дополненный столбцом с предсказанием цены"""
    items: List[Item] = []
    with file.file as f:
        reader = csv.DictReader(io.TextIOWrapper(f))
        for row in reader:
            items.append(Item.model_validate(row))

    df = model.predict_and_return_raw(Items(objects=items))

    f = NamedTemporaryFile(delete=False)
    df.to_csv(f, index=False)

    return FileResponse(
        path=f.name,
        media_type='text/csv',
        filename='results.csv',
        background=BackgroundTask(os.remove, f.name)
    )


# uvicorn.run(app, host="0.0.0.0", port=80)
