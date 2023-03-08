#Calling Libreries
import requests
import json
import pandas as pd

#Scan image function

def scan_image(path):
    link = 'https://app.nanonets.com/api/v2/OCR/Model/8e075f0c-ba58-451c-8f28-af3f1fda66d9/LabelFile/?async=false'
    url = link
    data = {'file': open(path, 'rb')}
    response = requests.post(url, auth=requests.auth.HTTPBasicAuth('51d0a0da-ba9d-11ed-a27e-22a1d9fde453', ''), files=data)
    data = response.text
    parse_json = json.loads(data)
    list_predictions = parse_json['result'][0]['prediction']
    Module_list = []
    Evaluation_list = []
    Note_list = []
    for i in list_predictions:
            for j in i['cells']:
                if (j['label']=='Matiere'):
                    Module_list.append(j['text'])
                elif (j['label']=='Type'):
                    Evaluation_list.append(j['text'])
                elif (j['label']=='Note'):
                    Note_list.append(j['text'])
    df = pd.DataFrame(list(zip(Module_list,Evaluation_list,Note_list)),columns=["Module","Evaluation","Note"])
    return df

#Adding scan_images function

def scan_images(images_links):
    df = pd.DataFrame()
    for each_image in images_links:
        df_temp = scan_image(each_image)
        ##print(df_temp)
        df=pd.concat([df,df_temp])
    return df    

#adding remove_replication function

def remove_rep(dataframe:dict):
     dataframe.reset_index(drop=True, inplace=True)
     dataframe = dataframe.drop_duplicates()
     return dataframe

#adding convert_to_dataframe function 

def convert_dataframe_to_json(dataframe:dict):
     dataframe = dataframe.to_json()
     return dataframe

