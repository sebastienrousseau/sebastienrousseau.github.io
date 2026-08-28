---
title: "Memperkenalkan Mata Wang Kripto Baharu dan Penyelesaian Pembayaran Lebih Pantas"
tags: "EXTC, ERC-223, Ethereum, smart contracts, cryptocurrency, blockchain, faster payments, decentralised finance, payment token, cross-border payments, ISO 20022, post-quantum cryptography, AI, tokenised deposits, stablecoins"
subtitle: "Mata wang kripto baharu dan penyelesaian pembayaran lebih pantas untuk kewangan generasi akan datang."
description: "Pada awal 2018, platform EXTC meneroka pembayaran rentas sempadan yang lebih pantas melalui kontrak pintar ERC-223 Ethereum - satu pelan awal bagi apa yang kelak dibina oleh kewangan terdesentralisasi."
date: "Feb 04, 2018"
language: "ms"
locale: "ms_MY"
banner: "https://cloudcdn.pro/stocks/images/laureen-missaire-DBbuhMbAIsQ.webp"
banner_alt: "Komputer riba yang dimatikan di atas meja kayu berwarna coklat"
keywords: "EXTC, ERC-223, kontrak pintar Ethereum, pembayaran lebih pantas, mata wang kripto, pembayaran blockchain, token pembayaran, kewangan terdesentralisasi, ERC-20, pembayaran rentas sempadan"
---

![Sebuah bangunan yang sangat tinggi dengan banyak lubang padanya](https://cloudcdn.pro/stocks/images/laureen-missaire-DBbuhMbAIsQ.webp).class=\"img-fluid clearfix\"

> **Ringkasan Eksekutif / Intipati Utama**
>
> - **Hipotesis teras.** Kontrak pintar Ethereum boleh menggantikan perlumbaan berganti-ganti perbankan koresponden untuk pembayaran rentas sempadan, menyelesaikan dalam saat dan bukannya hari serta menghapuskan lapisan yuran 3–7% ([World Bank, 2018](https://www.worldbank.org/en/topic/migrationremittancesdiasporaissues/brief/migration-remittances-data "World Bank Remittance Prices")).
> - **Sumbangan khusus ERC-223.** Piawaian ini membetulkan kelemahan kehilangan token secara senyap dalam ERC-20 dengan mewajibkan kontrak pintar mendedahkan fungsi `tokenFallback`, menyebabkan pemindahan yang gagal berbalik semula dan bukannya membakar token secara tidak boleh diundur ([Ethereum EIPs](https://eips.ethereum.org/EIPS/eip-20 "EIP-20: Token Standard")).
> - **Primitif pembayaran EXTC.** Reka bentuk token menyokong pemindahan atomik tunggal, arahan tetap dipicu masa, pembayaran korporat berbilang tandatangan, dan pinjaman mikro sokongan cagaran segera — semuanya tanpa institusi penjelasan.
> - **Apa yang didedahkan oleh eksperimen ini.** Reka bentuk teknikal adalah koheren, tetapi mainnet Ethereum pada 2018 memproses kira-kira 15 transaksi sesaat. Volum pembayaran pada skala besar memerlukan penyelesaian Layer-2 yang belum lagi siap untuk pengeluaran.
> - **Warisan.** Idea seni bina dalam EXTC — wang boleh atur cara, penyelesaian atomik, logik token terbenam pematuhan — muncul semula dalam protokol DeFi yang kemudian, reka bentuk CBDC, dan rangka kerja deposit token.

---

## Masalahnya: Pembayaran Rentas Sempadan pada 2018

Pembayaran antarabangsa pada awal 2018 lambat, mahal, dan legap secara reka bentuk. Pemindahan runcit dari United Kingdom ke Asia Tenggara biasanya melibatkan dua hingga empat bank koresponden, masing-masing mengenakan yuran dan menambah sehari kepada rantaian penyelesaian. Pangkalan data Remittance Prices Worldwide World Bank mencatatkan kos purata global sebanyak 6.9% bagi kiriman wang USD 200 pada suku pertama 2018.

Mata wang kripto telah membuktikan bahawa tunai digital rakan ke rakan adalah boleh dilaksanakan secara teknikal. Bitcoin menyelesaikan transaksi secara global dalam kira-kira sepuluh minit, dan lapisan boleh atur cara Ethereum menambah kontrak pintar — kod terlaksana sendiri yang boleh mengekod peraturan pembayaran terus ke dalam pemindahan itu sendiri. Jurang antara apa yang boleh dilakukan secara teknikal di atas rantai dan apa yang disampaikan oleh perbankan koresponden lama itulah ruang reka bentuk yang dimasuki EXTC.

## Asas Teknikal: ERC-20 dan Kelemahannya

Piawaian ERC-20, yang diformalkan dalam Ethereum Improvement Proposal 20, mentakrifkan antara muka kanonik untuk token boleh tukar ganti: `balanceOf`, `transfer`, `transferFrom`, `approve`, dan `allowance`. Menjelang awal 2018, ERC-20 merupakan piawaian token dominan, dengan ratusan token digunakan di mainnet.

Namun begitu, ERC-20 mempunyai masalah struktur. Apabila token dihantar terus ke alamat kontrak pintar menggunakan fungsi `transfer` piawai, kontrak itu tidak mempunyai cara untuk mengesan pemindahan masuk atau bertindak ke atasnya. Token yang dihantar dengan cara ini terperangkap secara kekal. Komuniti Ethereum menganggarkan bahawa berjuta-juta dolar dalam token ERC-20 telah hilang dengan cara ini menjelang pertengahan 2018.

ERC-223, yang dicadangkan oleh Dexaran pada penjejak isu GitHub Ethereum, menangani perkara ini dengan menambah keperluan fungsi `tokenFallback(address _from, uint _value, bytes _data)` pada kontrak penerima. Jika kontrak penerima tidak melaksanakan `tokenFallback`, pemindahan itu berbalik semula dan token dikembalikan kepada penghantar. Ini menjadikan pemindahan ERC-223 atomik: sama ada kontrak menerima token dan melaksanakan logiknya, atau transaksi gagal dengan bersih.

## Reka Bentuk Token EXTC

Token Express Transaction Credits direka bentuk berdasarkan lima ciri teras:

- **Nama, simbol, dan perpuluhan.** Medan identiti ERC-223 piawai, dengan 18 tempat perpuluhan untuk ketepatan bawah sen.
- **Jumlah bekalan.** Tetap pada masa penciptaan (mint), menjadikan EXTC aset deflasi kerana token yang hilang atau tidak dituntut tidak boleh diterbitkan semula.
- **Baki dan pemindahan.** Fungsi baca dan tulis piawai, dilanjutkan dengan keperluan `tokenFallback` ERC-223.
- **Sokongan berbilang tandatangan.** Pembayaran korporat memerlukan tandatangan bersama daripada berbilang alamat yang dibenarkan sebelum pelaksanaan, menyediakan jejak audit tanpa dewan penjelasan berpusat.
- **Pemindahan terkunci masa.** Satu primitif arahan tetap membolehkan EXTC menjadualkan pembayaran masa hadapan — satu keupayaan yang memerlukan pemindahan bank tradisional bergantung pada arahan luaran untuk dicapai.

## Primitif Pembayaran yang Disasarkan Platform

Seni bina EXTC direka bentuk untuk menggantikan empat aliran kerja pembayaran khusus yang dikendalikan secara tidak cekap oleh sistem lama:

**Pembayaran atomik tunggal** — pemindahan sekali sahaja yang diselesaikan dalam satu transaksi Ethereum, biasanya dalam masa 15–30 saat pada mainnet 2018.

**Arahan tetap berasaskan masa** — pemindahan berulang yang dikod sebagai panggilan kontrak pintar terkunci masa, menghapuskan keperluan bank untuk menerima dan melaksanakan semula arahan berkala.

**Pembayaran pukal korporat** — pembayaran berkelompok kepada berbilang penerima dalam satu transaksi, dengan setiap pemindahan individu memerlukan pengesahan berbilang tandatangan, mengurangkan kos dan risiko pihak lawan.

**Pinjaman segera sokongan cagaran** — peminjam mengunci token EXTC sebagai cagaran dalam kontrak pintar; kontrak melepaskan hasil pinjaman secara automatik apabila diterima, tanpa jawatankuasa kredit atau kelewatan pengunderaitan.

## Apa yang Didedahkan oleh Eksperimen Ini

Reka bentuk EXTC adalah koheren secara teknikal. Asas ERC-223 menyelesaikan kelemahan keselamatan yang paling ketara bagi piawaian token dominan, dan primitif pembayaran memetakan terus kepada aliran kerja sebenar yang dikendalikan secara tidak cekap oleh perbankan koresponden.

Kekangan praktikalnya ialah truput Ethereum. Pada suku pertama 2018, mainnet purata 15 transaksi sesaat dengan had gas kira-kira 8 juta setiap blok. Sebuah rangkaian pembayaran yang memproses walaupun sebahagian kecil daripada volum kiriman wang global — World Bank menganggarkan 270 juta migran menghantar wang pulang pada 2017 — akan menepukan mainnet dalam masa beberapa minit.

Penyelesaian penskalaan Layer-2, terutamanya saluran keadaan (state channels) dan versi awal apa yang kemudiannya menjadi teknologi rollup, sedang dalam penyelidikan aktif pada 2018 tetapi belum siap untuk pengeluaran. Lightning Network baru sahaja dilancarkan di mainnet Bitcoin pada Januari 2018 dengan kekangan yang ketara. Prasyarat teknikal untuk sebuah rangkaian pembayaran berasaskan blockchain beroperasi pada skala bank koresponden masih belum wujud.

## Idea yang Terus Bertahan

Beberapa konsep seni bina daripada EXTC dan projek token pembayaran sezaman telah disahkan oleh pembangunan seterusnya:

**Wang boleh atur cara** — mengekod peraturan pembayaran terus dalam logik pemindahan — menjadi ciri utama protokol pemberian pinjaman DeFi seperti Compound dan Aave, yang masing-masing dilancarkan pada 2018 dan 2020.

**Penyelesaian atomik tanpa dewan penjelasan** — sifat bahawa pemindahan sama ada berjaya sepenuhnya atau berbalik semula — kini menjadi keperluan reka bentuk dalam rangka kerja deposit token dan seni bina CBDC borong yang diteroka oleh bank pusat termasuk Bank of England dan European Central Bank.

**Token terbenam pematuhan** — sekatan pemindahan dan kewajipan pelaporan yang dikod dalam kontrak token itu sendiri — muncul dalam piawaian token terkawal seperti ERC-1400 (token sekuriti) dan dalam reka bentuk lapisan pematuhan untuk Project Agorá dan eksperimen pengetokenan berbilang bank pusat yang serupa.

Eksperimen EXTC tidak mencapai skala pengeluaran, tetapi soalan yang diajukannya — tentang penyelesaian boleh atur cara, pemindahan atomik, dan peraturan pembayaran terlaksana sendiri — adalah soalan yang tepat untuk 2018. Infrastruktur yang diperlukan untuk menjawabnya mengambil masa lima tahun lagi untuk matang.

## Soalan Lazim

**Apakah ERC-223 dan mengapa EXTC menggunakannya dan bukan ERC-20?**

Token ERC-20 yang dihantar terus ke alamat kontrak pintar hilang secara senyap kerana kontrak tidak mempunyai cara untuk mengesan pemindahan masuk. ERC-223 membetulkan perkara ini dengan mewajibkan kontrak penerima melaksanakan fungsi `tokenFallback`; jika fungsi itu tiada, pemindahan berbalik semula dan bukannya membakar token. EXTC menerima pakai ERC-223 untuk menjadikan semua pemindahan di atas rantai atomik dan selamat.

**Mengapa projek token pembayaran awal tidak berskala untuk menggantikan perbankan koresponden?**

Mainnet Ethereum pada 2018 memproses kira-kira 15 transaksi sesaat. Volum kiriman wang global sahaja — tanpa mengira kewangan perdagangan atau pembayaran korporat — akan memerlukan puluhan ribu transaksi sesaat. Infrastruktur penskalaan Layer-2 yang diperlukan untuk mencapai truput itu belum siap untuk pengeluaran sehingga 2021–2023.

**Apa yang berlaku kepada idea di sebalik EXTC?**

Konsep teras — peraturan pembayaran boleh atur cara, penyelesaian atomik, logik token terbenam pematuhan — telah diterima pakai oleh protokol DeFi, piawaian token sekuriti terkawal (ERC-1400), dan penyelidikan mata wang digital bank pusat. Rangka kerja deposit token yang kini sedang diuji rintis oleh bank komersial berpunca terus daripada soalan reka bentuk yang mula diajukan oleh eksperimen token pembayaran awal seperti EXTC.

**Bagaimanakah reka bentuk EXTC 2018 dibandingkan dengan cadangan deposit token 2026?**

Model penyelesaiannya serupa — token yang mewakili tuntutan monetari, dipindahkan secara atomik di atas lejar teragih. Perbezaan utamanya ialah: (1) deposit token 2026 merupakan liabiliti bank komersial dan bukannya token pembawa; (2) ia beroperasi di atas lejar berkebenaran atau hibrid dengan pengawasan kawal selia dan bukannya mainnet awam; (3) pematuhan dan pengesahan identiti dikuatkuasakan pada lapisan protokol dan bukannya diserahkan kepada peserta.

## Rujukan

- Ethereum Foundation, (2018). [EIP-20: Token Standard ⧉](https://eips.ethereum.org/EIPS/eip-20 "EIP-20 Token Standard").
- Dexaran, Ethereum GitHub, (2017). [ERC-223 Token Standard Proposal ⧉](https://github.com/ethereum/EIPs/issues/223 "ERC-223 discussion").
- World Bank, (2018). [Remittance Prices Worldwide — Q1 2018 ⧉](https://www.worldbank.org/en/topic/migrationremittancesdiasporaissues/brief/migration-remittances-data "World Bank Remittance Prices").
- Buterin, V., (2014). [Ethereum: A Next-Generation Smart Contract and Decentralised Application Platform ⧉](https://ethereum.org/whitepaper "Ethereum Whitepaper").
