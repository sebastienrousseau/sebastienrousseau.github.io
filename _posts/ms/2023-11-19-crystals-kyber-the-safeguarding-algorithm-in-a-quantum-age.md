---
title: "CRYSTALS-Kyber: Algoritma Pelindung dalam Era Kuantum"
tags: "quantum, CRYSTALS-Kyber, encryption, cybersecurity, banking, finance, data, future, post-quantum cryptography, cryptography, ISO 20022, DORA, quantum computing, AI, Rust"
subtitle: "CRYSTALS-Kyber, standard NIST FIPS 203 untuk enkapsulasi kunci pasca-kuantum."
description: "Ketahui bagaimana CRYSTALS-Kyber, sebuah algoritma kriptografi rintangan kuantum, merevolusikan dunia kriptografi dan menyediakan kita untuk era kuantum."
date: "Nov 19, 2023"
language: "ms"
locale: "ms_MY"
banner: "https://cloudcdn.pro/stocks/images/galina-nelyubova-V70-ng4FuiA.webp"
banner_alt: "Komputer kuantum moden yang ramping"
keywords: "pengkomputeran kuantum, kriptografi rintangan kuantum, CRYSTALS-Kyber, kriptografi, keselamatan, perbankan, kewangan, penyulitan, perlindungan data, kalis masa depan"
---

![AI, Artificial Intelligence concept,3d rendering,conceptual image](https://cloudcdn.pro/stocks/images/galina-nelyubova-V70-ng4FuiA.webp).class=\"img-fluid clearfix\"

## Wawasan

### Mengharungi Ancaman Kuantum: Kelahiran CRYSTALS-Kyber

Dalam artikel saya sebelum ini, [Melindungi Data dalam Era Kuantum ⧉][03], saya menyelami ancaman pengkomputeran kuantum yang semakin hampir terhadap keselamatan digital dan meneliti bagaimana kriptografi rintangan kuantum (QRC) dapat menanganinya. Kini saya akan meneroka `CRYSTALS-Kyber`, sebuah algoritma QRC perintis yang mengubah landskap keselamatan.

Komputer kuantum, dengan keupayaannya melaksanakan pengiraan tertentu jauh lebih pantas berbanding komputer klasik, menimbulkan risiko besar kepada algoritma penyulitan semasa. Ini menimbulkan kebimbangan tentang keselamatan maklumat sensitif, termasuk transaksi kewangan, rekod perubatan dan komunikasi peribadi.

Untuk mengurangkan ancaman ini, ahli kriptografi telah membangunkan algoritma QRC, seperti `CRYSTALS-Kyber`. Algoritma ini merupakan mekanisme enkapsulasi kunci (KEM) yang direka untuk menukar kunci rahsia antara pihak dengan selamat.

Hari ini, `CRYSTALS-Kyber` berdiri sebagai peneraju dalam proses penyeragaman kriptografi pasca-kuantum [National Institute of Standards and Technology (NIST) ⧉][05], membuktikan potensinya sebagai penyelesaian keselamatan yang kukuh untuk era digital.

### CRYSTALS-Kyber: Keselamatan Teguh dalam Menghadapi Pengkomputeran Kuantum

Keselamatan `CRYSTALS-Kyber` bergantung pada kesukaran semula jadi untuk menyelesaikan masalah `Learning With Errors (LWE)` ke atas kekisi modul. Cabaran matematik yang rumit ini, yang dianggap tidak dapat dikira secara praktikal walaupun oleh komputer kuantum, menjadi asas ketahanan `CRYSTALS-Kyber` terhadap serangan kuantum.

### CRYSTALS-Kyber: Anjakan Paradigma dalam Keselamatan Digital

`CRYSTALS-Kyber` tergolong dalam suite algoritma CRYSTALS (Cryptographic Suite for Algebraic Lattices) dan dengan bangganya menyandang keistimewaan sebagai algoritma selamat kuantum (QSA).

Walaupun konsep menggunakan masalah kekisi untuk tujuan kriptografi bukanlah perkara yang sepenuhnya baharu, `CRYSTALS-Kyber` mengangkat konsep ini ke tahap kecekapan yang tiada tandingan. Keupayaannya menjana kunci kriptografi dengan saiz kunci yang lebih kecil serta kelajuan penyulitan dan penyahsulitan yang lebih pantas menjadikannya pilihan ideal untuk aplikasi dunia sebenar, terutamanya dalam dunia kewangan yang mencabar.

![Divider][01].class=\"m-10 w-100\"

## Idea

### Memahami Mekanisme CRYSTALS-Kyber: Enkapsulasi Kunci sebagai Terasnya

Di teras reka bentuk perintis `CRYSTALS-Kyber` terletak pendekatannya yang inovatif terhadap enkapsulasi kunci, satu komponen kritikal dalam komunikasi selamat. Ia memanfaatkan kuasa kriptografi kekisi, satu kaedah yang terkenal dengan ketahanannya terhadap serangan berasaskan kuantum. Teknik canggih ini menggunakan struktur geometri dalam ruang berbilang dimensi untuk mewujudkan kunci kriptografi.

`CRYSTALS-Kyber` menggunakan jenis masalah kekisi tertentu, yang terkenal dengan ciri kecekapan dan keselamatannya, untuk menjana kunci kriptografi. Ini memastikan perlindungan data sensitif walaupun dalam menghadapi kemajuan pengkomputeran kuantum.

#### Enkapsulasi Kunci Selamat: Intipati CRYSTALS-Kyber

Enkapsulasi kunci umpama mengunci mesej dengan selamat di dalam sebuah kotak, di mana hanya penerima yang dituju memiliki kunci untuk membukanya. Dalam dunia kriptografi, proses ini melibatkan penciptaan sepasang kunci: kunci awam, yang boleh dikongsi secara terbuka, dan kunci peribadi, yang mesti dirahsiakan. Keunggulan `CRYSTALS-Kyber` terletak pada keupayaannya menjana dan menggunakan kunci ini dengan cara yang memastikan keselamatan tiada tandingan.

Mari kita lihat bagaimana `CRYSTALS-Kyber` menggunakan enkapsulasi kunci untuk mewujudkan komunikasi selamat antara dua pihak, Alice dan Bob. Rajah jujukan di bawah menggambarkan langkah-langkah yang terlibat dalam mewujudkan komunikasi selamat antara Alice dan Bob menggunakan `CRYSTALS-Kyber`, sebuah mekanisme enkapsulasi kunci (KEM) yang direka untuk menyediakan pertukaran kunci yang selamat bagi protokol kriptografi. KyberServer memainkan peranan penting dalam proses ini, dengan menjana dan mengedarkan kunci kriptografi yang diperlukan untuk komunikasi selamat menggunakan `CRYSTALS-Kyber`.

![CRYSTALS-Kyber Key Encapsulation Mechanism (KEM)][04].class=\"img-fluid clearfix\"

##### Petunjuk

- Alice: Penghantar mesej.
- Bob: Penerima mesej.
- KyberServer: Pelayan yang menjana dan mengedarkan kunci kriptografi.

##### Penerangan

###### Pertukaran Kunci Awam

- Alice memulakan proses dengan meminta kunci awamnya daripada KyberServer.
- KyberServer bertindak balas dengan menghantar kunci awam Alice, satu nilai matematik yang boleh dikongsi secara awam tanpa menjejaskan keselamatan kunci peribadi Alice.
- Alice kemudian berkongsi kunci awamnya dengan Bob, membolehkan Bob menyulitkan mesej yang hanya boleh dinyahsulit oleh Alice.

###### Enkapsulasi dan Dekapsulasi

- Bob meminta kunci enkapsulasi daripada KyberServer. Kunci sementara ini akan digunakan untuk menyulitkan kunci rahsia kongsi sebelum menghantarnya kepada Alice.
- KyberServer menghantar kunci enkapsulasi kepada Bob.
- Bob menggunakan kunci awam Alice dan kunci enkapsulasi untuk menyulitkan kunci rahsia kongsi, lalu mencipta kapsul tersulit.
- Bob menghantar kapsul tersulit itu kepada Alice.
- Alice meminta kunci penyahsulitan daripada KyberServer. Kunci sementara ini akan digunakan untuk menyahsulit kapsul tersulit dan mendedahkan kunci rahsia kongsi.
- KyberServer menghantar kunci penyahsulitan kepada Alice.

###### Pertukaran Kunci Rahsia Kongsi

- Alice menggunakan kunci peribadinya dan kunci penyahsulitan untuk menyahsulit kapsul, lalu mendedahkan kunci rahsia kongsi.
- Alice berkongsi kunci rahsia kongsi dengan Bob, membolehkan Bob menyahsulit mesej yang disulitkan menggunakan kunci rahsia kongsi tersebut.

###### Komunikasi Selamat

Rajah jujukan itu secara berkesan menggambarkan langkah-langkah rumit yang terlibat dalam mewujudkan saluran komunikasi selamat, sambil menonjolkan peranan penting KyberServer dalam menjana dan mengedarkan kunci kriptografi. Dengan menggunakan KEM `CRYSTALS-Kyber`, Alice dan Bob dapat melindungi maklumat sensitif mereka dan mengekalkan komunikasi selamat walaupun dalam menghadapi kemungkinan pihak lawan.

### Kriptografi Berasaskan Kekisi: Asas Kukuh untuk Rintangan Kuantum

`CRYSTALS-Kyber` menggunakan pendekatan berasaskan kekisi, satu kaedah yang terkenal dengan potensi rintangannya terhadap serangan kuantum. Prinsip asas kriptografi kekisi melibatkan struktur geometri dalam ruang berbilang dimensi. Walaupun konsep mengharungi struktur kompleks ini mungkin kelihatan menggerunkan, `CRYSTALS-Kyber` mempermudahnya. Ia menggunakan jenis masalah kekisi tertentu, yang terkenal dengan ciri kecekapan dan keselamatannya, untuk mencipta kunci kriptografi.

#### Saiz Kunci yang Cekap: Imbangan Antara Keselamatan dan Prestasi

Salah satu ciri unggul `CRYSTALS-Kyber` ialah saiz kuncinya. Berbanding algoritma kriptografi pasca-kuantum (PQC) yang lain, `CRYSTALS-Kyber` menawarkan saiz kunci yang jauh lebih kecil, menjadikannya lebih praktikal untuk aplikasi dunia sebenar. `CRYSTALS-Kyber` menyediakan tiga tahap keselamatan yang berbeza, setiap satunya dengan saiz kuncinya sendiri:

- **Kyber512**: Tahap keselamatan ini menyediakan 128 bit keselamatan dan menggunakan saiz kunci sebanyak 1,632 bait untuk kunci rahsia, 800 bait untuk kunci awam, dan 768 bait untuk teks sifer.
- **Kyber768**: Tahap keselamatan ini menyediakan 192 bit keselamatan dan menggunakan saiz kunci sebanyak 2,400 bait untuk kunci rahsia, 1,184 bait untuk kunci awam, dan 1,088 bait untuk teks sifer.
- **Kyber1024**: Tahap keselamatan ini menyediakan 256 bit keselamatan dan menggunakan saiz kunci sebanyak 3,168 bait untuk kunci rahsia, 1,568 bait untuk kunci awam, dan 1,568 bait untuk teks sifer.

Saiz kunci yang agak kecil ini menjadikan `CRYSTALS-Kyber` pilihan yang menarik untuk peranti yang terhad sumbernya, seperti telefon pintar dan peranti IoT. Ia juga mengurangkan lebar jalur yang diperlukan untuk menghantar kunci kriptografi, yang boleh memberi manfaat kepada aplikasi dengan sambungan rangkaian yang terhad.

#### Kelajuan yang Mantap: Mercu Tanda dalam Landskap Kewangan yang Pantas

Satu lagi aspek daya tarikan `CRYSTALS-Kyber` ialah kelajuannya. Dalam sektor perbankan dan perkhidmatan kewangan yang pantas, kelajuan sama pentingnya dengan keselamatan. Reka bentuk algoritma ini memastikan ia beroperasi dengan pantas, memudahkan proses penyulitan dan penyahsulitan yang cepat. Kecekapan ini tidak diperoleh dengan mengorbankan keselamatan; sebaliknya, ia hasil langsung daripada asas matematik canggih algoritma tersebut.

### CRYSTALS-Kyber: Simbiosis Keselamatan, Kecekapan dan Kelajuan

`CRYSTALS-Kyber` telah muncul sebagai peneraju dalam usaha mencari kriptografi rintangan kuantum, menawarkan gabungan unik antara keselamatan, kecekapan dan kelajuan. Pendekatan inovatif berasaskan kekisinya, saiz kunci yang lebih kecil, dan reka bentuk yang dioptimumkan menjadikannya pilihan ideal untuk melindungi maklumat sensitif dalam industri perbankan dan perkhidmatan kewangan. Sementara dunia terus menerima pakai teknologi digital, `CRYSTALS-Kyber` bersedia memainkan peranan penting dalam melindungi data kita untuk bertahun-tahun akan datang.

![Divider][01].class=\"m-10 w-100\"

## Kesan

### CRYSTALS-Kyber: Kelebihan untuk Perbankan dan Perkhidmatan Kewangan

Industri perbankan dan perkhidmatan kewangan sentiasa berlumba untuk kekal mendahului ancaman siber yang semakin canggih. Dalam konteks ini, `CRYSTALS-Kyber` menonjol bukan sahaja kerana ciri rintangan kuantum (QR)-nya tetapi juga kerana manfaat nyata yang ditawarkannya kepada industri ini. Bahagian ini menyelami kelebihan praktikal `CRYSTALS-Kyber`, sambil menekankan mengapa ia amat sesuai untuk keperluan unik institusi kewangan.

- **Keselamatan Dipertingkat dengan Kunci yang Lebih Kecil**: Salah satu kelebihan `CRYSTALS-Kyber` yang paling ketara ialah keupayaannya mencipta kunci penyulitan yang lebih kecil tanpa mengorbankan keselamatan. Dalam sektor di mana pelanggaran data boleh membawa akibat yang teruk, keselamatan yang kukuh tidak boleh ditawar-tawar. Saiz kunci yang lebih kecil yang ditawarkan oleh `CRYSTALS-Kyber` mempermudah proses pengurusan kunci, satu faktor kritikal dalam sistem perbankan berskala besar yang melibatkan ribuan kunci. Ini bukan sahaja meningkatkan keselamatan tetapi juga mengoptimumkan kecekapan storan dan penghantaran, satu faktor penting dalam era di mana kelajuan dan ruang amat bernilai.

- **Kelajuan dan Kecekapan**: Dalam perkhidmatan kewangan, di mana transaksi berlaku dalam milisaat, kelajuan operasi kriptografi amat penting. `CRYSTALS-Kyber` cemerlang dalam hal ini, menawarkan proses penjanaan kunci, enkapsulasi dan dekapsulasi yang pantas. Kelajuan ini memastikan langkah keselamatan tidak menjadi halangan dalam persekitaran dagangan frekuensi tinggi atau semasa transaksi berskala besar. Tambahan pula, kecekapan `CRYSTALS-Kyber` diterjemahkan kepada pengurangan sumber pengiraan, membawa kepada penjimatan kos dan operasi yang lebih mesra alam.

- **Kalis Masa Depan Terhadap Ancaman Kuantum**: Dengan kemunculan pengkomputeran kuantum, industri berhadapan dengan masa depan di mana kaedah kriptografi tradisional boleh menjadi lapuk. Dengan menerima pakai `CRYSTALS-Kyber`, institusi kewangan bukan sahaja menjamin masa kini mereka tetapi juga bersedia untuk dunia pasca-kuantum. Pendekatan proaktif terhadap keselamatan siber ini menunjukkan komitmen terhadap perlindungan data jangka panjang, satu pertimbangan penting bagi pihak berkepentingan dan pelanggan yang mengutamakan keselamatan data.

- **Pematuhan Kawal Selia dan Kelebihan Persaingan**: Sementara pengawal selia di seluruh dunia mula mengakui ancaman kuantum, mereka berkemungkinan akan mewajibkan penggunaan algoritma rintangan kuantum. Penerimaan awal `CRYSTALS-Kyber` meletakkan institusi kewangan sebagai peneraju dalam pematuhan dan keselamatan. Selain itu, ia menawarkan kelebihan persaingan, dengan meyakinkan pelanggan dan rakan kongsi tentang dedikasi institusi terhadap amalan keselamatan termaju.

![Divider][01].class=\"m-10 w-100\"

## Insentif

### Hujah untuk Menerima Pakai CRYSTALS-Kyber

Dalam landskap di mana keselamatan siber bukan sekadar keperluan malah pembeza persaingan, industri perbankan dan perkhidmatan kewangan berada pada satu detik genting. Penerimaan `CRYSTALS-Kyber` merupakan langkah strategik, yang selaras dengan kedua-dua keperluan keselamatan semasa dan anjakan teknologi masa depan. Bahagian akhir ini menggariskan insentif menarik untuk menyepadukan `CRYSTALS-Kyber` ke dalam infrastruktur kriptografi perkhidmatan kewangan.

- **Kekal Mendahului Aliran Keselamatan Siber**: Kebangkitan pengkomputeran kuantum menimbulkan ancaman besar kepada algoritma penyulitan tradisional, menjadikannya terdedah kepada penyahsulitan oleh komputer kuantum masa depan. Dengan menerima pakai `CRYSTALS-Kyber`, institusi kewangan dapat melindungi data sensitif dan infrastruktur kritikal mereka daripada ancaman yang sedang muncul ini.

- **Kecekapan Operasi dan Keberkesanan Kos**: Saiz kunci yang padat dan algoritma yang cekap pada `CRYSTALS-Kyber` membawa kepada penjimatan kos yang besar. Berbanding algoritma penyulitan tradisional, `CRYSTALS-Kyber` mengurangkan keperluan storan sehingga 50% dan penggunaan lebar jalur sehingga 30%, menghasilkan penjimatan kos yang ketara untuk institusi kewangan dengan volum data yang besar.

- **Penjajaran Kawal Selia dan Pengurusan Risiko**: Dengan beberapa badan kawal selia, termasuk National Institute of Standards and Technology (NIST) dan Agensi Kesiberan Kesatuan Eropah (ENISA), secara aktif mengesyorkan penerimaan penyelesaian kriptografi rintangan kuantum, penerima awal `CRYSTALS-Kyber` akan berada pada kedudukan yang baik untuk mematuhi keperluan kawal selia masa depan dan mengurangkan potensi risiko perundangan.

- **Meningkatkan Kepercayaan Pelanggan dan Reputasi Institusi**: Institusi kewangan terkemuka seperti Barclays dan Deutsche Bank telah menerima pakai `CRYSTALS-Kyber` untuk melindungi data pelanggan mereka dan menjamin transaksi kewangan kritikal mereka. Komitmen terhadap keselamatan termaju ini bukan sahaja melindungi institusi ini daripada kemungkinan serangan siber tetapi juga meningkatkan reputasi mereka sebagai penjaga amanah maklumat sensitif.

![Divider][01].class=\"m-10 w-100\"

## Kesimpulan

### Menjamin Masa Depan Kewangan dengan CRYSTALS-Kyber

Dalam menghadapi ancaman keselamatan siber yang sentiasa berkembang, industri perbankan dan perkhidmatan kewangan berdepan dengan pilihan penting. Algoritma penyulitan tradisional, yang dahulunya dianggap selamat, kini terdedah kepada kuasa pengkomputeran kuantum yang sedang muncul. `CRYSTALS-Kyber` muncul sebagai mercu keselamatan, menawarkan penyelesaian yang kukuh, cekap dan kalis masa depan untuk melindungi aset digital sektor kewangan.

Dengan gabungan unik ciri QR, kecekapan operasi dan saiz kunci yang lebih kecil, `CRYSTALS-Kyber` merupakan pengubah keadaan untuk keselamatan kewangan. Dengan menerima pakai `CRYSTALS-Kyber`, institusi bukan sahaja menjamin operasi semasa mereka tetapi juga bersedia untuk masa depan di mana pengkomputeran kuantum mentakrifkan semula keselamatan siber. Pendekatan proaktif ini menunjukkan komitmen terhadap standard keselamatan yang paling tinggi, meningkatkan kepercayaan pelanggan dan mengukuhkan daya tahan industri terhadap ancaman yang sentiasa berkembang.

Dalam dunia yang semakin saling berhubung dan digital, `CRYSTALS-Kyber` berdiri sebagai bukti kuasa penyelesaian yang inovatif dan berpandangan jauh. Penerimaannya oleh institusi kewangan terkemuka seperti Barclays dan Deutsche Bank merupakan pengesahan padu terhadap keupayaannya dan isyarat jelas kepada industri untuk memeluk penyelesaian kriptografi rintangan kuantum ini.

![Divider][01].class=\"m-10 w-100\"

Sebagai penutup, saya percaya penerokaan `CRYSTALS-Kyber` ini telah menerangi kesan mendalam kriptografi rintangan kuantum dalam sektor kewangan. Jika anda berminat untuk mendalami teknologi perintis ini atau mempunyai sebarang pertanyaan, saya menjemput anda untuk berhubung dengan saya di [LinkedIn ⧉][02] atau melalui [halaman hubungi][00].

Terima kasih sekali lagi atas masa anda dan saya berharap dapat mendengar daripada anda.

[00]: /contact/index.html "Hubungi"
[01]: https://cloudcdn.pro/clients/common/images/elements/divider.svg "Divider"
[02]: https://www.linkedin.com/in/sebastienrousseau/ "Sebastien Rousseau di LinkedIn"
[03]: /2023-10-16-protecting-data-in-the-quantum-age-the-hash-library-hsh/index.html "Melindungi Data dalam Era Kuantum: Pustaka Hash (HSH)"
[04]: https://cloudcdn.pro/stocks/diagrams/alice-bob-eve-kyber.svg "CRYSTALS-Kyber Key Encapsulation Mechanism (KEM)"
[05]: https://www.nist.gov/ "The National Institute of Standards and Technology (NIST)"
