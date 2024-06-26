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
CATEGORY_MAPPING_PATH = r'D:\project\FSL\FSL_codebase\api\HCFA\artifacts\hcfa_rd_notes_grouped_v2.json'
HCFA_RD_MODEL_PATH = r'D:\project\FSL\FSL_codebase\api\HCFA\artifacts\hcfa_rd_grouped_30.pth'
HCFA_FORM_KEY_MAPPING = r"D:\project\FSL\FSL_codebase\api\HCFA\artifacts\HCFA_Keys_All.xlsx"
HCFA_AVERAGE_COORDINATE_PATH = r"D:\project\FSL\FSL_codebase\api\HCFA\artifacts\average_coordinates_hcfa.xlsx"
group_key_mapping_dict = {'1_class': ['1A_PriInsIDNumber'],
 '2_class': ['2_PatFullName'],
 '3_class': ['3_PatDOB', '3_PatSexM', '3_PatSexF'],
 '5_class': ['5_PatAddr1',
  '5_PatCity',
  '5_PatState',
  '5_PatPostCode',
  '5_PatPhoneNumber'],
 '4_class': ['4_PriInsFullName'],
 '7_class': ['7_PriInsAddr1',
  '7_PriInsCity',
  '7_PriInsState',
  '7_PriInsPostCode',
  '7_PriInsPhoneNumber'],
 '9_class': ['9_SecInsFullName',
  '9A_SecInsPolGrpNumber',
  '9B_SecInsDOB',
  '9D_SecInsPlanName',
  '9B_SecInsSexM',
  '9B_SecInsSexF'],
 '10_class': ['10D_ClaimCodes',
  '10A_PatConditionEmpN',
  '10A_PatConditionEmpY',
  '10B_PatConditionAutoN',
  '10B_PatConditionAutoY',
  '10C_PatConditionOtherN',
  '10C_PatConditionOtherY'],
 '11_class': ['11_PriInsPolGrpNumber',
  '11A_PriInsDOB',
  '11B_OtherClaimIdCodeQual',
  '11C_PriInsPlanName',
  '11D_PriInsOtherPlanN',
  '11D_PriInsOtherPlanY'],
 '12_class': ['12_PatSignonFile'],
 '13_class': ['13_PriSignonFileList'],
 '14_class': ['14_PatCurrentDate'],
 '15_class': ['15_PatFirstDateOfIllQual'],
 '17_class': ['17A_RefProvOtherIdQual',
  '17A_RefProvOtherId',
  '17B_RefProvNPI',
  '17_RefProvOrgName'],
 '21_class': ['21_ICDInd', '21_DiagCode'],
 '22_class': ['22_MedicaidCode', '22_MedicaidRefNum'],
 '23_class': ['23_PriorAuthNum'],
 '24_class': ['24A_FromDate',
  '24A_ToDate',
  '24B_POS',
  '24C_EMG',
  '24D_ProcCode',
  '24_ProcDesc',
  '24D_Modifier',
  '24E_DiagPtr',
  '24F_LineCharges',
  '24G_Units',
  '24H_EPSDT',
  '24H_EPSDT1',
  '24J_RenProvNPIId',
  '24_ClmDiscountAmount',
  '24_MedicaidPaidAmount'],
 '25_class': ['25_BillProvFedIdCode', '25_BillProvSSN', '25_BillProvEIN'],
 '26_class': ['26_PatAcctNo'],
 '28_class': ['28_TotalCharges'],
 '31_class': ['31_PrnRenProvFullName', '31_RenProvOrgName'],
 '32_class': ['32_FacProvOrgName',
  '32_FacProvAddr1',
  '32_FacProvCity',
  '32_FacProvState',
  '32_FacProvPostCode',
  '32_FacProvNPIId',
  '32_FacProvOtherIdFull',
  '32_FacProvOtherId'],
 '33_class': ['33_BillProvOrgName',
  '33_BillProvFullName',
  '33_BillProvAddr1',
  '33_BillProvCity',
  '33_BillProvState',
  '33_BillProvPostCode',
  '33_BillProvPhone',
  '33_BillProvNPIId',
  '33_BillProvOtherIdFull'],
 '6_class': ['6_PatRelShipSelf', '6_PatRelShipSpouse', '6_PatRelShipChild'],
 '8_class': ['8_PatStatusSingle',
  '8_PatStatusMarried',
  '8_PatStatusOther',
  '8_PatEmpStatusCode',
  '8_PatStudentStatusCodeFT',
  '8_PatStudentStatusCodePT'],
 '27_class': ['27_AcceptAssignmentN', '27_AcceptAssignmentY'],
 '19_class': ['19_LocalUse']}

mapping_overlaps = {'8_PatStatus': ['8_PatStudent'],
  '19_LocalUse': ['19_LocalUse'],
  'Box19A_QQ': ['Box19A_QQ', 'Box19A_NPI',
  'Box19A_Provider',
  '19A_ProvFullNameQual',
  '19A_ProvLName',
  '19A_ProvFName',
  '19A_ProvMI',
  '19A_ProvSuffix',
  '19A_ProvPrefix',
  '19A_ProvCredential',
  'Box19B_NPI',
  'Box19B_Provider',
  '19B_ProvFullNameQual',
  '19B_ProvLName',
  '19B_ProvFName',
  '19B_ProvMI',
  '19B_ProvSuffix',
  '19B_ProvPrefix',
  '19B_ProvCredential'],
 '14_PatCurrentDate': ['14_PatCurrentDateQual'],
 '31_RenProvOrgName': ['31_RenProvTaxonomyCode'],
 '17_RefProvOrgName': ['17_RefProvFullName'],
 '9_SecInsFullName': ['9_SecInsLName',
  '9_SecInsFName',
  '9_SecInsMI',
  '9_SecInsSuffix',
  '9_SecInsPrefix'],
 '24_ClmDiscountAmount': ['24_ClmTaxAmount', '24_ClmNYSurChargeAmount'],
 '24H_EPSDT1': ['24_NDC', '24_NDCUnitsQual', '24_NDCUnits', 'MissApp'],
 '21_DiagCode': ['21_DiagDescription'],
 '32_FacProvOrgName': ['32_FacProvLName',
  '32_FacProvFName',
  '32_FacProvMI',
  '32_FacProvSuffix',
  '32_FacProvPrefix',
  '32_FacProvCredential'],
 '32_FacProvOtherId': ['32_AmbToFacProvOrgName',
  '32_AmbToFacProvLName',
  '32_AmbToFacProvFName',
  '32_AmbToFacProvMI',
  '32_AmbToFacProvSuffix',
  '32_AmbToFacProvPrefix',
  '32_AmbToFacProvCredential',
  '32_AmbToFacProvAddr1',
  '32_AmbToFacProvAddr2',
  '32_AmbToFacProvCity',
  '32_AmbToFacProvState',
  '32_AmbToFacProvPostCode',
  '32_AmbToFacProvPostCode5',
  '32_AmbToFacProvPostCodeExt',
  '32_AmbToFacProvFullPost',
  '32_AmbToFacProvNPIId',
  '32_AmbToFacProvOtherIdFull',
  '32_AmbToFacProvOtherId'],
 '6_PatRelShipSpouse': ['6_PatRelShipOther'],
 '28_TotalCharges': ['29_AmountPaid', '30_BalanceDue'],
 '11B_OtherClaimIdCodeQual': ['11B_OtherClaimIdCode'],
 '33_BillProvFullName': ['33_MediBillProvOrgName',
  '33_MediBillProvLName',
  '33_MediBillProvFName',
  '33_MediBillProvMI',
  '33_MediBillProvSuffix',
  '33_MediBillProvPrefix',
  '33_MediBillProvCredential',
  '33_MediBillProvAddr1',
  '33_MediBillProvAddr2',
  '33_MediBillProvCity',
  '33_MediBillProvState',
  '33_MediBillProvPostCode',
  '33_MediBillProvPostCode5',
  '33_MediBillProvPostCodeExt',
  '33_MediBillProvFullPost',
  '33_MediBillProvPhone',
  '33_MediBillProvNPIId',
  '33_MediBillProvOtherIdFull',
  '33_MediBillProvOtherId',
  '33_MedicaidTaxId'],
 '24H_EPSDT': ['24J_RenProvOtherId'],
 '24_ProcDesc': ['24_HCT']
}

average_coordinates_hcfa_df = pd.read_excel(HCFA_AVERAGE_COORDINATE_PATH)
key_mapping = pd.read_excel(HCFA_FORM_KEY_MAPPING)
mapping_dict = key_mapping.set_index('Key_Name').to_dict()['Modified_key']
reverse_mapping_dict = {v: k for k, v in mapping_dict.items()}


import json

class HCFARDRoiPredictor:
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
            return {c['id']: c['name'] for c in json.load(f)['categories']}

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
        if len(infer_df[infer_df['class_name'] == "23_class"]) == 0:
          # print(f"working on {image_path}")
          # Select rows with class 22_label
          print("Post processing class 23")
          class_22_rows = infer_df[infer_df['class_name'] == "22_class"]

          # Create a new DataFrame with label set to 23_label
          new_rows = class_22_rows.copy()
          new_rows['class_name'] = "23_class"

          # Append the new rows to the original DataFrame
          infer_df = pd.concat([infer_df, new_rows], ignore_index=True)

        return infer_df

    def predict_image(self, image):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.eval().to(device)
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

        infer_df = self._postprocessing_annotation(infer_df)
        return infer_df

# Load the RPI model
frcnn_predictor_hcfa_rd = HCFARDRoiPredictor(model_path = HCFA_RD_MODEL_PATH)


def roi_model_inference(image_path, image,):
    result_df = frcnn_predictor_hcfa_rd.predict_and_get_dataframe(image_path, image)
    max_score_indices = result_df.groupby('class_name')['score'].idxmax()
    result_df = result_df.loc[max_score_indices]
#     print("DataFrame", result_df[["class_name", "x0", "x1", "y0", "y1"]])
    result_df = result_df[["class_name", "x0", "x1", "y0", "y1"]]
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
        processor = AutoProcessor.from_pretrained("Laskari-Naveen/hcfa_rd_v1")
        model = VisionEncoderDecoderModel.from_pretrained("Laskari-Naveen/hcfa_rd_v1")
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
        print(f"Error occuring in convert_hcfa_predictions_to_df {e}")
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

def run_hcfa_rd_pipeline(image_path: str):
    try:

        print("got the image")
        # image_path = os.path.join(input_image_folder, each_image)
        pil_image = Image.open(image_path).convert('RGB')
        # pil_image = Image.open(io.BytesIO(image_path)).convert('RGB')
        image_height, image_width = pil_image.size[0], pil_image.size[1]
        to_tensor = transforms.ToTensor()
        image = to_tensor(pil_image)
        print("Converted to tensor")
        prediction, output = run_prediction_donut(pil_image, model, processor)
        donut_out = convert_hcfa_predictions_to_df(prediction)

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
        print("Startign ROI inference")
        res = roi_model_inference(image_path, image)
        df_dict = res.to_dict(orient='records')

        # print(f"Printing class 23 value {df_dict['23_class']}")
        # Path to the output JSON file

        # Implementing the average part here

        # # Convert the average coordinates DataFrame to a dictionary for easy access
        # average_coordinates_dict = average_coordinates_hcfa_df.set_index('label').to_dict(orient='index')

        # # Get all unique class names
        # all_class_names = set(average_coordinates_hcfa_df['label'])

        # Initialize the output dictionary
        output_dict_det = {}

        for item in df_dict:
            class_name = item['class_name']
            x1, y1, x2, y2 = item['x0'], item['y0'], item['x1'], item['y1']
            output_dict_det[class_name] = {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2}

        # print("output_dict_det --->>", output_dict_det)
        # Map the ROI keys with the Donut keys
        result_dict_1 = map_result1(output_dict_det, group_key_mapping_dict)
        # print("result_dict_1  ---->>", result_dict_1)

        print("Processing result_dict_2 --->>>")
        result_dict_2 = map_result1(result_dict_1, mapping_overlaps)


        apply_19_key_post_processing = ['Box19A_Provider', '19B_ProvCredential', '19B_ProvSuffix', 'Box19B_Provider', '19B_ProvLName', '19A_ProvMI', '19A_ProvSuffix', '19A_ProvPrefix', 'Box19B_NPI', '19A_ProvLName', '19B_ProvMI', '19B_ProvFName', '19B_ProvFullNameQual', '19A_ProvFName', '19B_ProvPrefix', '19A_ProvFullNameQual', 'Box19A_QQ', "Box19B_QQ'", '19A_ProvCredential', 'Box19A_NPI']
        apply_8_pat_key_post_processing = ["8_PatStatus", "8_PatStudent"]

        for missing_keys in apply_19_key_post_processing:
          result_dict_2[missing_keys] = {'x1': 1, 'y1': 1, 'x2': 100, 'y2': 100}

        for missing_keys in apply_8_pat_key_post_processing:
          result_dict_2[missing_keys] = {'x1': 0, 'y1': 0, 'x2': 0, 'y2': 0}

        result_dict_2["32_MedicaidTaxId"] = {'x1': 1, 'y1': 1, 'x2': image_height, 'y2': image_width}

        # result_dict_2 = map_result2(output_dict_det, BBOX_DONUT_Mapping_Dict)
        result_dict_2.update(result_dict_1)
        final_mapping_dict  = map_result1_final_output(result_dict_2, output_dict_donut)

        return {"result": final_mapping_dict}, None
    except Exception as e:
        print(e)
        return None, str(e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Your application description")
    parser.add_argument("input_image_folder", help="Path to the input image folder")
    parser.add_argument("output_ROI_folder", help="Path to the output ROI folder")
    parser.add_argument("output_extraction_folder", help="Path to the output extraction folder")
    args = parser.parse_args()
    processor, model = load_model(device)
    # run_application(args.input_image_folder, args.output_ROI_folder, args.output_extraction_folder)