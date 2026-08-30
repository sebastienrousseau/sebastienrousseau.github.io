---
title: "Infrastruktur Pembayaran Pasca-Kuantum: Mengapa Bank Mungkin Mengganti dan Bukan Memasang Semula Landasan Lama"
tags: "post-quantum cryptography, crypto-agility, HNDL, ML-KEM, ML-DSA, NIST, payment infrastructure, ISO 20022, SWIFT, HSM, PKI, operational resilience, DORA, quantum computing, AI"
subtitle: "ML-KEM dan ML-DSA tidak muat dengan kemas di dalam landasan yang membawa SWIFT MT dan ISO 20022. Jawapan kejuruteraan yang jujur ialah pemasangan semula merupakan rancangan migrasi terkawal dengan jangka hayat pendek, dan penggantian ialah satu-satunya destinasi yang stabil."
description: "Kriptografi pasca-kuantum memaksa satu pilihan binari ke atas landasan pembayaran: memasang semula RSA/ECC di dalam sampul SWIFT MT dan ISO 20022 yang tidak pernah disaiz untuk ML-KEM dan ML-DSA, atau menggantinya dengan infrastruktur tangkas-kripto. Arkitek mesti membuat keputusan sebelum HNDL menjadi kerugian operasi."
date: "May 31, 2026"
language: "ms"
locale: "ms_MY"
banner: "https://cloudcdn.pro/stocks/images/lan-pham-4qG2qqXi3tY.webp"
banner_alt: "Bahan kunci kriptografi hanyut ke dalam air biru gelap - melambangkan penangkapan harvest-now-decrypt-later terhadap mesej pembayaran yang sampul RSA dan ECC-nya tidak akan bertahan menghadapi komputer kuantum yang relevan secara kriptanalitik"
keywords: "kriptografi pasca-kuantum, pembayaran PQC, ketangkasan kripto, Harvest Now Decrypt Later, HNDL, piawaian pasca-kuantum NIST, ML-KEM, ML-DSA, FIPS 203, FIPS 204, migrasi landasan pembayaran, ISO 20022 PQC, penggantian SWIFT MT, HSM, keruntuhan PKI, daya tahan operasi, Akta Kesediaan Keselamatan Siber Pengkomputeran Kuantum"
---

## Infrastruktur Pembayaran Pasca-Kuantum: Mengapa Bank Mungkin Mengganti dan Bukan Memasang Semula Landasan Lama

Primitif kriptografi yang mengesahkan setiap pembayaran borong dalam pengeluaran hari ini — RSA, ECDSA, ECDH — mempunyai tarikh luput. [Akta Kesediaan Keselamatan Siber Pengkomputeran Kuantum ⧉](https://www.congress.gov/bill/117th-congress/house-bill/7535/text "H.R. 7535") Amerika Syarikat menulis tarikh luput itu ke dalam undang-undang perolehan persekutuan pada penghujung 2022. [Kertas Kerja BIS No. 1208 ⧉](https://www.bis.org/publ/work1208.htm "Project Leap: Quantum-proofing the financial system") meletakkan tarikh luput yang sama ke dalam rangka penyeliaan bagi bank pusat. [NIST FIPS 203 ⧉](https://csrc.nist.gov/pubs/fips/203/final "Module-Lattice-Based Key-Encapsulation Mechanism Standard") dan [FIPS 204 ⧉](https://csrc.nist.gov/pubs/fips/204/final "Module-Lattice-Based Digital Signature Standard") menerbitkan penggantinya pada Ogos 2024.

Infrastruktur pembayaran masih belum menyerap apa maksud semua itu.

Artikel ini ialah kes kejuruteraan untuk penggantian berbanding pemasangan semula. Ia ditulis untuk arkitek yang sudah memahami algoritma dan perlu memutuskan apa yang hendak dibuat dengan SWIFT MT, mesej pacs dan pain [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html), antara muka RTGS, estet HSM, dan hierarki sijil yang mendasari kesemuanya.

---

> **Ringkasan Eksekutif / Intipati Utama**
>
> - **Harvest-now-decrypt-later (HNDL) ialah ancaman operasi.** Musuh merakam trafik pembayaran tersulit pada 2026 untuk menyahsulitnya sebaik sahaja sebuah komputer kuantum yang relevan secara kriptanalitik (CRQC) wujud. Trafik yang ditangkap termasuk arahan penyelesaian, data benefisiari, dan bahan pengesahan dengan kepekaan yang berpanjangan.
> - **NIST telah memiawaikan penggantinya.** ML-KEM (FIPS 203) untuk enkapsulasi kunci dan ML-DSA (FIPS 204) untuk tandatangan digital ialah pilihan lalai. SLH-DSA (FIPS 205) merangkumi sandaran berasaskan cincang tanpa keadaan.
> - **Perbezaan saiz merosakkan andaian lama.** Kunci awam dan tandatangan adalah 5–20× lebih besar daripada setara RSA-2048. Ini berlanggar dengan MTU pada rangkaian pembayaran, andaian penimbal tetap dalam pengendali mesej MT, dan daya pemprosesan kriptografi armada HSM yang telah dipasang.
> - **Hibrid (klasik + PQC) ialah wahana migrasi, bukan destinasi.** TLS hibrid dan X.509 hibrid membeli dua hingga tiga tahun kesalingoperasian sementara landasan pengeluaran diganti. Ia tidak menyelesaikan masalah kapasiti yang mendasarinya.
> - **PKI ialah dinding penampung beban.** Sebuah pihak berkuasa sijil yang algoritma tandatangannya menjadi boleh dipalsukan membatalkan setiap sijil di bawahnya. Pendedahan institusi bank ialah rantai itu, bukan mana-mana titik akhir tunggal.
> - **Ketangkasan kripto ialah sifat seni bina yang perlu dijuruterakan.** Pengenal pasti algoritma, format kunci, sampul tandatangan, dan partisyen HSM mesti semuanya boleh diparameterkan. Apa sahaja yang dipaku kepada RSA pada masa kompilasi ialah hutang teknikal yang akan matang secara serentak.
>
---

## Harvest Now, Decrypt Later: Model Ancaman yang Menghapuskan Pilihan untuk Menunggu

HNDL menyongsangkan jadual masa kriptografi yang lazim. Penilaian risiko konvensional bertanya bilakah ancaman itu terwujud. HNDL bertanya bilakah data yang ditangkap hari ini menjadi berguna kepada musuh. Bagi mesej pembayaran — identiti benefisiari, nombor akaun, data kiriman wang berstruktur, muatan penyaringan sekatan, arahan penyelesaian antara bank — jendela kepekaan ialah bertahun hingga berdekad. Kebanyakan trafik itu sedang dirakam di suatu tempat sekarang juga.

[Jadual masa CNSA 2.0 NSA ⧉](https://media.defense.gov/2022/Sep/07/2003071834/-1/-1/0/CSA_CNSA_2.0_ALGORITHMS_.PDF "Commercial National Security Algorithm Suite 2.0") memberi sistem keselamatan negara sehingga 2035 untuk menyempurnakan peralihan. Penyelia kewangan bergerak mengikut jadual yang lebih pantas — [jangkaan PRA terhadap daya tahan operasi ⧉](https://www.bankofengland.co.uk/prudential-regulation/publication/2021/march/operational-resilience-impact-tolerances-for-important-business-services-ss "PRA SS1/21") menganggap ketangkasan kriptografi sebagai risiko penumpuan pihak ketiga. Jangkaan pada 2026 ialah landasan pembayaran yang penting menerbitkan pelan migrasi PQC mereka dalam pengesahan sendiri daya tahan mereka.

Musuh HNDL tidak memerlukan CRQC hari ini. Musuh memerlukan:

1. **Kedudukan rangkaian.** Cetusan kabel dasar laut, tangkapan pada peringkat ISP, dan kotak tengah yang terjejas semuanya dalam skop. Trafik pembayaran borong tertumpu melalui sebilangan kecil laluan rangkaian.
2. **Storan.** Satu petabait data pembayaran berstruktur ialah arkib yang boleh diurus pada 2026.
3. **Kesabaran.** Tangkapan itu tidak berkos apa-apa bagi setiap mesej yang dipintas. Hasilnya tiba kemudian.

Oleh itu, hujah migrasi bukanlah "komputer kuantum mungkin tiba pada 2035." Ia ialah "sebarang sesi TLS yang selesai malam ini dengan pertukaran kunci RSA-2048 terdedah selama mana data di dalamnya kekal sensitif."

## Masalah Saiz Ialah Masalah Kejuruteraan

Perbincangan awam mengenai migrasi PQC cenderung memfokuskan pemilihan algoritma. Masalah yang lebih sukar ialah masalah dimensi.

| Primitif | Kunci awam | Tandatangan / teks sifer |
|---|---|---|
| RSA-2048 | 256 bait | 256 bait (tandatangan) |
| ECDSA P-256 | 64 bait | 64 bait (tandatangan) |
| ML-KEM-768 | **1,184 bait** | **1,088 bait (teks sifer)** |
| ML-DSA-65 | **1,952 bait** | **3,309 bait (tandatangan)** |
| SLH-DSA-128f | 32 bait | **17,088 bait (tandatangan)** |

Angka-angka itu memetakan secara langsung kepada mod kegagalan yang tidak pernah direka untuk ditangani oleh infrastruktur pembayaran lama:

- **Pemecahan paket pada laluan.** Sebuah ClientHello yang membawa ML-KEM-768 hibrid ditambah X25519 klasik melebihi MTU Ethernet 1,500-bait yang lazim. Kotak tengah antara dua titik akhir pembayaran memecah, menggugurkan, atau menulis semula jabat tangan itu. Kegagalan itu muncul sebagai ralat TLS berselang-seli yang kelihatan seperti hingar rangkaian sementara.
- **Andaian penimbal dalam pengendali MT.** Banyak integrasi SWIFT MT membawa sampul bertandatangan yang disaiz untuk ECDSA. Masukkan tandatangan ML-DSA ke dalam sampul yang sama dan penghurai sama ada memangkas atau menolak.
- **Daya pemprosesan HSM.** Penandatanganan ML-DSA pada armada HSM yang dipasang adalah 3–10× lebih lambat daripada ECDSA bagi setiap operasi, pada perkakasan yang belanjawan kunci-per-saatnya sudah pun berjalan panas semasa tetingkap kelompok penghujung hari.
- **Berat rantai sijil.** Hierarki CA empat peringkat yang dikeluarkan semula dengan tandatangan ML-DSA membesar daripada kira-kira 6 KB kepada kira-kira 60 KB. Setiap jabat tangan TLS ke landasan itu membayar kos tersebut.

Laluan pemasangan semula ialah untuk mengelas kekangan ini satu demi satu — penimbal lebih besar di sini, HSM lebih pantas di sana, toleransi pemecahan pada kotak tengah. Itu ialah jambatan enam bulan yang boleh dipertahankan. Ia bukan seni bina.

## Pasang Semula Berbanding Ganti: Keputusan yang Mentakrifkan Program

Rangka kerja yang jujur ialah pemasangan semula merupakan rancangan migrasi terkawal dengan jangka hayat pendek, dan penggantian ialah satu-satunya destinasi yang stabil. Keputusannya ialah yang mana satu dibiayai oleh bank terlebih dahulu, dan berapa lama jendela pemasangan semula kekal terbuka sebelum ia menjadi tampalan kekal.

Pemasangan semula bermaksud:

- TLS hibrid (ML-KEM + X25519) ditamatkan pada sempadan landasan sedia ada.
- Sijil bertandatangan dua (RSA utama, ML-DSA sekunder) dikeluarkan daripada CA subordinat yang berkeupayaan PQC.
- Penimbal MT lebih besar dan dasar MTU yang lebih ketat pada VPN pembayaran.
- Kemas kini perisian tegar HSM di mana vendor menyokong primitif PQC; penggantian penuh HSM di mana mereka tidak.

Kerja itu boleh dilakukan. Ia tidak membetulkan masalah yang mendasari, iaitu SWIFT MT dan banyak pelaksanaan ISO 20022 mengekod sampul kriptografi di dalam format mesej yang memaku algoritma. Peralihan algoritma seterusnya — dan ia akan berlaku, apabila ML-KEM akhirnya menunjukkan kelemahan atau piawaian baharu menggantinya — menjalankan migrasi yang sama sekali lagi pada landasan yang sama.

Penggantian bermaksud menerima bahawa lapisan kriptografi bukanlah sifat format mesej. Ia adalah sifat sebuah perkhidmatan sampul yang boleh diasingkan yang dipanggil oleh format mesej. Secara konkrit:

- Sempadan keselamatan pengangkutan berpindah ke jejaring perkhidmatan atau sidecar yang menamatkan TLS hibrid dan mempersembahkan mesej teks jelas kepada landasan dengan antara muka yang stabil.
- Tandatangan peringkat mesej dihasilkan oleh perkhidmatan penandatanganan khusus yang pilihan algoritmanya ialah parameter konfigurasi, bukan andaian berkod tegar.
- Sijil dikeluarkan daripada sebuah CA yang algoritma penandatanganannya sendiri boleh diputarkan.
- Partisyen HSM dialamatkan mengikut tujuan (pengangkutan, penandatanganan, enkapsulasi kunci) dan bukan mengikut format mesej.

Reka bentuk penggantian bertahan menghadapi perubahan algoritma seterusnya tanpa menyentuh semula landasan.

## Seni Bina Tangkas-Kripto, Lapisan demi Lapisan

Lapisan infrastruktur yang penting bagi migrasi PQC bukanlah lapisan perniagaan "data, kawalan, ekonomi" yang sesuai dengan naratif perbankan generik. Lapisan yang penting ialah lapisan kriptografi.

| Lapisan | Apa yang dilakukannya | Persoalan PQC | Arahan seni bina |
|---|---|---|---|
| **Pengurusan HSM / kunci** | Menjana, menyimpan, dan mengoperasi bahan kunci di bawah pengasingan perkakasan | Adakah perisian tegar HSM yang dipasang menyokong ML-KEM, ML-DSA, dan API enkapsulasi kunci hibrid? Apakah perbezaan daya pemprosesan penandatanganan berbanding ECDSA pada perkakasan yang sama? | Inventori setiap partisyen HSM mengikut sokongan algoritma dan kapasiti per-saat. Nyahtauliahkan apa sahaja yang dipaku kepada RSA tanpa laluan perisian tegar. Dirikan partisyen PQC khusus sebelum peralihan pengeluaran. |
| **PKI / pihak berkuasa sijil** | Mengeluarkan, membatalkan, dan merantaikan kepercayaan melalui sijil X.509 | Bolehkah CA menandatangani dengan ML-DSA hari ini? Adakah terdapat proses teruji untuk memutarkan akar dan mengeluarkan semula rantai? Adakah penjawab CRL dan OCSP disaiz untuk berat tandatangan ML-DSA? | Anggap timbunan CA sebagai dinding penampung beban. Wujudkan subordinat berkeupayaan PQC sekarang. Tetapkan masa putaran akar untuk kebergantungan sijil yang paling lama hayatnya, bukan untuk kemudahan. |
| **Pengangkutan / rangkaian** | Menamatkan TLS, IPsec, dan MACsec antara titik akhir pembayaran | Adakah pengimbang beban, WAF, dan laluan kotak tengah bertoleransi dengan jabat tangan hibrid yang melebihi MTU lama? Adakah tiket penyambungan-semula sesi disaiz untuk kunci PQC? | Pindahkan penamatan TLS ke sempadan tangkas-kripto (sidecar atau jejaring). Naikkan dasar MTU pada VPN pembayaran. Uji keseluruhan laluan dengan pemecahan diaruh secara sengaja. |
| **Aplikasi / muatan mesej** | Membawa mesej SWIFT MT, ISO 20022 pacs / pain / camt dan sampul kriptografinya | Adakah pengendali mesej landasan bertoleransi dengan sampul bertandatangan bersaiz ML-DSA? Adakah penghurai perantaraan sedar-algoritma atau adakah ia memangkas apabila panjang? | Asingkan sampul daripada muatan. Tandatangani pada sempadan perkhidmatan, bukan di dalam pengendali format mesej. Anggap pengenal pasti algoritma sebagai data, bukan sebagai skema. |
| **Audit / bukti** | Menghasilkan rantai jagaan kriptografi yang menjadi sandaran penyelia dan pelanggan | Adakah rekod bertandatangan bersejarah masih boleh disahkan sebaik sahaja algoritma penandatanganan dinyahtaraf? Adakah terdapat pelan tandatangan arkib jangka panjang? | Tandatangan-balas arkib dengan primitif berasaskan cincang (SLH-DSA) untuk jaminan yang bertahan menghadapi sebarang pemecahan algoritma tunggal. Anggap rantai audit sebagai artefak yang dikawal selia, bukan sebagai hasil sampingan binaan. |

Disiplinnya ialah menjadikan setiap pilihan algoritma sebagai nilai konfigurasi pada setiap lapisan. Institusi yang mengekod tegar RSA-2048 pada mana-mana lapisan itu mewarisi satu peristiwa akhir-hayat yang diselaraskan apabila algoritma tersebut jatuh.

## Apa Maksudnya Mengikut Jenis Bank

Profil pendedahan berbeza mengikut institusi. Arahannya berbeza dengan sewajarnya.

### Bank Global

Bank global mengendalikan armada HSM yang dipasang terbesar, rantai sijil terpanjang, dan laluan rangkaian paling kompleks antara pihak lawan. Risiko dominan bukanlah pemilihan algoritma — ia adalah kos penyelarasan untuk menukar algoritma merentasi ratusan perkhidmatan dalaman dan berpuluh pihak lawan luaran secara serentak.

Arahannya ialah membiayai CA berkeupayaan PQC, sempadan pengangkutan tangkas-kripto, dan perkhidmatan penandatanganan berparameter-algoritma sebagai kerja 2026, sebelum mana-mana landasan tunggal dipasang semula. Pemasangan semula kemudian menjadi perubahan pengeluaran rutin di dalam rangka kerja yang diketahui. Tanpa rangka kerja itu, setiap pemasangan semula landasan membangkitkan semula keputusan seni bina yang sama.

### Bank Serantau

Bank serantau mempunyai kawasan permukaan algoritma yang lebih kecil tetapi kakitangan pakar yang lebih sedikit secara berkadaran. Risiko dominan ialah terkurung-vendor HSM kepada algoritma yang vendor belum berjanji untuk menyokong.

Arahannya ialah menulis sokongan PQC — khususnya ML-KEM dan ML-DSA, dengan laluan naik taraf perisian tegar yang teruji — ke dalam setiap pembaharuan kontrak HSM dari 2026 dan seterusnya. Bank tanpa klausa itu mewarisi penggantian perkakasan yang terpaksa mengikut jadual vendor, bukan jadual mereka sendiri.

### Fintek dan PSP

Penyedia perkhidmatan pembayaran dan fintek lazimnya berada di antara pihak lawan bank dan sistem peniaga atau pengguna akhir. Pendedahan kriptografi mereka ialah sempadan API pada kedua-dua belah.

Arahannya ialah menerbitkan antara muka TLS hibrid — klasik ditambah ML-KEM — pada bahagian yang menghadap bank sebagai syarat asas dalam perbualan komersial 2026. Fintek yang tiba dengan kesalingoperasian PQC yang telah pun ditunjukkan memenangi kitaran integrasi berbanding fintek yang belum bermula.

### Bendahari Korporat

Bendahari tidak mengendalikan infrastruktur kriptografi secara langsung. Mereka menggunakannya — setiap API bank, setiap pemindahan fail selamat, setiap pengesahan bertandatangan bergantung pada PKI bank.

Arahannya ialah menambah tiga soalan ke dalam setiap RFP bank pada 2026: algoritma PQC yang manakah digunakan oleh bank hari ini dalam TLS yang menghadap pelanggan, apakah pelan bank untuk pengesahan pembayaran bertandatangan ML-DSA, dan bagaimanakah bank bercadang untuk memelihara kebolehsahihan rekod bertandatangan bersejarah sebaik sahaja RSA dinyahtaraf. Bank yang tidak dapat menjawab soalan tersebut memberi isyarat sesuatu tentang kesediaan kejuruteraan asas mereka.

## Apa yang Berlaku Seterusnya

Gelombang pertama penggunaan PQC dalam pembayaran akan menjadi tidak kelihatan kepada pengguna akhir. TLS hibrid muncul dalam jabat tangan, rantai sijil membesar, kependaman penandatanganan HSM merangkak naik beberapa milisaat, dan landasan terus beroperasi. Itulah laluan kejayaan.

Kegagalan yang kelihatan akan didorong oleh pemasangan semula: landasan yang tidak dapat menerima sampul bertandatangan ML-DSA tanpa pemangkasan, sebuah CA yang titik pengedaran CRL-nya tercekik dengan berat tandatangan baharu, kotak tengah yang memecahkan jabat tangan hibrid menjadi ClientHello yang tersusun semula. Kegagalan tersebut akan mendarat dalam pengeluaran sepanjang 2027.

Keputusan seni bina pada 2026 ialah sama ada hendak membiayai infrastruktur penggantian yang menjadikan pemasangan semula tidak relevan, atau membiayai satu siri pembetulan khusus-landasan yang setiap satunya kelihatan lebih murah secara individu dan berkumpul menjadi migrasi yang lebih panjang serta lebih mahal. Bank yang memilih laluan pertama akan menjalankan operasi yang lebih tenang sepanjang peralihan. Bank yang memilih laluan kedua akan menghabiskan baki dekad ini menjelaskan kajian semula insiden kepada penyelia.

PQC bukan masalah kriptografi yang menyamar sebagai masalah infrastruktur. Ia ialah masalah infrastruktur yang kebetulan dimulakan oleh kriptografi.

## Soalan Lazim

**Adakah terdapat tarikh akhir yang memaksa kerja ini?**

Tarikh akhir kawal selia yang keras adalah mengikut bidang kuasa. [Akta Kesediaan Keselamatan Siber Pengkomputeran Kuantum ⧉](https://www.congress.gov/bill/117th-congress/house-bill/7535/text "H.R. 7535") Amerika Syarikat mengikat sistem persekutuan. [Jadual masa CNSA 2.0 NSA ⧉](https://media.defense.gov/2022/Sep/07/2003071834/-1/-1/0/CSA_CNSA_2.0_ALGORITHMS_.PDF "CNSA 2.0") mensasarkan 2035 untuk sistem keselamatan negara. Penerbitan [BIS Project Leap ⧉](https://www.bis.org/publ/work1208.htm "BIS Working Paper 1208") dan program kerja FSB sedang menarik ufuk itu ke hadapan bagi infrastruktur pembayaran sistemik. HNDL bermaksud jam operasi mula berjalan jauh sebelum mana-mana tarikh nominal tersebut.

**Mengapa ML-KEM ialah enkapsulasi kunci yang disyorkan dan bukan sesuatu yang lebih pantas?**

ML-KEM (versi piawai [CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html)) mempunyai gabungan terkuat antara saiz teks sifer dan kunci yang kecil dalam kalangan calon lattis, dengan pelaksanaan matang dan pengukuhan saluran-sisi. NIST menerbitkannya sebagai [FIPS 203 ⧉](https://csrc.nist.gov/pubs/fips/203/final "FIPS 203"). Calon yang lebih pantas wujud tetapi membawa saiz lebih besar atau selang keyakinan yang lebih lemah pada parameter keselamatan.

**Mengapa tidak gunakan SLH-DSA di mana-mana sahaja dan bukan ML-DSA?**

SLH-DSA (versi piawai SPHINCS+) berasaskan cincang dan oleh itu bergantung hanya pada keselamatan fungsi cincang, iaitu andaian paling konservatif yang ada. Tandatangannya adalah 5–20× lebih besar daripada ML-DSA. Itu boleh diterima untuk tandatangan-balas arkib, tetapi tidak boleh dilaksanakan untuk penandatanganan transaksi di mana saiz penting bagi setiap mesej. Corak piawai ialah ML-DSA untuk penandatanganan pengeluaran dan SLH-DSA untuk jaminan arkib.

**Bolehkah bank hanya menunggu sehingga landasan menerbitkan profil PQC?**

Bank yang menunggu mewarisi jendela migrasi yang diterbitkan oleh landasan, yang lebih pendek daripada kitaran perubahan dalaman bank itu sendiri. Menjelang masa SWIFT, pengendali RTGS tempatan, dan CCP yang berkaitan masing-masing menerbitkan profil PQC mereka, jendela migrasi akan menjadi dua belas hingga dua puluh empat bulan. Bank yang belum pra-membina keupayaan CA, pengangkutan, dan HSM mereka tidak akan memenuhinya tanpa jalan pintas operasi.

**Apakah satu perkara berdaya-ungkit tertinggi yang perlu dibiayai terlebih dahulu?**

Sebuah pihak berkuasa sijil subordinat berkeupayaan PQC, yang disepadukan ke dalam PKI sedia ada, yang boleh mengeluarkan sijil dua-algoritma (RSA ditambah ML-DSA) tanpa mengganggu kepercayaan pengeluaran. Itu mewujudkan primitif putaran. Segala yang lain — naik taraf pengangkutan, perancangan partisyen HSM, perubahan sampul-mesej — boleh dijadualkan di sekelilingnya.

## Rujukan

- Congress.gov, (2022). [H.R. 7535 — Quantum Computing Cybersecurity Preparedness Act ⧉](https://www.congress.gov/bill/117th-congress/house-bill/7535/text "Quantum Computing Cybersecurity Preparedness Act").
- NIST, (2024). [FIPS 203 — Module-Lattice-Based Key-Encapsulation Mechanism Standard ⧉](https://csrc.nist.gov/pubs/fips/203/final "FIPS 203").
- NIST, (2024). [FIPS 204 — Module-Lattice-Based Digital Signature Standard ⧉](https://csrc.nist.gov/pubs/fips/204/final "FIPS 204").
- NIST, (2024). [FIPS 205 — Stateless Hash-Based Digital Signature Standard ⧉](https://csrc.nist.gov/pubs/fips/205/final "FIPS 205").
- NSA, (2022). [Commercial National Security Algorithm Suite 2.0 ⧉](https://media.defense.gov/2022/Sep/07/2003071834/-1/-1/0/CSA_CNSA_2.0_ALGORITHMS_.PDF "CNSA 2.0").
- BIS, (2024). [Working Paper No. 1208 — Project Leap: Quantum-proofing the financial system ⧉](https://www.bis.org/publ/work1208.htm "BIS Working Paper 1208").
- Bank of England (PRA), (2024). [SS1/21 — Operational resilience: Impact tolerances for important business services ⧉](https://www.bankofengland.co.uk/prudential-regulation/publication/2021/march/operational-resilience-impact-tolerances-for-important-business-services-ss "PRA SS1/21").
