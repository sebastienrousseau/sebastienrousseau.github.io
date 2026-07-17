---
title: "Audio Analyser: Αγωγός Azure Speech, NLP και μετάφρασης"
tags: "Azure, CherryPy, SpeechToText, NLP, SentimentAnalysis, BatchTranscription, AudioAnalyser, NeuralASR, TextAnalytics, Multilingual, ISO 20022, post-quantum cryptography, AI, open source, DORA, platform engineering, sovereign cloud, cloud native banking"
subtitle: "Αρχιτεκτονική και αγωγός ενός εργαλείου ανάλυσης ομιλίας βασισμένου στο Azure"
description: "Το Audio Analyser χρησιμοποιεί νευρωνικά μοντέλα μετατροπής ομιλίας σε κείμενο των Azure Cognitive Services, NLP του Text Analytics και το CherryPy για τη μετατροπή ηχητικών εγγραφών σε αναζητήσιμες απομαγνητοφωνήσεις με βαθμολογίες συναισθήματος, εξαγωγή λέξεων-κλειδιών και πολύγλωσσες μεταφράσεις."
date: "Jan 29, 2024"
language: "el"
locale: "el_GR"
banner: "https://cloudcdn.pro/stocks/images/modern-corporate-office-with-technological-displays.webp"
banner_alt: "Ένα μινιμαλιστικό, σύγχρονο εταιρικό γραφείο"
keywords: "Azure Cognitive Services, μετατροπή ομιλίας σε κείμενο, νευρωνικό ακουστικό μοντέλο, Azure Text Analytics, επεξεργασία φυσικής γλώσσας, ανάλυση συναισθήματος, CherryPy, API μαζικής απομαγνητοφώνησης, πολύγλωσσο ASR, Azure Translator, απομαγνητοφώνηση ήχου, επεξεργασία ήχου με Python"
---

> **Σύνοψη για Στελέχη / Βασικά Συμπεράσματα**
>
> - **Το API μαζικής απομαγνητοφώνησης του Azure** δέχεται αρχεία ήχου διάρκειας έως 2,5 ωρών (WAV/MP3/OGG/FLAC), τα επεξεργάζεται ασύγχρονα και επιστρέφει έναν πίνακα JSON `recognizedPhrases` με υποψήφια `nBest` ανά φράση, βαθμολογίες εμπιστοσύνης, έξοδο με αντίστροφη κανονικοποίηση κειμένου (ITN) και προαιρετικό διαχωρισμό ομιλητών — χωρίς να απαιτείται σύνδεση ροής (Microsoft Azure, 2024).
> - **Τα νευρωνικά ακουστικά μοντέλα της Microsoft** μείωσαν το ποσοστό σφάλματος λέξεων κατά περίπου 50% σε σχέση με προηγούμενες βασικές γραμμές μοντέλων κρυφών Markov (HMM) στο συνομιλιακό benchmark Switchboard, φτάνοντας ισοτιμία με επαγγελματίες ανθρώπους απομαγνητοφωνητές σε αυτό το σύνολο δεδομένων με WER ~5,1% (Xiong et al., Microsoft Research, ενημέρωση 2016/2021).
> - **Το Azure Text Analytics** (πλέον μέρος του Azure AI Language) επεξεργάζεται το κείμενο της απομαγνητοφώνησης μέσω εξαγωγής φράσεων-κλειδιών, αναγνώρισης ονομαστικών οντοτήτων (NER), ανάλυσης συναισθήματος με εξόρυξη γνωμών και ανίχνευσης γλώσσας — όλα σε μία κλήση `analyze_sentiment` ή `begin_analyze_actions` με χρήση του Python SDK.
> - **Το CherryPy** παρέχει το επίπεδο web: δρομολόγηση URL, χειρισμό μεταφόρτωσης multipart, διαχείριση συνεδριών και απόδοση προτύπων Jinja2 σε μια ελάχιστη διεργασία Python που μπορεί να εκτελείται σε ένα μόνο χαμηλού κόστους VM χωρίς κόστος ενορχήστρωσης.
> - **Το Azure Translator NMT** ανιχνεύει αυτόματα τη γλώσσα-πηγή και μεταφράζει τις απομαγνητοφωνήσεις σε οποιαδήποτε από 135 γλώσσες-στόχους, επιτρέποντας ανάλυση NLP κατάντη τόσο στο πρωτότυπο όσο και στο μεταφρασμένο κείμενο εντός της ίδιας εκτέλεσης του αγωγού.

Το [**Audio Analyser ⧉**][00] είναι μια εφαρμογή ανοιχτού κώδικα σε Python που συνδέει τρεις υπηρεσίες Azure Cognitive Services σε μία ενιαία ροή εργασίας: τη Μαζική Απομαγνητοφώνηση για τη μετατροπή ομιλίας σε κείμενο, το Azure AI Language (Text Analytics) για NLP και τον Azure Translator για πολύγλωσση έξοδο. Η διαδικτυακή διεπαφή εξυπηρετείται από το CherryPy, και τα αποτελέσματα μπορούν να αποθηκευτούν σε JSON, απλό κείμενο ή σε τοπική βάση δεδομένων SQLite.

Αυτό το άρθρο περιγράφει την τεχνική αρχιτεκτονική κάθε σταδίου του αγωγού, τα συμβόλαια των API του Azure και τις σχεδιαστικές επιλογές που έγιναν στο επίπεδο του CherryPy.

## Πώς λειτουργεί το Audio Analyser: Επισκόπηση αρχιτεκτονικής

Ο αγωγός έχει πέντε διακριτά στάδια:

1. **Μεταφόρτωση** — ο χρήστης υποβάλλει ένα αρχείο ήχου μέσω της διαδικτυακής διεπαφής του CherryPy. Το CherryPy αποθηκεύει το αρχείο σε έναν προσωρινό κατάλογο και επιστρέφει ένα ID εργασίας.
2. **Απομαγνητοφώνηση** — το Audio Analyser υποβάλλει το αρχείο στο REST API Μαζικής Απομαγνητοφώνησης του Azure. Επειδή η μαζική απομαγνητοφώνηση είναι ασύγχρονη, η εφαρμογή δημοσκοπεί το endpoint κατάστασης της εργασίας ανά διαστήματα και περιμένει την κατάσταση `Succeeded` πριν προχωρήσει.
3. **NLP** — το ακατέργαστο κείμενο της απομαγνητοφώνησης περνά στο Azure AI Language για εξαγωγή φράσεων-κλειδιών, NER, ανάλυση συναισθήματος και ανίχνευση γλώσσας.
4. **Μετάφραση** (προαιρετικό) — εάν οριστεί μια γλώσσα-στόχος, η απομαγνητοφώνηση αποστέλλεται στον Azure Translator, και η ανάλυση NLP εκτελείται εκ νέου στο μεταφρασμένο κείμενο.
5. **Έξοδος** — τα αποτελέσματα εγγράφονται στην επιλεγμένη μορφή εξόδου (JSON, TXT ή SQLite) και αποδίδονται στη διαδικτυακή διεπαφή του CherryPy.

Οι μόνες εξαρτήσεις εκτέλεσης εκτός της τυπικής βιβλιοθήκης της Python είναι οι `azure-cognitiveservices-speech`, `azure-ai-textanalytics`, `azure-ai-translation-text` και `cherrypy`. Όλα τα διαπιστευτήρια του Azure διαβάζονται από μεταβλητές περιβάλλοντος.

## Azure Cognitive Services: Η μηχανή μαζικής απομαγνητοφώνησης

Το API μαζικής απομαγνητοφώνησης της υπηρεσίας Azure Speech (`/speechtotext/v3.0/transcriptions`) δέχεται μια αναφορά σε ένα αρχείο ήχου στο Azure Blob Storage και ένα σώμα διαμόρφωσης JSON. Το Audio Analyser μεταφορτώνει το τοπικό αρχείο στο Blob Storage χρησιμοποιώντας ένα προϋπογεγραμμένο URL SAS, και στη συνέχεια υποβάλλει την εργασία απομαγνητοφώνησης.

Ένα ελάχιστο φορτίο υποβολής εργασίας:

```json
{
  "contentUrls": ["https://<account>.blob.core.windows.net/<container>/<file>.wav?<sas>"],
  "locale": "en-US",
  "displayName": "audio-analyser-job-001",
  "properties": {
    "diarizationEnabled": true,
    "wordLevelTimestampsEnabled": true,
    "punctuationMode": "DictatedAndAutomatic",
    "profanityFilterMode": "Masked"
  }
}
```

Ο πίνακας `recognizedPhrases` της απόκρισης περιέχει ένα αντικείμενο ανά αναγνωρισμένη εκφορά. Κάθε καταχώρηση περιλαμβάνει:

- `nBest[0].confidence` — δεκαδικός αριθμός μεταξύ 0 και 1
- `nBest[0].lexical` — ακατέργαστες λέξεις όπως εκφωνήθηκαν
- `nBest[0].itn` — μορφή με αντίστροφη κανονικοποίηση κειμένου (αριθμοί, ημερομηνίες, νομίσματα σε αναπτυγμένη μορφή)
- `nBest[0].display` — μορφοποιημένη για ανάγνωση, με στίξη
- `speaker` — ακέραιο ID ομιλητή όταν είναι ενεργοποιημένος ο διαχωρισμός ομιλητών

Η βελτιστοποίηση **Custom Speech** είναι διαθέσιμη για λεξιλόγιο ειδικό ανά τομέα. Η μεταφόρτωση ενός λεξικού προφοράς ή ενός σώματος προσαρμογής (ένα σύνολο προτάσεων κειμένου αντιπροσωπευτικών του τομέα) προσαρμόζει το γλωσσικό μοντέλο και μπορεί να μειώσει ουσιαστικά το WER σε εξειδικευμένο περιεχόμενο, όπως χρηματοοικονομικοί όροι ή ιατρική ορολογία.

## Επεξεργασία φυσικής γλώσσας με το Azure AI Language

Μετά την απομαγνητοφώνηση, το Audio Analyser στέλνει την απομαγνητοφώνηση σε μορφή προβολής στο Azure AI Language μέσω του Python SDK `azure-ai-textanalytics`:

```python
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

client = TextAnalyticsClient(
    endpoint=os.environ["AZURE_LANGUAGE_ENDPOINT"],
    credential=AzureKeyCredential(os.environ["AZURE_LANGUAGE_KEY"])
)

documents = [{"id": "1", "language": detected_lang, "text": transcript}]

sentiment_result = client.analyze_sentiment(documents, show_opinion_mining=True)
for doc in sentiment_result:
    print(f"Sentiment: {doc.sentiment}")
    print(f"Scores: pos={doc.confidence_scores.positive:.2f} "
          f"neg={doc.confidence_scores.negative:.2f} "
          f"neu={doc.confidence_scores.neutral:.2f}")
    for sentence in doc.sentences:
        for opinion in sentence.mined_opinions:
            print(f"  Target: {opinion.target.text}, "
                  f"Assessment: {[a.text for a in opinion.assessments]}")

keyphrases_result = client.extract_key_phrases(documents)
entities_result  = client.recognize_entities(documents)
```

Το `show_opinion_mining=True` ενεργοποιεί το συναίσθημα σε επίπεδο πτυχής: το API επιστρέφει όχι μόνο την πολικότητα σε επίπεδο εγγράφου, αλλά συγκεκριμένα ζεύγη στόχου–αξιολόγησης (π.χ. στόχος="ποιότητα ήχου", αξιολόγηση="κακή"). Αυτό καθιστά την έξοδο χρήσιμη για τον εντοπισμό συγκεκριμένων προβλημάτων στην ανάλυση κλήσεων εξυπηρέτησης πελατών.

Η αναγνώριση ονομαστικών οντοτήτων ταξινομεί τμήματα ως ένα από: `Person`, `Organization`, `Location`, `Event`, `Product`, `DateTime`, `Quantity`, `IP`, `URL`, `Email`, `PersonType`, `Skill`, `Address`, `PhoneNumber`.

## Πολύγλωσση υποστήριξη μέσω του Azure Translator

Ο Azure Translator καλείται μετά την ανίχνευση γλώσσας όταν ο χρήστης ζητά μια γλώσσα-στόχο. Η υπηρεσία υποστηρίζει 135 γλώσσες και διαλέκτους με νευρωνική αυτόματη μετάφραση (NMT). Το Audio Analyser χρησιμοποιεί το REST endpoint `/translate` με `autodetect` ως παράμετρο `from`, ώστε να μην απαιτείται προσδιορισμός γλώσσας-πηγής:

```python
import requests, uuid

url = "https://api.cognitive.microsofttranslator.com/translate"
params = {"api-version": "3.0", "to": target_lang}
headers = {
    "Ocp-Apim-Subscription-Key": os.environ["AZURE_TRANSLATOR_KEY"],
    "Ocp-Apim-Subscription-Region": os.environ["AZURE_TRANSLATOR_REGION"],
    "Content-type": "application/json",
    "X-ClientTraceId": str(uuid.uuid4())
}
body = [{"text": transcript}]
response = requests.post(url, params=params, headers=headers, json=body)
translated_text = response.json()[0]["translations"][0]["text"]
detected_language = response.json()[0]["detectedLanguage"]["language"]
```

Μετά τη μετάφραση, το Audio Analyser εκτελεί προαιρετικά εκ νέου το πέρασμα NLP του Text Analytics στο μεταφρασμένο κείμενο, ώστε οι έξοδοι φράσεων-κλειδιών και συναισθήματος να είναι διαθέσιμες τόσο στη γλώσσα-πηγή όσο και στη γλώσσα-στόχο.

Η επιλογή μορφής εξόδου (JSON, TXT, SQLite) ορίζεται κατά την εκκίνηση. Η έξοδος SQLite αποθηκεύει κάθε συνεδρία ανάλυσης ως μια γραμμή με στήλες για το ID εργασίας, τη χρονοσφραγίδα, τη γλώσσα-πηγή, την απομαγνητοφώνηση, τη μεταφρασμένη απομαγνητοφώνηση, τις βαθμολογίες συναισθήματος και τις φράσεις-κλειδιά ως blob JSON — επιτρέποντας ερωτήματα SQL μεταξύ των συνεδριών.

## Το CherryPy ως επίπεδο web

Το CherryPy αντιστοιχίζει διαδρομές URL σε μεθόδους Python χρησιμοποιώντας ελεγκτές βασισμένους σε κλάσεις. Το Audio Analyser χρησιμοποιεί τρεις διαδρομές:

| Διαδρομή | Μέθοδος | Περιγραφή |
|---|---|---|
| `GET /` | `index()` | Αποδίδει τη φόρμα μεταφόρτωσης |
| `POST /analyse` | `analyse()` | Δέχεται μεταφόρτωση multipart, ενεργοποιεί τον αγωγό, επιστρέφει ID εργασίας |
| `GET /results/<job_id>` | `results()` | Δημοσκοπεί την κατάσταση της εργασίας· αποδίδει τη σελίδα αποτελεσμάτων όταν ολοκληρωθεί |

Η ελάχιστη διαμόρφωση διατηρεί μικρό το αποτύπωμα του διακομιστή:

```python
import cherrypy

cherrypy.config.update({
    "server.socket_host": "0.0.0.0",
    "server.socket_port": 8080,
    "tools.sessions.on": True,
    "tools.sessions.timeout": 60
})
cherrypy.quickstart(AudioAnalyserApp(), "/", conf)
```

Η κατάσταση της συνεδρίας διατηρεί το τρέχον ID εργασίας, την επιλεγμένη μορφή εξόδου και τη γλώσσα-στόχο μετάφρασης. Η ενσωματωμένη αποθήκευση συνεδριών του CherryPy υποστηρίζεται από αρχεία εξ ορισμού, χωρίς να απαιτείται εξωτερικό επίπεδο cache.

## Συχνές ερωτήσεις

**Ποιες μορφές ήχου και μεγέθη αρχείων δέχεται το Audio Analyser;**
Το API μαζικής απομαγνητοφώνησης του Azure υποστηρίζει αρχεία WAV, MP3, OGG και FLAC διάρκειας έως 2,5 ωρών. Τα αρχεία εκτός αυτού του εύρους θα πρέπει να διαχωρίζονται πριν από τη μεταφόρτωση. Τα στερεοφωνικά αρχεία γίνονται δεκτά· η μετατροπή σε μονοφωνικό δεν απαιτείται.

**Πώς λειτουργεί ο διαχωρισμός ομιλητών;**
Ο ορισμός `diarizationEnabled: true` στο αίτημα μαζικής απομαγνητοφώνησης ενεργοποιεί το μοντέλο διαχωρισμού ομιλητών του Azure. Κάθε `recognizedPhrase` στην απόκριση περιλαμβάνει ένα ακέραιο πεδίο `speaker`. Το μοντέλο αναγνωρίζει τους ομιλητές με βάση ακουστικά χαρακτηριστικά και αποδίδει συνεπή ID εντός μιας συνεδρίας, αλλά δεν αναγνωρίζει ποιοι είναι οι ομιλητές χωρίς ένα ξεχωριστό βήμα εγγραφής φωνητικού προφίλ.

**Διατηρούνται τα αρχεία ήχου μετά την απομαγνητοφώνηση;**
Τα αρχεία ήχου μεταφορτώνονται στο Azure Blob Storage με ένα βραχύβιο URL SAS και διαγράφονται από τον προσωρινό τοπικό κατάλογο μετά την ολοκλήρωση της μεταφόρτωσης. Η διατήρηση των blobs στο Azure Blob Storage εξαρτάται από την πολιτική κύκλου ζωής του container· εξ ορισμού, το Audio Analyser δεν ορίζει ρητή πολιτική διαγραφής, οπότε η διαμόρφωση ενός κανόνα με σύντομο TTL (π.χ. διαγραφή blobs παλαιότερων από 1 ημέρα) στην πύλη Azure συνιστάται για αναπτύξεις παραγωγής.

**Μπορεί η ανάλυση NLP να εκτελεστεί χωρίς μετάφραση;**
Ναι. Η μετάφραση είναι ένα προαιρετικό στάδιο του αγωγού που ελέγχεται από τη σημαία CLI `--target-lang` ή το αναπτυσσόμενο μενού γλώσσας-στόχου στη διαδικτυακή διεπαφή. Όταν δεν επιλέγεται καμία γλώσσα-στόχος, ο αγωγός εκτελεί μόνο μετατροπή ομιλίας σε κείμενο και Text Analytics.

## Αναφορές

1. Microsoft. *Batch transcription overview — Azure AI services*. Microsoft Learn, 2024. <https://learn.microsoft.com/en-us/azure/ai-services/speech-service/batch-transcription>
2. Xiong, W. et al. "Achieving Human Parity in Conversational Speech Recognition." *Microsoft Research Technical Report*, 2016; updated 2021. <https://arxiv.org/abs/1610.05256>
3. Microsoft. *What is Azure AI Language?* Microsoft Learn, 2024. <https://learn.microsoft.com/en-us/azure/ai-services/language-service/overview>
4. Microsoft. *Azure AI Translator — Supported languages*. Microsoft Learn, 2024. <https://learn.microsoft.com/en-us/azure/ai-services/translator/language-support>

[00]: https://audioanalyser.co/ "Audio Analyser — Azure-backed speech analytics tool"
