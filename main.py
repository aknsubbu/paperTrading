from typing import Union

from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/checkUpLink")
def read_upLink():
    return {"upLink": "Up Link is active"}


