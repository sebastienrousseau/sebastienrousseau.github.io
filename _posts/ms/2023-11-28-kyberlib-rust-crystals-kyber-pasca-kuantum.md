---
title: "KyberLib: Rust CRYSTALS-Kyber untuk Pasca-Kuantum"
tags: "KyberLib, Rust, CRYSTALS-Kyber, post-quantum cryptography, lattice-based cryptography, key encapsulation mechanism, NIST, libsignal, cryptography, ISO 20022, quantum computing, AI"
subtitle: "KyberLib, pelaksanaan Rust yang kukuh bagi CRYSTALS-Kyber untuk era kuantum."
description: "Pelaksanaan Kriptografi yang Kukuh dan Selamat-Kuantum bagi Algoritma CRYSTALS-Kyber, untuk Melindungi Data Anda daripada Ancaman Kuantum dan Serangan Kriptanalitik."
date: "Nov 28, 2023"
language: "ms"
locale: "ms_MY"
banner: "https://cloudcdn.pro/clients/kyberlib/v1/logos/kyberlib.svg"
banner_alt: "Memperkasakan Komunikasi Selamat dalam Era Kuantum dengan KyberLib"
keywords: "KyberLib, Rust CRYSTALS-Kyber, kriptografi pasca-kuantum, kriptografi berasaskan kekisi, pertukaran kunci rintangan-kuantum, NIST FIPS 203, Sebastien Rousseau, KEM, pengesahan pembayaran, pustaka PQC"
---

[![Memperkasakan Komunikasi Selamat dalam Era Kuantum dengan KyberLib](https://cloudcdn.pro/clients/kyberlib/v1/logos/kyberlib.svg).class=\"img-fluid clearfix\"][07]

`KyberLib` ialah pustaka berasaskan Rust yang melindungi data anda daripada potensi ancaman pengkomputeran kuantum. Dibina di atas **algoritma [CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html)**, `KyberLib` menyampaikan keselamatan, kecekapan dan kepelbagaian yang luar biasa, mudah disepadukan ke dalam pelbagai platform, termasuk persekitaran `no-std`.

![divider][divider].class=\"m-10 w-100\"

## Melindungi Data Anda dalam Era Kuantum

Kemunculan pengkomputeran kuantum telah memperkenalkan ancaman yang ketara terhadap langkah keselamatan kriptografi konvensional. Untuk menangani cabaran ini, bidang Kriptografi Selamat-Kuantum (QSC) sedang berkembang pesat.

Di barisan hadapan gerakan transformatif ini ialah Institut Piawaian dan Teknologi Kebangsaan (NIST), yang menerajui penyeragaman algoritma QSC.

Pada tahun 2023, NIST telah menyenarai pendek empat algoritma inovatif:

- [**[CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html)** ⧉][01] (mekanisme enkapsulasi kunci)
- [**CRYSTALS-Dilithium** ⧉][02] (tandatangan digital)
- [**FALCON** ⧉][03] (tandatangan digital ringan)
- [**SPHINCS+** ⧉][04] (tandatangan digital berasaskan cincang)

Algoritma-algoritma terobosan ini diasaskan pada pelbagai prinsip matematik, termasuk kriptografi berasaskan kekisi, kriptografi berasaskan cincang, dan kriptografi berasaskan kod dengan matlamat menyediakan pertahanan yang kukuh terhadap serangan kuantum.

## Meneroka Kriptografi Berasaskan Kekisi

Kriptografi Berasaskan Kekisi (LBC) muncul sebagai peneraju dalam QSC, menawarkan penyelesaian Kriptografi Pasca-Kuantum (PQC) yang menjanjikan. LBC serba boleh, dengan aplikasi yang merangkumi mekanisme enkapsulasi kunci (KEM), tandatangan digital, dan skema penyulitan kunci awam yang berakar umbi pada kekisi matematik.

Kekisi ialah konsep asas dalam matematik yang telah menemui aplikasi dalam pelbagai bidang, termasuk kriptografi. Secara ringkas, kekisi ialah susunan titik yang teratur dalam ruang, membentuk struktur seperti grid. Titik-titik ini disambungkan oleh garisan, membentuk rangkaian sel yang saling berhubung. Susunan titik yang khusus dan jarak antaranya menentukan ciri unik sesuatu kekisi.

### Perwakilan Kekisi 3D dengan Vektor Asas

Graf ini mempersembahkan struktur kekisi 3D yang dijana oleh tiga vektor asas:

- `b1 = [1, 0, 0]` dalam warna merah,
- `b2 = [0, 1, 0]` dalam warna hijau, dan
- `b3 = [0, 0, 1]` dalam warna biru.

Setiap titik pada kekisi terbentuk dengan menggabungkan vektor asas ini dalam pelbagai perkadaran integer, menghasilkan corak seperti grid yang terbentang dalam ketiga-tiga dimensi ruang. Visualisasi ini menangkap intipati kekisi 3D, satu konsep yang digunakan secara meluas dalam fizik dan matematik untuk mewakili susunan titik yang teratur dan berulang dalam ruang.

![Perwakilan Kekisi 3D dengan Vektor Asas][06].class=\"img-fluid mx-auto d-block\"

Dalam kriptografi, kekisi digunakan sebagai asas bagi algoritma kriptografi tertentu. Kriptografi Berasaskan Kekisi (LBC) mengeksploitasi sifat matematik kekisi untuk mencipta skema kriptografi selamat yang tahan terhadap serangan daripada komputer kuantum. Komputer kuantum menimbulkan ancaman yang ketara terhadap kriptografi konvensional, kerana ia boleh memecahkan algoritma yang bergantung pada pemfaktoran nombor besar atau menyelesaikan masalah logaritma diskret dengan cekap.

[CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html) menggambarkan kekuatan LBC, menyediakan rintangan yang kukuh terhadap serangan kuantum digandingkan dengan kecekapan dan saiz kunci yang luar biasa. Pelbagai platformnya dan keserasiannya dengan kriptografi menjadikannya pilihan keselamatan data era kuantum yang boleh dipercayai.

Spesifikasi semasa [CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html) adalah seperti berikut:

- **Kyber512**: Menyediakan tahap keselamatan setara dengan penyulitan AES 128-bit, melindungi data sensitif dengan perlindungan piawaian industri.
- **Kyber768**: Menyediakan tahap keselamatan setara dengan penyulitan AES 256-bit, memastikan kerahsiaan maklumat yang amat sensitif.
- **Kyber1024**: Menyediakan tahap keselamatan yang melebihi penyulitan AES 256-bit, menawarkan perlindungan yang kukuh terhadap serangan kuantum dan melindungi integriti data jauh ke masa hadapan.

### Perbandingan Tahap Keselamatan antara Algoritma Klasik dan Rintangan-Kuantum

Carta bar ini menggambarkan tahap keselamatan relatif algoritma kriptografi klasik seperti RSA-2048 dan Algoritma Tandatangan Digital Lengkung Eliptik (ECDSA) berbanding spesifikasi varian Algoritma [CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html) rintangan-kuantum (Kyber512, Kyber768, dan Kyber1024).

Walaupun carta ini menyediakan perbandingan visual, adalah penting untuk diperhatikan bahawa tahap keselamatan tidak boleh dibandingkan secara langsung kerana ia berasaskan prinsip matematik yang berbeza.

Namun, carta ini memang menyediakan titik rujukan yang berguna untuk memahami tahap keselamatan algoritma rintangan-kuantum.

![Kriptografi Berasaskan Kekisi][05].class=\"img-fluid mx-auto d-block\"

![divider][divider].class=\"m-10 w-100\"

## KyberLib: Pustaka Rust untuk Kriptografi Rintangan-Kuantum

KyberLib memanfaatkan kuasa [CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html) untuk menyampaikan keselamatan memori yang lebih baik dan keselamatan peringkat sistem yang kukuh. Ia menyokong pelbagai spesifikasi [CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html) (Kyber512, Kyber768, Kyber1024), menawarkan pelbagai tahap keselamatan untuk memenuhi keperluan khusus anda. Pematuhannya terhadap `no_std` menjadikannya pilihan yang ideal untuk sistem terbenam, manakala keserasiannya dengan WebAssembly (WASM) memudahkan penyepaduan yang lancar ke dalam aplikasi web.

![divider][divider].class=\"m-10 w-100\"

## Melindungi Aplikasi Web dengan Kriptografi Rintangan-Kuantum

Direka untuk jejak memori yang minimum, KyberLib sesuai untuk sistem terbenam dan sistem terhad sumber tanpa menjejaskan keselamatan. Pelaksanaannya berasaskan Rust memanfaatkan ciri keselamatan bahasa tersebut, mengukuhkan keselamatan yang ditawarkan oleh algoritma [CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html).

Selain itu, keserasian KyberLib dengan WebAssembly meningkatkan kegunaannya dalam aplikasi web, menjamin bahawa ia kekal sebagai alat penting dalam dunia kriptografi yang dinamik.

[Mulakan dengan KyberLib Sekarang! ⧉][00] Mudah dipasang, percuma untuk kegunaan peribadi mahupun komersial, KyberLib ialah penyelesaian pilihan anda untuk kriptografi rintangan-kuantum.

[00]: https://kyberlib.com/getting-started/index.html "Getting Started"
[01]: https://pq-crystals.org/kyber/ "Kyber: A CCA-secure module-lattice-based KEM"
[02]: https://pq-crystals.org/dilithium/ "Dilithium: A CCA-secure lattice-based signature scheme"
[03]: https://falcon-sign.info/ "FALCON: A post-quantum signature scheme"
[04]: https://sphincs.org/ "SPHINCS+: A stateless hash-based signature scheme"
[05]: https://cloudcdn.pro/stocks/diagrams/kyber-vs-classical.svg "Comparison of Security Levels between Classical and Quantum-Resistant Algorithms"
[06]: https://cloudcdn.pro/stocks/diagrams/3D-lattice-graph.svg "3D Lattice Representation with Basis Vectors"
[07]: https://kyberlib.com/ "Privacy and Security in a Quantum World"

[divider]: https://cloudcdn.pro/clients/common/images/elements/divider.svg "Divider"
