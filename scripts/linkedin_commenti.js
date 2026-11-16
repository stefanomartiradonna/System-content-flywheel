// linkedin_commenti.js - Fase 1 del content-cockpit: legge i commenti di UN post LinkedIn.
//
// Come si usa: aprire la pagina del post (https://www.linkedin.com/feed/update/urn:li:activity:ID/)
// in una scheda IN PRIMO PIANO del Chrome loggato, poi passare questo file intero come `function` a
// `mcp__chrome-devtools-mcp__evaluate_script`, con `filePath` = un .json nella scratchpad.
// In una scheda in background la pagina si carica a meta' e i commenti escono 0 anche quando non lo
// sono (verificato l'11/11/2026): per questo lo script si rifiuta di contare se la scheda non e' visibile.
//
// Legge solo il DOM, come lo vede l'utente: nessuna API interna. Espande "Carica altri commenti" e le
// risposte nascoste prima di contare. Il conteggio include le risposte dell'autore, come fa LinkedIn.
//
// Restituisce JSON: {activity_id, letto, stato, n_commenti, n_tuoi, commenti: [{autore, tuo, eta, testo}]}
async () => {
  const AUTORE = "Stefano Martiradonna";
  const attesa = (ms) => new Promise((r) => setTimeout(r, ms));
  const id = (location.href.match(/activity[:%3A]+(\d{19})/) || [])[1] || null;
  const esito = (stato, extra) => Object.assign(
    { activity_id: id, letto: new Date().toISOString(), stato, n_commenti: null, n_tuoi: null, commenti: [] },
    extra || {});

  // evaluate_script interrompe gli script oltre i 5 secondi: le attese stanno sotto i 4.
  // Se la pagina non e' pronta lo script lo dice, e il post si rilegge con una seconda chiamata.
  if (document.visibilityState !== "visible") return esito("scheda_in_background");
  for (let i = 0; i < 5; i++) {
    if (/Vedi analisi/.test(document.body.innerText)) break;
    await attesa(500);
  }
  if (!/Vedi analisi/.test(document.body.innerText)) return esito("pagina_non_caricata");

  // Espandi commenti e risposte nascoste (max 2 giri). Se ne restano, lo script lo segnala.
  const nascosti = () => [...document.querySelectorAll("button")].filter((b) =>
    /^(Carica altri commenti|Visualizza altri commenti|Carica le risposte precedenti|Visualizza.*rispost[ae])/i
      .test((b.innerText || b.getAttribute("aria-label") || "").trim()));
  for (let giro = 0; giro < 2; giro++) {
    const altri = nascosti();
    if (!altri.length) break;
    altri.forEach((b) => b.click());
    await attesa(700);
  }
  if (nascosti().length) return esito("commenti_ancora_nascosti");

  const RE_LABEL = /per il commento di (.+?)\.?$/;
  const bottoni = [...document.querySelectorAll('button[aria-label*="per il commento di"]')];
  const commenti = bottoni.map((b) => {
    const autore = (b.getAttribute("aria-label").match(RE_LABEL) || [])[1] || "?";
    // Il blocco del commento e' l'antenato piu' alto che contiene un solo bottone "per il commento di".
    let blocco = b;
    while (blocco.parentElement &&
           blocco.parentElement.querySelectorAll('button[aria-label*="per il commento di"]').length === 1) {
      blocco = blocco.parentElement;
    }
    const righe = (blocco.innerText || "").split("\n").map((s) => s.trim()).filter(Boolean);
    const RE_ETA = /^\d+\s*(min|or[ae]|h|giorn[oi]|g|settiman[ae]|sett|mes[ei]|ann[oi])\b/i;
    const RE_FINE = /^(\d+\s+reazion|\d+\s+impression|Mi piace|Rispondi|Reagisci|\d+$)/i;
    const iEta = righe.findIndex((r) => RE_ETA.test(r));
    const corpo = [];
    for (let k = iEta + 1; k < righe.length; k++) {
      if (RE_FINE.test(righe[k])) break;
      if (/^\(modificato\)$/i.test(righe[k])) continue;
      corpo.push(righe[k]);
    }
    return { autore, tuo: autore === AUTORE, eta: iEta >= 0 ? righe[iEta] : "", testo: corpo.join(" ") };
  });

  return esito("ok", {
    n_commenti: commenti.length,
    n_tuoi: commenti.filter((c) => c.tuo).length,
    commenti,
  });
}
