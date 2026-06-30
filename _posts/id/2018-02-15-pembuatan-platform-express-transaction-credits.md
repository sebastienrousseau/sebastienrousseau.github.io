---
title: "Pembuatan Platform Express Transaction Credits"
subtitle: "Merancang platform Express Transaction Credits dengan smart contract ERC-223."
description: "Kajian teknis tentang bagaimana platform EXTC dibangun di atas Ethereum ERC-223 pada 2018: arsitektur token, pencairan multi-tanda tangan, transfer berkunci waktu, dan pinjaman instan berbasis agunan."
date: "Feb 15, 2018"
language: "id-ID"
locale: "id_ID"
banner: "https://cloudcdn.pro/stocks/images/tarik-haiga-3637943.webp"
banner_alt: "Pilar putih berukuran besar"
keywords: "platform EXTC, ERC-223, Ethereum, smart contract, arsitektur token, multi-tanda tangan, transfer berkunci waktu, pembayaran blockchain, pinjaman berbasis agunan, keuangan terdesentralisasi, kripto 2018"
---

![Pilar putih berukuran besar](https://cloudcdn.pro/stocks/images/tarik-haiga-3637943.webp).class=\"img-fluid clearfix\"

> **TL;DR.** Kajian teknis tentang bagaimana platform EXTC dibangun di atas Ethereum ERC-223 pada 2018: arsitektur token, pencairan multi-tanda tangan, transfer berkunci waktu, dan pinjaman instan berbasis agunan.
>
> **Ringkasan eksekutif / kesimpulan utama**
>
> - **Akar masalahnya.** ERC-20, standar token Ethereum yang dominan pada 2018, memiliki kelemahan struktural: token yang dikirim langsung ke alamat smart contract dapat hilang diam-diam jika kontrak tersebut tidak memiliki handler. Platform pembayaran apa pun yang dibangun di atas ERC-20 mewarisi risiko itu ([Ethereum EIPs](https://eips.ethereum.org/EIPS/eip-20 "EIP-20: Token Standard")).
> - **ERC-223 sebagai perbaikan.** ERC-223 mewajibkan kontrak penerima mengimplementasikan fungsi `tokenFallback(address, uint, bytes)`. Jika fungsi itu tidak ada, transfer dibatalkan secara atomik. Token tidak dapat hilang diam-diam ([Ethereum EIPs GitHub](https://github.com/ethereum/EIPs/issues/223 "ERC-223 Token Standard Proposal")).
> - **Lima primitif kontrak EXTC.** Identitas token (nama, simbol, presisi 18 desimal), suplai tetap, transfer sesuai ERC-223, pencairan perusahaan multi-tanda tangan, dan standing order berbasis tinggi blok.
> - **Mekanisme pinjaman berbasis agunan.** Peminjam mengunci token EXTC dalam escrow kontrak; kontrak melepas dana pinjaman secara atomik setelah menerima agunan, tanpa antrean underwriting atau persetujuan komite kredit.
> - **Pelajaran tentang batas Ethereum.** Dengan throughput mainnet sekitar 15 TPS dan biaya gas sekitar $0,10-$1,00 per transaksi pada puncak Januari 2018, jaringan pembayaran dengan volume setara remitansi pun tidak layak secara ekonomi maupun teknis di Ethereum publik tanpa infrastruktur Layer-2.

---

## Masalah Desain: Mengapa ERC-20 Tidak Memadai

Standar ERC-20, yang diusulkan pada 2015 dan diformalkan dalam Ethereum Improvement Proposal 20, mendefinisikan antarmuka token fungible kanonis yang menopang ledakan ICO 2017-2018. Enam fungsi intinya - `totalSupply`, `balanceOf`, `transfer`, `transferFrom`, `approve`, dan `allowance` - cukup untuk penerbitan dan pertukaran token sederhana.

Namun untuk platform pembayaran, ERC-20 memiliki kelemahan produksi yang kritis. Fungsi `transfer(address _to, uint256 _value)` memindahkan token ke alamat mana pun, termasuk alamat kontrak, tanpa memicu kode apa pun di kontrak penerima. Kontrak yang tidak secara khusus diprogram untuk melacak transfer ERC-20 masuk tidak memiliki cara untuk mendeteksinya. Token yang dikirim dengan cara ini terjebak permanen, tanpa mekanisme pemulihan.

Komunitas Ethereum memperkirakan bahwa puluhan juta dolar dalam token ERC-20 telah hilang permanen pada pertengahan 2018 akibat mekanisme ini. Membangun platform pembayaran yang memungkinkan transfer gagal diam-diam dan menghancurkan dana pengguna bukanlah pilihan yang dapat diterima.

## Solusi ERC-223: Transfer Atomik dengan Notifikasi

ERC-223, yang diusulkan di pelacak isu GitHub Ethereum EIPs, mengatasi masalah kehilangan diam-diam dengan mengubah kewajiban sebuah transfer token. Dalam ERC-223, `transfer(address _to, uint256 _value, bytes _data)` memeriksa apakah alamat penerima berisi kode kontrak. Jika ya, transfer memanggil `_to.tokenFallback(address _from, uint256 _value, bytes _data)`.

Sifat kritisnya adalah ini: jika kontrak penerima tidak mengimplementasikan `tokenFallback`, seluruh transaksi transfer dibatalkan. Tidak ada token yang keluar dari saldo pengirim. Tidak ada token yang terjebak. Transfer bersifat atomik - entah selesai dengan kode penerima berjalan, atau gagal sepenuhnya tanpa perubahan state.

Bagi EXTC, ini berarti:

- **Pembayaran ke smart contract aman secara desain.** Kontrak escrow, dompet multi-sig, dan kontrak pinjaman dapat menerima token EXTC tanpa risiko dana hilang permanen.
- **Field `_data` memungkinkan metadata pembayaran yang kaya.** Payload bytes dapat membawa referensi invoice, kode routing, atau atestasi kepatuhan - informasi yang tidak dapat dibawa oleh transfer ERC-20 sederhana.
- **Biaya gas sedikit lebih tinggi.** Pemanggilan `tokenFallback` menambah sekitar 2.000-5.000 gas per transfer, overhead kecil pada harga gas 2018.

## Arsitektur Kontrak EXTC

Kontrak token EXTC adalah implementasi Solidity yang disusun di sekitar lima modul:

### 1. Identitas Token

```
string public name = "Express Transaction Credits";
string public symbol = "EXTC";
uint8 public decimals = 18;
```

Delapan belas tempat desimal memberi EXTC presisi sub-sen, sesuai dengan granularitas yang diperlukan untuk kasus penggunaan micropayment dan pinjaman mikro. Simbol `EXTC` adalah pengenal on-chain yang terdaftar di kontrak token.

### 2. Total Suplai Tetap

Total suplai ditetapkan saat deployment kontrak dan tidak dapat dinaikkan melalui pencetakan berikutnya. Pilihan desain ini membuat EXTC bersifat deflasioner: setiap token yang dihapus permanen dari peredaran melalui operasi burn yang tidak dapat dibalik akan mengurangi suplai tanpa pengganti. Model suplai tetap adalah pola umum dalam desain token pembayaran pada 2018, yang mencerminkan asumsi yang dipengaruhi Bitcoin bahwa tekanan deflasioner adalah fitur bagi medium pertukaran.

### 3. Saldo dan Transfer yang Sesuai ERC-223

Fungsi transfer inti mengimplementasikan antarmuka ERC-223 secara penuh. Mapping saldo internal melacak kepemilikan setiap alamat. Helper `isContract(address)` membedakan alamat EOA (externally owned account) dari alamat kontrak untuk menentukan apakah `tokenFallback` perlu dipanggil.

### 4. Pencairan Perusahaan Multi-Tanda Tangan

Alur pembayaran perusahaan membutuhkan otorisasi bersama: tidak ada satu penanda tangan pun yang boleh memulai pencairan di atas ambang tertentu secara sepihak. Kontrak EXTC mengimplementasikan skema multi-tanda tangan two-of-N:

1. Inisiator yang ditunjuk mengusulkan transfer, menentukan penerima, jumlah, dan nonce.
2. Penanda tangan pendamping mengonfirmasi nonce tersebut.
3. Transfer hanya dieksekusi setelah kedua tanda tangan tercatat on-chain.

Ini menghilangkan risiko single point of failure untuk akun perusahaan, sekaligus menjaga seluruh alur otorisasi tetap on-chain dan dapat diaudit tanpa perantara clearing house.

### 5. Standing Order Berkunci Waktu Berdasarkan Tinggi Blok

Pembayaran berulang - gaji, langganan, jadwal pelunasan pinjaman - membutuhkan primitif standing order. EXTC mengimplementasikannya sebagai time-lock: catatan transfer disimpan di kontrak dengan parameter `releaseBlock`. Transfer tidak dapat dieksekusi sampai tinggi blok Ethereum mencapai `releaseBlock`.

Tinggi blok sebagai proksi waktu adalah pilihan pragmatis pada 2018. Ethereum menargetkan interval blok 15 detik, sehingga tinggi blok cukup andal sebagai proksi waktu kalender dalam rentang beberapa menit. Timestamp absolut (`block.timestamp`) tersedia, tetapi rentan dimanipulasi miner dalam jendela sekitar +/-900 detik, sehingga tinggi blok menjadi rujukan yang lebih aman untuk kontrak finansial.

## Mekanisme Pinjaman Instan Berbasis Agunan

Primitif pinjaman EXTC adalah komponen paling kompleks. Desainnya:

1. **Peminjam mengunci agunan.** Peminjam memanggil `lockCollateral(uint256 _collateralAmount)`, mentransfer token EXTC ke escrow kontrak pinjaman melalui `tokenFallback` ERC-223.
2. **Pemeriksaan rasio loan-to-value.** Kontrak membaca rasio LTV yang telah dikonfigurasi, misalnya 50%, lalu menghitung jumlah pinjaman maksimum terhadap agunan yang dikunci.
3. **Pencairan pinjaman atomik.** Jika agunan memenuhi ambang minimum, kontrak langsung mentransfer jumlah pinjaman ke alamat peminjam. Tidak ada antrean underwriting, komite kredit, atau penundaan settlement.
4. **Pelunasan dan pelepasan.** Setelah pelunasan - pokok ditambah tingkat bunga tetap - kontrak melepas agunan kembali ke peminjam. Kegagalan membayar sampai `releaseBlock` memicu likuidasi otomatis: kontrak mentransfer agunan ke alamat pemberi pinjaman yang ditunjuk.

Seluruh alur ditegakkan oleh kode kontrak. Tidak ada pihak yang perlu mempercayai pihak lain atau bergantung pada perantara untuk menegakkan syarat.

## Apa yang Diungkap Eksperimen Ini

Arsitektur kontrak EXTC koheren secara teknis. ERC-223 menyelesaikan kelemahan keselamatan paling serius dari ERC-20. Primitif multi-tanda tangan dan time-lock memetakan langsung ke alur pembayaran perusahaan nyata. Mekanisme pinjaman berbasis agunan menunjukkan bahwa pinjaman terjamin dapat sepenuhnya diotomatisasi dan menegakkan dirinya sendiri on-chain.

Dua kendala muncul dalam praktik:

**Biaya gas.** Pada puncak Januari 2018, harga gas Ethereum mencapai 50-100 gwei, sehingga satu transfer token ERC-223 dapat menelan biaya $0,50-$2,00. Untuk micropayment atau remitansi $10-$50, biaya seperti itu terlalu tinggi.

**Throughput.** Batas gas blok mainnet Ethereum pada awal 2018 sekitar 8 juta gas. Transfer ERC-223 mengonsumsi kira-kira 50.000-80.000 gas. Dengan demikian jaringan hanya dapat memproses sekitar 100-160 transfer token EXTC per blok, atau sekitar 7-11 per detik pada interval blok 15 detik. Skala jaringan pembayaran - ratusan atau ribuan transaksi per detik - tidak dapat dicapai di Ethereum publik tanpa infrastruktur Layer-2 yang saat itu belum tersedia dalam bentuk produksi.

Ini adalah kendala infrastruktur, bukan cacat desain EXTC. Logika kontraknya benar. Blockchain dasarnya belum mampu mendukung volume pembayaran pada skala industri keuangan.

## Gagasan yang Mencapai Produksi

Beberapa pola desain dari EXTC kemudian divalidasi oleh perkembangan berikutnya:

**Transfer token atomik dengan notifikasi penerima** - sifat inti ERC-223 - menjadi dasar ERC-777 pada 2019, yang memperluas model notifikasi dan kemudian masuk ke protokol pinjaman DeFi. Pola `tokenFallback` muncul di banyak arsitektur DeFi modern.

**Otorisasi multi-tanda tangan untuk pencairan perusahaan** - pola yang mewajibkan beberapa tanda tangan on-chain sebelum eksekusi - menjadi model standar untuk pengelolaan treasury DAO dan solusi kustodian institusional. Gnosis Safe, diluncurkan pada 2018, memopulerkan pola ini dalam skala besar.

**Pinjaman instan berbasis agunan tanpa perantara** - mekanisme mengunci agunan dalam escrow dan melepas dana pinjaman secara atomik - adalah desain fundamental protokol pinjaman DeFi seperti Compound pada 2018 dan Aave pada 2020.

**Time-lock berbasis tinggi blok untuk pembayaran terjadwal** - pola pengodean waktu eksekusi masa depan di dalam kontrak - muncul dalam kontrak vesting token, proposal tata kelola tertunda, dan desain oracle time-weighted average price (TWAP) di seluruh ekosistem DeFi.

Eksperimen EXTC tidak mencapai skala produksi. Infrastruktur yang diperlukan agar desain ini layak membutuhkan tiga sampai lima tahun lagi untuk matang. Namun pertanyaan desain yang diajukannya adalah pertanyaan yang tepat untuk 2018.

## Pertanyaan yang Sering Diajukan

**Mengapa ERC-223 tidak pernah menjadi standar token dominan meski memperbaiki kelemahan ERC-20?**

ERC-223 mengharuskan kontrak penerima mengimplementasikan `tokenFallback`, sehingga memutus kompatibilitas mundur dengan ribuan kontrak yang sudah dideploy untuk token ERC-20. Ekosistem ERC-20 yang ada terlalu besar untuk dimigrasikan. Proposal berikutnya - terutama ERC-777 dan ERC-1363 - menangani masalah yang sama dengan trade-off kompatibilitas berbeda, tetapi ERC-20 tetap dominan karena efek jaringan dan munculnya pola wrapped token yang menghindari skenario kehilangan diam-diam.

**Apa yang terjadi pada token dan platform EXTC?**

EXTC adalah proof-of-concept dan proyek riset awal dari 2018. Pasar ICO dan token pembayaran yang lebih luas menyusut tajam sepanjang 2018-2019 ketika batas skalabilitas Ethereum dan ketidakpastian regulasi menjadi jelas. Gagasan yang tertanam dalam desain EXTC muncul kembali dalam protokol-protokol berikutnya yang memiliki akses ke infrastruktur Layer-2, tooling yang lebih baik, dan kerangka regulasi yang lebih jelas.

**Bagaimana model pinjaman agunan EXTC dibandingkan dengan protokol DeFi modern seperti Aave?**

Mekanisme intinya sama: kunci agunan, terima pinjaman yang dihitung terhadap rasio LTV, lalu lunasi atau hadapi likuidasi. Perbedaannya adalah: (1) protokol DeFi modern memakai feed harga oracle untuk LTV dinamis, bukan rasio tetap; (2) protokol modern memakai tingkat bunga algoritmik yang merespons utilisasi pool; (3) protokol tersebut berjalan di jaringan Layer-2 dengan biaya gas 10-100 kali lebih rendah daripada mainnet 2018; (4) Aave dan Compound telah menjalani audit keamanan formal dan menampung likuiditas miliaran dolar, memberikan validasi empiris bahwa model dasarnya sehat.

**Apa batasan versi Solidity pada awal 2018?**

Kontrak EXTC ditulis untuk Solidity 0.4.x, versi dominan pada awal 2018. Solidity 0.4 belum memiliki banyak fitur keselamatan yang diperkenalkan di versi berikutnya: pemeriksaan overflow integer otomatis (ditambahkan di 0.8.0), `require`/`revert` dengan pesan kesalahan yang lebih baik (terbatas di 0.4), dan visibilitas fungsi eksplisit (default-nya public di 0.4). Kontrak mengandalkan pustaka SafeMath dari OpenZeppelin untuk mencegah overflow, pola umum sebelum compiler menegakkannya secara native.

## Referensi

- Ethereum Foundation, (2015). [EIP-20: Token Standard ⧉](https://eips.ethereum.org/EIPS/eip-20 "EIP-20 Token Standard").
- Dexaran, Ethereum GitHub, (2017). [ERC-223 Token Standard Proposal ⧉](https://github.com/ethereum/EIPs/issues/223 "ERC-223 discussion").
- OpenZeppelin, (2018). [OpenZeppelin Contracts - SafeMath ⧉](https://github.com/OpenZeppelin/openzeppelin-contracts "OpenZeppelin Contracts").
- Ethereum Foundation, (2014). [Ethereum Whitepaper ⧉](https://ethereum.org/whitepaper "Ethereum Whitepaper").
