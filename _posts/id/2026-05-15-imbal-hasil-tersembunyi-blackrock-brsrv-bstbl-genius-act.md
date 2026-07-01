---
title: "Imbal Hasil Stablecoin dengan Nama Lain: Membaca Filing BRSRV dan BSTBL BlackRock"
subtitle: "Stablecoin tidak dapat membayar yield di bawah GENIUS Act. Pada 8 Mei 2026, BlackRock mengajukan dua produk yang secara hukum bukan stablecoin, tetapi dapat membayar yield di wallet pada blockchain publik."
description: "Stablecoin tidak dapat membayar yield di bawah GENIUS Act. Filing BRSRV dan BSTBL BlackRock menunjukkan cara yield on-chain berpindah ke tokenised money market funds."
date: "May 15, 2026"
language: "id-ID"
locale: "id_ID"
banner: "https://cloudcdn.pro/stocks/images/alev-takil-7ojyp-IXW7w-unsplash.webp"
banner_alt: "Diagram arsitektur money market fund tokenised BlackRock, BRSRV OnChain Shares dan share class ERC-20 BSTBL dengan alur cadangan GENIUS Act"
keywords: "BlackRock, BRSRV, BSTBL, BUIDL, GENIUS Act, OCC, stablecoin, tokenised money market fund, OnChain Shares, Securitize"
---

![Diagram arsitektur money market fund tokenised BlackRock, BRSRV OnChain Shares dan share class ERC-20 BSTBL dengan alur cadangan GENIUS Act](https://cloudcdn.pro/stocks/images/alev-takil-7ojyp-IXW7w-unsplash.webp).class=\"img-fluid clearfix\"

Stablecoin tidak dapat membayar yield di bawah GENIUS Act. Pada 8 Mei 2026, BlackRock mengajukan dua registration statement SEC untuk produk yang menyelesaikan batasan ini dengan diatur sebagai money market funds, bukan stablecoin, sambil berperilaku di wallet seperti dolar ber-yield di blockchain publik.

---

> **Kesimpulan utama**
>
> - **GENIUS Act**, ditandatangani pada Juli 2025 dan kini berada di bulan-bulan akhir rulemaking, melarang penerbit payment stablecoin membayar bunga atau yield kepada holder hanya karena memegang, memakai, atau menyimpan stablecoin. Proposal OCC Maret 2026 memperketat ini dengan rebuttable presumption bahwa pengaturan yield melalui affiliate dan pihak ketiga juga melanggar larangan tersebut.
> - Masalah ekonominya sederhana. Dengan sekitar **$281 miliar payment stablecoins beredar** dan Treasury yields pada level tertinggi multi-tahun, jarak antara yang diterima wallet holder, nol, dan yang dihasilkan cadangan mendasar, sekitar 4-5%, kini bernilai puluhan miliar dolar per tahun.
> - Pada **8 Mei 2026, BlackRock mengajukan dua SEC registration statements** yang menangkap gap ini tanpa melanggar larangan yield, karena tidak satu pun produk itu secara hukum adalah stablecoin.
> - **BRSRV** (BlackRock Daily Reinvestment Stablecoin Reserve Vehicle) adalah money market fund baru yang memegang cash, Treasuries berjatuh tempo di bawah 93 hari, dan overnight Treasury repos. Ia menerbitkan "OnChain Shares" melalui permissioned multi-chain framework dengan Securitize Transfer Agent LLC sebagai legal record of ownership. Investasi minimum: $3 juta. Produk ini direkayasa untuk memenuhi syarat sebagai eligible reserve asset di bawah GENIUS Act.
> - **BSTBL** adalah filing yang lebih penting secara arsitektural. Ia memasang share class ERC-20 pada **Select Treasury Based Liquidity Fund** BlackRock yang sudah ada, bernilai $6-7 miliar, dengan BNY Mellon Investment Servicing sebagai transfer agent, mencatat shareholder di Ethereum. Ini pertama kalinya share class public-Ethereum ditambahkan ke produk money-market BlackRock yang sudah ada.
> - Polanya kini terlihat di seluruh industri. **Tokenised money market funds adalah arsitektur yang dibuat tak terhindarkan oleh GENIUS Act ketika melarang yield pada stablecoins.** Pasar tokenised Treasury senilai $14 miliar, dipimpin BUIDL BlackRock dengan pangsa sekitar 40%, adalah pembacaan awal tentang tempat gelombang "wallet dollars" berikutnya berada.

---

## Filing yang Juga Merupakan Posisi Kebijakan

Dua filing BlackRock pada 8 Mei 2026 tidak datang dalam ruang hampa. Filing itu tiba satu minggu setelah BlackRock mengirim [comment letter tujuh belas halaman ⧉](https://www.theblock.co/post/399812/blackrock-urges-occ-to-drop-tokenized-reserve-cap-idea-expand-eligible-assets-in-genius-act-comment-letter "BlackRock urges OCC to drop tokenized reserve cap idea, expand eligible assets in GENIUS Act comment letter") kepada Office of the Comptroller of the Currency pada hari terakhir comment window untuk implementing rules GENIUS Act, dan empat hari setelah [BlackRock menerbitkan ringkasan publik di X ⧉](https://beincrypto.com/blackrock-occ-stablecoin-genius-act-comment/ "BlackRock Backs OCC Stablecoin Rules Under GENIUS Act") tentang tujuh rekomendasi intinya kepada lembaga tersebut.

Rekomendasi dan filing baru ini paling tepat dibaca sebagai satu dokumen dalam dua bagian. Comment letter berargumen bahwa OCC harus membatalkan usulan cap 20% atas tokenised reserve assets, menegaskan ETF yang memenuhi syarat mendapat perlakuan yang sama dengan government money market funds, dan mengizinkan same-day-settling GMMFs dihitung ke weekly liquidity floor. Filing empat hari kemudian mendaftarkan instrumen persis yang diuntungkan oleh posisi itu: fund baru, BRSRV, yang secara eksplisit direkayasa agar memenuhi syarat sebagai eligible reserve di bawah GENIUS Act, dan share class tokenised, BSTBL, di atas Treasury liquidity fund BlackRock yang sudah ada senilai $6-7 miliar. Apakah OCC mengadopsi posisi BlackRock dalam final rule atau tidak, perusahaan kini menempatkan produknya dalam debat kebijakan dengan spesifisitas yang sulit diabaikan regulator.

Inilah latar strategis untuk sesuatu yang pada bacaan pertama tampak seperti rekayasa hukum cerdas. Lebih akuratnya, ini adalah asset manager terbesar di dunia yang menyatakan di mana garis antara "stablecoin" dan "tokenised security" seharusnya berada dalam hukum AS, lalu mendaftarkan produk yang akan hidup di kedua sisi garis itu.

## Mengapa Stablecoin Tidak Dapat Membayar Yield

GENIUS Act, ditandatangani pada Juli 2025 dan kini menjadi dasar rulemaking OCC, FDIC, dan Federal Reserve yang tumpang tindih, menggambar pembedaan konseptual yang bersih. "Payment stablecoin" di bawah Act adalah digital asset yang dirancang mempertahankan nilai stabil terhadap fiat currency, didukung cadangan berkualitas tinggi, dan dapat ditebus pada par. "Permitted payment stablecoin issuer" (PPSI) adalah entitas berpiagam federal atau negara bagian yang diotorisasi menerbitkan token tersebut. Dan [section 4(a)(11) Act ⧉](https://www.lw.com/en/insights/occ-issues-proposal-to-implement-the-genius-act "OCC Issues Proposal to Implement the GENIUS Act") melarang PPSI membayar bunga atau yield kepada holder semata-mata karena memegang, menggunakan, atau menyimpan stablecoin.

[Proposed rule OCC Maret 2026 ⧉](https://www.nixonpeabody.com/insights/alerts/2026/04/02/proposed-occ-regulations-for-payment-stablecoins-under-the-genius-act "Proposed OCC regulations for payment stablecoins under the GENIUS Act") memperluas larangan ini secara operasional. Ia menetapkan rebuttable presumption bahwa pengaturan yang menyalurkan yield melalui affiliate atau pihak ketiga terkait, misalnya crypto exchange yang membayar "loyalty rewards" kepada holder stablecoin tertentu, juga melanggar larangan, dengan beban pada issuer untuk membuktikan sebaliknya. White-label arrangements, ketika PPSI menerbitkan digital asset berbrand partner yang kemudian membayar yield, secara eksplisit diperlakukan sebagai presumptively evasive. Office of the Comptroller [memberi sinyal pada awal 2026 ⧉](https://www.compliancecorylated.com/news/us-occ-closes-genius-act-loophole-allowing-yield-bearing-stablecoins/ "US OCC closes GENIUS Act loophole allowing yield-bearing stablecoins") bahwa framing "loophole" untuk model issuer-pays-via-affiliate tidak akan bertahan dalam final rule yang permisif.

Rasional ekonomi untuk larangan ini diperdebatkan. Submisi industri perbankan ke OCC mendukung larangan ketat atas dasar bahwa stablecoin ber-yield akan menguras transactional bank deposits, pasar yang diperkirakan [US Treasury advisory council sekitar $6,6 triliun ⧉](https://www.congress.gov/crs-product/IF13174 "The Stablecoin Yield Debate — Congressional Research Service"), dengan bagian bermakna "at risk" dari kompetisi dollar-substitutes ber-yield. Submisi industri crypto, dipimpin Coinbase, berargumen sebaliknya: insentif adalah pusat kompetisi pembayaran, dan larangan luas akan menimbulkan net welfare costs tanpa dampak material pada bank lending.

Pihak mana pun yang memiliki argumen kebijakan lebih baik, hasil hukum untuk saat ini jelas: stablecoin dalam arti regulasi GENIUS Act tidak dapat membayar yield kepada holder-nya. Namun yang tidak dapat dilakukan Act adalah mendefinisikan apa yang dapat dilakukan holder dengan uangnya berikutnya. Di sinilah arsitekturnya bercabang.

## Arsitektur BRSRV

BlackRock Daily Reinvestment Stablecoin Reserve Vehicle, dalam plumbing-nya, adalah money market fund biasa. Ia memegang cash, US Treasury securities dengan maturitas 93 hari atau kurang, dan overnight repurchase agreements yang didukung Treasuries. Ia selaras dengan Rule 2a-7 di bawah Investment Company Act of 1940, arsitektur regulasi yang sama yang mengatur institutional money market funds selama empat dekade. Yield-nya, seperti government MMF lain, berasal dari short-Treasury rate yang berlaku.

Yang baru adalah share class-nya. Saham BRSRV diterbitkan sebagai ["OnChain Shares" melalui permissioned framework ⧉](https://unchainedcrypto.com/blackrock-files-for-two-new-tokenized-money-market-funds-targeting-stablecoin-capital/ "BlackRock Files for Two New Tokenized Money-Market Funds Targeting Stablecoin Capital") yang terhubung ke beberapa blockchain publik, dengan [Securitize Transfer Agent LLC menjadi official transfer agent ⧉](https://www.crowdfundinsider.com/2026/05/278346-blackrock-focuses-on-tokenization-initiatives-with-blockchain-enabled-funds/ "BlackRock Focuses On Tokenization Initiatives With Blockchain Enabled Funds"). Sistem identity off-chain, jenis infrastruktur KYC yang sama yang menopang fund [BUIDL ⧉](https://stablecoininsider.org/top-10-tokenized-treasury-funds-in-2026-buidl-benji-and-the-highest-yielding-on-chain-options/ "Top 10 Tokenized Treasury Funds in 2026") BlackRock senilai $2,9 miliar, menghubungkan wallet address ke investor terverifikasi. Investasi minimum: $3 juta. Filing belum menyebut blockchain mana yang akan didukung saat launch.

Produk ini secara eksplisit direkayasa, [seperti dicatat banyak sumber ⧉](https://cryptobriefing.com/blackrock-tokenized-money-market-funds-stablecoins/ "BlackRock doubles down on tokenization with new stablecoin reserve funds"), untuk memenuhi syarat sebagai eligible reserve asset di bawah GENIUS Act. Pembeli targetnya bukan retail wallet user. Ia adalah stablecoin issuer, atau treasury operation yang memegang stablecoins sebagai bagian strategi working-capital, yang membutuhkan instrumen ber-yield Treasury yang dapat dipegang secara programmatic di rails blockchain yang sama dengan stablecoin itu sendiri. Pitch sederhananya: pertahankan cadangan on chain, dapatkan Treasury yield, penuhi regulator.

Bagi BlackRock, posisi strategisnya lebih tajam daripada terlihat. Fund BUIDL yang sudah ada telah mendukung lebih dari 90% cadangan dua produk stablecoin-adjacent "yield-bearing" terbesar, USDtb milik Ethena dan JupUSD berbasis Solana milik Jupiter. BRSRV adalah ekstensi khusus yang sadar GENIUS terhadap peran itu: produk wholesale Treasury-yield yang dibangun khusus untuk workflow reserve-management setiap PPSI yang akan ada di rezim baru.

## Arsitektur BSTBL

Filing kedua lebih menarik secara operasional dan lebih penting secara arsitektural. BSTBL, share class on-chain untuk BlackRock Select Treasury Based Liquidity Fund yang sudah ada, bukan fund baru. Ia adalah share class baru yang dilapiskan pada money market product yang sudah mengelola sekitar $6-7 miliar aset, [diretool pada Oktober 2025 menjadi konfigurasi GENIUS-compliant ⧉](https://www.theblock.co/post/399812/blackrock-urges-occ-to-drop-tokenized-reserve-cap-idea-expand-eligible-assets-in-genius-act-comment-letter "BlackRock urges OCC to drop tokenized reserve cap idea") dengan deadline trading 5 p.m. ET dan mandat Treasury-heavy, lalu kini diperluas ke Ethereum sebagai token ERC-20.

Transfer agent untuk share class ini adalah [BNY Mellon Investment Servicing ⧉](https://www.mexc.com/news/1080472 "BlackRock files for two new tokenized funds with the U.S. SEC on Ethereum"), yang akan memelihara official shareholder records di Ethereum memakai standar ERC-20. Infrastruktur KYC off-chain menghubungkan wallet ke identity records investor, seperti pada BUIDL dan tokenised fund patuh lain di pasar hari ini. Perbedaan substantif dari BRSRV adalah chain, Ethereum publik dengan token ERC-20 sebagai representasi saham, dan transfer agent, BNY bukan Securitize, serta fakta bahwa ini pertama kalinya share class public-Ethereum dipasang pada money-market fund BlackRock yang sudah ada.

Detail terakhir itulah yang layak diperhatikan. Produk tokenised BlackRock sebelumnya, terutama BUIDL, disusun sebagai fund baru dengan arsitektur native on-chain. BSTBL mengambil pendekatan berbeda dan mungkin lebih konsekuensial: men-tokenise produk money market konvensional besar yang sudah ada dengan menambahkan share class baru, bukan membangun struktur paralel. Implikasinya adalah setiap MMF BlackRock yang sudah ada pada prinsipnya dapat mengikuti pola yang sama. Begitu pula MMF pesaing, Vanguard, Fidelity, JPMorgan, State Street. Hambatan arsitektural untuk men-tokenise industri conventional money market fund setelah BSTBL lebih rendah daripada sebelumnya.

Sebagai konteks industri: tokenised US Treasuries tumbuh dari sekitar $2 miliar menjadi [$14 miliar per Mei 2026 ⧉](https://www.mexc.com/news/1080472 "BlackRock files for two new tokenized funds with the U.S. SEC on Ethereum"), dengan BUIDL BlackRock sekitar 40% pangsa pasar, BENJI/FOBXX Franklin Templeton sebesar $850 juta, dan produk gabungan OUSG serta USDY Ondo Finance di posisi kedua. $50-100 miliar berikutnya sangat mungkin sudah bergerak melalui filing seperti BSTBL.

## Payment Stablecoin vs Tokenised Money Market Fund: Perbedaan yang Penting

Bagi pembaca non-spesialis, perbedaan antara "stablecoin" dan "tokenised money market fund share" dapat terlihat seperti teknis regulasi. Bukan. Kedua instrumen menempati posisi yang benar-benar berbeda dalam hukum sekuritas AS dan konsekuensinya mengalir ke seluruh desain produk.

| Dimension | Payment Stablecoin (under GENIUS Act) | Tokenised MMF Share (BRSRV / BSTBL pattern) |
|---|---|---|
| Legal status | Payment instrument | Security (fund share) |
| Governing regime | GENIUS Act; OCC/FDIC/Fed rulemakings | Investment Company Act 1940; Rule 2a-7 |
| Issuer | Permitted Payment Stablecoin Issuer (PPSI) | SEC-registered fund (and transfer agent) |
| Reserve requirements | Cash, short Treasuries, repos — strict | Cash, short Treasuries, repos — Rule 2a-7 |
| Can pay yield to holder | **No** (Section 4(a)(11)) | **Yes** (the yield is the return on the share) |
| Redemption | At par, on demand | At NAV, typically T+0 or T+1 |
| Record of ownership | Issuer wallet / on-chain | Transfer agent (legal); blockchain (operational) |
| Minimum investment | None (retail typical) | Substantial ($3M for BRSRV; institutional for BSTBL) |
| Composability with DeFi | High | High (BUIDL is precedent) |
| User experience in a wallet | Token that holds $1 | Token whose value accrues toward yield |
| Bank-deposit substitution risk | The central regulatory concern | Materially lower (security, not deposit-like) |

*Sumber: Sintesis teks GENIUS Act, OCC NPRM Maret 2026, filing BlackRock 8 Mei 2026, dan framework Rule 2a-7.*

Baris terakhir menjelaskan arsitektur regulasinya. Payment stablecoin yang membayar yield terlihat bagi regulator bank seperti pengganti deposito. Tokenised money market fund share yang membayar yield terlihat seperti sekuritas, dan sekuritas yang bersaing dengan deposito bukan kekhawatiran baru, karena money market funds konvensional telah melakukan hal itu selama empat puluh tahun. GENIUS Act menggambar garisnya pada kekhawatiran deposit-substitute. Semua yang jelas berada di sisi sekuritas dari garis itu, secara konstruksi, berada di luar larangan yield Act.

## Apakah Ini Loophole?

Menggoda, dan framing ini luas muncul di LinkedIn serta crypto-Twitter sejak filing, untuk menyebut ini "loophole" GENIUS Act: stablecoin tidak dapat membayar yield, jadi BlackRock mengajukan sesuatu yang secara hukum bukan stablecoin. Framing itu menangkap headline dengan cerdas. Sebagai karakterisasi hukum, ia mengecilkan substansi.

Larangan yield dalam GENIUS Act adalah pilihan kebijakan spesifik dengan target spesifik: risiko deposit-substitution bagi sektor perbankan dari kelas instrumen yang dirancang berfungsi sebagai uang. Tokenised money market funds tidak dirancang berfungsi sebagai uang; mereka dirancang berfungsi sebagai fund shares, dengan semua bobot regulasi, Rule 2a-7, audited reserves, NAV disclosure, dan legal records of ownership oleh transfer agent, yang telah berlaku pada kategori itu selama puluhan tahun. Bahwa fund shares itu kini settle di Ethereum atau chain publik lain tidak mengubah apa mereka dalam hukum sekuritas. [Proposed rule OCC ⧉](https://www.morganlewis.com/pubs/2026/04/occs-genius-act-proposal-what-prospective-issuers-need-to-know "Stablecoin Regulation: OCC Proposal Under the GENIUS Act") sendiri secara eksplisit mempertimbangkan tokenised reserves sebagai kategori sah; debat terbukanya adalah cap 20%, bukan keberadaan asset class.

Yang benar-benar baru adalah user experience. Holder tokenised MMF share, di wallet pada public chain, memiliki sesuatu yang *terlihat* seperti stablecoin, token fungible, transferable peer-to-peer, composable dengan infrastruktur DeFi, tetapi *berperilaku* seperti sekuritas, NAV bertambah, holder berada di daftar KYC, dan catatan transfer agent mengontrol secara hukum. Observasi yang lebih dalam adalah bahwa GENIUS Act, dengan melarang yield pada kategori payment-stablecoin, secara efektif *mengharuskan* industri berkumpul pada tokenised MMFs sebagai pembawa yield-bearing on-chain dollars. Act menggambar garis; industri, seperti dapat diprediksi, menyusun produk di sisi yang lebih menguntungkan dari garis itu. Itu bukan loophole. Itu desain arsitektur regulasi yang bekerja kurang lebih sesuai niat, walaupun kecepatannya menghasilkan produk institusional lebih tinggi daripada yang diperkirakan banyak pihak.

## Artinya bagi Tiap Sektor

Implikasi filing 8 Mei tidak seragam. Respons strategis berbeda tergantung posisi institusi dalam value chain.

### Stablecoin Issuers (PPSIs)

Bagi Circle, Tether, PayPal, dan generasi berikutnya bank-issued payment stablecoins, BRSRV adalah jawaban operasional untuk pertanyaan yang sampai sekarang hanya punya jawaban ad hoc: di mana cadangan ditempatkan ketika harus sekaligus ber-yield Treasury dan native di chain yang sama dengan stablecoin yang diterbitkan? Memegang T-bills langsung bekerja pada skala penerbitan tetapi berat secara operasional. Memegang BUIDL bekerja, tetapi struktur BUIDL tidak dirancang khusus di sekitar framework cadangan GENIUS Act. BRSRV dirancang untuk itu.

### Bank dan Money Market Fund Operators

Bagi bank yang mengoperasikan franchise money market fund besar, JPMorgan, State Street, BNY Mellon, Northern Trust, Vanguard, Fidelity, BSTBL adalah template operasional untuk apa yang kemungkinan perlu dilakukan produk mereka sendiri. Pola arsitekturnya kini terlihat: ambil MMF yang sudah ada, daftarkan share class on-chain baru ke SEC, tunjuk transfer agent untuk memelihara shareholder records di Ethereum atau chain publik besar lain, dan gate akses melalui KYC off-chain. Hambatan masuk untuk share class tokenised pada MMF $10-50 miliar yang sudah ada, dalam pola BSTBL, terutama regulasi dan operasional, bukan teknis.

### DeFi Protocols dan On-Chain Treasury

Bagi DeFi protocols, BRSRV dan BSTBL memperluas pola yang dimulai BUIDL: migrasi high-quality Treasury collateral dari akun kustodian off-chain ke instrumen on-chain yang dapat dikomposisikan dengan lending, derivatives, dan structured products. USDtb Ethena dan JupUSD Jupiter adalah contoh early mover; ruang desain di belakangnya kini jauh lebih besar. Pertimbangan risikonya tidak sepele: instrumen dasar bersifat KYC-gated dan permissioned, yang membatasi derajat komposisi "permissionless" yang dapat diandalkan sistem DeFi-native.

### Regulator

Bagi OCC, FDIC, dan Federal Reserve, filing 8 Mei memperjelas apa yang diminta regulatory perimeter untuk akomodasi. Larangan yield dalam GENIUS Act jelas tidak menghentikan yield on-chain mencapai wallet holders; ia memigrasikan arsitektur delivery yield dari kategori payment-stablecoin, yang diawasi langsung regulator tersebut, ke kategori registered-fund, yang diawasi SEC. Ini tidak harus buruk, registered funds adalah kategori regulasi yang dipahami baik, tetapi berarti pertanyaan koordinasi lintas lembaga menjadi lebih tajam secara operasional. Final rule OCC, jatuh tempo Januari 2027, akan menentukan apakah cap 20% tokenised reserves bertahan dalam bentuk apa pun, dan apakah garis antara payment stablecoin dan tokenised MMF share dipertahankan pada level issuer atau dibiarkan semakin kabur pada level wallet.

## Kesimpulan

Filing 8 Mei 2026 bukan, sendirian, perubahan paradigma. Ia adalah produk individual dari satu asset manager, diajukan dalam jendela regulasi spesifik yang dibuka rulemaking OCC. Namun filing itu menangkap bentuk transisi tingkat industri yang sudah terlihat sejak BlackRock meluncurkan BUIDL pada Maret 2024 dan kini dipercepat, bukan dibatasi, oleh GENIUS Act.

Stablecoin, dalam arti GENIUS Act, akan terus melakukan hal yang sejak awal mereka kuasai: settlement efisien, pembayaran lintas batas hampir instan, programmable money untuk use case yang membutuhkan unit akun stabil. Mereka tidak akan, di bawah aturan saat ini dan usulan aturan, membayar yield kepada holder. Dolar ber-yield di wallet, produk yang mengambil form factor sama seperti stablecoin tetapi mengakumulasi Treasury yield untuk holder, akan berupa tokenised money market fund share, diterbitkan oleh registered fund, dengan transfer agent, Securitize, BNY Mellon, dan kemungkinan beberapa lainnya, sebagai legal record of ownership. BRSRV dan BSTBL adalah ekspresi institusional awal dari pola itu. Keduanya bukan yang terakhir.

Untuk konteks sebelumnya di situs ini, artikel [Januari 2018 tentang technology stack Ethereum ⧉](https://sebastienrousseau.com/2018-01-09-understanding-the-technology-behind-blockchain/index.html "Understanding the Technology behind Blockchain") membahas substrat tempat BSTBL kini berada, artikel [Januari 2018 tentang standar ERC-20 ⧉](https://sebastienrousseau.com/2018-01-24-the-erc-20-token-standard/index.html "ERC-20: The Ethereum Token Interface That Changed the World") membahas representasi share-class yang dipilih BlackRock, analisis [Februari 2018 tentang faster-payment cryptocurrencies ⧉](https://sebastienrousseau.com/2018-02-04-unveiling-a-new-cryptocurrency-and-offering-future-faster-payment-solution/index.html "Unveiling a New Cryptocurrency and Faster Payment Solution") membahas masalah user experience yang kini sebagian dipecahkan instrumen on-chain ber-yield, dan [artikel terbaru tentang tenggat structured-address SWIFT CBPR+](https://sebastienrousseau.com/2026-05-12-iso-20022-pacs008-structured-address-deadline/index.html "The November 2026 pacs.008 Structured-Address Deadline") berada berdampingan dalam percakapan modernisasi pembayaran yang lebih luas. Intinya bukan menyatakan satu arsitektur telah menang. Intinya adalah bahwa sistem keuangan institusional dan on-chain pada 2026 berkumpul pada primitive bersama lebih cepat daripada yang diperkirakan keduanya setahun lalu.

## Pertanyaan yang Sering Diajukan

**Apa perbedaan nyata antara BRSRV/BSTBL dan stablecoin seperti USDC?**

Di wallet, perbedaannya hampir tidak terlihat. Masing-masing token fungible pada blockchain publik, dapat ditebus untuk dolar atau nilai fund share, dan composable dengan DeFi. Dalam hukum, perbedaannya besar. USDC adalah payment stablecoin di bawah GENIUS Act, diterbitkan oleh Permitted Payment Stablecoin Issuer, dan dilarang membayar yield kepada holder. BRSRV dan BSTBL adalah share class dari registered money market funds di bawah Investment Company Act of 1940, diatur oleh Rule 2a-7, dengan yield sebagai return alami atas share. Holder BRSRV secara hukum adalah shareholder fund. Holder USDC secara hukum adalah holder payment instrument.

**Mengapa BSTBL berbeda dari BUIDL jika keduanya tokenised BlackRock funds di Ethereum?**

BUIDL, diluncurkan pada Maret 2024, disusun sebagai fund baru dengan arsitektur on-chain sejak awal, dengan Securitize sebagai partner dan desain native untuk digital-asset workflow. BSTBL sebaliknya adalah share class on-chain baru yang ditambahkan ke conventional money market fund yang sudah ada senilai $6-7 miliar, yaitu Select Treasury Based Liquidity Fund. BNY Mellon menjadi transfer agent. Signifikansi arsitekturalnya adalah BSTBL menunjukkan cara membawa produk money-market tradisional yang besar ke on-chain tanpa membangunnya ulang sebagai fund baru. Template itu, jika berhasil, portable ke MMF konvensional mana pun di industri.

**Mengapa cap 20% OCC atas tokenised reserves kontroversial?**

Proposal OCC Maret 2026 mengapungkan batas potensial 20% atas seberapa banyak cadangan stablecoin issuer boleh dipegang dalam bentuk tokenised. Comment letter BlackRock berargumen bahwa ini "extraneous" terhadap tujuan supervisory OCC, karena profil risiko reserve asset ditentukan oleh credit quality, duration, dan liquidity, bukan oleh apakah asset itu dipegang atau ditransfer di distributed ledger. Secara operasional, cap itu akan membatasi peran BUIDL sebagai cadangan utama produk seperti USDtb Ethena dan JupUSD Jupiter. Final rule OCC pada Januari 2027 akan menentukan apakah cap bertahan, dinaikkan, atau dibatalkan.

**Apa artinya filing BRSRV belum menyebut blockchain yang akan didukung?**

Itu fitur rutin filing tahap awal SEC, bukan ambiguitas strategis. Filing menetapkan struktur hukum, registered fund yang menerbitkan OnChain Shares melalui permissioned framework dengan Securitize sebagai transfer agent, tanpa berkomitmen ke chain tertentu. BlackRock kemungkinan mengumumkan chain mendekati launch. BUIDL sendiri diluncurkan di Ethereum lalu diperluas ke Polygon, Avalanche, Optimism, Aptos, dan Arbitrum; BRSRV kemungkinan mengikuti pola multi-chain serupa mengingat rujukan eksplisit pada "multiple public blockchains".

**Apakah ini akhir yield-bearing stablecoins sebagai kategori produk?**

Ini akhir yield-bearing payment stablecoins sebagai kategori, setidaknya di bawah hukum federal AS, kecuali Kongres mengubah GENIUS Act. Ini bukan akhir yield-bearing on-chain dollars sebagai kategori produk, yang sebenarnya diinginkan pengguna. Kategori itu kini bermigrasi ke tokenised money market fund shares, BUIDL, BENJI, BRSRV, BSTBL, produk Ondo, dan gelombang MMF tokenised pesaing yang kemungkinan dikatalisis pola BSTBL. Instrumennya akan terlihat sedikit berbeda di wallet, nilai token merefleksikan akumulasi yield alih-alih bertahan datar pada $1,00, tetapi fungsi ekonominya, exposure setara dolar dengan Treasury yield yang settle di public chain, dipertahankan melalui jalur regulasi berbeda.

## Referensi

- Sebastien Rousseau, (2026). [The November 2026 pacs.008 Structured-Address Deadline: A Six-Month View](https://sebastienrousseau.com/2026-05-12-iso-20022-pacs008-structured-address-deadline/index.html "The November 2026 pacs.008 Structured-Address Deadline").
- Sebastien Rousseau, (2018). [ERC-20: The Ethereum Token Interface That Changed the World](https://sebastienrousseau.com/2018-01-24-the-erc-20-token-standard/index.html "ERC-20: The Ethereum Token Interface That Changed the World").
- Sebastien Rousseau, (2018). [Understanding the Technology behind Blockchain](https://sebastienrousseau.com/2018-01-09-understanding-the-technology-behind-blockchain/index.html "Understanding the Technology behind Blockchain").
- Sebastien Rousseau, (2018). [Unveiling a New Cryptocurrency and Faster Payment Solution](https://sebastienrousseau.com/2018-02-04-unveiling-a-new-cryptocurrency-and-offering-future-faster-payment-solution/index.html "Unveiling a New Cryptocurrency and Faster Payment Solution").
- Unchained, (2026). [BlackRock Files for Two New Tokenized Money-Market Funds Targeting Stablecoin Capital ⧉](https://unchainedcrypto.com/blackrock-files-for-two-new-tokenized-money-market-funds-targeting-stablecoin-capital/ "BlackRock Files for Two New Tokenized Money-Market Funds Targeting Stablecoin Capital"). Unchained.
- The Block, (2026). [BlackRock urges OCC to drop tokenized reserve cap idea, expand eligible assets in GENIUS Act comment letter ⧉](https://www.theblock.co/post/399812/blackrock-urges-occ-to-drop-tokenized-reserve-cap-idea-expand-eligible-assets-in-genius-act-comment-letter "BlackRock urges OCC to drop tokenized reserve cap idea"). The Block.
- BeInCrypto, (2026). [BlackRock Backs OCC Stablecoin Rules Under GENIUS Act ⧉](https://beincrypto.com/blackrock-occ-stablecoin-genius-act-comment/ "BlackRock Backs OCC Stablecoin Rules Under GENIUS Act"). BeInCrypto.
- Latham & Watkins, (2026). [OCC Issues Proposal to Implement the GENIUS Act ⧉](https://www.lw.com/en/insights/occ-issues-proposal-to-implement-the-genius-act "OCC Issues Proposal to Implement the GENIUS Act"). Latham & Watkins.
- Nixon Peabody, (2026). [Proposed OCC Regulations for Payment Stablecoins Under the GENIUS Act ⧉](https://www.nixonpeabody.com/insights/alerts/2026/04/02/proposed-occ-regulations-for-payment-stablecoins-under-the-genius-act "Proposed OCC regulations for payment stablecoins under the GENIUS Act"). Nixon Peabody LLP.
- Morgan Lewis, (2026). [Stablecoin Regulation: OCC Proposal Under the GENIUS Act ⧉](https://www.morganlewis.com/pubs/2026/04/occs-genius-act-proposal-what-prospective-issuers-need-to-know "Stablecoin Regulation: OCC Proposal Under the GENIUS Act"). Morgan Lewis.
- Congressional Research Service, (2026). [The Stablecoin Yield Debate ⧉](https://www.congress.gov/crs-product/IF13174 "The Stablecoin Yield Debate"). Congress.gov.
- MEXC News, (2026). [BlackRock files for two new tokenized funds with the U.S. SEC on Ethereum ⧉](https://www.mexc.com/news/1080472 "BlackRock files for two new tokenized funds with the U.S. SEC on Ethereum"). MEXC News.
