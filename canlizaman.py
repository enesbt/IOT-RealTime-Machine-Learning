import pandas as pd
import matplotlib.pyplot as plt
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        main_process()  # Dosya değiştiğinde veri işleme fonksiyonunu çağır

      
def main_process():
    while True:
        df = pd.read_csv('sensor_verileri.csv')
        df =  df.iloc[:, -2:]
        df.columns = ['Time', 'Sonuc']
        df.head()
        veri = df.copy()

        veri['Sonuc'] = veri['Sonuc'].replace({0: 'hareketsiz', 1: 'yurume', 2: 'kosma', 3: 'dusme'})
        veri['Time'] = pd.to_datetime(veri['Time'])

        eslesme = (veri['Sonuc'] != veri['Sonuc'].shift()).cumsum()
        
        def sonucAnalizi(degisken):
            grup = veri[veri['Sonuc'] == degisken] 
            grup['Grup'] = eslesme

            sure = grup.groupby('Grup')['Time'].apply(lambda x: (x.max() - x.min()).total_seconds())
            sureler = pd.DataFrame(sure)
            sureler.columns = ['Sure']

            return sureler

        hareketsiz = sonucAnalizi('hareketsiz')

        toplam_hareketsiz_sure = hareketsiz['Sure'].sum()

        yurume = sonucAnalizi('yurume')

        toplam_sure_yurume = yurume['Sure'].sum()

        kosma = sonucAnalizi('kosma')

        toplam_kosma_sure = kosma['Sure'].sum()

        dusme = sonucAnalizi('dusme')

        toplam_dusme_sure = dusme['Sure'].sum()
        ref = db.reference('/')
        ref.update({'ToplamHareketsiz/ToplamHareketsiz': toplam_hareketsiz_sure})

        ref.update({'ToplamYuruyus/ToplamYuruyus': toplam_sure_yurume})

        ref.update({'ToplamKosma/ToplamKosma': toplam_kosma_sure})

        ref.update({'ToplamDusme/ToplamDusme': toplam_dusme_sure})


if __name__ == "__main__":
    cred = credentials.Certificate("proje-1018d-firebase-adminsdk-o2hrl-66002258bb.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://proje-1018d-default-rtdb.firebaseio.com/'  # Firebase projenizin URL'si
    })
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()