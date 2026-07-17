---
title: "Pembinaan Platform Express Transaction Credits"
tags: "EXTC platform, ERC-223, Ethereum, smart contracts, token architecture, multi-signature, time-locked transfer, blockchain, decentralised finance, collateral-backed loans, ISO 20022, post-quantum cryptography, AI, stablecoins"
subtitle: "Mereka bentuk platform Express Transaction Credits dengan kontrak pintar ERC-223."
description: "Penelitian teknikal mendalam tentang cara platform EXTC dibina di atas Ethereum ERC-223 pada 2018: seni bina token, pengeluaran dana berbilang tandatangan, pindahan berkunci masa, dan pinjaman segera bersandarkan cagaran."
date: "Feb 15, 2018"
language: "ms"
locale: "ms_MY"
banner: "https://cloudcdn.pro/stocks/images/tarik-haiga-3637943.webp"
banner_alt: "Tiang-tiang putih gergasi"
keywords: "platform EXTC, ERC-223, kontrak pintar Ethereum, seni bina token, berbilang tandatangan, pindahan berkunci masa, pembayaran blockchain, pinjaman bersandarkan cagaran, kewangan terdesentralisasi, kripto 2018"
---

![Tiang-tiang putih gergasi](https://cloudcdn.pro/stocks/images/tarik-haiga-3637943.webp).class=\"img-fluid clearfix\"

> **Ringkasan Eksekutif / Intipati Utama**
>
> - **Masalah asasnya.** ERC-20, piawaian token Ethereum yang dominan pada 2018, mempunyai kecacatan struktur: token yang dipindahkan terus ke alamat kontrak pintar akan dimusnahkan secara senyap jika kontrak itu tidak mempunyai pengendali. Mana-mana platform pembayaran yang dibina di atas ERC-20 mewarisi risiko tersebut ([Ethereum EIPs](https://eips.ethereum.org/EIPS/eip-20 "EIP-20: Token Standard")).
> - **ERC-223 sebagai penyelesaian.** ERC-223 mewajibkan kontrak penerima melaksanakan fungsi `tokenFallback(address, uint, bytes)`. Jika tiada, pindahan akan berbalik secara atomik. Tiada token boleh hilang secara senyap ([Ethereum EIPs GitHub](https://github.com/ethereum/EIPs/issues/223 "ERC-223 Token Standard Proposal")).
> - **Lima primitif kontrak EXTC.** Identiti token (nama, simbol, ketepatan 18-perpuluhan), bekalan tetap, pindahan patuh ERC-223, pengeluaran dana korporat berbilang tandatangan, dan arahan tetap berkunci masa mengikut ketinggian blok.
> - **Mekanisme pinjaman cagaran.** Peminjam mengunci token EXTC dalam eskro kontrak; kontrak melepaskan hasil pinjaman secara atomik apabila menerima cagaran, tanpa kelewatan penajajaminan atau kelulusan jawatankuasa kredit.
> - **Apa yang didedahkan eksperimen tentang batas Ethereum.** Pada daya pemprosesan mainnet sekitar ~15 TPS dan kos gas $0.10–$1.00 setiap transaksi pada kemuncak Januari 2018, sebuah rangkaian pembayaran yang memproses walaupun jumlah berskala remitans adalah tidak berdaya maju dari segi ekonomi dan teknikal di atas Ethereum awam tanpa infrastruktur Layer-2.

---

## Masalah Reka Bentuk: Mengapa ERC-20 Tidak Mencukupi

Piawaian ERC-20, yang dicadangkan pada 2015 dan diformalkan dalam Ethereum Improvement Proposal 20, mentakrifkan antara muka token boleh tukar ganti berkanun yang menggerakkan ledakan ICO pada 2017–2018. Enam fungsi terasnya — `totalSupply`, `balanceOf`, `transfer`, `transferFrom`, `approve`, dan `allowance` — sudah mencukupi untuk penerbitan dan pertukaran token yang mudah.

Namun, bagi sebuah platform pembayaran, ERC-20 mempunyai kecacatan kritikal untuk pengeluaran. Fungsi `transfer(address _to, uint256 _value)` memindahkan token ke mana-mana alamat, termasuk alamat kontrak, tanpa mencetuskan sebarang kod dalam kontrak penerima. Kontrak yang tidak diprogramkan secara khusus untuk menjejaki pindahan ERC-20 yang masuk tidak mempunyai cara untuk mengesannya. Token yang dihantar dengan cara ini terperangkap secara kekal, tanpa mekanisme untuk pemulihan.

Komuniti Ethereum menganggarkan bahawa berpuluh-puluh juta dolar token ERC-20 telah hilang secara kekal menjelang pertengahan 2018 melalui mekanisme ini. Membina platform pembayaran yang pindahannya boleh gagal secara senyap dan memusnahkan dana pengguna bukanlah sesuatu yang boleh diterima.

## Penyelesaian ERC-223: Pindahan Atomik dengan Pemberitahuan

ERC-223, yang dicadangkan pada penjejak isu GitHub Ethereum EIPs, menangani masalah kehilangan senyap dengan mengubah apa yang perlu dilakukan oleh sesuatu pindahan token. Di bawah ERC-223, `transfer(address _to, uint256 _value, bytes _data)` memeriksa sama ada alamat penerima mengandungi kod kontrak. Jika ya, pindahan itu memanggil `_to.tokenFallback(address _from, uint256 _value, bytes _data)`.

Sifat kritikalnya: jika kontrak penerima tidak melaksanakan `tokenFallback`, keseluruhan transaksi pindahan akan berbalik. Tiada token meninggalkan baki penghantar. Tiada token terperangkap. Pindahan itu bersifat atomik — ia sama ada selesai dengan kod penerima dilaksanakan, atau ia gagal sepenuhnya dengan keadaan kekal tidak berubah.

Bagi EXTC, ini bermaksud:

- **Pembayaran kepada kontrak pintar selamat secara reka bentuk.** Kontrak eskro, dompet berbilang tandatangan, dan kontrak pemberian pinjaman boleh menerima token EXTC tanpa sebarang risiko dana hilang secara tidak boleh balik.
- **Medan `_data` membolehkan metadata pembayaran yang kaya.** Muatan bait boleh membawa rujukan invois, kod penghalaan, atau atestasi pematuhan — maklumat yang tidak dapat disampaikan oleh pindahan ERC-20 yang ringkas.
- **Kos gas sedikit lebih tinggi.** Memanggil `tokenFallback` menambah kira-kira 2,000–5,000 gas setiap pindahan, satu overhed kecil pada harga gas 2018.

## Seni Bina Kontrak EXTC

Kontrak token EXTC ialah pelaksanaan Solidity yang distrukturkan sekitar lima modul:

### 1. Identiti Token

```
string public name = "Express Transaction Credits";
string public symbol = "EXTC";
uint8 public decimals = 18;
```

Lapan belas tempat perpuluhan memberikan EXTC ketepatan sub-sen, sepadan dengan kehalusan yang diperlukan bagi kes penggunaan mikro-pembayaran dan mikro-pinjaman. Simbol `EXTC` ialah pengecam atas rantai yang didaftarkan dalam kontrak token.

### 2. Jumlah Bekalan Tetap

Jumlah bekalan ditetapkan semasa penggunaan kontrak dan tidak boleh dikembang oleh cetakan seterusnya. Pilihan reka bentuk ini menjadikan EXTC deflasi: mana-mana token yang dikeluarkan secara kekal daripada peredaran — melalui operasi bakar yang tidak boleh balik — mengurangkan bekalan tanpa gantian. Model bekalan tetap adalah lazim dalam reka bentuk token pembayaran 2018, mencerminkan andaian berpengaruh Bitcoin bahawa tekanan deflasi adalah suatu ciri yang baik bagi medium pertukaran.

### 3. Baki dan Pindahan Patuh ERC-223

Fungsi pindahan teras melaksanakan antara muka ERC-223 sepenuhnya. Pemetaan baki dalaman menjejaki pegangan setiap alamat. Pembantu `isContract(address)` membezakan alamat EOA (akaun milik luaran) daripada alamat kontrak untuk menentukan sama ada `tokenFallback` perlu dipanggil.

### 4. Pengeluaran Dana Korporat Berbilang Tandatangan

Aliran kerja pembayaran korporat memerlukan keizinan bersama: tiada penandatangan tunggal boleh memulakan pengeluaran dana secara berat sebelah melebihi ambang yang ditakrifkan. Kontrak EXTC melaksanakan skema berbilang tandatangan dua-daripada-N:

1. Seorang pemula yang ditetapkan mencadangkan pindahan, menyatakan penerima, jumlah, dan satu nonce.
2. Seorang penandatangan bersama mengesahkan nonce tersebut.
3. Hanya selepas kedua-dua tandatangan direkodkan atas rantai barulah pindahan itu dilaksanakan.

Ini menghapuskan risiko titik kegagalan tunggal bagi akaun korporat sambil mengekalkan keseluruhan aliran keizinan atas rantai dan boleh diaudit tanpa perantara rumah penjelasan.

### 5. Arahan Tetap Berkunci Masa Mengikut Ketinggian Blok

Pembayaran berulang — gaji, langganan, bayaran balik pinjaman berjadual — memerlukan primitif arahan tetap. EXTC melaksanakan ini sebagai kunci masa: satu rekod pindahan disimpan dalam kontrak dengan parameter `releaseBlock`. Pindahan itu tidak boleh dilaksanakan sehingga ketinggian blok Ethereum mencapai `releaseBlock`.

Ketinggian blok sebagai proksi masa merupakan pilihan pragmatik pada 2018. Ethereum menyasarkan selang blok 15 saat, menjadikan ketinggian blok sebagai proksi yang agak boleh dipercayai bagi masa jam dinding dalam julat beberapa minit. Cap masa mutlak (`block.timestamp`) tersedia tetapi terdedah kepada manipulasi pelombong dalam tetingkap ±900 saat, menjadikan ketinggian blok sebagai rujukan yang lebih selamat bagi kontrak kewangan.

## Mekanisme Pinjaman Segera Bersandarkan Cagaran

Primitif pemberian pinjaman EXTC ialah komponen yang paling kompleks. Reka bentuknya:

1. **Peminjam mengunci cagaran.** Peminjam memanggil `lockCollateral(uint256 _collateralAmount)`, memindahkan token EXTC ke eskro kontrak pemberian pinjaman melalui `tokenFallback` ERC-223.
2. **Pemeriksaan nisbah pinjaman-nilai.** Kontrak membaca nisbah LTV yang telah dikonfigurasikan terlebih dahulu (cth. 50%) dan mengira jumlah pinjaman maksimum terhadap cagaran yang dikunci.
3. **Pengeluaran pinjaman atomik.** Jika cagaran memenuhi ambang minimum, kontrak segera memindahkan jumlah pinjaman ke alamat peminjam. Tiada barisan penajajaminan, tiada jawatankuasa kredit, tiada kelewatan penyelesaian.
4. **Bayaran balik dan pelepasan.** Apabila bayaran balik dibuat — prinsipal ditambah kadar faedah tetap — kontrak melepaskan cagaran semula kepada peminjam. Kegagalan membayar balik menjelang `releaseBlock` mencetuskan pembubaran automatik: kontrak memindahkan cagaran ke alamat yang ditetapkan oleh pemberi pinjaman.

Keseluruhan aliran dikuatkuasakan oleh kod kontrak. Tiada pihak perlu mempercayai pihak yang satu lagi atau bergantung pada perantara untuk menguatkuasakan terma.

## Apa Yang Didedahkan Oleh Eksperimen

Seni bina kontrak EXTC adalah koheren dari segi teknikal. ERC-223 menyelesaikan kecacatan keselamatan ERC-20 yang paling serius. Primitif berbilang tandatangan dan kunci masa memetakan secara langsung kepada aliran kerja pembayaran korporat sebenar. Mekanisme pinjaman cagaran menunjukkan bahawa pemberian pinjaman bercagar boleh diautomasikan sepenuhnya dan menguatkuasakan dirinya sendiri atas rantai.

Dua kekangan mendedahkan diri dalam amalan:

**Kos gas.** Pada kemuncak Januari 2018, harga gas Ethereum mencapai 50–100 gwei, menjadikan satu pindahan token ERC-223 berkos $0.50–$2.00. Bagi mikro-pembayaran atau remitans bernilai $10–$50, yuran tersebut adalah terlalu mahal.

**Daya pemprosesan.** Had gas blok mainnet Ethereum pada awal 2018 adalah kira-kira 8 juta gas. Satu pindahan ERC-223 menggunakan kira-kira 50,000–80,000 gas. Oleh itu, rangkaian boleh memproses kira-kira 100–160 pindahan token EXTC setiap blok, atau sekitar 7–11 sesaat pada selang blok 15 saat. Skala rangkaian pembayaran — beratus atau beribu transaksi sesaat — tidak dapat dicapai di atas Ethereum awam tanpa infrastruktur Layer-2 yang belum wujud dalam bentuk pengeluaran ketika itu.

Ini merupakan kekangan infrastruktur, bukan kecacatan reka bentuk dalam EXTC. Logik kontrak adalah betul. Blockchain asas belum mampu menyokong jumlah pembayaran pada skala industri kewangan.

## Idea-Idea Yang Sampai Ke Pengeluaran

Beberapa corak reka bentuk daripada EXTC disahkan oleh pembangunan seterusnya:

**Pindahan token atomik dengan pemberitahuan penerima** — sifat teras ERC-223 — menjadi asas kepada ERC-777 (2019), yang melanjutkan model pemberitahuan dan kemudiannya digabungkan ke dalam protokol pemberian pinjaman DeFi. Corak `tokenFallback` muncul di seluruh seni bina DeFi moden.

**Keizinan berbilang tandatangan untuk pengeluaran dana korporat** — corak mewajibkan berbilang tandatangan atas rantai sebelum pelaksanaan — menjadi model piawai bagi pengurusan perbendaharaan DAO dan penyelesaian kustodi institusi. Gnosis Safe, yang dilancarkan pada 2018, mempopularkan corak ini pada skala besar.

**Pinjaman segera bersandarkan cagaran tanpa perantara** — mekanisme mengunci cagaran dalam eskro dan melepaskan hasil pinjaman secara atomik — ialah reka bentuk asas protokol pemberian pinjaman DeFi seperti Compound (2018) dan Aave (2020).

**Kunci masa mengikut ketinggian blok untuk pembayaran berjadual** — corak mengekod masa pelaksanaan masa hadapan dalam kontrak — muncul dalam kontrak peletakhakan token, cadangan tadbir urus tertangguh, dan reka bentuk orakel harga purata berwajaran masa (TWAP) di seluruh ekosistem DeFi.

Eksperimen EXTC tidak mencapai skala pengeluaran. Infrastruktur yang diperlukan untuk menjadikan reka bentuk itu berdaya maju mengambil masa tiga hingga lima tahun lagi untuk matang. Persoalan reka bentuk yang diajukannya adalah persoalan yang tepat untuk 2018.

## Soalan Lazim

**Mengapa ERC-223 tidak pernah diterima pakai sebagai piawaian token dominan walaupun ia menyelesaikan kecacatan ERC-20?**

ERC-223 mewajibkan kontrak penerima melaksanakan `tokenFallback`, memutuskan keserasian ke belakang dengan ribuan kontrak yang sudah digunakan untuk token ERC-20. Ekosistem ERC-20 sedia ada terlalu besar untuk dipindahkan. Cadangan seterusnya — terutamanya ERC-777 dan ERC-1363 — menangani masalah yang sama dengan pertimbangan keserasian yang berbeza, tetapi ERC-20 kekal dominan menerusi gabungan kesan rangkaian dan pengenalan corak token berbalut yang mengelakkan senario kehilangan senyap.

**Apa yang berlaku kepada token dan platform EXTC?**

EXTC ialah bukti konsep dan projek penyelidikan awal dari 2018. Pasaran ICO dan token pembayaran yang lebih luas mengecut dengan mendadak sepanjang 2018–2019 apabila batas kebolehskalaan Ethereum dan ketidakpastian kawal selia menjadi jelas. Idea-idea yang terkandung dalam reka bentuk EXTC muncul semula dalam protokol kemudian yang mempunyai akses kepada infrastruktur Layer-2, perkakasan yang lebih baik, dan rangka kerja kawal selia yang lebih jelas.

**Bagaimanakah model pinjaman cagaran EXTC berbanding dengan protokol DeFi moden seperti Aave?**

Mekanisme terasnya sama: kunci cagaran, terima pinjaman yang bersaiz mengikut nisbah LTV, bayar balik atau hadapi pembubaran. Perbezaannya ialah: (1) protokol DeFi moden menggunakan suapan harga orakel untuk LTV dinamik dan bukannya nisbah tetap; (2) mereka menggunakan kadar faedah algoritma yang bertindak balas terhadap penggunaan kumpulan; (3) mereka beroperasi di atas rangkaian Layer-2 dengan kos gas 10–100 kali lebih rendah daripada mainnet 2018; (4) Aave dan Compound telah menjalani audit keselamatan formal dan memegang berbilion dolar kecairan, memberikan pengesahan empirikal bahawa model asas tersebut adalah kukuh.

**Apakah kekangan versi Solidity pada awal 2018?**

Kontrak EXTC ditulis untuk Solidity 0.4.x, versi dominan pada awal 2018. Solidity 0.4 tidak mempunyai banyak ciri keselamatan yang diperkenalkan dalam versi kemudian: pemeriksaan limpahan integer (ditambah secara automatik dalam 0.8.0), `require`/`revert` dengan mesej ralat (terhad dalam 0.4), dan keterlihatan fungsi eksplisit (lalai ialah awam dalam 0.4). Kontrak itu bergantung pada perpustakaan SafeMath OpenZeppelin untuk melindungi daripada limpahan, satu corak yang lazim sebelum pengkompil menguatkuasakannya secara asli.

## Rujukan

- Ethereum Foundation, (2015). [EIP-20: Token Standard ⧉](https://eips.ethereum.org/EIPS/eip-20 "EIP-20 Token Standard").
- Dexaran, Ethereum GitHub, (2017). [ERC-223 Token Standard Proposal ⧉](https://github.com/ethereum/EIPs/issues/223 "ERC-223 discussion").
- OpenZeppelin, (2018). [OpenZeppelin Contracts — SafeMath ⧉](https://github.com/OpenZeppelin/openzeppelin-contracts "OpenZeppelin Contracts").
- Ethereum Foundation, (2014). [Ethereum Whitepaper ⧉](https://ethereum.org/whitepaper "Ethereum Whitepaper").
