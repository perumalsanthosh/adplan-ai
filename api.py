from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from adplan.core import parse_brief, optimize

app = FastAPI(title="AdPlan AI API", version="0.1.0")

class BriefRequest(BaseModel):
    text: str

@app.post("/plan")
def plan(request: BriefRequest):
    try:
        return optimize(parse_brief(request.text))
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
