---
title: "Memahami Teknologi di Sebalik Blockchain"
tags: "blockchain, Ethereum, smart contracts, cryptography, Merkle tree, consensus mechanism, proof of work, EVM, Solidity, ERC-20, decentralised finance, ISO 20022, post-quantum cryptography, AI, stablecoins, tokenised deposits"
subtitle: "Panduan praktikal tentang kriptografi dan konsensus di sebalik blockchain."
description: "Pengenalan teknikal tentang cara blockchain berfungsi: rantaian cincang kriptografi, pepohon Merkle, konsensus teragih, dan mengapa lapisan boleh atur cara Ethereum mengubah lejar pembayaran menjadi platform untuk kontrak pintar dan aset ditokenkan."
date: "Jan 09, 2018"
language: "ms"
locale: "ms_MY"
banner: "https://cloudcdn.pro/stocks/images/adam-smigielski-K5mPtONmpHM.webp"
banner_alt: "Blok lejar digital abstrak yang dihubungkan oleh jejak cahaya di atas latar belakang gelap"
keywords: "teknologi blockchain, cincang kriptografi, pepohon Merkle, konsensus teragih, bukti kerja, Ethereum, kontrak pintar, EVM, Solidity, ERC-20, lejar teragih, kewangan terdesentralisasi"
---

![Blok lejar digital abstrak yang dihubungkan oleh jejak cahaya di atas latar belakang gelap](https://cloudcdn.pro/stocks/images/adam-smigielski-K5mPtONmpHM.webp).class=\"img-fluid clearfix\"

> **Ringkasan Eksekutif / Pengajaran Utama**
>
> - **Masalahnya.** Wang tunai digital memerlukan penyelesaian kepada masalah perbelanjaan berganda: menghalang unit yang sama daripada dibelanjakan dua kali tanpa rumah penjelasan yang dipercayai. Kertas putih Bitcoin 2008 menyelesaikan ini dengan menggantikan perantara yang dipercayai dengan bukti kriptografi dan konsensus teragih ([Nakamoto, 2008](https://bitcoin.org/bitcoin.pdf "Bitcoin: A Peer-to-Peer Electronic Cash System")).
> - **Struktur datanya.** Blockchain ialah senarai terpaut blok di mana setiap pengepala blok mengandungi cincang SHA-256 pengepala sebelumnya. Rantaian cincang menjadikan sejarah tokok-sahaja: mengubah mana-mana blok lalu membatalkan setiap cincang berikutnya, memaksa penyerang mengulang semula semua bukti-kerja berikutnya.
> - **Pepohon Merkle.** Transaksi dalam sesuatu blok dicincang menjadi pepohon Merkle binari. Cincang akar, yang disimpan dalam pengepala blok, membolehkan pengesahan cekap bagi mana-mana transaksi individu tanpa memuat turun keseluruhan blok — asas bagi klien SPV ringan.
> - **Peluasan Ethereum.** Kertas Kuning Ethereum (2014) memperkenalkan EVM — sebuah mesin tindanan berketentuan yang berjalan pada setiap nod penuh. Kontrak pintar ialah bytecode yang digunakan pada rantaian; ia dilaksanakan secara identik pada semua nod dan diselesaikan secara atomik, menggantikan perantara yang dipercayai dengan kod yang menguatkuasakan dirinya sendiri ([Wood, 2014](https://ethereum.github.io/yellowpaper/paper.pdf "Ethereum Yellow Paper")).
> - **Kepentingan praktikal.** Setiap aset ditokenkan, stablecoin, dan protokol DeFi yang digunakan sejak 2017 berjalan di atas asas ini. Memahami rantaian cincang, pepohon Merkle, dan model pelaksanaan EVM ialah prasyarat untuk bekerja dengan mana-mana sistem berasaskan Ethereum.

---

## Masalah yang Diselesaikan Blockchain

Sebelum Bitcoin, pembayaran digital memerlukan perantara yang dipercayai — bank, pemproses pembayaran, atau rumah penjelasan — untuk menghalang perbelanjaan berganda. Jika Alice menghantar fail digital yang mewakili £10 kepada Bob, tiada apa-apa dalam fail itu sendiri yang menghalangnya daripada menghantar salinan yang sama kepada Carol. Penyelesaian dalam setiap sistem sedia ada ialah penyimpanan rekod berpusat: lejar bank menyatakan bahawa wang itu telah dibelanjakan, jadi ia tidak boleh dibelanjakan sekali lagi.

Sumbangan Bitcoin ialah menggantikan lejar yang dipercayai itu dengan lejar teragih di mana rekod semua transaksi direplikasi merentas ribuan nod bebas. Rasa tidak percaya bersama antara nod ditukarkan menjadi keselamatan melalui dua mekanisme:

1. **Pemautan kriptografi.** Setiap blok transaksi mengandungi cincang blok sebelumnya. Fungsi cincang ialah pemetaan berketentuan sehala: diberi sebarang input, fungsi tersebut menghasilkan output panjang tetap, dan menukar walau satu bit input menghasilkan output yang sama sekali berbeza. Ini bermakna sebarang perubahan pada blok bersejarah membatalkan setiap blok selepasnya.

2. **Konsensus bukti-kerja.** Menambah blok baharu memerlukan pencarian nilai nonce sedemikian rupa sehingga cincang blok jatuh di bawah ambang sasaran — mahal dari segi pengiraan untuk dicari, remeh murah untuk disahkan. Ini menjadikan penulisan semula sejarah mahal secara berkadar dengan kedalaman blok yang diubah, kerana penyerang mesti mengulang semua bukti-kerja daripada blok itu hingga ke hujung rantaian.

Gabungan ini bermakna rantaian terpanjang dengan bukti-kerja terkumpul terbanyak, secara binaannya, ialah rantaian yang diselenggarakan oleh peserta jujur yang membelanjakan sumber sebenar.

## Blok Binaan Kriptografi

Teknologi blockchain menggabungkan tiga primitif kriptografi sedia ada menjadi seni bina baharu:

### Fungsi Cincang SHA-256

SHA-256 (Secure Hash Algorithm 256-bit) ialah ahli keluarga SHA-2 yang dipiawaikan oleh NIST. Ia mengambil input panjang sebarangan dan menghasilkan output 256-bit. Sifat utama untuk penggunaan blockchain:

- **Berketentuan.** Input yang sama sentiasa menghasilkan output yang sama.
- **Rintangan pra-imej.** Diberi output cincang, adalah tidak boleh laksana dari segi pengiraan untuk membina semula input.
- **Kesan runtuhan salji.** Menukar satu bit input menukar kira-kira separuh daripada bit output, menjadikan carian kekerasan tidak cekap.
- **Rintangan perlanggaran.** Adalah tidak boleh laksana dari segi pengiraan untuk mencari dua input berbeza yang menghasilkan cincang yang sama.

Bitcoin menerapkan SHA-256 dua kali (SHA-256d) untuk keselamatan tambahan terhadap serangan peluasan panjang. Ethereum menggunakan Keccak-256, sebuah varian finalis SHA-3.

### Pepohon Merkle

Pepohon Merkle ialah pepohon binari cincang. Setiap nod daun ialah cincang sesuatu transaksi. Setiap nod dalaman ialah cincang dua anaknya. Akar — akar Merkle — meringkaskan semua transaksi dalam blok menjadi satu nilai 32-bait tunggal yang disimpan dalam pengepala blok.

Akibat praktikalnya: untuk mengesahkan bahawa transaksi tertentu disertakan dalam sesuatu blok, anda hanya memerlukan `log₂(n)` cincang, bukan semua `n` transaksi. Bagi blok dengan 2,000 transaksi, pengesahan memerlukan 11 cincang dan bukan 2,000 — asas bagi Pengesahan Pembayaran Dipermudah (SPV) dalam klien ringan.

### Tandatangan Digital (ECDSA)

Kebenaran transaksi dalam Bitcoin dan Ethereum menggunakan Algoritma Tandatangan Digital Lengkung Eliptik (ECDSA) atas lengkung secp256k1. Kunci persendirian menandatangani transaksi; mana-mana nod boleh mengesahkan tandatangan menggunakan kunci awam yang sepadan tanpa mengetahui kunci persendirian. Ini memastikan bahawa hanya pemegang kunci persendirian yang boleh membenarkan perbelanjaan daripada sesuatu alamat.

Alamat Ethereum ialah 20 bait terakhir daripada cincang Keccak-256 kunci awam — satu terbitan yang menjadikan alamat padat dan mudah alih sambil kekal terikat secara kriptografi kepada pasangan kunci.

## Cara Blockchain Bitcoin Berfungsi

Sesuatu blok Bitcoin mengandungi tiga komponen logik:

**Pengepala blok** — 80 bait yang terdiri daripada: versi protokol, cincang pengepala blok sebelumnya, akar Merkle transaksi, cap waktu Unix, sasaran kesukaran semasa, dan nonce. Pelombong melelar nonce (dan kadangkala cap waktu atau nonce-tambahan dalam transaksi coinbase) sehingga cincang dua-SHA-256 pengepala jatuh di bawah sasaran kesukaran.

**Senarai transaksi** — set tertib transaksi yang disertakan dalam blok. Transaksi coinbase (yang pertama) memperuntukkan ganjaran blok dan yuran transaksi kepada alamat pelombong.

**Rantaian** — pemautan pengepala. Bukti-kerja terkumpul dalam rantaian (jumlah semua kerja yang dilakukan untuk menghasilkan setiap blok) menentukan cabang mana yang menjadi rantaian kanonik. Nod sentiasa mengikuti rantaian dengan kerja terkumpul terbanyak.

Masa blok disasarkan pada 10 minit untuk Bitcoin. Kesukaran diselaraskan setiap 2,016 blok (kira-kira dua minggu) untuk mengekalkan sasaran tersebut apabila jumlah kadar cincang rangkaian berubah.

## Lapisan Boleh Atur Cara Ethereum

Ethereum menyamaratakan model transaksi Bitcoin daripada "pindah nilai" kepada "laksana kod." Penambahan utama:

**Mesin Maya Ethereum (EVM).** Sebuah mesin maya berasaskan tindanan, perkataan 256-bit, yang dilaksanakan secara berketentuan pada semua nod penuh. Setiap opcode mempunyai kos gas yang eksplisit. Pengiraan dibatasi oleh had gas blok, menghalang gelung tak terhingga daripada menghentikan rangkaian. Semua nod yang melaksanakan bytecode yang sama pada keadaan yang sama mesti menghasilkan output yang sama — konsensus atas pelaksanaan inilah yang menjadikan kontrak pintar tanpa perlu kepercayaan.

**Akaun.** Ethereum mempunyai dua jenis akaun: Akaun Milik Luaran (EOA) yang dikawal oleh kunci persendirian, dan Akaun Kontrak yang kodnya disimpan atas-rantaian. Transaksi yang dihantar ke alamat kontrak mencetuskan pelaksanaan bytecode kontrak tersebut.

**Keadaan.** Keadaan global Ethereum ialah pemetaan alamat kepada keadaan akaun (nonce, baki, storan, cincang kod). Akar keadaan — sebuah trai Merkle Patricia bagi semua keadaan akaun — disertakan dalam setiap pengepala blok, membolehkan bukti cekap bagi keadaan mana-mana akaun pada mana-mana ketinggian blok.

**Gas.** Pengguna membayar gas (dalam ETH) untuk setiap operasi EVM. Gas mempunyai dua fungsi: ia memberi pampasan kepada pelombong/pengesah bagi pengiraan, dan ia menghadkan sumber yang boleh digunakan oleh mana-mana transaksi tunggal, menghalang serangan penafian-perkhidmatan melalui operasi yang mahal.

## Menulis Kontrak Pintar dalam Solidity

Solidity ialah bahasa berorientasikan kontrak yang bertaip secara statik, yang mengkompil kepada bytecode EVM. Sebuah kontrak token minimum menggambarkan konsep terasnya:

```solidity
pragma solidity ^0.8.0;

contract MyToken {
    string public name;
    string public symbol;
    uint8 public decimals;
    uint256 public totalSupply;
    mapping(address => uint256) public balanceOf;

    event Transfer(address indexed from, address indexed to, uint256 value);

    constructor(
        string memory _name,
        string memory _symbol,
        uint8 _decimals,
        uint256 _totalSupply
    ) {
        name = _name;
        symbol = _symbol;
        decimals = _decimals;
        totalSupply = _totalSupply;
        balanceOf[msg.sender] = _totalSupply;
    }

    function transfer(address _to, uint256 _value) external returns (bool) {
        require(balanceOf[msg.sender] >= _value, "Insufficient balance");
        balanceOf[msg.sender] -= _value;
        balanceOf[_to] += _value;
        emit Transfer(msg.sender, _to, _value);
        return true;
    }
}
```

Pemerhatian utama: `mapping(address => uint256)` ialah susun atur storan EVM, bukan struktur data dalam-ingatan — bacaan dan penulisan mengenakan kos gas. `require` memansuhkan keseluruhan transaksi apabila gagal, mengembalikan gas yang tidak digunakan. `event Transfer` memancarkan log yang digunakan oleh pengindeks luar-rantaian untuk menjejaki pemindahan tanpa membaca semula keseluruhan keadaan. `constructor` berjalan sekali sahaja semasa penggunaan; panggilan berikutnya pergi ke fungsi yang dinamakan.

Piawaian ERC-20 memformalkan antara muka biasa untuk token boleh tukar ganti — `transfer`, `transferFrom`, `approve`, `allowance`, `balanceOf`, `totalSupply` — membolehkan mana-mana token yang mematuhi ERC-20 berfungsi dengan mana-mana pertukaran atau dompet yang sedar ERC-20 tanpa integrasi tersuai.

## Daripada Lejar kepada Infrastruktur Kewangan

Primitif blockchain yang diterangkan di sini — rantaian cincang, pepohon Merkle, EVM, dan ERC-20 — menjadi asas bagi set aplikasi kewangan yang lebih luas antara 2018 dan 2026:

**Kewangan Terdesentralisasi (DeFi).** Protokol pinjaman (Compound, Aave), pembuat pasaran automatik (Uniswap), dan pengagregat hasil semuanya berjalan sebagai kontrak pintar EVM. Ia menggantikan fungsi penjelasan, jagaan, dan penyelesaian perantara kewangan tradisional dengan kod yang melaksanakan dirinya sendiri dan kolam kecairan atas-rantaian.

**Aset Ditokenkan.** Bank pusat dan bank perdagangan sedang menguji coba deposit ditokenkan, bon ditokenkan, dan dana pasaran wang ditokenkan pada varian berkebenaran rantaian serasi-EVM. Mekanik asasnya — peralihan keadaan yang dilindungi cincang, penyelesaian atomik, peraturan pemindahan boleh atur cara — ialah keturunan langsung seni bina Ethereum 2014.

**Mata Wang Digital Bank Pusat.** Penyelidikan CBDC borong Bank of England, program euro digital ECB, dan Project Agorá semuanya meneroka seni bina DLT yang diterbitkan daripada atau serasi dengan reka bentuk asas dalam Bitcoin dan Ethereum. Struktur konsensus dan rantaian cincang kekal relevan walaupun apabila model kebenaran dan tadbir urus berbeza sepenuhnya daripada blockchain awam.

Perjalanan daripada kertas putih Bitcoin 2008 kepada kewangan ditokenkan 2026 merentangi dua dekad, tetapi ia berjalan di atas keturunan teknikal yang koheren. Memahami cara rantaian cincang SHA-256 menguatkuasakan ketakbolehubahan, cara pepohon Merkle membolehkan pengesahan cekap, dan cara EVM melaksanakan kontrak pintar secara atomik ialah prasyarat untuk menilai sebarang dakwaan tentang apa yang boleh dan tidak boleh dilakukan oleh blockchain dalam perkhidmatan kewangan yang dikawal selia.

## Soalan Lazim

**Apakah perbezaan antara blockchain dan pangkalan data teragih?**

Pangkalan data teragih tradisional mereplikasi data merentas nod untuk ketersediaan dan prestasi, tetapi kepercayaan adalah berpusat — pentadbir boleh mengubah suai rekod. Blockchain menjadikan pemalsuan mahal dari segi pengiraan melalui perantaian cincang dan konsensus: mengubah suai mana-mana rekod bersejarah memerlukan pengulangan semula semua bukti-kerja atau bukti-pertaruhan berikutnya, dan meyakinkan rangkaian untuk menerima cabang yang diubah. Sifat yang membezakannya ialah bukti-usik yang dikuatkuasakan oleh kriptografi dan reka bentuk insentif dan bukannya oleh kawalan capaian.

**Mengapa Ethereum menggunakan Keccak-256 dan bukan SHA-256?**

Ethereum menerima pakai Keccak-256 (finalis SHA-3 sebelum penyesuaian pemiawaian NIST) sebahagiannya kerana pereka bentuknya mahukan kebebasan daripada keturunan SHA-2 yang telah pun dibergantungkan oleh Bitcoin. Keccak juga mempunyai sifat aljabar berbeza yang menjadikannya menarik untuk operasi EVM tertentu. Kesan praktikal bagi pembangun ialah terbitan alamat Ethereum dan pencincangan slot storan menggunakan Keccak-256, bukan SHA-256d seperti dalam Bitcoin.

**Apakah yang dihalang oleh "gas" dalam EVM?**

Gas menghalang dua kategori serangan. Pertama, ia menghalang penafian-perkhidmatan melalui operasi yang mahal dari segi pengiraan: setiap opcode mengenakan kos gas, jadi penyerang tidak boleh memaksa rangkaian melaksanakan gelung tak terhingga tanpa kos. Kedua, had gas blok menghadkan jumlah pengiraan setiap blok, memastikan masa pengesahan blok kekal terbatas dan boleh diramal bagi nod penuh. Tanpa gas, satu panggilan kontrak tunggal boleh menghentikan rangkaian dengan melaksanakan pengiraan tak terbatas.

**Bagaimana bukti-pertaruhan mengubah model keselamatan berbanding bukti-kerja?**

Dalam bukti-kerja, keselamatan disediakan oleh perbelanjaan tenaga: menyerang rantaian memerlukan kawalan lebih daripada 50% kadar cincang rangkaian, yang bermakna mengawal lebih daripada 50% perkakasan fizikal dan kuasanya. Dalam bukti-pertaruhan (digunakan oleh Ethereum sejak Penggabungan pada 2022), keselamatan disediakan oleh pertaruhan ekonomi: pengesah mengunci ETH sebagai cagaran, yang dipotong jika mereka menandatangani blok yang bercanggah. Serangan 51% memerlukan pemerolehan dan pertaruhan lebih daripada 50% semua ETH yang dipertaruhkan — satu kos modal dan bukan kos perkakasan dan tenaga. Model keselamatan adalah berbeza tetapi setara secara matematik dari segi ekonomi dengan andaian bahawa pengesah rasional lebih menyukai pendapatan yuran daripada pemusnahan modal.

## Rujukan

- Nakamoto, S., (2008). [Bitcoin: A Peer-to-Peer Electronic Cash System ⧉](https://bitcoin.org/bitcoin.pdf "Bitcoin Whitepaper").
- Buterin, V., (2014). [Ethereum: A Next-Generation Smart Contract and Decentralised Application Platform ⧉](https://ethereum.org/whitepaper "Ethereum Whitepaper").
- Wood, G., (2014). [Ethereum: A Secure Decentralised Generalised Transaction Ledger ⧉](https://ethereum.github.io/yellowpaper/paper.pdf "Ethereum Yellow Paper").
- NIST, (2015). [SHA-3 Standard: Permutation-Based Hash and Extendable-Output Functions ⧉](https://www.nist.gov/publications/sha-3-standard-permutation-based-hash-and-extendable-output-functions "NIST FIPS 202").
