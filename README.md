## PiWars Türkiye 2020: HisarCS tarafından dağıtılan robot kitleri için python kütüphanesi  
  
Bu python kütüphanesi, PiWars Türkiye 2020 katılımcılarının HisarCS tarafınndan hazırlanan robot kitlerindeki yazılımı, sensörleri ve hareketli parçaları kullanmalarını kolaylaştırmak amacıyla yapılmıştır.  


## Kurulum

Pi20'yi indirmek için [pip](https://pip.pypa.io/en/stable/) paketleme yöneticisini kullanın.


```
$ sudo pip3 install Pi20
```

Alternatif olarak Github'dan indirmek de mümkün.
```bash git clone https://github.com/HisarCS/Pi20.git
$ git clone https://github.com/HisarCS/Pi20.git
$ cd Pi20
$ sudo python setup.py install
```

## Kullanım

```python
import Pi20
```
## Belgeleme

Şu anda bu kütüphanede 5 sınıf bulunmaktadır:
- HizlandirilmisPiKamera (Pi Kamera ve opencv kullanmayı basitleştirmek ve optimize etmek için)
- Kumanda (pygame'in Joystick sınıfını PS4 sixaxis kumandalar ile kullanmayı basitleştirmek için)
- MotorKontrol (Raspberry Pi için Pololu DRV8835 motor sürücü devresinin kullanımını kolaylaştırmak için)
- ServoKontrol (Raspberry Pi'ın GPIO pinleri ile servo kontrol etmeyi kolaylaştırmak için)
- UltrasonikSensoru (Raspberry Pi'ın GPIO pinleri ile HC-SR04 ultrasonik uzaklık sensörünü kullanmayı kolaylaştırmak için)

Performans sebeplerinden dolayı sınıfların bir kısmı multithreading kullanmaktadır. Bu yazılımın bir kısmının diğerlerinin performansını değiştirmesini engellemek içindir. Multithreading özellikle kullanıldığı sınıflar HizlandirilmisPiKamera (hem görüntüyü almak hem göstermek için), Kumanda (sürekli olarak kumanda değerlerini almak için) ve ServoKontrol (içindeki sleep fonksiyonlarının ana threadi durdurmasını engellemek için).

HizlandirilmisPiKamera:
-
- Metodlar

```python
__veriGuncelle__()
```
Pi Kameradan gelen verileri bir while loop'un içerisinde günceller.  Ana threadde çağırmak **tavsiye edilmez** çünkü program bu satırda takılacaktır.

```python
veriOkumayaBasla()
```
Ana threadi yavaşlatmadan veriyi güncellemek için yeni bir threadde ``` __veriGuncelle__()``` fonksiyonunu çağırır.  Bunu sadece başlangıçta kullanarak programın her yerinde kamera verilerine ulaşabilirsiniz.

```python
veriOku()
```
NumPy listesi olarak kameranın o andaki değerlerini geri döndürür.  Bu döndürdüğü NumPy listesi ise yukarıda bahsedildiği gibi ``` __veriGuncelle__()``` fonksiyonunda bir while loop içerisinde her zaman yenilenir.

```python
__kareyiGostermeyiGuncelle__()
```
girilen parametreler dahilinde yeni opencv pencereleri açar ve pencereyi bir while loop içerisinde günceller. "q" tuşu ile pencere kapatılabilir.  Ana threadde çağırmak **tavsiye edilmez** çünkü program bu satırda takılacaktır.

```python
kareyiGoster()
```
Ana threadi yavaşlatmadan bir pencere açmak için  ``` __kareyiGostermeyiGuncelle__()``` fonksiyonunu başka bir threadde çağırır.  İki parametre alır ve bunlar da pencerenin ismi ve pencerede gösterilecek görüntüdür. Farklı pencere isimleri ve görüntüleri kullanarak ve bunları da bir while loop içeirisinde çağırarak gösterilecek olan görüntüleri güncelleyebilirsiniz. Eğer parametre olarak hiçbir şey girilmezse fonksiyon varsayılan olarak kameranın ham görüntüsünü 'frame' isimli bir pencerede göstermeye başlar.

- Örnek Kullanım

```python
from Pi20 import HizlandirilmisPiKamera
from time import sleep

camera = HizlandirilmisPiKamera()
camera.veriOkumayaBasla()
sleep(1)

while True:
	camera.kareyiGoster()
```
Yukarıdaki örnek yeni bir HizlandirilmisPiKamera objesi oluşturur, ``` veriOkumayaBasla()```   fonksiyonu ile kameradan verileri almaya başlar ve while loop'un içinde de ``` kareyiGoster()```  fonksiyonu ile okunan verileri ekranda 'frame' isimli pencere oluşturup kameradan okunan ham verileri gösterir.

Kamera objesi çağırılınca varsayılan çözünürlük 640x480 dir. Eğer başka bir çözünürlük istiyorsanız, örneğin 1280x720, kamera objesini bu şekilde oluşturabilirsiniz:

``` camera = HizlandirilmisPiKamera(cozunurluk=(1280, 720))```

Eğer ki sonradan yaptığınız görüntü işleme adımlarınızı da ayrı pencerelerde göstermek istiyorsanız ```kareyiGoster()```  fonksiyonunu birkaç kez kullanarak kodunuzu yavaşlatmadan pencereleri ayrı bir thread'de çalıştırabilirsiniz. Bunun için aşağıdaki kodu referans alabilirsiniz.

```python
from Pi20 import HizlandirilmisPiKamera
import imutils
import cv2
from time import sleep

kamera = HizlandirilmisPiKamera()
kamera.veriOkumayaBasla()
sleep(1)

while True:
	kamera.kareyiGoster()
	yenidenBoyutlandirilmis = imutils.resize(kamera.veriOku(), width=300)
	kamera.kareyiGoster("yenidenBoyutlandirilmis", yenidenBoyutlandirilmis)
	gri = cv2.cvtColor(kamera.veriOku(), cv2.COLOR_BGR2GRAY)
	kamera.kareyiGoster("siyah - beyaz", gri)
```
Yukarıdan da görüldüğü gibi, ```kareyiGoster()```  fonksiyonunu birkaç kez kullanarak görüntü işleme algoritmanızdaki farklı aşamaları ekranda izleyebilirsiniz. Ayrıca yukarıdaki programda, ilk kez ```veriOku()``` fonksiyonunu kullanmaktayız. Fonksiyon açıklamalarında da belirtildiği gibi, bize, kameranın o andaki gördüğü görüntüsünü geri döndürür. Biz de bunu kullanarak resmimizi yeniden boyutlandırabiliyoruz.

Kumanda
-
- Metodlar

```python
__yenile__()
```
Kumandadan alınan verileri bir while döngüsü içerisinde yeniler. Ana threadde çağırmak **tavsiye edilmez** çünkü program bu satırda takılacaktır.

```python
dinlemeyeBasla()
```
```__yenile__()``` metodunu ayrı bir thread üzerinde çağırarak ana thread'in kullanılabilmesini sağlar.

```python
solVerileriOku()
```
Soldaki joystick değerlerini iki float değeri, x ve y, olarak verir.

```python
sagVerileriOku()
```
Sağdaki joystick değerlerini iki float değeri, x ve y, olarak verir.

```python
butonlariOku()
```
Basılan bütün düğmeleri sayı değeri olarak bir arrayde geri verir.

```python
verileriOku()
```
Kumandanın bütün değerlerini tuple tipinde geri verir ```(python solVerileriOku(), python sagVerileriOku(), python butonlariOku())```

- Örnek Kullanım

```python
import Pi20

joystik = Pi20.Kumanda()
joystik.dinlemeyeBasla()

while True:
	lx, ly = joystik.solVerileriOku()
	rx, ry = joystik.sagVerileriOku()
	buttons = joystik.butonlariOku()

	print("Sağ joystik değerleri: ", lx, ly)
	print("Sol joystik değerleri: ", rx, ry)

	if(0 in buttons):
		print("0 Butonu basıldı!")
```
Yukarıdaki kod bir Kumanda objesi oluşturur ve sol ve sağ joysticklerin değerlerini ekrana basarken aynı zamanda belirlenmiş bir stringi bir düğmeye basıldığında ekrana basar. ```dinlemeyeBasla()``` metodunun veri alabilmek için ana kod başlatıldığında çağırılması gerektiğini unutmayınız.

MotorKontrol
-
- Metodlar

```python
hizlariAyarla(sagHiz, solHiz)
```
pololu-drv8835-rpi kütüphanesini kullanarak motorların hızını ayarlar. Hız -480'den +480'e kadar değerler olarak verilebilir (-480 geriye doğru tam hız olur). Sağ ve sol hız değerleri motor sürücüsünün birinci ve ikinci motorlarına denk gelir.

```python
kumandaVerisiniMotorVerilerineCevirme(x, y)
```
Motor hız değerlerini kumanda verisine dayanarak geri verir. x ve y, kumandanın joystick x ve y değerlerini temsil eder ve 0 ve 1 arasında bir değer alır.

- Örnek Kullanım

```python
import Pi20
motorlar = Pi20.MotorKontrol()

while True:
	motorlar.hizlariAyarla(480, 480)
```
Bu kod motorları başlatır ve ileri doğru tam hıza ayarlar.

- Kumanda ile Örnek Kullanım

```python
import Pi20

motorlar = Pi20.MotorKontrol()

joystik = Pi20.Kumanda()
joystik.dinlemeyeBasla()

while True:
	lx, ly = joystik.solVerileriOku()
	sagHiz, solHiz = motorlar.kumandaVerisiniMotorVerilerineCevirme(lx, ly)

	motorlar.hizlariAyarla(sagHiz, solHiz)
```
Yukarıdaki kod motorlar ve kumanda objelerini başlatır ve bir while döngüsünün içine girer. Döngüdeyken  ```kumandaVerisiniMotorVerilerineCevirme()``` metodu motorların hız değerlerini bulmak için kullanılır.

ServoKontrol
-
- Metodlar

```python
surekliDonmeyeAyarla()
tekDonmeyeAyarla()
```
Servoyu sürekli dönme ve tek sefer dönmeye ayarlar. Sürekli dönme modu dinamik olarak değerler verilmesini gerektirirken tek dönme servoyu verilen açıya getirir ve sonrasında uykuya geçer.

```python
aciAyarla(aci)
```
Servoyu derece cinsinden verilen açıya çevirir. Servo tek dönmeye ayarlıyken ayrı bir thread oluşturulur ve servo değeri istenen açıya gelince uyur.

- Örnek Kullanım

Sürekli Dönme:
```python
import Pi20
from time import sleep

servo = Pi20.ServoKontrol(35)
servo.surekliDonmeyeAyarla()

aci = 0
ekle = 0

while True:
	servo.aciAyarla(aci)

	if(aci == 180):
		ekle = -1
	elif(aci == 0):
		ekle = 1
	aci += ekle
	sleep(0.05)
```
Bu durumda servo sürekli dönmeye ayarlıdır. Bir while döngüsü servonun açısını 1er 1er arttırır ve servoyu yeni açıya getirir.

Tek Dönme:
```python
import Pi20
from time import sleep

servo = Pi20.ServoKontrol()
servo.tekDonmeyeAyarla()

while True:
	servo.aciAyarla(180)
	sleep(1)
	servo.aciAyarla(0)
	sleep(1)
```
Bu durumda servo tek dönmeye ayarlıdır. Bir while döngüsü servonun açısını 1 saniye aralıklarla 180 ve 0 arasında değiştirir.

UltrasonikSensoru
-
- Metodlar

```python
mesafeOku()
```
Ultrasonik sensörün ölçtüğü mesafeyi geri verir.

- Örnek Kullanım

```python
import Pi20

ultra = Pi20.UltrasonikSensoru(38, 40)
ultra.mesafeOlcmeyeBasla()
while True:
	anlikDeger = ultra.mesafeOku()
	print(anlikDeger)
```
Yukarıdaki kod ölçülen mesafeyi önce medyan ve sonra anlık değer olmak üzere ekrana basar. Yapıcının(constructor), ya da ultra nesnesi oluştururkenki kullandığımız kod satırı,  içindeki değerler ultrasonik sensörün takılı olduğu pinlerdir.


## Katkıda Bulunma
Çekme istekleri kabul edilir. Büyük değişikler için lütfen önce bir issue açarak istediğiniz değişikliği anlatın.

Lütfen testleri uygun şekilde güncellediğinizden emin olun.

## Lisans
[MIT](https://choosealicense.com/licenses/mit/)

