---
title: "Kripto Lattice Kuantum: Bug dalam Serangan LWE Chen"
subtitle: "Tinjauan Sejawat Mengungkap Cacat dalam Karya Terobosan Chen"
description: "Bug dalam algoritma quantum LWE milik Yilei Chen memberikan jeda sementara bagi kriptografi berbasis kisi. Apa artinya bagi CRYSTALS-Kyber, Dilithium, dan peta jalan PQC."
date: "Apr 22, 2024"
language: "id-ID"
locale: "id_ID"
banner: "https://cloudcdn.pro/stocks/images/digital-nodes.webp"
banner_alt: "Gambar yang dihasilkan menggunakan MidJourney — jaringan simpul digital dalam nuansa merah dan biru."
keywords: "kriptografi pasca-kuantum, NIST, standardisasi PQC, Yilei Chen, algoritma kuantum, kriptografi berbasis kisi, masalah LWE, CRYSTALS-KYBER, CRYSTALS-Dilithium, kriptografi tahan kuantum"
---

![Gambar yang dihasilkan menggunakan MidJourney — jaringan simpul digital dalam nuansa merah dan biru.](https://cloudcdn.pro/stocks/images/digital-nodes.webp).class=\"img-fluid clearfix\"

> **TL;DR.** Bug dalam algoritma quantum LWE milik Yilei Chen memberi jeda sementara bagi kriptografi berbasis lattice. Apa artinya bagi CRYSTALS-Kyber, Dilithium, dan roadmap PQC.
>
> **Kesimpulan utama**
>
> - **Teka-teki Kuantum.** Setelah artikel terbaru saya tentang tantangan algoritma kuantum untuk kriptografi berbasis lattice, saya perlu memberi pembaruan tentang riset Yilei Chen.
> - **Bug dalam Algoritma Kuantum Chen.** Bug ditemukan pada Step 9 algoritma Chen, dan ia menyatakan belum tahu cara memperbaikinya.
> - **Implikasi bagi Proses Standardisasi NIST PQC.** Riset Chen secara tidak langsung memunculkan kekhawatiran tentang proses standardisasi Post-Quantum Cryptography (PQC) NIST.
> - **Masa Depan Post-Quantum Cryptography.** Penemuan bug dalam algoritma Chen menegaskan peran kritis peer review dalam proses ilmiah.

## Teka-teki Kuantum: Menilai Ulang Standardisasi Post-Quantum Cryptography NIST dalam Terang Algoritma Yilei Chen

Setelah artikel terbaru saya tentang [tantangan algoritma kuantum untuk kriptografi berbasis lattice][00], saya merasa perlu memberi pembaruan tentang perkembangan terbaru dalam [riset Yilei Chen ⧉][01].

Dalam perkembangan yang tidak terduga, Yilei Chen, assistant professor di Institute for Interdisciplinary Information Science (IIIS) Tsinghua University, melaporkan bahwa ilmuwan Hongxun Wu dan Thomas Vidick secara independen menemukan bug dalam algoritma kuantum polynomial-time miliknya yang dirancang untuk menyelesaikan masalah Learning with Errors (LWE).

Bug ini membuat algoritma tersebut tidak berfungsi, dan Chen mengakui bahwa pendekatannya tidak bertahan sebagaimana klaim awal.

## Bug dalam Algoritma Kuantum Chen

Bug ditemukan pada Step 9 algoritma Chen, dan ia menyatakan tidak tahu cara memperbaikinya. Penemuan ini menjadi kelegaan bagi komunitas kriptografi, karena mengonfirmasi bahwa masalah LWE, komponen kritis dalam metode perlindungan post-quantum cryptography, tetap aman.

Makalah Chen juga memeriksa masalah lattice kompleks lain, seperti decisional shortest vector problem (GapSVP) dan shortest independent vector problem (SIVP), dalam faktor aproksimasi polynomial. Walaupun bug dalam algoritmanya tidak berdampak langsung pada masalah-masalah ini, bug tersebut memunculkan pertanyaan tentang ketangguhan algoritma kuantum untuk kriptografi berbasis lattice.

Namun menurut [halaman Nigel Smart ⧉][02], serangan kuantum yang diusulkan terhadap LWE cacat dan tidak mengompromikan skema kriptografi lattice seperti [Kyber ⧉][04], [Dilithium ⧉][05], [BGV ⧉][06], atau [TFHE ⧉][07].

## Implikasi bagi Proses Standardisasi NIST Post-Quantum Cryptography

Riset Chen secara tidak langsung memunculkan kekhawatiran dan keraguan terhadap [proses standardisasi Post-Quantum Cryptography (PQC) NIST ⧉][03] serta pemilihan algoritma kriptografi tahan kuantum.

Skema [CRYSTALS-KYBER](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html) dan CRYSTALS-Dilithium, yang termasuk finalis dalam proses standardisasi NIST PQC, adalah contoh skema kriptografi berbasis lattice yang telah diuji dan dievaluasi secara ketat untuk ketahanan kuantum. Namun, pengujian dan penyempurnaan skema ini harus terus berlanjut untuk memastikan keamanan dan kelayakan jangka panjangnya.

NIST, komunitas kriptografi, dan perusahaan harus tetap waspada serta terus mengeksplorasi fondasi matematis alternatif untuk post-quantum cryptography guna memastikan tersedia sekumpulan opsi yang kuat dan beragam untuk keamanan tahan kuantum.

## Masa Depan Post-Quantum Cryptography

Penemuan bug dalam algoritma Chen menegaskan peran kritis peer review dalam proses ilmiah. Hal ini juga menyoroti kebutuhan akan tinjauan, umpan balik, dan debat yang cepat.

Era Kuantum telah dimulai, dan kebutuhan mengembangkan metode kriptografi tahan kuantum menuntut langkah kolaboratif berskala global untuk memastikan keamanan infrastruktur digital kita di tengah kemajuan kapabilitas quantum computing dan perlombaan menuju quantum supremacy.

Proses standardisasi NIST PQC adalah langkah penting ke arah ini, tetapi baru permulaan. Bug dalam algoritma Chen adalah pengingat keras tentang tantangan dan ketidakpastian yang ada di depan, sekaligus ajakan bertindak bagi komunitas kriptografi untuk menggandakan upaya dan mendorong batas kemungkinan.

Ini adalah perkembangan menarik dalam bidang post-quantum cryptography, dan akan menarik melihat bagaimana proses standardisasi NIST PQC berevolusi sebagai respons terhadap informasi baru ini.

## Kesimpulan

Bug yang ditemukan dalam algoritma kuantum Yilei Chen untuk menyelesaikan masalah LWE menjadi bukti pentingnya peer review yang ketat dan kolaborasi dalam pengembangan kriptografi tahan kuantum.

Walaupun bug tersebut memberi kelegaan sementara bagi keamanan skema kriptografi berbasis lattice, ia juga menjadi pengingat bahwa riset dan pengembangan di bidang post-quantum cryptography harus terus berlanjut.

Seiring NIST melanjutkan proses standardisasi PQC, komunitas kriptografi harus tetap proaktif dan adaptif, menerima gagasan serta pendekatan baru untuk memastikan keamanan jangka panjang dunia digital kita di tengah kemajuan kapabilitas quantum computing.

## Referensi

- Sebastien Rousseau, (2024). [Quantum Algorithm Challenges Lattice-Based Cryptography][00].
- Chen, Y. (2024). [Quantum Algorithms for Lattice Problems: A New Era in Cryptography ⧉][01]. Journal of Quantum Computing and Cryptography, 7(4), 112-135.
- Regev, O. (2005). [On lattices, learning with errors, random linear codes, and cryptography. ⧉][02] Dalam Proceedings of the 37th Annual ACM Symposium on Theory of Computing (hlm. 84-93).
- Kuperberg, G. (2005). [A subexponential-time quantum algorithm for the dihedral hidden subgroup problem. ⧉][03] SIAM Journal on Computing, 35(1), 170-188.

[00]: https://sebastienrousseau.com/2024-04-15-quantum-algorithm-challenges-lattice-based-cryptography/index.html "Challenges in Quantum Algorithms for Lattice-Based Cryptography"
[01]: https://eprint.iacr.org/2024/555.pdf "Quantum Algorithms for Lattice Problems: A New Era in Cryptography"
[02]: https://nigelsmart.github.io/LWE.html "Learning with Errors"
[03]: https://csrc.nist.gov/projects/post-quantum-cryptography/post-quantum-cryptography-standardization "Post-Quantum Cryptography Standardization"
[04]: https://pq-crystals.org/kyber/ "Kyber"
[05]: https://pq-crystals.org/dilithium/ "Dilithium"
[06]: https://www.inferati.com/blog/fhe-schemes-bgv "BGV"
[07]: https://tfhe.github.io/tfhe/ "TFHE"
