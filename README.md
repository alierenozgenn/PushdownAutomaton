# PDA Simülatörü

Bu proje, matematiksel ifadelerin doğruluğunu kontrol eden bir Pushdown Automaton (PDA) simülatörüdür. Güzel bir grafik arayüzüyle donatılmış uygulama, matematiksel ifadelerdeki parantez dengesini ve operatörlerin doğru yerleşimini kontrol eder.

## Özellikler

- Matematiksel ifadelerin doğruluğunu anında kontrol etme
- PDA'nın çalışmasını adım adım görselleştirme
- Stack (yığın) durumunu gerçek zamanlı izleme
- İşlem geçmişini kaydetme ve inceleme
- Modern ve kullanıcı dostu arayüz

## Desteklenen Matematiksel İfadeler

- Sayılar: 0-9 arasındaki rakamlar
- Operatörler: +, -, *, /
- Parantezler: (, )

## Ekran Görüntüleri

![1](https://github.com/user-attachments/assets/3941040c-cfe8-413e-b0d3-0d3e6d5199cc)


## Gereksinimler

- Python 3.6 veya üzeri
- PyQt5

## Kurulum

1. Projeyi indirin ya da klonlayın:
   ```
   git clone https://github.com/kullaniciadi/pda-simulator.git
   cd pda-simulator
   ```

2. Gerekli kütüphaneleri yükleyin:
   ```
   pip install PyQt5
   ```

3. Uygulamayı çalıştırın:
   ```
   python main.py
   ```

## Kullanım

1. Üst kısımdaki metin kutusuna matematiksel bir ifade girin (örn. `(3+4)*5`)
2. "Kontrol Et" düğmesine basarak ifadenin geçerli olup olmadığını kontrol edin
3. Veya "Adım Adım Göster" düğmesine basarak PDA'nın ifadeyi nasıl analiz ettiğini görün
4. "Sonraki Adım" düğmesiyle simülasyonu ilerletin
5. Stack görünümünde yığının nasıl değiştiğini takip edin
6. Alt bölümde daha önce kontrol ettiğiniz ifadelerin geçmişini görüntüleyin

## Teknik Detaylar

Bu uygulama, bir matematiksel ifadenin geçerli olup olmadığını kontrol etmek için bir Pushdown Automaton (PDA) kullanır. PDA, aşağıdaki durumlara sahiptir:

- q0: Başlangıç durumu
- q1: Parantez açıldıktan sonraki durum
- q2: Rakam görüldükten sonraki durum
- q3: Operatör görüldükten sonraki durum
- q4: Parantez kapandıktan sonraki durum
- rejected: Reddedilme durumu

PDA, ifadeyi karakter karakter okur ve durumları arasında geçiş yapar. Parantezleri dengelemek için bir yığın (stack) kullanır.

## Geliştirme

Proje şu dosyalardan oluşur:

- `main.py`: Ana uygulama dosyası
- `pda.py`: PDA sınıfının uygulaması
- `gui.py`: Grafik arayüz bileşenleri
- `styles.py`: Stil tanımlamaları

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır.
