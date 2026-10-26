# Hypotheses — Ipotesi Attive

Questo file traccia cosa stai testando e le evidenze raccolte.

Regole:
- Un'ipotesi confermata 3+ volte → diventa regola in `platforms/[platform]/rules.md`
- Un'ipotesi smentita 2+ volte → spostala in `hypotheses/archived.md` con nota "smentita"
- Nuova ipotesi? Aggiungila qui con la data e il contesto

---

## Formato entry

```
### H[numero] — [Titolo ipotesi]
**Piattaforma**: LinkedIn / Substack / Entrambe
**Formulata**: [data]
**Ipotesi**: [descrizione in 1-2 frasi]
**Evidenze pro**: 
**Evidenze contro**: 
**Status**: in test / confermata / smentita
```

---

## Ipotesi attive

### H01 — Il reframe diagnostico ("Non hai problema X, hai problema Y") performa meglio di hook informativi sullo stesso tema
**Piattaforma**: LinkedIn
**Formulata**: aprile 2026
**Ipotesi**: Un hook che ribalta la diagnosi attesa del lettore genera più engagement rispetto a un hook che introduce direttamente l'insight o la lista, a parità di tema.
**Evidenze pro**:
- Wester: "You think your content problem is creativity. It's actually plumbing." → 164 reactions
- Wester: "It wasn't a copywriting problem. It was a positioning problem." → 185 reactions
- Estner: "Most early-stage startups don't have a GTM execution problem. They have a positioning problem." — pattern più usato tra i suoi migliori post
- Herubel: "Marketing 'strategy' and 'tactics' are different" → 1319 reactions
- Wester (28/09/2026): pubblica i numeri del suo assessment — 9 founder su 12 gli chiedono pipeline, 11 su 12 non hanno un ICP che il team usi. "They point at too many people, then call it a pipeline problem." → il reframe non è nell'hook, è nel rapporto tra due numeri
- Kaminski (22/09/2026): "Whenever I hear a founder say 'Companies SHOULD be doing X', I'm 99% sure they have a marketing problem" → 96 reactions, 32 commenti
**Evidenza dal campo (engagement, NON performance LinkedIn)**:
- energy-mgmt-b2b-startup-01: il founder formula il bisogno come "vendere di più / meno dipendente da me"; la diagnosi reale che ho portato è a monte (coerenza business model ↔ GTM + positioning). Conferma che il reframe è *vero* in un contesto di vendita reale → materiale concreto per testarlo come hook sulla mia audience.
**Evidenze contro**: 
**Status**: ipotesi forte — da testare sulla mia audience italiana. Ora ho un caso cliente mio da cui costruire il post (non più solo quote di Estner/Wester).
**Nota 2026-10-05 (perché NON è ancora una regola)**: le evidenze pro sono 6 e nessuna contro, quindi la soglia numerica delle 3 conferme è superata da tempo. Non promuovo perché **tutte e 6 vengono da audience altrui** — anglofone, follower alti, B2B US/NL/DE. Una regola in `platforms/linkedin/rules.md` mi direbbe cosa fare di default sui MIEI post, e la promuoverei su zero dati miei. La soglia che manca non è quantitativa: servono 2-3 miei post a parità di tema, uno con hook reframe e uno con hook informativo, e il confronto. Finché quel confronto non esiste, questa resta un'ipotesi forte e non una regola. **Blocco specifico: nessun mio post pubblicato con questo pattern misurato in `../posts/published.md`.**
**Nota 2026-07 (concept Accumulo)**: il bersaglio del reframe sale di livello — la misconception madre del nuovo buyer è "è un problema di copy: basta spiegare meglio le features". Il pattern resta identico; il ribaltamento ora punta a "hai una decisione di prodotto mai presa" (vedi `../foundation/pov.md`, B1).
**Nota 2026-10-12 (primo tentativo, risultato inutilizzabile)**: pubblicato un post con questo pattern ("non è un problema di sales/GTM, è perché non hai una Tesi di Prodotto" — vedi `../posts/published.md`, entry 2026-10). Reach crollato a 19 impressions, 15-30x sotto il baseline degli altri post con carosello. Il crollo è troppo estremo per essere spiegato da debolezza del hook (probabile causa: visibilità del post, zero engagement nella prima ora, o rendering del PDF — tutto da verificare da Stefano). **Il blocco descritto sopra resta aperto**: questo non conta come test di H01, perché il hook non è mai arrivato a un'audience ampia. Serve un retry con distribuzione sana prima di poter leggere qualcosa sul pattern stesso.
**Nota 2026-10-19 (il retry c'è stato, ma non testa H01)**: il post originale è stato eliminato e ripubblicato il 12/10 con lo stesso carosello e il corpo quasi identico. La ripubblicazione ha avuto una reach nella norma dei caroselli: il crollo era di distribuzione, non di contenuto. Ma nel riscriverlo Stefano ha tolto il reframe dalle prime righe: il nuovo hook parte dall'esperienza in prima persona ("una delle prime cose che faccio da fractional è ascoltare le call di vendita") e la causa arriva dopo i sintomi, con una domanda-ponte. Quindi neanche la ripubblicazione è un test di H01. Il blocco resta aperto: serve un post B2B core con il reframe nella prima riga. Da segnare anche come primo caso di correzione di Stefano che va nella direzione opposta a T01: se si ripete, è una divergenza da far decidere a lui. Numeri nel report privato del cockpit del 2026-10-19.
**Nota 2026-10-26 (due candidati al test, ancora freschi)**: il 19/10 e il 20/10 sono usciti due post B2B core con il reframe nella prima riga ("Il tuo sales non perde il deal. Il deal si chiude prima che ti chiamino." e "Il tuo prodotto funziona. Il tuo business no"). Sono i primi test veri di H01 sulla mia audience. Si leggono a maturità nel run del 2026-11-02. Attenzione: i due post differiscono anche in altro (il primo riassume una ricerca altrui ed è solo testo, il secondo regge su un conto proprio e ha un'immagine), quindi da soli non isolano il reframe. Segnale di voce: nel post del 20/10 Stefano ha scelto lui l'hook reframe al posto di quello proposto dalla bozza, cioè la direzione opposta alla correzione del 12/10. Uno a uno: la divergenza segnalata il 19/10 non si è ripetuta.

---

### H02 — La matematica semplice come proof nell'hook aumenta le reactions sui post senza lista
**Piattaforma**: LinkedIn
**Formulata**: aprile 2026
**Ipotesi**: Inserire un calcolo semplice (es. "10% di un mercato da 100M = 10M. 1% di un mercato da 1B = 10M. Stessa revenue, difficoltà completamente diversa.") in un post narrativo breve produce più reactions di un post equivalente senza dati numerici.
**Evidenze pro**:
- Estner: "If you're selling to everyone, you're selling to noone. / The math is simple: 10% of a €100M niche = €10M" → 128 reactions (suo top post non-giveaway)
- Wester: "If your ICP doesn't tell you your ACV, you're cooked. / A €5K client justifies €1K CAC. A €150K client justifies €50K. Those aren't the same motion." → 125 reactions
- Wester (28/09/2026): "12 founders took it. 11 had no sharp ICP. 0 had consistent proof. 9 asked me for pipeline." → quattro numeri secchi, nessuna lista, il proof è il rapporto
- Voje + Poyar (24/09/2026): anteprima survey con spaccato per fascia di ARR, il 73% come numero di apertura → 204 reactions, 145 commenti (il suo post con più commenti della finestra)
**Evidenze contro**: 
**Status**: 4 evidenze concordi, nessuna contro.
**Nota 2026-10-05 (perché NON è ancora una regola)**: vale lo stesso blocco di H01 — le 4 evidenze sono su audience altrui, zero su quella italiana. In più qui c'è una variabile che le evidenze non isolano: Wester e Voje mettono i numeri in un contesto dove sono *loro dati originali* (assessment proprio, survey propria). Non è dimostrato che un numero preso in prestito da un autore funzioni come proof allo stesso modo. Da testare separando i due casi: hook con un mio numero contro hook con un numero citato.
**Nota 2026-10-26 (prima coppia sulla mia audience)**: nella stessa settimana sono usciti un post che regge su un conto costruito da me (20/10: quanti contratti servono per pagare un sales a parità di ACV, tecnica T04) e due che riassumono ricerche altrui (19/10 Digital Applied, 23/10 Forrester). È la prima coppia utile per separare "numero mio" da "numero citato". Dati ancora freschi: si leggono a maturità nel run del 2026-11-02, e il cockpit del 2026-10-26 ne fa l'esperimento della settimana. Numeri nel report privato.

---

### H03 — Il dialogo con reazione emotiva esplicita performa meglio del dialogo neutro
**Piattaforma**: LinkedIn
**Formulata**: aprile 2026
**Ipotesi**: Un hook dialogo che include la reazione emotiva del consulente (shock, ironia, sorpresa) genera più engagement di un dialogo neutro Founder/Me a parità di tema.
**Evidenze pro**:
- Wester: "Founder: 'We serve three industries. ACV ranges from 5K to 50K.' At 2M ARR??!! Hold on, that's 9 different GTM motions." → 100 reactions — il dialogo con "??!!" è più alto
- Herubel: dialogo neutro "Founder: '...' Me: '...'" → 348-1626 reactions (ampio range — la reazione non è l'unica variabile)
**Evidenze contro**: 
**Status**: ipotesi preliminare — dati insufficienti, da testare

---

### H04 — I post con storia narrativa personale (confessione + trasformazione) performano meglio della media nei periodi di bassa frequenza editoriale
**Piattaforma**: LinkedIn
**Formulata**: aprile 2026
**Ipotesi**: Quando pubblico meno frequentemente, un post narrativo personale (es. "ho sbagliato X per Y mesi, poi ho capito...") genera più reactions e commenti rispetto a un post di framework o lista sullo stesso tema.
**Evidenze pro**:
- Wester: "My content sucked for two years straight." → 110 reactions, 56 commenti
- Herubel: "I've been a marketer for 9 years. This is the most surprising question I've been asked..." → 1646 reactions, 225 commenti (post più breve, 99 parole — massimo engagement)
**Evidenze contro**: 
**Status**: ipotesi — da testare al primo tentativo su mia audience

---

### H05 — L'apertura ironica (affermazione palesemente falsa + "hear me out") cattura attenzione fuori dal segmento target, generando reach ma commenti di bassa qualità
**Piattaforma**: LinkedIn
**Formulata**: aprile 2026
**Ipotesi**: Un hook ironico (es. zodiac, paradosso assurdo) genera alto volume di commenti da utenti fuori dall'ICP, mentre un hook diretto al problema dell'ICP genera meno commenti ma di qualità più alta (follower rilevanti, potenziali clienti).
**Evidenze pro**:
- Wester: zodiac post → 63 reactions, 92 commenti (alto ratio commenti/reactions = molto engagement curioso, probabilmente non ICP)
- Maja Voje: metafora paradossale → 97 commenti (simile pattern)
**Evidenze contro**: 
**Status**: ipotesi preliminare — usare l'ironia con consapevolezza, non come formula sistematica

---

### H06 — La chiusura con domanda aperta (senza CTA) genera più commenti di una chiusura con CTA diretta su LinkedIn
**Piattaforma**: LinkedIn
**Formulata**: aprile 2026
**Ipotesi**: Terminare un post con "What's your take?" o una domanda aperta sul tema genera più commenti rispetto a una chiusura con link, offerta, o CTA diretta verso un servizio.
**Evidenze pro**:
- Herubel: quasi tutti i suoi post finiscono con domanda aperta → engagement medio 79-115 commenti per post
- Maja Voje: stessa pattern + chiusura domanda → engagement simile
- Estner: i post con CTA ("comment GTM" per ricevere) hanno molti commenti ma engagement artificiale
**Evidenze contro**: 
- Dato mio (cockpit 2026-10-12, 77 post maturi, escluso l'outlier Como/Disney): i post che chiudono con una domanda (n=15) fanno una mediana di 5,70 commenti ogni 1000 impressioni, tutti gli altri (n=62) 5,48. Differenza del 4%: nessun effetto visibile sulla mia audience. Limiti: confronto osservazionale tra post su temi diversi, non un test a parità di tema; etichette di chiusura assegnate da un solo lettore; il gruppo "altri" mescola rimandi, affermazioni e CTA di contatto, quindi non isola il confronto domanda contro CTA diretta che l'ipotesi formula.
**Status**: ipotesi con evidenza indiziaria forte — da testare sistematicamente nei prossimi 10 post

---

### H07 — I contenuti agganciati a trigger di evento positivo portano lead più qualificati dei contenuti costruiti sul dolore
**Piattaforma**: LinkedIn (con effetto a valle su inbound)
**Formulata**: luglio 2026 (dal doc POV & Content Strategy — asserita da insight strategico, da validare con dati)
**Ipotesi**: Un contenuto agganciato a un trigger di evento positivo (round appena chiuso, lancio nuovo prodotto, nuovo CMO/primo marketing hire, espansione di segmento/mercato) genera meno reach di un contenuto costruito sul dolore, ma porta lead inbound più lucidi, con budget e più pronti al lavoro di radice — quindi con conversione migliore sull'offerta.
**Evidenze pro**:
**Evidenze contro**:
**Status**: in test — richiede tracking dei lead inbound per tipo di trigger del contenuto d'origine (colonna "Lead inbound" in `../posts/published.md`)

---

## Come formulare una buona ipotesi

Non "i post corti funzionano meglio" — troppo vago.
Sì: "I post con hook domanda + lista numerata ottengono più salvataggi dei post narrativi sullo stesso tema, nel mio pubblico early-stage B2B"

Specifica: piattaforma, tipo di contenuto, metrica, pubblico.
