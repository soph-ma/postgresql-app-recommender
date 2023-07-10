from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn

class FavouriteApp(BaseModel): 
    app: str

from db.db import DataBase

database = DataBase(csv_file="data/googleplaystore.csv")
app = FastAPI()

@app.get("/")
def check_connection() -> JSONResponse: 
    return JSONResponse({"connection": True})

@app.post("/feed_db") # if you want to refeed data for some reason
def feed_db() -> JSONResponse:
    database.feed_data()
    return JSONResponse({"DB status": "DB is fed."})

@app.get("/recommend_app")
def recommend_app(fav_app: FavouriteApp) -> JSONResponse: 
    results = database.get_relevant_apps(app_name=dict(fav_app)["app"])
    if len(results) == 0: 
        results = "We could not find any apps for you :("
    return JSONResponse({"results": results})

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8083, reload=True)