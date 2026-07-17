---
title: "Daripada Pain.001 kepada Kecairan Boleh Program: ISO 20022 sebagai Sistem Saraf Autonomik Perbendaharaan pada 2026"
tags: "ISO 20022, pain.001, pacs.008, MX, SWIFT, CBPR+, programmable liquidity, autonomous treasury, BIS, structured addresses, DORA, agentic AI, cross-border payments, CIB"
subtitle: "ISO 20022 pada 2026 bukan lagi projek migrasi. Ia ialah substrat data di sebalik kecairan boleh program, perbendaharaan agentik, dan peralihan SWIFT MT/MX November 2026 yang hampir separuh daripada bank dunia masih ketinggalan untuk memenuhinya."
description: "ISO 20022 pain.001 dan pacs.008 pada 2026 - bagaimana API perbendaharaan asli MX, alamat berstruktur, dan kecairan boleh program membina semula sistem saraf autonomik perbendaharaan CIB."
date: "June 23, 2026"
language: "ms"
locale: "ms_MY"
banner: "https://cloudcdn.pro/stocks/images/markus-spiske-FXFz-sW0uwo.webp"
banner_alt: "Arteri keluli sebuah pusat penjelasan moden ketika subuh - melambangkan ISO 20022 pain.001 dan pacs.008 sebagai sistem saraf autonomik yang membawa kecairan boleh program merentasi perbendaharaan global, SWIFT MX, dan rel CBPR+"
keywords: "ISO 20022, pain.001, pacs.008, MX, SWIFT, CBPR+, kecairan boleh program, perbendaharaan autonomi, BIS CPMI, alamat berstruktur, DORA, AI agentik, pembayaran rentas sempadan, CIB, MT103, MT202, RTGS, Basel III, SR 11-7, API perbendaharaan"
---

## Daripada Pain.001 kepada Kecairan Boleh Program: ISO 20022 sebagai Sistem Saraf Autonomik Perbendaharaan pada 2026

> **Ringkasan Eksekutif.** Lima bulan sebelum peralihan SWIFT MT/MX pada 22 November 2026, [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) telah berhenti menjadi projek migrasi dan menjadi substrat data untuk perbendaharaan Perbankan Korporat dan Pelaburan. 44% daripada bank yang dilaporkan ketinggalan oleh tinjauan kesediaan RedCompass Labs bukan sekadar tertinggal dalam pertukaran format wayar; mereka tertinggal dalam kewajipan yang boleh dipertanggungjawabkan di peringkat lembaga untuk menyampaikan kod tujuan berstruktur, alamat `<PstlAdr>` berstruktur, dan data kiriman wang patuh CBPR+ ke dalam setiap pembayaran rentas sempadan yang mereka mulakan atau terima. Artikel ini membingkaikan pain.001 sebagai degupan jantung tindanan kecairan boleh program — bagaimana rupa skema kanonik mengutamakan ISO, kemasukan pengesahan-semasa-menghurai, dan satah kawalan yang menggunakan pacs.008 secara langsung dalam pengeluaran — dan bagaimana rupa penalti kawal selia bagi bank yang tiba pada 22 November masih menganggapnya sebagai masalah terjemahan.

Pada Jun 2026, ISO 20022 telah berhenti menjadi cerita migrasi. Ia ialah substrat. Setiap bank korporat dan pelaburan yang serius kini menganggap `pain.001`, `pacs.008`, dan `camt.053` sebagai model data utama untuk perbendaharaan, bukan sebagai format wayar yang perlu diterjemahkan di pinggir. Namun begitu, dengan lima bulan menjelang [peralihan SWIFT MT/MX pada 22 November 2026](https://www.redcompasslabs.com/insights/what-now-iso-20022-deadlines-in-2026-onwards/ "RedCompass Labs: tarikh akhir ISO 20022 pada 2026 dan seterusnya"), [hampir separuh daripada bank dunia masih ketinggalan](https://financialit.net/news/banking/nearly-half-banks-are-behind-iso-20022 "Financial IT: hampir separuh bank ketinggalan dalam ISO 20022") untuk memenuhi kewajipan data berstruktur, alamat berstruktur, dan CBPR+ yang diperlukan oleh rangkaian.

Angka itu — 44% menurut tinjauan industri terkini — ialah fakta paling penting dalam pembayaran rentas sempadan tahun ini. Ia bukan cerita teknologi. Ia ialah cerita kebertanggungjawaban lembaga. Bank yang tiba pada 22 November masih memancarkan mesej MT103 atau pain.001 dengan blok alamat tidak berstruktur akan terputus daripada koresponden khusus MX, dikenakan caj tambahan oleh yang lain, dan tidak mampu menyuap mana-mana enjin perbendaharaan agentik yang bergantung pada data tujuan, kiriman wang, dan kawal selia yang boleh dibaca mesin.

Artikel 2023 di laman ini, [Mengautomasikan Penciptaan Fail Pembayaran Patuh ISO 20022 dengan pain.001](https://sebastienrousseau.com/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001), membingkaikan pain.001 sebagai masalah penjanaan. Pada 2026 bingkai itu berbeza. pain.001 kini ialah degupan jantung tindanan kecairan boleh program — apa yang [Indeks Perbendaharaan Autonomi 2026](https://sebastienrousseau.com/2026-06-07-autonomous-treasury-index-programmable-liquidity-tokenised-deposits-2026) panggil sebagai sistem saraf autonomik perbendaharaan CIB. Mesej ialah isyarat. Skema ialah pendawaian.

## 01. Penamat kewujudan bersama

Tempoh kewujudan bersama MT/MX SWIFT berakhir pada 22 November 2026. Selepas tarikh itu, kategori rentas sempadan FIN MT — MT103, MT202, MT202COV, dan mesej pelaporan MT9xx yang berkaitan — ditamatkan daripada penggunaan rentas sempadan. [Taklimat "bab terakhir" Banking Vision](https://banking.vision/en/iso-20022-the-final-chapter-begins/ "Banking Vision: ISO 20022 — bab terakhir bermula") menggambarkannya dengan tepat: ini bukan lanjutan yang lain. Get terjemahan rangkaian akan terus beroperasi, tetapi setiap bank yang menghantar atau menerima mesej yang diterjemahkan membayar keistimewaan itu dua kali — sekali dalam yuran, sekali dalam kesetiaan data yang hilang.

Masalah strukturnya ialah data. MT103 membawa 35 aksara kiriman wang tidak berstruktur dalam medan 70 dan alamat teks bebas dalam medan 50K. pacs.008 membawa `<RmtInf>` dengan rujukan pemiutang berstruktur, `<PstlAdr>` dengan jalan, poskod, bandar, dan kod negara sebagai elemen diskret, dan `<RgltryRptg>` untuk kewajipan khusus bidang kuasa. Peningkatan CBPR+ 2024 mengubah apa yang dahulunya medan "boleh" menjadi medan "mesti". Bank yang menterjemah turun kepada MT103 kehilangan data yang mereka perlukan untuk memenuhi [Saranan 16 FATF](https://www.fatf-gafi.org/en/publications/Fatfrecommendations/Fatf-recommendations.html "Saranan FATF") mengenai maklumat pemula dan benefisiari.

Kewujudan bersama ialah suatu ihsan. Ia telah tamat.

## 02. ISO sebagai substrat data untuk ejen

Kerja yang menarik dalam perbendaharaan 2026 berada di atas skema. Enjin kecairan boleh program, pengoptimum kredit intrahari, dan aliran kerja perbendaharaan agentik semuanya bergantung pada data pembayaran yang boleh dibaca mesin dan disahkan skema. Secara praktikal, sebuah perbendaharaan agentik secara automatik mengoptimumkan penempatan kecairan intrahari dengan menyelaraskan kod `<Purp>` berstruktur dan data kiriman wang terhadap keperluan pembiayaan masa nyata — memindahkan tunai, mengambil talian kredit, atau menahan pelaksanaan tanpa campur tangan manusia. MT103 tidak dapat membekalkannya. pacs.008 boleh.

[Laporan BIS CPMI mengenai penyelarasan ISO 20022 untuk pembayaran rentas sempadan](https://www.bis.org/cpmi/publ/d230.pdf "BIS CPMI: keperluan data ISO 20022 yang diselaraskan") menerbitkan set keperluan mesej-dan-data kanonik pada 2023. Suplemen 2026 menegaskan hujah yang sama dengan lebih tajam: penyelarasan bukan lagi saranan, ia ialah prasyarat untuk sasaran [peta jalan pembayaran rentas sempadan G20](https://www.bis.org/cpmi/publ/d193.htm "BIS CPMI: peta jalan pembayaran rentas sempadan G20") mengenai kos, kelajuan, ketelusan, dan akses. Tanpa kod `<Purp>` berstruktur, alamat berstruktur, dan kiriman wang berstruktur, seorang ejen tiada apa-apa untuk difikirkan. Ia hanya mempunyai prosa.

Di sinilah tesis [Indeks Perbendaharaan Autonomi 2026](https://sebastienrousseau.com/2026-06-07-autonomous-treasury-index-programmable-liquidity-tokenised-deposits-2026) mendarat. Kecairan boleh program bukan silap mata. Ia ialah disiplin menyuap ejen dengan mesej ISO 20022 yang kanonik dan disahkan skema serta membiarkan dasar-sebagai-kod mengawal apa yang boleh dipindahkan oleh ejen dan kepada siapa. Mesej MX ialah impuls saraf. Satah kawalan perbendaharaan ialah saraf tunjang. Tadbir urus risiko model SR 11-7 dan kebertanggungjawaban lembaga Perkara 5 DORA berada di atas sebagai sistem saraf pusat.

Buang MX dan ejen menjadi buta.

## 03. MX asli atau warganegara kelas kedua

Dua realiti operasi membentuk semula ekonomi pada suku ini. Pertama, bank koresponden utama telah menerbitkan jadual caj tambahan untuk rakan niaga khusus MT berkuat kuasa Q4 2026 — biasanya peningkatan setiap mesej pada trafik yang diterjemahkan, ditambah caj penolakan untuk mesej yang gagal pengesahan alamat berstruktur CBPR+. Kedua, saluran SWIFT FINplus menolak pacs.008 yang cacat secara terus, tanpa sandaran MT untuk aliran rentas sempadan baharu.

Itu mengubah kos tingkah laku ketinggalan daripada terlebih belanja projek menjadi bebanan berulang pada margin. Sebuah bank transaksi peringkat pertengahan yang memproses dua juta pembayaran rentas sempadan sebulan pada peningkatan setiap mesej walaupun beberapa sen sahaja sedang menghadapi kos tambahan tahunan tujuh angka, sebelum kos pengalaman pelanggan akibat pembayaran gagal dan kos reputasi menjadi pembayar cukai terjemahan.

Peraturan pengesahan CBPR+ itu sendiri tidak boleh dirunding. `<PstlAdr>` berstruktur dengan `<Ctry>` dan sekurang-kurangnya satu daripada `<StrtNm>`/`<TwnNm>`/`<PstCd>` diisi. LEI dalam `<OrgId>/<LEI>` di mana pemula atau pemiutang muktamad ialah entiti undang-undang. Kod mata wang ISO 4217. Tarikh ISO 8601 dengan zon waktu. Apa-apa selain itu gagal di get rangkaian, bukan di bank destinasi — yang bermakna bank penghantar membayar kos penolakan dan pelanggan melihat pembayaran gagal terlebih dahulu.

Tiada pendaratan lembut.

## 04. Mereka bentuk API perbendaharaan mengutamakan ISO

Corak kejuruteraan yang betul untuk 2026 ialah mengutamakan ISO. Skema dalaman, kontrak API, dan mesej-pada-wayar semuanya berkongsi model kanonik yang sama: `pain.001` untuk permulaan pelanggan-ke-bank, `pacs.008` untuk penyelesaian bank-ke-bank, `camt.054` untuk pemberitahuan kredit, `camt.053` untuk pelaporan hujung hari. Sampul JSON tiada masalah untuk lapisan pengalaman pembangun, tetapi nama medan, alamat berstruktur, kod tujuan, dan blok pelaporan kawal selia kekal kanonik dari hujung ke hujung.

Serpihan minimal pain.001.001.09 yang menunjukkan kewajipan alamat berstruktur:

```xml
<CdtTrfTxInf>
  <PmtId>
    <EndToEndId>E2E-2026-06-23-0001</EndToEndId>
  </PmtId>
  <Amt>
    <InstdAmt Ccy="EUR">125000.00</InstdAmt>
  </Amt>
  <Cdtr>
    <Nm>Acme Manufacturing SA</Nm>
    <PstlAdr>
      <StrtNm>Rue de la Loi</StrtNm>
      <BldgNb>200</BldgNb>
      <PstCd>1049</PstCd>
      <TwnNm>Brussels</TwnNm>
      <Ctry>BE</Ctry>
    </PstlAdr>
    <Id>
      <OrgId>
        <LEI>529900T8BM49AURSDO55</LEI>
      </OrgId>
    </Id>
  </Cdtr>
  <CdtrAcct>
    <Id><IBAN>BE71096123456769</IBAN></Id>
  </CdtrAcct>
  <Purp>
    <Cd>GDDS</Cd>
  </Purp>
  <RmtInf>
    <Strd>
      <CdtrRefInf>
        <Tp><CdOrPrtry><Cd>SCOR</Cd></CdOrPrtry></Tp>
        <Ref>RF18539007547034</Ref>
      </CdtrRefInf>
    </Strd>
  </RmtInf>
</CdtTrfTxInf>
```

Dua prinsip terhasil daripada ini. Pertama, blok `<PstlAdr>` bukan pilihan dari CBPR+ fasa 3 dan seterusnya. Mana-mana API dalaman yang menerima satu baris alamat teks bebas ialah penolakan pada masa hadapan. Kedua, kod `<Purp>` dan blok `<RmtInf><Strd>` ialah apa yang menjadikan mesej boleh dibaca mesin oleh ejen perbendaharaan. Kod tujuan `GDDS` ditambah rujukan pemiutang `SCOR` berstruktur boleh diselaraskan tanpa campur tangan manusia. Catatan teks bebas 35 aksara tidak boleh.

Permukaan API yang pragmatik untuk platform perbankan korporat 2026 ialah lapisan REST nipis di atas skema kanonik. `POST /v1/payments/credit-transfer` menerima badan JSON yang memetakan satu-dengan-satu kepada elemen pain.001. Pelayan mengesahkan terhadap XSD CBPR+ pada kemasukan, mengekalkan XML kanonik, menandatanganinya untuk bukan penafian, dan memancarkan peristiwa audit WORM. Titik akhir yang sama memancarkan panggil balik `camt.054` dan `camt.053` pada model kanonik. Tiada terjemahan. Tiada hanyut.

Itulah mengutamakan ISO dalam pengeluaran.

## Soalan Lazim

**Apa yang berubah pada 22 November 2026 yang tidak berubah pada November 2025?**
November 2025 ialah permulaan penurunan kewujudan bersama FIN MT/MX untuk kategori rentas sempadan. November 2026 ialah penamatnya. Selepas tarikh itu, FIN MT103, MT202, MT202COV dan siri pelaporan MT9xx ditamatkan daripada penggunaan rentas sempadan. Get terjemahan rangkaian akan terus beroperasi, tetapi setiap mesej yang diterjemahkan membayar dalam yuran dan dalam kesetiaan data yang hilang. Medan alamat berstruktur dan kiriman wang berstruktur CBPR+ berhenti menjadi pilihan.

**Adakah pain.001 perkara yang sama dengan pacs.008?**
Tidak. pain.001 ialah mesej permulaan pindahan kredit pelanggan — ERP korporat ke bank. pacs.008 ialah pindahan kredit antara bank — bank ke bank, melalui SWIFT atau rel setara. Kedua-duanya berkongsi tatabahasa ISO 20022 dan kebanyakan elemen struktur (`<PstlAdr>`, `<RmtInf>`, `<Purp>`, `<Dbtr>` / `<Cdtr>` / `<DbtrAgt>` / `<CdtrAgt>`) tetapi ia adalah mesej berbeza pada kaki berbeza. Platform perbendaharaan 2026 mengesahkan pain.001 korporat pada kemasukan dan memancarkan pacs.008 pada hop antara bank tanpa memetakan semula.

**Mengapa blok `<PstlAdr>` berstruktur begitu penting?**
Kerana Saranan 16 FATF dan CBPR+ fasa 3 kedua-duanya memerlukan data alamat berstruktur pada medan pemula dan benefisiari rentas sempadan. Baris alamat teks bebas tidak boleh disahkan, disaring, atau diselaraskan pada skala besar. Elemen `StrtNm` / `PstCd` / `TwnNm` / `Ctry` berstruktur boleh. Dari November 2026, bank yang memancarkan alamat tidak berstruktur ditolak semasa menghurai oleh koresponden khusus MX dan dikenakan caj tambahan oleh yang bertoleransi terhadap terjemahan.

**Apa maksud "mengutamakan ISO" untuk API dalaman?**
Ia bermakna model kanonik di sebelah bank pada API ialah pokok elemen ISO 20022, bukan JSON milik bank yang diratakan. `POST /v1/payments/credit-transfer` menerima badan permintaan yang memetakan satu-dengan-satu kepada pain.001. Pelayan mengesahkan terhadap XSD CBPR+ pada kemasukan, mengekalkan XML kanonik, dan memancarkan pacs.008 ke rel. Tiada terjemahan pinggir, tiada hanyut semantik antara permintaan korporat dan apa yang tiba di koresponden.

**Di mana kedudukan bank yang belum bermula?**
Lima bulan ialah masa yang cukup untuk menghantar profil mesej yang lebih ketat daripada CBPR+ dan kemasukan tolak-semasa-menghurai, menjalankan berganda pengesahan CBPR+ terhadap trafik koresponden langsung, dan kaki penyelesaian asli pacs.008 untuk 20 koridor teratas. Ia bukan masa yang cukup untuk memplatform semula teras. Bank dalam kedudukan itu perlu menyusun: pengesahan-semasa-menghurai dahulu (menghentikan pendarahan pada trafik keluar), pemulihan alamat berstruktur kedua (menutup jurang kawal selia), penyelesaian asli pacs.008 penuh ketiga (menangkap kelebihan kecairan boleh program selepas tarikh akhir).

## Kesimpulan

Tarikh akhir November 2026 ialah bahagian yang mudah. Bahagian yang sukar ialah apa yang dipaksa oleh tarikh akhir itu. Bank yang tiba tepat pada masanya masih menganggap pain.001 sebagai masalah terjemahan akan menghabiskan dekad seterusnya membina semula model data perbendaharaan mereka dari wayar ke dalam. Bank yang tiba dengan skema kanonik mengutamakan ISO, alamat berstruktur secara lalai, dan satah kawalan kecairan boleh program yang menggunakan pacs.008 secara langsung akan menjalankan perbendaharaan agentik di bawah kebertanggungjawaban lembaga Perkara 5 DORA, disiplin risiko operasi [Basel III](https://www.bis.org/bcbs/publ/d424.htm "Basel III: memuktamadkan pembaharuan pasca-krisis"), dan tadbir urus model [SR 11-7](https://www.federalreserve.gov/supervisionreg/srletters/sr1107.htm "SR 11-7 Panduan Pengurusan Risiko Model").

Bingkai sistem saraf autonomik bukan hiasan. Perbendaharaan tidak boleh membuat penaakulan tentang kecairan yang tidak dapat dilihatnya. Ejen tidak boleh bertindak atas data yang tidak dapat dihuraikannya. ISO 20022 ialah pendawaian perbendaharaan CIB pada 2026 — mesej berstruktur ialah potensi tindakan, skema ialah jejak audit yang akan dituntut oleh pengawal selia pada pagi selepas insiden seterusnya.

Lima bulan. Bina skema, bukan penyelesaian sementara.

## Rujukan

Bank for International Settlements, Committee on Payments and Market Infrastructures (2023). *Harmonised ISO 20022 data requirements for enhancing cross-border payments* (CPMI Papers No. 230). Tersedia di: [https://www.bis.org/cpmi/publ/d230.htm](https://www.bis.org/cpmi/publ/d230.htm "BIS CPMI 230 — keperluan data ISO 20022 yang diselaraskan")

Basel Committee on Banking Supervision (2017). *Basel III: Finalising post-crisis reforms*. Bank for International Settlements. Tersedia di: [https://www.bis.org/bcbs/publ/d424.htm](https://www.bis.org/bcbs/publ/d424.htm "Basel III: memuktamadkan pembaharuan pasca-krisis")

European Parliament and Council (2022). *Regulation (EU) 2022/2554 on digital operational resilience for the financial sector (DORA)*. Tersedia di: [https://eur-lex.europa.eu/eli/reg/2022/2554/oj](https://eur-lex.europa.eu/eli/reg/2022/2554/oj "Regulation (EU) 2022/2554 — DORA")

Financial Action Task Force (2023). *International standards on combating money laundering and the financing of terrorism — Recommendation 16 on wire transfers*. Tersedia di: [https://www.fatf-gafi.org/en/publications/Fatfrecommendations/Fatf-recommendations.html](https://www.fatf-gafi.org/en/publications/Fatfrecommendations/Fatf-recommendations.html "Saranan FATF")

Federal Reserve (2011). *SR 11-7 Guidance on Model Risk Management*. Tersedia di: [https://www.federalreserve.gov/supervisionreg/srletters/sr1107.htm](https://www.federalreserve.gov/supervisionreg/srletters/sr1107.htm "SR 11-7 Panduan Pengurusan Risiko Model")

International Organization for Standardization (2022). *ISO 20022 Financial services — Universal financial industry message scheme*. Tersedia di: [https://www.iso20022.org](https://www.iso20022.org "ISO 20022 — Universal financial industry message scheme")

RedCompass Labs (2025). *What now? ISO 20022 deadlines in 2026 onwards*. Tersedia di: [https://www.redcompasslabs.com/insights/what-now-iso-20022-deadlines-in-2026-onwards/](https://www.redcompasslabs.com/insights/what-now-iso-20022-deadlines-in-2026-onwards/ "RedCompass Labs — tarikh akhir ISO 20022 pada 2026 dan seterusnya")

SWIFT (2024). *Cross-Border Payments and Reporting Plus (CBPR+) usage guidelines*. Tersedia di: [https://www.swift.com/standards/iso-20022/iso-20022-programme](https://www.swift.com/standards/iso-20022/iso-20022-programme "SWIFT CBPR+ usage guidelines")
