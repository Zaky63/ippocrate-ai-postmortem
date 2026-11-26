# 7. Che cosa chiede la legge a chi fa software, oggi

## Anche un carretto ha bisogno di una licenza

Torniamo per un momento al carretto dei gelati del primo capitolo. Prima di uscire in strada, anche il gelataio più
bravo deve fare qualcosa che nessun cliente vedrà mai: chiedere una licenza, scrivere un piano per l'igiene, sapere
dove può fermarsi e dove no. Il gelato è la parte che si vede. Le carte sono la parte che lo rende possibile.

Con il software succede lo stesso, e da qualche anno molto più di prima. Chi oggi costruisce un programma che tocca la
salute e che usa l'intelligenza artificiale incontra, prima ancora del primo cliente, una piccola folla di norme: la
protezione dei dati, le regole europee sull'intelligenza artificiale, quelle sui dispositivi medici, la responsabilità
per i danni e, nel nostro caso, perfino le regole sulla pubblicità dei farmaci. Ognuna chiede qualcosa: un documento,
una scelta, a volte una sola frase, ma in un punto preciso della pagina.

Questo capitolo racconta come abbiamo attraversato quella folla, quasi da soli, in sei settimane di sere. Non è un
manuale di diritto e non è un parere: è la mappa come l'abbiamo letta noi, con le scelte che abbiamo fatto e quello
che ci è costato.

## «Meglio una documentazione forse imperfetta che il nulla»

All'inizio di ottobre la vetrina stava per aprire, e le carte erano ferme alle bozze di primavera. Il piano era
semplice: chiedere subito i preventivi a un legale e dargli l'incarico a fine lavori, con il materiale già pronto.

Il materiale, appunto, andava preparato. Ai primi di ottobre ho chiesto alla chat di scrivere i documenti in attesa
del legale, con una frase che è diventata il motto di quel mese: «meglio una documentazione forse imperfetta che il
nulla».

Pochi giorni dopo, un sabato sera, abbiamo fissato il metodo. Il punto di partenza l'ho dettato così: la
documentazione deve descrivere il prodotto finale, non quello di oggi. «Se per legge la retention è di 45 giorni e noi
l'abbiamo a 60, compila la doc legale con 45, poi segna le modifiche da fare e le facciamo».

Da lì sono nate poche regole, semplici da dire. Dove la legge fissa un requisito, il documento scrive il requisito.
Dove lascia la scelta a noi, per esempio per quanto tempo conservare il testo di una domanda, la chat propone un valore
e io lo ratifico. Ogni differenza fra quello che il documento promette e quello che il sistema fa finisce in una lista
di modifiche da fare. E un testo va sul sito solo quando quelle modifiche sono fatte: una bozza può precedere il
sistema, una pagina pubblicata no.

L'ultima regola è quella che, credo, vale di più per chi lavora con l'intelligenza artificiale. Per cercare le norme
usavamo un motore di ricerca giuridica basato sull'IA, e funzionava bene: nelle prove a risposta nota trovava i passi
giusti, e una sentenza che non aveva non se la inventava. Ma bastava poco per sbagliare. Cercando una sentenza della
Corte di giustizia per numero e anno, una volta ce ne restituì un'altra, del tutto diversa. Così la regola diventò
questa: lo strumento trova, il testo ufficiale conferma. Una citazione era «verificata» solo dopo il confronto,
carattere per carattere, con il testo scaricato da EUR-Lex, da Normattiva o dal sito del Garante. A metà novembre il
registro delle fonti contava più di cento righe, ciascuna con l'indirizzo ufficiale e il passo copiato da lì.

Il motivo era anche economico. Il legale, quando fosse arrivato, avrebbe ricevuto un pacchetto completo, con le fonti
già controllate, e avrebbe speso il suo tempo sul giudizio, non sulla ricerca della norma. Il tempo di un legale è il
suo prezzo.

Vediamo allora che cosa chiede la legge, una norma alla volta.

## Le domande dei medici sono dati sanitari

La prima è la più conosciuta: il regolamento europeo sulla protezione dei dati, il GDPR. Tutti pensano agli avvisi
sui cookie. Per noi il cuore era altrove: nel testo delle domande.

Un medico scrive: «82 anni, insufficienza renale stadio 4, warfarin». Non c'è un nome, eppure è la descrizione della
salute di una persona vera. Per la legge i dati sulla salute sono una categoria particolare, protetta più delle altre.
Abbiamo scelto di trattare il testo delle domande per quello che poteva essere, un possibile dato sanitario, e da
questa scelta è discesa una catena di documenti: il registro dei trattamenti, l'informativa, le istruzioni per chi
tratta i dati, la procedura per le richieste degli interessati, quella per le violazioni (che vanno notificate al
Garante entro settantadue ore), la politica di backup, gli accordi con i fornitori del server e dell'intelligenza
artificiale.

Il documento più impegnativo è stato la valutazione d'impatto, la DPIA. È un obbligo di chi tratta i dati, non del
legale, e per un'IA che legge testi che possono contenere dati sanitari è con ogni probabilità dovuta. L'abbiamo
scritta noi, a fine ottobre, con una regola severa: fra le misure in essere si scrive solo quello che è stato
accertato nel sistema, con il riferimento che lo prova; il resto va fra le misure pianificate.

E la DPIA ha fatto quello che deve fare: ci ha fatto vedere cose che non avremmo visto. Le condizioni del fornitore
del modello dicevano che una memoria temporanea, attiva per impostazione, poteva tenere il testo di una richiesta fino
a un giorno. Quell'«82 anni, warfarin» sarebbe rimasto lì per ventiquattro ore, anche se noi non l'avessimo conservato.
Fra le misure decise c'è stato spegnerla. Un'altra era più semplice e forse più utile: accanto alla casella in cui il
medico scrive, una riga che prima stava solo nei termini d'uso, che il medico non vede mentre scrive: «Non inserisca
dati che identifichino il paziente.»

C'è poi un successo che mi è caro. Una domenica di ottobre ho proposto di scrivere nella documentazione che IP era
«privacy by design» e «security by design». La chat ha risposto che un'etichetta così la può scrivere chiunque, e che
vale solo con le prove accanto. Così il paragrafo dell'informativa è diventato un elenco di fatti, ciascuno
controllabile: le ricerche nelle schede pubbliche non si memorizzano; i registri degli accessi al sito troncano gli
indirizzi IP; le visite si contano senza cookie e senza strumenti di tracciamento; nessun consenso è preselezionato;
nome ed email del medico non arrivano mai al modello. E nelle nostre regole interne è entrata una frase che rifarei identica: ogni
dato nuovo parte dalla domanda «ci serve davvero?», e la proprietà non si dichiara, si prova con un test che
fallirebbe se il codice la tradisse. Il contatore delle visite, per esempio, aveva un test che falliva se il codice
avesse letto l'indirizzo di chi visitava.

L'ultima domanda di questa famiglia è nuova, e chi sviluppa con l'IA se la farà sempre più spesso: lo strumento con
cui scrivo il codice diventa un mio fornitore? Claude Code lavorava sul nostro server con un abbonamento personale,
senza un accordo sul trattamento dei dati. Abbiamo scelto la strada più semplice: Claude Code non legge dati personali.
Sul server vede configurazioni e numeri aggregati; i lavori che richiedono dati personali li faccio io, a mano. Anche
i numeri di questo studio sono stati estratti così: conteggi, senza un solo indirizzo.

## Dire quando parla una macchina

La seconda norma è il regolamento europeo sull'intelligenza artificiale, l'AI Act. Per un prodotto come il nostro
contava soprattutto un articolo, il 50, che dal 2 agosto 2026 chiede due cose. La prima: chi usa un sistema di IA deve
sapere che sta parlando con una macchina. Era facile: la consultazione mostrava sempre l'avviso, e ogni risposta
diceva se a scriverla era stata l'intelligenza artificiale. La seconda è più difficile: i testi generati devono
essere marcati in un formato leggibile da un computer, e riconoscibili come artificiali. Per chi era già sul mercato,
il termine era il 2 dicembre 2026. E un decreto italiano di ottobre ha fissato le sanzioni: per le piccole imprese,
fino al minore fra quindici milioni di euro e il tre per cento del fatturato mondiale.

La soluzione ovvia sarebbe una filigrana nel testo. Non potevamo applicarla. Le filigrane per il testo lavorano mentre
il modello sceglie le parole, e il modello che usavamo era un servizio di Google che quel passaggio non lo espone.
Una filigrana aggiunta dopo avrebbe cambiato parole in risposte che riportano alla lettera le righe del foglio
ufficiale del farmaco. E rende poco proprio sulle risposte fattuali: «Controindicato in gravidanza» non lascia al
modello parole fra cui scegliere, che è il posto dove la filigrana si scrive.

Invece di chiedere al legale, abbiamo letto noi i testi, la norma, le linee guida della Commissione e le pagine di
Google, e abbiamo costruito l'altra metà dell'obbligo: la rilevazione. Un registro di verifica conservava, per ogni
risposta composta dal modello, un'impronta crittografica di ogni frase che non riportava il foglio ufficiale alla
lettera: niente testo, nessun identificativo, solo impronte. E una pagina pubblica, «Verifica un testo», diceva a
chiunque quante frasi di un testo venivano da noi. È entrata in esercizio il 14 novembre, quasi tre settimane prima della scadenza.
La nota che la accompagna dice di sé: «È una lettura dei testi, non un parere: dice che cosa facciamo, perché, e dove
la nostra posizione è debole». È il tono che userei per ogni documento di questo tipo.

## Quando un software diventa un dispositivo medico

La terza norma è la più pesante, e anche la più sottile: il regolamento europeo sui dispositivi medici. Come
raccontato nel primo capitolo, un software che fornisce informazioni usate per decidere una terapia è, di regola,
almeno di classe IIa. Vuol dire un organismo notificato che lo certifica, un sistema di qualità, una sorveglianza dopo
l'immissione sul mercato.

Le linee guida europee sulla qualificazione del software portano un esempio che, a rileggerlo oggi, fa
effetto. Fra i software che sono dispositivi medici c'è quello che analizza i dati di un singolo paziente per
suggerire aggiustamenti della dose, o segnalare possibili interazioni, nei pazienti con insufficienza renale. È, quasi
parola per parola, la domanda che un medico fa a un'IA generalista.

Che cosa un software sia lo decide anzitutto la sua destinazione d'uso, cioè quello che il fabbricante dichiara. Ma
una sentenza della Corte di giustizia del luglio 2026 ha aggiunto un tassello: la dichiarazione del fabbricante è un
elemento importante, non l'unico, e conta anche che cosa il prodotto fa davvero. Come l'abbiamo letta noi: le parole
sono necessarie, ma non bastano. Su questo confine IP è stato costruito (capitolo 5), e su questo confine passa
l'asimmetria del capitolo 6.

## Chi paga se qualcosa va storto

La quarta norma arriva adesso. Con la nuova direttiva europea sulla responsabilità da prodotto, per i prodotti immessi
sul mercato dopo il 9 dicembre 2026 anche il software è un prodotto, compreso quello fornito come servizio, e chi
fornisce un sistema di IA è trattato come un fabbricante. Risponde dei danni senza bisogno che si provi la sua colpa,
morte e lesioni comprese, e verso il danneggiato non può escludere la sua responsabilità con una clausola. Il governo
ha approvato a fine ottobre il decreto che la recepisce in Italia. IP si è spento prima di quella data; chi lancia oggi
ci entra in pieno.

Resta una domanda aperta, che avremmo portato al legale: la direttiva dice che le informazioni non sono un prodotto.
Una risposta composta da un modello è software o informazione?

Accanto alla direttiva c'è una legge italiana, in vigore da settembre, che chi costruisce con l'IA dovrebbe leggere
per intero. Quando qualcuno chiede il risarcimento di un danno causato usando un sistema di IA, il giudice può ordinare
di esibire le prove su come il sistema funziona: i registri, la gestione dei rischi, la documentazione tecnica. Se non
le esibisci, i fatti allegati da chi chiede il risarcimento si danno per ammessi. E se il danno viene dalla violazione
di un obbligo dell'AI Act, il nesso fra la violazione e il danno si presume, salvo prova contraria.

È qui che le carte smettono di sembrare burocrazia. Il nostro registro delle decisioni, che una volta chiusa una voce
non si tocca più, a noi serviva per lavorare. Davanti a un giudice sarebbe stato la nostra memoria.

## Un farmaco non si pubblicizza

La quinta norma era la più nostra. In Italia la pubblicità dei medicinali è definita dallo scopo: è pubblicità ogni
azione intesa a promuovere la prescrizione, la vendita o il consumo di un farmaco, e i farmaci con obbligo di ricetta
non si possono pubblicizzare al pubblico. Una pagina indicizzata da Google, con la scheda tecnica di un farmaco che
chiunque può leggere, è pubblicità?

Una domenica di fine ottobre l'ho chiesto alla chat così: se mostrare le caratteristiche dei farmaci fosse pubblicità,
le decine di siti che lo fanno, e la stessa AIFA, non sarebbero contro la legge? La risposta ha distinto due cose.
AIFA pubblica i fogli ufficiali perché la legge glielo impone, e questo non è un precedente per chi non è AIFA. Gli
altri siti ci dicono che il rischio di essere colpiti è basso, non che pubblicare sia lecito. L'argomento vero era
un altro: una sentenza della Corte di giustizia del 2011 dice che la riproduzione letterale e integrale del foglio
ufficiale, accessibile solo a chi la cerca, non è pubblicità vietata, nemmeno quando la fa l'azienda titolare del
farmaco. Chi cerca «bisoprololo scheda tecnica» ha cercato; chi non è interessato al bisoprololo non la vede.

Da lì sono venute le condizioni, scritte prima di aprire le schede ai motori di ricerca, all'inizio di novembre: testo
integrale e letterale, nessun prezzo, nessuna classe di rimborso, un'avvertenza in testa. Le pagine che invece
sceglievano parti del foglio in base alla domanda sono rimaste fuori dai motori: la selezione è proprio ciò che quella
sentenza distingue dalla riproduzione integrale. E per gli annunci a pagamento, mai il nome di un farmaco. Un annuncio
«Bisoprololo: scheda tecnica completa», comprato sulla parola «bisoprololo», lo vede chiunque cerchi il farmaco,
pazienti compresi. «Le schede tecniche AIFA, per il medico», comprato su «schede tecniche farmaci per medici» e diretto
alla home, pubblicizza il servizio.

Il rischio che restava l'ho accettato io, per iscritto, con le condizioni che avrebbero fatto cadere la scelta: se le
schede avessero cominciato a selezionare o a riordinare il testo, se vi fosse comparso un prezzo, se il progetto
avesse accettato pubblicità o finanziamenti dall'industria farmaceutica.

C'era infine il riuso dei fogli ufficiali. In primavera avevamo scritto ad AIFA con una PEC, presentando il progetto, e
la risposta era arrivata circa un mese dopo, a fine aprile, con una nota: i fogli si possono riusare, a condizione che
sia ben visibile una frase precisa, «Ippocrate AI ricorda che gli unici dati ufficiali sono quelli
pubblicati dalle autorità regolatorie nazionali ed europee di settore e/o sulle Gazzette Ufficiali». Quella frase era
su ogni pagina che riportava un foglio ufficiale. Chiedere direttamente all'autorità era costato una PEC e un mese di
attesa, e ci aveva dato una risposta scritta.

## Anche il nome ha un padrone

L'ultima voce è la più piccola, e la più facile da dimenticare. Una sera di novembre abbiamo cercato il nostro nome
nei registri dei marchi, attraverso una banca dati pubblica e gratuita. «ippocrate.ai» non era un marchio di nessuno.
Ma i marchi che contenevano «Ippocrate» o «Hippocrates» erano decine, e una parte stava proprio nelle classi del
software. Abbiamo deciso di non depositare nulla fino al parere del legale.

È una verifica che costa una sera, e che conviene fare il primo giorno, prima di affezionarsi a un nome.

## Il conto

A fine ottobre il pacchetto era quasi completo. Mancava il parere.

Il primo preventivo è arrivato sulle seicento euro, con l'oggetto ancora da precisare, e la spesa complessiva si
stimava già sopra i tremila. Così, la stessa domenica della domanda su AIFA, ho deciso: i pareri si rinviano a quando gli
incassi superano i mille euro al mese. Con incassi a zero, ogni euro dato al legale usciva dal margine del lancio, e
per noi l'IVA non si recuperava: era costo pieno. Nel frattempo i documenti si scrivevano e si approvavano in casa,
con il metodo di ottobre.

Intanto un secondo studio ci aveva proposto una videochiamata, e noi gli abbiamo chiesto il prezzo di tre pareri
scritti, uno per domanda, per sapere quanto sarebbe costato il giorno in cui fosse servito: la pubblicità dei
medicinali, la qualificazione come dispositivo medico, la responsabilità verso chi usa il servizio. La risposta è
arrivata all'inizio di novembre: quasi seimila euro, con spese, contributi e IVA. La domanda sul dispositivo medico,
da sola, valeva metà degli onorari. Il preventivo ha confermato la scelta.

## Il recinto, visto da vicino

Rileggendo oggi quelle sei settimane, la cosa che mi colpisce è questa: le carte non ci hanno fermato.

Le abbiamo scritte, verificate e in buona parte messe in esercizio. Informativa, termini e cookie erano online il
giorno in cui la vetrina si è accesa. La valutazione d'impatto era scritta e ratificata. Il registro di verifica dei
testi era in linea prima della scadenza. Le schede erano aperte ai motori di ricerca, con condizioni scritte. Più di
cento citazioni erano controllate sul testo ufficiale. Una ventina di documenti, nati la sera, dopo il lavoro.

Quello che ci ha fermato è un'altra cosa, e sta in una sola di quelle norme: la regola che trasforma un software che
ragiona sul paziente in un dispositivo medico. Il fascicolo ci diceva come restare in regola di qua dal recinto. Non
poteva dirci come attraversarlo. Attraversarlo voleva dire un organismo notificato, un sistema di qualità, una
sorveglianza continua: un'altra impresa, non un'altra sera di lavoro.

E non è una strada breve. Una software house italiana che produce una cartella clinica per i medici di famiglia lo
racconta sul proprio sito: ha firmato il contratto con l'organismo notificato nella primavera del 2024, ha consegnato
il fascicolo tecnico a febbraio del 2025, e a novembre del 2026 il suo modulo di supporto alle decisioni risulta
ancora in fase di classificazione in classe IIa. Quasi due anni dalla consegna delle carte, per un'azienda strutturata.

Restare di qua dal recinto, ma vicino al confine, come facevamo noi, ha un altro costo, che nessun preventivo mostra.
Il rischio non è solo la sanzione. Se per tre pareri scritti ci avevano chiesto quasi seimila euro, quanto sarebbe
costato un avvocato per difenderci da una contestazione? Per una grande azienda è una voce di bilancio. Per un
progetto portato avanti la sera, da una persona sola, è la fine del progetto.

È questa, per me, la lezione più amara del capitolo: davanti alla stessa legge, le grandi aziende partono
avvantaggiate. Hanno i soldi per gli avvocati, e il tempo per aspettare un organismo notificato.

È per questo che, nel primo capitolo, ho scritto che il limite era legale e non tecnico. Le carte si scrivono. Il
recinto no.

## Per chi costruisce

- **Fate l'inventario delle norme il primo mese.** Le carte si scrivono anche in sei settimane; ma sapere quali
  servono cambia il prodotto, e va saputo prima di costruirlo.
- **Scrivete i documenti per il prodotto che aprirà**, e tenete accanto la lista delle differenze fra quello che
  promettono e quello che il sistema fa oggi. Un testo si pubblica quando la lista che lo riguarda è vuota.
- **L'IA trova, il testo ufficiale conferma.** Una citazione giuridica si verifica sul testo scaricato dalla fonte
  ufficiale, mai sul riassunto di un modello.
- **Un'etichetta vale quanto le prove che le mettete accanto.** «Privacy by design» si dimostra con un elenco di fatti
  e con un test che fallirebbe se il codice la tradisse.
- **Tenete gli strumenti di sviluppo lontani dai dati personali.** Se l'assistente con cui scrivete il codice vede
  solo configurazioni e aggregati, la domanda sul fornitore non si pone.
- **Quando non potete fare ciò che la norma suggerisce, fate l'altra metà e scrivete perché.** Noi non potevamo
  marcare il testo; abbiamo costruito la rilevazione, e una nota che dice anche dove la nostra posizione è debole.
- **Trattate la documentazione come una prova.** Con le regole nuove sull'IA, in un processo il giudice può chiederla.
- **Portate al legale domande, non ricerche, e mettete in conto la parcella.** Per tre pareri scritti, l'ordine di
  grandezza è di qualche migliaio di euro: va nel budget prima del primo incasso, non dopo.
- **Pesate anche il costo di difendervi, non solo quello di mettervi in regola.** Se lavorate vicino al confine, la
  domanda da farsi non è solo «quanto è la sanzione?», ma «quanto costerebbe un avvocato, se qualcuno ci
  contestasse?». Per una piccola impresa può essere la cifra che decide.
- **Cercate il vostro nome nei registri dei marchi il primo giorno.** Costa una sera.

---

### Riquadro — Il fascicolo, per rifarlo

*Per il lettore tecnico: i documenti che abbiamo scritto, le norme da cui vengono, le date che contano. È la nostra
lettura dei testi al novembre 2026, non un parere legale.*

**I documenti, per tipologia**

| tipologia | documento | da dove viene l'obbligo |
|---|---|---|
| testi pubblici | informativa privacy | GDPR artt. 13–14 |
| | termini d'uso (il contratto con gli utenti registrati) | codice civile; Codice del consumo se l'utente è un consumatore |
| | cookie policy e avviso | Codice privacy (D.Lgs. 196/2003) art. 122 |
| | condizioni dell'abbonamento | codice civile; Codice del consumo se l'utente è un consumatore |
| | dichiarazioni pubbliche (destinazione d'uso, avvertenze, avviso d'uso dell'IA) | MDR (destinazione d'uso), AI Act art. 50 par. 1 |
| accountability GDPR (interni) | registro dei trattamenti | GDPR art. 30 |
| | valutazione sulla necessità della DPIA, poi la DPIA | GDPR art. 35 |
| | procedura per le richieste degli interessati | GDPR artt. 15–22 |
| | autorizzazione al trattamento e istruzioni | GDPR art. 29; Codice privacy art. 2-quaterdecies |
| | procedura per le violazioni dei dati | GDPR artt. 33–34 (notifica entro 72 ore) |
| | politica di backup, misure di sicurezza | GDPR art. 32 |
| contratti e fornitori | accordi di trattamento con hosting e fornitore del modello | GDPR art. 28 |
| regolatorio del prodotto | memo di qualificazione come dispositivo medico | MDR, Allegato VIII, regola 11; MDCG 2019-11 |
| | nota di conformità all'art. 50 | AI Act art. 50 par. 1 e 2 |
| | condizioni di riuso dei fogli ufficiali (RCP) | nota AIFA prot. 0057917 del 29/04/2026 |
| | registro delle fonti (104 righe al 15/11/2026) | metodo interno: ogni citazione confrontata col testo ufficiale |
| | lista delle modifiche da fare | metodo interno: gli scarti fra testo e sistema |
| impresa e proprietà | titolarità di codice e testi | un accordo scritto fra chi sviluppa e il titolare dell'impresa |
| | marchio e domini | ricerca su TMview; deposito rinviato |
| rapporti col legale | richiesta di preventivo, brief, quesiti | — |

**Le norme e le date**

| norma | che cosa chiede, in breve | date |
|---|---|---|
| GDPR (Reg. UE 2016/679) e Codice privacy | basi giuridiche, dati sanitari (art. 9), registro, DPIA, sicurezza, violazioni, fornitori | in vigore |
| AI Act (Reg. UE 2024/1689), art. 50 | par. 1: dire che si interagisce con un'IA; par. 2: testi generati marcati e rilevabili | dal 2/8/2026; par. 2 entro il 2/12/2026 per i sistemi già sul mercato |
| D.Lgs. 179/2026 | vigilanza sui sistemi di IA all'ACN; art. 50 sanzionato fino a 15 milioni di euro o al 3% del fatturato mondiale (per le PMI il minore dei due); per le violazioni lievi, ordine di eliminarle | in vigore dal 23/10/2026 |
| L. 132/2025, art. 7 | in sanità, il diritto di essere informati sull'uso dell'IA | in vigore dal 10/10/2025 |
| MDR (Reg. UE 2017/745), Allegato VIII regola 11 | software che informa decisioni diagnostiche o terapeutiche: almeno classe IIa, con organismo notificato | in vigore |
| MDCG 2019-11 rev. 1 (linee guida, non vincolanti) | esempio di dispositivo medico: «MDSW that analyse patient-specific data to suggest dosage adjustments or flag potential drug interactions for patients with kidney impairments» (Annex I, c.1) | giugno 2025 |
| Corte di giustizia, C-427/24 | la destinazione d'uso dichiarata è importante ma non l'unico elemento; contano anche le funzioni oggettive | 2/7/2026 |
| Reg. UE 2026/1744 | rinvia le regole dell'AI Act sull'alto rischio per i prodotti dell'Allegato I, MDR compreso | al 2/8/2028 |
| Dir. UE 2024/2853 | il software, anche come servizio, è un prodotto; responsabilità senza colpa; non limitabile per contratto verso il danneggiato; le informazioni non sono un prodotto | prodotti immessi sul mercato dopo il 9/12/2026; decreto di recepimento approvato dal Consiglio dei ministri il 28/10/2026 |
| D.Lgs. 160/2026, artt. 16–20 | danni da IA: esibizione delle prove sul funzionamento; fatti ammessi se non esibite; nesso causale presunto se si viola l'AI Act; la conformità, anche certificata, non esclude la responsabilità | in vigore dal 30/9/2026 |
| D.Lgs. 219/2006, artt. 113 e 148 | pubblicità dei medicinali definita dallo scopo; presso il pubblico, sanzione da 2.600 a 15.600 € | in vigore |
| Corte di giustizia, C-316/09, *MSD* | la riproduzione letterale e integrale dell'RCP, accessibile solo a chi la cerca, non è pubblicità vietata | 5/5/2011 |
| Corte di giustizia, C-530/20, *Euroaptieka* | la pubblicità può riguardare anche medicinali non determinati | 22/12/2022 |

**Il metodo, in sei regole**

1. I documenti descrivono il prodotto all'apertura, non quello di oggi.
2. Dove la legge fissa un requisito si scrive il requisito; dove lascia la scelta, si decide su un valore proposto.
3. Ogni scarto fra testo e sistema va in una lista di modifiche da fare.
4. Un testo si pubblica solo quando le modifiche che lo bloccano sono fatte.
5. Una citazione è «verificata» solo dopo il confronto meccanico con il testo ufficiale scaricato; lo strumento di
   ricerca basato sull'IA trova la fonte, non la verifica.
6. Al legale si chiede la revisione, con il pacchetto completo e il registro delle fonti allegato.

**Le domande che avremmo portato al legale**

La base giuridica per i dati sanitari nelle domande dei medici; il nostro ruolo rispetto ai dati dei pazienti che il
medico inserisce (titolare autonomo, o responsabile per conto del medico); il perimetro della DPIA; come scrivere la
destinazione d'uso; se la pubblicazione delle schede sia pubblicità dei medicinali; le clausole di responsabilità,
alla luce della direttiva del 2024; se depositare il marchio, dove e in quali classi.

**Il conto, in ordine di grandezza**

- Tre pareri scritti (pubblicità dei medicinali, dispositivo medico, responsabilità): circa 6.000 € con spese
  generali, contributo previdenziale e IVA; la domanda sul dispositivo medico vale metà degli onorari.
- Deposito di un marchio, tasse lette il 12/11/2026: in Italia circa 100 € per la prima classe; nell'UE, online,
  circa 850 € per una classe.
- Il tempo: sei settimane di sere, dalla prima bozza al registro di verifica in esercizio.
- Il tempo di una certificazione in classe IIa, da un caso pubblico italiano: contratto con l'organismo notificato il
  15/4/2024, fascicolo tecnico consegnato il 28/2/2025, modulo di supporto alle decisioni «in fase di
  classificazione in Classe IIa» alla lettura del 25/11/2026 (pagina del fabbricante).

**Il calendario**

| data (2026) | che cosa |
|---|---|
| 5 ottobre | i documenti si scrivono in casa, in attesa del legale |
| 10 ottobre | il metodo, in sei regole |
| 18 ottobre | «privacy by design» con le prove, nell'informativa e nelle regole interne |
| 19 ottobre | la vetrina si accende, con informativa, termini e cookie online |
| 25 ottobre | pareri rinviati a incassi oltre 1.000 € al mese; DPIA ratificata; Claude Code senza dati personali; l'avviso accanto alla casella delle domande |
| 30–31 ottobre | procedura per le violazioni e politica di backup; nota d'aggiornamento al memo sul dispositivo medico; nota sull'art. 50 |
| 2 novembre | il preventivo dei tre pareri, non commissionato |
| 5 novembre | le schede si aprono ai motori di ricerca, alle condizioni scritte |
| 12 novembre | la ricerca sul marchio |
| 14 novembre | il registro di verifica dei testi in esercizio |
| 24 novembre | IP si spegne |

---

*Scritto a quattro mani con Claude. Le scelte, e la responsabilità di quello che c'è scritto, sono mie.*
