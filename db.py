import sys
import sqlite3

class DB:

    con = sqlite3.connect("sqlite.db")
    cursor = con.cursor()
    #con.close()

    @classmethod
    def control(cls,entry):
        try: 
            int(entry)
            return True
        except ValueError:
            return False

    @classmethod
    def entry(cls,message):
        entry = input(message)
        if cls.control(entry):
            if int(entry)==0:
                print("Programı Sonlandırdırınız!")
                sys.exit()
        else:
            return entry


    @classmethod
    def close(cls):
        cls.con.close()
        return "DB bağlantısı kesildi."

    @classmethod
    def lists(cls):
        cls.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        result = cls.cursor.fetchall()
        res = "Tablo listesi : "
        for i in result:
            res += "{} - ".format(i[0])
        return res.rstrip('- ')

    @classmethod
    def exists(cls,tablo):
        istablo = "SELECT name FROM sqlite_master WHERE type='table' AND name='{}'".format(tablo)
        cls.cursor.execute(istablo)
        result = cls.cursor.fetchone()
        return result

    @classmethod
    def column(cls, tablo):
        tableNames = cls.cursor.execute("PRAGMA table_info({})".format(tablo))
        cls.con.commit()
        tableName = [i[1] for i in tableNames]
        return tableName

    @classmethod
    def create(cls):
        types = ['int','integer','tinyint','smallint','varchar','text','double','float','date','datetime']
        tablo = cls.entry("Tablo Adı: ")
        if not cls.exists(tablo):
            row = int(cls.entry("Kaç adet alan açılsın: "))
            print("Kullanılabilir tip tanımları : {}".format(types))
            col = ""
            for i in range(row):
                a = cls.entry("Name {}: ".format(i))
                b = cls.entry("Type {}: ".format(i))
                if b in types:
                    col += "{} {},".format(a,b)
                else:
                    print("Lütfen type tanımlarını doğru giriniz")
            col = col.rstrip(',')
            sql = "create table if not exists {} ({})".format(tablo,col)
            cls.cursor.execute(sql)
            cls.con.commit()
            print("{} isimli tablo yok ise oluşturuldu var ise bağlandı".format(tablo))
        else:
            print("{} isimli tablo zaten var!".format(tablo))

    @classmethod
    def insert(cls):
        tablo = cls.entry("Tablo Adı: ")
        if cls.exists(tablo):
            values = []
            for i in cls.column(tablo):
                values.append(cls.entry(i+": "))
            sql = "insert into {} values{}".format(tablo,tuple(values))
            cls.cursor.execute(sql)
            cls.con.commit()
            print("{} isimli tabloya {} değerleri eklendi".format(tablo,tuple(values)))
        else:
            print("{} isimli bir tablo bulunmuyor.".format(tablo))

    @classmethod
    def select(cls):
        tablo = cls.entry("Tablo adı: ")
        if cls.exists(tablo):
            sql = "select * from {}".format(tablo)
            cls.cursor.execute(sql)
            liste = cls.cursor.fetchall()
            print("{} isimli tablonun bilgileri.".format(tablo))
            for i in enumerate(liste):
                print(i)
        else:
            print("{} isimli bir tablo bulunmuyor.".format(tablo))

    @classmethod
    def update(cls):
        tablo = cls.entry("Tablo adı: ")
        if cls.exists(tablo):
            tableName = cls.column(tablo)
            print("{} isimli tablonun alan listesi".format(tablo))
            print(tableName)
            print("Not: Güncellenmeyek alanları boş bırakınız.")
            deger = []
            for i in range(len(tableName)):
                deger.append(cls.entry("{} -> alanı güncellenecek ise yeni değer giriniz : ".format(tableName[i])))
            print("Tablodaki hangi alanla eşleşme yapılacak?")
            print(cls.column(tablo))
            whereCol = cls.entry("where column: ")
            logical = cls.entry("logical: ")
            whereVal = cls.entry("where value: ")
            setList = ""
            for i in range(len(deger)):
                if deger[i]!="":
                    setList += "{} = '{}',".format(tableName[i],deger[i])
            setList = setList.rstrip(',')
            sql = "update {} set {} where {} {} '{}'".format(tablo, setList, whereCol, logical, whereVal)
            cls.cursor.execute(sql)
            cls.con.commit()
            if cls.cursor.rowcount:
                print("{} isimli tablo güncellendi.".format(tablo))
            else:
                print("HATA! {} isimli tablo güncellenemedi!".format(tablo))
        else:
            print("{} isimli bir tablo bulunmuyor.".format(tablo))

    @classmethod
    def delete(cls):
        tablo = cls.entry("Tablo adı: ")
        if cls.exists(tablo):
            print("Tablodaki hangi alanla eşleşme yapılacak?")
            print(cls.column(tablo))
            whereCol = cls.entry("where column: ")
            logical = cls.entry("logical: ")
            whereVal = cls.entry("where value: ")
            sql = "delete from {} where {} {} '{}'".format(tablo, whereCol, logical, whereVal)
            cls.cursor.execute(sql)
            cls.con.commit()
            if cls.cursor.rowcount:
                print("{} isimli tablodan {} alanı silindi.".format(tablo,whereVal))
            else:
                print("HATA! {} isimli tablodan {} alanı silinemedi!".format(tablo,whereVal))
        else:
            print("{} isimli bir tablo bulunmuyor.".format(tablo))
