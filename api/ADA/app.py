import uvicorn
from fastapi import FastAPI, UploadFile, FastAPI, File, UploadFile, Form, HTTPException

from fastapi.responses import JSONResponse, FileResponse
from typing import Annotated, Optional, List

from fastapi import FastAPI, File, UploadFile, Form
import torch
import json, os

from extraction_util import run_ada_pipeline
from logger import ada_logger

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
CATEGORY_MAPPING_PATH = 'notes.json'
MODEL_PATH = './ROI_Model/ada__88.pth'

# Load a DONUT model
# model, preprocessor = load_donut_model()
# frcnn_predictor = DentalRoiPredictor(model_path = MODEL_PATH)


app = FastAPI()

@app.get("/")
async def root_route():
    return "Application working"

@app.post("/ada_extraction")

async def ml_extraction(data: dict):

    try:



        # Get the image path from the payload

        # image_file_path = data["ClipData"][0]['FilePath']



        # image_file_path = data.get('FilePath')
        ada_logger.info(f"Got request to API {data}")



        image_file_path = data.get('FilePath')

        ada_logger.info(f"Image file path in the server {image_file_path}")


        if not image_file_path:
            ada_logger.exception(f"FilePath field is required. Received filepath {image_file_path}")
            raise HTTPException(status_code=400, detail="FilePath field is required")



        if not os.path.exists(image_file_path):
            ada_logger.exception(f"File Not Found. Received filepath {image_file_path}")
            raise HTTPException(status_code=400, detail=f"File not found: {image_file_path}")



        result, error = run_ada_pipeline(image_file_path)



        if error:
            ada_logger.error(f"Error while processing ADA pipeline {error}")
            # If there's an error, raise HTTPException with status code 500 (Internal Server Error)

            raise HTTPException(status_code=500, detail=error)



        # If there's no error, return the result with file path

        response_data = {"file_path": data.get('FilePath'), "result": result['result']}

        return JSONResponse(content=response_data)



    except Exception as e:

        print(f"Error occured while processing {e} >>> ")
        ada_logger.error(f"Final ADA API error >>> {e}")
        return JSONResponse(

            status_code=500,

            content=f"Error while processing Extraction {e}"

        )


@app.post("/ada_extraction_v2")
async def ml_extraction(file: UploadFile = File(...)):

    try:

        # Read the contents of the uploaded file

        contents = await file.read()



        file_name = file.filename



        # Call the function to process the image file contents

        result, error = run_ada_pipeline(contents, file_name)



        if error:

            # If there's an error, raise HTTPException with status code 500 (Internal Server Error)

            raise HTTPException(status_code=500, detail=error)



        # print({"result": result['result']})

        # If there's no error, return the result

        response_data= {"result": result['result']}

        return JSONResponse(content=response_data)



    except Exception as e:
        print(e)
        print(f"Error occurred while processing {e}")

        # Return an error response

        return JSONResponse(

            status_code=500,

            content=f"Error while processing Extraction {e}"

        )


if __name__ == '__main__':
    uvicorn.run("app:app", host="0.0.0.0", port=8080)


