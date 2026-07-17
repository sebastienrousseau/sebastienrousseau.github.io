---
title: "Mengautomasikan Penciptaan Fail Pembayaran ISO 20022 dengan pain001"
tags: "pain001, ISO 20022, CustomerCreditTransferInitiation, SEPACreditTransfer, CBPR, payment automation, XMLGeneration, XSDValidation, SWIFT, post-quantum cryptography, AI, open source, cross-border payments, Rust"
subtitle: "Automasi pembayaran ISO 20022 dan kejuruteraan pembayaran borong dengan pain001."
description: "Automasikan penciptaan fail pembayaran ISO 20022 pain.001 daripada CSV atau SQLite. pain001 ialah pustaka Python sumber terbuka yang memperkemas pematuhan."
date: "Sep 29, 2023"
language: "ms"
locale: "ms_MY"
banner: "https://cloudcdn.pro/stocks/images/andrea-de-santis-T3Qen8vVgRc.webp"
banner_alt: "Komputer riba yang dimatikan di atas meja kayu perang"
keywords: "pain001, ISO 20022, pain.001.001.09, CustomerCreditTransferInitiation, SEPA Credit Transfer, CBPR+, automasi pembayaran, penjanaan XML, pengesahan XSD, GrpHdr, PmtInf, CdtTrfTxInf, CtrlSum, SWIFT"
---

> **Ringkasan Eksekutif / Perkara Utama**
>
> - **ISO 20022 pain.001** (CustomerCreditTransferInitiation) ialah format mesej XML berstruktur yang digunakan untuk memulakan pemindahan kredit di bawah SEPA (buku peraturan EPC SCT) dan CBPR+ (piawaian pemesejan rentas sempadan SWIFT, wajib bagi bank koresponden mulai November 2025).
> - **[pain001 ⧉][00]** membaca data pembayaran daripada CSV atau SQLite, memetakan baris kepada hierarki mesej pain.001.001.09 (GrpHdr → PmtInf → CdtTrfTxInf), dan memapar fail XML yang mematuhi piawaian melalui penjana bertemplat, iaitu tiga baris Python daripada data kepada XML yang disahkan.
> - **Pengesahan XSD** berjalan pada setiap fail yang dijana sebelum output ditulis; pustaka ini menimbulkan pengecualian deskriptif yang mengenal pasti elemen, kardinaliti, atau ketidakpadanan jenis yang gagal, supaya ralat ditangkap pada masa penjanaan dan bukannya pada masa penyerahan ke bank.
> - **CtrlSum dan NbOfTxs** dikira daripada set transaksi, bukan dimasukkan secara manual, lantas menghapuskan punca penolakan fail pembayaran yang paling lazim di get pemprosesan SEPA dan CBPR+.
> - Kedua-dua varian mesej **SEPA Credit Transfer** (EUR, dalam zon SEPA) dan **CBPR+** (rentas sempadan, pelbagai mata wang) disokong melalui parameter `message_type`, dengan perbezaan pengesahan peringkat medan dikendalikan secara dalaman.

[**pain001 ⧉**][00] ialah pustaka Python sumber terbuka untuk menjana fail permulaan pembayaran ISO 20022. Ia membaca data pembayaran daripada input berstruktur (CSV atau SQLite), mengesahkan data, memapar dokumen XML pain.001.001.09 yang mematuhi piawaian, dan mengesahkan output terhadap skema XSD ISO 20022, semuanya dalam satu panggilan fungsi.

Artikel ini menerangkan struktur mesej ISO 20022 pain.001, cara pain001 memetakan data input kepada elemen mesej, saluran pengesahan, dan pilihan konfigurasi SEPA berbanding CBPR+.

## Struktur Mesej ISO 20022 pain.001

Mesej ISO 20022 pain.001.001.09 (CustomerCreditTransferInitiation) mempunyai tiga peringkat:

**GrpHdr** (Group Header), satu setiap fail:

| Elemen | Penerangan | Contoh |
|---|---|---|
| `MsgId` | Pengecam mesej yang unik | `ACME20240115-001` |
| `CreDtTm` | Tarikh dan masa penciptaan | `2024-01-15T09:00:00` |
| `NbOfTxs` | Jumlah bilangan transaksi | `3` |
| `CtrlSum` | Jumlah semua amaun yang diarahkan | `15000.00` |
| `InitgPty/Nm` | Nama pihak yang memulakan | `Acme Corp` |

**PmtInf** (Payment Information), satu atau lebih setiap fail, mengumpulkan transaksi mengikut akaun penghutang dan tarikh pembayaran:

| Elemen | Penerangan |
|---|---|
| `PmtInfId` | Pengecam maklumat pembayaran |
| `PmtMtd` | Kaedah pembayaran, sentiasa `TRF` untuk pemindahan kredit |
| `ReqdExctnDt/Dt` | Tarikh pelaksanaan yang diminta |
| `Dbtr/Nm` | Nama penghutang (penghantar) |
| `DbtrAcct/Id/IBAN` | IBAN penghutang |
| `DbtrAgt/FinInstnId/BICFI` | BIC bank penghutang |

**CdtTrfTxInf** (Credit Transfer Transaction Information), satu atau lebih setiap blok PmtInf:

| Elemen | Penerangan |
|---|---|
| `PmtId/EndToEndId` | Rujukan hujung ke hujung (dikekalkan sepanjang rantaian) |
| `Amt/InstdAmt` | Amaun yang diarahkan dengan atribut mata wang |
| `CdtrAgt/FinInstnId/BICFI` | BIC bank pemiutang |
| `Cdtr/Nm` | Nama pemiutang (penerima) |
| `CdtrAcct/Id/IBAN` | IBAN pemiutang |
| `RmtInf/Ustrd` | Maklumat kiriman wang tidak berstruktur (rujukan invois dsb.) |

## Menjana XML daripada CSV

Panggilan pain001 yang minimum:

```python
from pain001 import create_xml_v9

create_xml_v9(
    data_file="payments.csv",
    data_file_type="csv",
    xml_file_path="output/pain001.xml"
)
```

Fail CSV memetakan nama lajur kepada medan mesej. Contoh yang minimum:

```csv
id,date,nb_of_txs,ctrl_sum,initiating_party_name,debtor_name,debtor_account_IBAN,debtor_agent_BIC,creditor_name,creditor_account_IBAN,creditor_agent_BIC,instd_amt,instd_amt_ccy,end_to_end_id,remittance_info
1,2024-01-15,1,1000.00,Acme Corp,Acme Corp,GB29NWBK60161331926819,NWBKGB2L,Supplier Ltd,DE89370400440532013000,COBADEFFXXX,1000.00,EUR,ACME20240115001,INV-2024-0042
```

Pustaka ini membaca `ctrl_sum` dan `nb_of_txs` daripada baris CSV untuk fail baris tunggal. Untuk fail berbilang baris (berbilang transaksi dalam satu kelompok), pain001 mengira nilai ini daripada set transaksi dan bukannya mempercayai nilai input, yang menghalang ketidakpadanan.

Antara muka SQLite menggunakan konvensyen nama lajur yang sama. Hantar `data_file_type="sqlite"` dan laluan `data_file` ke fail pangkalan data SQLite; pain001 membaca jadual `payment` secara lalai.

## Struktur XML Terjana

Dokumen pain.001.001.09 yang dipapar dengan betul untuk baris CSV di atas:

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

## Saluran Pengesahan XSD

Selepas pemaparan, pain001 mengesahkan output terhadap skema XSD ISO 20022 pain.001.001.09. Pemeriksaan pengesahan:

- **Kehadiran elemen wajib**: GrpHdr/MsgId, GrpHdr/CreDtTm, GrpHdr/NbOfTxs, GrpHdr/CtrlSum semuanya diperlukan; jika mana-mana tiada, ralat pengesahan akan ditimbulkan.
- **Kekangan jenis**: format IBAN, format BIC (8 atau 11 aksara), kejituan amaun (maksimum 18 digit, 5 tempat perpuluhan).
- **Kardinaliti**: sekurang-kurangnya satu `CdtTrfTxInf` setiap `PmtInf`; sekurang-kurangnya satu `PmtInf` setiap dokumen.
- **Nilai penghitungan**: `PmtMtd` mestilah `TRF` untuk pemindahan kredit; `Ccy` mestilah kod mata wang ISO 4217 yang sah.

Apabila pengesahan gagal, pain001 menimbulkan `ValidationError` dengan mesej ralat lxml yang mengenal pasti ungkapan XPath, nama elemen, dan kekangan yang gagal. Ini mendedahkan salah konfigurasi pada masa penjanaan dan bukannya pada masa penyerahan ke bank, di mana kod penolakan lazimnya kurang deskriptif.

## Konfigurasi SEPA berbanding CBPR+

SEPA Credit Transfer (ISO 20022 pain.001.001.09 di bawah buku peraturan EPC SCT) dan CBPR+ (piawaian Cross-Border Payments and Reporting Plus SWIFT) menggunakan skema mesej yang sama tetapi berbeza dalam set medan wajib dan kekangan nilai:

| Aspek | SEPA SCT | CBPR+ |
|---|---|---|
| Mata wang | EUR sahaja | Pelbagai mata wang |
| IBAN wajib | Ya | Ya (pemiutang) |
| BIC wajib | Tidak (penghalaan zon SEPA) | Ya |
| Penanggung caj (`ChrgBr`) | `SLEV` | `DEBT`, `CRED`, atau `SHAR` |
| Skop | Zon SEPA (36 negara) | Perbankan koresponden global |

Konfigurasikan jenis mesej melalui parameter `payment_initiation_message_type`:

```python
create_xml_v9(
    data_file="payments.csv",
    data_file_type="csv",
    xml_file_path="output/pain001.xml",
    payment_initiation_message_type="pain.001.001.09"  # lalai; turut menerima "pain.001.001.03" untuk SEPA legasi
)
```

Pematuhan CBPR+ menjadi wajib untuk perbankan koresponden SWIFT pada November 2023 bagi mesej masuk dan November 2025 bagi mesej keluar. Menjana fail pain.001 yang mematuhi CBPR+ memerlukan medan BIC diisi dan elemen `ChrgBr` hadir.

## Soalan Lazim

**Apakah perbezaan antara pain.001 dan pain.008?**
pain.001 (CustomerCreditTransferInitiation) memulakan pemindahan kredit, iaitu bank penghantar mendebitkan akaun penghantar dan mengkreditkan penerima. pain.008 (CustomerDirectDebitInitiation) memulakan debit terus, iaitu bank pemiutang mengutip dana daripada penghutang. Pustaka pain001 menjana fail pain.001 sahaja.

**Versi ISO 20022 manakah yang disasarkan oleh pain001?**
Sasaran utama ialah pain.001.001.09, versi yang diperlukan untuk CBPR+ dan diwajibkan oleh EPC bagi pelaksanaan SEPA baharu. Pustaka ini turut menyokong pain.001.001.03 (versi SEPA legasi) melalui parameter `payment_initiation_message_type` untuk organisasi yang masih menggunakan antara muka bank yang lebih lama.

**Bolehkah pain001 mengendalikan berbilang akaun penghutang dalam satu fail?**
Ya. Berbilang blok `PmtInf` dengan IBAN penghutang yang berbeza boleh dihasilkan dengan mengumpulkan baris CSV yang mempunyai nilai akaun penghutang yang berbeza. pain001 mencipta satu blok `PmtInf` bagi setiap kombinasi unik (IBAN penghutang, tarikh pelaksanaan), dengan semua transaksi yang sepadan disarangkan sebagai anak `CdtTrfTxInf`.

**Apakah yang berlaku apabila pengesahan XSD gagal?**
pain001 menimbulkan `pain001.exceptions.ValidationError` dengan mesej pengesahan lxml. Fail XML tidak ditulis ke cakera apabila pengesahan gagal, jadi hanya fail yang sah mencapai laluan output. Punca kegagalan yang lazim ialah: IBAN dalam format yang salah, BIC bukan 8 atau 11 aksara, kod mata wang tiada dalam ISO 4217, atau elemen wajib yang hilang apabila lajur CSV yang diperlukan tidak ada.

## Rujukan

1. European Payments Council. *SEPA Credit Transfer Scheme Customer-to-Bank Implementation Guidelines (v1.1)*. EPC, 2023. https://www.europeanpaymentscouncil.eu/document-library/implementation-guidelines/sepa-credit-transfer-scheme-customer-bank
2. SWIFT. *CBPR+ Usage Guidelines — Customer Credit Transfer Initiation (pain.001)*. SWIFT Standards, 2023. https://www.swift.com/standards/iso-20022/cbpr-plus-usage-guidelines
3. ISO. *ISO 20022 — Financial services — Universal financial industry message scheme*. ISO.org, 2023. https://www.iso20022.org/
4. Rousseau, S. *pain001 — ISO 20022 payment file generator*. GitHub, 2023. https://github.com/sebastienrousseau/pain001

[00]: https://pain001.com/ "pain001: Automasikan Penciptaan Fail Pembayaran yang Mematuhi ISO 20022"
[01]: https://www.iso20022.org/ "ISO 20022: Skema mesej industri kewangan sejagat"
