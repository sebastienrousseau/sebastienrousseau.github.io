---
title: "Tarikh Akhir Alamat Berstruktur pacs.008 November 2026: Pandangan Enam Bulan"
tags: "ISO 20022, pacs.008, CBPR+, structured address, SWIFT, cross-border payments, sanctions screening, FI-to-FI credit transfer, payments, DORA, post-quantum cryptography, AI, tokenised deposits, open source, quantum computing"
subtitle: "Mulai pertengahan November 2026, SWIFT CBPR+ akan menolak alamat pos tidak berstruktur dalam pacs.008 dan mesej pembayaran rentas sempadan yang berkaitan. Dengan lebih kurang 65% mesej masih tidak mematuhi, tetingkap pemulihan sedang menutup dengan pantas."
description: "Mulai November 2026, SWIFT CBPR+ mewajibkan alamat pos berstruktur dalam mesej pembayaran rentas sempadan. Baris alamat tidak berstruktur (AdrLine sahaja) tidak akan lagi diterima untuk medan pihak utama dalam pacs.008. Pada tahap minimum, TwnNm dan Ctry diperlukan, dengan StrtNm dan BldgNb atau PstBx disyorkan. Dengan enam bulan lagi berbaki, 65% mesej pembayaran masih mengandungi alamat tidak berstruktur dan 44% bank kekal ketinggalan jadual."
date: "May 12, 2026"
language: "ms"
locale: "ms_MY"
banner: "https://cloudcdn.pro/stocks/images/markus-winkler-IrRbSND5EUc-unsplash.webp"
banner_alt: "Rajah alamat berstruktur ISO 20022 pacs.008 - medan mesej pembayaran rentas sempadan dengan TwnNm dan Ctry diserlahkan"
keywords: "ISO 20022, pacs.008, SWIFT CBPR+, alamat berstruktur, November 2026, alamat pos, TwnNm, Ctry, StrtNm, BldgNb"
---

Mulai pertengahan November 2026, SWIFT CBPR+ akan menolak alamat pos tidak berstruktur dalam pacs.008 dan mesej pembayaran rentas sempadan yang berkaitan. Dengan lebih kurang 65% mesej masih tidak mematuhi dan 44% bank ketinggalan jadual, tetingkap pemulihan sedang menutup lebih pantas daripada yang mampu dikendalikan oleh kebanyakan program kesediaan.

---

> **Intipati Utama**
>
> - Mulai **November 2026**, SWIFT CBPR+ tidak lagi menerima alamat pos tidak berstruktur dalam mesej pembayaran rentas sempadan. Perubahan ini terpakai kepada **pacs.008** (pindahan kredit pelanggan), **pacs.009** (pindahan kredit FI), **pacs.004** (pemulangan), dan **pacs.003** (debit terus), serta aliran **pain.001** di hulu yang menyuapkannya.
> - Pada tahap minimum, **Nama Bandar (TwnNm)** dan **Negara (Ctry)** mesti hadir dalam medan berstruktur khusus. **Nama Jalan (StrtNm)** dan sama ada **Nombor Bangunan (BldgNb)** atau **Peti Surat (PstBx)** amat disyorkan. Baris alamat teks bebas (AdrLine) sahaja tidak akan lagi memenuhi keperluan bagi medan pihak utama.
> - Perubahan ini meningkatkan ketepatan saringan sekatan, mengurangkan kadar pembaikan manual, dan melindungi pemprosesan lurus-terus — tetapi hanya untuk institusi yang telah memulihkan data pelanggan huluan mereka, bukan sekadar enjin mesej mereka.
> - Kesediaan industri tidak sekata. Sehingga Mac 2026, lebih kurang **65% mesej CBPR+ masih membawa alamat tidak berstruktur**, **44% bank** tidak berada pada landasan untuk tarikh akhir, dan **32% rekod alamat pelanggan** kekal tidak berstruktur secara purata.
> - Perkakas sumber terbuka — termasuk **[pacs008](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 Toolkit and API")**, sebuah pustaka Python dan perkhidmatan FastAPI untuk menjana, mengesahkan, dan menyelaraskan aliran mesej pacs.008 — boleh memampatkan garis masa pemulihan dengan mengautomasikan pengesahan skema, semakan kualiti alamat, dan penguatkuasaan pada peringkat CI sebelum mesej sampai ke rangkaian SWIFT.

---

## Tarikh Akhir Yang Sememangnya Akan Tiba

Keperluan alamat berstruktur November 2026 bukanlah langkah kawal selia yang mengejut. Ia telah berada dalam pelan hala tuju SWIFT CBPR+ sejak migrasi asal [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) diumumkan, dan ia menyusuli berakhirnya kewujudan bersama MT/MX pada November 2025. Apa yang telah berubah pada 2026 adalah jaraknya. Dengan lebih kurang enam bulan berbaki, industri kini beroperasi dalam tetingkap di mana isu kualiti data yang belum diselesaikan menjadi risiko operasi.

Angka-angkanya menceritakan kisah dengan jelas. Kemas kini komuniti SWIFT sendiri pada Mac 2026 menyatakan bahawa [lebih kurang 65% mesej pembayaran masih mengandungi alamat tidak berstruktur ⧉](https://www.swift.com/news-events/news/iso-20022-milestone-november-2026-unstructured-addresses-be-removed "ISO 20022 milestone for November 2026: Unstructured addresses to be removed"), dan bahawa penggunaan kekal tidak sekata merentasi geografi dan jenis institusi. Satu [tinjauan RedCompass Labs terhadap 308 profesional pembayaran kanan pada Mac 2026 ⧉](https://financialit.net/news/banking/nearly-half-banks-are-behind-iso-20022 "Nearly Half of Banks Are Behind on ISO 20022") mendapati bahawa 44% bank tidak berada pada landasan untuk memenuhi tarikh akhir alamat berstruktur, walaupun membelanjakan purata $20 juta — dan bagi institusi terbesar melebihi $30 juta — untuk kesediaan 2026, dengan purata 13 kakitangan tambahan ditugaskan kepada program [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html). Tinjauan yang sama mendapati bahawa 32% rekod alamat pelanggan kekal tidak berstruktur secara purata, dan bahawa 60% bank melaporkan jurang dalam sistem perbankan teras apabila menyokong medan alamat berstruktur.

Dengan kata lain, ini bukanlah masalah yang boleh diselesaikan dengan sebulan lagi kerja enjin mesej. Ia adalah masalah kualiti data yang bermula di hulu daripada lapisan mesej ke dalam sistem pendaftaran, proses KYC, saluran korporat, dan data induk pelanggan teks bebas yang terkumpul selama beberapa dekad.

## Apa Yang Sebenarnya Diperlukan Oleh Peraturan Ini

Di bawah SWIFT CBPR+ Standards Release 2026 (SR2026), keperluan utama adalah mudah dari segi prinsip dan tidak berbelah bahagi dari segi perincian. Mulai pertengahan November 2026, [Nama Bandar dan Negara mesti disediakan dalam medan berstruktur yang ditetapkan ⧉](https://www.swift.com/news-events/news/iso-20022-milestone-november-2026-unstructured-addresses-be-removed "ISO 20022 milestone for November 2026: Unstructured addresses to be removed") bagi semua ejen dan pihak dalam mesej pembayaran CBPR+, dengan pengecualian yang amat terhad (penyata dan pemberitahuan dalam camt.052, camt.053, camt.054, serta beberapa mesej pentadbiran kekal di luar keperluan ketat). Bagi ejen, penggunaan berterusan BIC sahaja kekal sebagai alternatif yang sah kepada nama-dan-alamat.

Dua format alamat dibenarkan selepas peralihan:

- **Berstruktur sepenuhnya** — setiap komponen alamat pos dipetakan kepada elemen [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) khususnya: StrtNm (Nama Jalan), BldgNb (Nombor Bangunan) atau BldgNm (Nama Bangunan), PstCd (Poskod), TwnNm (Nama Bandar), CtrySubDvsn (Subbahagian Negara), Ctry (Negara, sebagai kod ISO 3166-1 alpha-2). Ini adalah format yang secara jelas dikenal pasti oleh SWIFT sebagai pilihan yang lebih diingini apabila boleh.
- **Hibrid** — Nama Bandar dan Negara diisi dalam medan berstrukturnya, manakala baki alamat boleh menggunakan sehingga dua elemen AdrLine tidak berstruktur. Yang penting, [elemen berstruktur tidak boleh diulang di dalam baris tidak berstruktur ⧉](https://www.statestreet.com/web/insights/articles/documents/state-street-client-guide-to-iso-20022-2025.pdf "State Street Client Guide to ISO 20022 2025"); alamat itu adalah salah satu sahaja bagi mana-mana komponen tertentu.

Alamat tidak berstruktur sepenuhnya — di mana keseluruhan alamat berada di dalam elemen AdrLine tanpa TwnNm atau Ctry — tidak akan diterima bagi mana-mana medan pihak yang terjejas. European Payments Council telah menyelaraskan buku peraturan SEPA-nya dengan peralihan yang sama, jadi mulai [15 November 2026 format tidak berstruktur juga diharamkan merentasi SCT, SDD, dan SCT Inst ⧉](https://clearingpost.com/insights/iso-20022-structured-address-deadline-november-2026/ "The November 2026 Structured Address Deadline: What Every PSP Needs to Do Now"). Penyelarasan ini sengaja: SWIFT dan EPC telah merekayasa satu hujung minggu peralihan industri tunggal.

Untuk mengelakkan keraguan, [dokumentasi pacs008 menyenaraikan mesej yang terjejas secara langsung ⧉](https://pacs008.com/structured-address/ "November 2026 structured-address deadline — pacs008"): pacs.008 (penghutang dan pemiutang dalam pindahan kredit pelanggan), pacs.009 (alamat institusi dalam pindahan kredit FI dan pembayaran lindungan), pacs.004 (alamat pihak dalam pemulangan), dan pacs.003 (debit terus). Keperluan ini juga mengalir ke hulu: fail pain.001 korporat yang membawa alamat tidak berstruktur akan menyekat penjanaan pacs.008 yang mematuhi di bank penerima.

## Mengapa Industri Menjadikan Ini Keutamaan

Hujah untuk alamat berstruktur bukanlah estetik. Ia adalah operasi, dan ia muncul di tiga tempat.

**Saringan sekatan.** Manfaat praktikal tunggal yang terbesar ialah alamat berstruktur membolehkan sistem saringan memisahkan nama pihak daripada data lokasi. Blok alamat teks bebas kerap menyebabkan positif palsu apabila nama bandar kebetulan bertindih dengan token nama orang yang disekat, atau apabila sebuah negara yang terbenam dalam teks bebas terlepas sama sekali. Medan berstruktur membolehkan enjin saringan menerapkan peraturan risiko khusus negara secara deterministik, dan ia memungkinkan penguatkuasaan pemadanan senarai sekatan terhadap kod negara dan bukannya meneka rentetan yang dihuraikan. Analisis CGI UK yang diterbitkan pada Mac 2026 menekankan perkara ini secara jelas: [data alamat berstruktur sedang menjadi teras kepada daya tahan operasi, bukan sekadar kewajipan pematuhan ⧉](https://www.cgi.com/uk/en-gb/blog/banking-and-financial-markets/2026-defining-year-iso-20022-and-structured-data-enforcement "2026: A defining year for ISO 20022 and structured data enforcement").

**Kadar pembaikan manual.** Pembayaran rentas sempadan hari ini membawa kos operasi yang ketara dalam bentuk siasatan manual, pengendalian pengecualian, dan barisan pembaikan — sebahagian besarnya didorong oleh alamat yang tidak dapat dihuraikan dengan yakin oleh sistem saringan atau penghalaan. Bank yang telah pun beralih kepada alamat berstruktur melaporkan pengurangan ketara dalam pengecualian pemprosesan lurus-terus, terutamanya dalam aliran koridor tengah di mana ejen perantara sebelum ini terpaksa mentafsir data teks bebas yang bukan mereka asalkan.

**Penguatkuasaan pada peringkat rangkaian.** SR2026 mengukuhkan pengesahan pada lapisan rangkaian SWIFT. Sesetengah semakan baharu akan beroperasi dalam mod tidak menyekat pada mulanya — menandakan isu kualiti data tanpa menghentikan pembayaran — tetapi trajektorinya jelas, dan selepas peralihan, [mesej yang tidak mematuhi akan ditolak terus ⧉](https://www.redcompasslabs.com/insights/iso-20022-is-arriving-all-at-once-for-us-banks/ "ISO 20022 is arriving all at once for US banks"). Beberapa laluan pembayaran AS (Fedwire, CHIPS) dan SWIFT CBPR+ sedang menumpu pada garis masa yang pada dasarnya sama, yang menghapuskan pilihan peralihan berperingkat yang telah diandaikan oleh sesetengah institusi dalam pelan terdahulu.

## Pandangan Peringkat Medan: Apa Yang Berubah Dalam Mesej

Mesej pacs.008 telah membawa sokongan alamat berstruktur sejak garis panduan penggunaan CBPR+ awal mula digunakan pada Mac 2023. Apa yang berubah pada November 2026 bukanlah skema — ia adalah pengesahan. Sehingga kini, bank telah dibenarkan untuk mengisi elemen AdrLine dengan teks bebas dan menghantarnya melalui rangkaian. Mulai tarikh akhir, kandungan blok pihak mesti memenuhi keperluan minimum medan berstruktur.

### Diperlukan, Disyorkan, dan Ditamatkan

| Elemen | XPath (di bawah `PstlAdr`) | Status selepas Nov 2026 | Nota |
|---|---|---|---|
| Nama Bandar | `<TwnNm>` | **Wajib** | Sekurang-kurangnya satu Nama Bandar berstruktur bagi setiap pihak yang terjejas |
| Negara | `<Ctry>` | **Wajib** | Kod ISO 3166-1 alpha-2 |
| Nama Jalan | `<StrtNm>` | Amat disyorkan | Diperlukan untuk format berstruktur sepenuhnya |
| Nombor Bangunan | `<BldgNb>` | Disyorkan | Sama ada BldgNb atau PstBx, bukan kedua-duanya |
| Peti Surat | `<PstBx>` | Disyorkan | Alternatif kepada BldgNb |
| Poskod | `<PstCd>` | Disyorkan | Diperlukan oleh sesetengah skema tempatan |
| Subbahagian Negara | `<CtrySubDvsn>` | Pilihan | Negeri, wilayah, provinsi |
| Baris Alamat (teks bebas) | `<AdrLine>` | **Terhad** | Maksimum 2 baris di bawah hibrid; tidak pernah bersama komponen yang sama dalam medan berstruktur |
| Jenis Alamat | `<AdrTp>` | Pilihan | Penggunaan `ADDR` disyorkan untuk alamat pos |

*Sumber: Sintesis garis panduan penggunaan SWIFT CBPR+ untuk SR2026 dan [dokumentasi alamat berstruktur pacs008.com ⧉](https://pacs008.com/structured-address/ "November 2026 structured-address deadline — pacs008").*

Implikasi praktikalnya ialah mana-mana institusi yang masih bergantung pada AdrLine sahaja — sama ada dalam penjanaan mesej sendiri, dalam fail pain.001 yang diterima daripada pelanggan korporat, atau dalam rekod data induk yang digunakan untuk memperkaya pembayaran semasa dalam aliran — perlu memindahkan data itu kepada medan berstruktur sebelum peralihan. Perkhidmatan terjemahan dalam aliran SWIFT boleh membantu semasa transit, tetapi [ia dikenakan surcaj mulai Januari 2026 ⧉](https://www.pcbb.com/products/international-banking/international-payments/iso20022-faq "ISO 20022 FAQ — PCBB") dan tidak dapat menghuraikan setiap format alamat dengan boleh dipercayai. SWIFT juga telah mengeluarkan [model penstrukturan alamat AI sumber terbuka ⧉](https://www.swift.com/standards/iso-20022/iso-20022-faqs/swift-ai-address-structuring-model "ISO 20022: The Swift AI address structuring model") yang dilatih pada data daripada lebih 200 negara untuk menyimpulkan Bandar dan Negara daripada data warisan tidak berstruktur dengan skor keyakinan, tetapi ia secara jelas adalah alat bantu pemulihan, bukan pengganti jangka panjang untuk data huluan yang bersih.

## Bagaimana pacs008.com Membantu Memampatkan Garis Masa

Bagi institusi yang perlu mengindustrialisasikan saluran kualiti alamat dan pengesahan mesej mereka dengan pantas, [pacs008 ⧉](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 Toolkit and API") menyediakan perkakas sumber terbuka berlesen MIT dan perkhidmatan FastAPI yang direka khusus untuk aliran kerja pindahan kredit pelanggan FI-ke-FI. Ia menangani tiga lapisan di mana program pemulihan paling kerap tersangkut: pengesahan data, penjanaan XML, dan penguatkuasaan saluran.

Keupayaan alamat berstruktur perkakas ini diselaraskan dengan keperluan SR2026:

- **Pengesahan pra-penjanaan** medan alamat pos berstruktur dan hibrid, supaya data yang tidak mematuhi ditangkap sebelum sebarang XML dihasilkan atau dihantar.
- **Penandaan data alamat tidak berstruktur** yang akan gagal selepas tarikh akhir November 2026, dengan perbezaan yang jelas antara kes hibrid-boleh-diterima dan kes tidak berstruktur sepenuhnya.
- **Sokongan dwi-format** untuk kedua-dua format hibrid pra-tarikh-akhir dan susun atur berstruktur sepenuhnya pasca-tarikh-akhir, membolehkan institusi berhijrah secara progresif tanpa merosakkan kesalingoperasian dengan rakan niaga yang belum menyelesaikan peralihan mereka sendiri.
- **Integrasi saluran CI** supaya semakan kualiti alamat menjadi sebahagian daripada proses binaan, bukan renungan akhir-aliran — jawapan praktikal kepada [pemerhatian CGI bahawa tadbir urus data mesti menjadi prinsip reka bentuk asas ⧉](https://www.cgi.com/uk/en-gb/blog/banking-and-financial-markets/2026-defining-year-iso-20022-and-structured-data-enforcement "2026: A defining year for ISO 20022 and structured data enforcement") dan bukannya lapisan pematuhan.

Selain alamat, perkakas ini merangkumi permukaan pengesahan yang lebih luas yang diperketatkan oleh keluaran SR2026: pengesahan JSON Schema terhadap 20 skema khusus mesej, pengesahan format dan checksum IBAN merentasi 75 negara, pengesahan XSD XML yang dijana terhadap skema [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) rasmi, dan penjanaan yang peka versi merentasi semua 13 semakan pacs.008 yang disokong (pacs.008.001.01 hingga pacs.008.001.13). Bagi pasukan operasi dan pematuhan, ia juga termasuk pencegahan XXE melalui defusedxml, perlindungan traversal-laluan yang ketat, dan pelindungan PII dalam log JSON berstruktur untuk menyokong keperluan GDPR dan PCI DSS — jenis kawalan yang tidak boleh dirunding dalam aliran pembayaran pengeluaran tetapi kerap dipasang semula lewat dalam migrasi yang dipimpin vendor.

Pustaka ini tersedia [di PyPI ⧉](https://pypi.org/project/pacs008/ "pacs008 on PyPI") sebagai pakej `pip install pacs008` dan di [GitHub ⧉](https://github.com/sebastienrousseau/pacs008 "pacs008 on GitHub") dengan ketelusan sumber penuh. Bagi institusi yang menilai pilihan mereka, ini penting: perkakas sumber terbuka membolehkan pasukan dalaman mengaudit logik pengesahan, mengintegrasikannya ke dalam ladang Python atau FastAPI sedia ada tanpa rundingan lesen, dan menyumbang baik pulih kembali apabila kes tepi mereka sendiri muncul.

Adalah wajar untuk berhati-hati tentang skop. pacs008 adalah perkakas lapisan-mesej; ia tidak menggantikan enjin pembayaran, sistem saringan, atau pemulihan data induk pelanggan yang masih perlu dilakukan oleh institusi di sumbernya. Apa yang ia lakukan ialah mengambil kerja pemulihan itu dan menjadikannya boleh dikuatkuasakan — mengubah pematuhan alamat berstruktur daripada semakan manual pada penghujung saluran yang panjang kepada pintu automatik pada titik penjanaan. Bagi program yang kesuntukan masa, pintu itu adalah perbezaan antara peralihan yang bersih dan lonjakan penolakan pasca-peralihan.

## Landskap Perkakas

pacs008 berada dalam ekosistem yang lebih luas bagi perkakas mesej [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html), dan pilihan pendekatan bergantung pada timbunan, skala, dan falsafah migrasi institusi. Landskap sumber terbuka dan komersial merangkumi [pyiso20022 ⧉](https://github.com/phoughton/pyiso20022 "pyiso20022 — an ISO 20022 message generator and parser") (pustaka Python berbilang kategori yang luas dengan pengesahan beta), pustaka [pain001 ⧉](https://pain001.com/ "Pain001 — Automate ISO 20022-compliant payment file creation") yang berkaitan untuk permulaan pembayaran huluan, [Prowide ISO 20022 ⧉](https://www.prowidesoftware.com/development-tools/iso20022 "Prowide ISO 20022 — open source MX message parser for Java") (pustaka Java Apache 2.0 yang komprehensif dengan lapisan komersial untuk pengesahan dan terjemahan CBPR+), dan beberapa platform komersial — Mambu, Kyriba, PaymentComponents, dan lain-lain — yang menggabungkan keupayaan [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) ke dalam tawaran platform perbendaharaan atau pembayaran yang lebih luas.

Pertukaran timbang tara adalah biasa. Platform komersial mengurangkan beban kejuruteraan dalaman tetapi mengikat institusi kepada pelan hala tuju vendor yang mungkin tidak sepadan dengan miliknya sendiri. Pustaka berbilang kategori yang komprehensif merangkumi permukaan yang lebih luas tetapi memerlukan lebih banyak kerja integrasi bagi mana-mana jenis mesej tunggal. Pustaka sumber terbuka yang fokus — pacs008 untuk pindahan kredit pelanggan FI-ke-FI, [pain001](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) untuk permulaan pembayaran — meminimumkan masa integrasi bagi institusi yang perlu menangani halangan tertentu dengan pantas, dan ia membiarkan institusi mengawal peraturan pengesahannya sendiri. Untuk masalah alamat berstruktur khususnya, pendekatan yang fokus mempunyai kelebihan bahawa peraturan yang dikuatkuasakan adalah sempit, jelas ditakrifkan, dan tidak mungkin berubah sebelum peralihan.

## Apa Maknanya Mengikut Sektor

Tarikh akhir November 2026 tidak menjejaskan semua institusi secara sama rata. Tindak balas yang betul bergantung pada jumlah trafik rentas sempadan, kematangan ladang data sedia ada, dan peranan yang dimainkan oleh institusi dalam rantaian pembayaran.

### Bank Koresponden dan Rentas Sempadan Besar

Bagi bank peringkat pertama yang menjalankan trafik CBPR+ yang ketara, keperluan alamat berstruktur adalah satu aliran kerja dalam program kesediaan SR2026 yang jauh lebih besar yang juga merangkumi pengecualian dan siasatan, pengukuhan BAH, dan (di AS) migrasi Fedwire dan CHIPS secara serentak. Data RedCompass Labs mencadangkan kebanyakan institusi ini membelanjakan $20–30 juta untuk kesediaan 2026, dengan pasukan penyampaian 10–20 pakar. Risiko bagi kumpulan ini bukanlah keupayaan teknikal — ia adalah kapasiti penyampaian. Dengan pelbagai aliran kerja selari bersaing untuk tetingkap keluaran yang sama, pemulihan kualiti alamat boleh secara senyap tertinggal di belakang aliran kerja yang lebih ketara sehingga ia menjadi masalah minggu-peralihan. Mitigasi praktikalnya ialah membawa pengesahan alamat ke hadapan dalam saluran, supaya kegagalan muncul dalam persekitaran pembangunan dan ujian beberapa bulan sebelum ia sampai ke pengeluaran.

### Bank Peringkat Pertengahan dan Institusi Pembayaran

Bagi bank peringkat pertengahan dan institusi EMI/PI, keperluan alamat berstruktur seringkali merupakan kewajipan 2026 yang paling ketara yang mereka hadapi, kerana mereka tidak membawa beban aliran kerja sekeliling yang sama seperti bank peringkat pertama. Cabaran di sini biasanya adalah kualiti data huluan. Proses pendaftaran pelanggan yang telah menangkap alamat sebagai teks bebas selama beberapa dekad menghasilkan ladang data induk yang tidak mudah dihuraikan. Pemulihan automatik — menggunakan model penstrukturan alamat sumber terbuka SWIFT, perkhidmatan pembersihan alamat komersial, atau gabungan — boleh menangani sebahagian besar rekod, tetapi ekor panjang baki bagi alamat antarabangsa yang kompleks akan memerlukan semakan manual. Semakin awal kerja ini bermula, semakin kecil ekor itu menjadi.

### Korporat dan Pembekal Perkhidmatan Pembayaran

Korporat yang memulakan pembayaran melalui pain.001 berada di hulu penjanaan pacs.008 bank tetapi tidak terkecuali daripada keperluan alamat berstruktur. Bank tidak akan mengisi alamat penerima secara retroaktif bagi pihak pelanggan korporat; data berstruktur mesti berasal daripada sistem korporat itu sendiri. Bagi bendahari korporat, ini bermakna memastikan bahawa sistem ERP dan perbendaharaan menangkap alamat penerima dalam bentuk berstruktur, bahawa maklumat penandatangan dan penghutang muktamad turut berstruktur, dan bahawa templat permulaan pembayaran tidak menggugurkan medan secara senyap semasa penjanaan fail. Pengesahan pra-penerbangan fail pain.001 — menggunakan sama ada perkakas korporat itu sendiri atau perkhidmatan yang didedahkan oleh bank — sedang menjadi titik kawalan praktikal.

### Vendor, Fintech, dan Penyepadu Sistem

Bagi vendor yang membina di atas laluan pembayaran, tarikh akhir ini adalah fungsi pemaksa untuk keupayaan [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) yang mungkin telah ditolak ke fasa kemudian. Fintech yang menghala atau memulakan pembayaran rentas sempadan melalui rakan kongsi perbankan perlu mendedahkan penangkapan alamat berstruktur dalam UI dan API mereka sendiri, atau menerima bahawa fail pain.001 yang mematuhi tidak dapat dihasilkan daripada data mereka. Peluangnya, bagi vendor yang boleh bergerak pantas, ialah menyerap beban pemulihan bagi pihak pelanggan korporat — mengubah masalah pematuhan menjadi perkhidmatan.

## Kesimpulan

Tarikh akhir alamat berstruktur November 2026, dalam satu erti kata, adalah perubahan yang sempit: dua medan wajib, beberapa yang disyorkan, dan penamatan pilihan teks bebas yang sepatutnya tidak pernah digunakan untuk data berkaitan sekatan di tempat pertama. Dalam erti kata lain, ia adalah pencapaian [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) yang paling ketara dari segi operasi sejak migrasi CBPR+ asal, kerana ia memaksa data berstruktur bukan sahaja ke dalam lapisan mesej tetapi ke dalam sistem huluan yang menyuapkannya.

Gambaran kesediaan peringkat industri, enam bulan sebelumnya, tidak menggalakkan. Dua pertiga mesej CBPR+ masih membawa alamat tidak berstruktur. Hampir separuh bank tidak berada pada landasan. Hampir satu pertiga rekod alamat pelanggan kekal tidak dapat dihuraikan. Pembiayaan sudah tersedia — tinjauan secara konsisten menunjukkan pelaburan lapan dan sembilan angka — tetapi kerja itu belum, dan dimensi kualiti data bagi masalah ini tidak dapat diselesaikan dengan perbelanjaan sahaja pada bulan-bulan terakhir.

Apa yang membantu sekarang adalah automasi pada titik pengesahan: menolak peraturan ke dalam saluran yang menangkap masalah sebelum ia sampai ke rangkaian, dan bukannya selepasnya. Bagi institusi yang menjalankan ladang Python atau FastAPI, perkakas sumber terbuka seperti [pacs008 ⧉](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 Toolkit and API") menyediakan cara praktikal untuk membuat peralihan itu tanpa kitaran pemilihan vendor. Bagi semua orang, tanpa mengira timbunan, titik strategiknya adalah sama: institusi yang mengindustrialisasikan perubahan sekarang akan berada dalam kedudukan yang jauh lebih kuat berbanding yang bergantung pada pematuhan saat akhir — untuk meminjam frasa penyelidikan RedCompass Labs yang telah membingkai sebahagian besar perbualan 2026.

Hujung minggu peralihan pada November akan menutup satu bab. Institusi yang tiba dengan data yang bersih, pengesahan automatik, dan pemahaman yang berfungsi tentang apa yang sebenarnya dilakukan oleh alamat berstruktur untuk saringan sekatan akan menghabiskan hujung minggu itu memantau trafik. Mereka yang tiba tanpa perkara-perkara itu akan menghabiskannya di telefon.

## Soalan Lazim

**Apa sebenarnya yang berubah pada tarikh akhir November 2026?**

Mulai pertengahan November 2026, SWIFT CBPR+ akan menolak mesej pacs.008, pacs.009, pacs.004, dan pacs.003 yang medan pihaknya mengandungi alamat pos tidak berstruktur sahaja. Keperluan berstruktur minimum ialah Nama Bandar dalam elemen TwnNm dan Negara dalam elemen Ctry (menggunakan kod ISO 3166-1 alpha-2). Alamat hibrid masih dibenarkan — Bandar dan Negara dalam medan berstruktur, ditambah sehingga dua elemen AdrLine teks bebas untuk komponen yang selebihnya — tetapi komponen yang sama tidak boleh muncul dalam kedua-dua medan berstruktur dan tidak berstruktur. Alamat berstruktur sepenuhnya adalah format yang diutamakan. European Payments Council telah menyelaraskan skema SEPA (SCT, SDD, SCT Inst) dengan tarikh peralihan yang sama.

**Mesej mana dan medan pihak mana yang terjejas?**

Bagi pacs.008, keperluan ini terpakai kepada alamat pos penghutang dan pemiutang. Bagi pacs.009, ia terpakai kepada alamat institusi dalam pindahan kredit FI dan pembayaran lindungan. Bagi pacs.004, ia terpakai kepada alamat pihak dalam pemulangan pembayaran. Bagi pacs.003, ia terpakai kepada alamat pemiutang dan penghutang dalam debit terus pelanggan. Mesej penyata dan pemberitahuan (camt.052, camt.053, camt.054) dan mesej pentadbiran tertentu kekal di luar keperluan ketat. Mesej pain.001 huluan daripada pelanggan korporat tidak dikawal secara langsung oleh CBPR+, tetapi alamat tidak berstruktur dalam fail pain.001 akan menyekat penjanaan pacs.008 yang mematuhi di hiliran dan oleh itu secara efektif berada dalam skop.

**Apakah perbezaan antara alamat berstruktur, hibrid, dan tidak berstruktur?**

Alamat berstruktur sepenuhnya memetakan setiap komponen kepada elemen [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) khususnya: StrtNm, BldgNb atau PstBx, PstCd, TwnNm, CtrySubDvsn, Ctry. Alamat hibrid mempunyai Nama Bandar dan Negara dalam medan berstruktur, dengan selebihnya alamat dalam sehingga dua elemen AdrLine teks bebas; komponen yang sama tidak boleh muncul dalam kedua-duanya. Alamat tidak berstruktur mempunyai keseluruhan alamat pos dalam elemen AdrLine tanpa TwnNm atau Ctry berstruktur — inilah format yang sedang ditamatkan pada November 2026 bagi medan pihak yang terjejas.

**Bagaimana pacs008.com membantu peralihan ini?**

Pustaka [pacs008 ⧉](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 Toolkit and API") mengesahkan medan alamat pos berstruktur dan hibrid sebelum penjanaan XML, menandakan data tidak berstruktur yang akan gagal selepas tarikh akhir, menyokong kedua-dua format hibrid pra-tarikh-akhir dan berstruktur sepenuhnya pasca-tarikh-akhir, dan mengintegrasikan ke dalam saluran CI dan aliran kerja pengesahan kelompok. Ia menjana XML untuk semua 13 versi pacs.008 yang disokong, mengesahkan terhadap skema XSD [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) rasmi, dan mendedahkan perkhidmatan FastAPI untuk penyelarasan automatik. Ia adalah sumber terbuka di bawah lesen gaya-MIT, tersedia di PyPI, dan direka khusus untuk aliran kerja pindahan kredit pelanggan FI-ke-FI — jadi peraturan pengesahannya ditentukur mengikut garis panduan penggunaan CBPR+ SR2026 dan bukannya diabstrakkan merentasi banyak jenis mesej.

**Apa yang berlaku jika institusi saya belum bersedia menjelang November 2026?**

Mesej dengan alamat tidak berstruktur dalam medan pihak yang terjejas akan ditolak pada peringkat rangkaian selepas peralihan. Secara praktikal, ini diterjemahkan kepada kegagalan pembayaran, peningkatan jumlah pengecualian, lonjakan pembaikan manual, dan kemungkinan kesan kepada pelanggan. Perkhidmatan terjemahan dalam aliran SWIFT tersedia untuk sesetengah kes peralihan tetapi dikenakan surcaj mulai Januari 2026 dan tidak dapat menghuraikan setiap format alamat dengan boleh dipercayai. SWIFT juga telah mengeluarkan model penstrukturan alamat AI sumber terbuka yang menyimpulkan Bandar dan Negara daripada data tidak berstruktur warisan, tetapi ia direka untuk pemulihan dan prapemprosesan, bukan sebagai pengganti kekal untuk data huluan yang bersih. Institusi yang tiba pada tarikh akhir tanpa ladang data induk pelanggan yang telah dipulihkan dan saluran pengesahan automatik harus menjangkakan minggu peralihan yang sukar dan peningkatan operasi yang ketara pada bulan-bulan berikutnya.

## Rujukan

- Sebastien Rousseau, (2023). [Automating ISO 20022-Compliant Payment File Creation with Pain001](https://sebastienrousseau.com/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html "Automating ISO 20022-Compliant Payment File Creation with Pain001").
- pacs008, (2026). [November 2026 structured-address deadline ⧉](https://pacs008.com/structured-address/ "November 2026 structured-address deadline — pacs008"). pacs008.com.
- pacs008, (2026). [pacs008 — ISO 20022 pacs.008 Toolkit and API ⧉](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 Toolkit and API"). pacs008.com.
- SWIFT, (2026). [ISO 20022 milestone for November 2026: Unstructured addresses to be removed ⧉](https://www.swift.com/news-events/news/iso-20022-milestone-november-2026-unstructured-addresses-be-removed "ISO 20022 milestone for November 2026: Unstructured addresses to be removed"). SWIFT.
- SWIFT, (2026). [ISO 20022 for Financial Institutions ⧉](https://www.swift.com/standards/iso-20022/iso-20022-financial-institutions-focus-payments-instructions "ISO 20022 for Financial Institutions"). SWIFT.
- SWIFT, (2026). [The Swift AI address structuring model ⧉](https://www.swift.com/standards/iso-20022/iso-20022-faqs/swift-ai-address-structuring-model "ISO 20022: The Swift AI address structuring model"). SWIFT.
- RedCompass Labs, (2026). [Nearly Half of Banks Are Behind on ISO 20022 ⧉](https://financialit.net/news/banking/nearly-half-banks-are-behind-iso-20022 "Nearly Half of Banks Are Behind on ISO 20022"). Financial IT.
- RedCompass Labs, (2026). [ISO 20022 is arriving all at once for US banks ⧉](https://www.redcompasslabs.com/insights/iso-20022-is-arriving-all-at-once-for-us-banks/ "ISO 20022 is arriving all at once for US banks"). RedCompass Labs.
- ClearingPost, (2026). [The November 2026 Structured Address Deadline: What Every PSP Needs to Do Now ⧉](https://clearingpost.com/insights/iso-20022-structured-address-deadline-november-2026/ "The November 2026 Structured Address Deadline"). ClearingPost.
- CGI UK, (2026). [2026: A defining year for ISO 20022 and structured data enforcement ⧉](https://www.cgi.com/uk/en-gb/blog/banking-and-financial-markets/2026-defining-year-iso-20022-and-structured-data-enforcement "2026: A defining year for ISO 20022 and structured data enforcement"). CGI UK.
- J.P. Morgan, (2026). [ISO 20022 Migration: Guidance, Messaging & More ⧉](https://www.jpmorgan.com/insights/payments/fx-cross-border/iso-20022-migration "ISO 20022 Migration: Guidance, Messaging & More"). J.P. Morgan.
- ING, (2026). [FAQ Swift ISO 20022 ⧉](https://www.ingwb.com/en/service/payments-and-collections/swift-iso20022/faq-swift-iso-20022 "FAQ Swift ISO 20022 — ING"). ING Wholesale Banking.
- Mambu, (2026). [CBPR+ is live: what ISO 20022 means in practice ⧉](https://mambu.com/en/insights/articles/cbpr-is-live-what-iso-20022-means-in-practice "CBPR+ is live: what ISO 20022 means in practice"). Mambu.
- Kyriba, (2026). [ISO 20022 migration: what every treasury team needs to know about what's next ⧉](https://www.kyriba.com/blog/iso-20022-corporate-treasury-2026/ "ISO 20022 migration: what every treasury team needs to know about what's next"). Kyriba.
- Standard Chartered, (2025). [ISO 20022 – Standard Chartered Address Guidelines (H2H and API) ⧉](https://www.sc.com/en/uploads/sites/66/content/docs/sc-cib-tb-ISO-20022%E2%80%93CBPR-Address-guidelines-H2H-and-API-sept-2025.pdf "Standard Chartered ISO 20022 Address Guidelines"). Standard Chartered.
- State Street, (2025). [Client Guide to ISO 20022 ⧉](https://www.statestreet.com/web/insights/articles/documents/state-street-client-guide-to-iso-20022-2025.pdf "State Street Client Guide to ISO 20022 2025"). State Street.
- ISO 20022, (2026). [Message Definitions Catalogue ⧉](https://www.iso20022.org/iso-20022-message-definitions "ISO 20022 Message Definitions"). ISO 20022.
