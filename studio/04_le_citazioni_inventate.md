# 4. Le citazioni inventate

## Lo studente e la pagina del manuale

Chi ha fatto un esame orale conosce la scena. Lo studente, un po' in difficoltà, dice con sicurezza: «come spiega il
manuale al capitolo quattro». Il professore annuisce. La frase è plausibile, forse è persino vera. Ma lo studente quel
capitolo non l'ha mai aperto, e il professore se ne accorge solo se va a controllare.

Un modello linguistico fa la stessa cosa, e la fa con una disinvoltura che nessuno studente avrebbe. Scrive una dose,
mette accanto «RCP, sezione 4.2» e il nome di un medicinale vero. Il nome vero fa da copertura: il medico che legge
vede una fonte, e si fida.

Per uno strumento che prometteva di riportare i documenti ufficiali, era il pericolo peggiore. Questo capitolo
racconta come lo abbiamo scoperto, come abbiamo sbagliato la prima diagnosi, e come alla fine lo abbiamo fermato: non
con una frase nelle istruzioni del modello, ma con un controllo nel codice.

## Cinquanta volte la stessa domanda

A luglio abbiamo costruito un validatore delle citazioni. L'idea era semplice: dopo che il modello ha scritto la
risposta, il codice legge ogni citazione e la confronta con le fonti che il modello aveva davvero ricevuto. I controlli
erano due. Il primo guardava il nome: il medicinale citato era fra quelli forniti? Se no, era una citazione
fabbricata. Il secondo guardava la sezione: il medicinale era fra le fonti, ma quella sezione del suo foglio ufficiale
gli era stata data? Se no, il contenuto non era tracciato, anche quando era clinicamente giusto.

Sulla batteria di prove il validatore non trovava nessuna citazione fabbricata: zero su oltre quattrocento. Poteva
sembrare una buona notizia. Ma il numero era piccolo per un evento raro: con le poche ripetizioni che avevamo, la
probabilità di vederlo era più o meno una su cinque.

Allora abbiamo fatto una cosa diversa: una sola domanda, lo schema di cura per eradicare l'Helicobacter pylori,
ripetuta cinquanta volte. In quattro risposte il modello nominava un medicinale a base di esomeprazolo. Due volte lo
faceva onestamente, scrivendo che le sezioni fornite non contenevano informazioni su quel farmaco. Le altre due volte
gli attaccava posologia, controindicazioni e avvertenze, con la sezione accanto, da un foglio che non aveva mai
ricevuto. Il validatore le ha prese entrambe, senza un falso allarme, prima che arrivassero in produzione.

È la prima lezione del capitolo, e vale per qualunque sistema con un modello dentro: gli errori rari non si vedono
guardando tante domande una volta. Si vedono guardando la stessa domanda tante volte.

## La cura che peggiorava il male

La diagnosi sembrava ovvia. Nelle istruzioni del modello c'era un blocco di dati anagrafici che nominava più medicinali
di quelli di cui il modello riceveva il testo: nomi senza contenuto. Il modello vedeva un nome, e qualche volta
riempiva il vuoto.

Abbiamo misurato quanto fosse frequente, ed era molto più frequente del previsto: quasi una domanda su tre aveva
almeno un nome senza testo. Abbiamo scritto una correzione ragionevole, e prima di metterla in produzione l'abbiamo
misurata come avevamo misurato il problema: centocinquanta esecuzioni della stessa domanda, divise in tre gruppi,
prima, dopo, e un gruppo di controllo che cambiava una sola cosa.

La correzione peggiorava il male. Con lei, la posologia inventata passava da zero a undici risposte su cinquanta. E il
gruppo di controllo diceva perché: la colpa non era del nome senza testo, ma di quanti pezzi di testo per farmaco il
modello riceveva. Con meno testo a cui appoggiarsi, il modello inventava di più, anche sui farmaci che il loro testo
l'avevano. La premessa da cui eravamo partiti era falsa.

Nulla di tutto questo è arrivato al medico: la correzione non è mai entrata nel codice di produzione. Ma rileggendo
quei giorni capisco quanto sia stato importante misurarla. Una correzione che sembra ovvia e non si misura è un
problema nuovo travestito da soluzione.

## Mai togliere in silenzio

Ad agosto abbiamo deciso il primo controllo che non si limitava a registrare, ma agiva. Riguardava una forma più sottile
dello stesso errore: il modello prendeva il contenuto del foglio ufficiale di un medicinale e lo attribuiva a un altro,
con lo stesso principio attivo. Il dato poteva essere vero, ma era scritto sotto il nome sbagliato.

Per accorgercene serviva un'impronta della risposta: per ogni blocco, da quali documenti venivano davvero le sue frasi.
Quando un blocco intitolato a un medicinale era fatto, per almeno un terzo, di frasi di un altro, il codice lo
sostituiva. E
qui abbiamo fissato una regola che ha guidato tutto il resto: mai togliere in silenzio. Al posto del blocco, un testo
costante, scritto dal codice e mai dal modello, che diceva al medico che cosa mancava e perché, e lo rimandava al
foglio ufficiale.

Il ragionamento era un'asimmetria. Se il controllo sbagliava, il costo era un'omissione dichiarata: il medico leggeva
che quel contenuto non era riportato, e andava a vedere. Se il controllo non c'era, il costo era un'attribuzione falsa
servita al medico.

## Una citazione senza fonte non arriva al medico

Il validatore dei nomi, invece, era rimasto un osservatore. Lo avevamo voluto così: prima di lasciargli togliere
qualcosa, volevamo sapere quanto spesso sbagliava, e avevamo scritto in anticipo a quali condizioni sarebbe passato
all'azione.

Il giorno è arrivato a ottobre. Dopo un aggiornamento, la batteria ha mostrato una risposta sulla terapia del diabete
che citava tre medicinali, con la sezione delle avvertenze, che non erano fra le fonti fornite. Il validatore le ha
segnalate e le ha lasciate passare, come doveva.

Prima di decidere abbiamo contato. Da luglio, su quasi milleottocento risposte controllate, gli allarmi sul nome erano
tre: due volte quel caso, una volta un identificativo di un articolo scientifico trascritto con una cifra in più. Sulle
poche risposte date a utenti veri, nessuno. Agire costava quasi nulla.

Così la regola è cambiata: una riga della risposta che cita un medicinale assente dalle fonti non si serve. Al suo
posto va un testo costante del codice, che nomina il medicinale e la sezione e rimanda all'RCP ufficiale. Il resto
della risposta resta identico, carattere per carattere.

Durante la discussione io avevo proposto una soluzione più semplice: al posto della riga, un separatore. L'ho ritirata,
e a ragione. Era una soppressione silenziosa, proprio quella che ci eravamo vietati ad agosto. E aveva
anche un difetto tecnico divertente: nella sintassi con cui scrivevamo le risposte, tre trattini possono diventare una
riga orizzontale, o trasformare in titolo la frase sopra.

C'era infine un'ultima regola, per le guardie che tolgono qualcosa: se qualcosa va storto nel controllo, la risposta
passa com'era. La guardia può togliere una riga con un'ancora falsa; non può mai rompere una risposta.

## Le reti nel posto giusto

Da tutto questo è venuta la lezione più generale del capitolo, e forse dell'intero progetto.

Le prime protezioni contro gli errori del modello le avevamo scritte, come si fa di solito, nelle sue istruzioni: per
esempio di non citare ciò che non gli era stato fornito, o di dichiarare quando una sezione era parziale. Funzionano,
ma non sempre. Una
regola nelle istruzioni riduce la probabilità di un errore; non la porta a zero.

In agosto, prima di aprire le schede pubbliche, abbiamo fatto l'inventario di tutte le protezioni del sistema. Erano
centinaia, sparse in decine di file, e solo una parte erano istruzioni al modello. Ma la sorpresa è stata un'altra.
Anche molte protezioni scritte nel codice vivevano nel percorso della consultazione, dove le schede pubbliche non
passavano. L'abbiamo scritta così: indipendente dal prompt vuol dire indipendente dall'obbedienza del modello, non
indipendente dal percorso.

E l'inventario lo abbiamo fatto partendo dalla parte giusta: non dalle centinaia di righe di codice, ma dalle dieci
cose che una scheda pubblica afferma al lettore. Per ognuna, quali protezioni la reggono, e se quelle protezioni sono
davvero sul percorso della scheda.

In ottobre la regola è diventata una frase che rifarei identica: il canale è il codice, non il prompt; una rete che
vive nel prompt non arriva ai percorsi che non ne passano. Il capitolo 5 racconta il caso più chiaro, quello del
pavimento di sicurezza. E a novembre ne abbiamo aggiunta un'altra, che vale come avvertenza per chiunque: una regola di
prompt non è una tutela finché non la si è vista fallire.

## La promessa di una citazione

Una citazione è una promessa. Dice al medico: non devi fidarti di me, vai a controllare, è lì. Un modello linguistico
non sa mantenere questa promessa da solo, per quanto bene glielo si chieda. Il codice sì, se gli si insegna a
controllare, e se il testo che compare al posto di un errore lo scrive il codice e non il modello.

È una delle cose di cui vado più fiero, di questi otto mesi. Non perché IP non sbagliasse mai, ma perché, da ottobre,
quando il modello citava un medicinale che non aveva ricevuto, quella riga non arrivava al medico, e il medico leggeva
perché.

## Per chi costruisce

- **Controllate le citazioni su due livelli.** Il nome (il documento citato è fra quelli forniti?) e la sezione (quella
  parte del documento è stata fornita?). Il primo scopre le invenzioni; il secondo, i contenuti presi dalla memoria
  del modello.
- **Ripetete la stessa domanda molte volte.** Gli errori rari non compaiono in una batteria vista una volta sola.
- **Misurate la correzione come il problema, con un gruppo di controllo.** La nostra correzione più ragionevole
  peggiorava le cose, e solo il controllo ha detto perché.
- **Prima registrate, poi agite**, con le condizioni del passaggio scritte in anticipo. Quando agite, contate prima
  quanto costa.
- **Mai togliere in silenzio.** Al posto di ciò che togliete va un testo costante che dice che cosa manca e dove
  trovarlo.
- **Il testo che sostituisce un errore lo scrive il codice, mai il modello.**
- **Le guardie che tolgono devono fallire aperte.** Se il controllo si rompe, la risposta passa com'era.
- **Fate l'inventario delle protezioni partendo da ciò che affermate al lettore**, e per ciascuna chiedetevi se è sul
  percorso che quel lettore attraversa.
- **Una regola nelle istruzioni del modello non è una tutela finché non l'avete vista fallire.**

---

### Riquadro — Il validatore delle citazioni, per rifarlo

*Per il lettore tecnico: i controlli, i testi costanti e le misure. Vale per qualunque sistema che fa citare a un
modello documenti forniti.*

**I tre controlli dopo la generazione**

| controllo | che cosa confronta | che cosa fa | deciso |
|---|---|---|---|
| nome | il medicinale citato con l'insieme delle fonti fornite | prima registra; poi la riga non si serve e al suo posto va un testo costante (in produzione l'8/10/2026, con la batteria: fabbricazioni sul nome 0) | 19/7/2026; azione il 6/10/2026 |
| sezione | la sezione citata con le sezioni fornite per quel medicinale | registra, con la causa (sezione portata solo dal pavimento di sicurezza o recuperata) | 19/7/2026 |
| attribuzione | l'impronta di ogni blocco: da quali documenti vengono le sue frasi | se un blocco intitolato a un medicinale è fatto per almeno il 30 % di frasi di un altro, il blocco si sostituisce con un testo costante | 1/8/2026 |

**I testi costanti** (scritti dal codice; NOME e sezione sono quelli della citazione)

- Nome: «⚠ Questa riga non è riportata: citava NOME (§4.4), che non è fra le fonti fornite per questa risposta.
  Consultare l'RCP ufficiale del medicinale.»
- Attribuzione: «⚠ Il contenuto generato per NOME (§X.Y) non è riportato: non è risultato riconducibile al Riassunto
  delle Caratteristiche del Prodotto di questo medicinale. Consultare l'RCP ufficiale dal collegamento nelle fonti.»

**Le regole di comportamento**

- unità minima: la riga (nome) o il blocco (attribuzione); il resto della risposta resta identico byte per byte;
- prefisso markdown conservato: rientro, punto elenco, numero, riga di tabella con lo stesso numero di celle;
- telemetria: l'esito misurato resta quello che il modello ha prodotto, e la voce sostituita porta in più
  `suppressed: true`;
- fail-open: qualunque eccezione lascia risposta e telemetria invariate.

**Le misure**

| che cosa | valore | quando |
|---|---|---|
| citazioni fabbricate sulla batteria | 0 su 425, con circa il 22 % di probabilità di vedere l'evento | luglio 2026 |
| una domanda ripetuta 50 volte | il medicinale nominato in 4 risposte: 2 oneste, 2 con citazioni fabbricate; 2 catture su 2, 0 falsi allarmi | 19/7/2026 |
| domande con almeno un nome senza testo | circa una su tre (20 su 66) | 20/7/2026 |
| la correzione misurata: posologia inventata su 50 esecuzioni | 0 prima, 1 nel controllo, 11 dopo | 22/7/2026 |
| attribuzione incrociata osservata | 12 documenti su 424 (2,8 %), sempre con più medicinali dello stesso principio attivo | 27/7–1/8/2026 |
| inventario delle protezioni | 447 in 39 file: 53 istruzioni al modello, 56 testi composti dal codice, 36 miste, 302 logica di codice | 6–7/8/2026 |
| allarmi sul nome dal 19/7 | 3 su 1.778 risposte validate; nessuno sulle 17 risposte agli utenti | 6/10/2026 |

---

*Scritto a quattro mani con Claude. Le scelte, e la responsabilità di quello che c'è scritto, sono mie.*
