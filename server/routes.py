from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from server.model import ReadingSchema
from server.fillbert import TOEICBert
import re

Bertmodel = 'bert-large-uncased'
model = TOEICBert(Bertmodel)
router = APIRouter()

@router.post('/reading')
def result_reading(reading: ReadingSchema = Body(...)) -> dict:
    row = reading.dict()
    print(row)
    questions = row['question'].replace('\r', '').split('\n')
    row['question'] = questions[0].strip()
    question_list = []
    for e  in questions[1:]:
        print(e)
        question_list.append(re.sub(
            '</?.*?>', '', e.replace('(', '<').replace(')', '>')).strip())
    row['options'] = question_list
    predict_anwser = model.predict(row)
    row['anwser'] = predict_anwser
    return row
