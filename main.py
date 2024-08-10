from fastapi import FastAPI, Depends
import utils.models as models
from utils.database import engine
from sqlalchemy.orm import Session
from utils.utils import get_db
from routers import auth, address


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


app.include_router(auth.router)
app.include_router(address.router)