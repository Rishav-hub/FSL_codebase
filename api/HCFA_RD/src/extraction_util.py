import json
import torch
import io
import torchvision
import pandas as pd
from torchvision.io import read_image
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torchvision.transforms import v2 as T
from PIL import Image
from torchvision import transforms
import pandas as pd
from transformers import AutoProcessor, VisionEncoderDecoderModel
import requests
import json
from PIL import Image
import torch
import argparse
# import os
import warnings
# from tqdm import tqdm


warnings.filterwarnings('ignore')

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
CATEGORY_MAPPING_PATH = r'D:\project\FSL\FSL_codebase\api\HCFA\artifacts\notes.json'
MODEL_PATH = r'D:\project\FSL\FSL_codebase\api\HCFA\artifacts\hcfa__94.pth'
HCFA_FORM_KEY_MAPPING = r"D:\project\FSL\FSL_codebase\api\HCFA\artifacts\HCFA_Keys_All.xlsx"
HCFA_AVERAGE_COORDINATE_PATH = r"D:\project\FSL\FSL_codebase\api\HCFA\artifacts\average_coordinates_hcfa.xlsx"
BBOX_HCFA_DONUT_Mapping_Dict = {
"10. IS PATIENT’S CONDITION RELATED TO:": ["10A_PatConditionEmpN", "10A_PatConditionEmpY", "10B_PatConditionAutoN",\
                                           "10B_PatConditionAutoY","10C_PatConditionOtherN","10C_PatConditionOtherY"],
"10D_Claim_Codes": "10D_ClaimCodes",
"11. INSURED’S POLICY GROUP OR FECA NUMBER": "11_PriInsPolGrpNumber",
"11. d. IS THERE ANOTHER HEALTH BENEFIT PLAN?": ["11D_PriInsOtherPlanN", "11D_PriInsOtherPlanY"],
"11A_Ins_DOB":  "11A_PriInsDOB",
"11B_Other_Claim_Id": ["11B_OtherClaimIdCode", "11B_OtherClaimIdCodeQual"],
"11C_Ins_Plan_Name": "11C_PriInsPlanName",
"12_Patient_Auth_Sign": "12_PatSignonFile",
"13. INSURED’S OR AUTHORIZED PERSON’S SIGNATURE":  "13_PriSignonFileList", 
"14. DATE OF CURRENT": ["14_PatCurrentDate","14_PatCurrentDateQual"],
"15_Other_Date": ["15_PatFirstDateOfIllQual"],
"16_Date": "16_Date",
"17. NAME OF REFERRING PHYSICIAN OR OTHER SOURCE": ["17_RefProvFullName", "17_RefProvOrgName"],
"17a. Qual": ["17A_RefProvOtherId", "17A_RefProvOtherIdQual"],
"17b. NPI": "17B_RefProvNPI",
"19. Additional Claim Information": ["19A_ProvCredential", "19A_ProvFName", "19A_ProvLName",\
                "19A_ProvMI", "19A_ProvPrefix", "19A_ProvFullNameQual", "19A_ProvSuffix", \
                "19B_ProvCredential", "19B_ProvFName", "19B_ProvLName", "19B_ProvMI",\
                "19B_ProvPrefix", "19B_ProvFullNameQual", "19B_ProvSuffix"],
"19_Hospitalization_Date": ['Box19B_Provider', 'Box19B_NPI', 'Box19A_QQ', 'Box19A_Provider', 'Box19A_NPI', '19_LocalUse'],
"1_InsType":  "1_InsType",
"1a. INSURED’S I.D. NUMBER": "1A_PriInsIDNumber",
"2. PATIENT’S NAME (Last Name, First Name, Middle Initial)": "2_PatFullName",
"20_Outside_Lab": ["20_Outside_Lab", "MissApp"],
"21. DIAGNOSIS OR NATURE OF ILLNESS OR INJURY.": ["21_DiagDescription","21_DiagCode", "21_ICDInd"],
"22. MEDICAID RESUBMISSION CODE and Original Ref No": ["22_MedicaidCode", "22_MedicaidRefNum"],
"23. PRIOR AUTHORIZATION NUMBER": "23_PriorAuthNum",
"24. Table": ["24_HCT", "24_MedicaidPaidAmount", "24_NDC", "24_NDCUnits", "24_NDCUnitsQual", "24_ProcDesc", \
              "24_ClmTaxAmount", "24A_FromDate", "24A_ToDate", "24B_POS", "24C_EMG", "24D_Modifier", "24D_ProcCode",\
                "24E_DiagPtr", "24F_LineCharges", "24G_Units", "24H_EPSDT", "24H_EPSDT1", "24J_RenProvNPIId", \
                "24J_RenProvOtherId", "24_ClmNYSurChargeAmount", "24_ClmDiscountAmount"],
"25. FEDERAL TAX I.D. NUMBER_SSN_EIN": ["25_BillProvFedIdCode", "25_BillProvEIN", "25_BillProvSSN"],
"26. PATIENT’S ACCOUNT NO.": "26_PatAcctNo", 
"27. ACCEPT ASSIGNMENT?": ["27_AcceptAssignmentN", "27_AcceptAssignmentY"],
"28. TOTAL CHARGE": "28_TotalCharges",
"29. AMOUNT PAID":"29_AmountPaid",
"3. PATIENT’S BIRTH DATE": ["3_PatSexF", "3_PatSexM", "3_PatDOB"],
"30_Reserved_NUCC": "30_BalanceDue",
"31. SIGNATURE OF PHYSICIAN OR SUPPLIER  INCLUDING DEGREES OR CREDENTIALS": ["31_RenProvTaxonomyCode", \
                                                                             "31_PrnRenProvFullName", "31_RenProvOrgName"],
"32. SERVICE FACILITY LOCATION INFORMATION": ["32_AmbToFacProvAddr1" ,"32_AmbToFacProvAddr2", "32_AmbToFacProvCity",\
                "32_AmbToFacProvCredential", "32_AmbToFacProvFName" , "32_AmbToFacProvFullPost", "32_AmbToFacProvLName",\
                "32_MedicaidTaxId", "32_AmbToFacProvMI", "32_AmbToFacProvNPIId", "32_AmbToFacProvOrgName", \
                "32_AmbToFacProvOtherId", "32_AmbToFacProvOtherIdFull", "32_AmbToFacProvPostCode", \
                "32_AmbToFacProvPostCode5", "32_AmbToFacProvPostCodeExt", "32_AmbToFacProvPrefix", "32_FacProvOrgName", \
                "32_FacProvAddr1", "32_FacProvCity", "32_FacProvCredential", "32_FacProvFName", "32_FacProvLName", \
                "32_FacProvMI", "32_FacProvNPIId", "32_FacProvOtherId", "32_FacProvOtherIdFull", "32_FacProvPostCode", \
                "32_FacProvPrefix", "32_FacProvState", "32_FacProvSuffix", "32_AmbToFacProvState", "32_AmbToFacProvSuffix"],
"32A_NPI_Code": "32_FacProvNPIId",
"32B_Code": "32_FacProvOtherId", 
"33. PHYSICIAN’S, SUPPLIER’S BILLING NAME, ADDRESS": ["33_BillProvAddr1", "33_BillProvCity","33_BillProvFullName",\
"33_MedicaidTaxId","33_MediBillProvAddr1","33_MediBillProvAddr2","33_MediBillProvCity","33_MediBillProvCredential",\
"33_MediBillProvFName","33_MediBillProvFullPost","33_MediBillProvLName","33_MediBillProvMI","33_MediBillProvNPIId",\
"33_MediBillProvOrgName","33_MediBillProvOtherId","33_MediBillProvOtherIdFull","33_MediBillProvPhone","33_MediBillProvPostCode",\
"33_MediBillProvPostCode5","33_MediBillProvPostCodeExt","33_MediBillProvPrefix","33_MediBillProvState","33_MediBillProvSuffix",\
"33_BillProvNPIId","33_BillProvOrgName","33_BillProvOtherIdFull","33_BillProvPhone","33_BillProvPostCode","33_BillProvState"],
"33. PHYSICIAN’S, SUPPLIER’S FullID": "33_BillProvOtherIdFull", 
"33. PHYSICIAN’S, SUPPLIER’S NPI": "33_BillProvNPIId",
"4. INSURED’S NAME (Last Name, First Name, Middle Initial)":"4_PriInsFullName",
"5. PATIENT’S ADDRESS (No., Street)":  "5_PatAddr1", 
"5. Pat_CITY": "5_PatCity", 
"5. Pat_STATE": "5_PatState", 
"5. Pat_ZIP CODE": "5_PatPostCode", 
"5_Telephone": "5_PatPhoneNumber", 
"6. PATIENT RELATIONSHIP TO INSURED": ["6_PatRelShipChild", "6_PatRelShipOther", "6_PatRelShipSelf", "6_PatRelShipSpouse"],
"7. INSURED’S ADDRESS (No., Street)": "7_PriInsAddr1", 
"7. Insurer_CITY":  "7_PriInsCity", 
"7. Insurer_STATE":"7_PriInsState", 
"7. Insurer_ZIP CODE": "7_PriInsPostCode", 
"7_Telephone": "7_PriInsPhoneNumber",
"8_Reserved_NUCC" :  ["8_PatEmpStatusCode", "8_PatStatus", "8_PatStatusMarried", "8_PatStatusOther", "8_PatStatusSingle", \
                      "8_PatStudent", "8_PatStudentStatusCodeFT", "8_PatStudentStatusCodePT"],
"9. a. OTHER INSURED’S POLICY OR GROUP NUMBER": "9A_SecInsPolGrpNumber",
"9. d. INSURANCE PLAN NAME OR PROGRAM NAME": "9D_SecInsPlanName",
"9B_Reserved_NUCC": ["9B_SecInsDOB", "9B_SecInsSexF", "9B_SecInsSexM"],
"9C_Reserved_NUCC" : ["9B_SecInsDOB", "9B_SecInsSexF", "9B_SecInsSexM"],
"9_Other_InsName": ["9_SecInsFName", "9_SecInsFullName", "9_SecInsLName", "9_SecInsMI", "9_SecInsPrefix", "9_SecInsSuffix"]
}

average_coordinates_hcfa_df = pd.read_excel(HCFA_AVERAGE_COORDINATE_PATH)
key_mapping = pd.read_excel(HCFA_FORM_KEY_MAPPING)
mapping_dict = key_mapping.set_index('Key_Name').to_dict()['Modified_key']
reverse_mapping_dict = {v: k for k, v in mapping_dict.items()}


class HCFARoiPredictor:
    def __init__(self, model_path, category_mapping_path=CATEGORY_MAPPING_PATH):
        self.category_mapping = self._load_category_mapping(category_mapping_path)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self._load_model(model_path)
        self.transform = self._get_transforms()

    def _load_model(self, model_path):
        model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
        num_classes = len(self.category_mapping) + 1
        in_features = model.roi_heads.box_predictor.cls_score.in_features
        model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)
        model.load_state_dict(torch.load(model_path, map_location=self.device))
        return model

    def _load_category_mapping(self, category_mapping_path):
        with open(category_mapping_path) as f:
            return {c['id'] + 1: c['name'] for c in json.load(f)['categories']}

    def _get_transforms(self):
        return T.Compose([T.ToDtype(torch.float, scale=True), T.ToPureTensor()])

    def _apply_nms(self, orig_prediction, iou_thresh=0.3):
        keep = torchvision.ops.nms(
            orig_prediction['boxes'], orig_prediction['scores'], iou_thresh)
        final_prediction = orig_prediction
        final_prediction['boxes'] = final_prediction['boxes'][keep]
        final_prediction['scores'] = final_prediction['scores'][keep]
        final_prediction['labels'] = final_prediction['labels'][keep]
        return final_prediction

    def _postprocessing_annotation(self, infer_df):
        # APPLYING Post prrocessing
        # Calculate mean values for specific labels
        xmin_24_table = infer_df.loc[infer_df['class_name'] == '9. d. INSURANCE PLAN NAME OR PROGRAM NAME', 'x0'].mean()
        xmax_patient_birth_date = infer_df.loc[infer_df['class_name'] == '3. PATIENT’S BIRTH DATE', 'x1'].mean()
        xmax_21_diagnosis_or_nature_of_illness = infer_df.loc[infer_df['class_name'] == '21. DIAGNOSIS OR NATURE OF ILLNESS OR INJURY.', 'x1'].mean()
        # 1a. INSURED’S I.D. NUMBER
        xmax_1a_insured_id_number = infer_df.loc[infer_df['class_name'] == '1a. INSURED’S I.D. NUMBER', 'x1'].mean()


        # Apply post-processing for '1_InsType' class
        infer_df.loc[(infer_df['class_name'] == '1_InsType'), 'x0'] = xmin_24_table
        infer_df.loc[(infer_df['class_name'] == '1_InsType'), 'x1'] = xmax_patient_birth_date

        # Apply post-processing for '35_Remarks' class
        infer_df.loc[(infer_df['class_name'] == '12_Patient_Auth_Sign'), 'x0'] = xmin_24_table
        infer_df.loc[(infer_df['class_name'] == '12_Patient_Auth_Sign'), 'x1'] = xmax_patient_birth_date

        infer_df.loc[(infer_df['class_name'] == '21. DIAGNOSIS OR NATURE OF ILLNESS OR INJURY.'), 'x0'] = xmin_24_table
        infer_df.loc[(infer_df['class_name'] == '21. DIAGNOSIS OR NATURE OF ILLNESS OR INJURY.'), 'x1'] = xmax_patient_birth_date

        infer_df.loc[(infer_df['class_name'] == '19. Additional Claim Information'), 'x0'] = xmin_24_table
        infer_df.loc[(infer_df['class_name'] == '19. Additional Claim Information'), 'x1'] = xmax_patient_birth_date

        # 24. Table
        infer_df.loc[(infer_df['class_name'] == '24. Table'), 'x0'] = xmin_24_table
        infer_df.loc[(infer_df['class_name'] == '24. Table'), 'x1'] = xmax_1a_insured_id_number
        return infer_df

    def predict_image(self, image):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.eval().to(device)
        # pil_image = Image.open(image_path)
        # to_tensor = transforms.ToTensor()
        # image = to_tensor(pil_image)
        image_tensor = self.transform(image).unsqueeze(0).to(device)
        with torch.no_grad():
            predictions = self.model(image_tensor)
        return predictions

    def predict_and_get_dataframe(self, image_path, image,  iou_thresh=0.5):
        predictions = self.predict_image(image)
        pred = predictions[0]
        pred_nms = self._apply_nms(pred, iou_thresh=iou_thresh)

        pred_dict = {
            'boxes': pred_nms['boxes'].cpu().numpy(),
            'labels': pred_nms['labels'].cpu().numpy(),
            'scores': pred_nms['scores'].cpu().numpy()
        }

        boxes_flat = pred_dict['boxes'].reshape(-1, 4)
        labels_flat = pred_dict['labels'].reshape(-1)
        scores_flat = pred_dict['scores'].reshape(-1)

        class_names = [self.category_mapping[label_id] for label_id in labels_flat]
        num_predictions = len(boxes_flat)
        file_name = [image_path.split(".")[0]] * num_predictions
        # file_name = [image_path] * num_predictions


        infer_df = pd.DataFrame({
            'file_name': file_name,
            'x0': boxes_flat[:, 0],
            'y0': boxes_flat[:, 1],
            'x1': boxes_flat[:, 2],
            'y1': boxes_flat[:, 3],
            'label': labels_flat,
            'class_name': class_names,
            'score': scores_flat
        })

        post_processed_df = self._postprocessing_annotation(infer_df)
        return post_processed_df

# Load the RPI model
frcnn_predictor = HCFARoiPredictor(MODEL_PATH)


def roi_model_inference(image_path, image):
    result_df = frcnn_predictor.predict_and_get_dataframe(image_path, image)
    max_score_indices = result_df.groupby('class_name')['score'].idxmax()
    result_df = result_df.loc[max_score_indices]
    return result_df

def run_prediction_donut(image, model, processor):
    pixel_values = processor(image, return_tensors="pt").pixel_values
    task_prompt = "<s>"
    decoder_input_ids = processor.tokenizer(task_prompt, add_special_tokens=False, return_tensors="pt").input_ids

    outputs = model.generate(
        pixel_values.to(device),
        decoder_input_ids=decoder_input_ids.to(device),
        max_length=model.decoder.config.max_position_embeddings,
        early_stopping=True,
        pad_token_id=processor.tokenizer.pad_token_id,
        eos_token_id=processor.tokenizer.eos_token_id,
        use_cache=True,
        num_beams=2,
        epsilon_cutoff=6e-4,
        bad_words_ids=[[processor.tokenizer.unk_token_id]],
        return_dict_in_generate=True,
    )
    prediction = processor.batch_decode(outputs.sequences)[0]
    prediction = prediction.replace("<one>", "1")
    prediction = processor.token2json(prediction)
    return prediction, outputs

def split_and_expand(row):
    if row['Key'] == "33_Missing_Teeth":
        keys = [row['Key']]
        values = row['Value'].split(';')[0]
    else:
        keys = [row['Key']] * len(row['Value'].split(';'))
        values = row['Value'].split(';')
    return pd.DataFrame({'Key': keys, 'Value': values})


def load_model(device):
    try:
        processor = AutoProcessor.from_pretrained("Laskari-Naveen/HCFA_99")
        model = VisionEncoderDecoderModel.from_pretrained("Laskari-Naveen/HCFA_99")
        model.eval().to(device)
        print("Model loaded successfully")
    except:
        print("Model Loading failed !!!")
    return processor, model


def convert_hcfa_predictions_to_df(prediction):
    expanded_df = pd.DataFrame()
    result_df_each_image = pd.DataFrame()    
    each_image_output = pd.DataFrame(list(prediction.items()), columns=["Key", "Value"])
    try:    
        expanded_df = pd.DataFrame(columns=['Key', 'Value'])
        for index, row in each_image_output[each_image_output['Value'].str.contains(';')].iterrows():
            expanded_df = pd.concat([expanded_df, pd.DataFrame(split_and_expand(row))], ignore_index=True)

        result_df_each_image = pd.concat([each_image_output, expanded_df], ignore_index=True)
        result_df_each_image = result_df_each_image.drop(result_df_each_image[result_df_each_image['Value'].str.contains(';')].index)

        for old_key, new_key in reverse_mapping_dict.items():
            result_df_each_image["Key"].replace(old_key, new_key, inplace=True)
    except Exception as e:
        pass
        
    return result_df_each_image

# def plot_bounding_boxes(image, df, enable_title = False):
#     image = image.permute(1,2,0)
#     colors = ['red', 'blue', 'green', 'orange', 'purple', 'magenta', 'brown']
#     fig, ax = plt.subplots(1, figsize=(50, 50))
#     ax.set_aspect('auto')
#     ax.imshow(image)
#     for index, row in df.iterrows():
#         class_name = row['class_name']
#         x0, y0, x1, y1 = row['x0'], row['y0'], row['x1'], row['y1']
#         box_color = random.choice(colors)
#         rect = patches.Rectangle((x0, y0), x1 - x0, y1 - y0, linewidth=1.5, edgecolor=box_color, facecolor='none')
#         ax.add_patch(rect)

#         if enable_title:
#             ax.text(x0, y0, class_name, color=box_color, fontsize=9, weight='bold')
#     ax.axis('off')
#     plt.show()

def map_result1(dict1, dict2):
    result_dict_1 = {}
    for key, value in dict1.items():
        if key in dict2:
            mapping_keys = dict2[key] if isinstance(dict2[key], list) else [dict2[key]]
            for mapping_key in mapping_keys:
                result_dict_1[mapping_key] = value
    return result_dict_1

def map_result2(dict1, dict2):
    result_dict_2 = {}
    for key, value in dict1.items():
        if key in dict2:
            mapping_keys = dict2[key] if isinstance(dict2[key], list) else [dict2[key]]
            for mapping_key in mapping_keys:
                result_dict_2[key] = {
                    "Mapping_key": mapping_keys,
                    "coordinates": value
                }
    return result_dict_2

def map_result1_final_output(result_dict_1, additional_info_dict):
    updated_result_dict_1 = {}

    # Iterate over additional_info_dict
    for key, additional_info in additional_info_dict.items():
        # Check if the key exists in result_dict_1
        if key in result_dict_1:
            coordinates = result_dict_1[key]
        else:
            # If the key is missing in result_dict_1, set coordinates to None
            coordinates = None

        # Store the coordinates and additional_info in updated_result_dict_1
        updated_result_dict_1[key] = {"coordinates": coordinates, "text": additional_info}

    return updated_result_dict_1

# def run_application(input_image_folder, output_ROI_folder, output_extraction_folder):
#     root = os.getcwd()
#     os.makedirs(output_ROI_folder, exist_ok=True)
#     os.makedirs(output_extraction_folder, exist_ok=True)
#     # image_list = os.listdir(os.path.join(root, input_image_folder))
#     image_list = os.listdir(input_image_folder)
#     for each_image in tqdm(image_list):
#         image_path = os.path.join(input_image_folder, each_image)
#         pil_image = Image.open(image_path).convert('RGB')
#         to_tensor = transforms.ToTensor()
#         image = to_tensor(pil_image)
        
#         print("Staring ROI extraction")
#         # print(uploaded_file.)
#         fasterrcnn_result_df = roi_model_inference(image_path, image)
#         print("Staring data extraction")
#         prediction, output = run_prediction_donut(image, model, processor)
#         extraction_df = convert_predictions_to_df(prediction)

#         output_ROI_path = os.path.join(root, output_ROI_folder,each_image.split(".")[0]+".xlsx" )
#         fasterrcnn_result_df.to_excel(output_ROI_path, index=False)

#         output_extraction_path = os.path.join(root, output_extraction_folder, each_image.split(".")[0]+".xlsx" )
#         extraction_df.to_excel(output_extraction_path, index=False)


# Load the models
processor, model = load_model(device)



def run_hcfa_pipeline(image_path: str):
    try:
        # image_path = os.path.join(input_image_folder, each_image)
        pil_image = Image.open(image_path).convert('RGB')
        # pil_image = Image.open(io.BytesIO(image_path)).convert('RGB')
        to_tensor = transforms.ToTensor()
        image = to_tensor(pil_image)
        prediction, output = run_prediction_donut(pil_image, model, processor)
        donut_out = convert_hcfa_predictions_to_df(prediction)

        # What is this? Is it Mapping the donut keys to XML values? Can't understand.
        # for old_key, new_key in reverse_mapping_dict.items():
        #     donut_out["Key"].replace(old_key, new_key, inplace=True)

        # This is just converting the dataframe to dictionary
        json_data = donut_out.to_json(orient='records')
        data_list = json.loads(json_data)
        # output_dict_donut = {item['Key']: item['Value'] for item in data_list}

        output_dict_donut = {}

        # Iterate through the data_list
        for item in data_list:
            key = item['Key']
            value = item['Value']

            # Check if the key already exists in the output dictionary
            if key in output_dict_donut:
                # If the key exists, append the value to the list of dictionaries
                output_dict_donut[key].append({'value': value})
            else:
                # If the key doesn't exist, create a new list with the current value
                output_dict_donut[key] = [{'value': value}]

        # This is just doing the ROI inference and converting DF to dict
        res = roi_model_inference(image_path, image)
        df_dict = res.to_dict(orient='records')

        # Implementing the average part here

        # Convert the average coordinates DataFrame to a dictionary for easy access
        average_coordinates_dict = average_coordinates_hcfa_df.set_index('label').to_dict(orient='index')

        # Get all unique class names
        all_class_names = set(average_coordinates_hcfa_df['label'])

        # Initialize the output dictionary
        output_dict_det = {}

        # Iterate over all class names
        for class_name in all_class_names:
            # Check if the class name exists in df_dict
            item = next((item for item in df_dict if item['class_name'] == class_name), None)
            if item:
                # If the class name exists, use the coordinates from df_dict
                x1, y1, x2, y2 = item['x0'], item['y0'], item['x1'], item['y1']
            else:
                # If the class name doesn't exist, replace coordinates with average coordinates
                avg_coords = average_coordinates_dict.get(class_name, None)
                if avg_coords:
                    x1 = avg_coords['xmin']
                    y1 = avg_coords['ymin']
                    x2 = avg_coords['xmax']
                    y2 = avg_coords['ymax']
                else:
                    # If average coordinates are not available, set coordinates to NaN
                    x1, y1, x2, y2 = float('nan'), float('nan'), float('nan'), float('nan')

            # Store the coordinates in the output dictionary
            output_dict_det[class_name] = {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2}

        # Map the ROI keys with the Donut keys
        result_dict_1 = map_result1(output_dict_det, BBOX_HCFA_DONUT_Mapping_Dict)
        # result_dict_2 = map_result2(output_dict_det, BBOX_DONUT_Mapping_Dict)
        final_mapping_dict  = map_result1_final_output(result_dict_1, output_dict_donut)

        return {"result": final_mapping_dict}, None
    except Exception as e:
        return None, str(e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Your application description")
    parser.add_argument("input_image_folder", help="Path to the input image folder")
    parser.add_argument("output_ROI_folder", help="Path to the output ROI folder")
    parser.add_argument("output_extraction_folder", help="Path to the output extraction folder")
    args = parser.parse_args()
    processor, model = load_model(device)
    # run_application(args.input_image_folder, args.output_ROI_folder, args.output_extraction_folder)