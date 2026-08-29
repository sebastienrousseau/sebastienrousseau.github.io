---
title: "Ambang Kuantum Bergeser: Risiko Shor 10.000 Qubit"
subtitle: "Sebuah makalah baru menunjukkan Shor's algorithm dapat berjalan hanya dengan 10.000 qubit. Implikasinya bagi kriptografi sulit untuk diabaikan."
description: "Shor's algorithm kini mungkin berjalan hanya dengan 10.000 qubit. RSA, ECC, dan jadwal migrasi post-quantum semuanya semakin dekat. Inilah alasannya."
date: "Apr 11, 2026"
language: "id-ID"
locale: "id_ID"
banner: "https://cloudcdn.pro/stocks/images/leo_visions-Q_y8ZzhQ2_s-unsplash.webp"
banner_alt: "Diagram ambang batas qubit Shor's algorithm. Papan sirkuit komputasi kuantum dengan pola cahaya biru"
keywords: "komputasi kuantum, Shor's algorithm, 10000 qubit, kriptografi post-quantum, RSA-2048, elliptic curve cryptography, neutral atom qubits, koreksi kesalahan kuantum, cryptographic agility, jadwal ancaman kuantum"
---

![Diagram ambang batas qubit Shor's algorithm. Papan sirkuit komputasi kuantum dengan pola cahaya biru](https://cloudcdn.pro/stocks/images/leo_visions-Q_y8ZzhQ2_s-unsplash.webp).class=\"img-fluid clearfix\"

> **TL;DR.** Shor's algorithm mungkin kini dapat berjalan hanya dengan 10.000 qubit. RSA, ECC, dan jadwal migrasi post-quantum semuanya semakin dekat. Inilah alasannya.
>
> **Kesimpulan utama**
>
> - Sebuah makalah baru mengusulkan bahwa Shor's algorithm dapat dieksekusi hanya dengan **10.000 physical qubits**, kira-kira seratus kali lebih sedikit daripada estimasi konsensus sebelumnya.
> - Penurunan ini didorong oleh tiga kemajuan yang bertemu: high-rate quantum error-correcting codes, reconfigurable neutral atom arrays, dan paralelisme yang meningkat.
> - Ancaman tidak seragam. **Elliptic Curve Cryptography (ECC)** lebih rentan pada jumlah qubit lebih rendah; RSA-2048 membutuhkan runtime jauh lebih lama pada skala sebanding.
> - Ini adalah **proyeksi teoretis**, bukan demonstrasi yang sudah berjalan. Kesenjangan rekayasa besar masih ada antara hardware saat ini dan operasi fault-tolerant pada skala tersebut.
> - Standar post-quantum cryptography sudah final. Prioritas sekarang adalah **mempercepat migrasi**, bukan menunggu sistem kuantum muncul.

## Ambang Kuantum Bergeser Lagi

Sebuah makalah baru menunjukkan Shor's algorithm dapat berjalan hanya dengan 10.000 qubit. Ambang untuk quantum computing yang relevan secara kriptografis turun lebih cepat daripada asumsi kebanyakan pihak.

## Asumsi yang Akrab, Kini di Bawah Tekanan

Selama satu dekade terakhir, diskusi tentang quantum computing dan kriptografi mengikuti pola yang akrab. Mesin kuantum diakui kuat secara teoretis, tetapi dianggap tidak praktis pada skala besar. Memecahkan sistem kriptografi modern diperkirakan membutuhkan jutaan physical qubits, dan jadwalnya tetap terasa jauh. Asumsi itu kini berada di bawah tekanan serius.

Makalah terbaru, [Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits ⧉](https://arxiv.org/pdf/2603.28627 "Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits (PDF)"), mengusulkan sesuatu yang lebih konsekuensial daripada satu terobosan tunggal. Makalah ini menunjukkan bahwa ambang untuk komputasi kuantum yang relevan secara kriptografis mungkin satu orde magnitudo lebih rendah daripada yang sebelumnya diyakini. Bukan jutaan qubit, melainkan puluhan ribu. Perbedaan ini penting, dan arah yang ditunjukkannya sulit diabaikan.

## Konvergensi yang Mendorong Pergeseran: Error Correction, Arsitektur, dan Paralelisme

Hasil ini tidak muncul dari satu penemuan tunggal. Ia mencerminkan konvergensi peningkatan di beberapa lapisan stack quantum computing yang, jika digabungkan, menggeser batas dari apa yang tampak layak.

Peningkatan pertama berkaitan dengan error correction. Pendekatan tradisional membutuhkan overhead besar, sering kali ratusan physical qubits untuk mewakili satu logical qubit. Makalah ini justru bergantung pada high-rate quantum error-correcting codes, yang secara signifikan mengurangi overhead tersebut. ([Emergent Mind ⧉](https://www.emergentmind.com/papers/2603.28627 "Shor's Algorithm with 10000 Atomic Qubits")) Peningkatan kedua berkaitan dengan arsitektur. Sistemnya dibangun di atas array atom netral yang dapat dikonfigurasi ulang, yang dapat disusun ulang selama komputasi untuk memungkinkan konektivitas lebih fleksibel dan eksekusi lebih efisien. ([The Quantum Insider ⧉](https://thequantuminsider.com/2026/03/31/oratomic-launches-to-build-utility-scale-quantum-computers/ "Oratomic Launches to Build Utility-scale Quantum Computers")) Yang ketiga adalah paralelisme: meningkatkan jumlah qubit memungkinkan lebih banyak operasi berjalan secara simultan, mengurangi waktu eksekusi keseluruhan.

Tidak satu pun gagasan ini baru jika dilihat terpisah. Namun jika digabungkan, semuanya membingkai ulang apa yang sebelumnya dianggap batas keras.

## Dari Jutaan ke Puluhan Ribu: Apa Arti Angka-angkanya

Selama bertahun-tahun, estimasi konsensus untuk menjalankan Shor's algorithm pada skala kriptografis membutuhkan jutaan physical qubits. Analisis baru menunjukkan bahwa, dengan asumsi tertentu, angka ini dapat turun menjadi sekitar 10.000. ([arXiv ⧉](https://arxiv.org/abs/2603.28627 "Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits")) Namun angka tersebut bukan gambaran lengkap.

Pada batas bawah rentang itu, runtime tetap panjang. Memfaktorkan RSA-2048 dengan jumlah qubit minimal masih dapat memerlukan operasi kontinu selama bertahun-tahun. Eksekusi lebih cepat membutuhkan lebih banyak qubit, mungkin dalam puluhan ribu. Hubungan antara jumlah qubit dan runtime tidak linear, dan makalah ini berhati-hati menyajikannya sebagai spektrum, bukan ambang tetap. Yang berubah adalah arahnya: hambatan tidak lagi murni teoretis. Kini ia menjadi persoalan rekayasa.

### Asumsi Lama vs Realitas Baru

| Dimensi | Asumsi Lama | Realitas Baru |
|---|---|---|
| Physical qubits yang dibutuhkan (Shor's algorithm) | ~1.000.000+ | ~10.000-26.000 |
| Waktu untuk memecahkan RSA-2048 (pada qubit minimum) | Tidak layak dekade ini | Bertahun-tahun (pada 10K qubit); lebih cepat dengan lebih banyak qubit |
| Waktu untuk memecahkan ECC-256 | Tidak layak dekade ini | Beberapa hari (estimasi pada ~26K qubit) |
| Paradigma hardware dominan | Superconducting qubits | Reconfigurable neutral atom arrays |
| Overhead error correction | Ratusan physical qubits per logical qubit | Berkurang signifikan lewat high-rate codes |
| Sifat hambatan | Teoretis | Rekayasa |
| Urgensi migrasi | Perencanaan jangka panjang | Deployment aktif diperlukan sekarang |

*Sumber: Analisis berdasarkan [arXiv:2603.28627 ⧉](https://arxiv.org/abs/2603.28627) dan literatur sebelumnya.*

## Waktu, Skala, dan Kerentanan Sistem Kriptografi yang Tidak Merata

Salah satu kontribusi penting makalah ini adalah nuansa yang diperkenalkannya tentang waktu. Quantum advantage tidak tiba sekaligus. Ia berada pada spektrum yang ditentukan oleh skala sistem dan sifat target kriptografis.

Dengan sekitar 26.000 qubit, para penulis memperkirakan pemecahan elliptic curve cryptography dapat memakan waktu beberapa hari dalam kondisi menguntungkan. ([arXiv ⧉](https://arxiv.org/abs/2603.28627 "Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits")) Untuk RSA-2048, waktunya jauh lebih lama. Asimetri ini penting. Ini menunjukkan bahwa sistem kriptografi berbeda dapat menjadi rentan pada titik waktu berbeda, bukan secara bersamaan, dan transisi ke standar post-kuantum kemungkinan bukan satu peristiwa dengan satu tenggat tunggal.

Pola ini konsisten dengan pelaporan yang lebih luas. Analisis beberapa bulan terakhir menunjukkan bahwa sistem kuantum yang mampu menantang enkripsi yang umum digunakan dapat muncul sebelum akhir dekade. ([Nature ⧉](https://www.nature.com/articles/d41586-026-01054-1 "Quantum-computing breakthroughs pose risks to encryption")) Pemerintah dan badan standar sudah merencanakan transisi ke post-quantum cryptography, dengan timeline implementasi yang memanjang hingga 2030-an. ([The Quantum Insider ⧉](https://thequantuminsider.com/2026/03/31/oratomic-launches-to-build-utility-scale-quantum-computers/ "Oratomic Launches to Build Utility-scale Quantum Computers")) Diskusi telah bergeser dari apakah menjadi kapan.

## Kesenjangan Rekayasa yang Masih Tersisa

Penting untuk tepat tentang apa yang direpresentasikan makalah ini. Ini adalah proyeksi, bukan demonstrasi. Sistem yang diusulkan bergantung pada asumsi tentang error rates, stabilitas hardware, dan perilaku scaling yang belum divalidasi pada skala yang dibutuhkan. Eksperimen saat ini beroperasi pada level ratusan hingga ribuan rendah qubit, bukan puluhan ribu qubit yang beroperasi secara fault-tolerant dalam periode panjang. ([Phys.org ⧉](https://phys.org/news/2026-04-quantum-built-qubits-team.html "Useful quantum computers could be built with as few as 10,000 qubits"))

Kesenjangan rekayasa besar masih ada. Jalur dari model teoretis yang meyakinkan menuju sistem berfungsi yang mampu menjalankan operasi fault-tolerant berkelanjutan pada skala ini melibatkan tantangan yang belum sepenuhnya dipahami, apalagi diselesaikan. Yang berubah bukan kedekatan mesin yang sudah bekerja, melainkan kredibilitas targetnya. Kesenjangannya menyempit, dan arah kemajuannya konsisten.

## Mengapa Timeline yang Memadat Menuntut Perhatian Sekarang

Signifikansi karya ini bukan bahwa kriptografi akan segera pecah dalam waktu dekat. Signifikansinya adalah timeline memadat dengan cara yang memengaruhi keputusan hari ini. Sistem keamanan dirancang dengan lifecycle panjang. Data yang dienkripsi sekarang mungkin perlu tetap rahasia selama puluhan tahun. Keputusan infrastruktur yang dibuat tahun ini akan sulit dibalik dalam jendela lima tahun. Jika kapabilitas kuantum tiba lebih cepat dari perkiraan, asumsi tersebut menjadi rapuh.

Inilah alasan post-quantum cryptography sudah mulai diterapkan di sektor kritis. Bukan karena ancamannya segera, tetapi karena transisi membutuhkan waktu dan biaya keterlambatan bersifat asimetris. Ada pola berulang dalam sejarah komputasi: kemajuan tampak lambat sampai tiba-tiba tidak lagi lambat. Sesuatu yang bermula sebagai peningkatan teoretis menjadi kendala praktis, dan sesuatu yang dulu dianggap jauh menjadi sesuatu yang harus direncanakan. Quantum computing mungkin mengikuti lintasan itu, bukan melalui satu terobosan dramatis, tetapi melalui pengurangan bertahap dalam biaya, kompleksitas, dan skala.

## Apa Artinya bagi Industri: Panduan Praktis

Implikasi riset ini tidak seragam di semua sektor. Respons yang tepat bergantung pada jenis aset kriptografis yang berisiko, sensitivitas dan umur data, serta kecepatan bergeraknya ekspektasi regulasi.

### Layanan Keuangan dan FinTech

Lembaga keuangan menghadapi risiko berlapis: mereka menyimpan data sensitif berumur panjang, beroperasi pada infrastruktur dengan siklus penggantian lambat, dan berada di bawah pengawasan regulasi yang meningkat terkait ketahanan kriptografi. ECC banyak digunakan dalam koneksi TLS, autentikasi mobile, dan tanda tangan digital di payment rails. Kategori kriptografi yang diidentifikasi makalah ini paling rentan pada jumlah qubit lebih rendah. Institusi yang belum memulai inventaris kriptografi atau roadmap migrasi post-kuantum harus memperlakukan makalah ini sebagai pemicu percepatan, bukan alasan panik. [CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html) dan CRYSTALS-Dilithium, yang kini distandarkan NIST, adalah target migrasi yang tepat untuk key encapsulation dan tanda tangan digital.

### Pemerintah dan Pertahanan

Aktor negara memiliki motivasi terkuat, dan dalam banyak kasus sumber daya, untuk mempercepat pengembangan hardware kuantum melampaui apa yang diketahui publik. Pemerintah yang memegang komunikasi sensitif, data intelijen, atau kunci infrastruktur kritis harus mengasumsikan bahwa adversary sudah mengumpulkan data terenkripsi untuk didekripsi nanti, strategi yang dikenal sebagai "harvest now, decrypt later." Untuk organisasi sektor publik, kepatuhan terhadap mandat kesiapan kuantum nasional semakin tidak terhindarkan, dan jendela migrasi proaktif semakin menyempit.

### Kesehatan dan Infrastruktur Kritis

Rekam medis, sistem kontrol utilitas, dan jaringan industri memiliki kerentanan yang sama: data dan sistem dengan usia operasional sangat panjang, dilindungi standar kriptografi yang dirancang untuk model ancaman pra-kuantum. Rekam medis yang dienkripsi hari ini mungkin perlu tetap privat selama lima puluh tahun. Sistem kontrol yang disertifikasi tahun ini mungkin tetap beroperasi selama dua dekade. Untuk sektor-sektor ini, timeline yang memadat bukan kekhawatiran abstrak. Ini adalah tantangan langsung terhadap asumsi dasar di balik arsitektur keamanan saat ini.

## Kesimpulan

Aspek terpenting dari makalah ini bukan jumlah qubit spesifik yang disajikannya. Yang penting adalah arah yang disiratkan oleh angka tersebut. Pertanyaannya bukan lagi apakah komputer kuantum dapat menantang kriptografi modern. Pertanyaannya adalah seberapa cepat sistem yang dibutuhkan dapat dibangun, dan apakah organisasi yang bergantung pada standar saat ini bergerak cukup cepat sebagai respons.

Untuk saat ini, jawabannya tetap tidak pasti. Namun margin untuk menunda pertanyaan itu semakin menyempit, dan biaya menunggu meningkat dengan setiap penurunan kredibel pada ambang teoretis. Komunitas kriptografi, perencana keamanan, dan industri yang bergantung pada mereka sebaiknya memperlakukan makalah ini bukan sebagai alasan panik, melainkan sebagai dorongan serius untuk mempercepat transisi yang sudah berjalan.

## Pertanyaan yang Sering Diajukan

**Bisakah 10.000 qubit benar-benar memecahkan enkripsi RSA?**

Secara teoretis, ya. Tetapi dengan catatan penting. Walaupun estimasi sebelumnya menunjukkan jutaan physical qubits dibutuhkan, riset baru tentang high-rate error correction codes dan reconfigurable neutral atom arrays menunjukkan ambang tersebut jauh lebih rendah. Namun, pada 10.000 qubit, estimasi runtime untuk memfaktorkan RSA-2048 tetap sangat panjang, berpotensi bertahun-tahun operasi kontinu. Serangan yang lebih cepat membutuhkan lebih banyak qubit, kemungkinan di rentang puluhan ribu. Makalah ini adalah proyeksi berbasis asumsi yang dimodelkan, bukan demonstrasi pada sistem yang berfungsi.

**Enkripsi mana yang paling berisiko dari quantum computing?**

Elliptic Curve Cryptography (ECC) umumnya lebih rentan terhadap jumlah qubit lebih rendah daripada RSA-2048. Makalah ini memperkirakan pemecahan ECC dapat memakan waktu beberapa hari menggunakan sekitar 26.000 reconfigurable qubits dalam kondisi menguntungkan. RSA-2048 membutuhkan runtime jauh lebih panjang pada jumlah qubit sebanding. Asimetri ini berarti sistem yang bergantung pada ECC, umum dalam TLS, autentikasi mobile, dan blockchain, dapat menghadapi risiko pada timeline yang lebih pendek daripada infrastruktur berbasis RSA.

**Apa itu reconfigurable neutral atom qubit?**

Neutral atom qubits adalah atom individu, biasanya rubidium atau caesium, yang dijebak dan dimanipulasi menggunakan cahaya laser dalam ruang vakum. "Reconfigurable" berarti susunan atom dapat diubah secara dinamis selama komputasi, memungkinkan eksekusi rangkaian kuantum kompleks yang lebih efisien. Fleksibilitas ini mengurangi jumlah physical qubits yang dibutuhkan untuk mengimplementasikan operasi logis fault-tolerant dan menjadi alasan kunci makalah baru ini mencapai estimasi qubit lebih rendah daripada karya sebelumnya berbasis arsitektur superconducting qubit.

**Apa itu post-quantum cryptography dan mengapa diterapkan sekarang?**

Post-quantum cryptography (PQC) merujuk pada algoritma kriptografi yang diyakini aman terhadap komputer klasik maupun kuantum. NIST menyelesaikan set pertama standar PQC pada 2024, termasuk [CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html) untuk key encapsulation dan CRYSTALS-Dilithium untuk tanda tangan digital. Deployment dimulai sekarang, jauh sebelum komputer kuantum menjadi ancaman langsung, karena transisi kriptografi berjalan lambat. Mengganti standar tertanam di infrastruktur global biasanya membutuhkan satu dekade atau lebih, dan data yang dienkripsi hari ini mungkin perlu tetap rahasia lama setelah kapabilitas kuantum matang.

**Berapa banyak qubit yang dimiliki komputer kuantum paling kuat saat ini?**

Per awal 2026, sistem kuantum terdepan beroperasi pada rentang ratusan hingga ribuan rendah physical qubits. Yang penting, sebagian besar belum fault-tolerant. Sistem tersebut beroperasi di bawah ambang error-correction yang dibutuhkan untuk komputasi logis yang berkelanjutan dan andal. Kesenjangan antara hardware hari ini dan puluhan ribu logical qubits berfidelitas tinggi dan fault-tolerant yang dijelaskan dalam makalah baru ini masih signifikan, walaupun laju kemajuan di platform superconducting, neutral atom, dan trapped-ion semakin cepat.

## Referensi

- Sebastien Rousseau, (2025). [Quantum-Safe Payments: Why the Payments Industry Must Act Now](https://sebastienrousseau.com/2025-09-01-quantum-safe-payments-epaa/index.html "Quantum-Safe Payments: Why the Payments Industry Must Act Now").
- Sebastien Rousseau, (2023). [Quantum Key Distribution: Revolutionising Security in Banking](https://sebastienrousseau.com/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html "Quantum Key Distribution: Revolutionising Security in Banking").
- Sebastien Rousseau, (2023). [[CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html): The Safeguarding Algorithm in a Quantum Age](https://sebastienrousseau.com/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html "
[CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html): The Safeguarding Algorithm in a Quantum Age").
- Anonymous, (2026). [Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits ⧉](https://arxiv.org/abs/2603.28627 "Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits"). arXiv preprint arXiv:2603.28627.
- Castelvecchi, D. (2026). [Quantum-computing breakthroughs pose risks to encryption ⧉](https://www.nature.com/articles/d41586-026-01054-1 "Quantum-computing breakthroughs pose risks to encryption"). Nature.
- Phys.org, (2026). [Useful quantum computers could be built with as few as 10,000 qubits ⧉](https://phys.org/news/2026-04-quantum-built-qubits-team.html "Useful quantum computers could be built with as few as 10,000 qubits"). Phys.org.
