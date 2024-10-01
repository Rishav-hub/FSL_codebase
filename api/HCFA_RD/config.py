################# HCFA RD CONFIG ########################3

CATEGORY_MAPPING_PATH = r'D:\project\FSL\FSL_codebase\api\HCFA\artifacts\hcfa_rd_notes_grouped_v2.json'
HCFA_RD_MODEL_PATH = r'D:\project\FSL\FSL_codebase\api\HCFA\artifacts\hcfa_rd_grouped_30.pth'
HCFA_FORM_KEY_MAPPING = r"D:\project\FSL\FSL_codebase\api\HCFA\artifacts\HCFA_Keys_All.xlsx"
HCFA_AVERAGE_COORDINATE_PATH = r"D:\project\FSL\FSL_codebase\api\HCFA\artifacts\average_coordinates_hcfa.xlsx"
KEYS_FROM_OLD = ["29_AmountPaid", "33_BillProvPhone", "11D_PriInsOtherPlanN", "22_MedicaidCode", \
                     "11D_PriInsOtherPlanY", "22_MedicaidRefNum", "24C_EMG", "19_LocalUse", "30_BalanceDue"]

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
  '10C_PatConditionOtherY',
    '10B_PatAAState'],
 '11_class': ['11_PriInsPolGrpNumber',
  '11A_PriInsDOB',
  '11B_OtherClaimIdCodeQual',
  '11C_PriInsPlanName',
  '11D_PriInsOtherPlanN',
  '11D_PriInsOtherPlanY',
   '11A_PriInsSexF',
    '11A_PriInsSexM',
 '11B_OtherClaimIdCode',
 '11B_PriInsEmpName'],
 '12_class': ['12_PatSignonFile'],
 '13_class': ['13_PriSignonFileList'],
 '14_class': ['14_PatCurrentDate', '14_PatCurrentDateQual'],
 '15_class': ['15_PatFirstDateOfIllQual', '15_PatFirstDateOfIll'],
 '17_class': ['17A_RefProvOtherIdQual',
  '17A_RefProvOtherId',
  '17B_RefProvNPI',
  '17_RefProvOrgName',
  '17_RefProvFullName',
  '17_RefProvFullNameQual'],
 '21_class': ['21_ICDInd', '21_DiagCode', '21_DiagDescription'],
 '22_class': ['22_MedicaidCode', '22_MedicaidRefNum'],
 '23_class': ['23_PriorAuthNum', '16_PatUTWFromDate',
 '16_PatUTWToDate', '18_PatHospFromDate',
 '18_PatHospToDate', '20_OSLabCharges',
 '20_OSLabN',
 '20_OSLabY',],
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
  '24_MedicaidPaidAmount', '24J_RenProvFullName',
    '24J_RenProvOtherId',
     '24J_RenProvOtherIdQual','24_AnesEndTime','24_AnesMod','24_AnesStartTime',
     '24_AnesTotalMin',
     '24_AnesTotalTime',
     '24_AnesUnits',
     '24_ClmNYSurChargeAmount',
     '24_ClmTaxAmount',
     '24_HCT',
     '24_NDC',
     '24_NDCCharges',
     '24_NDCQualifier',
     '24_NDCUnits',
     '24_NDCUnitsQual',
],
 '25_class': ['25_BillProvFedIdCode', '25_BillProvSSN', '25_BillProvEIN'],
 '26_class': ['26_PatAcctNo'],
 '28_class': ['28_TotalCharges', '29_AmountPaid', '30_BalanceDue'],
 '31_class': ['31_PrnRenProvFullName', '31_RenProvOrgName', '31_RenDateSigned',
 '31_RenProvTaxonomyCode'],
 '32_class': ['32_FacProvOrgName',
  '32_FacProvAddr1',
  '32_FacProvCity',
  '32_FacProvState',
  '32_FacProvPostCode',
  '32_FacProvNPIId',
  '32_FacProvOtherIdFull',
  '32_FacProvOtherId', '32_AmbToFacProvAddr1',
 '32_AmbToFacProvCity',
 '32_AmbToFacProvFullName',
 '32_AmbToFacProvNPIId',
 '32_AmbToFacProvOrgName',
 '32_AmbToFacProvOtherIdFull',
 '32_AmbToFacProvPostCode',
 '32_AmbToFacProvPostCodeExt',
 '32_AmbToFacProvState',
 '32_FacProvFullName',
 '32_MedicaidTaxId',],
 '33_class': ['33_BillProvOrgName',
  '33_BillProvFullName',
  '33_BillProvAddr1',
  '33_BillProvCity',
  '33_BillProvState',
  '33_BillProvPostCode',
  '33_BillProvPhone',
  '33_BillProvNPIId',
  '33_BillProvOtherIdFull','33_MediBillProvAddr1',
 '33_MediBillProvCity',
 '33_MediBillProvNPIId',
 '33_MediBillProvOrgName',
 '33_MediBillProvOtherIdFull',
 '33_MediBillProvPhone',
 '33_MediBillProvPostCode',
 '33_MediBillProvState',
 '33_MedicaidTaxId'],
 '6_class': ['6_PatRelShipSelf', '6_PatRelShipSpouse', '6_PatRelShipChild', '6_PatRelShipOther'],
 '8_class': ['8_PatStatusSingle',
  '8_PatStatusMarried',
  '8_PatStatusOther',
  '8_PatEmpStatusCode',
  '8_PatStudentStatusCodeFT',
  '8_PatStudentStatusCodePT'],
 '27_class': ['27_AcceptAssignmentN', '27_AcceptAssignmentY'],
 '19_class': ['19_LocalUse', '19_LocalUsePrefix']}

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
  '32_AmbToFacProvOtherId',
  '32_AmbToFacProvAddr1',
 '32_AmbToFacProvCity',
 '32_AmbToFacProvFullName',
 '32_AmbToFacProvNPIId',
 '32_AmbToFacProvOrgName',
 '32_AmbToFacProvOtherIdFull',
 '32_AmbToFacProvPostCode',
 '32_AmbToFacProvPostCodeExt',
 '32_AmbToFacProvState',
 '32_FacProvFullName',
 '32_MedicaidTaxId',],
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
  '33_MedicaidTaxId',
   '33_MediBillProvAddr1',
 '33_MediBillProvCity',
 '33_MediBillProvNPIId',
 '33_MediBillProvOrgName',
 '33_MediBillProvOtherIdFull',
 '33_MediBillProvPhone',
 '33_MediBillProvPostCode',
 '33_MediBillProvState',
 '33_MedicaidTaxId'],
 '24H_EPSDT': ['24J_RenProvOtherId'],
 '24_ProcDesc': ['24_HCT']
}

################# HCFA NORMAL CONFIG ########################3
CATEGORY_MAPPING_PATH = r'D:\project\FSL\FSL_codebase\api\HCFA\artifacts\notes.json'
MODEL_PATH = r'D:\project\FSL\FSL_codebase\api\HCFA\artifacts\hcfa__94.pth'
HCFA_FORM_KEY_MAPPING = r"D:\project\FSL\FSL_codebase\api\HCFA\artifacts\HCFA_Keys_All.xlsx"
HCFA_AVERAGE_COORDINATE_PATH = r"D:\project\FSL\FSL_codebase\api\HCFA\artifacts\average_coordinates_hcfa.xlsx"
KEYS_FROM_OLD = ["29_AmountPaid", "33_BillProvPhone", "11D_PriInsOtherPlanN", "22_MedicaidCode", \
                     "11D_PriInsOtherPlanY", "22_MedicaidRefNum", "24C_EMG", "19_LocalUse", "30_BalanceDue"]


BBOX_HCFA_DONUT_Mapping_Dict = {
"10. IS PATIENT’S CONDITION RELATED TO:": ["10A_PatConditionEmpN", "10A_PatConditionEmpY", "10B_PatConditionAutoN",\
                                           "10B_PatConditionAutoY","10C_PatConditionOtherN","10C_PatConditionOtherY",
                                          "10B_PatAAState"],
"10D_Claim_Codes": "10D_ClaimCodes",
"11. INSURED’S POLICY GROUP OR FECA NUMBER": "11_PriInsPolGrpNumber",
"11. d. IS THERE ANOTHER HEALTH BENEFIT PLAN?": ["11D_PriInsOtherPlanN", "11D_PriInsOtherPlanY"],
"11A_Ins_DOB":  ["11A_PriInsDOB",'11A_PriInsSexF', '11A_PriInsSexM'],
"11B_Other_Claim_Id": ["11B_OtherClaimIdCode", "11B_OtherClaimIdCodeQual", "11B_PriInsEmpName"],
"11C_Ins_Plan_Name": "11C_PriInsPlanName",
"12_Patient_Auth_Sign": "12_PatSignonFile",
"13. INSURED’S OR AUTHORIZED PERSON’S SIGNATURE":  "13_PriSignonFileList", 
"14. DATE OF CURRENT": ["14_PatCurrentDate","14_PatCurrentDateQual"],
"15_Other_Date": ["15_PatFirstDateOfIllQual", "15_PatFirstDateOfIll"],
"16_Date": ["16_Date", '16_PatUTWFromDate', '16_PatUTWToDate'],
"17. NAME OF REFERRING PHYSICIAN OR OTHER SOURCE": ["17_RefProvFullName", "17_RefProvOrgName", "17_RefProvFullNameQual"],
"17a. Qual": ["17A_RefProvOtherId", "17A_RefProvOtherIdQual"],
"17b. NPI": "17B_RefProvNPI",
"19. Additional Claim Information": ["19A_ProvCredential", "19A_ProvFName", "19A_ProvLName",\
                "19A_ProvMI", "19A_ProvPrefix", "19A_ProvFullNameQual", "19A_ProvSuffix", \
                "19B_ProvCredential", "19B_ProvFName", "19B_ProvLName", "19B_ProvMI",\
                "19B_ProvPrefix", "19B_ProvFullNameQual", "19B_ProvSuffix",\
                "19_LocalUsePrefix"],
"19_Hospitalization_Date": ['Box19B_Provider', 'Box19B_NPI', 'Box19A_QQ', 'Box19A_Provider', 'Box19A_NPI', '19_LocalUse', '18_PatHospFromDate',
 '18_PatHospToDate'],
"1_InsType":  "1_InsType",
"1a. INSURED’S I.D. NUMBER": "1A_PriInsIDNumber",
"2. PATIENT’S NAME (Last Name, First Name, Middle Initial)": "2_PatFullName",
"20_Outside_Lab": ["20_Outside_Lab", "MissApp", '20_OSLabCharges', '20_OSLabN', '20_OSLabY',],
"21. DIAGNOSIS OR NATURE OF ILLNESS OR INJURY.": ["21_DiagDescription","21_DiagCode", "21_ICDInd"],
"22. MEDICAID RESUBMISSION CODE and Original Ref No": ["22_MedicaidCode", "22_MedicaidRefNum"],
"23. PRIOR AUTHORIZATION NUMBER": "23_PriorAuthNum",
"24. Table": ["24_HCT", "24_MedicaidPaidAmount", "24_NDC", "24_NDCUnits", "24_NDCUnitsQual", "24_ProcDesc", \
              "24_ClmTaxAmount", "24A_FromDate", "24A_ToDate", "24B_POS", "24C_EMG", "24D_Modifier", "24D_ProcCode",\
                "24E_DiagPtr", "24F_LineCharges", "24G_Units", "24H_EPSDT", "24H_EPSDT1", "24J_RenProvNPIId", \
                "24J_RenProvOtherId", "24_ClmNYSurChargeAmount", "24_ClmDiscountAmount", "24J_RenProvFullName",
                 "24J_RenProvOtherIdQual", '24_AnesEndTime', '24_AnesMod','24_AnesStartTime', '24_AnesTotalMin',\
                '24_AnesTotalTime', '24_AnesUnits', '24_NDCCharges','24_NDCQualifier'],
"25. FEDERAL TAX I.D. NUMBER_SSN_EIN": ["25_BillProvFedIdCode", "25_BillProvEIN", "25_BillProvSSN"],
"26. PATIENT’S ACCOUNT NO.": "26_PatAcctNo", 
"27. ACCEPT ASSIGNMENT?": ["27_AcceptAssignmentN", "27_AcceptAssignmentY"],
"28. TOTAL CHARGE": "28_TotalCharges",
"29. AMOUNT PAID":"29_AmountPaid",
"3. PATIENT’S BIRTH DATE": ["3_PatSexF", "3_PatSexM", "3_PatDOB"],
"30_Reserved_NUCC": "30_BalanceDue",
"31. SIGNATURE OF PHYSICIAN OR SUPPLIER  INCLUDING DEGREES OR CREDENTIALS": ["31_RenProvTaxonomyCode", \
                                                                             "31_PrnRenProvFullName", "31_RenProvOrgName", '31_RenDateSigned'],
"32. SERVICE FACILITY LOCATION INFORMATION": ["32_AmbToFacProvAddr1" ,"32_AmbToFacProvAddr2", "32_AmbToFacProvCity",\
                "32_AmbToFacProvCredential", "32_AmbToFacProvFName" , "32_AmbToFacProvFullPost", "32_AmbToFacProvLName",\
                "32_MedicaidTaxId", "32_AmbToFacProvMI", "32_AmbToFacProvNPIId", "32_AmbToFacProvOrgName", \
                "32_AmbToFacProvOtherId", "32_AmbToFacProvOtherIdFull", "32_AmbToFacProvPostCode", \
                "32_AmbToFacProvPostCode5", "32_AmbToFacProvPostCodeExt", "32_AmbToFacProvPrefix", "32_FacProvOrgName", \
                "32_FacProvAddr1", "32_FacProvCity", "32_FacProvCredential", "32_FacProvFName", "32_FacProvLName", \
                "32_FacProvMI", "32_FacProvNPIId", "32_FacProvOtherId", "32_FacProvOtherIdFull", "32_FacProvPostCode", \
                "32_FacProvPrefix", "32_FacProvState", "32_FacProvSuffix", "32_AmbToFacProvState", "32_AmbToFacProvSuffix", \
                '32_AmbToFacProvFullName', '32_FacProvFullName'],
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