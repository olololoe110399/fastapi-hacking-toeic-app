from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from server.model import ReadingSchema
from fitbert import FitBert

fb = FitBert()

router = APIRouter()

@router.post('/reading')
def result_reading(reading: ReadingSchema = Body(...))->dict:
    row = reading.dict()
    masked_string = str(row['question']).replace('___', '***mask***')
    options = list(row["options"])
    row['answer'] = fb.rank_with_prob(masked_string, options)[0][0]
    return row
    