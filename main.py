from fastapi import FastAPI, Depends
import utils.models as models
from utils.database import engine
from sqlalchemy.orm import Session
from utils.utils import get_db


app = FastAPI()

models.Base.metadata.create_all(bind=engine)


@app.get('/')
async def home(db: Session = Depends(get_db)):
    try:
        records = db.query(models.Records) \
                .all()
        print(f"Fetched records: \n{records}")
    except Exception as e:
        print("Unable to fetch query")