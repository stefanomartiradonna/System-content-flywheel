# Convenzione UTM per i link pubblicati su LinkedIn

Regola operativa: **nessun link esce da un post senza UTM.** Un link non taggato è traffico
che arriva sul sito e risulta genericamente "LinkedIn", senza nessun modo di risalire al post.
Non è recuperabile a posteriori: o è taggato quando pubblichi, o quel dato è perso per sempre.

PostHog (project `415565`) cattura gli UTM in automatico, quindi non va toccato niente sul sito.
L'unico cambio è nel link che incolli.

---

## Lo schema

```
https://stefanomartiradonna.com/?utm_source=linkedin&utm_medium=<dove>&utm_campaign=<tema>&utm_content=<slug>
```

| Parametro | Valore | Perché |
|---|---|---|
| `utm_source` | sempre `linkedin` | separa LinkedIn da newsletter, DM, altro |
| `utm_medium` | `post` se il link è nel corpo, `comment` se è nel primo commento | **misura quanto ti costa mettere il link nel primo commento**, che oggi è la tua abitudine di default e non è mai stata verificata |
| `utm_campaign` | il tema: `positioning`, `gtm`, `icp`, `pricing`, `ai`, `product-strategy` | aggrega per argomento senza doverlo dedurre dal testo |
| `utm_content` | slug del post: `<topic>-<AAAA-MM-GG>`, es. `tesi-prodotto-2026-10-07` | è la chiave che aggancia la sessione al singolo post |

### Perché lo slug e non l'ID del post

L'`activity_id` di LinkedIn esiste solo **dopo** che hai pubblicato, mentre il link lo scrivi prima.
Quindi si usa uno slug deciso da te, e il run del lunedì riaggancia slug e `activity_id` confrontando
data e testo. La chiave primaria del dataset resta `activity_id`, in `claude-private-refs/linkedin/metrics.csv`.

### Le destinazioni possibili

Stesso schema, cambia solo il dominio di partenza:

- Sito: `https://stefanomartiradonna.com/?utm_...`
- Newsletter: `https://stefanopm.substack.com/?utm_...`
- Calendly diretto: `https://calendly.com/stefano-martiradonna/new-meeting?utm_...`
- Tool: `https://backend-friend.lovable.app/?utm_...` e `https://gtm-snapshot.lovable.app/?utm_...`

**Attenzione sui due tool Lovable:** se non hanno PostHog installato, chi ci arriva sparisce dal
tracciamento proprio nel momento di massima intenzione. Da verificare prima di usarli come destinazione
in un post che vuoi misurare.

---

## Cosa NON misura

Da dire chiaramente, perché è il limite di questo schema:

- PostHog vede il **click** sulla CTA Calendly, non la **prenotazione**: Calendly è un dominio esterno.
  La prenotazione si recupera dalle mail di conferma Calendly.
- Stessa cosa per l'iscrizione a Substack: si vede il click, non l'iscrizione. Serve l'export iscritti.
- I DM non sono tracciabili in nessun modo automatico. Si registrano a mano in
  `claude-private-refs/linkedin/conversions.md`.
