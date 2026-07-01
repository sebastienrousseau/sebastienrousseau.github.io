---
title: "AI Generatif pada 2023: Cara Kerja dan Area Penerapannya"
subtitle: "Kecerdasan buatan terapan dalam perbankan dan jasa keuangan."
description: "Telusuri AI Generatif pada 2023: bagaimana cara kerjanya, di mana pertama kali diterapkan dalam jasa keuangan, serta pertanyaan etika dan arsitektur yang perlu diajukan."
date: "Nov 12, 2023"
language: "id-ID"
locale: "id_ID"
banner: "https://cloudcdn.pro/stocks/images/getty-images-aTWKwJllPOA.webp"
banner_alt: "Visualisasi jaringan saraf abstrak bernuansa biru dan ungu yang merepresentasikan pemrosesan AI"
keywords: "AI generatif, large language model, arsitektur transformer, GPT-4, AI jasa keuangan, halusinasi, retrieval-augmented generation, tata kelola AI, foundation model, fine-tuning"
---

![Visualisasi jaringan saraf abstrak bernuansa biru dan ungu yang merepresentasikan pemrosesan AI](https://cloudcdn.pro/stocks/images/getty-images-aTWKwJllPOA.webp).class=\"img-fluid clearfix\"

<!-- lead-start -->
<aside class="post-lead" aria-label="Ringkasan artikel">
<p class="post-lead-tldr"><strong>TL;DR.</strong> Telusuri AI Generatif pada 2023: bagaimana cara kerjanya, di mana pertama kali diterapkan dalam jasa keuangan, serta pertanyaan etika dan arsitektur yang perlu diajukan.</p>
<p class="post-lead-heading"><strong>Kesimpulan utama</strong></p>
<ul class="post-lead-takeaways">
  <li><strong>Cara kerja arsitektur transformer.</strong> Setiap model bahasa penting yang digunakan pada 2023 - GPT-4, Claude 2, Llama 2, Mistral, Falcon - dibangun di atas arsitektur transformer.</li>
  <li><strong>Lanskap model 2023.</strong> Tahun 2023 menghasilkan lebih banyak rilis model signifikan daripada tahun-tahun sebelumnya.</li>
  <li><strong>Area awal di jasa keuangan.</strong> Pada akhir 2023, lembaga keuangan bergerak dari eksperimen internal menuju program pilot terstruktur.</li>
  <li><strong>Risiko produksi.</strong> Perpindahan dari demo ke produksi mengungkap risiko yang membutuhkan mitigasi arsitektural.</li>
</ul>
</aside>
<!-- lead-end -->

> **Ringkasan eksekutif / kesimpulan utama**
>
> - **Arsitektur yang mengubah segalanya.** Paper transformer 2017 memperkenalkan self-attention: mekanisme yang menghitung bobot relevansi antara setiap pasangan token dalam input, mengganti pemrosesan sekuensial RNN dengan operasi matriks yang dapat diparalelkan. Setiap model bahasa besar pada 2023 adalah varian transformer ([Vaswani et al., 2017](https://arxiv.org/abs/1706.03762 "Attention Is All You Need")).
> - **GPT-4 sebagai tolok ukur 2023.** Dirilis Maret 2023, GPT-4 meraih persentil ke-90 pada US Bar exam, ke-99 pada GRE Verbal, dan menunjukkan penalaran multi-langkah pada dokumen panjang. Model ini menetapkan tolok ukur kapabilitas yang ingin dicapai atau dilampaui model berikutnya ([OpenAI, 2023](https://arxiv.org/abs/2303.08774 "GPT-4 Technical Report")).
> - **Model open-weight mendemokratisasi akses.** Llama 2 dari Meta (Juli 2023) dan Mistral 7B dari Mistral AI (September 2023) menunjukkan bahwa model dengan kapabilitas kompetitif setara kelas GPT-3.5 dapat berjalan di infrastruktur privat, menjawab kebutuhan data residency industri teregulasi.
> - **Pilot jasa keuangan pada 2023.** Deployment luas pada akhir 2023 mencakup review kontrak hukum, pemantauan perubahan regulasi, dan alat produktivitas developer. Goldman Sachs melaporkan penggunaan internal asisten coding AI oleh 10.000 developer.
> - **Halusinasi adalah penghambat produksi.** LLM menghasilkan output yang terdengar meyakinkan tetapi faktualnya salah pada tingkat yang tidak sepele. Dalam use case teregulasi - keputusan kredit, opini kepatuhan, pengungkapan kepada nasabah - halusinasi bukan cacat kosmetik; ini risiko regulasi dan tanggung jawab hukum yang membutuhkan mitigasi arsitektural seperti retrieval-augmented generation (RAG).

---

## Cara Kerja Arsitektur Transformer

Setiap model bahasa penting yang digunakan pada 2023 - GPT-4, Claude 2, Llama 2, Mistral, Falcon - dibangun di atas arsitektur transformer yang diperkenalkan dalam paper 2017 "Attention Is All You Need." Memahami mekanisme intinya menjelaskan mengapa model-model ini bekerja dan di mana mereka gagal.

**Token dan embedding.** Model memulai dengan memecah teks input menjadi token sub-kata, biasanya memakai byte-pair encoding. Setiap token dipetakan ke vektor berdimensi tinggi, atau embedding, yang mengodekan hubungan semantiknya dengan token lain, dipelajari selama pre-training.

**Self-attention.** Untuk setiap token, model menghitung tiga vektor: Query (apa yang dicari token ini), Key (apa yang ditawarkan token ini), dan Value (apa kontribusi token ini). Skor attention dihitung dengan dot product setiap Query terhadap semua Key, menerapkan softmax untuk menghasilkan bobot, lalu menjumlahkan Value yang dibobot oleh skor tersebut. Artinya setiap token memperhatikan setiap token lain dalam context window secara simultan - mekanisme yang memberi transformer kemampuan menangani dependensi jarak jauh.

**Multi-head attention.** Beberapa attention head berjalan paralel, masing-masing mempelajari jenis hubungan berbeda, seperti sintaksis, semantik, dan posisi. Output-nya digabungkan lalu diproyeksikan secara linear.

**Lapisan feed-forward.** Setelah attention, setiap posisi melewati dua transformasi linear dengan aktivasi non-linear. Lapisan ini melakukan komputasi per-token secara independen, menangkap transformasi fitur lokal.

**Skala.** GPT-4 diperkirakan memiliki lebih dari satu triliun parameter, meski tidak dikonfirmasi OpenAI. Llama 2 70B memakai 70 miliar parameter. Mistral 7B memakai 7 miliar parameter, dengan grouped-query attention dan sliding window attention untuk efisiensi. Model yang lebih besar umumnya menunjukkan penalaran zero-shot dan few-shot yang lebih baik - kapabilitas emergen yang membuatnya berguna untuk tugas yang tidak dilatih secara eksplisit.

## Lanskap Model 2023

Tahun 2023 menghasilkan lebih banyak rilis model signifikan daripada tahun-tahun sebelumnya:

**GPT-4 (OpenAI, Maret 2023).** Multimodal (input teks + gambar), context window hingga 128.000 token pada varian GPT-4 Turbo berikutnya, dan penalaran multi-langkah yang kuat. Menetapkan tolok ukur untuk tugas domain profesional.

**Claude 2 (Anthropic, Juli 2023).** Context window 100.000 token, terpanjang saat peluncuran, dengan performa kuat pada tugas dokumen panjang seperti review kontrak dan analisis regulasi. Constitutional AI training digunakan untuk mengurangi output berbahaya.

**Llama 2 (Meta, Juli 2023).** Rilis open-weight pada varian parameter 7B, 13B, 34B, dan 70B. Penggunaan komersial diizinkan. Memungkinkan deployment on-premise untuk industri teregulasi. Melahirkan ratusan varian fine-tuned seperti Code Llama, Vicuna, dan WizardLM.

**Mistral 7B (Mistral AI, September 2023).** Model 7 miliar parameter yang mengungguli Llama 2 13B di sebagian besar benchmark. Grouped-query attention dan sliding window attention mengurangi biaya inferensi. Ini adalah model frontier Eropa pertama yang signifikan, relevan dalam konteks GDPR dan EU AI Act.

**Falcon 180B (TII, September 2023).** Model open-weight 180 miliar parameter, dilatih pada 3,5 triliun token data RefinedWeb. Menunjukkan bahwa model open-weight dapat mendekati skala kelas GPT-4.

## Di Mana AI Generatif Pertama Kali Mendarat di Jasa Keuangan

Pada akhir 2023, lembaga keuangan telah bergerak dari eksperimen internal menuju program pilot terstruktur dalam beberapa use case yang berbeda:

**Produktivitas developer.** Alat pembuatan kode seperti GitHub Copilot, Amazon CodeWhisperer, dan model internal yang di-fine-tune menjadi kategori paling luas di-deploy. Goldman Sachs melaporkan bahwa 10.000 developer memiliki akses ke bantuan coding AI. Morgan Stanley menerapkan GPT-4 secara internal untuk membantu financial adviser mengambil informasi dari basis pengetahuan berisi 100.000 dokumen.

**Pemrosesan dokumen hukum dan regulasi.** Ekstraksi klausul kontrak, pemantauan perubahan regulasi, dan pemetaan kepatuhan menjadi pilot bernilai tertinggi. Riset JPMorgan tentang DocLLM menunjukkan bahwa model bahasa yang sadar tata letak dokumen mengungguli LLM generik pada tugas pemahaman dokumen finansial.

**Augmentasi layanan pelanggan.** Bank menerapkan asisten bertenaga LLM untuk pertanyaan pelanggan lini pertama, dengan eskalasi manusia untuk nasihat teregulasi. Batasannya jelas: model tidak boleh memberi nasihat teregulasi, tidak boleh mengarang ketentuan produk, dan harus dapat diaudit.

**Pembuatan narasi KYC dan AML.** Merangkum pola transaksi kompleks dan profil pelanggan untuk review analis - menggantikan pekerjaan penulisan manual - muncul sebagai use case kredibel dengan risiko halusinasi lebih rendah karena model merangkum data yang diberikan, bukan menghasilkan klaim baru.

## Risiko yang Diungkap Produksi

Perpindahan dari demo ke produksi dalam jasa keuangan memunculkan serangkaian risiko yang membutuhkan respons arsitektural:

**Halusinasi.** LLM menghasilkan output salah yang terdengar percaya diri pada tingkat yang berbeda-beda menurut jenis tugas dan model. Pada tugas factual recall, bahkan GPT-4 masih berhalusinasi pada tingkat yang tidak dapat diterima untuk opini kepatuhan atau pengungkapan kredit. Mitigasi utama adalah retrieval-augmented generation (RAG): mendasarkan output model pada dokumen yang diambil dan dapat diverifikasi, bukan hanya pengetahuan parametrik.

**Prompt injection.** Input adversarial yang disisipkan dalam dokumen atau pesan pengguna dapat mengarahkan ulang perilaku model. Dalam jasa keuangan, di mana LLM memproses dokumen tidak tepercaya seperti kontrak, email, dan kiriman pelanggan, prompt injection adalah risiko keamanan produksi, bukan teori.

**Kebocoran data.** Model yang di-fine-tune atau diprompt dengan data rahasia dapat mereproduksi data tersebut dalam output - risiko material bagi PII, posisi trading, dan informasi klien. Kontrol arsitektural seperti deployment privat, pengelolaan data-in-context, dan penyaringan output wajib diterapkan.

**Provenance model dan auditability.** Regulator mengharapkan lembaga keuangan mampu menjelaskan keputusan otomatis. LLM yang menghasilkan penilaian kredit tanpa jejak penalaran yang dapat diaudit gagal memenuhi persyaratan explainability GDPR Pasal 22, ketentuan high-risk AI dalam EU AI Act, dan panduan model risk FCA yang sudah ada.

**Pengetahuan usang.** LLM memiliki training cutoff. Model yang dilatih pada data hingga awal 2023 tidak mengetahui perubahan regulasi, keputusan suku bunga, atau peristiwa pasar setelah tanggal itu - batasan signifikan untuk use case kepatuhan real-time atau komentar pasar tanpa RAG atau retrieval real-time.

## Persyaratan Tata Kelola Sebelum Deployment

Praktisi jasa keuangan pada 2023 tidak menunggu kepastian regulasi sebelum deployment, tetapi institusi terdepan mengadopsi kerangka model risk management (MRM) yang diadaptasi dari SR 11-7 dan panduan SS3/18:

**Inventaris dan dokumentasi model.** LLM yang digunakan untuk fungsi bisnis memerlukan dokumentasi provenance data pelatihan, metodologi fine-tuning, mode kegagalan yang diketahui, dan performa pada validation set khusus domain.

**Checkpoint human-in-the-loop.** Untuk output teregulasi seperti keputusan kredit, opini kepatuhan, dan pengungkapan pelanggan, review manusia tetap wajib pada 2023. Otomasi diterapkan untuk drafting dan summarisation; sign-off akhir tetap oleh manusia.

**Risiko vendor.** Memakai API model pihak ketiga seperti OpenAI, Anthropic, atau Google menimbulkan risiko konsentrasi vendor, risiko data residency, dan risiko perubahan model karena penyedia dapat memperbarui model diam-diam. Enterprise agreement dan deployment privat sebagian memitigasi risiko ini.

**Keterlibatan regulator.** FCA, PRA, ECB, dan FINRA semuanya menerbitkan paper atau pidato tentang tata kelola AI pada 2023. Pesan konsistennya: kerangka model risk yang ada berlaku untuk AI, dan perusahaan harus proaktif mendokumentasikan pendekatan tata kelola mereka sebelum panduan formal diterbitkan.

## Pertanyaan yang Sering Diajukan

**Apa perbedaan antara large language model dan foundation model?**

Large language model (LLM) adalah model yang dilatih pada data teks skala besar untuk memprediksi dan menghasilkan bahasa. Foundation model adalah istilah yang lebih luas untuk model pra-latih besar yang dapat diadaptasi melalui fine-tuning atau prompting untuk banyak tugas turunan - mencakup LLM, tetapi juga model vision, model kode, dan model multimodal. GPT-4 adalah LLM sekaligus foundation model. DALL-E 3 adalah foundation model tetapi bukan LLM. Dalam praktik, istilah-istilah ini sering dipakai bergantian saat merujuk pada sistem pembangkit teks.

**Apa itu retrieval-augmented generation dan mengapa penting bagi jasa keuangan?**

RAG menggabungkan model bahasa dengan sistem retrieval: alih-alih hanya mengandalkan pengetahuan parametrik model, yaitu apa yang dipelajarinya saat training, RAG mengambil dokumen relevan pada waktu inferensi dan memberikannya sebagai konteks. Ini secara signifikan mengurangi halusinasi pada tugas faktual karena model mensintesis teks yang diberikan, bukan mengingat fakta yang dipelajari. Untuk jasa keuangan, RAG memungkinkan use case seperti pemantauan perubahan regulasi yang selalu mengambil aturan terbaru, dan review kontrak yang mendasarkan model pada teks kontrak aktual.

**Bagaimana lembaga keuangan sebaiknya menangani EU AI Act terkait deployment AI generatif pada 2023?**

EU AI Act masih dalam proses legislasi pada 2023, disahkan Parlemen Eropa pada Maret 2024 dan mulai berlaku Agustus 2024. Namun institusi dengan operasi atau pelanggan di UE sudah menilai pipeline mereka. Sistem AI high-risk dalam credit scoring, keputusan ketenagakerjaan, dan infrastruktur kritis memerlukan conformity assessment, mekanisme pengawasan manusia, dan audit logging. General-purpose AI (GPAI), termasuk foundation model seperti GPT-4, memiliki lapisan persyaratan tersendiri terkait transparansi dan risiko sistemik. Perusahaan yang memulai dokumentasi dan tata kelola pada 2023 berada dalam posisi lebih baik menghadapi tenggat implementasi.

**Apa perbedaan praktis antara fine-tuning dan prompt engineering untuk deployment LLM enterprise?**

Fine-tuning memodifikasi bobot model dengan melanjutkan training pada data khusus domain - mengajarkan model pengetahuan dan pola perilaku baru. Proses ini membutuhkan data pelatihan berlabel, anggaran komputasi, dan pemeliharaan berkelanjutan saat model dasar diperbarui. Prompt engineering, termasuk contoh few-shot dan system prompt, membentuk perilaku pada waktu inferensi tanpa mengubah bobot - lebih cepat diterapkan dan diperbarui, tetapi dibatasi oleh apa yang sudah diketahui model dasar. Untuk sebagian besar deployment jasa keuangan pada 2023, RAG plus prompt engineering menjadi titik awal yang disukai; fine-tuning dicadangkan untuk kasus ketika model perlu mempelajari terminologi proprietary atau mengikuti format output yang ketat.

## Referensi

- Vaswani, A., et al., (2017). [Attention Is All You Need ⧉](https://arxiv.org/abs/1706.03762 "Attention Is All You Need").
- OpenAI, (2023). [GPT-4 Technical Report ⧉](https://arxiv.org/abs/2303.08774 "GPT-4 Technical Report").
- Touvron, H., et al., Meta AI, (2023). [Llama 2: Open Foundation and Fine-Tuned Chat Models ⧉](https://arxiv.org/abs/2307.09288 "Llama 2").
- Jiang, A., et al., Mistral AI, (2023). [Mistral 7B ⧉](https://arxiv.org/abs/2310.06825 "Mistral 7B").
