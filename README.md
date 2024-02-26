# Gerçek Zamanlı Hareket Tanıma
## Proje Tanımı
Sensörden gelen veri ile yapılan hareket anlık olarak tahmin edilir ve yapılan hareketin süresi saniye cinsinden anlık olarak hesaplanarak mobil uygulama üzerinden kullanıcı bilgilendirilir.
## Proje Hazırlanışı
Makine öğrenmesi kullanarak anlık olarak hareket analizi yapmak istedim. Öncelikle hareket türleri tanımladım. Bunlar: Hareketsiz, Yürüyüş, Koşma, Düşme bu tanımları yaptım. MPU6050 sensörü ile bu durumları tanımlayacak verileri kaydettim. Bu verilerle makine öğrenmesi modeli oluşturarak modeli eğittim ve kaydettim. Sensörden gelen anlık veriler ile de modele tahmin yaptırıp hangi hareket türü olduğunu belirledim ve kaydettim. Yapılan hareketi aynı zamanda kaydederek anlık olarak hareket süresini hesapladım. Firebase veritabanına kaydederek anlık olarak mobil uygulama üzerinden de kullanıcının takip etmesini sağladım. 
### Projede Kullanılan Teknolojiler
-	Python
-	FireBase
-	AppInventor
-	Arduino IDE
### Projede Kullanılan Ekipmanlar
-	Nodemcu
-	MPU6050
-	4 adet jumper kablo
-	Micro USB
## Devre Şeması
![image](https://github.com/enesbt/IOT-RealTime-Machine-Learning/assets/95939881/eece1cea-39ea-416b-99ad-33097e7c2623)
## Akış Diyagram
![image](https://github.com/enesbt/IOT-RealTime-Machine-Learning/assets/95939881/fec3c735-5164-4592-875d-d975eb18e338)
## Veri Tabanı Görüntüsü
![image](https://github.com/enesbt/IOT-RealTime-Machine-Learning/assets/95939881/314d4d58-3eb7-4ab6-a5ec-9dc481844faf)
## Mobil Uygulama
![image](https://github.com/enesbt/IOT-RealTime-Machine-Learning/assets/95939881/9a36fad4-618c-4673-b074-16e221707a35)
