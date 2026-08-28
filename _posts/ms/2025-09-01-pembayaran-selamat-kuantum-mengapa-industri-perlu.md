---
title: "Pembayaran Selamat Kuantum: Mengapa Industri Perlu Bertindak Sekarang"
tags: "quantum-safe payments, post-quantum cryptography, payments, EPAA, ISO 20022, SWIFT, SEPA, DORA, quantum computing, AI, cross-border payments, stablecoins"
subtitle: "Kesediaan selamat kuantum ialah keputusan infrastruktur semasa. Bukan keputusan masa hadapan."
description: "Pengkomputeran kuantum mengancam kriptografi sistem pembayaran. Kertas putih EPAA menggariskan risiko struktur dan keperluan mendesak untuk migrasi PQC."
date: "Sep 01, 2025"
language: "ms"
locale: "ms_MY"
banner: "https://cloudcdn.pro/stocks/images/digital-nodes.webp"
banner_alt: "Papan litar pengkomputeran kuantum dalam cahaya biru"
keywords: "pembayaran selamat kuantum, kriptografi pasca-kuantum, SEPA, SWIFT gpi, ISO 20022, keselamatan perkhidmatan kewangan, EPAA, tuai sekarang nyahsulit kemudian, ketangkasan kriptografi, Sebastien Rousseau"
---

## Ancaman Kuantum kepada Sistem Pembayaran

Infrastruktur pembayaran moden bergantung pada kriptografi kunci awam. RSA, ECC, dan Diffie-Hellman. Untuk mengesahkan transaksi, melindungi data pemegang kad, dan menjamin pemesejan antara institusi kewangan. Algoritma ini menjadi tunjang kepada SWIFT, SEPA, sistem penyelesaian kasar masa nyata, dan hampir setiap skim kad yang beroperasi hari ini.

Komputer kuantum yang menjalankan algoritma Shor akan berupaya memecahkan primitif kriptografi ini. Walaupun mesin kuantum toleran-kerosakan belum wujud pada skala yang diperlukan, trajektori pembangunan perkakasan. Sebagaimana ditunjukkan oleh IBM, Google, dan lain-lain. Menjadikan ini persoalan garis masa kejuruteraan dan bukannya persoalan teori. National Institute of Standards and Technology (NIST) telah pun memuktamadkan set piawaian kriptografi pasca-kuantum pertamanya (FIPS 203, 204, dan 205) sebagai tindak balas.

## Risiko Tuai Sekarang Nyahsulit Kemudian

Ancaman itu tidak terhad kepada tarikh masa hadapan apabila komputer kuantum mencapai keupayaan yang mencukupi. Pelaku peringkat negara dan musuh yang canggih sudah pun memintas dan menyimpan data tersulit hari ini, dengan hasrat untuk menyahsulitnya sebaik sahaja sumber kuantum tersedia. Strategi tuai sekarang nyahsulit kemudian (harvest-now decrypt-later, HNDL) ini bermakna sebarang data pembayaran yang mempunyai kepekaan jangka panjang. Rekod kawal selia, arkib pematuhan, kewajipan kontraktual. Sudah pun berisiko.

Pengawal selia kewangan telah mula bertindak balas. Monetary Authority of Singapore (MAS) telah mengeluarkan panduan mengenai kesediaan kuantum. Australian Prudential Regulation Authority (APRA) telah menandakan risiko kriptografi dalam rangka kerja daya tahan teknologinya. Digital Operational Resilience Act (DORA) Kesatuan Eropah mewajibkan pengurusan risiko ICT yang mesti mengambil kira ancaman yang sedang muncul, termasuk pengkomputeran kuantum.

## Kesan Merentas Landasan Pembayaran

Implikasinya merangkumi keseluruhan skop infrastruktur pembayaran:

**Pemesejan SWIFT:** Format mesej MT dan MX bergantung pada TLS dan tandatangan digital untuk integriti dan pengesahan. Infrastruktur kunci yang terjejas akan menjejaskan model kepercayaan yang menghubungkan lebih 11,000 institusi di seluruh dunia.

**SEPA dan pembayaran segera:** Skim SEPA Instant Credit Transfer daripada European Payments Council memproses transaksi tak boleh batal dalam masa kurang sepuluh saat. Kompromi kriptografi pada kelajuan ini tidak meninggalkan sebarang jendela untuk campur tangan manusia atau pengesahan manual.

**Sistem pembayaran masa nyata:** Faster Payments (UK), FedNow (AS), dan NPP (Australia) semuanya berkongsi kebergantungan yang sama pada primitif kriptografi klasik untuk pengesahan mesej dan pengesahan peserta.

**Pematuhan dan data hayat panjang:** Rekod pembayaran yang disimpan untuk tujuan kawal selia. Selalunya diwajibkan untuk lima hingga sepuluh tahun atau lebih lama. Akan hidup lebih lama daripada jaminan keselamatan kriptografi yang melindunginya pada masa ia dicipta. Program migrasi [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) mesti mengambil kira jangka hayat kriptografi bagi data yang mereka hasilkan.

**Blok rantai dan teknologi lejar teragih:** Platform aset digital dan instrumen pembayaran ditokenkan yang bergantung pada kriptografi lengkung eliptik menghadapi ancaman langsung dan difahami dengan baik daripada algoritma kuantum.

## Apa yang Organisasi Perlu Lakukan Sekarang

Peralihan kepada kriptografi selamat kuantum bukanlah satu naik taraf tunggal tetapi sebuah program berbilang tahun yang memerlukan persediaan berstruktur:

**Inventori kriptografi:** Organisasi mesti mengkatalog setiap sistem, protokol, dan stor data yang bergantung pada kriptografi kunci awam klasik. Ini termasuk sijil TLS, pengesahan API, konfigurasi HSM, sistem pengurusan kunci, dan penyulitan data-dalam-simpanan.

**Penerapan algoritma pasca-kuantum:** NIST telah memiawaikan ML-KEM (FIPS 203) untuk enkapsulasi kunci dan ML-DSA (FIPS 204) untuk tandatangan digital. Organisasi harus mula menguji algoritma ini dalam persekitaran bukan pengeluaran dan membangunkan pelan tindakan migrasi bagi sistem kritikal.

**Ketangkasan kriptografi:** Sistem mesti direka bentuk. Atau difaktor semula. Supaya algoritma kriptografi boleh digantikan tanpa memerlukan reka bentuk semula aplikasi sepenuhnya. Prinsip ini terpakai kepada gerbang pembayaran, perisian tengah pemesejan, dan API yang menghadap pelanggan sama.

**Pendekatan hibrid:** Semasa tempoh peralihan, skim kriptografi hibrid yang menggabungkan algoritma klasik dan pasca-kuantum menyediakan pertahanan berlapis. Pendekatan ini memelihara keserasian ke belakang sambil memperkenalkan ketahanan kuantum.

## Kumpulan Kerja EPAA dan Kerjasama Industri

Emerging Payments Association Asia (EPAA) menubuhkan Kumpulan Kerja Kriptografi Selamat Kuantumnya untuk menangani cabaran ini melalui tindakan industri yang diselaraskan. Kumpulan kerja itu menghimpunkan peserta dari seluruh ekosistem pembayaran, termasuk IBM, HSBC, KPMG, JPMorgan Chase, dan PayPal, antara lain.

Melalui bengkel yang diadakan di Sydney, Hong Kong, dan Singapura, kumpulan kerja itu telah membangunkan rangka kerja sepunya untuk menilai risiko kuantum dalam sistem pembayaran dan mengenal pasti laluan migrasi yang praktikal. Kertas putih yang terhasil. [Pembayaran Selamat Kuantum: Mengapa Industri Pembayaran Perlu Bertindak Sekarang][epaa]. Mewakili kedudukan konsensus tentang keperluan mendesak dan skop cabaran itu.

Analisis kumpulan kerja itu menyimpulkan bahawa kesediaan selamat kuantum ialah keputusan infrastruktur semasa, bukan keputusan masa hadapan. Organisasi yang berlengah berisiko mendapati diri mereka tidak mampu memenuhi jangkaan kawal selia, melindungi data hayat panjang, atau mengekalkan kesalingoperasian dengan rakan kongsi yang telah pun bermigrasi.

## Mengenai Penulis

Sebastien Rousseau ialah Pengurus Produk Digital Kanan di HSBC Bank plc, mengetuai produk API pembayaran korporat dalam Commercial & Investment Bank HSBC. Beliau menyumbang kepada Kumpulan Kerja Kriptografi Selamat Kuantum EPAA dan menyelidik aplikasi Kriptografi Pasca-Kuantum kepada perkhidmatan kewangan. [Baca lebih lanjut mengenai Sebastien ❯][00]

## Artikel Berkaitan

- [[Pengagihan Kunci Kuantum](/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html): Merevolusikan Keselamatan dalam Perbankan][rel1]
- [[CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html): Algoritma Pelindung dalam Zaman Kuantum][rel2]

[00]: /about/index.html "About Sebastien Rousseau"
[epaa]: https://emergingpaymentsasia.org/wp-content/uploads/2025/09/Quantum-Safe-Payments-Why-the-Payments-Industry-Must-Act-Now.pdf "EPAA Quantum-Safe Payments White Paper"
[rel1]: /2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html "Quantum Key Distribution: Revolutionising Security in Banking"
[rel2]: /2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html "CRYSTALS-Kyber: The Safeguarding Algorithm in a Quantum Age"
