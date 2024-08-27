from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from typing import List
import json
import utils  # Make sure this imports the utils module correctly

app = FastAPI()

@app.post("/uploadfile/")
async def create_upload_file(files: List[UploadFile] = File(...)):
    recipes = []
    for file in files:
        try:
            data = utils.read_data(file.file)
            recipes.append(data)
        except json.JSONDecodeError:
            return JSONResponse(content={"error": "Invalid JSON data"}, status_code=400)
        except Exception as e:
            return JSONResponse(content={"error": str(e)}, status_code=500)

    return {"recipes": recipes}
