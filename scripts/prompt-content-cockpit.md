Esegui la skill content-cockpit. E' il run settimanale del lunedi.

DIRECTORY DI LAVORO: {{FLYWHEEL}}
Il repo privato con i dati: {{PRIVATO}}

Prima di qualsiasi altra cosa verifica di essere nella directory giusta e che sia davvero il repo
giusto: devono esistere CLAUDE.md, knowledge/INDEX.md e scripts/prompt-content-cockpit.md. Se non ci sei, spostati. Se quel
percorso non esiste o quei file mancano (altro computer, clone incompleto), FERMATI e chiedimi dove
sta il repo: non indovinare e non lavorare in una cartella diversa, perche il git pull e tutti i
percorsi del workflow sono relativi a quella.

POI: carica la skill content-cockpit e confermami in una riga che l'hai letta, citando il
titolo della Fase 9. Se non riesci a caricarla, FERMATI e dimmelo invece di improvvisare: il workflow
vive li dentro, e senza quel file le fasi elencate qui sotto non esistono da nessuna parte.

Le 11 fasi, solo come indice per sapere cosa aspettarsi. Le istruzioni vere stanno nella skill e
vincono su questo elenco:

  Fase 0  Contesto: git pull, legge foundation/, hypotheses, craft, voce-analisi, temi.csv,
          cosa-funziona.md, scelte.csv e le liste degli ultimi due report (per non riproporre
          gli stessi angoli)
  Fase 1  Aggiorna il dataset: snapshot LinkedIn da Chrome, poi parse_snapshot.py che unisce i
          post nuovi allo storico (non lo sovrascrive), tagga i post nuovi in temi.csv, aggiorna
          scelte.csv e lancia cosa_funziona.py che ricalcola cosa funziona su tutto lo storico
  Fase 2  KPI dei post sulla finestra matura, migliore della settimana, trend, anti-rumore
  Fase 3  PostHog: visite al sito e click sulle CTA (attenzione al project, punto 1 sotto)
  Fase 4  Conversioni manuali: legge conversions.md (i DM, che nessun sistema vede)
  Fase 5  Autori della watchlist, OGNI settimana, sulla finestra dall'ultimo report a oggi, piu'
          i temi core sul web
  Fase 6  Temi della settimana da quattro fonti:
          (a) la mia settimana: commit, file nuovi, mail, calendario e le CALL CON I CLIENTI
              lette da Granola (domande che tornano, parole loro, sintomo prima della diagnosi)
              -> anonimizzazione obbligatoria all'ingresso: solo ruolo, settore, scala
          (b) il mercato: gli autori della watchlist e le conversazioni sui temi core
          (c) l'archivio: post sopra la mediana di 6+ mesi fa da aggiornare o fondere
          (d) le mosse delle aziende tech negli ultimi 7-10 giorni, cercate sul web: la notizia
              e' il pretesto per spiegare un mio pillar su un caso famoso, numeri verificati
  Fase 7  Due liste: 5 notizie tech e fino a 5 angoli dagli autori, registrate in scelte.csv
          -> QUI TI FERMI E ASPETTI
  Fase 8  Scrive solo quello che ho scelto, con brief immagine e link UTM
  Fase 9  Auto-miglioramento: impara dalle mie correzioni, dalle previsioni verificate e da quali
          voci delle liste scelgo
  Fase 10 Output: report su GOOGLE DOC (cartella Content Cockpit su Drive), copia .md nel repo
          privato in linkedin/cockpit/, poi committa

Fermati alla Fase 7 e aspetta. Proponi le due liste (5 notizie tech, fino a 5 angoli dagli autori) e NON
scrivere i post finche non ti dico cosa sviluppare. Scrivere pezzi che poi non pubblico butta via il
lavoro e mi toglie il gate editoriale.

I cinque punti dove si sbaglia piu facilmente:

1. PostHog: il project di default del connector puo essere il sito di un CLIENTE. Il mio e
   413969, organizzazione "Mio Sito". Fai switch-organization e switch-project, poi verifica con una
   query su properties.$host che il dominio sia stefanomartiradonna.com PRIMA di riportare qualsiasi
   numero. Se non lo e, fermati e dimmelo.

2. Misura la finestra MATURA (post pubblicati tra 14 e 8 giorni fa), non quella fresca. Le impressioni
   crescono per circa una settimana: misurare i post di ieri premia chi ha pubblicato lunedi scorso
   per un artefatto di misurazione, non per merito.

3. Controllo anti-rumore obbligatorio: per ogni confronto tra gruppi, somma reazioni + commenti del
   gruppo. Sotto 30, dichiara la differenza non leggibile a meno che non superi il 50%. Scrivilo nel
   report. La mediana e 275 impressioni: la maggior parte delle oscillazioni e rumore.

4. Precedenza tra le fonti: la skill linkedin-viral-post-writer e l'autorita sulla voce (e mia, la uso
   anche fuori da questa routine). voce-analisi.md e evidenza su cosa faccio di fatto, informa ma non
   comanda. Le regole generiche di copywriting perdono sempre. Se la skill e i dati divergono, NON
   decidere: mettilo nel report e lascia che scelga io.

5. Se Chrome non risponde o un connector e giu, dichiaralo in cima al report e lavora sui dati
   esistenti segnando cosa e fermo alla settimana scorsa. Non inventare numeri e non fingere che il
   dato sia fresco.

Tre regole su cosa resta privato:

- Nei repo pubblici (System-content-flywheel e claude-brain) non entrano nomi di clienti, di persone
  o loro identificativi, nemmeno nei messaggi di commit.
- Bozze, report, numeri dei post e frasi raccolte dalle call vanno nel repo privato.
- A fine run committa e pusha il repo privato: e' la copia che mi permette di ripartire da un
  altro computer. Nei repo pubblici pusha solo dopo aver controllato che non escano riferimenti privati.

Non pubblicare NULLA: ne post, ne commenti, ne modifiche al sito. L'output sono bozze che edito io.

Prima della Fase 1 verifica che Chrome sia aperto e loggato su LinkedIn; se non lo e, avvisami e
chiedi come procedere.
