import pandas as pd

from date.SecureString import login, passw

import auxiliary_functions

from functions_hikvision import reboot, hikvision_modify_date_seting, data_collection

filename = "hikvision.csv"
df = pd.DataFrame([["Регистратор", "deviceName", "devicemodel", "device_firmwareVersion", "device_firmwareReleasedDate",
                    "NTPServer", "Канал", "Имя камеры", "IP камеры", "videoCodecType_main",
                    "videoResolutionWidth", "vide+oResolutionHeight_main", "videoQualityControlType_main",
                    "SmartCodec_main", "vbrUpperCap_main", "maxFrameRate_main", "videoCodecType_sub",
                    "videoResolutionWidth_sub",
                    "videoResolutionHeight_sub", "videoQualityControlType_sub", "vbrUpperCap_sub", "maxFrameRate_sub",
                    "детекция движения", "ActiveSearch", "MotionDetection", "gridMap",
                    "DateTimeOverlay", "ipAddress_1", "subnetMask_1", "addressingType_1", "MACAddress_1",
                    "ipAddress_2", "subnetMask_2", "addressingType_2", "MACAddress_2", "Пользователи",
                    "Блок записи 1", "Блок записи 2", "Блок записи 3", "Блок записи 4", "Блок записи 5",
                    "Блок записи 6", "Блок записи 7", ]])

Title = {"title": "Сheck service hikvision",
         "description": """
              Author: Kharitonov Evgeny
              Welcome to hikvision video recorder settings check service

              """}


registrators = auxiliary_functions.list_of_servers()


print(Title["description"])

for serv in registrators:
    print("Start checking the video recorder : " + serv)
    datereg = data_collection(serv, login, passw)
    df = df.append(pd.DataFrame(datereg), ignore_index=True)
    print("End checking the video recorder : " + serv)
df.to_csv(filename, sep=';', encoding="utf-8-sig", index=False, header=0)

