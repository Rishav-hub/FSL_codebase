import uvicorn
from fastapi import FastAPI, UploadFile, FastAPI, File, UploadFile, Form, HTTPException

from fastapi.responses import JSONResponse, FileResponse
from typing import Annotated, Optional, List

from fastapi import FastAPI, File, UploadFile, Form
import torch
import json, os

from extraction_util import run_hcfa_pipeline

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

app = FastAPI()

@app.get("/")
async def root_route():
    return "Application working"

@app.post("/hcfa_extraction")
async def ml_extraction(file: UploadFile = File(...)):
    try:
        # Read the contents of the uploaded file
        contents = await file.read()

        file_name = file.filename

        # Call the function to process the image file contents
        result, error = run_hcfa_pipeline(contents, file_name)

        if error:
            # If there's an error, raise HTTPException with status code 500 (Internal Server Error)
            raise HTTPException(status_code=500, detail=error)

        # print({"result": result['result']})
        # If there's no error, return the result
        response_data= {"result": result['result']}
        return JSONResponse(content=response_data)

    except Exception as e:
        print(f"Error occurred while processing {e}")
        # Return an error response
        return JSONResponse(
            status_code=500,
            content=f"Error while processing Extraction {e}"
        )

if __name__ == '__main__':
    uvicorn.run("app:app", host="0.0.0.0", port=5001)

