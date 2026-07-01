---
title: "Mengamankan Buku Besar: Panduan Dewan untuk Migrasi Post-Quantum di Corporate Finance"
subtitle: "Risiko kuantum telah bergeser dari rasa ingin tahu riset menjadi mandat regulasi aktif. Dengan roadmap G7 Januari 2026 dan BIS Project Leap membuktikan kelayakan pada sistem pembayaran live, pertanyaan bagi dewan bukan lagi apakah harus bermigrasi, melainkan apakah migrasi dapat selesai sebelum umur simpan kriptografis data hari ini habis."
description: "Risiko kuantum kini menjadi mandat regulasi aktif. Roadmap G7, timeline EU, UK, dan ASD, serta BIS Project Leap membuat migrasi post-quantum menjadi prioritas dewan."
date: "May 14, 2026"
language: "id-ID"
locale: "id_ID"
banner: "https://cloudcdn.pro/stocks/images/getty-images-LaU3HadwEeE-unsplash.webp"
banner_alt: "Diagram roadmap migrasi post-quantum cryptography, infrastruktur corporate banking berpindah dari RSA ke ML-KEM dan ML-DSA"
keywords: "post-quantum cryptography, migrasi PQC, corporate banking, financial services, G7 CEG roadmap, BIS Project Leap, ML-KEM, ML-DSA, FIPS 203, FIPS 204"
---

![Diagram roadmap migrasi post-quantum cryptography, infrastruktur corporate banking berpindah dari RSA ke ML-KEM dan ML-DSA](https://cloudcdn.pro/stocks/images/getty-images-LaU3HadwEeE-unsplash.webp).class=\"img-fluid clearfix\"

Risiko kuantum telah bergeser dari rasa ingin tahu riset menjadi mandat regulasi aktif. Dengan roadmap G7 yang diterbitkan pada Januari 2026, timeline EU, UK, dan Australia yang semakin jelas, serta BIS Project Leap yang membuktikan kelayakan di sistem pembayaran live, pertanyaan bagi dewan bukan lagi apakah harus bermigrasi, melainkan apakah migrasi dapat selesai sebelum umur simpan kriptografis data hari ini habis.

---

> **Kesimpulan utama**
>
> - **2026 adalah tahun ketika postur regulasi mengeras.** Roadmap Januari dari G7 Cyber Expert Group, timeline terkoordinasi EU NIS Cooperation Group, dan rencana tiga fase UK NCSC memindahkan percakapan dari awareness ke eksekusi. Australian Signals Directorate bahkan lebih jauh, menetapkan tanggal akhir 2030 untuk kriptografi asimetris klasik.
> - **Eksposurnya asimetris.** RSA, ECC, dan Diffie-Hellman adalah masalah langsung, yaitu algoritma asimetris yang menopang SWIFT handshakes, TLS, PKI, code signing, dan autentikasi clearing network. Enkripsi simetris seperti AES-256 tetap stabil jika panjang kunci dijaga. Fokus dewan harus berada pada permukaan asimetris.
> - **Harvest-now-decrypt-later bukan skenario masa depan.** Adversary sudah mencegat dan menyimpan log keuangan terenkripsi, settlement records, materi M&A, dan data wire lintas batas hari ini, dengan niat eksplisit mendekripsinya ketika cryptographically relevant quantum computer (CRQC) tersedia. Untuk data dengan kebutuhan kerahasiaan 10-20 tahun, risiko itu sudah terealisasi.
> - **Industri kini memiliki titik referensi yang bekerja.** [BIS Project Leap Phase 2 ⧉](https://www.bis.org/publ/othp107.htm "Project Leap phase 2: quantum-proofing payment systems"), diterbitkan Desember 2025, berhasil mengganti tanda tangan digital tradisional dengan post-quantum cryptography dalam transfer likuiditas live di TARGET2, sekaligus memunculkan biaya rekayasa spesifik, yaitu verification latency dan packet size, yang akan dihadapi setiap program migrasi.
> - **Suite NIST adalah jangkar global.** [FIPS 203 (ML-KEM) ⧉](https://csrc.nist.gov/pubs/fips/203/final "FIPS 203, Module-Lattice-Based Key-Encapsulation Mechanism Standard") dan FIPS 204 (ML-DSA) dirujuk oleh setiap yurisdiksi besar, bahkan ketika posisi nasional berbeda pada parameter set dan persyaratan hybrid. Dewan sebaiknya memperlakukan ML-KEM-768/ML-DSA-65 sebagai lantai dan ML-KEM-1024/ML-DSA-87 sebagai baseline konservatif untuk data berumur panjang.
> - **Hybrid adalah satu-satunya jalur kredibel.** Pure cut-over tidak disarankan otoritas besar mana pun. Menjalankan algoritma klasik dan quantum-resistant secara paralel adalah pola deployment yang didukung NCSC, ANSSI, BSI, dan dibuktikan dalam Project Leap. Pola ini lebih berat daripada alternatif mana pun, tetapi satu-satunya yang menangani kompatibilitas hari ini dan ancaman besok.

---

## Tahun Ketika Postur Regulasi Mengeras

Selama sebagian besar dekade terakhir, post-quantum cryptography berada di sudut nyaman roadmap jangka panjang. Komputer kuantum mengesankan tetapi jauh; matematika kriptografis di balik RSA dan elliptic curves diperlakukan sebagai substrat stabil; dan percakapan migrasi sebagian besar terbatas pada kelompok kerja spesialis. Posisi itu tidak lagi dapat dipertahankan.

Pada Januari 2026, [G7 Cyber Expert Group menerbitkan pernyataan paling konsekuensialnya sejauh ini ⧉](https://www.gov.uk/government/publications/advancing-a-coordinated-roadmap-for-the-transition-to-post-quantum-cryptography-in-the-financial-sector/g7-cyber-expert-group-statement-on-advancing-a-coordinated-roadmap-for-the-transition-to-post-quantum-cryptography-in-the-financial-sector-january-20 "G7 CEG Statement on Advancing a Coordinated Roadmap for the Transition to Post-Quantum Cryptography in the Financial Sector"), dipimpin bersama oleh US Treasury dan Bank of England. Dokumen itu bukan regulasi, tetapi bobotnya lebih besar daripada guidance biasa: ia mewakili pandangan bersama kementerian keuangan, bank sentral, dan otoritas pengawas di yurisdiksi G7 bahwa transisi kriptografis kini isu systemic risk management. Roadmap menyelaraskan horizon perencanaannya di sekitar pertengahan 2030-an, dengan sistem keuangan kritis didorong bermigrasi lebih awal, bahasa yang dalam idiom hati-hati bank sentral menandakan ekspektasi, bukan sekadar saran.

Dua bulan sebelumnya, BIS Innovation Hub dan Eurosystem menerbitkan hasil [Project Leap Phase 2 ⧉](https://www.bis.org/publ/othp107.htm "Project Leap phase 2: quantum-proofing payment systems"), eksperimen teknis yang mengganti tanda tangan digital tradisional dengan post-quantum cryptography dalam transfer likuiditas live antara Bank of Italy, Banque de France, Deutsche Bundesbank, Nexi-Colt, dan Swift. Headline-nya sukses: transfer bertanda tangan quantum-resistant melewati sistem pembayaran operasional end-to-end. Detail di bawah headline lebih instruktif, dan itulah yang menentukan biaya operasional migrasi.

Kombinasi dua peristiwa ini, kerangka kebijakan G7 yang terkoordinasi dan proof point yang bekerja di sistem pembayaran nyata, memberikan jawaban yang ditunggu komunitas teknis selama satu dekade atas pertanyaan "apakah ini nyata?" Pada Mei 2026, jawabannya ya. Pertanyaan yang tersisa adalah kecepatan.

## Tiga Vektor Ancaman yang Perlu Diperhatikan Dewan

Sebelum membahas mekanik migrasi, penting untuk tepat tentang apa yang berisiko. Risiko kuantum dalam corporate banking tidak seragam di seluruh estate kriptografis, dan perhatian dewan paling baik diarahkan pada tiga vektor dengan eksposur paling akut.

### 1. Harvest Now, Decrypt Later (HNDL)

Kekhawatiran paling langsung bukan masa depan. Ia masa kini. Adversary tingkat negara dan kriminal canggih secara sistematis mencegat dan menyimpan traffic keuangan terenkripsi, wire transfers, SWIFT message flows, komunikasi M&A, cross-border settlement logs, swap agreements, dan KYC files, tanpa kemampuan saat ini untuk membacanya. Tujuannya sederhana: simpan sekarang, dekripsi nanti, setelah CRQC ada. Seperti [Bank for International Settlements catat secara eksplisit ⧉](https://www.bis.org/about/bisih/topics/cyber_security/leap.htm "Project Leap: quantum-proofing the financial system"), pengumpulan ini sudah terjadi.

Bagi dewan, implikasinya tidak nyaman tetapi spesifik: setiap data sensitif yang dikirim dengan enkripsi asimetris klasik hari ini, dan yang kebutuhan kerahasiaannya melampaui hadirnya CRQC, harus sudah dianggap terekspos. Tidak ada breach notification ketika HNDL terjadi. Tidak ada alarm di SIEM. Enkripsi masih bertahan, untuk saat ini, tetapi data sudah keluar dari perimeter.

### 2. Risiko Sensitivitas Jangka Panjang

Data corporate banking memiliki umur simpan institusional yang tidak biasa panjang. Dokumentasi M&A strategis dapat tetap sensitif pasar selama satu dekade. Komunikasi trade secret dan valuasi intellectual property dapat tetap rahasia selama lima belas sampai dua puluh tahun. Cross-border settlement logs, central counterparty exposures, dan counterparty credit assessments mempertahankan sensitivitas komersial jauh melampaui umur transaksional langsungnya.

[Mosca equation ⧉](https://www.cryptomathic.com/a-bankers-guide-to-quantum-safe-cryptography-part-3-roadmap-to-pqc-migration-for-financial-institutions-cryptomathic "A Banker's Guide to Quantum Safe Cryptography — Part 3"), awalnya dirumuskan Michele Mosca dan kini tertanam di setiap framework migrasi serius, memformalkan masalah ini. Jika **S** adalah shelf life data, **M** adalah waktu yang dibutuhkan untuk memigrasikan sistem pelindungnya, dan **Q** adalah waktu sampai CRQC tersedia, maka:

```
If S + M > Q, the data is already exposed.
```

Untuk data dengan horizon kerahasiaan dua puluh tahun dan program migrasi yang realistis membutuhkan lima sampai tujuh tahun, nilai Q implisit yang dipertaruhkan dewan setidaknya 25 tahun. Kumpulan penilaian pakar yang semakin besar, termasuk [prediksi APAC 2026 Forrester ⧉](https://www.forrester.com/press-newsroom/forrester-apac-2026-predictions/ "Forrester's 2026 APAC Predictions"), survei tahunan Global Risk Institute, dan makalah arsitektur Februari 2026 yang mengusulkan CRQC sekitar 100.000 physical qubits memakai QLDPC codes, menunjukkan taruhan itu tidak aman.

### 3. Kerentanan Core Handshakes

Vektor ketiga adalah yang paling signifikan secara arsitektural. Cipher simetris seperti AES-256 tetap relatif stabil; Grover's algorithm memang membagi dua effective security level, tetapi menggandakan panjang kunci memulihkan margin. Eksposur katastrofik berada pada algoritma asimetris, dan algoritma inilah yang menopang setiap authenticated handshake dalam corporate finance: RSA dalam SWIFT public-key infrastructure, ECDSA dalam autentikasi TLS client/server, ECDH dalam pembentukan session key, dan varian ECC di seluruh mobile client authentication, API signatures, dan code-signing pipelines.

CRQC fungsional yang menjalankan Shor's algorithm tidak melemahkan sistem ini secara bertahap. Ia memecahkannya. Setelah CRQC beroperasi, setiap handshake yang dilindungi RSA, setiap tanda tangan ECDSA, dan setiap pertukaran kunci elliptic-curve menjadi dapat dipulihkan, bukan dalam bulan-bulan kerja, melainkan dalam hitungan jam. Transisi dari "aman" ke "compromised" bersifat biner, dan menyebar serentak ke setiap sistem yang memakai algoritma terdampak. Inilah fondasi urgensi regulasi.

## Pengetatan Regulasi: Tampilan per Yurisdiksi

Gambaran regulasi global pada Mei 2026 bukan lagi tambal sulam saran. Ia adalah kumpulan timeline terkoordinasi yang berbeda ketatnya tetapi menuju tujuan yang sama. Bank multinasional yang beroperasi di pusat keuangan besar kini tunduk pada yurisdiksi yang paling ketat berlaku, bukan yang paling lunak.

### Amerika Serikat

AS memiliki posisi paling preskriptif untuk institusi yang menyentuh sistem federal. [Commercial National Security Algorithm Suite 2.0 ⧉](https://informedclearly.com/en/technology/46563/quantum-encryption-race-post-quantum-security-standards-2026 "Quantum-Encryption Race 2026") dari NSA mewajibkan ML-KEM-1024 dan ML-DSA-87 untuk national security systems, dengan sistem baru harus menerapkan PQC mulai Januari 2027 dan migrasi infrastruktur selesai pada 2035. OMB Memorandum M-23-02 mengikat lembaga federal ke lintasan yang sama. Bagi bank komersial, eksposur langsung datang melalui rantai pengadaan federal, kontrak yang berdekatan dengan NSS, dan tekanan tidak langsung yang diberikan guidance NSA pada pasar yang lebih luas.

### Uni Eropa

EU beroperasi pada tiga layer. [Coordinated Implementation Roadmap Komisi Eropa ⧉](https://pqshield.com/pqc-transition-roadmaps-and-guidance/ "PQC Roadmaps and Transition Guidance"), dielaborasi NIS Cooperation Group pada Juni 2025, menetapkan milestone bertahap pada 2026 untuk strategi nasional, 2030 untuk migrasi sistem berisiko tinggi, dan 2035 untuk transisi penuh. Cyber Resilience Act akan mewajibkan upgrade keamanan state-of-the-art untuk produk digital mulai akhir 2027. NIS2 memperkuat ICT risk management, walaupun tidak ada direktif yang memuat persyaratan PQC eksplisit. Namun regulator nasional bergerak lebih cepat daripada Komisi. BSI Jerman mewajibkan hybrid key exchange dan menyetujui keranjang konservatif ML-KEM, FrodoKEM, dan Classic McEliece. ANSSI Prancis mewajibkan hybrid untuk key encapsulation dan signatures. NLNCSA Belanda dan otoritas Norwegia menyelaraskan diri pada ML-KEM-1024 sebagai baseline konservatif untuk data berumur panjang.

### Britania Raya

UK NCSC menerbitkan guidance definitif pada Maret 2025 dan menegaskannya kembali melalui Annual Review 2025. Timeline tiga fasenya eksplisit:

- **Hingga 2028** — Identifikasi layanan kriptografis yang membutuhkan upgrade, bangun rencana migrasi, dan hasilkan inventaris kriptografis lengkap.
- **2028 hingga 2031** — Jalankan upgrade prioritas tinggi, terutama pada sistem kritis dan protokol internet yang menghadap eksternal.
- **2031 hingga 2035** — Selesaikan migrasi di semua sistem, layanan, dan produk.

Bagi institusi keuangan UK, [CMORG PQC Guidance ⧉](https://www.cmorg.org.uk/sites/default/files/2025-06/CMORG%20-%20Guidance%20for%20Post-Quantum%20Cryptography%20-%20April%202025%20-%20TLP%20CLEAR%20(1).pdf "CMORG Guidance for Post-Quantum Cryptography") berada berdampingan dengan framework NCSC, memperlakukan bank sebagai critical national infrastructure dan menekankan kesiapan vendor serta penyelarasan supply chain.

### Asia-Pasifik

Postur APAC lebih terfragmentasi tetapi bergerak cepat. ASD Australia memiliki posisi paling keras secara global: kriptografi public-key klasik tidak boleh digunakan melewati akhir 2030, tanpa rekomendasi hybrid, dan ML-KEM-1024 diwajibkan (ML-KEM-768 hanya dapat diterima hingga 2030). Organisasi harus memiliki rencana transisi yang disempurnakan pada akhir 2026. Monetary Authority of Singapore telah menerbitkan guidance quantum-safe readiness formal. Jepang dan Korea Selatan berinvestasi besar, walaupun keduanya memiliki jalur algoritma nasional. National Quantum Mission India, didukung alokasi pemerintah Rs. 6.003,65 crore, secara eksplisit mengidentifikasi sistem perbankan dan keuangan sebagai prioritas strategis. [Prediksi APAC 2026 Forrester ⧉](https://www.forrester.com/press-newsroom/forrester-apac-2026-predictions/ "Forrester's 2026 APAC predictions") menempatkan jumlah enterprise regional yang diperkirakan berinvestasi dalam teknologi post-quantum tahun ini lebih dari 90%.

### Posisi Bersih

Bagi dewan, sintesis praktis dari posisi yurisdiksi ini jelas. Bank multinasional tidak dapat mengelola pada timeline satu regulator saja; ia harus mengelola pada yang paling ketat berlaku. Untuk sebagian besar institusi besar, itu berarti horizon perencanaan akhir 2030 untuk sistem berisiko tinggi dan akhir 2035 untuk long tail, dengan entitas terekspos ASD menargetkan pure-PQC pada 2030 dan entitas terekspos CNSA menargetkan jendela yang sama dengan ML-KEM-1024 dan ML-DSA-87 secara spesifik.

## BIS Project Leap: Apa yang Sebenarnya Dibuktikan Industri

Project Leap layak mendapat perhatian dewan bukan karena tonggak pemasaran, tetapi karena ia adalah demonstrasi end-to-end paling kredibel post-quantum cryptography dalam sistem pembayaran keuangan live sampai saat ini. Kesimpulan headline-nya sederhana: berhasil. Detail di bawahnya adalah tempat implikasi operasional berada.

Phase 1, selesai pada 2023, membangun VPN quantum-resistant antara sistem TI Bank of France dan Deutsche Bundesbank, dengan pesan pembayaran dikirim antara Paris dan Frankfurt di bawah skema enkripsi hybrid. Phase 2, selesai pada akhir 2025 dan [dilaporkan pada Desember ⧉](https://www.bis.org/publ/othp107.htm "Project Leap phase 2: quantum-proofing payment systems"), bergerak jauh lebih jauh. Konsorsium mengganti tanda tangan digital berbasis RSA tradisional dengan post-quantum signatures dalam eksekusi transfer likuiditas di TARGET2, sistem Real-Time Gross Settlement Eurosystem. Pesertanya, BIS Innovation Hub Eurosystem Centre, Bank of Italy, Banque de France, Deutsche Bundesbank, Nexi-Colt, dan Swift, adalah institusi yang infrastrukturnya memang pada akhirnya harus bermigrasi.

Laporan itu menandai tiga temuan yang harus diinternalisasi setiap program migrasi:

- **Verification latency jauh lebih tinggi.** Verifikasi post-quantum signature membutuhkan waktu material lebih lama daripada verifikasi berbasis RSA pada hardware yang sama. Untuk sistem RTGS yang dirancang di sekitar penanganan pesan sub-detik, ini bukan observasi marginal; ini input capacity planning.
- **Ukuran paket membutuhkan redevelop sistem.** PQC signatures satu orde magnitudo lebih besar daripada padanan ECDSA. Sistem pembayaran yang internal queues, monitoring tools, dan database schemas-nya disetel untuk ukuran pesan legacy tidak dapat menampung payload baru tanpa redesign. Project Leap secara eksplisit menemukan TARGET2 tidak dapat "easily accommodate" model hybrid tanpa redevelop substansial.
- **Hybrid adalah jawaban yang tepat, tetapi lebih berat.** Menjalankan algoritma klasik dan post-quantum secara paralel menjaga backward compatibility dan memberi defence in depth, tetapi menggandakan overhead pemrosesan kriptografis. Ini biaya operasional melakukan PQC dengan benar selama transisi; tidak dapat dihindari hanya dengan engineering pintar.

Bagi CFO yang meninjau business case PQC, temuan Project Leap berguna justru karena presisi. Biaya migrasi post-quantum bukan satu baris capital. Ia adalah verification latency yang merambat ke SLA contracts, ekspansi message-size yang menyentuh storage dan bandwidth budgets, serta periode transisi operasi kriptografis ganda yang memengaruhi compute capacity planning. Tidak satu pun spekulatif. Semuanya sudah diukur di sistem bank sentral live.

## Toolkit NIST: Perbandingan ML-KEM dan ML-DSA

Pusat teknis setiap framework nasional yang kredibel adalah suite standar post-quantum NIST yang diterbitkan pada Agustus 2024. Dua standar adalah fokus langsung corporate banking: ML-KEM (FIPS 203) untuk key encapsulation dan ML-DSA (FIPS 204) untuk digital signatures. Keduanya berbagi fondasi matematis, bergantung pada hardness Module Learning With Errors (ML-LWE) dan Module Short Integer Solution problems di structured lattices, tetapi perannya berbeda dalam estate kriptografis, dan profil performa serta ukurannya berbeda material.

### ML-KEM (FIPS 203) — Key Encapsulation

ML-KEM, diturunkan dari [CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html), adalah pengganti ECDH dan RSA-KEM dalam protokol ketika dua pihak perlu membangun shared symmetric key di channel tidak aman. Secara praktis, inilah arah TLS handshakes setelah RSA dan ECDH dipensiunkan. NIST menetapkan tiga parameter set dengan security strength meningkat dan performa menurun: ML-KEM-512 (NIST Category 1), ML-KEM-768 (Category 3), dan ML-KEM-1024 (Category 5).

### ML-DSA (FIPS 204) — Digital Signatures

ML-DSA, diturunkan dari CRYSTALS-Dilithium, adalah pengganti tanda tangan RSA dan ECDSA. Ia menangani certificate signing, code signing, document signing, dan authentication. Tiga parameter set-nya adalah ML-DSA-44, ML-DSA-65, dan ML-DSA-87, kira-kira sesuai NIST Categories 2, 3, dan 5.

### Profil Ukuran dan Performa

Bagi CIO yang menskop kapasitas migrasi, angka paling penting adalah ukuran artefak. Inilah input untuk network capacity planning, storage projections, dan pengujian tingkat protokol.

| Algorithm | Public Key | Ciphertext / Signature | Closest Classical Equivalent | Size vs Classical |
|---|---|---|---|---|
| ML-KEM-512 | 800 bytes | 768 bytes (ciphertext) | ECDH P-256 (~32 bytes pub key) | ~25× larger |
| ML-KEM-768 | 1,184 bytes | 1,088 bytes (ciphertext) | ECDH P-384 | ~25× larger |
| ML-KEM-1024 | 1,568 bytes | 1,568 bytes (ciphertext) | ECDH P-521 | ~25× larger |
| ML-DSA-44 | 1,312 bytes | ~2,420 bytes (signature) | ECDSA P-256 (64-byte sig) | ~38× larger |
| ML-DSA-65 | 1,952 bytes | ~3,293 bytes (signature) | ECDSA P-384 | ~50× larger |
| ML-DSA-87 | 2,592 bytes | ~4,595 bytes (signature) | ECDSA P-521 | ~70× larger |

*Sumber: Sintesis [NIST FIPS 203 ⧉](https://csrc.nist.gov/pubs/fips/203/final "FIPS 203, Module-Lattice-Based Key-Encapsulation Mechanism Standard") dan spesifikasi FIPS 204, dengan data pembanding dari literatur benchmarking independen.*

Tiga implikasi operasional mengikuti langsung. **Pertama**, ukuran tanda tangan adalah constraint utama untuk sebagian besar deployment enterprise. Signature ML-DSA-65 sekitar lima puluh kali ukuran signature ECDSA P-256, dan TLS certificate chains yang membawa intermediate CA bertumbuh proporsional. **Kedua**, ML-KEM kompetitif secara komputasi dengan ECDH dan dalam beberapa implementasi lebih cepat, terutama pada hardware dengan dukungan vectorised untuk arithmetic lattice. **Ketiga**, verifikasi ML-DSA konsisten cepat, sering lebih cepat daripada verifikasi ECDSA, tetapi signing ML-DSA melibatkan rejection-sampling loop yang dapat membutuhkan beberapa percobaan pada hardware terbatas. Untuk signing services ber-throughput tinggi, ini benchmark yang harus diverifikasi, bukan diasumsikan.

### Memilih Parameter Set

Posisi yurisdiksi pada pemilihan parameter tidak identik, tetapi konvergensinya jelas. ML-KEM-768 dan ML-DSA-65 adalah lantai enterprise, didukung UK NCSC sebagai baseline untuk organisasi UK dan dapat diterima di sebagian besar framework Eropa. ML-KEM-1024 dan ML-DSA-87 adalah ceiling konservatif, diwajibkan NSA CNSA 2.0 untuk national security systems AS dan diwajibkan ASD untuk entitas teregulasi Australia pada 2030. Untuk data dengan sensitivitas jangka sangat panjang, sovereign settlement logs, intellectual property lebih dari satu dekade, custody records untuk instrumen long-dated, parameter set lebih tinggi adalah default yang defensible.

### Fondasi Matematis Bersama, Risiko Bersama

Poin tingkat dewan yang layak dicatat: ML-KEM dan ML-DSA sama-sama mengambil keamanan dari keluarga masalah lattice yang sama. Terobosan cryptanalytic masa depan terhadap Module-LWE akan memengaruhi kedua standar sekaligus. Inilah alasan beberapa otoritas nasional, terutama BSI Jerman dan ANSSI Prancis, merekomendasikan melengkapi stack berbasis lattice dengan hash-based signatures (SLH-DSA, FIPS 205) untuk use case long-term signing dan code signing. Crypto-agility, dalam arti ini, bukan hanya kemampuan mengganti RSA dengan ML-KEM. Ia adalah kemampuan mengganti satu algoritma PQC dengan algoritma PQC lain ketika lanskap cryptanalytic bergeser.

## Jalur Migrasi Logis: Discovery -> Triage -> Hybrid Deployment

Bagi dewan yang menyetujui program PQC multi-tahun, pertanyaan operasionalnya adalah bagaimana memfasekan pekerjaan tanpa mengambil risiko service availability yang tidak dapat diterima. Pola yang muncul di roadmap G7, framework NCSC, BIS Project Leap, dan guidance nasional besar berkumpul pada tiga fase.

```
┌──────────────────────┐   ┌──────────────────────┐   ┌──────────────────────┐
│  1. DISCOVERY & CBOM │ → │  2. TRIAGE (MOSCA)   │ → │  3. HYBRID DEPLOYMENT│
│  Cryptographic       │   │  Risk-based          │   │  Dual-envelope       │
│  inventory across    │   │  prioritisation by   │   │  classical + PQC,    │
│  all systems         │   │  data shelf life     │   │  crypto-agile        │
└──────────────────────┘   └──────────────────────┘   └──────────────────────┘
```

### Phase 1 — Discovery dan Cryptographic Bill of Materials (CBOM)

Migrasi tidak dapat direncanakan untuk estate kriptografis yang belum dipetakan, dan kebanyakan institusi belum memiliki peta akurat. Fase pertama adalah produksi Cryptographic Bill of Materials, inventaris terstruktur dari setiap instance kriptografi asimetris di organisasi, dengan setiap instance diberi tag untuk algoritma, panjang kunci, konteks protokol, sensitivitas data, dan system owner. Scanning otomatis di codebases, web applications, container images, database configurations, certificate stores, hardware security modules, dan vendor interfaces adalah mekanisme praktis; inventaris manual sistem legacy dan protokol proprietary adalah pelengkap yang tidak terhindarkan.

Output Phase 1 tidak glamor, tetapi satu-satunya fondasi untuk Phase 2 dan 3. Ini juga deliverable pertama yang akan dicari internal audit dan regulator eksternal ketika attestasi kepatuhan PQC mulai diminta.

### Phase 2 — Risk Triage Menggunakan Mosca Equation

Dengan CBOM di tangan, institusi dapat menerapkan framework Mosca asset demi asset. Untuk setiap ketergantungan kriptografis, pertanyaannya apakah **S + M > Q**, yaitu apakah shelf life data ditambah waktu migrasi melebihi estimasi waktu menuju CRQC. Asset yang ketimpangannya paling akut, data sensitif berumur panjang pada infrastruktur yang membutuhkan bertahun-tahun untuk bermigrasi, masuk ke depan antrean. Asset dengan lifespan data pendek atau infrastruktur yang sudah dimodernisasi dapat disekuensikan belakangan.

Di fase inilah risk appetite dewan paling terlihat. Nilai Q yang dipilih institusi pada dasarnya adalah taruhan strategis pada laju kemajuan hardware kuantum. Q konservatif, pertengahan 2030-an, menghasilkan rencana migrasi lebih agresif dan capital line jangka pendek lebih tinggi. Q optimistis, setelah 2040, menghasilkan rencana lebih santai dan residual exposure lebih tinggi terhadap data yang sudah dipanen. Keduanya harus menjadi keputusan eksplisit dewan, bukan default implisit fungsi teknologi.

### Phase 3 — Hybrid Deployment

Setelah asset prioritas diidentifikasi, deployment sebaiknya mengikuti pola hybrid yang dibuktikan Project Leap dan didukung NCSC, ANSSI, BSI, serta roadmap G7. Deployment hybrid menjalankan algoritma klasik dan algoritma post-quantum secara paralel, menggabungkan outputnya ke satu envelope. Komposit ini aman terhadap serangan klasik karena algoritma klasik bertahan hari ini, dan terhadap serangan kuantum karena algoritma PQC bertahan besok. Pola umum adalah X25519 digabung dengan ML-KEM-768 atau ML-KEM-1024 untuk key encapsulation, serta ECDSA digabung dengan ML-DSA untuk signatures ketika dual signatures feasible secara operasional.

Temuan Project Leap bahwa hybrid "much, much heavier" daripada pendekatan murni mana pun adalah penyeimbang jujur rekomendasi ini. Dewan perlu mengharapkan uplift compute dan storage capacity, handshake lebih panjang, serta kompleksitas certificate-chain tambahan selama transisi. Trade-off-nya: hybrid menghilangkan sumber risiko migrasi terbesar, yaitu cliff-edge cut-over dari satu fondasi kriptografis ke fondasi lain di environment produksi.

## Biayanya, dan Mengapa Tidak Melakukan Apa-apa Lebih Mahal

Analisis Mastercard, [dilaporkan awal 2026 ⧉](https://www.qnulabs.com/blog/bank-2030-expiry-date-q-day-fatal-strategy "Your Bank's 2030 Expiry — QNu Labs"), menempatkan biaya migrasi PQC sektor keuangan global pada $28-42 miliar. Di dalam agregat itu, riset [RedCompass Labs dan CMORG ⧉](https://www.cmorg.org.uk/sites/default/files/2025-06/CMORG%20-%20Guidance%20for%20Post-Quantum%20Cryptography%20-%20April%202025%20-%20TLP%20CLEAR%20(1).pdf "CMORG Guidance for Post-Quantum Cryptography") yang melacak belanja institusional aktual menunjukkan bank tier-one berkomitmen $20-30 juta per tahun untuk program kesiapan, dengan timeline implementasi melintasi beberapa siklus kepemimpinan. Angka-angka ini besar. Namun itu bukan pembanding yang relevan.

Pembanding yang relevan adalah biaya satu peristiwa dekripsi retrospektif. Bagi institusi yang wire traffic, korespondensi M&A, atau data counterparty exposure yang dipanen menjadi dapat dibaca adversary pada 2032, biaya operasional dan reputasinya tidak dibatasi oleh baris capex migrasi. Ia dibatasi oleh nilai satu dekade informasi strategis yang mendasarinya, yang bagi institusi systemically important mana pun secara material lebih besar daripada budget migrasi yang masuk akal. Framing G7 atas transisi kriptografis sebagai isu systemic risk-management, bukan upgrade teknologi, tepat, dan dewan harus menanganinya seperti itu.

Ada baris biaya kedua yang layak dipisahkan. Migrasi ke PQC adalah forcing function untuk crypto-agility, kemampuan arsitektural mengganti algoritma kriptografis tanpa membangun ulang sistem yang bergantung padanya. Kebanyakan institusi belum memiliki crypto-agility; dependensi RSA dan ECC mereka tertanam dalam PKI, code-signing chains, vendor integrations, dan protokol bespoke yang terakumulasi selama puluhan tahun. Investasi dalam agility, dibuat di bawah tekanan transisi PQC, bersifat tahan lama. Ia akan dipakai lagi ketika transisi kriptografis berikutnya tiba, apakah itu penerus PQC berbasis lattice, overlay quantum-key-distribution, atau sesuatu yang belum berada di roadmap standar.

## Kesimpulan

Argumen untuk memperlakukan migrasi post-quantum sebagai prioritas tingkat dewan pada 2026 tidak dibangun di atas imminence CRQC. Estimasinya tetap tidak pasti; opini akademik kredibel menempatkan probabilitas CRQC pada 2028 jauh di bawah satu persen, naik ke sekitar lima puluh persen pada 2037-2040. Argumennya dibangun pada tiga observasi lain yang tidak tidak pasti.

Pertama, harvest-now-decrypt-later terjadi hari ini, dan data dengan kebutuhan kerahasiaan lebih dari satu dekade terekspos terlepas dari kapan CRQC datang. Kedua, migrasi estate kriptografis institusi keuangan besar membutuhkan lima sampai tujuh tahun bahkan dengan pendanaan dan fokus kepemimpinan memadai, artinya program yang dimulai pada 2026 selesai sekitar 2031, masih di dalam ujung konservatif distribusi probabilitas CRQC. Ketiga, ekspektasi regulasi mengeras secara material dalam dua belas bulan terakhir, dan institusi yang risalah dewan 2026-nya mencatat program PQC jelas akan berada di posisi jauh lebih kuat daripada yang hanya mencatat watching brief.

Institusi yang mulai sekarang memiliki keuntungan pilihan. Mereka dapat menyusun pekerjaan melintasi siklus kepemimpinan, mengintegrasikannya dengan inisiatif resilience yang lebih luas, dan menyerap biaya operasional hybrid deployment dalam capital planning normal. Institusi yang menunggu akan menghadapi pekerjaan yang sama di bawah tenggat lebih ketat, dengan ruang sequencing lebih sedikit, dan di tengah keterbatasan pasokan hardware, expertise, dan kapasitas vendor yang mendukung PQC. Biaya bertindak lebih awal diketahui; biaya bertindak terlambat asimetris persis dengan cara yang hendak dihindari risk management.

Untuk konteks sebelumnya di situs ini, artikel [April 2026 tentang kompresi ambang kuantum](https://sebastienrousseau.com/2026-04-11-quantum-thresholds-are-moving-again/index.html "Quantum Thresholds Are Moving Again") membahas lintasan hardware yang mendasari, analisis [November 2023 tentang CRYSTALS-Kyber](https://sebastienrousseau.com/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html "CRYSTALS-Kyber: The Safeguarding Algorithm in a Quantum Age") membahas fondasi matematis yang kini distandarkan sebagai ML-KEM, artikel [Desember 2023 tentang Quantum Key Distribution](https://sebastienrousseau.com/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html "Quantum Key Distribution Revolutionising Security in Banking") membahas overlay [QKD](/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html) komplementer, dan [implementasi referensi open-source KyberLib](https://sebastienrousseau.com/2023-11-28-kyberlib-a-rust-powered-shield-against-quantum-threats/index.html "KyberLib: A Rust-Powered Shield Against Quantum Threats") menyediakan implementasi Rust dari primitive terkait bagi institusi yang ingin memeriksa permukaan kriptografis secara langsung. Keterlibatan dengan detail praktis dan teknis, bukan hanya headline regulasi, adalah cara dewan membedakan program migrasi kredibel dari compliance theatre.

## Pertanyaan yang Sering Diajukan

**Kapan cryptographically relevant quantum computer benar-benar akan ada?**

Estimasi kredibel sangat bervariasi. Per awal 2026, demonstrasi kuantum publik telah mencapai kira-kira 24 sampai 28 logical qubits, sementara CRQC diperkirakan membutuhkan sekitar 6.000 logical qubits yang ditopang oleh sesuatu antara 100.000 dan beberapa juta physical qubits, bergantung pada pendekatan error correction. Konsensus pakar menempatkan probabilitas CRQC di bawah satu persen pada 2028, sekitar lima puluh persen pada 2037-2040, dengan variasi signifikan antar prakiraan. Penurunan terbaru dalam estimasi resource teoretis, dari 20 juta qubit beberapa tahun lalu ke di bawah satu juta dalam karya Gidney 2025, lalu sekitar 100.000 dalam makalah arsitektur QLDPC Februari 2026, telah memadatkan horizon perencanaan. Untuk dewan, asumsi perencanaan yang sesuai adalah pertengahan 2030-an untuk sistem berisiko tinggi, akhir 2030-an sebagai midpoint konservatif, dan lebih awal jika HNDL exposure menjadi concern utama.

**Mengapa hybrid deployment, bukan pure post-quantum?**

Tiga alasan. Pertama, ML-KEM dan ML-DSA, walaupun telah ditelaah baik, memiliki sejarah cryptanalytic lebih pendek daripada RSA dan ECC. Skema hybrid tetap aman jika salah satu komponennya bertahan; skema PQC murni terekspos jika masalah lattice tiba-tiba melemah. Kedua, hybrid menjaga backward compatibility dengan counterparty yang belum bermigrasi, hal kritis dalam transisi industri multi-tahun. Ketiga, setiap otoritas besar di luar Australian Signals Directorate secara eksplisit merekomendasikan hybrid selama periode transisi: NCSC, ANSSI, BSI, NLNCSA, dan framework G7 semuanya mendukung pendekatan dual-envelope. Trade-off-nya, seperti dikuantifikasi Project Leap, adalah overhead compute dan storage yang lebih tinggi. Itulah harga optionality.

**Apakah kita membutuhkan ML-KEM dan ML-DSA, atau cukup salah satu?**

Keduanya. ML-KEM dan ML-DSA melayani peran kriptografis berbeda. ML-KEM mengganti primitive key-establishment di TLS, VPN, mobile authentication, dan protokol serupa ketika dua pihak perlu menyepakati shared symmetric key. ML-DSA mengganti primitive digital-signature dalam PKI certificates, code signing, document signing, SWIFT-style authenticated messaging, dan identity assertions. Estate kriptografis institusi memakai kedua jenis primitive di tempat berbeda; migrasi harus menangani keduanya.

**Bagaimana mengukur kemajuan program sebesar ini?**

Tiga metrik praktis dan selaras dengan framework regulasi besar. **Coverage CBOM**, yaitu persentase instance kriptografi asimetris institusi yang telah diinventarisasi, diklasifikasi, dan diberi prioritas migrasi. **Migration coverage high-risk assets**, yaitu persentase asset tempat kondisi Mosca S + M > Q terpenuhi yang telah dipindahkan ke hybrid PQC. **Crypto-agility coverage**, yaitu persentase sistem dengan dependensi kriptografis yang dapat mengganti algoritma tanpa perubahan kode, hanya konfigurasi. Roadmap G7 CEG, framework tiga fase NCSC, dan roadmap terkoordinasi EU semuanya kira-kira memetakan ke tiga ukuran ini, walaupun istilahnya berbeda.

**Apa biaya menunggu satu tahun lagi?**

Biayanya tidak nol, dan tidak simetris. Menunggu satu tahun mengorbankan satu tahun perlindungan HNDL pada data berumur panjang, data yang kebutuhan kerahasiaannya hingga 2040 terekspos setahun lebih lama daripada perlu. Ini memadatkan jendela migrasi terhadap tenggat regulasi tetap, seperti ASD 2030, milestone NSA CNSA 2.0, dan target EU 2030 untuk critical systems, yang menerjemah menjadi delivery risk lebih tinggi dan sequencing flexibility lebih rendah. Ini juga mengekspos institusi pada keterbatasan vendor dan talenta yang sudah terlihat di pasar dan akan memburuk ketika pemain terbesar industri berpindah dari planning ke execution. Biayanya tidak katastrofik dalam satu tahun mana pun, tetapi terakumulasi.

## Referensi

- Sebastien Rousseau, (2026). [Quantum Thresholds Are Moving Again](https://sebastienrousseau.com/2026-04-11-quantum-thresholds-are-moving-again/index.html "Quantum Thresholds Are Moving Again").
- Sebastien Rousseau, (2023). [CRYSTALS-Kyber: The Safeguarding Algorithm in a Quantum Age](https://sebastienrousseau.com/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html "CRYSTALS-Kyber: The Safeguarding Algorithm in a Quantum Age").
- Sebastien Rousseau, (2023). [Quantum Key Distribution Revolutionising Security in Banking](https://sebastienrousseau.com/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html "Quantum Key Distribution Revolutionising Security in Banking").
- Sebastien Rousseau, (2023). [KyberLib: A Rust-Powered Shield Against Quantum Threats](https://sebastienrousseau.com/2023-11-28-kyberlib-a-rust-powered-shield-against-quantum-threats/index.html "KyberLib: A Rust-Powered Shield Against Quantum Threats").
- G7 Cyber Expert Group, (2026). [Advancing a Coordinated Roadmap for the Transition to Post-Quantum Cryptography in the Financial Sector ⧉](https://www.gov.uk/government/publications/advancing-a-coordinated-roadmap-for-the-transition-to-post-quantum-cryptography-in-the-financial-sector/g7-cyber-expert-group-statement-on-advancing-a-coordinated-roadmap-for-the-transition-to-post-quantum-cryptography-in-the-financial-sector-january-20 "G7 CEG Statement, January 2026"). GOV.UK.
- Bank for International Settlements, (2025). [Project Leap Phase 2: Quantum-Proofing Payment Systems ⧉](https://www.bis.org/publ/othp107.htm "Project Leap phase 2: quantum-proofing payment systems"). BIS.
- NIST, (2024). [FIPS 203: Module-Lattice-Based Key-Encapsulation Mechanism Standard ⧉](https://csrc.nist.gov/pubs/fips/203/final "FIPS 203, Module-Lattice-Based Key-Encapsulation Mechanism Standard"). NIST.
- UK NCSC, (2025). [Timelines for Migration to Post-Quantum Cryptography ⧉](https://www.ncsc.gov.uk/guidance/pqc-migration-timelines "Timelines for migration to post-quantum cryptography — NCSC"). UK National Cyber Security Centre.
- CMORG, (2025). [Guidance for Post-Quantum Cryptography ⧉](https://www.cmorg.org.uk/sites/default/files/2025-06/CMORG%20-%20Guidance%20for%20Post-Quantum%20Cryptography%20-%20April%202025%20-%20TLP%20CLEAR%20(1).pdf "CMORG Guidance for Post-Quantum Cryptography"). Cross-Market Operational Resilience Group.
