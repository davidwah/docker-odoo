# Odoo-V12
Repo ini berisi docker-compose untuk menjalankan Odoo pada lingkungan docker.  
Cara menjalankannya sebagai berikut:
* ubah permission folder `etc` dan `addons` dengan menjalankan perintah berikut:
	* sudo chmod 777 -R addons
	* sudo chmod 777 -R etc

* container odoo dapat di akses pada port `8012` atau bisa disesuaikan dengan merubah port pada file .yml:
```
    ports:
      - "8012:8069"
```

* untuk menjalankan dengan perintah:
```
$ docker-compose up
```

* untuk menghentikan dengan perintah:
```
$ docker-compose down
```

* untuk merestart dengan perintah:
```
$ docker-compose restart
```

