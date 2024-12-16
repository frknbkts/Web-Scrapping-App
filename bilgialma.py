from bs4 import BeautifulSoup
import pymongo
import re
import requests 

#kategoriler, yapay zeka , bilgisayar , programlama, fizik
siteler = [
    "https://scholar.google.com/scholar?hl=tr&as_sdt=0%2C5&q=yapay+zeka&btnG=&oq=Yapay+",
"https://scholar.google.com/scholar?start=10&q=yapay+zeka&hl=tr&as_sdt=0,5",
"https://scholar.google.com/scholar?start=20&q=yapay+zeka&hl=tr&as_sdt=0,5",
"https://scholar.google.com/scholar?start=30&q=yapay+zeka&hl=tr&as_sdt=0,5",
"https://scholar.google.com/scholar?start=40&q=yapay+zeka&hl=tr&as_sdt=0,5",
"https://scholar.google.com/scholar?hl=tr&as_sdt=0%2C5&q=programlama&btnG=&oq=programlama",
"https://scholar.google.com/scholar?start=10&q=programlama&hl=tr&as_sdt=0,5",
"https://scholar.google.com/scholar?start=20&q=programlama&hl=tr&as_sdt=0,5",
"https://scholar.google.com/scholar?start=30&q=programlama&hl=tr&as_sdt=0,5",
"https://scholar.google.com/scholar?start=40&q=programlama&hl=tr&as_sdt=0,5",
"https://scholar.google.com/scholar?hl=tr&as_sdt=0%2C5&q=fizik&btnG=",
"https://scholar.google.com/scholar?start=10&q=fizik&hl=tr&as_sdt=0,5",
"https://scholar.google.com/scholar?start=20&q=fizik&hl=tr&as_sdt=0,5",
"https://scholar.google.com/scholar?start=30&q=fizik&hl=tr&as_sdt=0,5",
"https://scholar.google.com/scholar?start=40&q=fizik&hl=tr&as_sdt=0,5",
"https://scholar.google.com/scholar?hl=tr&as_sdt=0%2C5&q=bilgisayar&btnG=",
"https://scholar.google.com/scholar?start=10&q=bilgisayar&hl=tr&as_sdt=0,5",
"https://scholar.google.com/scholar?start=20&q=bilgisayar&hl=tr&as_sdt=0,5",
"https://scholar.google.com/scholar?start=30&q=bilgisayar&hl=tr&as_sdt=0,5",
"https://scholar.google.com/scholar?start=40&q=bilgisayar&hl=tr&as_sdt=0,5"
]
client = pymongo.MongoClient("mongodb://localhost:27017/")
veritabani = client.get_database("yazlab") 

makaleler = veritabani['deneme'] 




def urldenbilgial(url):
    try:
        proxy = "http://c11bff38d3734e89aff371ef848bf03cab82d935:@proxy.zenrows.com:8001" 
        proxies = {"http": proxy, "https": proxy}
        response = requests.get(url)
        if response.status_code == 200:
          
            soup = BeautifulSoup(response.text, 'html.parser')
            siteler2 = soup.find_all('div',class_='gs_r gs_or gs_scl')
            for site in siteler2:
                baslık = site.find('h3',class_= 'gs_rt')
                print("başlık:" +baslık.text)
                yönlendirme_linki = 'yönlendirme linki yok'
                if baslık.find('a'):
                    yönlendirme_linki = baslık.find('a').get('href')


                acıklama = site.find('div',class_='gs_rs')
                print(4)
                print("desc: "+acıklama.text)
                indirme_linki = 'indirme linki yok' 
                if site.find('div',class_='gs_or_ggsm'):
                    indirme_linki = site.find('div',class_='gs_or_ggsm').find('a').get('href')
                    print(5)
                print("dlink:"+ indirme_linki)
                alinti_sayisi = re.sub(r'\D+', '', site.find('div',class_='gs_fl gs_flb').find_all('a')[2].text)
                print(6)
                print("ALINTI:"+alinti_sayisi)
                yazarbilgisi = site.find('div',class_='gs_a').text
                print(7)
                yazar = re.sub(r'\d+', '', yazarbilgisi)
                tarih = re.sub(r'\D+', '', yazarbilgisi)
                print("yazar: "+ yazar +"çıkış tarihi:"+tarih+ ' link: '+ indirme_linki)
                
                makale = { "Başlık":baslık.text , "Açıklama": acıklama.text ,"Yazar":yazar,"Çıkış Tarihi":tarih,
                "Alıntılar":alinti_sayisi,"Yönlendirme":yönlendirme_linki,"İndirme":indirme_linki}
                makaleler.insert_one(makale)
        else:
            print(f"Erişilemiyor: {url}. Hata kodu: {response.status_code}")
    except Exception as e:
        print(f"Hata: {url}: {e}")
for site in siteler:
    print(f"bilgi alınıyor {site}")
    urldenbilgial(site)
    print("\nYeni Siteye geçildi\n")