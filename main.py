import db

welcome = """************************ İŞLEMLER ************************
1) İşlemler Listesi
2) Tablo Listesi
3) Tablo Oluştur    : (create)
4) Veri Ekle        : (insert)
5) Veri Listele     : (select)
6) Veri Güncelle    : (update)
7) Veri Sil         : (delete)
0) Programı Sonlandır.
************************ İŞLEMLER ************************"""

print(welcome)

def control(entry):
    try: 
        int(entry)
        return True
    except ValueError:
        return False

db = db.DB
while True:
    print("")
    islem = input("İşlem Seçiniz: ")
    print("")
    if not control(islem):
        print("Lütfen Sadece Rakam Olarak İşlem Seçiniz.")
    else:
        islem = int(islem)
        if islem==1:
            print(welcome)
        elif islem==2:
            print("Mevcut Tablo Listesi")
            print(db.lists())
        elif islem==3:
            print("Tablo oluşturmak için adımları doğru takip ediniz.")
            db.create()
        elif islem==4:
            print("Tablo oluşturmak için önce var olan tablolardan birini seçiniz.")
            print(db.lists())
            db.insert()
        elif islem==5:
            print("Listedeki Hangi Tablonun Verilerini Çekmek İstiyorsunuz?.")
            print(db.lists())
            db.select()
        elif islem==6:
            print("Listedeki Hangi Tablonun Verilerini Güncelleme İstiyorsunuz?.")
            print(db.lists())
            db.update()
        elif islem==7:
            print("Listedeki Hangi Tabloyu Silmek İstiyorsunuz?.")
            print(db.lists())
            db.delete()
        elif islem==0:
            print(db.close())
            print("Good Bye.")
            break
        else:
            print("Geçersiz işlem")
