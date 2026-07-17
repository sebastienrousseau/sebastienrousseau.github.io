---
title: "Set Semula Kriptografi Kuantum pada 2026: Piawaian PQC, Jaminan QKD, dan Kerja Migrasi yang Tidak Boleh Ditangguhkan Bank"
tags: "quantum cryptography, post-quantum cryptography, NIST, FIPS 203, FIPS 204, FIPS 205, ML-KEM, ML-DSA, SLH-DSA, NCSC, IETF, TLS, IPsec, QKD, ETSI, crypto-agility, HNDL, cybersecurity, ISO 20022, AI"
subtitle: "Kriptografi kuantum telah beralih daripada tinjauan masa hadapan kepada disiplin pelaksanaan: piawaian PQC NIST sudah bersedia, panduan NCSC UK telah mempersempit pilihan algoritma, kerja protokol IETF masih matang, dan jaminan QKD sedang beralih daripada keyakinan makmal kepada bahasa pensijilan."
description: "Kriptografi kuantum pada 2026 bukan lagi perdebatan tentang sama ada komputer kuantum sudah hampir tiba. Ia merupakan program migrasi merentasi kriptografi pasca-kuantum, ketangkasan kripto, jaminan pengagihan kunci kuantum, piawaian protokol, kesediaan pembekal, dan data kewangan berhayat panjang yang sudah terdedah kepada risiko tuai-sekarang-nyahsulit-kemudian."
date: "May 18, 2026"
language: "ms"
locale: "ms_MY"
banner: "https://cloudcdn.pro/stocks/images/alex-shuper-YYZnrK8NrSw-unsplash.webp"
banner_alt: "Peta migrasi kriptografi selamat-kuantum untuk 2026 yang menunjukkan piawaian PQC NIST, kerja protokol hibrid, jaminan QKD, ketangkasan kripto, dan tingkatan risiko data bank"
keywords: "kriptografi kuantum 2026, kriptografi pasca-kuantum, NIST FIPS 203, FIPS 204, FIPS 205, ML-KEM, ML-DSA, SLH-DSA, NCSC PQC, IETF TLS, IPsec, RFC 9794, pertukaran kunci hibrid, QKD, ETSI QKD, ISO IEC 23837, ketangkasan kripto, tuai sekarang nyahsulit kemudian, HNDL, kriptografi perkhidmatan kewangan, keselamatan perbankan"
---

## Set Semula Kriptografi Kuantum pada 2026: Piawaian PQC, Jaminan QKD, dan Kerja Migrasi yang Tidak Boleh Ditangguhkan Bank

Kriptografi kuantum pada 2026 telah berpecah kepada dua landasan praktikal. Kriptografi pasca-kuantum kini menjadi program pelaksanaan, kerana NIST berkata tiga piawaian pasca-kuantum sudah bersedia untuk digunakan dan sistem persekutuan mesti menganggapnya sebagai piawaian FIPS ([NIST](https://www.nist.gov/pqc "NIST Post-Quantum Cryptography")); [pengagihan kunci kuantum](/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html) menjadi masalah jaminan dan pensijilan, kerana penggunaan [QKD](/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html) memerlukan bahasa penilaian, profil perlindungan, dan piawaian operasi dan bukan sekadar demonstrasi makmal sahaja ([ID Quantique / ETSI QKD 016](https://www.idquantique.com/etsi-releases-qkd-protection-profile/ "ETSI releases QKD Protection Profile")).

---

> **Ringkasan Eksekutif / Perkara Utama**
>
> - **NIST telah menggerakkan PQC ke peringkat pelaksanaan.** Piawaian semasa ialah FIPS 203 untuk penubuhan kunci ML-KEM, FIPS 204 untuk tandatangan ML-DSA, dan FIPS 205 untuk tandatangan SLH-DSA, dengan NIST menggesa organisasi mengenal pasti kriptografi yang terdedah dan memulakan migrasi sekarang ([NIST](https://www.nist.gov/pqc "NIST Post-Quantum Cryptography")).
> - **NCSC UK telah mempersempit pilihan praktikal.** Ia mengesyorkan ML-KEM-768 dan ML-DSA-65 untuk kebanyakan kes penggunaan, sambil memberi amaran bahawa sistem harus bergantung pada pelaksanaan piawaian akhir yang kukuh dan bukannya eksperimen serasi-draf ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "NCSC next steps in preparing for PQC")).
> - **Kesediaan protokol tidak sekata.** IETF sedang mengemas kini TLS dan IPsec untuk PQC dan pertukaran kunci hibrid, tetapi NCSC memberi amaran bahawa sistem operasi harus mengutamakan RFC yang telah diterbitkan berbanding Internet Draft yang sentiasa berubah ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "NCSC next steps in preparing for PQC")).
> - **Hibrid ialah mekanisme peralihan, bukan keadaan akhir.** Skim kunci awam hibrid bersama pasca-kuantum membantu menyusun migrasi secara berperingkat dan melindung nilai risiko pelaksanaan, tetapi ia menambah kerumitan dan mungkin memerlukan migrasi kedua kepada PQC sahaja kemudian ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "NCSC next steps in preparing for PQC")).
> - **[QKD](/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html) bukan pengganti untuk PQC.** [QKD](/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html) boleh berkhidmat untuk pautan berjaminan tinggi yang khusus, tetapi kaitannya dengan perbankan bergantung pada pensijilan, kesalingoperasian, kos operasi, dan integrasi dengan sistem pengurusan kunci sedia ada dan bukan pada fizik semata-mata ([ID Quantique / ETSI QKD 016](https://www.idquantique.com/etsi-releases-qkd-protection-profile/ "ETSI releases QKD Protection Profile")).
> - **Soalan di peringkat bank ialah inventori.** Institusi kewangan yang tidak dapat mengesan RSA, ECDH, ECDSA, EdDSA, kripto VPN proprietari, templat HSM, jangka hayat sijil, dan kriptografi yang diurus pembekal tidak boleh bermigrasi, tanpa mengira piawaian mana yang tersedia.
> - **Risiko sudah pun aktif.** Serangan tuai-sekarang-nyahsulit-kemudian menjadikan data kewangan berhayat panjang terdedah sebelum wujudnya komputer kuantum yang relevan dari segi kriptografi, kerana pihak lawan hanya perlu mengumpul teks sifer hari ini.
> - **Ketangkasan kripto ialah kawalan yang tahan lama.** Seni bina yang menang bukanlah pertukaran sekali sahaja daripada RSA kepada ML-KEM; ia ialah keupayaan platform untuk memutar algoritma, parameter, pustaka, sijil, dasar perkakasan, dan mod protokol tanpa membina semula bank.
>
---

## Mengapa Minggu Ini Penting

Perbincangan tentang piawaian telah melepasi tahap abstraksi. Panduan awam NIST menyatakan bahawa organisasi harus mula menggunakan piawaian baharu sekarang, mengenal pasti tempat algoritma yang terdedah digunakan, dan merancang kemas kini produk, perkhidmatan, dan protokol ([NIST](https://www.nist.gov/pqc "NIST Post-Quantum Cryptography")). Bahasa itu penting kerana ia mengubah PQC daripada topik penyelidikan kepada kebergantungan penyegaran teknologi.

Masa juga penting kerana data kewangan mempunyai separuh hayat kerahsiaan yang panjang. Bahan M&A, aliran perbendaharaan, siasatan sekatan, dokumen identiti pelanggan, metadata penghalaan pembayaran, dan rekod penyelesaian borong boleh kekal sensitif selama bertahun-tahun. Komputer kuantum yang memecahkan kriptografi kunci awam klasik tidak perlu wujud hari ini untuk pendedahan itu menjadi rasional hari ini.

## Garis Dasar Kriptografi 2026: Empat Aliran Kerja

### 1. Piawaian PQC Sudah Cukup Sedia untuk Dirancang

Garis dasar pertama adalah algoritma. Program PQC NIST kini memberikan pemimpin teknologi sasaran yang bernama: ML-KEM untuk penubuhan kunci, ML-DSA untuk tandatangan digital am, dan SLH-DSA untuk tandatangan berasaskan cincang ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "NCSC next steps in preparing for PQC")). Kesan praktikalnya ialah pasukan perolehan, seni bina, dan pengurusan pembekal boleh berhenti bertanya sama ada piawaian PQC akan wujud dan mula bertanya bila setiap sistem akan menyokongnya.

Perkara yang lebih sukar ialah keserasian. NCSC memberi amaran bahawa pelaksanaan berdasarkan piawaian draf mungkin tidak serasi dengan piawaian akhir, yang merupakan jenis butiran yang menggagalkan migrasi bank besar jika diabaikan ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "NCSC next steps in preparing for PQC")). Oleh itu, bank harus memisahkan perintis eksperimen daripada laluan migrasi pengeluaran.

### 2. Protokol Ialah Halangan Utama

Algoritma tidak mengamankan trafik perbankan dengan sendirinya. TLS, IPsec, SSH, S/MIME, API pembayaran, integrasi HSM, dan tindanan pengurusan sijil semuanya memerlukan sokongan di peringkat protokol. NCSC menyatakan bahawa IETF sedang mengemas kini protokol yang digunakan secara meluas seperti TLS dan IPsec supaya algoritma PQC boleh disepadukan ke dalam mekanisme pertukaran kunci dan tandatangan ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "NCSC next steps in preparing for PQC")).

Ini menimbulkan masalah pelaksanaan berperingkat. Bank boleh menginventori kriptografi dengan segera, menuntut peta jalan pembekal dengan segera, dan mereka bentuk ketangkasan kripto dengan segera, tetapi ia mungkin masih perlu menunggu pelaksanaan protokol yang stabil sebelum memindahkan saluran pengeluaran berkekritikalan tinggi.

### 3. QKD Menjadi Disiplin Jaminan

[Pengagihan kunci kuantum](/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html) kekal relevan untuk pautan yang sangat khusus, terutamanya apabila institusi mengawal titik akhir dan laluan rangkaian. Perkembangan penting 2026 bukanlah satu kotak [QKD](/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html) baharu; ia ialah kemunculan bahasa pensijilan, dengan ETSI GS [QKD](/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html) 016 digambarkan sebagai satu pencapaian profil perlindungan untuk penilaian produk [QKD](/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html) ([ID Quantique / ETSI QKD 016](https://www.idquantique.com/etsi-releases-qkd-protection-profile/ "ETSI releases QKD Protection Profile")).

Bagi bank, ini mengalihkan perbincangan pembelian. Soalan yang betul bukan lagi sama ada [QKD](/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html) selamat-kuantum pada prinsipnya. Soalan yang betul ialah sama ada peranti, integrasi, proses pengurusan kunci, persekitaran operasi, dan bukti pensijilan memenuhi model ancaman bank.

### 4. Ketangkasan Kripto Ialah Seni Bina

Ketangkasan kripto ialah keupayaan untuk menukar algoritma tanpa menukar keseluruhan sistem. Ia meliputi pustaka perisian, rundingan protokol, dasar HSM, profil sijil, jangka hayat kunci, perkhidmatan tandatangan, bukti audit, dan laluan pengunduran. Tanpanya, setiap migrasi kriptografi menjadi projek tempahan khas.

Inilah pengajaran seni bina yang teras. Peralihan pasca-kuantum bukanlah peralihan kriptografi terakhir yang akan dihadapi oleh sistem kewangan. Bank yang membina ketangkasan kripto sekarang memperoleh satah kawalan yang boleh diguna semula untuk kemas kini algoritma, risiko pembekal, pembatalan kecemasan, dan bukti pengawal selia.

## Apa yang Perlu Dilakukan Bank Sekarang

### Bina Inventori Aset Kriptografi

Penyampaian pertama ialah bil bahan kriptografi. Ia harus merangkumi algoritma kunci awam, panjang kunci, pihak berkuasa sijil, templat HSM, versi TLS, produk VPN, get laluan pembayaran, API pihak ketiga, SDK mudah alih, pembungkus penyulitan data-rehat, kunci tandatangan, proses tandatangan perisian tegar, dan kriptografi yang diurus pembekal.

Inventori itu harus membezakan antara kerahsiaan dan ketulenan. Data tersulit berhayat panjang terdedah kepada risiko tuai-sekarang-nyahsulit-kemudian, manakala kunci tandatangan berhayat panjang menimbulkan risiko pemalsuan pada masa hadapan jika ia kekal berakar pada algoritma kunci awam yang terdedah.

### Segmentkan mengikut Separuh Hayat Data

Bukan semua data memerlukan urutan migrasi yang sama. Mesej pengesahan kad masa nyata mungkin mempunyai separuh hayat kerahsiaan yang berbeza daripada siasatan sekatan, fail pemerolehan korporat, pek identiti perbankan persendirian, atau dokumen terbitan hutang berdaulat. Inilah sebabnya migrasi kuantum tergolong dalam pengelasan data dan bukan hanya dengan keselamatan rangkaian.

Keutamaan harus diberikan kepada sistem yang melindungi data berhayat panjang dengan penubuhan kunci yang terdedah. Itulah sistem yang pengumpulannya hari ini mewujudkan pendedahan pada masa hadapan.

### Wajibkan Peta Jalan Pembekal dalam Kontrak

NIST menyatakan bahawa produk, perkhidmatan, dan protokol memerlukan kemas kini untuk peralihan ini ([NIST](https://www.nist.gov/pqc "NIST Post-Quantum Cryptography")). Ini bermakna bahasa perolehan mesti berubah. Pembekal harus mendedahkan garis masa sokongan PQC, keserasian piawaian akhir, tingkah laku mod hibrid, kekangan modul perkakasan, kesan prestasi, sokongan profil sijil, dan kawalan sandaran.

Pembekal yang hanya berkata "peta jalan selamat-kuantum" belum menjawab soalan itu. Bank memerlukan tarikh, algoritma, sempadan integrasi, dan bukti.

## PQC, QKD, dan Hibrid: Jadual Keputusan Praktikal

| Kawalan | Kegunaan Terbaik | Status 2026 | Peringatan Perbankan |
|---|---|---|---|
| **ML-KEM / FIPS 203** | Penubuhan kunci untuk kerahsiaan kalis masa hadapan | Dipiawaikan dan bersedia untuk perancangan pelaksanaan ([NIST](https://www.nist.gov/pqc "NIST Post-Quantum Cryptography")) | Memerlukan sokongan protokol dan pustaka sebelum pelancaran pengeluaran kritikal |
| **ML-DSA / FIPS 204** | Tandatangan digital am | Disyorkan untuk kebanyakan kes penggunaan tandatangan am oleh NCSC ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "NCSC next steps in preparing for PQC")) | Rantaian sijil dan migrasi PKI sukar dari segi operasi |
| **SLH-DSA / FIPS 205** | Tandatangan berasaskan cincang untuk tandatangan perisian tegar dan perisian | Piawaian akhir NIST yang dirujuk oleh NCSC ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "NCSC next steps in preparing for PQC")) | Tandatangan yang lebih besar mungkin menjejaskan persekitaran terkekang |
| **Skim PQ/T hibrid** | Migrasi sementara dan kesalingoperasian | Berguna sebagai langkah peralihan ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "NCSC next steps in preparing for PQC")) | Menambah kerumitan dan boleh memerlukan migrasi kedua |
| **QKD** | Pautan berjaminan tinggi yang khusus | Kerja jaminan semakin matang melalui aktiviti profil perlindungan ETSI ([ID Quantique / ETSI QKD 016](https://www.idquantique.com/etsi-releases-qkd-protection-profile/ "ETSI releases QKD Protection Profile")) | Tidak menyelesaikan pengesahan berskala internet am atau inventori kripto perusahaan |

## Apa Maksudnya mengikut Jenis Institusi

### Bank Universal Peringkat Pertama

Bank peringkat pertama memerlukan pejabat program, bukan bukti konsep. Model operasi sasaran harus menggabungkan inventori kriptografi, penguatkuasaan pembekal, pengurusan peta jalan HSM, persekitaran ujian untuk TLS/IPsec hibrid, dan bukti yang sedia untuk pengawal selia. Kerja awal yang bernilai paling tinggi bukanlah menukar setiap sifer dengan segera; ia ialah membina satah kawalan yang menjadikan perubahan selamat.

### Bank Peringkat Pertengahan dan Serantau

Bank peringkat pertengahan harus menganggap PQC sebagai latihan pengurusan pembekal dan pemiawaian platform. Mereka boleh mengelakkan kerja tempahan khas yang mahal dengan menumpukan sistem di sekitar pustaka yang disokong, tindanan TLS piawai, perkhidmatan sijil terurus, dan tarikh akhir pembekal yang jelas. Risiko utama ialah kriptografi tersembunyi di dalam perkakas, get laluan pembayaran, dan perisian tengah lama.

### Fintech, PSP, dan Institusi Bersempadan-Kripto

Fintech boleh bergerak lebih pantas kerana mereka biasanya mempunyai lebih sedikit sauh amanah lama. Risikonya ialah rasa berpuas hati dalam API pihak ketiga, tetapan lalai KMS awan, infrastruktur dompet, dan integrasi kustodi. Firma bersempadan-kripto harus berhati-hati terutamanya supaya tidak mengelirukan naratif keselamatan asli-blockchain dengan kesediaan pasca-kuantum.

### Jurutera dan Arkitek Keselamatan

Disiplin kejuruteraan adalah konkrit: tambah metadata algoritma pada inventori perkhidmatan, log mod protokol yang dirundingkan, cipta bendera ciri yang selamat untuk ujian hibrid, pendekkan jangka hayat sijil jika boleh, buang andaian algoritma berkod-keras, dan jadikan dasar kripto boleh digunakan melalui konfigurasi dan bukannya cabang kod.

## Kesimpulan

Set semula kriptografi kuantum bukanlah satu pembelian teknologi tunggal. Ia ialah model operasi kriptografi. NIST telah memberikan industri satu garis dasar piawaian, NCSC telah mempersempit panduan praktikal, badan protokol masih bergerak, dan jaminan QKD semakin menjadi formal. Institusi perbankan yang menang dalam peralihan ini bukanlah mereka yang mengumumkan perintis paling besar. Mereka ialah institusi yang tahu di mana kriptografi mereka berada, tahu data mana yang perlu dilindungi terlebih dahulu, dan boleh menukar primitif kriptografi tanpa membina semula bank.

## Soalan Lazim

**Adakah kriptografi pasca-kuantum sudah bersedia untuk digunakan oleh bank?**

Ia bersedia untuk perancangan, penglibatan pembekal, perintis, dan kerja pelaksanaan terpilih. NIST menyatakan bahawa tiga piawaian bersedia untuk dilaksanakan, manakala NCSC memberi amaran bahawa penggunaan operasi harus bergantung pada pelaksanaan piawaian akhir dan protokol stabil yang kukuh ([NIST](https://www.nist.gov/pqc "NIST Post-Quantum Cryptography"), [NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "NCSC next steps in preparing for PQC")).

**Adakah QKD menghapuskan keperluan untuk PQC?**

Tidak. QKD mungkin berguna untuk pautan terkawal yang khusus, tetapi PQC ialah laluan migrasi berskala untuk perisian am, protokol internet, API, sijil, dan sistem perusahaan. QKD juga bergantung pada rangka kerja jaminan dan pensijilan sebelum ia boleh dianggap sebagai infrastruktur bertaraf-bank ([ID Quantique / ETSI QKD 016](https://www.idquantique.com/etsi-releases-qkd-protection-profile/ "ETSI releases QKD Protection Profile")).

**Apa yang harus dimigrasikan terlebih dahulu?**

Sistem yang melindungi data sensitif berhayat panjang harus diutamakan. Ini termasuk penyulitan arkib, siasatan pembayaran, dokumen perbendaharaan dan pasaran modal, rekod identiti perbankan persendirian, fail perjanjian strategik, pihak berkuasa sijil akar, tandatangan perisian tegar, dan saluran antara bank.

**Apakah perangkap pelaksanaan yang terbesar?**

Perangkap terbesar ialah menganggap PQC sebagai pertukaran algoritma. Migrasi ini menyentuh protokol, sijil, HSM, pembekal, ujian prestasi, tindak balas insiden, pemantauan, dan tadbir urus. Tanpa ketangkasan kripto, institusi hanya mencipta semula masalah migrasi yang sama untuk perubahan algoritma yang seterusnya.

## Rujukan

- NIST, (2025). [Kriptografi pasca-kuantum ⧉](https://www.nist.gov/pqc "Kriptografi pasca-kuantum").
- NCSC, (2024). [Langkah seterusnya dalam bersedia untuk kriptografi pasca-kuantum ⧉](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "Panduan PQC NCSC").
- NIST CSRC, (2026). [Projek Kriptografi Pasca-Kuantum NIST ⧉](https://csrc.nist.gov/presentations/2026/mpts2026-3b1 "Projek PQC NIST").
- ID Quantique, (2024). [ETSI mengeluarkan Profil Perlindungan pertama di dunia untuk QKD ⧉](https://www.idquantique.com/etsi-releases-qkd-protection-profile/ "ETSI QKD 016").
