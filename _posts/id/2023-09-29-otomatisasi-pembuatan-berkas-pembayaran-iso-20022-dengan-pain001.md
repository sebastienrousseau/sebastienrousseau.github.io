---
title: "Mengotomatiskan Pembuatan File Pembayaran ISO 20022 dengan pain001"
subtitle: "Otomasi pembayaran ISO 20022 dan rekayasa pembayaran grosir dengan pain001."
description: "Otomatiskan pembuatan file pembayaran ISO 20022 pain.001 dari CSV atau SQLite. pain001 adalah pustaka Python sumber terbuka yang menyederhanakan kepatuhan."
date: "Sep 29, 2023"
language: "id-ID"
locale: "id_ID"
banner: "https://cloudcdn.pro/stocks/images/andrea-de-santis-T3Qen8vVgRc.webp"
banner_alt: "Laptop yang dimatikan di atas meja kayu berwarna cokelat"
keywords: "pain001, ISO 20022, pain.001.001.09, CustomerCreditTransferInitiation, SEPA Credit Transfer, CBPR+, otomasi pembayaran, pembuatan XML, validasi XSD, GrpHdr, PmtInf, CdtTrfTxInf, CtrlSum, SWIFT"
---

![Laptop yang dimatikan di atas meja kayu berwarna cokelat](https://cloudcdn.pro/stocks/images/andrea-de-santis-T3Qen8vVgRc.webp).class=\"img-fluid clearfix\"

<!-- lead-start -->
<aside class="post-lead" aria-label="Ringkasan artikel">
<p class="post-lead-tldr"><strong>TL;DR.</strong> Otomatiskan pembuatan file pembayaran ISO 20022 pain.001 dari CSV atau SQLite. pain001 adalah pustaka Python sumber terbuka yang menyederhanakan kepatuhan.</p>
<p class="post-lead-heading"><strong>Kesimpulan utama</strong></p>
<ul class="post-lead-takeaways">
  <li><strong>Struktur pesan ISO 20022 pain.001.</strong> Pesan ISO 20022 pain.001.001.09 (CustomerCreditTransferInitiation) memiliki tiga tingkat.</li>
  <li><strong>Menghasilkan XML dari CSV.</strong> Pemanggilan pain001 minimal membutuhkan hanya beberapa argumen.</li>
  <li><strong>Struktur XML yang dihasilkan.</strong> Dokumen pain.001.001.09 yang benar mempertahankan hierarki GrpHdr, PmtInf, dan CdtTrfTxInf.</li>
  <li><strong>Pipeline validasi XSD.</strong> Setelah rendering, pain001 memvalidasi output terhadap skema XSD ISO 20022 pain.001.001.09.</li>
</ul>
<p class="post-lead-related"><strong>Bacaan terkait:</strong> <a href="https://sebastienrousseau.com/2023-10-09-the-fastest-rust-based-static-site-generator/index.html">Static Site Generator: Fastest Rust-Based SSG</a>, <a href="https://sebastienrousseau.com/2018-01-02-blockchain-the-technology-that-matters-in-2018/index.html">Blockchain explained, the technology that matters the most</a>, <a href="https://sebastienrousseau.com/2026-05-14-securing-the-ledger-post-quantum-migration-corporate-finance">Securing the Ledger: A Board-Level Guide to Post-Quantum Migration for Corporate Finance</a>.</p>
</aside>
<!-- lead-end -->

> **Ringkasan eksekutif / kesimpulan utama**
>
> - **ISO 20022 pain.001** (CustomerCreditTransferInitiation) adalah format pesan XML terstruktur yang digunakan untuk memulai transfer kredit di bawah SEPA (rulebook EPC SCT) dan CBPR+ (standar pesan lintas batas SWIFT, wajib bagi bank koresponden untuk pesan outbound mulai November 2025).
> - **[pain001 ⧉][00]** membaca data pembayaran dari CSV atau SQLite, memetakan baris ke hierarki pesan pain.001.001.09 (GrpHdr -> PmtInf -> CdtTrfTxInf), lalu merender file XML yang sesuai melalui generator bertemplat - tiga baris Python dari data menjadi XML tervalidasi.
> - **Validasi XSD** berjalan pada setiap file yang dihasilkan sebelum output ditulis; pustaka menaikkan exception deskriptif yang mengidentifikasi elemen, kardinalitas, atau mismatch tipe yang gagal, sehingga kesalahan tertangkap saat generasi, bukan saat pengiriman ke bank.
> - **CtrlSum dan NbOfTxs** dihitung dari kumpulan transaksi, bukan dimasukkan manual - menghilangkan salah satu penyebab penolakan file pembayaran paling umum di gateway pemrosesan SEPA dan CBPR+.
> - Varian pesan **SEPA Credit Transfer** (EUR, di zona SEPA) dan **CBPR+** (lintas batas, multi-mata uang) didukung melalui parameter `message_type`, dengan perbedaan validasi per field ditangani secara internal.

[**pain001 ⧉**][00] adalah pustaka Python sumber terbuka untuk menghasilkan file inisiasi pembayaran ISO 20022. Pustaka ini membaca data pembayaran dari input terstruktur (CSV atau SQLite), memvalidasi data, merender dokumen XML pain.001.001.09 yang sesuai, lalu memvalidasi output terhadap skema XSD ISO 20022 - semuanya dalam satu pemanggilan fungsi.

Artikel ini menjelaskan struktur pesan ISO 20022 pain.001, bagaimana pain001 memetakan data input ke elemen pesan, pipeline validasi, serta opsi konfigurasi SEPA dibandingkan CBPR+.

## Struktur Pesan ISO 20022 pain.001

Pesan ISO 20022 pain.001.001.09 (CustomerCreditTransferInitiation) memiliki tiga tingkat:

**GrpHdr** (Group Header) - satu per file:

| Elemen | Deskripsi | Contoh |
|---|---|---|
| `MsgId` | Pengidentifikasi pesan unik | `ACME20240115-001` |
| `CreDtTm` | Tanggal dan waktu pembuatan | `2024-01-15T09:00:00` |
| `NbOfTxs` | Jumlah total transaksi | `3` |
| `CtrlSum` | Jumlah seluruh amount yang diinstruksikan | `15000.00` |
| `InitgPty/Nm` | Nama pihak penginisiasi | `Acme Corp` |

**PmtInf** (Payment Information) - satu atau lebih per file, mengelompokkan transaksi berdasarkan rekening debitur dan tanggal pembayaran:

| Elemen | Deskripsi |
|---|---|
| `PmtInfId` | Pengidentifikasi informasi pembayaran |
| `PmtMtd` | Metode pembayaran - selalu `TRF` untuk transfer kredit |
| `ReqdExctnDt/Dt` | Tanggal eksekusi yang diminta |
| `Dbtr/Nm` | Nama debitur atau pengirim |
| `DbtrAcct/Id/IBAN` | IBAN debitur |
| `DbtrAgt/FinInstnId/BICFI` | BIC bank debitur |

**CdtTrfTxInf** (Credit Transfer Transaction Information) - satu atau lebih per blok PmtInf:

| Elemen | Deskripsi |
|---|---|
| `PmtId/EndToEndId` | Referensi end-to-end yang dipertahankan sepanjang rantai |
| `Amt/InstdAmt` | Amount yang diinstruksikan dengan atribut mata uang |
| `CdtrAgt/FinInstnId/BICFI` | BIC bank kreditur |
| `Cdtr/Nm` | Nama kreditur atau penerima |
| `CdtrAcct/Id/IBAN` | IBAN kreditur |
| `RmtInf/Ustrd` | Informasi remitansi tidak terstruktur, misalnya referensi invoice |

## Menghasilkan XML dari CSV

Pemanggilan pain001 minimal:

```python
from pain001 import create_xml_v9

create_xml_v9(
    data_file="payments.csv",
    data_file_type="csv",
    xml_file_path="output/pain001.xml"
)
```

File CSV memetakan nama kolom ke field pesan. Contoh minimal:

```csv
id,date,nb_of_txs,ctrl_sum,initiating_party_name,debtor_name,debtor_account_IBAN,debtor_agent_BIC,creditor_name,creditor_account_IBAN,creditor_agent_BIC,instd_amt,instd_amt_ccy,end_to_end_id,remittance_info
1,2024-01-15,1,1000.00,Acme Corp,Acme Corp,GB29NWBK60161331926819,NWBKGB2L,Supplier Ltd,DE89370400440532013000,COBADEFFXXX,1000.00,EUR,ACME20240115001,INV-2024-0042
```

Pustaka membaca `ctrl_sum` dan `nb_of_txs` dari baris CSV untuk file satu baris. Untuk file multi-baris, yaitu beberapa transaksi dalam satu batch, pain001 menghitung nilai tersebut dari kumpulan transaksi alih-alih mempercayai nilai input. Ini mencegah mismatch.

Antarmuka SQLite memakai konvensi nama kolom yang sama. Berikan `data_file_type="sqlite"` dan path `data_file` ke file database SQLite; secara default pain001 membaca tabel `payment`.

## Struktur XML yang Dihasilkan

Dokumen pain.001.001.09 yang dirender dengan benar untuk baris CSV di atas:

```xml
<Document xmlns="urn:iso:std:iso:20022:tech:xsd:pain.001.001.09">
  <CstmrCdtTrfInitn>
    <GrpHdr>
      <MsgId>ACME20240115-001</MsgId>
      <CreDtTm>2024-01-15T09:00:00</CreDtTm>
      <NbOfTxs>1</NbOfTxs>
      <CtrlSum>1000.00</CtrlSum>
      <InitgPty><Nm>Acme Corp</Nm></InitgPty>
    </GrpHdr>
    <PmtInf>
      <PmtInfId>ACME20240115-PMT-001</PmtInfId>
      <PmtMtd>TRF</PmtMtd>
      <ReqdExctnDt><Dt>2024-01-16</Dt></ReqdExctnDt>
      <Dbtr><Nm>Acme Corp</Nm></Dbtr>
      <DbtrAcct><Id><IBAN>GB29NWBK60161331926819</IBAN></Id></DbtrAcct>
      <DbtrAgt><FinInstnId><BICFI>NWBKGB2L</BICFI></FinInstnId></DbtrAgt>
      <CdtTrfTxInf>
        <PmtId><EndToEndId>ACME20240115001</EndToEndId></PmtId>
        <Amt><InstdAmt Ccy="EUR">1000.00</InstdAmt></Amt>
        <CdtrAgt><FinInstnId><BICFI>COBADEFFXXX</BICFI></FinInstnId></CdtrAgt>
        <Cdtr><Nm>Supplier Ltd</Nm></Cdtr>
        <CdtrAcct><Id><IBAN>DE89370400440532013000</IBAN></Id></CdtrAcct>
        <RmtInf><Ustrd>INV-2024-0042</Ustrd></RmtInf>
      </CdtTrfTxInf>
    </PmtInf>
  </CstmrCdtTrfInitn>
</Document>
```

## Pipeline Validasi XSD

Setelah rendering, pain001 memvalidasi output terhadap skema XSD ISO 20022 pain.001.001.09. Validasi memeriksa:

- **Keberadaan elemen wajib**: GrpHdr/MsgId, GrpHdr/CreDtTm, GrpHdr/NbOfTxs, dan GrpHdr/CtrlSum semuanya wajib; ketiadaan salah satunya menaikkan validation error.
- **Batasan tipe**: format IBAN, format BIC (8 atau 11 karakter), presisi amount (maksimum 18 digit, 5 desimal).
- **Kardinalitas**: minimal satu `CdtTrfTxInf` per `PmtInf`; minimal satu `PmtInf` per dokumen.
- **Nilai enumerasi**: `PmtMtd` harus `TRF` untuk transfer kredit; `Ccy` harus kode mata uang ISO 4217 yang valid.

Ketika validasi gagal, pain001 menaikkan `ValidationError` dengan pesan lxml yang mengidentifikasi ekspresi XPath, nama elemen, dan constraint yang gagal. Ini memunculkan salah konfigurasi pada waktu generasi, bukan saat pengiriman ke bank, ketika kode penolakan biasanya kurang deskriptif.

## Konfigurasi SEPA vs CBPR+

SEPA Credit Transfer (ISO 20022 pain.001.001.09 di bawah rulebook EPC SCT) dan CBPR+ (standar SWIFT Cross-Border Payments and Reporting Plus) memakai skema pesan yang sama, tetapi berbeda dalam field wajib dan batasan nilai:

| Aspek | SEPA SCT | CBPR+ |
|---|---|---|
| Mata uang | Hanya EUR | Multi-mata uang |
| IBAN wajib | Ya | Ya (kreditur) |
| BIC wajib | Tidak (routing zona SEPA) | Ya |
| Charge bearer (`ChrgBr`) | `SLEV` | `DEBT`, `CRED`, atau `SHAR` |
| Cakupan | Zona SEPA (36 negara) | Perbankan koresponden global |

Konfigurasikan tipe pesan melalui parameter `payment_initiation_message_type`:

```python
create_xml_v9(
    data_file="payments.csv",
    data_file_type="csv",
    xml_file_path="output/pain001.xml",
    payment_initiation_message_type="pain.001.001.09"  # default; also accepts "pain.001.001.03" for legacy SEPA
)
```

Kepatuhan CBPR+ menjadi wajib untuk perbankan koresponden SWIFT pada November 2023 untuk pesan inbound dan November 2025 untuk outbound. Menghasilkan file pain.001 yang sesuai CBPR+ mensyaratkan field BIC terisi dan elemen `ChrgBr` hadir.

## Pertanyaan yang Sering Diajukan

**Apa perbedaan antara pain.001 dan pain.008?**

pain.001 (CustomerCreditTransferInitiation) memulai transfer kredit: bank pengirim mendebit rekening pengirim dan mengkredit penerima. pain.008 (CustomerDirectDebitInitiation) memulai direct debit: bank kreditur menagih dana dari debitur. Pustaka pain001 hanya menghasilkan file pain.001.

**Versi ISO 20022 apa yang ditargetkan pain001?**

Target utama adalah pain.001.001.09, versi yang diperlukan untuk CBPR+ dan diwajibkan oleh EPC untuk implementasi SEPA baru. Pustaka juga mendukung pain.001.001.03, versi SEPA lama, melalui parameter `payment_initiation_message_type` untuk organisasi yang masih memakai antarmuka bank lama.

**Apakah pain001 dapat menangani beberapa rekening debitur dalam satu file?**

Ya. Beberapa blok `PmtInf` dengan IBAN debitur berbeda dapat dibuat dengan mengelompokkan baris CSV yang memiliki nilai rekening debitur berbeda. pain001 membuat satu blok `PmtInf` per kombinasi unik (IBAN debitur, tanggal eksekusi), dengan semua transaksi yang cocok disarangkan sebagai anak `CdtTrfTxInf`.

**Apa yang terjadi ketika validasi XSD gagal?**

pain001 menaikkan `pain001.exceptions.ValidationError` dengan pesan validasi lxml. File XML tidak ditulis ke disk ketika validasi gagal, sehingga hanya file valid yang mencapai path output. Penyebab umum kegagalan adalah IBAN dengan format salah, BIC bukan 8 atau 11 karakter, kode mata uang tidak ada di ISO 4217, atau elemen wajib hilang karena kolom CSV yang diperlukan tidak ada.

## Referensi

1. European Payments Council. *SEPA Credit Transfer Scheme Customer-to-Bank Implementation Guidelines (v1.1)*. EPC, 2023. https://www.europeanpaymentscouncil.eu/document-library/implementation-guidelines/sepa-credit-transfer-scheme-customer-bank
2. SWIFT. *CBPR+ Usage Guidelines - Customer Credit Transfer Initiation (pain.001)*. SWIFT Standards, 2023. https://www.swift.com/standards/iso-20022/cbpr-plus-usage-guidelines
3. ISO. *ISO 20022 - Financial services - Universal financial industry message scheme*. ISO.org, 2023. https://www.iso20022.org/
4. Rousseau, S. *pain001 - ISO 20022 payment file generator*. GitHub, 2023. https://github.com/sebastienrousseau/pain001

[00]: https://pain001.com/ "pain001: Automate ISO 20022-Compliant Payment File Creation"
[01]: https://www.iso20022.org/ "ISO 20022: Universal financial industry message scheme"
