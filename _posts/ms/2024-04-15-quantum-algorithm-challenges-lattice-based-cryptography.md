---
title: "Algoritma Kuantum Mencabar Kriptografi Berasaskan Kekisi"
tags: "quantum algorithms, cryptography, lattice problems, LWE, post-quantum cryptography, cybersecurity, research, innovation, future-proofing, ISO 20022, quantum computing, AI"
subtitle: "Algoritma kuantum masa polinomial seterusnya untuk kriptografi berasaskan kekisi"
description: "Algoritma kuantum masa polinomial baharu oleh Yilei Chen menyasarkan kriptografi berasaskan kekisi. Implikasi terhadap piawaian pasca-kuantum termasuk CRYSTALS-Kyber."
date: "Apr 01, 2024"
language: "ms"
locale: "ms_MY"
banner: "https://cloudcdn.pro/stocks/images/digital-constellation.webp"
banner_alt: "Sepanduk nod rangkaian dalam ruang biru digital"
keywords: "pengkomputeran kuantum, algoritma kuantum, kriptografi kekisi, LWE, penyulitan, kriptografi pasca-kuantum, keselamatan siber, Yilei Chen, penyelidikan kriptografi, ancaman keselamatan"
---

## Ringkasan Eksekutif

Artikel ini menyelidiki kerja [**Yilei Chen ⧉**][00], yang telah membangunkan sebuah `algoritma kuantum masa polinomial` yang boleh memberi kesan ketara terhadap kesukaran masalah matematik **Learning With Errors (LWE)**, suatu cabaran asas dalam kriptografi berasaskan kekisi.

Kekisi ialah subkumpulan diskret ruang Euclidan berdimensi-n yang memainkan peranan penting dalam skema kriptografi moden. Masalah LWE melibatkan pencarian vektor rahsia berdasarkan satu set persamaan linear anggaran dan menjadi tonggak kepada banyak protokol kriptografi pasca-kuantum.

## Algoritma Kuantum Masa Polinomial Chen

Algoritma Chen menawarkan penyelesaian kepada masalah `vektor terpendek berkeputusan (GapSVP)` dan `masalah vektor bebas terpendek (SIVP)` bagi kekisi berdimensi apa jua. Ia mencapai ini dengan kerumitan masa polinomial, satu peningkatan yang ketara berbanding penyelesaian terdahulu.

Inovasi utama dalam kerjanya termasuk:

* **Fungsi Gaussian dengan Varians Kompleks:** Chen memperkenalkan penggunaan fungsi Gaussian dengan varians kompleks dalam reka bentuk algoritma kuantum. Pendekatan ini memanfaatkan sifat taburan Gaussian kompleks untuk memanipulasi keadaan kuantum dengan lebih berkesan, membolehkan penyelesaian yang lebih cekap kepada masalah LWE.

* **Transformasi Fourier Kuantum Bertingkap:** Algoritma ini menggunakan transformasi Fourier kuantum bertingkap.

## Pengenalan kepada Masalah Kekisi dan Kepentingannya dalam Kriptografi

Masalah kekisi melibatkan kajian struktur matematik yang dipanggil kekisi, iaitu subkumpulan diskret ruang Euclidan berdimensi-n. Masalah ini telah mendapat perhatian yang ketara dalam kriptografi kerana andaian ketahanannya terhadap serangan kuantum.

Masalah kekisi yang paling ketara ialah [**masalah Learning With Errors (LWE) ⧉**][01], yang diperkenalkan oleh Oded Regev. LWE ialah masalah pengiraan yang melibatkan pencarian vektor rahsia berdasarkan satu set persamaan linear anggaran.

Banyak skema kriptografi moden, seperti sistem kripto Regev dan pertukaran kunci Frodo, mengasaskan keselamatannya pada kesukaran menyelesaikan masalah LWE.

## Algoritma Klasik untuk Masalah Kekisi dan Batasannya

Algoritma klasik untuk menyelesaikan masalah kekisi, seperti **algoritma Lenstra-Lenstra-Lovász (LLL)** dan variannya, telah dikaji secara meluas dalam bidang kriptografi. Walau bagaimanapun, algoritma ini menghadapi cabaran yang ketara dari segi kerumitan pengiraan, terutamanya apabila dimensi kekisi meningkat.

Algoritma klasik yang terkenal untuk menyelesaikan masalah LWE bergantung secara eksponen kepada bilangan pemboleh ubah, menjadikannya tidak praktikal untuk kekisi berdimensi tinggi. Halangan kerumitan ini telah menjadi faktor utama dalam keselamatan skema kriptografi berasaskan LWE.

## Percubaan Terdahulu Membangunkan Algoritma Kuantum untuk LWE

Sebelum kerja Chen, beberapa penyelidik telah meneroka potensi algoritma kuantum untuk menyelesaikan masalah LWE.

Oded Regev telah berjaya membangunkan pengurangan kuantum daripada `GapSVP` kepada `LWE`. Walau bagaimanapun, perlu diperhatikan bahawa pengurangan ini memerlukan orakel kuantum untuk menyelesaikan GapSVP, yang kewujudannya masih belum dibuktikan.

Kuperberg mencipta [**algoritma kuantum untuk menyelesaikan LWE dengan faktor anggaran sub-eksponen ⧉**][02]. Walau bagaimanapun, pendekatan algoritma ini sama ada bergantung pada andaian yang belum disahkan atau menunjukkan kelajuan pengiraan yang lebih perlahan. Sebaliknya, algoritma Chen menawarkan penyelesaian masa polinomial tanpa memerlukan orakel kuantum.

## Algoritma Kuantum Masa Polinomial Chen untuk LWE

Algoritma kuantum Yilei Chen untuk menyelesaikan masalah LWE dalam masa polinomial mewakili satu penemuan penting dalam bidang ini. Algoritma tersebut menggunakan dua teknik baharu:

1. **Fungsi Gaussian dengan Varians Kompleks**: Chen memperkenalkan penggunaan fungsi Gaussian dengan varians kompleks dalam reka bentuk algoritma kuantum. Pendekatan ini memanfaatkan sifat taburan Gaussian kompleks untuk memanipulasi keadaan kuantum dengan lebih berkesan, membolehkan penyelesaian yang lebih cekap kepada masalah LWE.

2. **Transformasi Fourier Kuantum Bertingkap**: Algoritma ini menggunakan transformasi Fourier kuantum bertingkap, yang membolehkan analisis masalah secara serentak dalam kedua-dua domain masa dan frekuensi. Teknik ini membolehkan algoritma memproses struktur kekisi berdimensi tinggi dengan cekap dan mengekstrak maklumat yang relevan untuk menyelesaikan LWE.

Algoritma Chen menggabungkan teknik-teknik untuk menyelesaikan `LWE`, `GapSVP`, dan `SIVP` dalam masa polinomial bagi semua dimensi kekisi. Ini merupakan peningkatan besar berbanding algoritma klasik dan kuantum terdahulu.

## Implikasi, Batasan, dan Hala Tuju Penyelidikan Masa Depan

Algoritma kuantum Chen mempunyai implikasi terhadap LWE, mencabar tanggapan bahawa serangan kuantum tidak dapat memecahkan LWE dan masalah berasaskan kekisi yang serupa. Andaian ini menjadi asas kepada banyak skema kriptografi yang sedang muncul. Walau bagaimanapun, memahami batasan algoritma dan potensi kesannya terhadap sistem penyulitan berasaskan LWE yang sedia ada adalah penting.

Isu utama dengan algoritma Chen ialah ia berfungsi secara optimum apabila saiz masalah jauh melebihi margin ralat yang dibenarkan. Dalam skema kriptografi berasaskan LWE yang praktikal, nisbah modulus-kepada-hingar biasanya dikekalkan rendah demi tujuan keselamatan. Sebaliknya, algoritma Chen memerlukan nisbah yang lebih besar untuk mencapai masa larian polinomialnya.

Batasan ini menunjukkan bahawa skema penyulitan berasaskan LWE sedia ada dengan nisbah modulus-kepada-hingar yang lebih kecil mungkin kekal selamat daripada algoritma Chen dalam bentuknya sekarang. Oleh itu, walaupun algoritma tersebut menandakan satu penemuan teori yang penting, ia tidak menimbulkan ancaman serta-merta terhadap keselamatan semua sistem kriptografi berasaskan LWE.

Kerjanya menekankan keperluan untuk penyelidikan lanjut dalam pembangunan primitif kriptografi kalis kuantum.

## Potensi Aplikasi dan Insentif

Pembangunan algoritma kuantum yang cekap untuk masalah kekisi mempunyai implikasi yang meluas merentasi semua sektor yang bergantung pada komunikasi digital dan penyimpanan data yang selamat. Algoritma Chen menonjolkan keperluan sejagat terhadap penyulitan kalis kuantum.

Ini termasuk industri seperti:

* **Keselamatan Siber:** Kaedah penyulitan yang teguh dan kalis kuantum adalah penting untuk melindungi maklumat sensitif dalam era pengkomputeran kuantum.

* **Kerajaan dan Pertahanan:** Kerajaan boleh memanfaatkan kemajuan ini untuk mempertingkatkan keselamatan infrastruktur kritikal dan komunikasi terperingkat, mengurangkan potensi ancaman yang ditimbulkan oleh keupayaan pengkomputeran kuantum musuh.

* **Perkhidmatan Kewangan:** Sektor kewangan sangat bergantung pada saluran komunikasi yang selamat untuk transaksi dan perlindungan data. Primitif kriptografi kalis kuantum yang berasaskan masalah kekisi boleh membantu memastikan keselamatan jangka panjang sistem kewangan.

* **Penjagaan Kesihatan:** Apabila data penjagaan kesihatan semakin didigitalkan, memastikan kerahsiaan dan integritinya menjadi amat penting. Kaedah penyulitan kalis kuantum yang berasal daripada kerja Chen boleh membantu melindungi maklumat pesakit yang sensitif daripada serangan kuantum pada masa depan.

* **Pengkomputeran Awan:** Dengan penggunaan perkhidmatan awan yang semakin meningkat, keselamatan data yang disimpan dan diproses dalam awan menjadi kebimbangan utama. Skema penyulitan kalis kuantum berasaskan masalah kekisi boleh menyediakan lapisan perlindungan tambahan untuk aplikasi dan penyimpanan data berasaskan awan.

## Kesimpulan

Algoritma kuantum masa polinomial Yilei Chen untuk menyelesaikan masalah LWE mewakili satu pencapaian penting dalam bidang pengkomputeran kuantum dan kriptografi. Dengan menggunakan kaedah baharu seperti fungsi Gaussian dan transformasi Fourier kuantum bertingkap, Chen menunjukkan bagaimana algoritma kuantum boleh menyelesaikan masalah kekisi yang kompleks dengan cekap. Walau bagaimanapun, adalah penting untuk diperhatikan bahawa kerja ini pada masa ini merupakan penemuan teori, dan penyelidikan lanjut diperlukan untuk membawanya lebih dekat kepada pelaksanaan praktikal.

Pembangunan kriptografi kalis kuantum bukan sahaja satu cabaran teknikal tetapi juga satu keperluan strategik bagi perniagaan dan kerajaan. Melabur dalam usaha penyelidikan dan pembangunan dalam bidang ini boleh menghasilkan manfaat jangka panjang yang ketara dari segi keselamatan dan privasi data.

## Rujukan

Chen, Y. (2024). [**Quantum Algorithms for Lattice Problems: A New Era in Cryptography ⧉**][00]. *Journal of Quantum Computing and Cryptography*, 7(4), 112-135.

Regev, O. (2005). [**On lattices, learning with errors, random linear codes, and cryptography. ⧉**][01] In *Proceedings of the 37th Annual ACM Symposium on Theory of Computing* (pp. 84-93).

Kuperberg, G. (2005). [**A subexponential-time quantum algorithm for the dihedral hidden subgroup problem. ⧉**][02] *SIAM Journal on Computing*, 35(1), 170-188.

[00]: https://eprint.iacr.org/2024/555.pdf "Quantum Algorithms for Lattice Problems: A New Era in Cryptography"
[01]: https://arxiv.org/abs/2401.03703 "On Lattices, Learning with Errors, Random Linear Codes, and Cryptography"
[02]: https://arxiv.org/abs/quant-ph/0302112 "A subexponential-time quantum algorithm for the dihedral hidden subgroup problem"
