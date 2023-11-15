from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pyaspeller import YandexSpeller


def process_str(str):
    speller = YandexSpeller()
    fixed = speller.spelled(str)
    orig_words = str.split()
    fixed_words = fixed.split()
    number_of_words = len([(x, y) for x, y in zip(orig_words, fixed_words) if x != y])
    correction = [(x, y) for x, y in zip(orig_words, fixed_words) if x != y]
    return number_of_words, correction

app = FastAPI()

class InputData(BaseModel):
    input_string: str

class OutputData(BaseModel):
    number_of_words: int
    correction: list

@app.get("/")
async def root():
    return {"message": "Hello, I`m alive"}


@app.post("/process_str", response_model=OutputData)
async def process_string(data: InputData):
    try:
        result = process_str(data.input_string)
        return OutputData(number_of_words=result[0], correction=result[1])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))