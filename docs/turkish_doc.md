Tabii. Bu projeyi sana teknik detaylarıyla ama anlaşılır bir dille, sıfırdan anlatayım.

Öncelikle şunu söyleyeyim: Mini ROV Simulator, su altında çalışan uzaktan kumandalı bir robotun (ROV – Remotely Operated Vehicle) gerçek donanım olmadan bilgisayar ortamında simüle edilmesini sağlayan bir yazılım projesidir.

Yani gerçek bir su altı robotu üretmeden önce onun motorlarını, sensörlerini, kontrol sistemlerini ve güvenlik mekanizmalarını sanal ortamda test edebilmeni sağlar.

# 1. Bu proje tam olarak ne yapıyor?

Örneğin bir su altı robotu geliştirdiğini düşün.

Bu robotun:

- Sağ ve sol iticileri (thruster) var.
- Yukarı ve aşağı hareket etmesini sağlayan motorları var.
- Derinliğini ölçen sensörü var.
- Yatay ve dikey açısını ölçen IMU sensörü var.
- Motorların hızını kontrol eden elektronik hız kontrolcüleri (ESC) var.
- Robotun güvenli çalışmasını sağlayan bir kontrol sistemi var.

Normal şartlarda bunları test etmek için fiziksel bir ROV'a ihtiyacın olur.

Ancak bu projede gerçek donanımların yerine yazılımsal karşılıkları oluşturulmuş.

Delta Inspector 1 ROV preliminary design - Upcoming Products - Delta ROV Forum

Design and Construction of an ROV for Underwater Exploration

ROV System Components

Projenin amacı şu:

Bilgisayarda sanal bir ROV oluşturmak, ona komut göndermek, hareketlerini simüle etmek ve sonuçları grafikler üzerinden izlemek.

Örneğin ground station üzerinden:

- İleri git komutu gönderirsin.
- Robotun motorları tepki verir.
- Sensör değerleri değişir.
- Kontrolcü robotun hareketini hesaplar.
- Güvenlik sistemi değerleri kontrol eder.
- Sonuçlar bilgisayar ekranında gösterilir.

# 2. Projenin mimarisi

Proje üç ana parçadan oluşuyor.

## Mini ROV Simulator mimarisi

GROUND STATION

Python – Kullanıcı arayüzü, grafikler ve kontrol

JSON mesajları

PROTOCOL LAYER

Python / Pydantic – İletişim ve veri doğrulama

JSON mesajları

FIRMWARE SIMULATOR

C++20 – Motorlar, ESC, kontrolcü ve güvenlik

Bu üç bölümün görevlerini ayrı ayrı inceleyelim.

# 3. Firmware Simulator – Robotun beyni

C++20Firmware, gerçek bir ROV'un elektronik kontrol kartında çalışacak yazılımın simüle edilmiş halidir.

Gerçek bir ROV'da firmware, motorlara ne kadar güç verileceğini ve sensörlerden gelen verilere göre robotun nasıl davranacağını belirler.

Bu projede firmware içerisinde şu modüller bulunuyor:

## A. Motor (motor.cpp / motor.h)

T200 Thruster – Spot X Underwater Vision

[spotx.com.au](<https://www.spotx.com.au/products/t200-thruster?utm_source=chatgpt.com>)

Motor sınıfı, robotun iticilerini temsil eder.

Örneğin:

- Motora güç gönderilir.
- Motorun RPM değeri hesaplanır.
- Motorun hızlanması sınırlandırılır.
- Voltaj düşüşü modellenir.

RPM, motorun dakikadaki dönüş sayısıdır.

Örneğin motorun hedef hızı 2000 RPM ise motorun aniden 2000 RPM'e çıkması yerine belirli bir hızlanma süresiyle bu değere ulaşması modellenebilir.

Bu, gerçek motor davranışına daha yakın bir simülasyon oluşturur.

## B. ESC (esc.cpp / esc.h)

Tekko32 2-6S AM32 Brushless ESC, Small but Mighty (Soldered\!) – Just 'Cuz Robotics

[justcuzrobotics.com](<https://justcuzrobotics.com/products/tekko32-3s-6s-am32-brushless-esc-soldered?utm_source=chatgpt.com>)

ESC, Electronic Speed Controller anlamına gelir.

Türkçesi elektronik hız kontrolcüsüdür.

Görevi motorun hızını kontrol etmektir.

Örneğin:

| Throttle | ESC davranışı |
| --- | --- |
| 0.0 | Motor kapalı |
| 0.25 | Düşük güç |
| 0.50 | Orta güç |
| 0.75 | Yüksek güç |
| 1.0 | Maksimum komut |

Burada throttle, motora gönderilen güç komutudur.

ESC sınıfı bu komutu alır ve uygun çıkış voltajını hesaplar.

## C. Controller (controller.cpp / controller.h)

Burası projenin en önemli parçalarından biri.

PID Controller Explained: Loop Tuning, Formulas & Industrial Examples

[electrical-world.com](<https://electrical-world.com/posts/pid-controller-explained-loop-tunning-and-formulas?utm_source=chatgpt.com>)

Controller, robotun istenen hareketi yapmasını sağlayan kontrol sistemidir.

Projede PID kontrol yöntemi kullanılıyor.

PID üç bileşenden oluşur:

- P (Proportional): Hedef ile mevcut değer arasındaki hataya göre tepki verir.
- I (Integral): Zaman içerisinde biriken hatayı düzeltir.
- D (Derivative): Hatanın değişim hızına göre tepki verir.

Örneğin:

ROV'un 5 metre derinlikte kalmasını istiyorsun.

Ancak robot şu anda 4 metre derinlikte.

Controller:

1. Hedef derinliği 5 metre olarak alır.
2. Mevcut derinliği sensörden okur.
3. Aradaki farkı hesaplar.
4. PID algoritmasını çalıştırır.
5. Dikey iticiye gerekli komutu üretir.

Bu sayede robotun hedef derinliğe ulaşması ve o derinliği koruması amaçlanır.

Projede ayrıca heading/yaw kontrolü de bulunuyor.

Yani robotun baktığı yönü kontrol etmek için de PID sistemi kullanılıyor.

## D. Safety Manager (safety\_manager.cpp / .h)

Güvenlik sistemiBu bölüm robotun güvenli çalışmasını kontrol eder.

Örneğin:

- Robot izin verilen maksimum derinliği aşarsa,
- Roll veya pitch açısı belirlenen sınırları geçerse,
- Besleme voltajı güvenli aralığın dışına çıkarsa,

SafetyManager devreye girer.

Projede tanımlanan güvenlik mantığına göre tehlikeli bir durum tespit edildiğinde itici çıkışları sıfırlanır.

Bu sistemin amacı robotun kontrolsüz şekilde çalışmasını önlemektir.

## E. Sensor Data

Bu dosya sensörlerden ve aktüatörlerden gelen verileri temsil eden veri yapılarını içerir.

Örneğin:

| Veri | Açıklama |
| --- | --- |
| IMUData | Roll, pitch ve yaw |
| DepthData | Derinlik bilgisi |
| ThrusterData | İtici bilgileri |
| SensorData | Sensör verilerinin bütünü |
| ActuatorOutput | Motorlara gönderilecek komutlar |

Yani bu yapılar diğer yazılım modüllerinin ortak veri kaynağıdır.

# 4. Ground Station – Operatörün kontrol ekranı

Python 3.12+UiASub | ROV

Control & inspection software for VideoRay ROVs

Spotlight: Duke Robotics Club’s journey to underwater autonomy. | Foxglove

Ground Station, operatörün robotu izlemesini ve kontrol etmesini sağlayan bilgisayar uygulamasıdır.

Gerçek hayatta bir ROV operatörünün önünde bulunan kontrol ekranı gibi düşünebilirsin.

Bu bölüm Python ile geliştirilmiş.

Temel görevleri:

- Firmware ile iletişim kurmak.
- Sensör verilerini almak.
- Robotun durumunu takip etmek.
- Grafikler oluşturmak.
- Kontrol komutlarını iletmek.

### application.py

Bu dosya Ground Station'ın ana uygulamasıdır.

İki önemli sınıf bulunuyor:

1. FirmwareProcess

Firmware simülatörünü ayrı bir işlem olarak başlatır.

Görevleri:

- C++ programını çalıştırmak.
- Programın çıktısını okumak.
- Firmware ile bağlantıyı yönetmek.
- Firmware başlatılamazsa simülasyon verilerine geçmek.

2. ROVApp

Uygulamanın ana arayüz ve durum yönetimi bölümüdür.

Matplotlib kullanarak dört grafik oluşturur:

- Roll: Robotun sağa veya sola yatması.
- Pitch: Robotun öne veya arkaya eğilmesi.
- Yaw: Robotun baktığı yön.
- Status: Robotun çalışma durumuyla ilgili bilgiler.

`FuncAnimation` sayesinde grafikler belirli aralıklarla güncellenir.

Yani ekrandaki grafikler sabit değildir, simülasyon ilerledikçe değişir.

# 5. Protocol Layer – İki sistemin ortak dili

Pydantic + JSONBence projenin mimari açıdan en önemli bölümlerinden biri de burası.

Şöyle düşün:

C++ firmware bir veri gönderiyor.

Python Ground Station bu veriyi alıyor.

Ancak iki programın birbirinin anlayabileceği ortak bir veri formatı kullanması gerekiyor.

İşte Protocol Layer bunu sağlıyor.

JSON for Beginners: What It Is and Why Developers Use It - DEV Community

[dev.to](<https://dev.to/ezeanyim_henry/json-for-beginners-what-it-is-and-why-developers-use-it-3aki?utm_source=chatgpt.com>)

Bu projede JSON kullanılıyor.

Örneğin firmware'in gönderdiği örnek bir durum mesajı şöyle olabilir:

json

```json
{
  "type": "firmware_status",
  "depth": 5.2,
  "roll": 2.5,
  "pitch": -1.3,
  "yaw": 90.0,
  "voltage": 12.4
}
```

Bu yalnızca protokolün çalışma mantığını göstermek için hazırlanmış örnek bir mesajdır.

Python tarafında Pydantic bu mesajın doğru olup olmadığını kontrol eder.

Örneğin:

- Derinlik sayısal mı?
- Roll değeri izin verilen aralıkta mı?
- Gerekli alanlar mevcut mu?
- Veri beklenen formata uygun mu?

Böylece hatalı verilerin uygulamaya girmesi engellenebilir.

Projede tanımlanan temel mesaj modelleri:

| Model | Görevi |
| --- | --- |
| FirmwareStatus | Robotun mevcut durumunu bildirir. |
| ControlCommand | Robota kontrol komutu gönderir. |
| Configuration | Sistem ayarlarını taşır. |
| Alert | Uyarı ve hata mesajlarını taşır. |

# 6. Üç sistem birlikte nasıl çalışıyor?

Şimdi gerçek bir senaryo üzerinden düşünelim.

Operatör olarak robotun 3 metre derinliğe inmesini istiyorsun.

## Örnek çalışma senaryosu

1. Operatör komut gönderir
   Ground Station üzerinden hedef derinlik 3 metre olarak belirlenir.
2. Protocol mesajı oluşturulur
   Komut JSON formatına dönüştürülür ve doğrulanır.
3. Firmware komutu alır
   C++ tarafındaki Controller hedef derinliği işler.
4. PID hesaplaması yapılır
   Mevcut derinlik ile hedef derinlik karşılaştırılır ve gerekli itici komutu hesaplanır.
5. Motor ve ESC çalışır
   İtici motorların davranışı simüle edilir.
6. Güvenlik kontrolü yapılır
   SafetyManager sensör değerlerini ve güvenlik limitlerini kontrol eder.
7. Yeni veriler Ground Station'a gönderilir
   Python uygulaması robotun güncel durumunu alır.
8. Grafikler güncellenir
   Operatör robotun durumunu gerçek zamanlı olarak izler.

Bu döngü sürekli devam eder.

Böylece operatör komut verir, firmware hesaplama yapar ve Ground Station sonuçları gösterir.

# 7. Hangi teknolojiler neden kullanılmış?

| Teknoloji | Kullanım amacı |
| --- | --- |
| C++20 | Firmware ve fiziksel davranış simülasyonu |
| Python 3.12 | Ground Station uygulaması |
| Matplotlib | Gerçek zamanlı grafikler |
| Pydantic | Veri doğrulama |
| JSON | Sistemler arası veri iletişimi |
| CMake | C++ derleme sistemi |
| UV | Python paket yönetimi |
| Pytest | Python testleri |

# 8. Projenin şu anki eksikleri ve dikkat edilmesi gerekenler

Paylaştığın proje açıklamasına göre bazı önemli noktalar var.

Bunları bilmen önemli çünkü proje şu anda tamamen tamamlanmış, gerçek bir ROV simülatörü seviyesinde görünmüyor.

1. Gerçek fizik simülasyonu sınırlı

Motor RPM ve voltaj davranışları modelleniyor. Ancak suyun kaldırma kuvveti, sürükleme kuvveti, akıntı, kütle ve atalet gibi fiziksel etkilerin kapsamlı bir modeli açıklamada görünmüyor.

2. İletişim altyapısı tamamlanmamış olabilir

JSON mesaj modelleri var ancak gerçek zamanlı haberleşmenin hangi mekanizmayla yapıldığı net değil. TCP, UDP veya seri haberleşme gibi bir iletişim katmanı gerekiyor.

3. Ground Station arayüzü temel seviyede

Matplotlib grafikleri mevcut ancak kapsamlı bir operatör paneli, joystick desteği ve gelişmiş kontrol arayüzü henüz açıklanmamış.

4. Firmware entegrasyonu geliştirilmeli

FirmwareProcess şu anda firmware başlatılamazsa yapay veriler oluşturabiliyor. Gerçek firmware ile haberleşmenin güvenilir biçimde çalışması için bu bölümün geliştirilmesi gerekiyor.

5. Dosya yapısında bazı tutarsızlıklar var

Örneğin `ground_station/src/ground_station/` ile `ground_station/src/ground_stain` isimleri arasında tutarsızlık belirtilmiş. Ayrıca firmware altında birden fazla `main.cpp` ve test dizini bulunuyor. Gerçek dosya yapısı kontrol edilmeli.

# 9. Bu projeyi geliştirirken nasıl bir yol izlenmeli?

Ben olsam şu sırayla ilerlerdim:

## Geliştirme yol haritası

1. Mevcut sistemi çalıştırmak
   C++ firmware'i derlemek, Python uygulamasını çalıştırmak ve mevcut testleri geçirmek.
2. Firmware modüllerini tamamlamak
   Motor, ESC, PID Controller ve SafetyManager davranışlarını doğrulamak.
3. Gerçekçi fizik modeli oluşturmak
   Sürükleme, kaldırma kuvveti, ağırlık, itici kuvveti ve hareket dinamiklerini eklemek.
4. Haberleşme katmanını oluşturmak
   C++ ve Python arasında TCP veya UDP üzerinden JSON mesajlaşmasını sağlamak.
5. Ground Station geliştirmek
   Kontrol paneli, joystick, sensör göstergeleri ve grafikler eklemek.
6. Test ve doğrulama
   Farklı arıza senaryoları, sensör hataları ve güvenlik durumlarını test etmek.

# 10. Sonuç: Bu proje neden önemli?

Bu proje aslında tek başına bir motor simülatörü değil.

Bir ROV'un kontrol sisteminin yazılımsal prototipini oluşturmayı hedefleyen, birden fazla teknolojiyi bir araya getiren bir sistem.

Bu projede şunları öğrenebilirsin:

- Gömülü sistem yazılımı (Embedded Systems).
- C++ ile donanım davranışlarının modellenmesi.
- PID kontrol algoritmaları.
- Sensör verilerinin işlenmesi.
- Motor ve ESC kontrolü.
- Python ile operatör arayüzü geliştirme.
- JSON tabanlı haberleşme protokolleri.
- Gerçek zamanlı sistem mimarisi.

Benim değerlendirmem: Projenin en önemli tarafı C++ firmware ile Python Ground Station'ı birbirinden ayırması ve aralarında bağımsız bir protokol katmanı tasarlamasıdır. Bu mimari, ileride simülatörün gerçek bir ROV donanımına bağlanmasını da kolaylaştırabilir.

## Sana önerim: Bir sonraki adım

Bu projeyi gerçekten öğrenmek istiyorsan sadece dosyaların ne işe yaradığını bilmek yerine sistemin nasıl çalıştığını kod üzerinden anlamanı öneririm.

Özellikle şu sırayla ilerleyebiliriz:

1. Firmware kodlarını inceleyelim: Motor, ESC, PID ve SafetyManager nasıl çalışıyor?
2. PID kontrolünü anlayalım: Robot derinliğini ve yönünü nasıl koruyor?
3. Protocol Layer'ı inceleyelim: C++ ile Python nasıl haberleşiyor?
4. Ground Station'ı inceleyelim: Grafikler ve kontrol sistemi nasıl çalışıyor?

İlk olarak firmware tarafındaki `motor.cpp`, `esc.cpp` ve `controller.cpp` dosyalarını incelersek projenin çalışma mantığını çok daha iyi kavrayabiliriz.