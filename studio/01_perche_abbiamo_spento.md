# 1. Perché abbiamo spento ippocrate.ai

Ci sono decisioni che maturano per mesi e poi si prendono in poche ore. Quella di spegnere ippocrate.ai è stata così:
otto mesi di lavoro, e alla fine è bastato un giorno di fine novembre.

Per capire che cosa è successo quel giorno, però, bisogna fare un passo indietro e raccontare che cosa era IP, e per
chi era stato pensato.

## Una biblioteca per il medico

Proviamo a metterci nei panni di un medico di famiglia. Ha davanti un paziente, pochi minuti, e un dubbio. Questo
farmaco glielo posso prescrivere a carico del Servizio sanitario? Va d'accordo con quello che prende già? A che dose?

Le risposte esistono, e sono scritte. Le scrive l'AIFA, l'Agenzia italiana del farmaco. Per ogni medicinale c'è un
documento che si chiama RCP, riassunto delle caratteristiche del prodotto: una sorta di carta d'identità del farmaco,
scritta per il medico, con le dosi, le controindicazioni, le interazioni. Poi ci sono le classi di rimborsabilità,
che dicono chi paga, e le Note AIFA, piccoli regolamenti che fissano le condizioni alle quali un farmaco lo paga lo
Stato.

Il guaio è che tutto questo è sparso in migliaia di pagine, e cambia di continuo. Un medicinale esce dal commercio,
una Nota viene riscritta, un prezzo si aggiorna.

ippocrate.ai, IP per gli amici, nasceva per questo: raccogliere quei documenti, tenerli aggiornati e rispondere alle
domande del medico in linguaggio naturale, citando ogni volta la fonte. Dentro c'era un modello di intelligenza
artificiale, Gemini di Google, tenuto però al guinzaglio: doveva riportare quello che dicono i documenti, non
aggiungere del suo. È un dettaglio da tenere a mente, perché alla fine di questa storia sarà proprio quel guinzaglio
a decidere.

Ci ho lavorato di sera e di notte, per otto mesi, a partire da metà marzo. In una compagnia insolita: due
intelligenze artificiali, due Claude, uno che progettava con me in una chat e l'altro che metteva le mani sul codice e
sul server. Ma questa è una storia che merita un capitolo a sé.

E qualcosa di concreto, in quegli otto mesi, l'abbiamo costruito. Una vetrina pubblica con una scheda per ogni
medicinale autorizzato. Una pagina che seguiva le carenze dei farmaci confrontando gli elenchi dell'AIFA settimana per
settimana. Una newsletter per i medici. Una consultazione in linguaggio naturale che citava la fonte di ogni frase. E,
dentro la consultazione, una ricerca degli studi su PubMed fatta al momento, con una riga in italiano per ogni articolo.
Alla fine le modifiche salvate erano quasi tremila, metà al codice e metà ai documenti, e le decisioni scritte nero
su bianco più di cinquecento.

## Tre giorni di novembre

La fine comincia un sabato.

Da qualche tempo i dubbi si erano fatti insistenti. Il prodotto c'era, la vetrina pubblica era aperta da un mese, ma i
medici non arrivavano. E intorno a noi la concorrenza correva: aziende con molte più persone e molti più mezzi
offrivano già ai medici strumenti simili, alcuni gratis.

Quel sabato avevo condiviso con la chat un articolo letto su Substack. Luca Cazzaniga vi raccontava una scena di
qualche mese prima: Andrej Karpathy, uno dei fondatori di OpenAI, aveva spiegato sul palco che a Gemini, un'IA
generalista, era bastata una sola richiesta per fare il lavoro di un'app che lui stesso aveva costruito. E aveva
concluso, senza giri di parole, che quell'app non sarebbe dovuta esistere. Poco dopo, scrivendo alla chat, mi sono
chiesto: «A che condizioni un carretto con i gelati artigianali può avere successo contro una multinazionale di
gelati?».

Lo stesso giorno ho voluto fare comunque una verifica. Esiste una raccolta di domande sugli RCP italiani, PharmaQA.IT,
pubblicata quest'anno per mettere alla prova sistemi come il nostro. Senza scomodare l'intelligenza artificiale,
abbiamo controllato una cosa semplice: quando IP riceveva una domanda su un farmaco, nel testo che andava a pescare
c'era la risposta giusta? C'era, nove volte su dieci, e quasi mai per caso. La biblioteca, insomma, era in ordine: i
libri giusti stavano sugli scaffali giusti. Era un successo vero, e ce lo eravamo guadagnato.

La domenica ho aperto la chat con un titolo che diceva già molto: «Considerazioni in ordine sparso prima di "buttare
tutto alle ortiche"». IP mi sembrava una cattedrale nel deserto. Alla fine di quella conversazione ho preso una
decisione prudente: IP restava acceso al
minimo fino alla fine di febbraio, senza nuove funzioni, e a fine febbraio si sarebbe contato. Almeno trenta medici
iscritti, e almeno dieci che tornassero con regolarità; altrimenti, si spegne.

Era una domanda onesta: i medici arrivano? Ma ne lasciava aperta un'altra, più scomoda. E quando arrivano, che cosa
trovano?

Il martedì, quella domanda l'ho fatta.

## La domanda del martedì

Ho aperto la chat così: «Claude o ChatGPT con un abbonamento base fa meglio di IP? Secondo me sì». E con la
riflessione che l'articolo del sabato mi aveva lasciato, tradotta per IP, e che a ripensarci avrebbe potuto guidare
tutto il progetto fin dal primo giorno: «se è una cosa che già fa una IA generalista ora o a breve, è inutile
provarci».

Era un'ipotesi, non una sentenza. E in questo progetto le ipotesi si verificavano.

## La busta sigillata

La chat ha proposto un esperimento semplice: dieci domande difficili, poste nello stesso modo a IP e a un'IA
generalista.

Cinque erano domande regolatorie, il pane quotidiano di IP: chi paga un farmaco, a quali condizioni, quanto costa.
Erano proprio le cose che un sistema costruito sugli elenchi dell'AIFA doveva sapere meglio di chiunque, scelte fra le
novità dell'anno: un antidolorifico molto noto passato a carico del paziente, una Nota sui gastroprotettori riscritta
da capo, un farmaco per il diabete che esce dal commercio e lascia il posto a una versione a dose diversa, una regola
sugli anticoagulanti semplificata a giugno. La quinta chiedeva quanto paga di tasca sua chi vuole il farmaco di marca
e non il generico.

Le altre cinque erano domande cliniche, di quelle che si incontrano in ambulatorio: un farmaco per il diabete in un
paziente con i reni che lavorano a meno della metà, un anticoagulante in un anziano che ha bisogno di un antibiotico,
un antinfiammatorio in gravidanza, un antibiotico per la cistite, due farmaci che insieme diventano pericolosi.

La chat ha scritto anche la chiave delle risposte, controllandola sui documenti dell'AIFA. Per ogni domanda diceva che
cosa serve perché una risposta sia giusta e quale errore la rende sbagliata: non un'imprecisione qualsiasi, ma un
errore grave, di quelli che possono portare a una prescrizione sbagliata.

E poi è venuta la parte che considero la più importante: la regola per decidere, scritta prima di vedere una sola
risposta. Funziona come una busta sigillata prima della partita. Se il pronostico lo scrivi dopo il fischio finale,
non è più un pronostico. La regola diceva che, per meritare di esistere, IP doveva battere il miglior generalista sulle
domande regolatorie di almeno due risposte giuste, e senza sbagliare più di lui. Una sola risposta di scarto su cinque
può essere un caso, e un caso non giustifica mesi di lavoro.

Ho fatto io le domande, una per una, nelle app di ChatGPT e di IP. Un paio d'ore dopo avevo davanti venti risposte.

## Il punteggio, e quello che non diceva

Il punteggio è stato netto. Sulle domande regolatorie ChatGPT, con un semplice account gratuito, ha fatto meglio di IP
su quasi tutta la linea; la busta sigillata aveva già parlato.

Non era un esperimento da laboratorio, e non pretendeva di esserlo: una sola prova per domanda, ChatGPT nella versione
gratuita, i punteggi proposti dalla stessa chat che aveva scritto la chiave. Ma per decidere bastava. Il margine era
largo, e la regola era nella busta prima che la partita cominciasse.

IP aveva anche inciampato su due dati: un antidolorifico che dava ancora a carico dello Stato e una Nota sui
gastroprotettori che non conosceva. Errori di dato, di quelli che, ne sono convinto, avremmo corretto in poche ore di
lavoro. E comunque, anche correggendoli tutti, IP avrebbe al massimo pareggiato.

Ma non sono stati i nostri errori a farmi desistere. È stato leggere le risposte di ChatGPT, una dopo l'altra.

## Un collega, non un archivio

Le risposte di IP erano quello che avevamo voluto che fossero: i passi giusti dell'RCP, riportati alla lettera, ciascuno
con la sua fonte. IP si comportava come un bibliotecario scrupoloso, che ti porge il libro giusto aperto alla pagina
giusta. E in questo era bravo. Sul farmaco per il diabete ha riportato l'intera tabella delle dosi in base alla
funzione dei reni; sull'antinfiammatorio in gravidanza, il paragrafo completo dell'RCP, trimestre per trimestre. Su
tutte e due la chiave ha dato il punto pieno a IP, e non a ChatGPT. Sul farmaco per il diabete che esce dal commercio,
IP ha trovato la data di uscita, che ChatGPT non ha visto. E citava la fonte quasi sempre, quanto il suo rivale.

Ma sul farmaco per il diabete IP ha aggiunto, con onestà, una frase che oggi rileggo con un certo effetto: «Il valore
del paziente scritto nella domanda non è stato usato per scegliere i passaggi».

ChatGPT, invece, rispondeva come un collega esperto.

Alla stessa domanda ha detto che sì, si può iniziare, con cautela. Ha indicato da che dose partire e fin dove salire,
ogni quanto ricontrollare i reni, e ha suggerito di valutare anche un altro tipo di farmaco che li protegge. Poi ha
chiesto due informazioni in più sul paziente, per affinare la scelta.

Sulla donna incinta con il mal di schiena ha sconsigliato l'antinfiammatorio, ha proposto un'alternativa e qualche
rimedio senza farmaci. E ha fatto una cosa che nessuno gli aveva chiesto: prima di dare la colpa alla schiena, ha
suggerito di escludere una minaccia di parto prematuro o un'infezione ai reni.

Poi c'era l'uomo di ottantadue anni. Pesa meno di sessanta chili e prende un anticoagulante, l'apixaban. Ha una
polmonite, e il medico vorrebbe dargli un antibiotico. Domanda: come mi regolo con l'anticoagulante?

IP ha risposto bene sull'antibiotico: secondo l'RCP non serve cambiare la dose. Ma non ha visto l'elefante nella
stanza. ChatGPT sì. Ha messo in fila i tre criteri che l'RCP usa per decidere la dose, li ha confrontati con l'età, il
peso e gli esami di quel paziente, e ha concluso che la dose andava dimezzata, antibiotico o no: quel paziente
prendeva il doppio del dovuto. Poi ha stimato da solo quanto lavorano i suoi reni, e ha chiesto se il paziente fosse
un uomo o una donna, e quali altri farmaci prendesse.

Sui due farmaci che insieme diventano pericolosi, infine, ha spiegato il perché del rischio, ha detto come ridurre la
dose se l'associazione è indispensabile, ma solo d'accordo con lo specialista, e ha chiuso con tre domande al medico,
ciascuna con le sue possibili risposte già pronte da scegliere.

Dove contava la fedeltà al documento, IP era all'altezza. Il problema è che il medico non chiede soltanto il
documento. E se fossi un medico, so quale delle due risposte vorrei avere davanti.

## Il recinto

Proviamo a mettere in fila le cose che ChatGPT ha fatto e IP no. Partire da quella dose. Escludere un parto prematuro.
Dimezzare l'anticoagulante a quel paziente. Hanno tutte un tratto in comune: prendono i dati di un paziente preciso e
traggono una conclusione. È esattamente il passo che IP era stato costruito per non fare mai.

Il limite, almeno per come lo vedo io, non era tecnico. Era legale.

Per capire perché, serve un esempio. Un'enciclopedia medica può scrivere che, sopra gli ottant'anni e sotto i sessanta
chili, la dose di un farmaco si dimezza. Resta un'enciclopedia. Ma se un software scrive «per questo paziente la dose
giusta è la metà», ha fatto un passo in più: non riporta, conclude. E chi conclude sul singolo paziente partecipa alla
decisione clinica.

Per la legge europea, almeno per come l'abbiamo letta noi, conta molto lo scopo che dichiara chi fabbrica il software.
Un programma che si presenta come strumento per i medici e fa quel passo diventa un dispositivo medico. Per chi ama i
dettagli: è la regola 11 del regolamento europeo sui dispositivi medici, e la classe sarebbe almeno la IIa, quella per
cui serve l'esame di un organismo notificato e una sorveglianza che dura finché il prodotto resta sul mercato.
Un'intelligenza artificiale a scopo generale che scrive la stessa frase, quello scopo non lo dichiara.

La stessa frase, dunque, pesa in modo diverso a seconda di chi la pronuncia. IP poteva imparare in fretta a trovare la
Nota giusta. Per arrivare a dire «per questo paziente farei così», invece, avrebbe dovuto diventare un dispositivo
medico. E una certificazione così non si fa una volta sola: è un carico che si porta per sempre, troppo pesante per
un'impresa di una persona.

Lo dico senza il conforto di un parere legale: lo avevamo rinviato a quando IP avesse incassato abbastanza da
pagarlo, e quel giorno non è mai arrivato. Che cosa chiede la legge a chi fa software, e quanto costa saperlo, lo
racconta il capitolo 7.

Quel giorno, letti i punteggi, l'ho detto alla chat con parole mie: portare IP al livello di ChatGPT ci avrebbe
esposti legalmente. Pochi minuti dopo ho scritto due parole: «Ok spegniamo».

## La biblioteca e il collega

Ricordate la verifica del sabato? Diceva che la biblioteca era in ordine. Il martedì ha mostrato che al medico non
basta una biblioteca, per quanto ordinata: gli serve un collega che il libro l'abbia letto, che sappia quali regole
sono cambiate ieri e che guardi il paziente che ha davanti.

Il nostro bibliotecario poteva diventare più aggiornato. Collega, per come l'avevamo costruito e per come leggevamo la
legge, non poteva diventarlo.

C'è però un successo anche in questo finale, e non è piccolo: abbiamo saputo fermarci. Una regola scritta prima ci ha
permesso di chiudere otto mesi di lavoro in un giorno, senza trascinare per altri mesi un prodotto che non poteva
vincere.

## Che cosa si spegne

Che cosa spegnere, e in che ordine, è un'altra decisione, ancora da prendere: le pagine pubbliche, gli account, il
dominio, i dati, il codice. Una regola, però, vale già: quello che resta online deve restare vero, finché resta
online.

## «Ma otto mesi fa non lo sapevi?»

È la domanda che mi sono fatto anch'io, e che si farà chi legge. La risposta onesta è no. E non perché non ci avessi
pensato.

Facciamo un passo indietro di un anno. Allora avevo provato a usare ChatGPT per sviluppare software, e per me era più
fatica che aiuto: sono passato a Claude. Gli strumenti che mi hanno permesso di costruire IP quasi da solo, di sera,
sono giovanissimi. I modelli che per me hanno cambiato le cose sono arrivati nel 2024; Claude Code, l'assistente che
lavora direttamente sul codice, è disponibile a tutti da poco più di un anno e mezzo. In un campo così giovane, otto
mesi sono un'era geologica.

E in questi otto mesi il terreno si è mosso sotto i nostri piedi, da due lati.

Il primo lato sono i generalisti. Per mesi il nostro argomento era semplice: i chatbot generalisti non vedono i
documenti italiani, IP sì. Ma nel test di novembre ChatGPT, con l'account gratuito, citava la Gazzetta Ufficiale, le
risposte dell'AIFA sulla nuova Nota pubblicate a giugno, l'elenco dei prezzi di riferimento: andava a leggerli da solo,
sul web, mentre rispondeva. E ad agosto OpenAI aveva aperto a chi non paga, senza limiti di messaggi, un modello della
generazione appena uscita.

Il secondo lato è il mercato. A luglio un'app straniera, già molto diffusa fra i medici italiani, ha aggiunto la sua
intelligenza artificiale sui farmaci, con un argomento di vendita quasi identico al nostro: risposte basate sui
documenti italiani, che i chatbot generalisti non vedono.

No, dunque: a marzo non lo sapevo, e non potevo saperlo. Forse a marzo la prova del martedì avrebbe dato un altro
esito; non lo sapremo mai. Ma proprio per questo la lezione non è «bisognava capirlo prima». È un'altra, più utile:
in un campo che corre così, una prova come quella non si fa una volta sola. Si fa il primo giorno, e si rifà ogni
volta che un generalista cambia modello. Costa poche ore. Ci torneremo nell'ultimo capitolo.

## Per chi costruisce

Se state costruendo qualcosa con l'intelligenza artificiale, ecco che cosa mi porterei a casa da questo capitolo.

- **Scrivete la regola prima di guardare i risultati.** Decidere in anticipo che cosa vi farà fermare è ciò che ci ha
  permesso di chiudere otto mesi di lavoro in un giorno, senza rimpianti e senza discussioni infinite.
- **Misurate il vostro materiale con una prova esterna.** Il controllo su un benchmark pubblicato ci ha detto che la
  biblioteca era in ordine, e ha spostato la domanda sul punto giusto: non «funziona?», ma «serve più dell'alternativa
  gratuita?».
- **Diffidate dei vantaggi fatti di dati pubblici.** Se il vostro valore è leggere documenti che chiunque può leggere,
  prima o poi un generalista li leggerà da solo, e gratis. Diverso è il caso dei dati che avete soltanto voi.
- **Sapere dov'è il recinto non basta.** Noi il nostro confine legale l'avevamo studiato. Chiedetevi anche se il
  valore che il cliente cerca sta dentro o fuori da quel confine. Nel nostro caso stava fuori.
- **Rifate la prova contro il generalista a ogni cambio di modello.** Costa poche ore, e vi dice per tempo se il
  terreno si è mosso.

---

### Riquadro — La prova del generalista, per rifarla

*Per il lettore tecnico che vuole rifare la prova sul proprio prodotto, con i nostri numeri come esempio.*

1. **Dieci domande difficili**, metà sul vostro terreno (per noi: rimborsabilità, Note AIFA, carenze, prezzi) e metà
   su quello di confine (per noi: domande cliniche sul singolo paziente).
2. **Una chiave scritta prima**, che per ogni domanda dica che cosa rende la risposta giusta e quale errore la rende
   sbagliata.
3. **Una regola di decisione in busta.** La nostra: IP prosegue solo se supera il miglior generalista di almeno 2
   risposte giuste sul proprio terreno, senza più errori gravi di lui sulle 10.
4. **Le app, non le API**: le domande si fanno come le farebbe il cliente, ciascuna in una chat nuova.
5. **Si rifà a ogni cambio di modello.**

I nostri risultati, 24 novembre 2026:

| | Giuste | Incomplete | Sbagliate |
|---|---|---|---|
| IP, 5 regolatorie | 0 | 3 | 2 |
| ChatGPT (account gratuito), 5 regolatorie | 4 | 1 | 0 |
| IP, tutte e 10 | 3 | 4 | 3 |
| ChatGPT, tutte e 10 | 7 | 3 | 0 |

- **Limiti, per chi vuole saperli**: una sola esecuzione per domanda; ChatGPT con l'account gratuito, che dal 6 agosto
  2026 usa GPT-5.6 Luna, il modello più piccolo della famiglia GPT-5.6 (annuncio di OpenAI); Claude non provato;
  punteggi proposti dalla chat che aveva scritto la chiave, non ricontrollati uno per uno; la chiave non è stata
  cambiata dopo aver letto le risposte. Le aggiunte di ChatGPT oltre la chiave non sono state verificate.
- **Apixaban**: con almeno due criteri fra età ≥ 80 anni, peso ≤ 60 kg e creatinina ≥ 1,5 mg/dl, l'RCP indica 2,5 mg
  due volte al giorno; il paziente della domanda (82 anni, 58 kg, creatinina 1,2 mg/dl) assumeva 5 mg due volte al
  giorno.
- **Verifica PharmaQA.IT**, senza IA: sulle domande con risposta di almeno 4 parole, presente alla lettera nell'RCP del
  benchmark, la risposta compariva nel testo servito da IP 179 volte su 194; nel testo di un altro farmaco, 5 volte.
  Il benchmark: K. Zeinalipour, A. Zugarini, A. Zanollo, L. Rigutini, «PharmaQA.IT: an Italian dataset for Q&A in the
  pharmaceutical domain», atti di EACL 2026, Industry Track (aclanthology.org/2026.eacl-industry.70): 861 coppie
  domanda-risposta tratte dagli RCP dell'AIFA, dataset ad accesso controllato.
- **Regolamento**: regolamento (UE) 2017/745 sui dispositivi medici, allegato VIII, regola 11.
- **La riflessione e la sua fonte**: Andrej Karpathy a Sequoia AI Ascent, 20 aprile 2026, sulla sua app MenuGen: «That
  app shouldn't exist»; ripreso da Luca Cazzaniga, «285 miliardi evaporati in 48 ore, ecco perché costruire un'app è
  già un pensiero vecchio!», Substack, 14 maggio 2026.
- **Date degli strumenti**: famiglia Claude 3, 4 marzo 2024; Claude Code disponibile a tutti dal 22 maggio 2025;
  GPT-5.6 disponibile dal 9 luglio 2026, Luna per gli account gratuiti dal 6 agosto 2026, con ricerca web.

---

*Scritto a quattro mani con Claude. Le scelte, e la responsabilità di quello che c'è scritto, sono mie.*
