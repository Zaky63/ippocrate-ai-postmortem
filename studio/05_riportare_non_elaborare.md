# 5. Riportare, non elaborare

## Lo specchio

Uno specchio è uno strumento onesto. Mostra quello che c'è, così com'è, e non aggiunge niente. Non ti dice che hai
l'aria stanca, non ti consiglia un'altra camicia. Se vuoi un parere, devi chiederlo a qualcun altro.

Per gran parte della sua vita IP ha cercato di essere uno specchio: lo specchio dei documenti ufficiali sui farmaci. Questo capitolo
racconta come lo abbiamo costruito, pezzo per pezzo, e perché. Non è stata una scelta di comodo. È stata la scelta che
ci teneva dalla parte giusta di un confine, quello fra un'opera di consultazione e un dispositivo medico, che passa
per una sola cosa: prendere i dati di un paziente e concludere.

## Il bivio di fine maggio

A fine maggio, al terzo mese, stavamo insegnando al sistema a capire le domande dei medici. E lì è venuta fuori la
domanda di fondo: che cosa può produrre, IP? Un confronto come «questo farmaco è meglio di quello», o una dose
calcolata sul peso del paziente, non sono dati riportati: sono elaborazioni.

Abbiamo scritto le due strade, una accanto all'altra. La prima era IP come consulente: sintetizza raccomandazioni,
esprime giudizi, calcola le dosi. Accanto avevamo annotato, con onestà, «massima utilità percepita», e subito dopo il
rischio: un'inferenza clinica non tracciabile, un calcolo che può sbagliare, un giudizio che non poggia su una fonte.
La seconda era IP come specchio tracciato delle fonti ufficiali: riporta il dato così come lo scrivono, senza
calcolarlo e senza rielaborarlo.

Abbiamo scelto lo specchio. La ragione più forte l'abbiamo scritta in una riga che rileggo ancora volentieri: un
disclaimer apposto su un numero allucinato non protegge, perché il medico si fida della cifra. La sicurezza non stava
nell'avvertenza in fondo alla pagina, ma nella fonte cliccabile accanto a ogni dato.

Da quel giorno le regole sono state concrete. Se il foglio ufficiale dice «40 mg/kg al giorno», IP riporta «40 mg/kg al
giorno», e il calcolo lo fa il medico. Due farmaci si mettono uno accanto all'altro, senza dire quale vince. Una terapia
si raccomanda solo dove la raccomanda una linea guida ufficiale, e allora è la linea guida a parlare, non noi.

## Dieci paletti

In agosto il memo sulla qualificazione come dispositivo medico ci ha mostrato anche il lato legale di quella scelta.
Lo abbiamo tradotto in un documento breve, il Vademecum, da leggere all'inizio di ogni sessione di lavoro, per la chat
come per Claude Code. Breve per scelta: un documento che non si riesce a rileggere ogni volta non serve.

Dentro c'erano dieci paletti. Alcuni sembrano ovvi, finché non si prova a rispettarli tutti insieme:

- **nessun calcolo**: mai una dose, una conversione, un aggiustamento derivato;
- **nessuna selezione sul paziente**: se la domanda porta l'età, il peso o la funzione renale, non si colloca il
  paziente in una fascia per mostrargli la sua riga, si restituisce la tabella intera, e la scelta è del medico;
- **nessun verdetto comparativo**: si giustappone, non si conclude, e se le fonti non concordano si mostra il
  disaccordo;
- **mai una sezione tagliata in silenzio**: o intera, o dichiarata parziale;
- **il canale pubblico è deterministico**: sulle schede aperte a tutti, nessun modello generativo, solo il testo
  ufficiale, integrale e letterale.

E poi l'ultimo, che li regge tutti: ogni affermazione ancorata alla sua fonte, con il codice del medicinale e la
sezione del foglio ufficiale da cui viene.

## Ordinare sì, collocare no

I paletti, però, si mettono alla prova sui casi difficili. Uno ci ha fatto pensare più degli altri.

Il foglio ufficiale di un farmaco ha una sezione sulle avvertenze che può essere lunghissima, e non entra mai tutta in
una risposta. Qualcosa va scelto. Se il medico chiede di un antipsicotico, l'aripiprazolo, in un paziente diabetico, e
noi prendiamo le avvertenze dall'inizio del documento, quella sul diabete può restare fuori. La risposta direbbe, in
pratica, che non esiste.

Allora il sistema mette per prime le parti che contengono le parole della domanda, come «diabete». È un aiuto del
paziente? Ci abbiamo ragionato a lungo, e a settembre la risposta è diventata una regola: ordinare sì, collocare no.
Il quadro del paziente può decidere quali parti entrano per prime, a tre condizioni: lo spazio è lo stesso con e senza
paziente; il criterio è la presenza delle parole nel testo, non un giudizio sul paziente; e la sezione si dichiara
parziale al medico.

Tutt'altra cosa sarebbe leggere «funzione renale 40», mettere il paziente nella fascia fra 30 e 44 e mostrare solo
quella riga. Il primo è cercare per pertinenza, come fa un buon indice analitico. Il secondo è classificare il
paziente, ed è il passo che ci era vietato.

## Il documento parla

In ottobre lo specchio ha preso la sua forma migliore. Sulla home lo dicevamo in tre frasi, una per ogni modo di
rispondere: «Risponde il documento», «L'IA sceglie, il documento parla», «L'IA compone».

Nel primo modo l'intelligenza artificiale è spenta. Se il medico scrive un farmaco e un tema riconoscibile, la
posologia, le controindicazioni, le interazioni, la gravidanza, il codice trova la sezione e la mostra, letterale.
Dalla fine di ottobre, anche chi scriveva il solo nome di un farmaco riceveva l'elenco dei medicinali con quel nome,
ciascuno con la sua scheda, senza che un modello scrivesse una parola.

Nel secondo modo il modello ha un compito piccolo e preciso: scegliere. Per una coppia di farmaci, o per un farmaco in
una certa condizione del paziente, legge l'elenco delle parti del foglio ufficiale e indica quali servono, con i loro
identificativi. Poi il codice va a prendere quelle parti e le inserisce alla lettera. Lo abbiamo riassunto così: il
modello indica, il documento parla.

Attorno al modello abbiamo messo delle reti, e tutte sono codice, nessuna sta nelle istruzioni del modello. Nelle
interazioni, il codice aggiunge sempre le parti che nominano l'altro farmaco, anche se il modello non le ha scelte. Se
il modello sceglie una riga di tabella per un paziente, il codice serve la tabella intera. Un identificativo che non
esiste non arriva al medico: si scarta e si conta. E se la scelta torna vuota, si servono le sezioni intere,
dichiarate.

Il terzo modo è il più vicino a un'IA generalista: il modello compone la risposta. Lì il testo è riformulato, e IP lo
dichiarava su ogni risposta.

La misura che ci ha convinti a costruire così l'abbiamo fatta in una notte di ottobre, con un budget di cinque euro per
il servizio di Google, e ne abbiamo spesi meno di due. Il modello piccolo che sceglieva le parti, interrogato due volte
sulle stesse domande, ha dato risposte identiche in 368 domande su 368. Per uno strumento che deve dire la stessa cosa
a due medici diversi, era il risultato che contava di più.

Pochi giorni dopo è arrivata la regola che chiude il cerchio: la domanda la interpreta il codice, non un modello. La
scintilla è stata una mia domanda, banale come le domande buone: se un medico scrive solo il nome di un farmaco, perché
parte comunque l'intelligenza artificiale? Il codice riconosce farmaci, temi e condizioni con regole scritte, che un
test può vedere fallire; il modello resta una destinazione dichiarata, non il centralino che decide la strada. Fra noi
lo dicevamo in quattro parole: il codice non indovina.

A novembre, infine, il modello che sceglieva le parti è diventato un modello addestrato da noi, sullo stesso servizio,
con qualche centinaio di esempi. L'addestramento è costato circa undici euro.

## Il pavimento

C'è un episodio di quelle settimane che racconto volentieri, perché mostra il metodo al lavoro.

Da giugno IP aveva un «pavimento di sicurezza»: qualunque fosse la domanda, la risposta doveva portare con sé le
controindicazioni, le avvertenze e la sezione su gravidanza e allattamento. Ma il pavimento viveva nel vecchio
percorso, quello che passava da un modello. Le risposte nuove, quelle in cui parlava il documento, arrivavano prima e
mostravano solo la sezione chiesta.

Non è stata la fortuna a farcelo scoprire. Ce l'ha detto la batteria di prove, che abbiamo fatto girare sul percorso
nuovo prima di accenderlo: sulle dieci domande a cui rispondeva, nove controlli del pavimento fallivano. La rete di sicurezza
esisteva, ma era scritta in un posto dove le risposte nuove non passavano.

L'abbiamo riscritta come codice, prima di accendere: sotto ogni risposta, chiuse e apribili con un clic, le sezioni
del pavimento che la risposta non portava già, ciascuna con la sua fonte. È una lezione che vale per chiunque metta un
modello in un prodotto: una protezione scritta nelle istruzioni del modello non arriva ai percorsi dove il modello non
c'è.

## Le schede, senza modello

Lo specchio più fedele erano le schede pubbliche, quelle che chiunque poteva aprire, anche arrivando da Google. Erano
composte dal codice, senza nessun modello sul percorso: il testo del foglio ufficiale, integrale e letterale, con la
data del documento d'origine e l'avvertenza in testa.

Quella scelta faceva due lavori insieme. Teneva le schede fuori dal territorio del dispositivo medico, e le teneva
anche dentro la sentenza europea sulla pubblicità dei farmaci raccontata nel capitolo 7, che protegge la riproduzione
integrale e letterale. Ed è servita una terza volta, per l'AI Act: il registro di verifica dei testi doveva prendere
l'impronta solo delle frasi che non riportavano il foglio alla lettera. Dove parlava il documento, non c'era niente da
marcare.

## Il prezzo dello specchio

Lo specchio funzionava. Nel test contro ChatGPT, IP ha avuto i suoi momenti migliori proprio dove la risposta stava
scritta nel documento: la tabella intera della metformina, la sezione giusta sulla gravidanza, la data in cui un
farmaco esce dal commercio.

Ma il medico, davanti a un paziente, non sempre vuole uno specchio. A volte vuole un collega che gli dica: questa dose
è sbagliata. È quello che ha fatto ChatGPT, ed è il passo che noi ci eravamo vietati, come racconta il capitolo 6.

Non rinnego la scelta di maggio. Per uno strumento dichiarato per i medici era l'unica strada che una persona sola
poteva percorrere in regola. Ma oggi la scriverei con una riga in più, accanto alla strada che non abbiamo preso: chi
la offrirà al nostro cliente, se non noi?

E lascio una cosa a chi costruisce in un altro campo. Riportare per costruzione, con il codice che interpreta, il
modello che indica e il documento che parla, è un metodo che vale ovunque un numero sbagliato costa caro: le norme
tecniche, il fisco, i contratti. Lì lo specchio può bastare, e può essere esattamente quello che il cliente cerca.

## Per chi costruisce

- **Scrivete le due strade, elaborare e riportare, prima del codice.** Accanto a ciascuna il rischio, il valore per il
  cliente e chi altro la offre già.
- **Un disclaimer non protegge un numero sbagliato.** La sicurezza sta nella fonte accanto al dato, non nell'avvertenza
  in fondo alla pagina.
- **Separate chi sceglie da chi parla.** Il modello indica gli identificativi; il codice inserisce il testo alla
  lettera. Così il modello può sbagliare la scelta, ma non può inventare il contenuto.
- **Mettete le reti di sicurezza nel codice, non nelle istruzioni del modello.** Le seconde non arrivano ai percorsi
  dove il modello non c'è, e un test non le vede fallire.
- **Lasciate interpretare la domanda al codice, dove può.** Regole scritte, che un test vede fallire; il modello come
  destinazione dichiarata, non come centralino.
- **Distinguete ordinare da collocare.** Mettere per prime le parti pertinenti è cercare; mettere il cliente in una
  fascia e mostrargli solo la sua riga è decidere al suo posto.
- **Misurate la ripetibilità.** Se lo stesso strumento dà due risposte diverse alla stessa domanda, non è uno specchio.
- **Fate girare una batteria di prove prima di ogni accensione.** È lei che vi dice quale protezione è rimasta indietro.

---

### Riquadro — Riportare per costruzione, la ricetta

*Per il lettore tecnico: i paletti, i tre modi di rispondere, le reti di codice e le misure. Vale per qualunque
dominio in cui il testo d'origine fa fede.*

**I dieci paletti** (Vademecum di IP, agosto 2026, con le precisazioni successive)

1. Nessun calcolo: mai una dose, una conversione, un aggiustamento derivato.
2. Nessuna selezione sul paziente: con un parametro individuale si restituisce la tabella intera. Si può ordinare per
   pertinenza testuale, sotto un tetto uguale con e senza paziente, dichiarando la sezione parziale.
3. Nessun verdetto comparativo; se le fonti non concordano, si mostra il disaccordo.
4. Nessun numero che non sia nel contesto recuperato.
5. Mai una sezione troncata in silenzio: intera o dichiarata parziale, anche nella struttura delle tabelle.
6. Destinatario dichiarato: il medico, in ogni documento.
7. Canale pubblico deterministico: nessun modello generativo sulle schede pubbliche.
8. Uso dell'IA dichiarato dove c'è (AI Act, art. 50).
9. Data dichiarata su ogni scheda, generazione e documento d'origine.
10. Ogni affermazione ancorata: codice AIC e sezione dell'RCP, riferimento della linea guida, PMID.

**I tre modi di rispondere** (ottobre 2026)

| modo | chi interpreta la domanda | chi sceglie che cosa mostrare | chi scrive il testo | dichiarazione |
|---|---|---|---|---|
| «Risponde il documento» (L1): un farmaco e una sezione, o il solo nome | il codice | il codice | il documento, alla lettera | nessun modello |
| «L'IA sceglie, il documento parla» (L2): una coppia di farmaci, o un farmaco con una condizione | il codice | un modello piccolo, che restituisce identificativi in JSON | il documento, alla lettera, inserito dal codice | IA usata per scegliere |
| «L'IA compone» (L3): tutto il resto | un modello (il piano) | il recupero | il modello | IA che compone |

**Le reti di codice attorno a L2**

- nomi: nelle interazioni, sempre le parti che nominano l'altro principio attivo;
- popolazione: per una condizione del paziente, le parti della posologia che la nominano;
- tabella intera: una riga scelta per un paziente diventa la tabella intera;
- identificativi: quelli inesistenti si scartano e si contano;
- selezione vuota: le sezioni intere, dichiarate;
- tetto: oltre 20 parti scelte, la scelta vale come non riuscita e si servono le sezioni intere;
- pavimento: sotto ogni risposta, chiuse, controindicazioni, avvertenze e gravidanza che la risposta non porta già.

**Le misure**

| che cosa | valore | quando |
|---|---|---|
| ripetibilità del selettore, due esecuzioni sulle stesse domande | risposte identiche in 368 su 368 | notte del 19/10/2026 |
| spesa per le misure della notte | 1,65 € su un budget di 5 € | 19/10/2026 |
| domande scritte da noi fra marzo e ottobre riconosciute dal codice | 82 su 536 (15 %), prima di aprire il solo nome | 22/10/2026 |
| domande riconosciute dal codice ma mandate al modello per scelta di perimetro | circa 224, di cui 127 erano il solo nome di un farmaco | 22/10/2026 |
| addestramento del selettore | 377 esempi, 3 epoche, circa 11 € al listino | 8/11/2026 |
| controlli del pavimento falliti sul percorso nuovo, prima della correzione | 9, sulle 10 domande della batteria servite da quel percorso | 20/10/2026 |

---

*Scritto a quattro mani con Claude. Le scelte, e la responsabilità di quello che c'è scritto, sono mie.*
