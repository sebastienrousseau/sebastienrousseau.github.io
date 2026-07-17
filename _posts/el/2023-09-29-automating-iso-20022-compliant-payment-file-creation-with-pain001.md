---
title: "Αυτοματοποίηση της δημιουργίας αρχείων πληρωμών ISO 20022 με το pain001"
tags: "pain001, ISO 20022, CustomerCreditTransferInitiation, SEPACreditTransfer, CBPR, payment automation, XMLGeneration, XSDValidation, SWIFT, post-quantum cryptography, AI, open source, cross-border payments, Rust"
subtitle: "Αυτοματοποίηση πληρωμών ISO 20022 και μηχανική πληρωμών χονδρικής με το pain001."
description: "Αυτοματοποιήστε τη δημιουργία αρχείων πληρωμών ISO 20022 pain.001 από CSV ή SQLite. Το pain001 είναι η βιβλιοθήκη Python ανοικτού κώδικα που απλοποιεί τη συμμόρφωση."
date: "Sep 29, 2023"
language: "el"
locale: "el_GR"
banner: "https://cloudcdn.pro/stocks/images/andrea-de-santis-T3Qen8vVgRc.webp"
banner_alt: "Απενεργοποιημένος φορητός υπολογιστής πάνω σε καφέ ξύλινο τραπέζι"
keywords: "pain001, ISO 20022, pain.001.001.09, CustomerCreditTransferInitiation, SEPA Credit Transfer, CBPR+, αυτοματοποίηση πληρωμών, δημιουργία XML, επικύρωση XSD, GrpHdr, PmtInf, CdtTrfTxInf, CtrlSum, SWIFT"
---

> **Εκτελεστική σύνοψη / Βασικά συμπεράσματα**
>
> - Το **ISO 20022 pain.001** (CustomerCreditTransferInitiation) είναι η δομημένη μορφή μηνύματος XML που χρησιμοποιείται για την εκκίνηση μεταφορών πίστωσης στο πλαίσιο του SEPA (κανονισμός EPC SCT) και του CBPR+ (το πρότυπο διασυνοριακής μηνυματοδοσίας του SWIFT, υποχρεωτικό για τις ανταποκρίτριες τράπεζες από τον Νοέμβριο 2025).
> - Το **[pain001 ⧉][00]** διαβάζει δεδομένα πληρωμών από CSV ή SQLite, αντιστοιχίζει τις γραμμές στην ιεραρχία μηνύματος pain.001.001.09 (GrpHdr → PmtInf → CdtTrfTxInf) και αποδίδει ένα συμμορφούμενο αρχείο XML μέσω μιας γεννήτριας με πρότυπα — τρεις γραμμές Python από τα δεδομένα σε επικυρωμένο XML.
> - Η **επικύρωση XSD** εκτελείται σε κάθε παραγόμενο αρχείο πριν εγγραφεί η έξοδος· η βιβλιοθήκη εγείρει μια περιγραφική εξαίρεση που προσδιορίζει το στοιχείο, τον πληθαρισμό ή την αναντιστοιχία τύπου που αποτυγχάνει, ώστε τα σφάλματα να εντοπίζονται κατά τη δημιουργία και όχι κατά την υποβολή στην τράπεζα.
> - Τα **CtrlSum και NbOfTxs** υπολογίζονται από το σύνολο των συναλλαγών, δεν εισάγονται χειροκίνητα — εξαλείφοντας τη μεμονωμένη πιο συχνή αιτία απόρριψης αρχείων πληρωμών στις πύλες επεξεργασίας SEPA και CBPR+.
> - Υποστηρίζονται τόσο οι παραλλαγές μηνυμάτων **SEPA Credit Transfer** (EUR, εντός της ζώνης SEPA) όσο και **CBPR+** (διασυνοριακές, πολυνομισματικές) μέσω της παραμέτρου `message_type`, με τις διαφορές επικύρωσης σε επίπεδο πεδίου να αντιμετωπίζονται εσωτερικά.

Το [**pain001 ⧉**][00] είναι μια βιβλιοθήκη Python ανοικτού κώδικα για τη δημιουργία αρχείων εκκίνησης πληρωμών ISO 20022. Διαβάζει δεδομένα πληρωμών από μια δομημένη είσοδο (CSV ή SQLite), επικυρώνει τα δεδομένα, αποδίδει ένα συμμορφούμενο έγγραφο XML pain.001.001.09 και επικυρώνει την έξοδο έναντι του σχήματος XSD ISO 20022 — όλα σε μία μόνο κλήση συνάρτησης.

Αυτό το άρθρο περιγράφει τη δομή του μηνύματος ISO 20022 pain.001, τον τρόπο με τον οποίο το pain001 αντιστοιχίζει τα δεδομένα εισόδου στα στοιχεία του μηνύματος, τη διοχέτευση επικύρωσης και τις επιλογές διαμόρφωσης SEPA έναντι CBPR+.

## Δομή μηνύματος ISO 20022 pain.001

Το μήνυμα ISO 20022 pain.001.001.09 (CustomerCreditTransferInitiation) έχει τρία επίπεδα:

**GrpHdr** (Κεφαλίδα ομάδας) — ένα ανά αρχείο:

| Στοιχείο | Περιγραφή | Παράδειγμα |
|---|---|---|
| `MsgId` | Μοναδικό αναγνωριστικό μηνύματος | `ACME20240115-001` |
| `CreDtTm` | Ημερομηνία και ώρα δημιουργίας | `2024-01-15T09:00:00` |
| `NbOfTxs` | Συνολικός αριθμός συναλλαγών | `3` |
| `CtrlSum` | Άθροισμα όλων των εντελλόμενων ποσών | `15000.00` |
| `InitgPty/Nm` | Όνομα του μέρους που εκκινεί | `Acme Corp` |

**PmtInf** (Πληροφορίες πληρωμής) — μία ή περισσότερες ανά αρχείο, ομαδοποιεί τις συναλλαγές ανά λογαριασμό οφειλέτη και ημερομηνία πληρωμής:

| Στοιχείο | Περιγραφή |
|---|---|
| `PmtInfId` | Αναγνωριστικό πληροφοριών πληρωμής |
| `PmtMtd` | Μέθοδος πληρωμής — πάντα `TRF` για μεταφορά πίστωσης |
| `ReqdExctnDt/Dt` | Ζητούμενη ημερομηνία εκτέλεσης |
| `Dbtr/Nm` | Όνομα οφειλέτη (αποστολέα) |
| `DbtrAcct/Id/IBAN` | IBAN οφειλέτη |
| `DbtrAgt/FinInstnId/BICFI` | BIC τράπεζας οφειλέτη |

**CdtTrfTxInf** (Πληροφορίες συναλλαγής μεταφοράς πίστωσης) — μία ή περισσότερες ανά μπλοκ PmtInf:

| Στοιχείο | Περιγραφή |
|---|---|
| `PmtId/EndToEndId` | Αναφορά από άκρο σε άκρο (διατηρείται σε όλη την αλυσίδα) |
| `Amt/InstdAmt` | Εντελλόμενο ποσό με χαρακτηριστικό νομίσματος |
| `CdtrAgt/FinInstnId/BICFI` | BIC τράπεζας πιστωτή |
| `Cdtr/Nm` | Όνομα πιστωτή (παραλήπτη) |
| `CdtrAcct/Id/IBAN` | IBAN πιστωτή |
| `RmtInf/Ustrd` | Μη δομημένες πληροφορίες εμβάσματος (αναφορά τιμολογίου κ.λπ.) |

## Δημιουργία XML από CSV

Μια ελάχιστη κλήση του pain001:

```python
from pain001 import create_xml_v9

create_xml_v9(
    data_file="payments.csv",
    data_file_type="csv",
    xml_file_path="output/pain001.xml"
)
```

Το αρχείο CSV αντιστοιχίζει τα ονόματα στηλών σε πεδία μηνύματος. Ένα ελάχιστο παράδειγμα:

```csv
id,date,nb_of_txs,ctrl_sum,initiating_party_name,debtor_name,debtor_account_IBAN,debtor_agent_BIC,creditor_name,creditor_account_IBAN,creditor_agent_BIC,instd_amt,instd_amt_ccy,end_to_end_id,remittance_info
1,2024-01-15,1,1000.00,Acme Corp,Acme Corp,GB29NWBK60161331926819,NWBKGB2L,Supplier Ltd,DE89370400440532013000,COBADEFFXXX,1000.00,EUR,ACME20240115001,INV-2024-0042
```

Η βιβλιοθήκη διαβάζει τα `ctrl_sum` και `nb_of_txs` από τη γραμμή CSV για αρχεία μίας γραμμής. Για αρχεία πολλών γραμμών (πολλαπλές συναλλαγές σε μία παρτίδα), το pain001 υπολογίζει αυτές τις τιμές από το σύνολο των συναλλαγών αντί να εμπιστεύεται τις τιμές εισόδου, γεγονός που αποτρέπει τις αναντιστοιχίες.

Η διεπαφή SQLite χρησιμοποιεί την ίδια σύμβαση ονομάτων στηλών. Περάστε `data_file_type="sqlite"` και τη διαδρομή `data_file` προς ένα αρχείο βάσης δεδομένων SQLite· το pain001 διαβάζει τον πίνακα `payment` από προεπιλογή.

## Δομή του παραγόμενου XML

Ένα σωστά αποδοσμένο έγγραφο pain.001.001.09 για την παραπάνω γραμμή CSV:

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

## Διοχέτευση επικύρωσης XSD

Μετά την απόδοση, το pain001 επικυρώνει την έξοδο έναντι του σχήματος XSD ISO 20022 pain.001.001.09. Οι έλεγχοι επικύρωσης:

- **Παρουσία υποχρεωτικών στοιχείων**: τα GrpHdr/MsgId, GrpHdr/CreDtTm, GrpHdr/NbOfTxs, GrpHdr/CtrlSum απαιτούνται όλα· η απουσία οποιουδήποτε εγείρει σφάλμα επικύρωσης.
- **Περιορισμοί τύπου**: μορφή IBAN, μορφή BIC (8 ή 11 χαρακτήρες), ακρίβεια ποσού (μέγιστο 18 ψηφία, 5 δεκαδικά ψηφία).
- **Πληθαρισμός**: τουλάχιστον ένα `CdtTrfTxInf` ανά `PmtInf`· τουλάχιστον ένα `PmtInf` ανά έγγραφο.
- **Τιμές απαρίθμησης**: το `PmtMtd` πρέπει να είναι `TRF` για μεταφορές πίστωσης· το `Ccy` πρέπει να είναι έγκυρος κωδικός νομίσματος ISO 4217.

Όταν η επικύρωση αποτυγχάνει, το pain001 εγείρει ένα `ValidationError` με το μήνυμα σφάλματος του lxml που προσδιορίζει την έκφραση XPath, το όνομα του στοιχείου και τον περιορισμό που αποτυγχάνει. Αυτό αναδεικνύει τις εσφαλμένες διαμορφώσεις κατά τη δημιουργία και όχι κατά την υποβολή στην τράπεζα, όπου οι κωδικοί απόρριψης είναι συνήθως λιγότερο περιγραφικοί.

## Διαμόρφωση SEPA έναντι CBPR+

Το SEPA Credit Transfer (ISO 20022 pain.001.001.09 στο πλαίσιο του κανονισμού EPC SCT) και το CBPR+ (το πρότυπο Cross-Border Payments and Reporting Plus του SWIFT) χρησιμοποιούν το ίδιο σχήμα μηνύματος, αλλά διαφέρουν στα σύνολα υποχρεωτικών πεδίων και στους περιορισμούς τιμών:

| Πτυχή | SEPA SCT | CBPR+ |
|---|---|---|
| Νόμισμα | Μόνο EUR | Πολυνομισματικό |
| IBAN υποχρεωτικό | Ναι | Ναι (πιστωτής) |
| BIC υποχρεωτικό | Όχι (δρομολόγηση εντός ζώνης SEPA) | Ναι |
| Επιβάρυνση εξόδων (`ChrgBr`) | `SLEV` | `DEBT`, `CRED` ή `SHAR` |
| Εμβέλεια | Ζώνη SEPA (36 χώρες) | Παγκόσμια τραπεζική ανταπόκρισης |

Διαμορφώστε τον τύπο μηνύματος μέσω της παραμέτρου `payment_initiation_message_type`:

```python
create_xml_v9(
    data_file="payments.csv",
    data_file_type="csv",
    xml_file_path="output/pain001.xml",
    payment_initiation_message_type="pain.001.001.09"  # default; also accepts "pain.001.001.03" for legacy SEPA
)
```

Η συμμόρφωση με το CBPR+ κατέστη υποχρεωτική για την τραπεζική ανταπόκρισης του SWIFT τον Νοέμβριο 2023 για τα εισερχόμενα μηνύματα και τον Νοέμβριο 2025 για τα εξερχόμενα. Η δημιουργία αρχείων pain.001 συμμορφούμενων με το CBPR+ απαιτεί να είναι συμπληρωμένο το πεδίο BIC και να είναι παρόν το στοιχείο `ChrgBr`.

## Συχνές ερωτήσεις

**Ποια είναι η διαφορά μεταξύ pain.001 και pain.008;**
Το pain.001 (CustomerCreditTransferInitiation) εκκινεί μια μεταφορά πίστωσης — η τράπεζα του αποστολέα χρεώνει τον λογαριασμό του αποστολέα και πιστώνει τον παραλήπτη. Το pain.008 (CustomerDirectDebitInitiation) εκκινεί μια άμεση χρέωση — η τράπεζα του πιστωτή εισπράττει κεφάλαια από τον οφειλέτη. Η βιβλιοθήκη pain001 παράγει μόνο αρχεία pain.001.

**Ποια έκδοση ISO 20022 στοχεύει το pain001;**
Ο κύριος στόχος είναι το pain.001.001.09, η έκδοση που απαιτείται για το CBPR+ και προβλέπεται από το EPC για νέες υλοποιήσεις SEPA. Η βιβλιοθήκη υποστηρίζει επίσης το pain.001.001.03 (την παλαιά έκδοση SEPA) μέσω της παραμέτρου `payment_initiation_message_type` για οργανισμούς που εξακολουθούν να χρησιμοποιούν παλαιότερες τραπεζικές διεπαφές.

**Μπορεί το pain001 να χειριστεί πολλαπλούς λογαριασμούς οφειλέτη σε ένα μόνο αρχείο;**
Ναι. Πολλαπλά μπλοκ `PmtInf` με διαφορετικά IBAN οφειλέτη μπορούν να παραχθούν ομαδοποιώντας γραμμές CSV με διαφορετικές τιμές λογαριασμού οφειλέτη. Το pain001 δημιουργεί ένα μπλοκ `PmtInf` ανά μοναδικό συνδυασμό (IBAN οφειλέτη, ημερομηνία εκτέλεσης), με όλες τις αντίστοιχες συναλλαγές ένθετες ως θυγατρικά `CdtTrfTxInf`.

**Τι συμβαίνει όταν αποτυγχάνει η επικύρωση XSD;**
Το pain001 εγείρει ένα `pain001.exceptions.ValidationError` με το μήνυμα επικύρωσης του lxml. Το αρχείο XML δεν εγγράφεται στον δίσκο όταν η επικύρωση αποτυγχάνει, επομένως μόνο έγκυρα αρχεία φτάνουν στη διαδρομή εξόδου. Συνήθεις αιτίες αποτυχίας είναι: IBAN σε λανθασμένη μορφή, BIC που δεν έχει 8 ή 11 χαρακτήρες, κωδικός νομίσματος που δεν ανήκει στο ISO 4217, ή απουσία υποχρεωτικών στοιχείων όταν λείπει μια απαιτούμενη στήλη CSV.

## Αναφορές

1. European Payments Council. *SEPA Credit Transfer Scheme Customer-to-Bank Implementation Guidelines (v1.1)*. EPC, 2023. https://www.europeanpaymentscouncil.eu/document-library/implementation-guidelines/sepa-credit-transfer-scheme-customer-bank
2. SWIFT. *CBPR+ Usage Guidelines — Customer Credit Transfer Initiation (pain.001)*. SWIFT Standards, 2023. https://www.swift.com/standards/iso-20022/cbpr-plus-usage-guidelines
3. ISO. *ISO 20022 — Financial services — Universal financial industry message scheme*. ISO.org, 2023. https://www.iso20022.org/
4. Rousseau, S. *pain001 — ISO 20022 payment file generator*. GitHub, 2023. https://github.com/sebastienrousseau/pain001

[00]: https://pain001.com/ "pain001: Automate ISO 20022-Compliant Payment File Creation"
[01]: https://www.iso20022.org/ "ISO 20022: Universal financial industry message scheme"
