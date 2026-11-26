# 8. Quanto costa

## Il conto della spesa

Quando si dice «intelligenza artificiale», molti pensano a capannoni pieni di computer che ronzano e a bollette da
capogiro. Per i giganti del settore è così: un grande modello si addestra con centinaia di milioni di dollari, e chi lo
offre a milioni di persone al giorno paga conti che finiscono sui giornali. Un progetto piccolo, però, i modelli non li
costruisce: li prende in affitto. E allora il conto ha un'altra forma, e riserva qualche sorpresa.

Questo capitolo è il nostro conto della spesa. Dice quanto è costato IP in otto mesi, voce per voce, e lo prende dalle
fatture, non dalla memoria. La risposta breve: la voce più piccola è stata il modello che rispondeva ai medici. Una
batteria di settantadue domande, il controllo che facevamo dopo ogni modifica importante, costava meno di quaranta
centesimi. Le voci grosse stavano altrove: un lavoro fatto una volta sola, lo strumento che scriveva il codice e, più
grossa di tutte, una voce che non compare in nessuna fattura.

## Quaranta centesimi

Cominciamo dalla voce che tutti temono: quanto costa ogni risposta. Quando un medico faceva una domanda, IP di solito
chiamava un modello Gemini due volte. La prima chiamata serviva a capire la domanda e a decidere che cosa cercare; la
seconda a comporre la risposta sui documenti trovati. Ogni chiamata si paga a gettoni, i *token*, che sono pezzetti di
parola: qualche migliaio entra nel modello, qualche centinaio ne esce.

A novembre, col modello più piccolo e veloce della famiglia, le settantadue domande della batteria sono costate 0,38
euro in tutto. Fa mezzo centesimo a domanda, circa cinque euro ogni mille. A giugno, con un modello della generazione
precedente, la media era di un centesimo, e una sola domanda mandata al modello più grande pesava quasi quanto tutte le
altre insieme. È il primo dettaglio da tenere a mente. Il costo dipende meno dal numero delle domande che dal modello
che le riceve e da quanto testo gli si dà da leggere. In un sistema come IP i gettoni sono quasi tutti in entrata: sono
i brani dei documenti ufficiali che il modello deve leggere prima di scrivere una riga.

A ogni domanda si fa anche un'altra operazione: il testo diventa un elenco di numeri, l'*embedding*, che serve a
cercare i brani più vicini (capitolo 3). Da giugno quell'operazione non costava niente, perché il modello che la faceva
girava sul nostro server e non era più a noleggio.

Come facevamo a saperlo con tanta precisione? Da metà giugno ogni risposta registrava i gettoni consumati, divisi per
modello e per fase, e un piccolo script li moltiplicava per il listino. Ogni batteria aveva poi un tetto di spesa,
dichiarato prima di lanciarla, un euro, e il referto confrontava il conto con quel tetto. Prima di giugno le stime si
facevano a occhio, e fra poco vedremo dove portano le stime a occhio.

A maggio, prima di avere quelle misure, avevamo previsto che IP in esercizio sarebbe costato fra cinquecento e
millecinquecento euro al mese. A luglio il costo vero era di una trentina di euro al mese, spesi quasi tutti nelle
batterie di controllo. Un solo medico abbonato avrebbe pagato un mese intero di batterie.

## La sera in cui finì il credito

Il costo delle risposte era piccolo; quello dei lavori fatti una volta sola no. Il più grande l'abbiamo fatto a maggio.

L'idea era ambiziosa. Un modello avrebbe letto i riassunti delle caratteristiche di tutti i farmaci, uno per uno, e da
ciascuno avrebbe ricavato una scheda ordinata, con le stesse voci per tutti: settemilacinquecento farmaci. E per
misurare quanto fosse stabile ogni scheda, l'avrebbe compilata tre volte. L'abbiamo lanciato a tarda sera, il 12
maggio, e doveva girare per due notti. Ha girato quasi tre giorni, in tre riprese, ed è costato circa
trecentocinquanta euro, più del doppio della stima.

La stima veniva dalle prove su pochi farmaci, e quei pochi avevano riassunti più corti della media. Sul corpus vero ogni
scheda chiedeva un terzo di testo in più da leggere, e la forma rigida della scheda chiedeva più testo in uscita. Da
allora la regola è questa: la stima di un lavoro lungo si fa su un campione a caso di qualche centinaio di elementi, si
guardano i casi più pesanti e non la media, e il risultato si moltiplica per due.

La seconda sera è successa una cosa più istruttiva. Il lavoro girava sul credito di prova che Google regala a chi apre
un conto, trecento dollari, e a metà strada il credito è finito. Senza un metodo di pagamento di riserva, Google ha
chiuso il conto, e ogni chiamata ha cominciato a ricevere un rifiuto: permesso negato. Lo script sapeva aspettare e
riprovare quando il servizio è sovraccarico. Ha preso quel rifiuto per un intoppo passeggero, e per mezz'ora ha bussato
a una porta chiusa, finché non l'abbiamo fermato. Abbiamo spostato il progetto su un conto a pagamento, ma la carta
collegata aveva un tetto mensile troppo basso, e un addebito di un centinaio di euro è rimasto in sospeso. Il lavoro è
ripartito il giorno dopo ed è finito nella notte del 16 maggio. La pratica con Google si è chiusa a fine luglio, con i
pagamenti in regola.

In quei giorni abbiamo scoperto anche un'altra cosa. Sul conto c'era un secondo credito, di oltre ottocento euro, e
contavamo di usarlo. Era un credito di prova per un altro prodotto di Google, e sulle nostre chiamate non si è mai
potuto spendere: nemmeno sull'addestramento del selettore (capitolo 5), che a novembre l'ha lasciato intatto. Un
credito vale quello che dicono le sue condizioni, non la cifra che mostra.

Nessuno di questi inciampi è stato grave: tutti insieme ci sono costati qualche giorno e un centinaio di euro. Ma
insegnano tre cose che conviene sapere prima e non dopo. Prima di un lavoro lungo si guarda quale credito si sta
consumando, quando scade e su che cosa si può spendere. Si collega una carta con un tetto adeguato, e si attiva un
avviso di spesa. E nel codice un rifiuto per permessi è definitivo: si ferma tutto e non si riprova.

## Le stime sbagliano nei due sensi

La stima dell'estrazione era bassa di più della metà. Quella del costo in esercizio era alta di oltre dieci volte. E ce
n'è una terza, la più spettacolare.

All'inizio IP trasformava i testi in numeri con un modello di Google, a noleggio. A fine maggio, mentre ne provavamo
altri, era circolata una stima del costo di quell'operazione sull'intero corpus: fra ottocento e mille euro. A fattura
chiusa, la prova su quindicimila frammenti era costata quarantotto centesimi, e tutto il corpus ne sarebbe costati una
ventina. Tre ordini di grandezza.

A giugno il modello a noleggio l'abbiamo sostituito con un modello libero che gira sul nostro hardware. Non per
risparmiare, perché il risparmio era piccolo, ma per la qualità della ricerca e per non dipendere da un solo fornitore.
Da allora abbiamo ricostruito il corpus più volte sulla scheda video del PC di casa (capitolo 3): ogni ricostruzione
costava tre ore di scheda video, cioè la corrente di una sera.

La morale non è che le stime non servono. È che una stima vale finché non arriva la fattura, e la fattura va letta. Da
giugno in poi le decisioni sui costi le abbiamo prese sui numeri misurati: i gettoni di ogni risposta, il conto
mensile, il costo di ogni batteria scritto nel suo referto.

## Le spese fisse

Poi ci sono le spese che corrono comunque, che il prodotto lo usi qualcuno o no.

C'è il server. IP girava su un server virtuale in affitto, in Italia: 25 euro al mese più IVA. Lì stavano la base di
dati dei farmaci e quella dei vettori. Accanto c'era lo spazio per le copie di sicurezza, pochi euro.

C'è il nome. Un dominio che finisce in .ai si registra per due anni, pagati in anticipo: 194 euro. La posta, compresa
quella certificata, costa una quarantina di euro l'anno.

C'è un mese di abbonamento, 29 euro, a uno strumento di ricerca giuridica con l'intelligenza artificiale, che abbiamo
usato per le ricerche raccontate nel capitolo 7.

E c'è Google, fuori dai lavori grossi. Da maggio a novembre le fatture mensili del conto a pagamento sono andate da meno
di cinque euro a poco più di quaranta, IVA compresa, e hanno sommato poco meno di duecento euro. I mesi più cari sono
stati gli ultimi, ottobre e novembre, con le prove dei modelli nuovi, l'addestramento del selettore, le misure notturne
e il confronto con ChatGPT.

## Lo strumento che scrive il codice

Una voce non riguarda il prodotto ma chi lo costruisce, ed è stata la più grande di tutte: l'abbonamento a Claude.

Il capitolo 2 racconta come abbiamo lavorato: una persona e due Claude, la chat che progetta e Claude Code che esegue.
Tutti e due giravano su un abbonamento personale, il piano Max, da marzo: 109,80 euro al mese IVA compresa, quasi mille
euro fino a novembre. È più del doppio di quanto sia costato Google in tutto, e più del triplo del server.
L'abbonamento, però, non si paga a chiamata. Per questo nei nostri briefing «costo zero» voleva dire zero su Google, e
la spesa si dichiarava solo per i modelli del prodotto; quando a ottobre ho delegato a Claude le scelte di routine, il
limite che ho messo riguardava quella spesa, dieci euro.

Lo stesso abbonamento serviva anche ad altro, quindi non va tutto sul conto di IP. Per chi costruisce, però,
la lezione resta: con questo modo di lavorare la voce più cara non è il modello che risponde ai clienti, è quello che
scrive il codice. Va messa nel budget dal primo giorno.

## I crediti che non sono arrivati

Google ha un programma per le startup che regala crediti, anche consistenti, e noi ci abbiamo provato due volte, a
luglio e a ottobre. La seconda volta abbiamo accompagnato la domanda con una mail che diceva le cose come stavano:
un'impresa individuale, autofinanziata, senza nessun piano di cercare capitale di rischio. Tutte e due le domande sono
state respinte.

Il motivo non lo sappiamo. Sappiamo però che fra i primi criteri del programma c'è l'intenzione di raccogliere capitale
di rischio a breve, e che un'impresa artigiana del software, come avevamo scelto di essere, non è il cliente per cui il
programma è pensato. Non c'è niente di male: basta saperlo prima, e non contarci nel piano. L'addestramento del
selettore, che speravamo di pagare con quei crediti, l'abbiamo pagato noi: undici euro.

## Il conto totale, e quello vero

Mettiamo tutto in fila. In otto mesi IP è costato, in denaro, quasi duemila euro, IVA compresa. Quasi mille sono andati
all'abbonamento a Claude; fra trecento e quattrocento a Google, oltre al credito di prova; poco meno di trecento al
server; il resto al dominio, alla posta e a un mese di ricerca giuridica. La batteria da quaranta centesimi, ripetuta
dopo ogni modifica, in questo conto è una goccia.

Un confronto aiuta. I tre pareri legali scritti che avevamo chiesto, e poi rinviato, sarebbero costati quasi seimila
euro (capitolo 7): tre volte tutto il resto messo insieme. E poi c'è la voce che non compare in nessuna fattura, il
tempo: otto mesi di sere e di notti, quasi tremila modifiche registrate nel codice, più di cinquecento decisioni
scritte.

Non sono stati i soldi a fermare IP: né quelli dei modelli, né quelli del server. Con meno di cento euro al mese, fra
server, modelli e dominio, stava in piedi un servizio che leggeva novemila documenti ufficiali e metteva la fonte
accanto a ogni frase. I conti che non tornavano erano altri: quello del recinto legale, raccontato nei capitoli 6 e 7,
e quello del tempo che serve per trovare chi paga, raccontato nel capitolo 9.

---

## Per chi costruisce

**Da replicare**

- **Misura il costo di ogni risposta nel codice, dal primo giorno**: gettoni in entrata e in uscita, per modello e per
  fase, col listino scritto in un posto solo. Con quella misura le decisioni sui modelli si prendono sui numeri.
- **Dai un tetto di spesa a ogni lavoro ripetuto** (il nostro era un euro a batteria, scritto nel briefing e controllato
  nel referto; meglio ancora se a farlo rispettare è il codice) e **un limite a quanto l'assistente può spendere da
  solo** (dieci euro, capitolo 2).
- **Tieni separati i lavori fatti una volta dai costi di esercizio.** Hanno ordini di grandezza diversi e si stimano in
  modo diverso: i primi si sottostimano, i secondi si sopravvalutano. Ma su un corpus che cresce il lavoro «fatto una
  volta» torna per i documenti nuovi, e va messo a budget come costo ricorrente: le schede le abbiamo estratte a maggio
  per 7.550 farmaci, e a luglio 2.639 farmaci del corpus ne erano senza.
- **Se hai una scheda video, valuta di far girare in casa i modelli piccoli**, come quello dell'embedding. Il guadagno
  vero non è il risparmio, ma poter ricostruire tutto quando serve senza guardare il conto.
- **Metti nel budget lo strumento che scrive il codice.** Con un assistente come Claude Code è facilmente la voce più
  grande.

**Da evitare**

- **Le stime su un campione piccolo e comodo.** Per un lavoro lungo prendi qualche centinaio di elementi a caso, guarda
  i casi più pesanti, e moltiplica per due.
- **Un controllo di coerenza preso alla leggera.** Se rifà lo stesso lavoro tre volte, triplica il conto: decidi prima
  se vale il prezzo.
- **Lanciare un lavoro lungo senza sapere quale credito stai consumando**, quando scade, su che cosa si può spendere e
  se la carta di riserva regge.
- **Trattare un rifiuto per permessi come un intoppo passeggero.** È definitivo: si ferma tutto.
- **Contare sui crediti dei programmi per startup** se non hai il profilo per cui sono pensati.
- **Guardare solo il costo dei modelli.** Il nostro conto più alto stava fuori dalle fatture del cloud.

---

## Riquadro: il conto, voce per voce

**Le voci** (IVA compresa dove non è detto altro; marzo–novembre 2026)

| voce | importo | note |
|---|---|---|
| abbonamento Claude Max | 109,80 € al mese; 988 € da marzo a novembre | prima c'era il piano Pro; usato anche per altro |
| prime prove su conti personali Google | circa 48 € | marzo–maggio, prima del conto a pagamento |
| credito di prova di Google | 300 dollari (256 €) | consumato a maggio, quasi tutto nell'estrazione delle schede; non pagato da noi |
| estrazione delle schede, 7.550 farmaci, tre letture per farmaco | circa 350 €: circa 175 sul credito di prova, circa 180 pagati | 12–16 maggio, circa 67 ore in tre riprese; stima iniziale circa 150 € |
| conto Google a pagamento, fatture mensili | 183 € in tutto, da 4,77 € (agosto) a 46,04 € (ottobre) | maggio–25 novembre; saldi di fine mese |
| di cui: addestramento del selettore | 10,98 € al listino | 377 esempi, 3 epoche, novembre |
| di cui: misure di una notte di ottobre | 1,65 € su un budget di 5 € | 19 ottobre |
| credito per un altro prodotto Google | 855 € | mai spendibile sulle nostre chiamate né sull'addestramento |
| server virtuale | 25 € al mese più IVA; circa 275 € da marzo a novembre | in Italia |
| dominio .ai di IP | 194 € | registrazione obbligatoria per due anni anticipati |
| posta, compresa la certificata | circa 41 € l'anno | |
| strumento di ricerca giuridica con IA | 29 € | un mese di abbonamento |
| pareri legali | 0 € | preventivo di circa 6.000 € per tre pareri, rinviati (capitolo 7) |
| pubblicità | 0 € | 300 € previsti, mai spesi (capitolo 9) |
| **totale in denaro** | **quasi 2.000 €** | fra 1.830 e 1.940 € secondo come si legge maggio; credito di prova escluso |

**Il costo di una risposta**

| quando | modello | domande | costo | per domanda |
|---|---|---|---|---|
| giugno 2026 | Gemini 2.5 Flash, più una chiamata a 2.5 Pro | 16 | 0,16 € | 1 centesimo; 0,6 senza la chiamata Pro |
| novembre 2026 | Gemini 3.5 Flash-Lite, più 4 chiamate al selettore addestrato | 72 | 0,3754 € (generazione 0,3070, piano 0,0684) | 0,52 centesimi, circa 5,2 € ogni mille (calcolo nostro) |
| da giugno | embedding e5 sul nostro server | ogni domanda | 0 € | — |

Gettoni della batteria di novembre: 532.992 in entrata alla generazione, 64.080 in uscita, di cui 19.277 di
ragionamento, che si pagano come uscita.

**La ricetta per tenere il conto sotto controllo**

1. Registra a ogni risposta il modello e i gettoni in entrata, in uscita e di ragionamento.
2. Tieni il listino in un posto solo nel codice, e fai calcolare il conto a uno script.
3. Dai un tetto a ogni lavoro ripetuto e all'assistente che lavora da solo.
4. Attiva l'avviso di spesa sul conto del cloud, e sappi quando l'addebito diventa immediato: per noi, oltre 100 € di
   saldo.
5. Prima di un lavoro lungo controlla i crediti: quale si consuma per primo (quello che scade prima), su quali servizi
   vale, quanto ne resta. Tieni una carta di riserva con un tetto adeguato e un margine di 100–150 €.
6. Stima su 50–200 elementi presi a caso, guardando i casi più pesanti (il 95° percentile), e moltiplica per due.
7. Un rifiuto per permessi ferma il lavoro: nessun nuovo tentativo.

---

*Scritto a quattro mani con Claude. Le scelte, e la responsabilità di quello che c'è scritto, sono mie.*
