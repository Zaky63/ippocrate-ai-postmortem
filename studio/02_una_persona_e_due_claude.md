# 2. Un'azienda di una persona e due Claude

Usare un'IA per sviluppare un progetto è meno facile di quanto si pensi. Per un progetto semplice o la demo di un
software, effettivamente è sufficiente scrivere un prompt (per i non addetti: le istruzioni che si scrivono in chat per
l'IA) abbastanza dettagliato di ciò che si vuole ottenere, e l'IA parte e rende reale la vostra idea.

Come alcuni di voi già sanno, una sessione con un'IA ha un limite in merito alla quantità di informazioni che può
conservare in memoria.

Per un progetto di ampio respiro è necessario aprire decine o centinaia di nuove sessioni.

## Il collega che dimentica

Immaginate di lavorare con un consulente geniale. Conosce i linguaggi di programmazione meglio di chiunque abbiate
incontrato, scrive in un'ora quello che a voi costerebbe una settimana, non si stanca mai. Ha un solo difetto: a ogni
incontro ha dimenticato tutto quello che vi siete detti la volta prima.

Lavorare con un'intelligenza artificiale su un progetto lungo è così. Ogni sessione nuova comincia da zero. E le
sessioni, per IP, non sono state poche: solo sul mio computer, dalla fine di settembre, Claude Code ne ha aperte più di
ottocento. A queste vanno aggiunte quelle sul server e le conversazioni con la chat, che non ho contato.

La domanda, allora, non era come far ricordare all'IA. Era come dare memoria a un progetto in cui chi lavora dimentica.
La risposta che abbiamo trovato si può dire in una riga: la memoria della sessione finisce, quella del progetto no. Il
progetto ricordava attraverso i file.

## Tre ruoli

Prima ancora dei file, però, servivano dei ruoli chiari. Ne abbiamo fissati tre, e li abbiamo chiamati, con poca
fantasia, Modello III.

Pensate a un cantiere. C'è l'architetto, che disegna e scrive le istruzioni; c'è l'impresa, che costruisce; c'è il
committente, che decide e firma. Da noi l'architetto era la chat: progettava, scriveva il codice, le istruzioni di
lavoro e i documenti, e proponeva ogni scelta con una soluzione predefinita. L'impresa era Claude Code: eseguiva, sul
mio computer e sul server, e salvava il lavoro nel repository. Il committente ero io: decidevo, ratificavo, e facevo
con le mie mani i passi più delicati, le scritture sui dati di produzione, i comandi da amministratore, i riavvii.

La divisione aveva un vantaggio che all'inizio non avevo previsto. Chi progetta non esegue, e chi esegue non decide.
Quando qualcosa andava storto, era facile capire dove: nel disegno, nell'esecuzione o nella decisione.

## Il registro che non si riscrive

Il cuore della memoria era il registro delle decisioni. A luglio, al quarto mese, era un unico file di oltre
settemila righe con un centinaio di decisioni. Accanto c'era il registro dei lavori da fare, con un problema
ancora peggiore: lo stato di ogni voce era scritto in tre punti diversi, e a volte i tre punti non concordavano. Una
voce poteva essere «risolta» nel titolo e «aperta» nel testo.

Per un'IA che deve leggere e modificare quei file, un documento enorme è il terreno più scivoloso: basta un passaggio
sbagliato per rovinare un pezzo che non si voleva toccare. Così in una sessione di luglio abbiamo rovesciato
l'impianto. Ogni decisione è diventata un file a sé, con la data nel nome, e una volta chiusa non si tocca più: se
cambiamo idea, si scrive una decisione nuova, o una nota in coda. Ogni lavoro da fare è diventato un file a sé, con lo
stato scritto in un punto solo e scelto da un elenco chiuso di parole. Gli indici, che permettono di leggere tutto con
uno sguardo, li genera uno script, che sa anche dire se l'indice salvato è rimasto indietro.

Abbiamo valutato anche strade più sofisticate: un database, un'altra intelligenza artificiale che riassumesse i
documenti alla chat, un motore di ricerca sui file. Le prime due le abbiamo scartate, la terza rimandata, con un
argomento che mi fa ancora sorridere: il principio di IP, riportare e non elaborare, valeva anche per la nostra documentazione. Alla chat serviva leggere il
testo così com'era, non un riassunto fatto da qualcun altro.

Con il tempo, ogni decisione ha preso anche una forma fissa: che cosa si decide, i presupposti, ciascuno con un esempio, le conseguenze, e
che cosa la decisione non decide. L'esempio è la parte che ho imparato ad apprezzare di più. Una regola astratta si
può approvare senza capirla; un esempio concreto no.

A fine novembre le decisioni registrate erano 541, le voci dei lavori 557, i referti delle misure circa 1.800.

## La data su ogni documento

C'è un altro dettaglio, piccolo, che consiglio a chiunque. Ogni documento che racconta come stanno le cose porta in
testa due righe: la data in cui è stato scritto e l'ultima decisione di cui tiene conto. Le chiamavamo data epistemica.

Serve a una cosa semplice: dire a chi legge quanto fidarsi. Una sessione nuova che apre un documento di due mesi prima
sa che può essere superato, e lo verifica prima di usarlo. Ci ha insegnato anche il caso opposto, meno ovvio: un
documento che si dichiara «da fare» mentre descrive qualcosa che è già stato fatto inganna quanto uno vecchio, perché
nasconde quello che resta davvero da fare.

E ogni sessione cominciava sempre con le stesse letture: il Vademecum con i paletti, l'indice delle decisioni,
l'indice dei lavori aperti, le regole di lavoro. Pochi file, piccoli, aggiornati: la memoria minima per non ripartire
da zero.

## Chiedere sulla logica, non sui dettagli

Con un'IA che propone tutto, il rischio opposto è diventare un timbro. A settembre è successo, e l'abbiamo scritto: in
una sola giornata la chat mi aveva chiesto di ratificare i nomi di tre contatori, il nome di una funzione, se una riga
malformata spezzasse una tabella. E, nella stessa giornata, la soglia di leggibilità delle tabelle che i medici
avrebbero visto. Le prime erano esecuzione; l'ultima era filosofia di prodotto. Chiederle allo stesso modo diluiva le
domande che contavano fra quelle che non contavano.

La regola è diventata questa: si chiede ratifica sulla logica, non sull'operativo. Che cosa vede il medico, che cosa
conta come vero, quanto si spende, che cosa si pubblica: questo lo decido io. Nomi, strutture, quale misura fare prima:
la chat procede con la sua scelta, ma la scrive nel file, con l'alternativa e il perché. Un default non dichiarato è
una decisione nascosta; un default dichiarato è esecuzione trasparente. E una frase che rifarei: un «ok» non si
aspetta, una scelta sì.

A ottobre ho fatto un passo in più: ho ratificato in anticipo i default della chat, con un limite di spesa di dieci
euro sul servizio di intelligenza artificiale per le misure. Restavano a me la spesa oltre quel limite, i passi sul
server e sui dati di produzione, il cambio di modello, i paletti, i testi che il medico legge come affermazioni del
sistema, e tutto ciò che non si può disfare. Il lavoro ha smesso di fermarsi a ogni passaggio, senza che perdessi il
controllo di ciò che contava.

## Le prove nel repository

Un'altra regola è nata da un errore di ordine pratico. A luglio alcuni referti, cioè le prove su cui poggiavano le
decisioni, vivevano in una sola copia sul server, fuori dal repository e dai backup. Le decisioni erano immutabili e
versionate; le loro prove no.

Da allora ogni referto entra nel repository nello stesso giro di lavoro in cui nasce. Le istruzioni di lavoro per
Claude Code, invece, sono effimere: servono finché il giro è aperto, poi si cancellano. L'abbiamo riassunto così: il
repository è l'archivio unico, il server è il posto dove il codice gira.

## Il ponte

Per mesi i due Claude hanno lavorato sullo stesso computer senza potersi parlare. La chat, la mente che progettava,
viveva in un'applicazione di Windows. Claude Code, le mani, viveva in un terminale Linux sullo stesso PC. Fra i due
c'ero io, a fare il postino: la chat scriveva le istruzioni, io le copiavo nel terminale, aspettavo, e riportavo
l'esito alla chat. Per un po' abbiamo usato una coda: la chat lasciava un file, e Claude Code ogni dieci minuti
andava a vedere se ce n'era uno nuovo. Funzionava, ma era una cassetta delle lettere.

L'idea che ha cambiato tutto, a metà ottobre, era semplice, e a pensarci bene geniale. La chat usava già un sistema
per collegarsi a strumenti esterni, lo stesso con cui leggeva i file del progetto: un protocollo aperto, che si chiama
MCP. Se attraverso quella presa la chat poteva leggere un file, perché non poteva anche avviare Claude Code? La chat ha
scritto da sé il pezzo che mancava: un piccolo server, un solo file in Python, senza nessuna dipendenza, che
l'applicazione della chat avvia dentro Linux. L'abbiamo chiamato cc-bridge, il ponte.

Da quel giorno la chat affida un lavoro a Claude Code con una riga, di solito «esegui le istruzioni di questo file»,
ne segue l'avanzamento e ne riceve l'esito: com'è andata, quanti passi, quanto sarebbe costato a prezzo di listino,
quanto dell'abbonamento ha consumato, e ogni comando che le regole di sicurezza hanno bloccato, con il motivo.

I dettagli, però, sono quelli che lo rendono una piccola opera d'ingegno.

Il primo è un limite scoperto misurando: una chiamata della chat a uno strumento esterno cade dopo sessanta secondi,
e il risultato va perso. Un lavoro di Claude Code può durare un'ora. Allora il ponte non aspetta mai più di
cinquanta secondi: se il lavoro non è finito, restituisce «ancora in corso» con un numero, e la chat torna a chiedere.
Ogni volta riceve solo le attività nuove. Nel frattempo Claude Code va avanti per conto suo, in un processo che
sopravvive anche se si chiude l'applicazione della chat.

Il secondo è la sicurezza. A ogni lavoro la chat sceglie quanta libertà dare a Claude Code: solo leggere, modificare i
file, oppure anche lanciare comandi, con il controllo di sicurezza di Claude Code che blocca ciò che va oltre la
richiesta. La libertà totale è spenta, e la può accendere solo chi installa il ponte. Il ponte lavora solo nelle
cartelle che gli ho indicato. E c'è una regola che ho trovato saggia: dopo un rifiuto, niente varianti. Se un comando
è stato bloccato, non lo si riprova travestito; decido io.

Il terzo è la continuità. Una sessione avviata dalla chat la posso riprendere io nel terminale, e una che ho aperto io
la può riprendere la chat. La chat può anche rileggere che cosa è successo in una sessione: «che cosa ho fatto ieri
sera?» ha finalmente una risposta.

E il quarto, il più prosaico: il ponte usa il mio abbonamento, non il pagamento a consumo. Lavorare così non costava
un euro in più.

Non ho più fatto il postino. La ratifica è rimasta mia; il trasporto no. Restano a me, per scelta, i lavori lunghi,
quelli oltre i venti minuti, che lancio dal mio terminale. Tutto il resto passa dal ponte, compresa buona parte di questo
studio: i conteggi, le ricerche nei documenti, le verifiche dei numeri che leggete in queste pagine sono stati chiesti
dalla chat a Claude Code, in queste sere di novembre, decine di volte. È fra gli strumenti che pubblichiamo.

## Quando l'IA dice di aver letto

Resta la difficoltà più insidiosa, e la scrivo perché chi comincia oggi la incontrerà di sicuro. Un'IA scrive con la
stessa sicurezza quello che ha letto e quello che immagina. Può dire che il sistema «fa» una cosa che è soltanto
progettata, o attribuire un numero a un documento che non ha aperto.

A noi è successo più volte: in una sola sessione d'agosto tre volte, e due di queste in documenti destinati a un
valutatore esterno. La regola che ne è venuta sta
nelle nostre regole interne: mai affermare che il sistema fa qualcosa senza averlo letto nel codice, perché una
proprietà progettata non è una proprietà accertata. In pratica: ogni affermazione con il suo file e la sua riga, e ogni
numero con la data della misura e da dove viene.

Le altre lezioni sugli strumenti le abbiamo raccolte in un documento a parte, con un titolo onesto: lezioni e casi. La
più istruttiva è quella raccontata nel capitolo 10: una regola che si viola due volte non sta nel posto sbagliato, sta
nella forma sbagliata, e va trasformata in uno strumento.

## Che cosa rende

Alla fine di otto mesi, il repository contava quasi 2.800 salvataggi del lavoro, fatti da una persona che di giorno fa
un altro mestiere, con due intelligenze artificiali al fianco. Senza questo metodo IP non sarebbe esistito. Con questo
metodo è esistito, ha funzionato, e quando è arrivato il momento di fermarsi la decisione è stata scritta come tutte le
altre: un file nuovo, con i suoi presupposti e il suo esempio.

## Per chi costruisce

- **La memoria del progetto sta nei file, non nella sessione.** Ogni sessione nuova deve poter ripartire leggendo
  pochi file piccoli e aggiornati.
- **Una decisione, un file, che non si riscrive.** Se cambiate idea, scrivete una decisione nuova: la storia resta
  leggibile, e il «perché» di ieri non sparisce.
- **Lo stato in un punto solo, con un vocabolario chiuso.** Due punti che dicono lo stato prima o poi si contraddicono.
- **Indici generati da uno script**, con un controllo che dica se sono rimasti indietro.
- **Separate i ruoli**: chi progetta, chi esegue, chi decide.
- **Chiedete ratifica sulla logica, non sui dettagli**, e fate scrivere i default nel file, con l'alternativa e il
  perché.
- **Delegate con limiti scritti**: una spesa massima, la produzione, l'irreversibile.
- **Mettete la data epistemica su ogni documento** che racconta come stanno le cose.
- **Le prove nel repository, nello stesso giro in cui nascono.**
- **Non credete a un'IA che dice di aver letto**: fatele citare file e riga, e numeri con data e provenienza.

---

### Riquadro — Il kit della memoria, per rifarlo

*Per il lettore tecnico: la struttura che abbiamo usato. È nata per un progetto con un'IA, ma vale per qualunque
progetto lungo con più persone che si alternano.*

**Le cartelle**

| cartella | che cosa contiene | regola |
|---|---|---|
| `docs/decisions/` | una decisione per file, `D-AAAA-MM-GG-tag.md` | immutabile dopo la chiusura; rettifiche con una voce nuova o una nota in coda |
| `docs/backlog/` | un lavoro per file, `IP-FIX-NN.md` | mutabile finché il lavoro è vivo; lo stato solo nell'intestazione |
| `docs/report/` | referti e verbali delle misure | entrano nel repository nello stesso giro in cui nascono |
| `docs/BR/` | istruzioni di lavoro per Claude Code e passaggi di consegne | fuori dal repository, effimere |
| `INDEX.md` in ciascuna delle prime due | gli indici | generati da uno script, mai a mano |

**La voce di decisione**

- intestazione: `id`, `date`, `title`, e se serve `supersedes` e i lavori collegati;
- due righe in testa: data epistemica e ultima decisione di cui tiene conto;
- corpo: origine (chi ha detto che cosa), decisione, presupposti con un esempio ciascuno, conseguenze, che cosa non
  decide;
- una scelta presa per delega si dichiara come tale.

**Il vocabolario dello stato** (chiuso, controllato dallo script): `open`, `in-progress`, `resolved`, `closed`,
`deferred`, `frozen`, `superseded`. Gravità: `alta`, `media`, `bassa`.

**Le letture di inizio sessione**: i paletti, l'indice delle decisioni, l'indice dei lavori, le regole di lavoro; più,
secondo il fronte, il documento sul flusso logico o quello sul flusso dei dati.

**Le regole della ratifica**

| che cosa | chi decide |
|---|---|
| che cosa vede il medico, che cosa conta come vero, che cosa si pubblica, la direzione | Maurizio |
| nomi, strutture, ordine delle misure, strumenti, forma dei controlli | la chat, con il default scritto nel file |
| spesa oltre 10 € per le misure, passi sul server, dati di produzione, cambio di modello, paletti, testi letti dal medico, l'irreversibile | Maurizio, anche dopo la delega di ottobre |

**Gli strumenti** (da pubblicare, ripuliti): il generatore degli indici con il controllo `--check`; i due script di
salvataggio con il controllo sul numero di file attesi; le istruzioni per Claude Code su come si scrive una voce; il
ponte fra la chat e Claude Code (capitolo 10).

**Il ponte, cc-bridge, in breve**

| che cosa | come |
|---|---|
| che cos'è | un server MCP in un solo file Python, senza dipendenze, che Claude Desktop avvia in WSL |
| gli strumenti per la chat | `cc_run` (avvia o riprende un lavoro), `cc_status` (avanzamento ed esito), `cc_cancel` (ferma), `cc_sessions` e `cc_transcript` (sessioni recenti e loro contenuto), `cc_info` (diagnostica) |
| come lancia Claude Code | `claude -p` in modalità non interattiva, con l'uscita in streaming, in un gruppo di processi proprio che sopravvive al riavvio di Claude Desktop |
| le attese | al massimo 50 secondi per chiamata, perché le chiamate inoltrate da Claude Desktop cadono a 60 (misurato il 15/10/2026); oltre, «in corso» e un identificativo, poi `cc_status` |
| le modalità | `plan` (sola lettura), `edit` (modifica file), `auto` (modifica e comandi, col classificatore di sicurezza di Claude Code), `full` (spenta per impostazione) |
| i limiti | cartelle ammesse fissate all'installazione; tetto alla modalità; due lavori contemporanei; comandi negati elencati con il motivo |
| l'abbonamento | toglie la chiave API dall'ambiente di Claude Code, così il lavoro resta sull'abbonamento |
| le regole per i prompt | una riga che rimanda a un file del repository, verificato con lo sha; niente codice codificato; comandi brevi e separati; dopo un rifiuto, niente varianti |
| che cosa non fa | i lavori oltre i 20 minuti li lancia Maurizio dal terminale; un rifiuto deciso dalla chat prima della chiamata non arriva al ponte |

**I numeri**

| che cosa | valore | data |
|---|---|---|
| registro delle decisioni prima della riforma | 102 voci, circa 7.500 righe in un file | 8/7/2026 |
| registro dei lavori prima della riforma | 143 voci, stato scritto in tre punti | 8/7/2026 |
| decisioni registrate | 541 | 24/11/2026 |
| voci dei lavori | 557 | 24/11/2026 |
| referti | circa 1.800 file | 24/11/2026 |
| salvataggi nel repository (commit) | 2.792, dal 13/3/2026 | 24/11/2026 |
| sessioni di Claude Code sul solo PC | 810 file di sessione, dal 30/9/2026 | 25/11/2026 |

---

*Scritto a quattro mani con Claude. Le scelte, e la responsabilità di quello che c'è scritto, sono mie.*
