---
title: "Mengamankan Lejar: Panduan Peringkat Lembaga untuk Migrasi Pasca-Kuantum dalam Kewangan Korporat"
tags: "post-quantum cryptography, corporate banking, G7 CEG, BIS Project Leap, ML-KEM, ML-DSA, NCSC, ASD, CNSA 2.0, harvest now decrypt later, Mosca equation, crypto-agility, hybrid cryptography, ISO 20022, DORA, quantum computing, AI, Rust, open source, cross-border payments"
subtitle: "Risiko kuantum telah beralih daripada sekadar rasa ingin tahu penyelidikan kepada mandat kawal selia yang aktif. Dengan peta jalan G7 yang diterbitkan pada Januari 2026 dan BIS Project Leap yang membuktikan kebolehlaksanaan dalam sistem pembayaran langsung, persoalan peringkat lembaga bukan lagi sama ada perlu bermigrasi - sebaliknya sama ada migrasi itu dapat disiapkan sebelum jangka hayat data hari ini luput."
description: "Risiko kuantum telah beralih daripada sekadar rasa ingin tahu penyelidikan kepada mandat kawal selia yang aktif. Dengan peta jalan G7 yang diterbitkan pada Januari 2026, garis masa EU, UK dan ASD yang telah diperjelas, serta BIS Project Leap yang membuktikan kebolehlaksanaan pada peringkat bank pusat, persoalan bagi lembaga pengarah bukan lagi sama ada perlu bermigrasi - sebaliknya sama ada migrasi itu dapat disiapkan sebelum jangka hayat kriptografi bagi data hari ini luput."
date: "May 14, 2026"
language: "ms"
locale: "ms_MY"
banner: "https://cloudcdn.pro/stocks/images/getty-images-LaU3HadwEeE-unsplash.webp"
banner_alt: "Rajah peta jalan migrasi kriptografi pasca-kuantum - infrastruktur perbankan korporat beralih daripada RSA kepada ML-KEM dan ML-DSA"
keywords: "kriptografi pasca-kuantum, migrasi PQC, perbankan korporat, perkhidmatan kewangan, peta jalan G7 CEG, BIS Project Leap, ML-KEM, ML-DSA, FIPS 203, FIPS 204"
---

Risiko kuantum telah beralih daripada sekadar rasa ingin tahu penyelidikan kepada mandat kawal selia yang aktif. Dengan peta jalan G7 yang diterbitkan pada Januari 2026, garis masa EU, UK dan Australia yang telah diperjelas, serta BIS Project Leap yang membuktikan kebolehlaksanaan dalam sistem pembayaran langsung, persoalan bagi lembaga pengarah bukan lagi sama ada perlu bermigrasi — sebaliknya sama ada migrasi itu dapat disiapkan sebelum jangka hayat kriptografi bagi data hari ini luput.

---

> **Perkara Utama**
>
> - **2026 ialah tahun pendirian kawal selia mengeras.** Peta jalan Januari daripada G7 Cyber Expert Group, garis masa terselaras EU NIS Cooperation Group, dan pelan tiga fasa UK NCSC telah mengalihkan perbincangan daripada kesedaran kepada pelaksanaan. Australian Signals Directorate melangkah lebih jauh lagi, menetapkan tarikh akhir tegas 2030 untuk kriptografi asimetri klasik.
> - **Pendedahannya bersifat asimetri.** RSA, ECC dan Diffie–Hellman ialah masalah paling segera — algoritma asimetri yang mendasari jabat tangan SWIFT, TLS, PKI, penandatanganan kod, dan pengesahan rangkaian penjelasan. Penyulitan simetri (AES-256) kekal stabil selagi panjang kunci dikekalkan. Tumpuan peringkat lembaga mesti diberikan kepada permukaan asimetri.
> - **Harvest-now-decrypt-later bukan senario masa depan.** Musuh sedang memintas dan menyimpan log kewangan tersulit, rekod penyelesaian, bahan M&A, dan data wayar rentas sempadan pada hari ini, dengan niat jelas untuk menyahsulitnya sebaik sahaja komputer kuantum berkaitan kriptografi (CRQC) wujud. Bagi data dengan keperluan kerahsiaan 10–20 tahun, risiko itu sudah menjadi kenyataan.
> - **Industri kini mempunyai titik rujukan yang berfungsi.** [BIS Project Leap Fasa 2 ⧉](https://www.bis.org/publ/othp107.htm "Project Leap phase 2: quantum-proofing payment systems"), yang diterbitkan pada Disember 2025, berjaya menggantikan tandatangan digital tradisional dengan kriptografi pasca-kuantum dalam pemindahan kecairan langsung merentas TARGET2 — dan mendedahkan kos kejuruteraan khusus (kependaman pengesahan, saiz paket) yang akan dihadapi oleh setiap program migrasi.
> - **Suite NIST ialah sauh global.** [FIPS 203 (ML-KEM) ⧉](https://csrc.nist.gov/pubs/fips/203/final "FIPS 203, Module-Lattice-Based Key-Encapsulation Mechanism Standard") dan FIPS 204 (ML-DSA) dirujuk oleh setiap bidang kuasa utama, walaupun di tempat pendirian negara berbeza tentang set parameter dan keperluan hibrid. Lembaga pengarah harus menganggap ML-KEM-768/ML-DSA-65 sebagai tahap minimum dan ML-KEM-1024/ML-DSA-87 sebagai garis dasar konservatif untuk data berhayat panjang.
> - **Hibrid ialah satu-satunya laluan yang boleh dipercayai.** Peralihan terus sepenuhnya tidak disyorkan oleh mana-mana pihak berkuasa utama. Menjalankan algoritma klasik dan tahan-kuantum secara selari ialah corak penggunaan yang disokong oleh NCSC, ANSSI, BSI, dan terbukti dalam Project Leap. Ia lebih berat daripada kedua-dua alternatif, tetapi ia satu-satunya yang menangani keserasian hari ini serta ancaman esok.

---

## Tahun Pendirian Kawal Selia Mengeras

Untuk sebahagian besar dekad yang lalu, kriptografi pasca-kuantum hidup di sudut selesa dalam peta jalan jangka panjang. Komputer kuantum mengagumkan tetapi jauh; matematik kriptografi yang mendasari RSA dan lengkung eliptik dianggap sebagai substrat yang stabil; dan perbincangan migrasi sebahagian besarnya terhad kepada kumpulan kerja pakar. Kedudukan itu tidak lagi boleh dipertahankan.

Pada Januari 2026, [G7 Cyber Expert Group menerbitkan kenyataannya yang paling berpengaruh setakat ini ⧉](https://www.gov.uk/government/publications/advancing-a-coordinated-roadmap-for-the-transition-to-post-quantum-cryptography-in-the-financial-sector/g7-cyber-expert-group-statement-on-advancing-a-coordinated-roadmap-for-the-transition-to-post-quantum-cryptography-in-the-financial-sector-january-20 "G7 CEG Statement on Advancing a Coordinated Roadmap for the Transition to Post-Quantum Cryptography in the Financial Sector"), yang dipengerusikan bersama oleh Perbendaharaan AS dan Bank of England. Dokumen itu bukan peraturan, tetapi ia membawa lebih banyak bidasan daripada panduan biasa: ia mewakili pandangan bersama kementerian kewangan, bank pusat, dan pihak berkuasa penyeliaan merentas bidang kuasa G7 bahawa peralihan kriptografi kini menjadi isu pengurusan risiko sistemik. Peta jalan itu menyelaraskan ufuk perancangannya sekitar pertengahan 2030-an, dengan sistem kewangan kritikal digalakkan bermigrasi lebih awal — bahasa yang, dalam ungkapan berhati-hati para bank pusat, menandakan jangkaan dan bukan sekadar cadangan.

Dua bulan sebelumnya, BIS Innovation Hub dan Eurosystem menerbitkan keputusan [Project Leap Fasa 2 ⧉](https://www.bis.org/publ/othp107.htm "Project Leap phase 2: quantum-proofing payment systems"), suatu eksperimen teknikal yang menggantikan tandatangan digital tradisional dengan kriptografi pasca-kuantum dalam pemindahan kecairan langsung antara Bank of Italy, Banque de France, Deutsche Bundesbank, Nexi-Colt, dan Swift. Penemuan utamanya ialah kejayaan — pemindahan yang ditandatangani secara tahan-kuantum berjaya melalui sistem pembayaran operasi dari hujung ke hujung. Butiran di sebalik tajuk utama itu lebih memberi pengajaran, dan ia diteliti kemudian dalam artikel ini.

Gabungan dua peristiwa ini — rangka kerja dasar G7 yang terselaras dan bukti kerja dalam sistem pembayaran sebenar — telah menghasilkan apa yang telah dinantikan oleh komuniti teknikal selama sedekad: jawapan muktamad kepada persoalan "adakah ini nyata?" Jawapannya, pada Mei 2026, ialah ya. Persoalan yang tinggal ialah soal kelajuan.

## Tiga Vektor Ancaman Yang Sepatutnya Membimbangkan Lembaga

Sebelum membincangkan mekanik migrasi, wajar untuk tepat tentang apa sebenarnya yang berisiko. Risiko kuantum dalam perbankan korporat tidak seragam merentas estet kriptografi, dan perhatian lembaga paling baik diarahkan kepada tiga vektor di mana pendedahannya paling akut.

### 1. Harvest Now, Decrypt Later (HNDL)

Kebimbangan yang paling segera bukan masa depan. Ia masa kini. Musuh peringkat negara dan jenayah canggih sedang secara sistematik memintas dan menyimpan trafik kewangan tersulit — pemindahan wayar, aliran mesej SWIFT, komunikasi M&A, log penyelesaian rentas sempadan, perjanjian swap, dan fail KYC — tanpa keupayaan semasa untuk membacanya. Objektif mereka jelas: simpan sekarang, nyahsulit kemudian, sebaik sahaja CRQC wujud. Sebagaimana [Bank for International Settlements telah menyatakan secara jelas ⧉](https://www.bis.org/about/bisih/topics/cyber_security/leap.htm "Project Leap: quantum-proofing the financial system"), pengumpulan ini sudah pun berlaku.

Bagi lembaga pengarah, implikasinya tidak selesa tetapi khusus: sebarang data sensitif yang dihantar di bawah penyulitan asimetri klasik hari ini, yang keperluan kerahsiaannya melangkaui ketibaan CRQC, mesti sudah dianggap terdedah. Tiada notifikasi pelanggaran apabila HNDL berlaku. Tiada penggera dalam SIEM. Penyulitan itu bertahan — buat masa ini — tetapi data itu sudah pun meninggalkan perimeter.

### 2. Risiko Sensitiviti Jangka Panjang

Data perbankan korporat mempunyai jangka hayat institusi yang luar biasa panjang. Dokumentasi M&A strategik boleh kekal sensitif kepada pasaran selama satu dekad. Komunikasi rahsia perdagangan dan penilaian harta intelek mungkin kekal rahsia selama lima belas hingga dua puluh tahun. Log penyelesaian rentas sempadan, pendedahan pihak lawan pusat, dan penilaian kredit pihak lawan mengekalkan sensitiviti komersial jauh melangkaui hayat transaksi terdekatnya.

[Persamaan Mosca ⧉](https://www.cryptomathic.com/a-bankers-guide-to-quantum-safe-cryptography-part-3-roadmap-to-pqc-migration-for-financial-institutions-cryptomathic "A Banker's Guide to Quantum Safe Cryptography — Part 3"), yang asalnya dinyatakan oleh Michele Mosca dan kini terbenam dalam setiap rangka kerja migrasi yang serius, memformalkan masalah itu. Jika **S** ialah jangka hayat data, **M** ialah masa yang diperlukan untuk bermigrasi sistem yang melindunginya, dan **Q** ialah masa sehingga CRQC tersedia, maka:

```
Jika S + M > Q, data itu sudah terdedah.
```

Bagi data dengan ufuk kerahsiaan dua puluh tahun dan program migrasi yang secara realistik memerlukan lima hingga tujuh tahun untuk disiapkan, nilai Q tersirat yang dipertaruhkan oleh lembaga ialah sekurang-kurangnya 25 tahun ke hadapan. Semakin banyak penilaian pakar — [ramalan APAC 2026 daripada Forrester ⧉](https://www.forrester.com/press-newsroom/forrester-apac-2026-predictions/ "Forrester's 2026 APAC Predictions"), tinjauan tahunan Global Risk Institute, dan kertas seni bina Februari 2026 yang mencadangkan CRQC pada kira-kira 100,000 qubit fizikal menggunakan kod QLDPC — mencadangkan pertaruhan itu tidak selamat.

### 3. Kerentanan Jabat Tangan Teras

Vektor ketiga paling penting dari segi seni bina. Sifer simetri (AES-256) kekal agak stabil; algoritma Grover memotong tahap keselamatan berkesan kepada separuh, tetapi menggandakan panjang kunci memulihkan margin. Pendedahan yang bencana ialah kepada algoritma asimetri, dan inilah tepatnya algoritma yang mendasari setiap jabat tangan yang disahkan dalam kewangan korporat: RSA dalam infrastruktur kunci awam SWIFT, ECDSA dalam pengesahan klien/pelayan TLS, ECDH dalam penubuhan kunci sesi, dan varian ECC di seluruh pengesahan mudah alih klien, tandatangan API, dan saluran penandatanganan kod.

Sebuah CRQC berfungsi yang menjalankan algoritma Shor tidak melemahkan sistem ini secara beransur-ansur. Ia mematahkannya. Sebaik sahaja CRQC beroperasi, setiap jabat tangan yang dilindungi RSA, setiap tandatangan ECDSA, dan setiap pertukaran kunci lengkung eliptik menjadi boleh dipulihkan — bukan dalam usaha berbulan-bulan, tetapi dalam beberapa jam. Peralihan daripada "selamat" kepada "terjejas" adalah binari, dan ia merebak serentak merentas setiap sistem yang menggunakan algoritma yang terjejas. Inilah asas yang menyokong keperluan mendesak kawal selia.

## Pengetatan Kawal Selia: Pandangan Bidang Kuasa demi Bidang Kuasa

Gambaran kawal selia global pada Mei 2026 bukan lagi tampalan cadangan. Ia satu set garis masa terselaras yang berbeza dari segi ketegasan tetapi menuju ke destinasi yang sama. Sebuah bank multinasional yang beroperasi merentas pusat kewangan utama kini tertakluk kepada bidang kuasa terpakai yang paling ketat, bukan yang paling longgar.

### Amerika Syarikat

AS mempunyai pendirian paling preskriptif untuk mana-mana institusi yang menyentuh sistem persekutuan. [Commercial National Security Algorithm Suite 2.0 ⧉](https://informedclearly.com/en/technology/46563/quantum-encryption-race-post-quantum-security-standards-2026 "Quantum-Encryption Race 2026") daripada NSA mewajibkan ML-KEM-1024 dan ML-DSA-87 untuk sistem keselamatan negara, dengan sistem baharu dikehendaki menggunakan PQC dari Januari 2027 dan menyiapkan migrasi infrastruktur menjelang 2035. Memorandum OMB M-23-02 mengikat agensi persekutuan kepada trajektori yang sama. Bagi bank komersial, pendedahan segera ialah melalui rantaian perolehan persekutuan, kontrak berkaitan NSS, dan tekanan tidak langsung yang diletakkan oleh panduan NSA ke atas pasaran yang lebih luas.

### Kesatuan Eropah

EU beroperasi pada tiga lapisan. [Peta Jalan Pelaksanaan Terselaras Suruhanjaya Eropah ⧉](https://pqshield.com/pqc-transition-roadmaps-and-guidance/ "PQC Roadmaps and Transition Guidance"), yang diperincikan oleh NIS Cooperation Group pada Jun 2025, menetapkan pencapaian berfasa pada 2026 (strategi kebangsaan), 2030 (sistem berisiko tinggi dimigrasi), dan 2035 (peralihan penuh). Cyber Resilience Act akan mewajibkan naik taraf keselamatan mutakhir untuk produk digital dari hujung 2027. NIS2 mengukuhkan pengurusan risiko ICT, walaupun kedua-dua arahan itu tidak mengandungi keperluan PQC yang jelas. Pengawal selia kebangsaan, bagaimanapun, telah bergerak mendahului Suruhanjaya. BSI Jerman mewajibkan pertukaran kunci hibrid dan meluluskan bakul konservatif ML-KEM, FrodoKEM, dan Classic McEliece. ANSSI Perancis memerlukan hibrid untuk kedua-dua enkapsulasi kunci dan tandatangan. NLNCSA Belanda dan pihak berkuasa Norway telah menyelaraskan diri sekitar ML-KEM-1024 sebagai garis dasar konservatif untuk data berhayat panjang.

### United Kingdom

UK NCSC menerbitkan panduan muktamadnya pada Mac 2025 dan mengesahkannya semula melalui Annual Review 2025. Garis masa tiga fasa itu jelas:

- **Sehingga 2028** — Kenal pasti perkhidmatan kriptografi yang memerlukan naik taraf, bina pelan migrasi, dan hasilkan inventori kriptografi yang lengkap.
- **2028 hingga 2031** — Laksanakan naik taraf keutamaan tinggi, terutamanya pada sistem kritikal dan protokol internet menghadap luar.
- **2031 hingga 2035** — Siapkan migrasi merentas semua sistem, perkhidmatan, dan produk.

Bagi institusi kewangan UK, [Panduan PQC CMORG (Cross-Market Operational Resilience Group) ⧉](https://www.cmorg.org.uk/sites/default/files/2025-06/CMORG%20-%20Guidance%20for%20Post-Quantum%20Cryptography%20-%20April%202025%20-%20TLP%20CLEAR%20(1).pdf "CMORG Guidance for Post-Quantum Cryptography") berdiri di sisi rangka kerja NCSC, menganggap bank sebagai infrastruktur negara kritikal dan menekankan kesediaan vendor serta penyelarasan rantaian bekalan.

### Asia-Pasifik

Pendirian APAC lebih berpecah tetapi bergerak pantas. ASD Australia mempunyai pendirian paling keras secara global: kriptografi kunci awam klasik tidak boleh digunakan melangkaui hujung 2030, tiada saranan hibrid, dan ML-KEM-1024 diperlukan (ML-KEM-768 hanya boleh diterima sehingga 2030). Organisasi seharusnya mempunyai pelan peralihan yang diperhalusi menjelang hujung 2026. Monetary Authority Singapura telah mengeluarkan panduan kesediaan tahan-kuantum yang formal. Jepun dan Korea Selatan melabur secara besar-besaran, walaupun kedua-duanya mempunyai landasan algoritma kebangsaan (Korea telah memilih NTRU+ dan SMAUG-T sebagai KEM, ALMer dan HAETAE sebagai tandatangan). National Quantum Mission India, yang disokong oleh perbelanjaan kerajaan sebanyak Rs. 6,003.65 crore, secara jelas mengenal pasti sistem perbankan dan kewangan sebagai keutamaan strategik. [Ramalan APAC 2026 daripada Forrester ⧉](https://www.forrester.com/press-newsroom/forrester-apac-2026-predictions/ "Forrester's 2026 APAC predictions") meletakkan bilangan perusahaan serantau yang dijangka melabur dalam teknologi pasca-kuantum tahun ini pada lebih daripada 90%.

### Pendirian Bersih

Bagi sebuah lembaga, sintesis praktikal daripada pendirian bidang kuasa ini adalah mudah. Sebuah bank multinasional tidak boleh menguruskan mengikut garis masa mana-mana satu pengawal selia; ia mesti menguruskan mengikut yang paling ketat yang terpakai. Bagi kebanyakan institusi utama, ini bermakna ufuk perancangan hujung 2030 untuk sistem berisiko tinggi dan hujung 2035 untuk ekor panjang — dengan entiti terdedah ASD menyasarkan PQC tulen menjelang 2030 dan entiti terdedah CNSA menyasarkan tetingkap yang sama dengan ML-KEM-1024 dan ML-DSA-87 secara khusus.

## BIS Project Leap: Apa Yang Sebenarnya Telah Dibuktikan Oleh Industri

Project Leap wajar mendapat perhatian lembaga bukan kerana ia satu pencapaian pemasaran tetapi kerana ia demonstrasi kriptografi pasca-kuantum hujung-ke-hujung yang paling boleh dipercayai dalam sistem pembayaran kewangan langsung setakat ini. Kesimpulan utamanya adalah mudah: ia berfungsi. Butiran di sebaliknya ialah tempat implikasi operasi berada.

Fasa 1, yang disiapkan pada 2023, mewujudkan VPN tahan-kuantum antara sistem IT di Bank of France dan Deutsche Bundesbank, dengan mesej pembayaran dihantar antara Paris dan Frankfurt di bawah skim penyulitan hibrid. Fasa 2, yang disiapkan pada penghujung 2025 dan [dilaporkan pada Disember ⧉](https://www.bis.org/publ/othp107.htm "Project Leap phase 2: quantum-proofing payment systems"), melangkah jauh lebih ke hadapan. Konsortium itu menggantikan tandatangan digital tradisional berasaskan RSA dengan tandatangan pasca-kuantum dalam pelaksanaan pemindahan kecairan merentas TARGET2, sistem Real-Time Gross Settlement Eurosystem. Peserta — BIS Innovation Hub Eurosystem Centre, Bank of Italy, Banque de France, Deutsche Bundesbank, Nexi-Colt (yang menyediakan sambungan TARGET2), dan Swift — mewakili tepat institusi yang infrastrukturnya akhirnya mesti bermigrasi.

Laporan itu menandakan tiga penemuan yang setiap program migrasi harus hayati:

- **Kependaman pengesahan jauh lebih tinggi.** Pengesahan tandatangan pasca-kuantum mengambil masa jauh lebih lama daripada pengesahan berasaskan RSA pada perkakasan yang sama. Bagi sistem RTGS yang direka bentuk sekitar pengendalian mesej sub-saat, ini bukan pemerhatian marginal; ia satu input perancangan kapasiti.
- **Saiz paket memerlukan pembangunan semula sistem.** Tandatangan PQC lebih besar satu magnitud daripada setara ECDSA (lebih lanjut mengenai ini di bawah). Sistem pembayaran yang baris gilir dalaman, alat pemantauan, dan skema pangkalan datanya bersaiz untuk dimensi mesej lama tidak dapat menampung muatan baharu tanpa reka bentuk semula. Project Leap secara jelas mendapati bahawa TARGET2 tidak dapat "menampung dengan mudah" model hibrid tanpa pembangunan semula yang besar.
- **Hibrid ialah jawapan yang betul — tetapi ia lebih berat.** Menjalankan algoritma klasik dan pasca-kuantum secara selari mengekalkan keserasian ke belakang dan menyediakan pertahanan berlapis, tetapi ia menggandakan overhed pemprosesan kriptografi. Ini ialah kos operasi melaksanakan PQC dengan betul semasa peralihan; ia tidak dapat dielakkan melalui kejuruteraan bijak semata-mata.

Bagi seorang CFO yang menyemak kes perniagaan PQC, penemuan Project Leap berguna tepat kerana ia tepat. Kos migrasi pasca-kuantum bukan satu baris modal tunggal. Ia kependaman pengesahan yang menjalar melalui kontrak SLA, pengembangan saiz mesej yang menyentuh belanjawan storan dan lebar jalur, serta tempoh peralihan operasi kriptografi berganda yang menjejaskan perancangan kapasiti pengiraan. Tiada satu pun daripadanya bersifat spekulatif. Ia telah diukur dalam sistem bank pusat yang langsung.

## Kit Alat NIST: ML-KEM dan ML-DSA Dibandingkan

Tumpuan teknikal setiap rangka kerja kebangsaan yang boleh dipercayai ialah suite piawaian pasca-kuantum NIST yang diterbitkan pada Ogos 2024. Dua daripada piawaian ini menjadi fokus segera bagi perbankan korporat: ML-KEM (FIPS 203) untuk enkapsulasi kunci dan ML-DSA (FIPS 204) untuk tandatangan digital. Kedua-duanya berkongsi asas matematik — kedua-duanya bergantung pada kesukaran masalah Module Learning With Errors (ML-LWE) dan Module Short Integer Solution ke atas kekisi berstruktur — tetapi mereka memainkan peranan yang sangat berbeza dalam estet kriptografi, dan profil prestasi serta saiznya berbeza secara ketara.

### ML-KEM (FIPS 203) — Enkapsulasi Kunci

ML-KEM, yang diperoleh daripada [CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html), ialah pengganti untuk ECDH dan RSA-KEM dalam protokol di mana dua pihak perlu mewujudkan kunci simetri kongsi melalui saluran yang tidak selamat. Dari segi praktikal, di sinilah jabat tangan TLS pergi selepas RSA dan ECDH dipersara. NIST mentakrifkan tiga set parameter pada kekuatan keselamatan yang meningkat dan prestasi yang menurun: ML-KEM-512 (NIST Kategori 1), ML-KEM-768 (Kategori 3), dan ML-KEM-1024 (Kategori 5).

### ML-DSA (FIPS 204) — Tandatangan Digital

ML-DSA, yang diperoleh daripada CRYSTALS-Dilithium, ialah pengganti untuk tandatangan RSA dan ECDSA. Ia mengendalikan penandatanganan sijil, penandatanganan kod, penandatanganan dokumen, dan pengesahan. Tiga set parameter ialah ML-DSA-44, ML-DSA-65, dan ML-DSA-87, yang secara luas sepadan dengan NIST Kategori 2, 3, dan 5.

### Profil Saiz dan Prestasi

Bagi seorang CIO yang menentukan skop kapasiti migrasi, angka yang paling penting ialah saiz artifak. Inilah input kepada perancangan kapasiti rangkaian, unjuran storan, dan pengujian peringkat protokol.

| Algoritma | Kunci Awam | Sifer Teks / Tandatangan | Setara Klasik Terdekat | Saiz berbanding Klasik |
|---|---|---|---|---|
| ML-KEM-512 | 800 bait | 768 bait (sifer teks) | ECDH P-256 (~32 bait kunci awam) | ~25× lebih besar |
| ML-KEM-768 | 1,184 bait | 1,088 bait (sifer teks) | ECDH P-384 | ~25× lebih besar |
| ML-KEM-1024 | 1,568 bait | 1,568 bait (sifer teks) | ECDH P-521 | ~25× lebih besar |
| ML-DSA-44 | 1,312 bait | ~2,420 bait (tandatangan) | ECDSA P-256 (tandatangan 64 bait) | ~38× lebih besar |
| ML-DSA-65 | 1,952 bait | ~3,293 bait (tandatangan) | ECDSA P-384 | ~50× lebih besar |
| ML-DSA-87 | 2,592 bait | ~4,595 bait (tandatangan) | ECDSA P-521 | ~70× lebih besar |

*Sumber: Sintesis [NIST FIPS 203 ⧉](https://csrc.nist.gov/pubs/fips/203/final "FIPS 203, Module-Lattice-Based Key-Encapsulation Mechanism Standard") dan spesifikasi FIPS 204, dengan data perbandingan daripada literatur penanda aras bebas.*

Tiga implikasi operasi mengikut secara langsung. **Pertama**, saiz tandatangan ialah kekangan mengikat bagi kebanyakan penggunaan perusahaan. Tandatangan ML-DSA-65 kira-kira lima puluh kali saiz tandatangan ECDSA P-256, dan rantaian sijil TLS yang membawa CA perantaraan berkembang secara berkadaran. Kerja kapasiti pada permukaan ini bukan pilihan — ia menanggung beban. **Kedua**, ML-KEM berdaya saing dari segi pengiraan dengan ECDH dan dalam sesetengah pelaksanaan jauh lebih pantas, terutamanya pada perkakasan dengan sokongan tervektor untuk aritmetik kekisi yang mendasarinya. **Ketiga**, pengesahan ML-DSA secara konsisten pantas (selalunya lebih pantas daripada pengesahan ECDSA), tetapi penandatanganan ML-DSA melibatkan gelung persampelan-penolakan yang mungkin memerlukan beberapa percubaan pada perkakasan terkekang. Bagi perkhidmatan penandatanganan berdaya pemprosesan tinggi, ini ialah penanda aras yang perlu disahkan dan bukan diandaikan.

### Memilih Set Parameter

Pendirian bidang kuasa tentang pemilihan parameter tidak sama, tetapi penumpuannya jelas. ML-KEM-768 dan ML-DSA-65 ialah tahap minimum perusahaan — disokong oleh UK NCSC sebagai garis dasar untuk organisasi UK dan boleh diterima di bawah kebanyakan rangka kerja Eropah. ML-KEM-1024 dan ML-DSA-87 ialah siling konservatif — diwajibkan oleh NSA CNSA 2.0 untuk sistem keselamatan negara AS dan diperlukan oleh ASD untuk entiti terkawal Australia menjelang 2030. Bagi data dengan sensitiviti jangka panjang yang melampau — log penyelesaian berdaulat, harta intelek melebihi satu dekad, rekod jagaan bagi instrumen bertarikh panjang — set parameter yang lebih tinggi ialah lalai yang boleh dipertahankan.

### Asas Matematik Yang Dikongsi, Risiko Yang Dikongsi

Satu perkara peringkat lembaga yang wajar diperhatikan: kedua-dua ML-KEM dan ML-DSA memperoleh keselamatannya daripada keluarga masalah kekisi yang sama. Suatu penemuan kriptanalisis masa depan terhadap Module-LWE akan menjejaskan kedua-dua piawaian secara serentak. Inilah tepatnya sebab beberapa pihak berkuasa kebangsaan — terutamanya BSI Jerman dan ANSSI Perancis — mengesyorkan melengkapkan tindanan berasaskan kekisi dengan tandatangan berasaskan cincang (SLH-DSA, FIPS 205) untuk kes penggunaan penandatanganan jangka panjang dan penandatanganan kod. Keanjalan kripto, dalam erti kata ini, bukan sekadar tentang keupayaan menukar RSA dengan ML-KEM. Ia tentang keupayaan menukar satu algoritma PQC dengan yang lain apabila landskap kriptanalisis beralih.

## Laluan Migrasi Logik: Penemuan → Triase → Penggunaan Hibrid

Bagi sebuah lembaga yang meluluskan program PQC berbilang tahun, persoalan operasinya ialah bagaimana untuk memfasakan kerja tanpa mengambil risiko ketersediaan perkhidmatan yang tidak boleh diterima. Corak yang telah muncul merentas peta jalan G7, rangka kerja NCSC, BIS Project Leap, dan dokumen panduan kebangsaan utama menuju kepada tiga fasa.

```
┌──────────────────────┐   ┌──────────────────────┐   ┌──────────────────────┐
│  1. PENEMUAN & CBOM  │ → │  2. TRIASE (MOSCA)   │ → │  3. GUNA HIBRID      │
│  Inventori           │   │  Keutamaan berasaskan│   │  Sampul-berganda     │
│  kriptografi merentas│   │  risiko mengikut     │   │  klasik + PQC,       │
│  semua sistem        │   │  jangka hayat data   │   │  anjal-kripto        │
└──────────────────────┘   └──────────────────────┘   └──────────────────────┘
```

### Fasa 1 — Penemuan dan Bil Bahan Kriptografi (CBOM)

Migrasi tidak dapat dirancang untuk estet kriptografi yang belum dipetakan, dan kebanyakan institusi tidak mempunyai peta yang tepat. Fasa pertama oleh itu ialah penghasilan Bil Bahan Kriptografi — inventori berstruktur bagi setiap contoh kriptografi asimetri merentas organisasi, dengan setiap contoh ditandakan untuk algoritma, panjang kunci, konteks protokol, sensitiviti data, dan pemilik sistem. Pengimbasan automatik merentas pangkalan kod, aplikasi web, imej kontena, konfigurasi pangkalan data, stor sijil, modul keselamatan perkakasan, dan antara muka vendor ialah mekanisme praktikalnya; inventori manual bagi sistem lama dan protokol proprietari ialah pelengkap yang tidak dapat dielakkan.

Keluaran Fasa 1 tidak menawan, tetapi ia satu-satunya asas untuk Fasa 2 dan 3 berdiri. Ia juga penyerahan yang paling banyak dicari oleh kebanyakan fungsi audit dalaman dan pengawal selia luaran apabila pengesahan pematuhan PQC mula diminta.

### Fasa 2 — Triase Risiko Menggunakan Persamaan Mosca

Dengan CBOM di tangan, institusi boleh menggunakan rangka kerja Mosca aset demi aset. Bagi setiap kebergantungan kriptografi, persoalannya ialah sama ada **S + M > Q** — sama ada jangka hayat data ditambah masa migrasi melebihi anggaran masa sehingga CRQC. Aset di mana ketaksamaan itu paling akut — data sensitif berhayat panjang pada infrastruktur yang mengambil masa bertahun-tahun untuk bermigrasi — pergi ke hadapan barisan. Aset dengan jangka hayat data yang pendek atau infrastruktur yang telah dimodenkan boleh disusun kemudian dalam program.

Inilah fasa di mana selera risiko lembaga paling ketara. Nilai Q yang dipilih oleh institusi untuk dirancang, pada dasarnya, ialah pertaruhan strategik terhadap kadar kemajuan perkakasan kuantum. Q konservatif (pertengahan 2030-an) menghasilkan pelan migrasi yang lebih agresif dan baris modal jangka pendek yang lebih tinggi. Q optimistik (selepas 2040) menghasilkan pelan yang lebih santai dan pendedahan sisa yang lebih tinggi kepada data yang sedang dituai. Kedua-duanya bukan salah; kedua-duanya harus menjadi keputusan lembaga yang jelas, bukan lalai tersirat fungsi teknologi.

### Fasa 3 — Penggunaan Hibrid

Sebaik sahaja aset keutamaan dikenal pasti, penggunaan harus mengikut corak hibrid yang terbukti dalam Project Leap dan disokong oleh NCSC, ANSSI, BSI, dan peta jalan G7. Penggunaan hibrid menjalankan algoritma klasik dan algoritma pasca-kuantum secara selari, menggabungkan keluarannya menjadi satu sampul tunggal. Komposit itu selamat terhadap kedua-dua serangan klasik (algoritma klasik bertahan hari ini) dan serangan kuantum (algoritma PQC bertahan esok). Secara khusus, corak yang biasa ialah X25519 digabungkan dengan ML-KEM-768 atau ML-KEM-1024 untuk enkapsulasi kunci, dan ECDSA digabungkan dengan ML-DSA untuk tandatangan di mana tandatangan berganda boleh dilaksanakan dari segi operasi.

Penemuan Project Leap bahawa hibrid "jauh, jauh lebih berat" daripada mana-mana pendekatan tulen ialah penyeimbang jujur kepada saranan ini. Lembaga harus menjangka peningkatan kapasiti pengiraan dan storan, jabat tangan yang lebih lama, dan kerumitan rantaian sijil tambahan semasa peralihan. Pertukarannya ialah hibrid membuang sumber tunggal terbesar risiko migrasi: peralihan terus di tepi tebing daripada satu asas kriptografi ke satu lagi dalam persekitaran pengeluaran.

## Berapa Kosnya dan Mengapa Tidak Berbuat Apa-apa Lebih Mahal

Analisis Mastercard, [dilaporkan pada awal 2026 ⧉](https://www.qnulabs.com/blog/bank-2030-expiry-date-q-day-fatal-strategy "Your Bank's 2030 Expiry — QNu Labs"), meletakkan kos migrasi PQC sektor kewangan global pada $28–42 bilion. Dalam agregat itu, [penyelidikan RedCompass Labs dan CMORG ⧉](https://www.cmorg.org.uk/sites/default/files/2025-06/CMORG%20-%20Guidance%20for%20Post-Quantum%20Cryptography%20-%20April%202025%20-%20TLP%20CLEAR%20(1).pdf "CMORG Guidance for Post-Quantum Cryptography") yang menjejaki perbelanjaan institusi sebenar mencadangkan bank peringkat pertama komited $20–30 juta setahun kepada program kesediaan, dengan garis masa pelaksanaan merentangi berbilang kitaran kepimpinan. Ini angka yang besar. Namun, ia bukan perbandingan yang relevan.

Perbandingan yang relevan ialah kos satu peristiwa nyahsulit retrospektif tunggal. Bagi institusi yang trafik wayarnya yang dituai, korespondensi M&A, atau data pendedahan pihak lawan menjadi boleh dibaca oleh musuh pada 2032, kos operasi dan reputasinya tidak terbatas kepada baris capex migrasi. Ia terbatas kepada nilai satu dekad maklumat strategik yang mendasarinya — yang, bagi mana-mana institusi penting secara sistemik, jauh lebih besar daripada mana-mana belanjawan migrasi yang munasabah. Pembingkaian G7 tentang peralihan kriptografi sebagai isu pengurusan risiko sistemik dan bukan naik taraf teknologi adalah betul, dan lembaga harus melibatkan diri atas dasar itu.

Ada baris kos kedua yang wajar diasingkan. Migrasi kepada PQC ialah fungsi pemaksa untuk keanjalan kripto — keupayaan seni bina untuk menukar algoritma kriptografi tanpa membina semula sistem yang bergantung padanya. Kebanyakan institusi kini tidak mempunyai keanjalan kripto; kebergantungan RSA dan ECC mereka terbenam dalam-dalam pada PKI, rantaian penandatanganan kod, integrasi vendor, dan protokol tersuai yang telah terkumpul selama berdekad. Pelaburan dalam keanjalan, yang dibuat di bawah tekanan peralihan PQC, adalah tahan lama. Ia akan digunakan semula apabila peralihan kriptografi seterusnya tiba — sama ada pengganti kepada PQC berasaskan kekisi, lapisan pengedaran kunci kuantum, atau sesuatu yang belum lagi ada dalam peta jalan piawaian. Ditangani dengan betul, capex migrasi PQC ialah pelaburan sekali sahaja yang menghasilkan pilihan berulang.

## Kesimpulan

Hujah untuk menganggap migrasi pasca-kuantum sebagai keutamaan peringkat lembaga pada 2026 tidak dibina atas keakraban CRQC. Anggaran mengenainya kekal benar-benar tidak pasti — pendapat ilmiah yang boleh dipercayai meletakkan kebarangkalian CRQC menjelang 2028 pada jauh di bawah satu peratus, meningkat kepada kira-kira lima puluh peratus menjelang 2037–2040. Hujah itu dibina atas tiga pemerhatian lain yang tidak tidak pasti.

Pertama, harvest-now-decrypt-later berlaku hari ini, dan data dengan keperluan kerahsiaan melebihi satu dekad terdedah tanpa mengira bila CRQC tiba. Kedua, migrasi estet kriptografi institusi kewangan utama mengambil masa lima hingga tujuh tahun walaupun dengan pembiayaan dan tumpuan kepimpinan yang mencukupi — bermakna program yang dimulakan pada 2026 selesai sekitar 2031, yang jelas dalam hujung konservatif taburan kebarangkalian CRQC. Ketiga, jangkaan kawal selia telah mengeras secara ketara dalam dua belas bulan yang lalu, dan institusi yang minit lembaganya pada 2026 merekodkan program PQC yang jelas akan berada dalam kedudukan yang jauh lebih kukuh berbanding yang minitnya merekodkan sekadar sikap memerhati.

Institusi yang bermula sekarang mempunyai kelebihan pilihan. Mereka boleh menyusun kerja merentas kitaran kepimpinan, mengintegrasikannya dengan inisiatif daya tahan yang lebih luas, dan menyerap kos operasi penggunaan hibrid dalam perancangan modal biasa. Institusi yang menunggu akan menghadapi kerja yang sama di bawah tarikh akhir yang lebih ketat, dengan ruang penjujukan yang kurang, dan berlatar belakangkan kekangan bekalan pada perkakasan berkeupayaan PQC, kepakaran, dan kapasiti vendor. Kos bertindak awal diketahui; kos bertindak lewat bersifat asimetri tepat pada cara yang pengurusan risiko direka untuk mengelakkannya.

Untuk konteks terdahulu di laman ini, [tulisan April 2026 tentang pemampatan ambang kuantum](https://sebastienrousseau.com/2026-04-11-quantum-thresholds-are-moving-again/index.html "Quantum Thresholds Are Moving Again") meneliti trajektori perkakasan yang mendasari, [analisis November 2023 tentang CRYSTALS-Kyber](https://sebastienrousseau.com/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html "CRYSTALS-Kyber: The Safeguarding Algorithm in a Quantum Age") merangkumi asas matematik yang kini dipiawaikan sebagai ML-KEM, [artikel Disember 2023 tentang Pengedaran Kunci Kuantum](https://sebastienrousseau.com/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html "Quantum Key Distribution Revolutionising Security in Banking") menangani lapisan pelengkap [QKD](/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html), dan [pelaksanaan rujukan sumber terbuka KyberLib](https://sebastienrousseau.com/2023-11-28-kyberlib-a-rust-powered-shield-against-quantum-threats/index.html "KyberLib: A Rust-Powered Shield Against Quantum Threats") menyediakan pelaksanaan Rust yang berfungsi bagi primitif yang mendasari untuk institusi yang ingin memeriksa permukaan kriptografi secara langsung. Penglibatan dengan butiran praktikal dan teknikal — bukan sekadar tajuk kawal selia — ialah cara lembaga membezakan program migrasi yang boleh dipercayai daripada teater pematuhan.

## Soalan Lazim

**Bilakah komputer kuantum berkaitan kriptografi sebenarnya akan wujud?**

Anggaran yang boleh dipercayai berbeza dengan luas. Sehingga awal 2026, demonstrasi kuantum awam telah mencapai kira-kira 24 hingga 28 qubit logik, manakala CRQC dianggarkan memerlukan kira-kira 6,000 qubit logik yang disokong oleh sesuatu antara 100,000 dan beberapa juta qubit fizikal, bergantung pada pendekatan pembetulan ralat. Konsensus pakar meletakkan kebarangkalian CRQC di bawah satu peratus menjelang 2028, sekitar lima puluh peratus menjelang 2037–2040, dengan kebolehubahan yang ketara merentas ramalan. Pengurangan terkini dalam anggaran sumber teori — daripada 20 juta qubit beberapa tahun lalu kepada di bawah satu juta dalam kerja Gidney 2025, dan kepada kira-kira 100,000 dalam kertas seni bina QLDPC Februari 2026 — telah memampatkan ufuk perancangan. Untuk tujuan lembaga, andaian perancangan yang sesuai ialah pertengahan 2030-an untuk sistem berisiko tinggi, hujung 2030-an sebagai titik tengah konservatif, dan lebih awal jika pendedahan HNDL ialah kebimbangan yang mengikat.

**Mengapa penggunaan hibrid dan bukan pasca-kuantum tulen?**

Tiga sebab. Pertama, ML-KEM dan ML-DSA, walaupun telah disemak dengan baik, mempunyai sejarah kriptanalisis yang lebih pendek berbanding RSA dan ECC. Skim hibrid kekal selamat jika salah satu komponen bertahan; skim PQC tulen terdedah jika masalah kekisi dilemahkan secara tidak dijangka. Kedua, hibrid mengekalkan keserasian ke belakang dengan pihak lawan yang belum bermigrasi — kritikal dalam peralihan industri berbilang tahun. Ketiga, setiap pihak berkuasa utama selain Australian Signals Directorate secara jelas mengesyorkan hibrid untuk tempoh peralihan: NCSC, ANSSI, BSI, NLNCSA, dan rangka kerja G7 semuanya menyokong pendekatan sampul-berganda. Pertukarannya, seperti yang dikuantifikasi oleh Project Leap, ialah overhed pengiraan dan storan yang jauh lebih tinggi. Itulah harga pilihan.

**Adakah kita memerlukan kedua-dua ML-KEM dan ML-DSA, atau bolehkah kita memilih satu?**

Kedua-duanya. ML-KEM dan ML-DSA memainkan peranan kriptografi yang berbeza. ML-KEM menggantikan primitif penubuhan kunci dalam TLS, VPN, pengesahan mudah alih, dan protokol serupa di mana dua pihak perlu mempersetujui kunci simetri kongsi. ML-DSA menggantikan primitif tandatangan digital dalam sijil PKI, penandatanganan kod, penandatanganan dokumen, pemesejan yang disahkan gaya SWIFT, dan pernyataan identiti. Estet kriptografi institusi menggunakan kedua-dua jenis primitif di tempat yang berbeza; migrasi mesti menangani kedua-duanya. Saiz tandatangan ML-DSA yang jauh lebih besar (50–70× ECDSA) biasanya lebih menuntut dari segi operasi antara kedua-duanya; kerja perancangan rangkaian dan storan untuk ML-DSA mendominasi kebanyakan penilaian kapasiti migrasi.

**Bagaimanakah kita mengukur kemajuan pada program sebesar ini?**

Tiga metrik yang praktikal dan sejajar dengan rangka kerja kawal selia utama. **Liputan CBOM** — berapa peratus contoh kriptografi asimetri institusi telah diinventori, dikelaskan, dan ditandakan untuk keutamaan migrasi. **Liputan migrasi aset berisiko tinggi** — berapa peratus aset di mana syarat S + M > Q Mosca berlaku telah dipindahkan ke PQC hibrid. **Liputan keanjalan kripto** — berapa peratus sistem kebergantungan kriptografi boleh menukar algoritma tanpa perubahan kod, hanya konfigurasi. Peta jalan G7 CEG, rangka kerja tiga fasa NCSC, dan peta jalan terselaras EU semuanya memetakan lebih kurang kepada tiga ukuran ini, walaupun mereka menggunakan istilah yang berbeza.

**Berapakah kos menunggu setahun lagi?**

Ia bukan sifar, dan ia bukan simetri. Menunggu setahun mengorbankan setahun perlindungan HNDL pada data berhayat panjang — data yang keperluan kerahsiaannya melangkaui 2040 terdedah setahun lebih lama daripada yang diperlukan. Ia memampatkan tetingkap migrasi terhadap tarikh akhir kawal selia yang tetap (ASD 2030, pencapaian NSA CNSA 2.0, sasaran sistem kritikal EU 2030), yang diterjemahkan kepada risiko penyampaian yang lebih tinggi dan fleksibiliti penjujukan yang berkurangan. Ia mendedahkan institusi kepada kekangan bekalan vendor dan bakat yang sudah kelihatan dalam pasaran dan akan bertambah buruk apabila pemain terbesar industri beralih daripada perancangan kepada pelaksanaan. Kosnya tidak membencana dalam mana-mana satu tahun, tetapi ia berkompaun, dan persekitaran kawal selia sedang menuju kepada pendirian di mana lembaga akan dijangka menjelaskan kelewatan dan bukannya perbelanjaan.

## Rujukan

- Sebastien Rousseau, (2026). [Quantum Thresholds Are Moving Again](https://sebastienrousseau.com/2026-04-11-quantum-thresholds-are-moving-again/index.html "Quantum Thresholds Are Moving Again").
- Sebastien Rousseau, (2023). [CRYSTALS-Kyber: The Safeguarding Algorithm in a Quantum Age](https://sebastienrousseau.com/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html "CRYSTALS-Kyber: The Safeguarding Algorithm in a Quantum Age").
- Sebastien Rousseau, (2023). [Quantum Key Distribution Revolutionising Security in Banking](https://sebastienrousseau.com/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html "Quantum Key Distribution Revolutionising Security in Banking").
- Sebastien Rousseau, (2023). [KyberLib: A Rust-Powered Shield Against Quantum Threats](https://sebastienrousseau.com/2023-11-28-kyberlib-a-rust-powered-shield-against-quantum-threats/index.html "KyberLib: A Rust-Powered Shield Against Quantum Threats").
- G7 Cyber Expert Group, (2026). [Advancing a Coordinated Roadmap for the Transition to Post-Quantum Cryptography in the Financial Sector ⧉](https://www.gov.uk/government/publications/advancing-a-coordinated-roadmap-for-the-transition-to-post-quantum-cryptography-in-the-financial-sector/g7-cyber-expert-group-statement-on-advancing-a-coordinated-roadmap-for-the-transition-to-post-quantum-cryptography-in-the-financial-sector-january-20 "G7 CEG Statement, January 2026"). GOV.UK.
- Bank for International Settlements, (2025). [Project Leap Phase 2: Quantum-Proofing Payment Systems ⧉](https://www.bis.org/publ/othp107.htm "Project Leap phase 2: quantum-proofing payment systems"). BIS.
- Bank for International Settlements, (2025). [Project Leap: Quantum-Proofing the Financial System ⧉](https://www.bis.org/about/bisih/topics/cyber_security/leap.htm "Project Leap: quantum-proofing the financial system"). BIS.
- NIST, (2024). [FIPS 203: Module-Lattice-Based Key-Encapsulation Mechanism Standard ⧉](https://csrc.nist.gov/pubs/fips/203/final "FIPS 203, Module-Lattice-Based Key-Encapsulation Mechanism Standard"). NIST.
- UK NCSC, (2025). [Timelines for Migration to Post-Quantum Cryptography ⧉](https://www.ncsc.gov.uk/guidance/pqc-migration-timelines "Timelines for migration to post-quantum cryptography — NCSC"). UK National Cyber Security Centre.
- CMORG, (2025). [Guidance for Post-Quantum Cryptography ⧉](https://www.cmorg.org.uk/sites/default/files/2025-06/CMORG%20-%20Guidance%20for%20Post-Quantum%20Cryptography%20-%20April%202025%20-%20TLP%20CLEAR%20(1).pdf "CMORG Guidance for Post-Quantum Cryptography"). Cross-Market Operational Resilience Group.
- Post-Quantum Cryptography Coalition, (2025). [International PQC Requirements ⧉](https://pqcc.org/international-pqc-requirements/ "International PQC Requirements — Post-Quantum Cryptography Coalition"). PQCC.
- PQShield, (2025). [PQC Roadmaps and Transition Guidance ⧉](https://pqshield.com/pqc-transition-roadmaps-and-guidance/ "PQC Roadmaps and Transition Guidance"). PQShield.
- Banking.Vision, (2026). [The Year of Quantum Computing: 2026 ⧉](https://banking.vision/en/the-year-of-quantum-computing/ "The Year of Quantum Computing 2026"). Banking.Vision / msg for banking.
- The Quantum Insider, (2026). [How to Prep For Post-Quantum Cryptography: G7 Releases Roadmap ⧉](https://thequantuminsider.com/2026/01/15/how-to-prep-for-post-quantum-crytography-g7-releases-roadmap-to-help-financial-sector-navigate-transition-to-quantum-era/ "How to Prep For Post-Quantum Cryptography — The Quantum Insider"). The Quantum Insider.
- Quantum Computing Report, (2026). [Shor, QLDPC Codes, and the Compression of RSA-2048 Resource Estimates ⧉](https://quantumcomputingreport.com/shor-qldpc-codes-and-the-compression-of-rsa-2048-resource-estimates-part-i/ "Shor, QLDPC Codes, and the Compression of RSA-2048 Resource Estimates"). Quantum Computing Report.
- Cryptomathic, (2025). [A Banker's Guide to Quantum Safe Cryptography — Roadmap to PQC Migration for Financial Institutions ⧉](https://www.cryptomathic.com/a-bankers-guide-to-quantum-safe-cryptography-part-3-roadmap-to-pqc-migration-for-financial-institutions-cryptomathic "A Banker's Guide to Quantum Safe Cryptography"). Cryptomathic.
- Forrester, (2025). [2026 Asia Pacific Predictions: Quantum Security ⧉](https://www.forrester.com/press-newsroom/forrester-apac-2026-predictions/ "Forrester's 2026 APAC Predictions"). Forrester Research.
- The Asian Banker, (2025). [Building Resilience for a Quantum-Ready Financial System ⧉](https://www.theasianbanker.com/updates-and-articles/building-resilience-for-a-quantum-ready-financial-system "Building resilience for a quantum-ready financial system"). The Asian Banker.
