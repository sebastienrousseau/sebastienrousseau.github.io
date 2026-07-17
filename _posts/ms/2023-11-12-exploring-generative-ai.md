---
title: "AI Generatif pada 2023: Cara Ia Berfungsi, Di Mana Ia Mendarat"
tags: "generative AI, LLM, GPT-4, transformer, financial services, hallucination, RAG, AI governance, foundation model, fine-tuning, ISO 20022, DORA, post-quantum cryptography, quantum computing, AI"
subtitle: "Kecerdasan buatan gunaan dalam perbankan dan perkhidmatan kewangan."
description: "Terokai AI Generatif pada 2023: cara ia berfungsi, di mana ia mendarat dahulu dalam perkhidmatan kewangan, dan persoalan etika serta seni bina yang wajar ditanya."
date: "Nov 12, 2023"
language: "ms"
locale: "ms_MY"
banner: "https://cloudcdn.pro/stocks/images/getty-images-aTWKwJllPOA.webp"
banner_alt: "Visualisasi rangkaian neural abstrak dalam nada biru dan ungu yang mewakili pemprosesan AI"
keywords: "AI generatif, model bahasa besar, seni bina transformer, GPT-4, AI perkhidmatan kewangan, halusinasi, penjanaan diperkukuh perolehan, tadbir urus AI, model asas, penalaan halus"
---

![Visualisasi rangkaian neural abstrak dalam nada biru dan ungu yang mewakili pemprosesan AI](https://cloudcdn.pro/stocks/images/getty-images-aTWKwJllPOA.webp).class=\"img-fluid clearfix\"

> **Ringkasan Eksekutif / Intipati Utama**
>
> - **Seni bina yang mengubah segalanya.** Makalah transformer 2017 memperkenalkan swaperhatian (self-attention): satu mekanisme yang mengira pemberat kaitan antara setiap pasangan token dalam input, menggantikan pemprosesan berjujukan RNN dengan operasi matriks yang boleh diselarikan. Setiap model bahasa utama pada 2023 ialah varian transformer ([Vaswani et al., 2017](https://arxiv.org/abs/1706.03762 "Attention Is All You Need")).
> - **GPT-4 sebagai penanda aras 2023.** Dikeluarkan pada Mac 2023, GPT-4 memperoleh markah pada persentil ke-90 dalam peperiksaan Bar Amerika Syarikat, ke-99 dalam GRE Verbal, dan menunjukkan penaakulan berbilang langkah merentasi dokumen panjang. Ia menetapkan penanda aras keupayaan yang disasarkan untuk dicapai atau diatasi oleh model berikutnya ([OpenAI, 2023](https://arxiv.org/abs/2303.08774 "GPT-4 Technical Report")).
> - **Model pemberat terbuka mendemokrasikan akses.** Llama 2 daripada Meta (Julai 2023) dan Mistral 7B daripada Mistral AI (September 2023) menunjukkan bahawa model yang setanding dengan keupayaan kelas GPT-3.5 boleh dijalankan pada infrastruktur persendirian, menangani keperluan pemastautinan data bagi industri yang dikawal selia.
> - **Perintis perkhidmatan kewangan pada 2023.** Penggunaan meluas menjelang penghujung 2023 termasuk semakan kontrak undang-undang (penyelidikan DocLLM oleh JPMorgan), pemantauan perubahan kawal selia, dan alat produktiviti pembangun. Goldman Sachs melaporkan penggunaan dalaman pembantu pengekodan AI merentasi 10,000 pembangun.
> - **Halusinasi ialah penghalang pengeluaran.** LLM menjana output yang kedengaran munasabah tetapi tidak tepat dari segi fakta pada kadar yang tidak remeh. Dalam kes penggunaan yang dikawal selia (keputusan kredit, pendapat pematuhan, pendedahan pelanggan) halusinasi bukanlah kecacatan kosmetik; ia merupakan risiko kawal selia dan liabiliti yang memerlukan mitigasi seni bina seperti penjanaan diperkukuh perolehan (RAG).

---

## Cara Seni Bina Transformer Berfungsi

Setiap model bahasa penting yang digunakan pada 2023 (GPT-4, Claude 2, Llama 2, Mistral, Falcon) dibina di atas seni bina transformer yang diperkenalkan dalam makalah 2017 "Attention Is All You Need." Memahami mekanisme teras menjelaskan kedua-dua sebab model ini berfungsi dan di mana ia gagal.

**Token dan embedding.** Model bermula dengan memecahkan teks input kepada token sub-perkataan (biasanya menggunakan pengekodan pasangan bait). Setiap token dipetakan kepada vektor berdimensi tinggi (satu embedding) yang mengekod hubungan semantiknya dengan token lain, yang dipelajari semasa pra-latihan.

**Swaperhatian.** Bagi setiap token, model mengira tiga vektor: Query (apa yang dicari oleh token ini), Key (apa yang ditawarkan oleh token ini), dan Value (apa yang disumbangkan oleh token ini). Skor perhatian dikira dengan mengambil hasil darab titik setiap Query terhadap semua Key, menggunakan softmax untuk menghasilkan pemberat, dan menjumlahkan Value yang dipemberatkan oleh skor tersebut. Ini bermakna setiap token memberi perhatian kepada setiap token lain dalam tetingkap konteks secara serentak, iaitu mekanisme yang memberikan transformer keupayaannya untuk mengendalikan kebergantungan jarak jauh.

**Perhatian berbilang kepala.** Beberapa kepala perhatian berjalan selari, setiap satu mempelajari jenis hubungan yang berbeza (sintaksis, semantik, kedudukan). Output mereka dicantumkan dan diunjurkan secara linear.

**Lapisan suap ke hadapan.** Selepas perhatian, setiap kedudukan melalui dua transformasi linear dengan pengaktifan tak linear. Lapisan ini melaksanakan pengiraan setiap token secara bebas, menangkap transformasi ciri setempat.

**Skala.** GPT-4 dianggarkan melebihi satu trilion parameter (tidak disahkan oleh OpenAI). Llama 2 70B menggunakan 70 bilion. Mistral 7B menggunakan 7 bilion, dengan perhatian pertanyaan berkumpulan dan perhatian tetingkap gelongsor untuk kecekapan. Model yang lebih besar secara umumnya mempamerkan penaakulan zero-shot dan few-shot yang lebih baik, iaitu keupayaan bermunculan yang menjadikannya berguna untuk tugas yang ia tidak dilatih secara eksplisit.

## Landskap Model 2023

Tahun 2023 menghasilkan lebih banyak keluaran model penting berbanding mana-mana tahun sebelumnya:

**GPT-4 (OpenAI, Mac 2023).** Berbilang mod (input teks + imej), tetingkap konteks sehingga 128,000 token dalam varian GPT-4 Turbo kemudian, penaakulan berbilang langkah yang kukuh. Menetapkan penanda aras untuk tugas domain profesional.

**Claude 2 (Anthropic, Julai 2023).** Tetingkap konteks 100,000 token (terpanjang semasa pelancaran), prestasi kukuh pada tugas dokumen panjang seperti semakan kontrak dan analisis kawal selia. Latihan Constitutional AI untuk mengurangkan output berbahaya.

**Llama 2 (Meta, Julai 2023).** Keluaran pemberat terbuka dalam varian parameter 7B, 13B, 34B, dan 70B. Penggunaan komersial dibenarkan. Membolehkan penggunaan di premis sendiri bagi industri yang dikawal selia. Melahirkan ratusan varian yang ditala halus (Code Llama, Vicuna, WizardLM).

**Mistral 7B (Mistral AI, September 2023).** Model 7 bilion parameter yang mengatasi Llama 2 13B pada kebanyakan penanda aras. Perhatian pertanyaan berkumpulan dan perhatian tetingkap gelongsor mengurangkan kos inferens. Model perintis Eropah yang signifikan pertama, relevan memandangkan konteks GDPR dan Akta AI EU.

**Falcon 180B (TII, September 2023).** Model pemberat terbuka 180 bilion parameter, dilatih pada 3.5 trilion token data RefinedWeb. Menunjukkan bahawa model pemberat terbuka boleh menghampiri skala kelas GPT-4.

## Di Mana AI Generatif Mendarat Dahulu dalam Perkhidmatan Kewangan

Menjelang penghujung 2023, institusi kewangan telah beralih daripada eksperimen dalaman kepada program perintis berstruktur dalam beberapa kes penggunaan yang berbeza:

**Produktiviti pembangun.** Alat penjanaan kod (GitHub Copilot, Amazon CodeWhisperer, model yang ditala halus secara dalaman) menjadi kategori yang paling meluas digunakan. Goldman Sachs melaporkan bahawa 10,000 pembangun mempunyai akses kepada bantuan pengekodan AI. Morgan Stanley menggunakan GPT-4 secara dalaman untuk membantu penasihat kewangan memperoleh maklumat daripada pangkalan pengetahuan 100,000 dokumen.

**Pemprosesan dokumen undang-undang dan kawal selia.** Pengekstrakan klausa kontrak, pemantauan perubahan kawal selia, dan pemetaan pematuhan merupakan perintis bernilai tertinggi. Penyelidikan JPMorgan tentang DocLLM menunjukkan bahawa model bahasa yang sedar susun atur dokumen mengatasi LLM generik pada tugas pemahaman dokumen kewangan.

**Peningkatan khidmat pelanggan.** Bank menggunakan pembantu berkuasa LLM untuk pertanyaan pelanggan barisan pertama, dengan peningkatan kepada manusia bagi nasihat yang dikawal selia. Kekangan utama: model tidak boleh memberikan nasihat yang dikawal selia, tidak boleh berhalusinasi tentang terma produk, dan mesti boleh diaudit.

**Penjanaan naratif KYC dan AML.** Meringkaskan corak transaksi kompleks dan profil pelanggan untuk semakan penganalisis, menggantikan kerja penulisan manual sebelumnya, muncul sebagai kes penggunaan yang boleh dipercayai dengan risiko halusinasi lebih rendah kerana model meringkaskan data yang diberikan dan bukannya menjana dakwaan baharu.

## Risiko Yang Didedahkan oleh Pengeluaran

Peralihan daripada demo kepada pengeluaran dalam perkhidmatan kewangan mendedahkan satu set risiko yang memerlukan tindak balas seni bina:

**Halusinasi.** LLM menjana output tidak tepat yang kedengaran yakin pada kadar yang berbeza mengikut jenis tugas dan model. Pada tugas ingatan fakta, walaupun GPT-4 berhalusinasi pada kadar yang tidak boleh diterima untuk pendapat pematuhan atau pendedahan kredit. Mitigasi utama ialah penjanaan diperkukuh perolehan (RAG): mengasaskan output model pada dokumen yang diperoleh dan boleh disahkan, bukannya bergantung pada pengetahuan berparameter semata-mata.

**Suntikan gesaan.** Input bermusuhan yang tertanam dalam dokumen atau mesej pengguna boleh mengalihkan tingkah laku model. Dalam perkhidmatan kewangan, di mana LLM memproses dokumen tidak dipercayai (kontrak, e-mel, penyerahan pelanggan), suntikan gesaan ialah risiko keselamatan pengeluaran, bukan teori semata-mata.

**Kebocoran data.** Model yang ditala halus atau digesa pada data sulit boleh menghasilkan semula data tersebut dalam output, iaitu risiko material untuk PII, kedudukan dagangan, dan maklumat pelanggan. Kawalan seni bina (penggunaan persendirian, pengurusan data-dalam-konteks, penapisan output) diperlukan, bukan pilihan.

**Asal usul model dan kebolehauditan.** Pengawal selia mengharapkan institusi kewangan menjelaskan keputusan automatik. LLM yang menghasilkan penilaian kredit tanpa jejak penaakulan yang boleh diaudit gagal memenuhi keperluan kebolehjelasan Perkara 22 GDPR, peruntukan AI berisiko tinggi Akta AI EU, dan panduan risiko model FCA yang sedia ada.

**Pengetahuan lapuk.** LLM mempunyai titik potong latihan. Model yang dilatih pada data sehingga awal 2023 tidak mengetahui tentang perubahan kawal selia, keputusan kadar, atau peristiwa pasaran selepas tarikh tersebut, iaitu batasan penting bagi kes penggunaan pematuhan masa nyata atau ulasan pasaran tanpa RAG atau perolehan masa nyata.

## Keperluan Tadbir Urus Sebelum Penggunaan

Pengamal perkhidmatan kewangan yang beroperasi pada 2023 tidak menunggu kepastian kawal selia sebelum melaksanakan penggunaan, tetapi institusi terkemuka menerima pakai rangka kerja pengurusan risiko model (MRM) yang disesuaikan daripada panduan SR 11-7 dan SS3/18:

**Inventori dan dokumentasi model.** LLM yang digunakan untuk fungsi perniagaan memerlukan dokumentasi tentang asal usul data latihan, metodologi penalaan halus, mod kegagalan yang diketahui, dan prestasi pada set pengesahan khusus domain.

**Titik semak manusia-dalam-gelung.** Untuk output yang dikawal selia (keputusan kredit, pendapat pematuhan, pendedahan pelanggan), semakan manusia kekal wajib pada 2023. Automasi digunakan untuk penyediaan draf dan peringkasan; kelulusan akhir kekal di tangan manusia.

**Risiko vendor.** Penggunaan API model pihak ketiga (OpenAI, Anthropic, Google) memperkenalkan risiko penumpuan vendor, risiko pemastautinan data, dan risiko perubahan model (penyedia boleh mengemas kini model secara senyap). Perjanjian perusahaan dan penggunaan persendirian sebahagiannya memitigasi perkara ini.

**Penglibatan kawal selia.** FCA, PRA, ECB, dan FINRA kesemuanya mengeluarkan makalah atau ucapan tentang tadbir urus AI pada 2023. Mesej yang konsisten: rangka kerja risiko model sedia ada terpakai kepada AI, dan firma seharusnya proaktif dalam mendokumentasikan pendekatan tadbir urus mereka sebelum panduan formal dikeluarkan.

## Soalan Lazim

**Apakah perbezaan antara model bahasa besar dan model asas?**

Model bahasa besar (LLM) ialah model yang dilatih pada data teks secara skala besar untuk meramal dan menjana bahasa. Model asas ialah istilah yang lebih luas bagi mana-mana model pra-latihan besar yang boleh disesuaikan (ditala halus atau digesa) untuk pelbagai tugas hiliran, termasuk LLM tetapi juga model penglihatan, model kod, dan model berbilang mod. GPT-4 ialah kedua-dua LLM dan model asas. DALL-E 3 ialah model asas tetapi bukan LLM. Dalam amalan, istilah ini sering digunakan secara bergantian apabila merujuk kepada sistem penjanaan teks.

**Apakah penjanaan diperkukuh perolehan dan mengapa ia penting bagi perkhidmatan kewangan?**

RAG menggabungkan model bahasa dengan sistem perolehan: dan bukannya bergantung semata-mata pada pengetahuan berparameter model (apa yang dipelajarinya semasa latihan), RAG mengambil dokumen relevan pada masa inferens dan menyediakannya sebagai konteks. Ini mengurangkan halusinasi dengan ketara pada tugas fakta kerana model mensintesis teks yang diberikan dan bukannya mengingati fakta yang dipelajari. Bagi perkhidmatan kewangan, RAG membolehkan kes penggunaan seperti pemantauan perubahan kawal selia (sentiasa memperoleh peraturan semasa) dan semakan kontrak (mengasaskan model pada teks kontrak sebenar) yang terlalu terdedah kepada halusinasi dengan pendekatan penjanaan tulen.

**Bagaimana institusi kewangan patut mengendalikan Akta AI EU berkaitan penggunaan AI generatif pada 2023?**

Akta AI EU masih dalam proses perundangan pada 2023 (diluluskan oleh Parlimen Eropah pada Mac 2024, berkuat kuasa Ogos 2024). Namun begitu, institusi dengan operasi EU atau pelanggan EU sudah pun menilai saluran paip mereka. Sistem AI berisiko tinggi dalam pemarkahan kredit, keputusan pekerjaan, dan infrastruktur kritikal memerlukan penilaian pematuhan, mekanisme pengawasan manusia, dan pengelogan audit. Model AI tujuan umum (GPAI), yang merangkumi model asas seperti GPT-4, mempunyai lapisan keperluan tersendiri berkaitan ketelusan dan risiko sistemik. Firma yang memulakan kerja dokumentasi dan tadbir urus pada 2023 berada dalam kedudukan lebih baik untuk tarikh akhir pelaksanaan.

**Apakah perbezaan praktikal antara penalaan halus dan kejuruteraan gesaan bagi penggunaan LLM perusahaan?**

Penalaan halus mengubah suai pemberat model dengan menyambung latihan pada data khusus domain, iaitu ia mengajar model pengetahuan dan corak tingkah laku baharu. Ia memerlukan data latihan berlabel, belanjawan pengiraan, dan penyelenggaraan berterusan apabila model asas dikemas kini. Kejuruteraan gesaan (termasuk contoh few-shot dan gesaan sistem) membentuk tingkah laku pada masa inferens tanpa mengubah pemberat, iaitu lebih pantas untuk dilaksanakan dan dikemas kini, tetapi terhad oleh apa yang model asas sudah ketahui. Bagi kebanyakan penggunaan perkhidmatan kewangan pada 2023, RAG berserta kejuruteraan gesaan ialah titik permulaan yang diutamakan; penalaan halus dikhaskan untuk kes di mana model perlu mempelajari terminologi proprietari atau menerima pakai format output yang ketat.

## Rujukan

- Vaswani, A., et al., (2017). [Attention Is All You Need ⧉](https://arxiv.org/abs/1706.03762 "Attention Is All You Need").
- OpenAI, (2023). [GPT-4 Technical Report ⧉](https://arxiv.org/abs/2303.08774 "GPT-4 Technical Report").
- Touvron, H., et al., Meta AI, (2023). [Llama 2: Open Foundation and Fine-Tuned Chat Models ⧉](https://arxiv.org/abs/2307.09288 "Llama 2").
- Jiang, A., et al., Mistral AI, (2023). [Mistral 7B ⧉](https://arxiv.org/abs/2310.06825 "Mistral 7B").
