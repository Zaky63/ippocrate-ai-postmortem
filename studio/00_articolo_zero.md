# Ho spento il mio prodotto dopo otto mesi. Vi racconto perché, e che cosa ho imparato

Il 24 novembre ho spento ippocrate.ai, il prodotto a cui lavoravo da otto mesi.

Non l'ha fermato un bug, e nemmeno la mancanza di soldi: in tutto era costato meno di duemila euro. L'ha fermato una
prova di poche ore contro un'intelligenza artificiale generalista, usata con un account gratuito, e una regola per
decidere che era stata scritta prima di guardare i risultati.

Questa serie racconta come ci sono arrivato. La scrivo per chi costruisce software con l'intelligenza artificiale,
soprattutto da solo o quasi: perché possa evitare i miei errori e rifare, se gli servono, le cose che hanno
funzionato. Perché ce ne sono state anche di quelle.

È anche la storia di un'idea che oggi sembra a portata di mano: che una persona sola, con un'IA, possa portare un
prodotto dall'idea al lancio. Si può, ho scoperto, a una condizione: che le decisioni restino sue, e che l'IA lavori
dentro una rete di controlli e accanto a persone che sanno quello che lei non sa. Noi avevamo l'IA e i controlli. Il
parere di un legale l'avevamo rinviato, e i medici non sono arrivati: è proprio lì che IP si è fermato.

## Una biblioteca per il medico di famiglia

ippocrate.ai, IP per gli amici, era un assistente per i medici di famiglia italiani. Rispondeva alle loro domande sui
farmaci, in linguaggio normale, citando la fonte di ogni frase: i documenti ufficiali dell'AIFA (il foglio del farmaco
scritto per il medico, chi paga, a quali condizioni, quali medicinali sono in carenza), le linee guida italiane e gli
studi scientifici di PubMed.

Dentro c'era un modello di intelligenza artificiale, ma tenuto al guinzaglio: doveva riportare quello che dicono i
documenti, non aggiungere del suo.

Ci ho lavorato di sera e di notte, a partire da metà marzo, in una compagnia insolita: due intelligenze artificiali.
Un Claude progettava con me in una chat, un altro, Claude Code, metteva le mani sul codice e sul server. Io decidevo.
Alla fine le modifiche salvate erano quasi tremila, metà al codice e metà ai documenti, e le decisioni scritte nero
su bianco più di cinquecento.

Anche questa serie l'ho scritta a quattro mani con Claude: io ho scelto che cosa raccontare, ho scritto alcune parti
e ho approvato ogni stesura; Claude ha letto le fonti del progetto e ha scritto le bozze.

## La busta sigillata

A fine novembre mi sono fatto una domanda scomoda: un'IA generalista, di quelle che tutti hanno sul telefono, fa
meglio del mio prodotto?

Per rispondere abbiamo preparato dieci domande difficili, metà sul nostro terreno e metà cliniche, con una chiave
delle risposte giuste. E, prima di vedere una sola risposta, abbiamo scritto la regola per decidere: per meritare di
esistere, IP doveva battere il generalista sul proprio terreno con un margine chiaro. Funziona come una busta
sigillata prima della partita. Se il pronostico lo scrivi dopo il fischio finale, non è più un pronostico.

ChatGPT ha fatto meglio quasi su tutta la linea. Ma a farmi desistere non sono stati gli errori di IP: erano errori di
dato, di quelli che si correggono in poche ore. È stato leggere le risposte dell'altro. IP rispondeva come un
bibliotecario scrupoloso, che ti porge il libro giusto aperto alla pagina giusta. ChatGPT rispondeva come un collega:
guardava il paziente descritto nella domanda e traeva una conclusione su di lui.

Ed è proprio lì che passava il nostro recinto. Per la legge europea, almeno per come l'abbiamo letta noi, un software
che si presenta come strumento per i medici e trae conclusioni sul singolo paziente diventa un dispositivo medico, con
una certificazione che non si fa una volta sola: è un carico che si porta per sempre. Troppo, per un'impresa di una
persona. Un'IA generalista, che quello scopo non lo dichiara, può scrivere la stessa frase.

Letti i punteggi, ho scritto due parole: «Ok spegniamo».

## Se avete fretta: tre lezioni in tre righe

1. **Prima del codice, guardate il recinto.** Non basta sapere dove passa il confine legale: chiedetevi se il valore
   che il cliente cerca sta dentro o fuori. Noi l'abbiamo capito all'ottavo mese; si poteva capire al primo.
2. **Fate la prova del generalista il primo giorno, e rifatela a ogni nuovo modello.** Costa poche ore. In un campo che
   corre così, otto mesi sono un'era geologica.
3. **Cominciate a costruire il pubblico il primo mese, non l'ottavo.** È l'errore più rimediabile dei tre, ma è un
   errore.

## Che cosa troverete nella serie

Dieci capitoli, uno per articolo.

1. **Perché abbiamo spento ippocrate.ai**: la prova contro il generalista, per intero, e come rifarla sul vostro
   prodotto.
2. **Un'azienda di una persona e due Claude**: il metodo, una chat che progetta, Claude Code che esegue e una persona
   che decide, con un registro di decisioni che una volta scritto non si tocca più.
3. **Dai PDF alle risposte**: come diventano una risposta novemila documenti ufficiali, e come si misura che sia giusta.
4. **Le citazioni inventate**: perché un modello che inventa una fonte si ferma solo con un controllo nel codice.
5. **Riportare, non elaborare**: il confine fra un'opera di consultazione e un dispositivo medico, e come abbiamo
   costruito per restarne di qua.
6. **L'asimmetria regolatoria**: la stessa frase che pesa in modo diverso a seconda di chi la scrive.
7. **Che cosa chiede la legge a chi fa software, oggi**: protezione dei dati, regole sull'IA, dispositivi medici,
   responsabilità per i danni; i documenti che abbiamo scritto in casa e quanto sarebbe costato il parere di un legale.
8. **Quanto costa**: il conto vero, voce per voce, dalle fatture. La voce più piccola è stata il modello che
   rispondeva ai medici.
9. **Prima il prodotto, poi i medici**: il canale verso i clienti, cercato troppo tardi.
10. **Cosa rifarei, e cosa lasciamo**: le tre domande da fare prima della prima riga di codice, e gli strumenti che
    pubblichiamo.

## Dove leggere tutto

Lo studio completo sta in un repository pubblico su GitHub, [github.com/Zaky63/ippocrate-ai-postmortem](https://github.com/Zaky63/ippocrate-ai-postmortem),
con gli strumenti che il metodo ha prodotto: il generatore degli indici delle decisioni, gli script che fanno i commit
nell'ordine giusto, le istruzioni per Claude Code su come si scrive una decisione, e il ponte che permette alla chat di
affidare un lavoro a Claude Code sul computer e di seguirne l'esito. Il testo è libero di essere ripreso citando la
fonte; il codice è libero di essere usato.

Un prodotto spento può ancora insegnare qualcosa, se quello che resta di lui è a disposizione di tutti. Ci vediamo al
primo capitolo.

---

*Scritto a quattro mani con Claude. Le scelte, e la responsabilità di quello che c'è scritto, sono mie.*
