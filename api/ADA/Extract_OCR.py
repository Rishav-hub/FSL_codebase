from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from flask import Flask, jsonify, request
import torch.quantization
from  Xelp_OCR import *
from flask import jsonify
import gc
import sys
import time
gc.collect()
import logging

app = Flask(__name__)
app.logger.addHandler('OCR')
print("Looging")

try:
    base_processor = TrOCRProcessor.from_pretrained('D:/Xelp_work/FSL Project/Models/TrOCR_Base',local_files_only=True)
    b_model = VisionEncoderDecoderModel.from_pretrained('D:/Xelp_work/FSL Project/Models/TrOCR_Base',local_files_only=True)
    b_model_quantized=torch.quantization.quantize_dynamic(b_model, {torch.nn.Linear}, dtype=torch.qint8)
    del b_model
    gc.collect()
    logger.info("OCR Model Loaded")
except Exception as Model_error:
    logger.exception(Model_error)

@app.route('/ExtractClip', methods=['GET', 'POST'])
def ExtractClip():
    if request.method == 'POST':
        st = time.time()
        try:
            data = request.get_json(force=True)
            for x in range(len(data)):
                file_path = data["ClipData"][x]["FilePath"]
                logger.info("OCR Request received for the file"+"\n"+file_path+"\n")
                Page_no = data["ClipData"][x]["PageNo"]
                output_field_list = []
                for fl in range(len(data["ClipData"][x]["Fields"])):
                    All_fields = {"Data":" " ,"GroupName": " ","PageNo": " ", "FieldName": " ","RowNo":" ","Model": " ","Crds":{}, "Conf":[]}
                    field_coordinates = {}
                    All_fields["Data"]= data["ClipData"][x]["Fields"][fl]["Data"]
                    All_fields["GroupName"]= data["ClipData"][x]["Fields"][fl]["GroupName"]
                    All_fields["PageNo"]= data["ClipData"][x]["Fields"][fl]["PageNo"]
                    All_fields["FieldName"]= data["ClipData"][x]["Fields"][fl]["FieldName"]
                    All_fields["RowNo"]= data["ClipData"][x]["Fields"][fl]["RowNo"]
                    All_fields["Model"] = data["ClipData"][x]["Fields"][fl]["Model"]
                    All_fields["Conf"]= data["ClipData"][x]["Fields"][fl]["Conf"]
                    field_coordinates["x1"] = data["ClipData"][x]["Fields"][fl]["Crds"]["x1"]
                    field_coordinates["y1"] = data["ClipData"][x]["Fields"][fl]["Crds"]["y1"]
                    field_coordinates["x2"] = data["ClipData"][x]["Fields"][fl]["Crds"]["x2"]
                    field_coordinates["y2"] = data["ClipData"][x]["Fields"][fl]["Crds"]["y2"]
                    All_fields["Crds"] = field_coordinates
                    result_api_data=api_controller(file_path,All_fields,base_processor, b_model_quantized, base_processor, b_model_quantized)
                    All_fields["Data"] = result_api_data["Output_text"]
                    All_fields["Conf"] = result_api_data["Output_char_conf"]
                    output_field_list.append(All_fields)
                    
                result_api_data["FilePath"] = file_path
                result_api_data["PageNo"] = Page_no
            logger.info("File processed Successfully")   
            et = time.time()
            logger.info(f"Execution Time for One Request is {(et-st)/60} Minutes ") 
            return jsonify({"FilePath":result_api_data["FilePath"],
						"Fields":output_field_list })
            
        except Exception as  message:
            logger.exception(message)


if __name__ == '__main__':
	app.run(host='localhost',port='5000',debug=True)
