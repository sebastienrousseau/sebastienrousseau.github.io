---
title: "ISO 20022 Selepas Migrasi: Menjadikan Data Pembayaran sebagai Produk Perbankan pada 2026"
tags: "ISO 20022, structured address, CBPR+, payment data, reconciliation, sanctions screening, fraud detection, post-quantum cryptography, AI, tokenised deposits, cross-border payments"
subtitle: "Ganjaran sebenar ISO 20022 bukanlah pematuhan mesej. Ia adalah menjadikan data pembayaran berstruktur sebagai produk bank yang pelanggan sanggup bayar dan pasukan operasi boleh automasikan."
description: "ISO 20022 selepas migrasi ialah peluang produk data. Alamat berstruktur, kod tujuan, butiran invois, mesej penyiasatan, dan peristiwa status pembayaran yang lebih kaya boleh menjadi produk penyesuaian, penipuan, kecairan, pematuhan, dan analitik."
date: "May 29, 2026"
language: "ms"
locale: "ms_MY"
banner: "https://cloudcdn.pro/stocks/images/humphrey-muleba-1660004-1200.webp"
banner_alt: "Rajah produk data pembayaran ISO 20022 yang menunjukkan alamat berstruktur, kod tujuan, penyesuaian, pengesanan penipuan, ramalan kecairan, saringan sekatan, dan produk analitik"
keywords: "ISO 20022 2026, alamat berstruktur, CBPR+, produk data pembayaran, kod tujuan pembayaran, perbendaharaan korporat, penyesuaian, saringan sekatan, pengesanan penipuan"
---

## ISO 20022 Selepas Migrasi: Menjadikan Data Pembayaran sebagai Produk Perbankan pada 2026

[ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) selepas migrasi ialah kerja kejuruteraan, bukan strategi. Kewujudan bersama SWIFT MT / MX untuk pembayaran rentas sempadan berakhir pada 22 November 2025; MT 103, MT 202 dan MT 202COV tidak lagi diproses untuk nilai rentas sempadan. CHAPS menyelesaikan migrasinya pada Jun 2023; T2 dan T2S bermigrasi pada Mac 2023; Fedwire Funds Service bermigrasi pada Mac 2025; CHIPS dan SIC diselaraskan. Mandat alamat berstruktur pacs.008 November 2026 tinggal lima bulan lagi, dan ekor panjang kandungan `<AdrLine>` bentuk bebas berterusan di banyak koridor. Persoalan institusi untuk 2026 bukanlah sama ada untuk menggunakan ISO 20022 — itu sudah selesai — tetapi sama ada belakang pejabat bank adalah MX asli atau sama ada lapisan terjemahan secara senyap melucutkan muatan berstruktur sebelum data itu sampai ke pasukan produk. ([SWIFT](https://www.swift.com/news-events/news/2025-iso-20022-progress "Kemajuan ISO 20022 SWIFT 2025")).

---

> **Ringkasan Eksekutif / Pengajaran Utama**
>
> - **Kewujudan bersama MT / MX telah ditutup.** Peralihan akhir 22 November 2025. SWIFT FINplus ialah satu-satunya format wayar untuk tunai rentas sempadan di rangkaian dari tarikh itu.
> - **Lima bulan ke tarikh akhir seterusnya.** CBPR+ Fasa 2 mengamanahkan komponen `<PstlAdr>` berstruktur mulai November 2026 — `<StrtNm>`, `<TwnNm>`, `<Ctry>` — dengan `<AdrLine>` dinyahtaraf untuk mesej baharu.
> - **MX asli atau anda tidak bermigrasi.** Bank yang menjalankan lapisan terjemahan MX-ke-kanonikal-dalaman yang kehilangan `<RmtInf><Strd>`, `<Purp>`, `<UltmtDbtr>`, `<UltmtCdtr>`, `<LEI>` sedang mengeluarkan mesej patuh dan menangkap tiada nilai. Kerja itu adalah asli-belakang-pejabat, bukan asli-antara-muka.
> - **Produk data pertama ialah lebih sedikit penyiasatan.** camt.027 / .028 / .029 / .087 yang disambungkan ke platform pengurusan kes memotong masa kitaran penyiasatan rentas sempadan sebanyak ~60% pada koridor MX-penuh. Metriknya ialah penyiasatan yang ditutup setiap hari-FTE, bukan "penggunaan" apa-apa.
> - **Yang kedua ialah pengurangan positif palsu sekatan.** `<Nm>`, `<PstlAdr>`, BIC, LEI, `<Othr>` berstruktur memotong positif palsu senarai disatukan OFAC / OFSI / EU sebanyak 15–40% berbanding medan bentuk bebas MT 103, bergantung pada kualiti mesej warisan.
> - **Yang ketiga ialah data perbendaharaan korporat.** pacs.008 `<RmtInf><Strd><RfrdDocAmt>`, `<CdtrRefInf>`, `<AddtlRmtInf>` ditambah pain.001 `<RmtId>` membolehkan penyesuaian peringkat invois. Korporat membayar untuk ini; kebanyakan bank belum lagi membungkusnya.
> - **SWIFT gpi kini asli-ISO.** UETR berterusan; penjejak membaca pacs.002 / .004 / .028 secara langsung. Pengalaman pelanggan perbendaharaan bergantung pada sama ada saluran asli-MX menghasilkan peristiwa status berstruktur atau pengakuan generik.
>
---

## Apa yang Ditutup pada November 2025 dan Apa yang Tidak

Peralihan SWIFT rentas sempadan pada 22 November 2025 menyingkirkan MT 103, MT 202, MT 202COV, MT 205 dan MT 205COV untuk penggunaan rentas sempadan yang membawa nilai. SWIFT FINplus — perkhidmatan berasaskan InterAct yang membawa ISO 20022 MX — menjadi satu-satunya laluan untuk aliran tersebut. CBPR+ Fasa 1 menjadi mandatori dalam tingkap yang sama. Pengendali ESMIG di ECB telah mengesahkan migrasi sepadan untuk T2 dan T2S; [perkhidmatan CHAPS Bank of England ⧉](https://www.bankofengland.co.uk/payment-and-settlement/chaps "CHAPS — Bank of England") diselesaikan pada MX penuh pada Jun 2023; Rizab Persekutuan menyiapkan migrasi Fedwire Funds Service pada Mac 2025.

Apa yang tidak ditutup:

- **MT domestik untuk aliran bukan-rentas-sempadan.** Bank yang menjalankan mesej berbentuk MT dalaman untuk skim domestik bukan-SWIFT terus beroperasi. Peralihan itu ialah peristiwa rentas sempadan SWIFT FIN, bukan persaraan global MT.
- **Pemesejan MT untuk kewangan perdagangan.** MT 7XX (kredit dokumentari), MT 4XX (kutipan), MT 5XX (dagangan sekuriti) kekal di FIN buat masa ini. Padanan ISO 20022 (semt.*, tsmt.*) wujud tetapi belum berada di bawah mandat rentas sempadan.
- **Penyata nostro MT 9XX di belakang-pejabat warisan.** Penyata MT 940 / 942 / 950 berterusan daripada banyak koresponden; padanan camt.052 / camt.053 / camt.054 tersedia tetapi proses penyesuaian nostro warisan belum semuanya bermigrasi.
- **Ekor panjang MX dengan kandungan `<AdrLine>`.** Mandat Fasa 1 menerima alamat berstruktur-tambah-tidak-berstruktur hibrid. Mandat Fasa 2 pada November 2026 tidak.

Perubahan format wayar tidak sama dengan perubahan seni bina data. Bank yang menterjemah MX masuk kepada kanonikal dalaman berbentuk MT melucutkan `<RmtInf><Strd>`, `<Purp>`, `<UltmtDbtr>`, `<UltmtCdtr>`, `<LEI>`, `<UETR>` sebelum gudang datanya, enjin sekatan, enjin penipuan, enjin AML dan saluran penyesuaian melihat mesej itu. Format wayar ialah MX; institusi itu beroperasi pada data berbentuk MT yang miskin secara dalaman. Dari perspektif kawal selia dan komersial, migrasi itu tidak lengkap.

## Mandat Alamat Berstruktur November 2026

CBPR+ Fasa 2 mengamanahkan bentuk berstruktur `<PstlAdr>` mulai November 2026. Bentuk berstruktur memerlukan:

```xml
<PstlAdr>
  <StrtNm>200 Aldersgate Street</StrtNm>
  <TwnNm>London</TwnNm>
  <PstCd>EC1A 4HD</PstCd>
  <Ctry>GB</Ctry>
</PstlAdr>
```

Alternatif bentuk bebas yang dinyahtaraf — `<AdrLine>200 Aldersgate Street, London, EC1A 4HD</AdrLine>` — dibenarkan hari ini di bawah Fasa 1 tetapi tidak lagi boleh diterima untuk mesej baharu dari peralihan Fasa 2. Kandungan minimum mandatori ialah `<TwnNm>` dan `<Ctry>`; `<StrtNm>` dan `<PstCd>` sangat disyorkan.

Realiti penggunaan di kebanyakan bank peringkat-1 pada pertengahan 2026:

- **Sisi pemula (data debitur).** Onboarding yang menghadap pelanggan telah menangkap medan alamat berstruktur selama bertahun-tahun. Induk pelanggan bank biasanya memilikinya. Isunya ialah pemetaan daripada induk-pelanggan kepada medan `<DbtrAcct><Acct>` / `<Dbtr><PstlAdr>` di bawah garis panduan penggunaan HVPS+ atau CBPR+.
- **Sisi masuk (data pemiutang pada mesej pihak lawan).** Di sinilah ekor panjang berada. Data benefisiari dibina oleh bank pemula daripada arahan pelanggan mereka. Bank yang mengendalikan volum besar daripada koridor di mana bank pemula masih mengeluarkan kandungan `<AdrLine>` memerlukan saluran pengayaan yang menukar bentuk bebas kepada berstruktur untuk penggunaan hiliran — dan kemudian strategi untuk apa yang perlu dilakukan dengan mesej yang gagal peralihan November 2026.
- **Garis panduan amalan pasaran CBPR+.** [Garis panduan penggunaan CBPR+ SWIFT ⧉](https://www2.swift.com/mystandards/CBPR+/ "SWIFT MyStandards CBPR+") ialah sumber berautoriti. Garis panduan HVPS+ (sistem pembayaran bernilai tinggi yang digunakan oleh bank pusat) mengikut corak alamat berstruktur yang sama dengan medan mandatori yang sedikit berbeza.

Penghantaran kejuruteraan untuk lima bulan akan datang: saluran pengayaan alamat berstruktur di antara muka MX masuk, pengesahan gagal-keras di antara muka keluar untuk mana-mana alamat yang tidak memenuhi minimum mandatori Fasa 2, dan baris giliran pengendalian pengecualian untuk koridor yang mengeluarkan mesej tidak patuh selepas tarikh akhir.

## Produk Data yang Boleh Dibina Bank Sebenarnya

Sampul pacs.008 membawa lebih banyak data berstruktur berbanding MT 103. Peluang produk terletak pada tiga medan tertentu.

### Kiriman Wang Berstruktur: `<RmtInf><Strd>`

Kiriman wang bentuk bebas — `<RmtInf><Ustrd>` — ialah teks kurang-dan-gabung yang akhirnya memerlukan penghuraian gaya OCR di sisi korporat. Kiriman wang berstruktur — `<RmtInf><Strd>` — membawa `<RfrdDocInf>` (rujukan invois dengan jenis, nombor, tarikh dikeluarkan, jumlah), `<CdtrRefInf>` (satu rujukan pemiutang dengan jenis), `<RfrdDocAmt>` (pembahagian antara jumlah dokumen), `<AddtlRmtInf>` (teks bebas tambahan sehingga empat kejadian). Untuk penyesuaian perbendaharaan korporat, inilah medan yang memonetisasikan.

Produknya: penyesuaian automatik peringkat invois sebagai perkhidmatan perbendaharaan. Sistem AR korporat menyesuaikan pembayaran masuk kepada invois tertentu tanpa padanan manual. Bank yang menetapkan harga ini sebagai perkhidmatan nilai tambah untuk korporat dengan volum invois tinggi dapat mengenakan caj antara 0.5 dan 3 mata asas pada nilai pembayaran bergantung pada tahap volum.

### Kod Tujuan: `<Purp>`

Medan `<Purp><Cd>` membawa ISO 20022 ExternalPurpose1Code — SALA (gaji), DIVI (dividen), GOVT (pembayaran kerajaan), INTC (intra-syarikat), CASH (pengurusan tunai), GDDS (pembelian barangan), SCVE (pembelian perkhidmatan), TRAD (penyelesaian perdagangan), dan ~280 yang lain diselenggarakan oleh ISO. Alternatif teks bebas berada dalam `<Purp><Prtry>`.

Permukaan produk lebih luas daripada penyesuaian:

- **Pemarkahan risiko sekatan dan AML.** Kod tujuan menyuap model pemantauan transaksi dengan data niat berstruktur yang tiada pada bentuk bebas MT 103. Satu pacs.008 dengan `<Purp><Cd>TRAD</Purp>` pada koridor dan pihak lawan yang model risiko bank hanya jangka `<Purp><Cd>SALA</Purp>` mencetuskan semakan bertingkat lebih tinggi.
- **Ramalan kecairan.** Pengurusan perbendaharaan boleh mengunjur kecairan pada butiran intra-hari dengan mengagregat pembayaran mengikut kod tujuan dan bukan mengikut pihak lawan sahaja. Aliran SALA dan DIVI mempunyai kebolehramalan masa yang berbeza daripada TRAD atau CASH.
- **Pengkategorian cukai dan pelaporan.** Kod tujuan memetakan kepada banyak kategori pelaporan cukai tanpa memerlukan langkah pengayaan berasingan.

### Pengecam Pihak: `<UltmtDbtr>`, `<UltmtCdtr>`, `<LEI>`, `<BIC>`

pacs.008 membawa debitur dan pemiutang muktamad yang berbeza daripada debitur / pemiutang segera — yang penting apabila pembayaran dipengantarakan. Elemen `<LEI>` di bawah `<FinInstnId>` membawa Pengecam Entiti Undang-undang apabila hadir.

Produknya: saringan sekatan dipertingkat dengan data pihak berstruktur. Positif palsu pada saringan senarai disatukan OFAC, OFSI, dan EU menurun secara ketara apabila enjin saringan melihat `<Nm>`, `<PstlAdr>` (berstruktur), `<Id><OrgId><LEI>`, `<Id><OrgId><Othr>` berstruktur berbanding medan teks bentuk bebas. Data penggunaan daripada pasukan saringan sekatan G-SIB pada 2025 — diterbitkan di SIBOS dan pelbagai persidangan teknologi-risiko — menunjukkan pengurangan positif palsu 15–40% bergantung pada kualiti warisan sumber MT 103.

### Mesej Penyiasatan

camt.027 (tuntutan bagi tidak menerima), camt.028 (maklumat tambahan), camt.029 (penyelesaian penyiasatan), camt.087 (permintaan untuk ubah suai) menggantikan perbualan MT 192 / 195 / 196 / 199. Semantik berstruktur — pertanyaan, respons, penyelesaian — mengubah baris giliran penyiasatan daripada proses triaj teks bentuk-panjang kepada aliran kerja.

Produknya bersifat operasi, bukan komersial: masa kitaran penyiasatan rentas sempadan yang diukur pada 5–7 hari pada koridor MT warisan menurun kepada bawah 48 jam pada koridor MX-penuh apabila mesej camt.* disambungkan ke platform pengurusan kes. ROI ialah FTE operasi yang tidak perlu ditambah oleh bank apabila volum berkembang.

## Corak Kejuruteraan: MX Asli lawan Lapisan Terjemahan

Kebanyakan bank peringkat-1 memilih salah satu daripada tiga corak migrasi. Keupayaan produk data pasca-migrasi mereka mengikut secara langsung daripada pilihan itu.

### Corak A: Terjemahan di Wayar, Kanonikal Warisan di Dalam

MX masuk, diterjemahkan kepada kanonikal berbentuk MT di get laluan, diproses oleh sistem sedia ada, diterjemahkan semula kepada MX keluar. Paling ringkas, gangguan paling rendah. **Timbal balik:** gudang data belakang-pejabat, enjin AML, enjin penipuan, enjin sekatan, dan saluran penyesuaian semuanya melihat data berbentuk MT. Bank mengeluarkan MX patuh tetapi menangkap tiada nilai data berstruktur. Baris giliran penyiasatan, positif palsu sekatan, dan usaha penyesuaian semuanya kekal pada tahap era-MT. Kebanyakan pemerhati menjangkakan bank Corak A akan menjalankan gelombang kedua kerja belakang-pejabat sepanjang 2026–2028 untuk mengakses muatan berstruktur.

### Corak B: Kanonikal Dalaman Direka untuk MX

MX masuk, diterjemahkan kepada kanonikal dalaman yang memelihara kiriman wang berstruktur, kod tujuan, data pihak-muktamad, alamat berstruktur, dan mesej penyiasatan. Enjin sekatan, enjin AML, dan saluran penyesuaian dinaik taraf untuk menggunakan data berstruktur. **Timbal balik:** kos pelaksanaan lebih tinggi, program lebih panjang. **Manfaat:** produk data yang diterangkan di atas boleh diakses tanpa gelombang kedua kerja belakang-pejabat.

### Corak C: MX Asli Hujung-ke-Hujung

Aliran MX format-wayar terus ke belakang pejabat dan gudang data tanpa berubah. Model data dalaman bank memetakan terus kepada elemen ISO 20022. **Timbal balik:** gangguan tertinggi kepada sistem warisan; sesetengah platform perbankan teras tidak dapat menerima ini sehingga keluaran utama mereka yang seterusnya. **Manfaat:** laluan paling rendah geseran ke monetisasi produk data dan kedudukan paling bersih untuk mandat alamat berstruktur November 2026, fasa CBPR+ masa depan, dan migrasi akhirnya skim domestik yang masih pada MT.

Corak yang betul bergantung pada platform teras bank, selera program dan pendedahan kepada produk data berstruktur. Hasil yang salah ialah memilih Corak A secara lalai dan kemudian mendapati semasa separuh kedua 2026 bahawa mandat alamat berstruktur, integrasi penjejak-gpi dan peta jalan produk perbendaharaan korporat setiap satunya memerlukan perubahan belakang-pejabat yang tidak berada dalam skop program asal.

## Apa Maknanya Mengikut Jenis Bank

### Bank Penting Sistemik Secara Global

Peralihan CBPR+ Fasa 1 telah berlalu. Peralihan alamat berstruktur November 2026 ialah keutamaan segera, dan program produk data yang memonetisasikan muatan berstruktur ialah keutamaan jangka sederhana. Bina saluran pengayaan alamat berstruktur dahulu — tarikh akhirnya adalah keras. Kemudian jujukkan produk pengurangan positif palsu sekatan dan penyesuaian perbendaharaan korporat terhadap garis dasar era-MT yang sudah wujud dalam papan pemuka operasi.

### Bank Transaksi dan Koresponden

Tekanan persaingan adalah akut. Korporat dan bank responden yang menilai rakan koresponden pada 2026 bertanya tentang peristiwa status berstruktur penjejak gpi, masa kitaran penyiasatan, dan penyesuaian peringkat invois sebagai ciri perkhidmatan. Bank yang menjalankan Corak A — terjemahan di wayar, kanonikal warisan di dalam — menjawab soalan tersebut dengan kurang kompetitif berbanding bank Corak B atau C. Persoalan peta jalan produk untuk separuh kedua 2026 ialah sama ada untuk komited kepada peningkatan belakang-pejabat Corak B atau menerima susutan di hujung tinggi.

### Bank Serantau dan Peringkat Pertengahan

Strategi yang betul ialah menggunakan kekayaan MX dan bukan menghasilkannya secara asli. Pilih vendor platform mesej-pembayaran yang kanonikal dalamannya memelihara muatan berstruktur, sahkan kesediaan CBPR+ Fasa 2 vendor, integrasikan produk data sebagai perkhidmatan dihoskan-vendor dan bukan membinanya secara dalaman. Produk penyesuaian perbendaharaan korporat secara khusus ialah calon untuk sumber platform label-putih.

### Perbendahara Korporat dan PSP

Soalan untuk ditanya kepada bank adalah langsung: "Bolehkah platform anda menyampaikan penyesuaian kiriman wang berstruktur terhadap data peringkat invois, dan apakah penyampaian penjejak gpi untuk pembayaran masuk ke akaun kami?" Bank yang menjawab dengan ciri produk data berstruktur berada pada Corak B atau C; bank yang menjawab dengan "kami patuh CBPR+" mungkin tidak.

## Kesimpulan

ISO 20022 selepas migrasi bukanlah topik penutupan. Perubahan format wayar ditutup pada November 2025; perubahan seni bina data sebahagian besarnya masih di hadapan. Mandat alamat berstruktur November 2026 memaksa keupayaan belakang-pejabat yang banyak bank Corak A tangguhkan. Peluang produk data — pengurangan masa kitaran penyiasatan, pengurangan positif palsu sekatan, penyesuaian peringkat invois korporat, status berstruktur penjejak gpi — hanya berjaya apabila muatan berstruktur bertahan hujung-ke-hujung.

Institusi yang kelihatan boleh dipercayai kepada pelanggan korporat pada 2027 ialah mereka yang beralih daripada Corak A semasa 2026, menyiapkan kejuruteraan alamat berstruktur Fasa 2 dan membungkus produk kiriman wang berstruktur terhadap manfaat pelanggan yang dinyatakan. Institusi yang tidak akan terus mengenakan kadar era-perbankan-koresponden untuk perkhidmatan era-MT di atas wayar MX.

Ukur migrasi cara anda mengukur mana-mana program operasi: penyiasatan ditutup setiap hari-FTE, kadar positif palsu sekatan, liputan alamat berstruktur pada keluaran, populasi kiriman wang berstruktur pada masuk, kadar penyampaian peristiwa-berstruktur penjejak gpi. Metrik pematuhan bukanlah migrasi; metrik operasilah yang menjadinya.

## Soalan Lazim

**Apa yang berakhir pada 22 November 2025?**

MT 103, MT 202, MT 202COV, MT 205 dan MT 205COV untuk aliran nilai rentas sempadan di perkhidmatan SWIFT FIN. Dari tarikh itu semua pemesejan tunai rentas sempadan di SWIFT berjalan di FINplus yang membawa ISO 20022 MX di bawah garis panduan penggunaan CBPR+ Fasa 1. Penggunaan MT domestik, pemesejan kewangan-perdagangan MT 7XX dan penyata nostro MT 9XX berada di luar skop untuk peralihan ini.

**Apakah tarikh akhir November 2026?**

CBPR+ Fasa 2 mengamanahkan bentuk berstruktur `<PstlAdr>` — `<StrtNm>`, `<TwnNm>`, `<Ctry>` — dengan `<AdrLine>` dinyahtaraf untuk mesej baharu. Kandungan minimum mandatori ialah `<TwnNm>` ditambah `<Ctry>`. Tarikh akhir terpakai pada mesej yang dihantar melalui rangkaian SWIFT untuk nilai rentas sempadan.

**Adakah bank "bermigrasi" jika belakang pejabatnya berjalan pada kanonikal dalaman berbentuk MT?**

Format wayar telah bermigrasi; seni bina data tidak. Bank menghantar MX patuh dan menerima MX patuh, tetapi muatan berstruktur dilucutkan sebelum gudang data, enjin AML, enjin penipuan, enjin sekatan dan saluran penyesuaian melihatnya. Dari perspektif kawal selia migrasi itu lengkap; dari perspektif komersial ia tidak.

**Apakah peluang produk data terbesar?**

Untuk korporat: penyesuaian peringkat invois terhadap kiriman wang berstruktur. Untuk bank itu sendiri: pengurangan positif palsu sekatan (15–40% bergantung pada kualiti warisan) dan pengurangan masa kitaran penyiasatan (5–7 hari menurun kepada bawah 48 jam pada koridor MX-penuh). Pengurangan penyiasatan ialah ROI operasi pada volum sedia ada; pengurangan sekatan ialah ROI operasi ditambah kedudukan kawal selia; produk penyesuaian korporat ialah hasil yuran baharu.

**Adakah SWIFT gpi masih terpakai?**

Ya. UETR berterusan; penjejak gpi membaca pacs.002, pacs.004 dan pacs.028 secara langsung. Pengalaman pelanggan perbendaharaan gpi — keterlihatan hujung-ke-hujung dengan peristiwa status berstruktur — bergantung pada saluran asli-MX bank menghasilkan peristiwa status berstruktur dan bukan pengakuan generik.

## Rujukan

- SWIFT, (2025). [Kemajuan ISO 20022 2025 ⧉](https://www.swift.com/news-events/news/2025-iso-20022-progress "Kemajuan SWIFT 2025").
- SWIFT, (2025). [Garis panduan penggunaan CBPR+ di MyStandards ⧉](https://www2.swift.com/mystandards/CBPR+/ "MyStandards CBPR+").
- Bank of England, (2023). [CHAPS — Bank of England ⧉](https://www.bankofengland.co.uk/payment-and-settlement/chaps "CHAPS").
- European Central Bank, (2023). [Konsolidasi TARGET Services ⧉](https://www.ecb.europa.eu/paym/target/consolidation/html/index.en.html "Konsolidasi T2 / T2S").
- Federal Reserve, (2025). [Pelaksanaan ISO 20022 Fedwire Funds Service ⧉](https://www.frbservices.org/resources/financial-services/wires/iso-20022-implementation-center "Fedwire ISO 20022").
- ISO, (2024). [Katalog mesej ISO 20022 ⧉](https://www.iso20022.org/iso-20022-message-definitions "Takrifan mesej ISO 20022").
