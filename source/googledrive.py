from pathlib import Path
import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import pydrive.settings


def upload_to_google_drive():

    path=Path(__file__).parent

    pydrive.settings.LoadSettingsFile(filename=str(path.parent.joinpath("pydriveConf","settings.yaml")))
    # pydrive.settings.SetClientSecretsFile(filename=str(path.parent.joinpath("pydriveConf","client_secrets.json")))
    
    gauth = GoogleAuth()           
    drive = GoogleDrive(gauth)

    gauth.DEFAULT_SETTINGS['client_config_file'] = str(path.parent.joinpath("pydriveConf","client_secrets.json"))
    credentials_location = str(path.parent.joinpath("pydriveConf","credentials.json"))
    if not (credentials_location == None):
        gauth.LoadCredentialsFile(credentials_location)

    web_root_folder=path.parent.parent

    DRIVE_ROOT_FOLDER_ID= "16UlV3auKBupPyv1jeiYuRxziMdaOJsvP"

    try:
        tender_date_list=os.listdir(web_root_folder.joinpath("media","Tender"))
    except FileNotFoundError:
        print("=====No Tender folder found=====")
        exit()

    if len(tender_date_list)==0:
        print("=====Tender folder is empty=====")
        exit()



    for date in tender_date_list:
        try:
            date_folder_name_query=drive.ListFile({"q": "mimeType='application/vnd.google-apps.folder' and trashed=false and '{}' in parents and title='{}'".format(DRIVE_ROOT_FOLDER_ID,date)}).GetList()
            gauth.SaveCredentialsFile(str(path.parent.joinpath("pydriveConf","credentials.json")))
            if len(date_folder_name_query)==0:
                date_folder=drive.CreateFile({'parents': [{'id': DRIVE_ROOT_FOLDER_ID}],'mimeType': 'application/vnd.google-apps.folder','title':date})
                date_folder.Upload()
            else:
                date_folder=drive.CreateFile({'id': date_folder_name_query[0]['id']})
        except Exception as e:
            print(e)
            exit()

        newspaper_list=os.listdir(web_root_folder.joinpath("media","Tender",date))
        if len(newspaper_list)==0:
            print("=====No newspaper folder found=====")
            continue
        for newspaper in newspaper_list:
            try:
                newspaper_folder_query_name=drive.ListFile({"q": "mimeType='application/vnd.google-apps.folder' and trashed=false and '{}' in parents and title='{}'".format(date_folder['id'],newspaper)}).GetList()
                if len(newspaper_folder_query_name)==0:
                    newspaper_folder=drive.CreateFile({'parents': [{'id': date_folder['id']}],'mimeType': 'application/vnd.google-apps.folder','title':newspaper})
                    newspaper_folder.Upload()
                else:
                    newspaper_folder=drive.CreateFile({'id': newspaper_folder_query_name[0]['id']})
            except Exception as e:
                print(e)
                exit()
            tender_img_list=os.listdir(web_root_folder.joinpath("media","Tender",date,newspaper))
            if len(tender_img_list)==0:
                print("=====No tender image found=====")
                continue
            for img in tender_img_list:
                img_query_name=drive.ListFile({"q": "trashed=false and '{}' in parents and title='{}'".format(newspaper_folder['id'],f"Tender/{date}/{newspaper}/{img}")}).GetList()
                if not len(img_query_name)>0:                    
                    img_file = drive.CreateFile({'parents': [{'id': newspaper_folder['id']}],'title':f"Tender/{date}/{newspaper}/{img}"})
                    img_file.SetContentFile(str(web_root_folder.joinpath("media","Tender",date,newspaper,img)))
                    img_file.Upload()
                    print("Uploaded {}".format(img))
                else:
                    print(f"====={img} already uploaded=====")
                    continue

if __name__=="__main__":
    upload_to_google_drive()
