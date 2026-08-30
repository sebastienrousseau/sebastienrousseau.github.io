---
title: "Perbendaharaan Agentik 2026: Daripada Indeks Perbendaharaan Autonomi kepada Ko-Pilot Bertaraf Pengeluaran"
tags: "agentic AI, treasury co-pilots, autonomous treasury, cash forecasting, liquidity, agentic banking, governance, SR 11-7, DORA, EU AI Act, CIB, ISO 20022, MCP"
subtitle: "Daripada Indeks Perbendaharaan Autonomi kepada ko-pilot bertaraf pengeluaran - cara perbendaharaan CIB mengoperasikan AI agentik pada data ISO 20022, panggilan alat MCP, dan tadbir urus bercorak SR 11-7 pada 2026."
description: "Ko-pilot perbendaharaan agentik beralih daripada perintis kepada pengeluaran pada 2026 - data ISO 20022 serta panggilan alat, dengan kawalan SR 11-7, DORA, dan EU AI Act di sekelilingnya."
date: "June 27, 2026"
language: "ms"
locale: "ms_MY"
banner: "https://cloudcdn.pro/stocks/images/sebastien-rousseau-20260617-ai-7.webp"
banner_alt: "Cahaya lantai dagangan menyinari atrium bank moden - melambangkan ko-pilot perbendaharaan agentik mengimbang semula kecairan intrahari dalam jalur dasar, di bawah kawalan SR 11-7 dan EU AI Act"
keywords: "AI agentik, ko-pilot perbendaharaan, perbendaharaan autonomi, ramalan tunai, pengurusan kecairan, perbankan agentik, tadbir urus, SR 11-7, DORA, EU AI Act, CIB, ISO 20022, pacs.008, RTGS, SWIFT, MCP, pengurusan risiko model, MRM"
---

## Perbendaharaan Agentik 2026: Daripada Indeks Perbendaharaan Autonomi kepada Ko-Pilot Bertaraf Pengeluaran

Ko-pilot perbendaharaan pada 2026 bukanlah chatbot yang dipasang pada skrin kedudukan tunai. Ia ialah ejen bersempadan yang membaca penyata [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html), menganggar kecairan intrahari, dan mencadangkan — atau, dalam sampul dasar yang ketat, melaksanakan — sapuan (sweep), lindung nilai FX, dan repo intrahari. Coraknya sama merentas perbendaharaan Perbankan Korporat dan Pelaburan (CIB): ejen sentiasa mengimbang semula kecairan dalam jalur dasar, mengeskalasikan kepada manusia hanya apabila sesuatu jalur bakal dilanggar atau had rakan niaga sudah hampir. Kajian pengamal meletakkan pengurangan beban kerja manual pada [30-50% merentas pemposisian tunai, ramalan, dan pengendalian pengecualian](https://assistents.ai/blogs/ai-agent-use-cases-in-banking-2026 "Kes penggunaan ejen AI dalam perbankan — penilaian 2026"), dan [tinjauan perbankan 2026 Capgemini](https://www.capgemini.com/insights/research-library/banking-top-trends-2026/ "Capgemini — Trend teratas dalam perbankan 2026") menyenaraikan AI agentik dalam perbendaharaan sebagai salah satu daripada segelintir kes penggunaan yang perbelanjaan 2026-nya menghasilkan pemampatan kos-untuk-berkhidmat yang boleh diukur.

Artikel ini ialah Bahagian II semula jadi bagi [Indeks Perbendaharaan Autonomi](https://sebastienrousseau.com/2026-06-07-autonomous-treasury-index-programmable-liquidity-tokenised-deposits-2026/). Indeks itu mentakrifkan destinasi — kecairan boleh aturcara, deposit ditokenkan, dasar boleh dibaca mesin. Ko-pilot ialah unit pengeluaran yang membawa perbendaharaan CIB ke sana tanpa melanggar SR 11-7, DORA, atau EU AI Act.

## 01. Daripada eksperimen kepada pengeluaran

2024–2025 ialah era perintis perbendaharaan. 2026 ialah era pengeluaran perbendaharaan.

[Ramalan 2026 Forrester: Perbankan dan Pelaburan](https://www.forrester.com/report/predictions-2026-banking-and-investing/RES185001 "Forrester — Ramalan 2026: Perbankan dan Pelaburan") menyatakannya secara terus: pada 2026, majoriti bank Peringkat 1 akan memindahkan sekurang-kurangnya satu kes penggunaan agentik daripada kotak pasir kepada persekitaran pengeluaran yang hidup dan terukur, dan perbendaharaan ialah salah satu daripada tiga yang pertama menyeberangi ambang itu. [Laporan trend teratas perbankan 2026 Capgemini](https://www.capgemini.com/insights/research-library/banking-top-trends-2026/ "Capgemini — Trend teratas perbankan 2026") membuat kesimpulan yang sama dari sudut berbeza — pelaburan AI agentik beralih daripada eksperimen produktiviti mendatar kepada penggunaan menegak khusus fungsi, dengan perbendaharaan korporat, operasi pembayaran, dan pemulihan KYC mengambil sebahagian besar bajet baharu 2026.

Apa yang berubah? Tiga perkara.

Pertama, lapisan data. Migrasi ISO 20022 telah selesai bagi kebanyakan mata wang utama pada November 2025, jadi data tunai dan pembayaran tiba dalam bentuk berstruktur yang boleh ditaakul oleh ejen tanpa lapisan pengikisan skrin yang rapuh.

Kedua, satah kawalan. MCP menyeragamkan cara ejen memanggil alat, dan kini bank mempunyai jawapan yang boleh dipertahankan kepada soalan CRO: "apakah yang sebenarnya boleh dilakukan oleh ejen ini?" Jawapannya ialah daftar alat MCP yang terikat padanya, tidak lebih daripada itu.

Ketiga, pengawal selia tidak lagi bersifat hipotesis. Garis panduan penyeliaan SR 11-7 telah diperluas untuk merangkumi model bukan berketentuan; DORA mula berkuat kuasa pada Januari 2025; rejim pengelasan berisiko tinggi EU AI Act mula menggigit pada Ogos 2026.

## 02. Seni bina: data + ISO + panggilan alat

Ko-pilot perbendaharaan pengeluaran pada 2026 mempunyai tiga lapisan, mengikut susunan ini.

**Data.** Ejen membaca mesej ISO 20022 — `camt.052` (penyata intrahari), `camt.053` (hujung hari), `camt.054` (pemberitahuan debit/kredit) — dan pindahan kredit pelanggan pacs.008 semasa ia mengalir melalui rel pembayaran bank. Ejen membaca mesej berstruktur itu dan menyelaraskannya dengan lejar am. [Buku panduan AI perbendaharaan 2026 Elire](https://web.archive.org/web/20260124183820/https://elire.com/treasurys-ai-playbook-ete-2025/ "Elire — Buku panduan AI perbendaharaan 2025-2026") merangka perkara ini sebagai prasyarat: jika ejen tidak dapat membaca data ISO 20022 berstruktur, setiap dakwaan hiliran tentang ketepatan ramalan hanyalah pemasaran.

**Penaakulan.** Model asas terkawal — biasanya model perintis dalaman dengan penyesuai dasar perbendaharaan yang diperhalusi — menukar realiti ISO 20022 kepada tindakan yang dicadangkan. Langkah penaakulan tidak pernah menyentuh rel pembayaran. Ia menghasilkan permintaan panggilan alat berstruktur: "sapu £180 juta daripada nostro EUR pada rakan niaga peringkat BoE X ke akaun RTGS GBP Y pada 14:30 untuk mengekalkan penampan intrahari GBP melebihi lantai dasar."

**Panggilan alat.** Ejen memanggil alat yang didaftarkan pada MCP. Setiap alat ialah fungsi bertaip dan diaudit: `propose_sweep`, `simulate_fx_hedge`, `query_limit`, `submit_pacs008_for_human_approval`. Alat MCP ialah satu-satunya laluan kepada kesan dunia sebenar. Penyerahan SWIFT melebihi ambang yang dikonfigurasikan dihalakan kepada pegawai perbendaharaan manusia untuk kelulusan; di bawah ambang, ejen boleh menyerahkannya dalam jalur dasar siang hari dan tindakan itu mendarat dalam log audit WORM dalam saat yang sama.

Disiplinnya ialah model tidak pernah mempunyai akses tulis pangkalan data, tidak pernah mempunyai kelayakan SWIFT langsung, dan tidak pernah membaca skrin tidak berstruktur. Daftar MCP ialah sempadan keselamatan, dan dasar OPA menguatkuasakan apa yang boleh dipanggil oleh setiap identiti ejen.

## 03. Kes penggunaan dan metrik

Tiga kes penggunaan ko-pilot perbendaharaan berada dalam pengeluaran pada skala CIB pada 2026.

**Pemposisian tunai.** Ejen mengekalkan kedudukan tunai intrahari secara langsung merentas akaun nostro, menjangka mesej pacs.008 dalam perjalanan, dan mencadangkan sapuan untuk mengekalkan penampan dalam jalur dasar. Kesan yang dilaporkan: pengurangan 35-45% dalam masa penyelarasan manual, penurunan terukur dalam lebihan pendanaan penampan hujung hari (yang menambah baik Margin Faedah Bersih pada tunai terbiar), dan peristiwa overdraf RTGS intrahari yang menghala ke arah sifar dalam perintis yang telah menyelesaikan satu suku penuh.

**Ramalan tunai.** Ejen menyerap aliran ISO 20022 sejarah, isyarat tingkah laku pelanggan, dan peristiwa kalendar yang diketahui (tarikh cukai, tarikh dividen, kupon bon) dan menghasilkan ramalan tunai 1 hari, 5 hari, dan 30 hari dengan selang keyakinan. Ralat peratusan mutlak min bagi ramalan 5 hari telah menurun daripada ~7-9% (garis dasar regresi) kepada ~3-4% dalam perbendaharaan CIB yang lebih baik peralatannya, yang menambah baik pelan pendanaan CFO secara ketara.

**Pengendalian pengecualian.** Ejen menyaring pengecualian pembayaran — mesej pacs.008 yang gagal, padanan rakan niaga tersekat sekatan, kiriman wang tidak sepadan — dan mencadangkan pelupusannya (baiki, pulangkan, eskalasi). Masa penyaringan telah menurun daripada ~7 minit (manusia sahaja) kepada ~90 saat (manusia-dalam-gelung), dan peranan manusia beralih daripada pengumpulan data kepada keputusan.

Metrik yang jujur bukanlah "tugas yang diautomasikan"; sebaliknya "perhatian pegawai perbendaharaan yang dialihkan daripada pemasangan data kepada pertimbangan." Itulah angka yang boleh dipertahankan oleh CFO kepada lembaga dan boleh dipertahankan oleh CRO kepada pengawal selia.

## 04. Tadbir urus, audit, dan kesesuaian SR 11-7

Perbendaharaan agentik ialah masalah risiko model sebelum ia menjadi kisah produktiviti.

**SR 11-7 dan MRM.** Di bawah [garis panduan pengurusan risiko model SR 11-7](https://web.archive.org/web/20260414150921/https://www.federalreserve.gov/supervisionreg/srletters/sr1107.htm "Federal Reserve — Pengurusan risiko model SR 11-7") Rizab Persekutuan, mana-mana model yang menjejaskan keputusan kewangan secara ketara memerlukan pembangunan berdokumen, pengesahan bebas, dan pemantauan prestasi berterusan. Ko-pilot perbendaharaan ialah satu model di bawah SR 11-7. MRM memiliki kemasukan inventori, pengesahan memiliki ujian pencabar (adakah ramalan ejen mengatasi garis dasar regresi pada tetingkap terpisah?), dan pengeluaran memiliki pemantauan hanyutan. Bank yang menganggap ko-pilot sebagai "sekadar perkakasan" telah salah mengelaskan risiko itu.

**DORA.** Artikel 5 [Peraturan (EU) 2022/2554 (DORA)](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32022R2554 "DORA — Akta Ketahanan Operasi Digital") menjadikan lembaga akhirnya bertanggungjawab atas risiko ICT. Ko-pilot perbendaharaan ialah sistem ICT yang menyokong fungsi kritikal — lembaga mesti meluluskan rangka kerja risiko, penumpuan pembekal pihak ketiga, dan pelan keluar. Suis mati (menarik balik akses alat MCP dan berundur kepada operasi manusia sahaja dalam beberapa minit) ialah kawalan DORA, bukan sekadar tambahan yang elok ada.

**EU AI Act.** Ko-pilot perbendaharaan yang mempengaruhi keputusan kewangan yang ketara tergolong di bawah pengelasan berisiko tinggi, yang mewajibkan bank untuk mengekalkan sistem pengurusan risiko, mencatatkan semua operasi ke telemetri patuh OTLP, menjalankan pengawasan manusia, dan menghasilkan dokumentasi pematuhan atas permintaan. Pelaksanaan yang realistik ialah jejak OTLP penuh pada setiap langkah penaakulan ejen serta log audit panggilan alat yang disimpan secara WORM, dan penyemak manusia bagi mana-mana tindakan yang melintasi jalur dasar.

**Dialog penyeliaan.** Bank of England (BoE) dan Financial Conduct Authority (FCA) telah menyatakan dengan jelas sepanjang 2025-2026 bahawa mereka menjangka untuk melihat inventori, bukti pengesahan, dan suis mati, mengikut susunan itu. Perbualan berjalan lancar apabila CRO dapat menunjukkan ketiga-tiganya dalam satu bilik.

Satah kawalan itulah bentengnya. Bank yang dapat menunjukkan kepada penyelianya daftar MCP, fail dasar OPA, log audit WORM, aliran jejak OTLP, dan pek pengesahan SR 11-7 — dalam satu sesi — sudah bersedia untuk menjalankan ko-pilot perbendaharaan dalam pengeluaran. Bank yang tidak mampu sedang menjalankan perintis yang tidak dibenarkan.

## Kesimpulan

Indeks Perbendaharaan Autonomi mentakrifkan destinasi: kecairan boleh aturcara, deposit ditokenkan, dasar boleh dibaca mesin. Tulisan ini ialah Bahagian II — unit pengeluaran yang membawa perbendaharaan CIB ke sana. Coraknya stabil: data ISO 20022, panggilan alat bersempadan MCP, tadbir urus SR 11-7, akauntabiliti DORA, audit EU AI Act. Ko-pilot perbendaharaan 2026 yang bertahan dalam semakan penyelia pertama mereka mempunyai bentuk yang sama; yang tidak bertahan kekurangan tiga perkara yang sama — pek pengesahan MRM, suis mati, dan log audit WORM.

Kerja yang menarik pada 2026 bukanlah modelnya. Ia ialah satah kawalan di sekeliling model, dan perbualan CFO yang menukar pengurangan beban kerja manual 30-50% kepada angka kos-untuk-berkhidmat yang boleh dipertahankan.

Untuk konteks huluan, lihat [Indeks Perbendaharaan Autonomi](https://sebastienrousseau.com/2026-06-07-autonomous-treasury-index-programmable-liquidity-tokenised-deposits-2026/ "Indeks Perbendaharaan Autonomi 2026") dan, untuk rangka tadbir urus, [Indeks AI Agentik untuk Bank](https://sebastienrousseau.com/2026-06-03-agentic-ai-index-banks-autonomy-governance-auditability-2026/ "Indeks AI Agentik untuk Bank 2026").
