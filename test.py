import serial
import json
import re
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db as firebase_db
from datetime import datetime
import pandas as pd
import joblib

arduino_port = "COM8"  # Arduino'nun bağlı olduğu portu belirtin
baud_rate = 9600  # Arduino seri bağlantı hızı ile eşleşmeli

ser = serial.Serial(arduino_port, baud_rate)


cred = credentials.Certificate("proje-1018d-firebase-adminsdk-o2hrl-66002258bb.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://proje-1018d-default-rtdb.firebaseio.com/'  # Firebase projenizin URL'si
})
data={}
data_list = []

loaded_model = joblib.load('decision_tree_model.pkl')
while True:
    if ser.in_waiting > 0:
        veri = ser.readline().decode('latin-1').rstrip()  # Seri porttan gelen veriyi oku ve boşlukları temizle
        acceleration = re.search(r'Acceleration X: (.*?), Y: (.*?), Z: (.*?) m/s\^2', veri)
        rotation = re.search(r'Rotation X: (.*?), Y: (.*?), Z: (.*?) rad/s', veri)
        #temperature = re.search(r'Temperature: (.*?) degC', veri)
        
        temperature = re.search(r'Temperature:\s*([\d\.]+)\s*degC', veri)
        #print(json_veri)
       
        if acceleration:
            acc_x, acc_y, acc_z = acceleration.groups()
            data["Acceleration"] = {"X": acc_x, "Y": acc_y, "Z": acc_z}

        if rotation:
            rot_x, rot_y, rot_z = rotation.groups()
            data["Rotation"] = {"X": rot_x, "Y": rot_y, "Z": rot_z}

        if temperature:
            temp_value = temperature.group(1)
            data["Temperature"] = temp_value

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        data["Time"] = current_time
        if all(data.values()):
            
            json_data = json.dumps({"SensorData": data}, indent=4)
            #print(json_data)
            #firebase_db.reference("/SensorData/Acceleration/X").set(json_data['SensorData']['Acceleration']['X'])
            #ref = firebase_db.reference('/SensorData')
            json_data = json.loads(json_data)

            #print(json_data)
            if 'Acceleration' in json_data['SensorData']:
                firebase_db.reference("/SensorData/Acceleration/X").set(json_data['SensorData']['Acceleration']['X'])         
                firebase_db.reference("/SensorData/Acceleration/Y").set(json_data['SensorData']['Acceleration']['Y'])
                firebase_db.reference("/SensorData/Acceleration/Z").set(json_data['SensorData']['Acceleration']['Z'])
            
            if 'Rotation' in json_data['SensorData']:
                firebase_db.reference("/SensorData/Rotation/X").set(json_data['SensorData']['Rotation']['X'])         
                firebase_db.reference("/SensorData/Rotation/Y").set(json_data['SensorData']['Rotation']['Y'])
                firebase_db.reference("/SensorData/Rotation/Z").set(json_data['SensorData']['Rotation']['Z'])
            
            if 'Temperature' in json_data['SensorData']:
                firebase_db.reference("/SensorData/Temperature/Value").set(json_data['SensorData']['Temperature'])

            if 'Time' in json_data['SensorData']:
                firebase_db.reference("/SensorData/Time/Value").set(json_data['SensorData']['Time'])

            #data_list.append(json_data)
            df = pd.json_normalize(json_data)
            #print("df:",df)
            if "SensorData.Temperature" in df.columns:
                sonucdf =df.copy() 
                df = df.drop(columns=["SensorData.Time","SensorData.Temperature"],axis=1)
                #print(df)
                tahmin = loaded_model.predict(df)
                #print("Tahmin:", tahmin)
                tahminstr=""
                if tahmin==0:
                    tahminstr = "Haraketsiz"
                elif tahmin ==1:
                    tahminstr = "Yuruyus"
                elif tahmin ==2:
                    tahminstr = "Kosu"
                elif tahmin ==3:
                    tahminstr = "Dusme"

                firebase_db.reference("Sonuc/Sonuc").set(tahminstr)


                tahminler_df = pd.DataFrame({"Tahminler": tahmin})
                
                birlesik_df = pd.concat([df, tahminler_df], axis=1)
                sonucdf = pd.concat([sonucdf, tahminler_df], axis=1)
                sonucdf.to_csv('sensor_verileri.csv', mode='a',header=False, index=False)

                print(birlesik_df)

            # if len(data_list)>200:
                
            #     df = pd.json_normalize(data_list)
                
            #     df.reset_index(drop=True, inplace=True)
            #     df.to_csv('dusme.csv', index=True)  # CSV dosyasına dönüştürme
            #     #print(df)
            #     data_list=[]

            data = {
                "Acceleration": {},
                "Rotation": {},
                "Temperature": None,
                "Time":None
            }
        
       
        
        
        #print(veri)



