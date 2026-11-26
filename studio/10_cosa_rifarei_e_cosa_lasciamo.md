# 10. Cosa rifarei, e cosa lasciamo

Alla fine di un viaggio resta sempre la stessa domanda: che cosa farei di diverso, se potessi ripartire?

La mia risposta comincia con una confessione. La voglia di costruire il prodotto mi ha reso cieco ai problemi fin
quando non ci ho sbattuto contro.

Con due intelligenze artificiali al fianco, costruire era diventato veloce. Ogni sera qualcosa in più funzionava: una
scheda, una tabella letta bene, una risposta più fedele alla fonte. È un ritmo che trascina, e che lascia in ombra le
domande a cui non si risponde con una riga di codice. Quelle domande erano tre. Se tornassi a marzo, le farei tutte e
tre prima di cominciare, e in quest'ordine.

## Primo: guardare il recinto

A fine maggio, al terzo mese, ci siamo trovati davanti a un bivio, e lo abbiamo scritto nero su bianco.

Da una parte c'era IP come consulente: un sistema che elabora, confronta i farmaci, calcola la dose per quel paziente.
Accanto a questa strada avevamo annotato, con onestà, «massima utilità percepita». Dall'altra c'era IP come specchio
delle fonti ufficiali: riporta il dato così com'è scritto, con la fonte accanto, e il calcolo lo lascia al medico.

Abbiamo scelto lo specchio, e per buone ragioni: un numero inventato da una macchina è pericoloso anche se accanto c'è
un'avvertenza, perché il medico si fida della cifra. In agosto, un memo sulla qualificazione come dispositivo medico ci
ha aiutato a vedere anche dove passava il confine legale. A grandi linee, e come l'abbiamo letto noi: riportare stava
di qua, concludere sul singolo paziente stava di là.

Quello che non ci siamo chiesti è la domanda più semplice di tutte. Se il medico vuole il consulente, chi glielo darà?

A novembre la risposta è arrivata da sola: un'intelligenza artificiale generalista, gratis.

Ecco perché metto il recinto al primo posto. Sapere dov'è non basta. Bisogna chiedersi se il valore che il cliente
cerca sta dentro o fuori. Se sta fuori, ci sono solo due strade: attraversare il recinto, e pagarne il prezzo, oppure
cambiare destinazione. Noi lo abbiamo capito all'ottavo mese. La domanda si poteva fare al terzo; anzi, al primo.

## Secondo: la prova del generalista, in agenda

La seconda cosa è la prova del primo capitolo. Dieci domande, una chiave, una regola chiusa in una busta, e un'IA
generalista come avversario. Costa poche ore.

L'idea non è mia. Viene da una frase di Andrej Karpathy, che avevo letto in un articolo di Luca Cazzaniga: un'app
diventata inutile perché a un'IA generalista bastava una richiesta per fare lo stesso lavoro. Io l'ho tradotta così,
per IP: se è una cosa che già fa una IA generalista ora o a breve, è inutile provarci.

Ma una prova sola non basta. Come raccontato nel primo capitolo, in otto mesi il terreno si è mosso più di quanto si
potesse prevedere. La prova del generalista va trattata come il controllo dal dentista: non si fa una volta nella vita,
si mette in agenda. Il primo giorno, e poi ogni volta che un generalista cambia modello.

## Terzo: la strada prima del carretto

La terza cosa è quella del capitolo 9. Il pubblico si comincia a costruire il primo mese, non l'ottavo, con contenuti
utili da soli: una newsletter che racconta dati pubblici non promette nulla e non brucia nessun contatto.

È un errore vero, ma lo metto per ultimo perché è il più rimediabile dei tre. Una strada, con pazienza e un po' di
denaro, si popola. Un recinto legale no.

L'ordine, del resto, non è casuale. La prima domanda può chiudere la partita prima ancora di cominciarla. La seconda la
chiude, o la riapre, in poche ore. La terza si risolve con tempo e denaro.

## Una persona sola, e chi le serve accanto

Le tre domande hanno una cosa in comune: nessuna si risolve con una riga di codice. Ciascuna chiede qualcuno di fuori:
chi conosce la legge, un rivale da battere, i clienti. Una persona sola, con un'IA, può costruire quasi tutto, e questi
otto mesi lo dimostrano. Ma le cose che non può fare da sola sono proprio quelle da fare per prime.

## Che cosa lasciamo

Spegnere un prodotto non vuol dire buttare tutto. Di questi otto mesi restano tre cose, e le pubblichiamo.

La prima è un metodo: una chat che progetta, Claude Code che esegue, una persona che decide. Ogni decisione sta in un
file suo, che una volta chiuso non si tocca più: se cambia idea, si scrive una voce nuova. Il capitolo 2 lo racconta per
intero.

La seconda sono gli strumenti che quel metodo ha prodotto, ripuliti dalle cose che riguardano solo noi.

- **Un generatore di indici.** Quando le decisioni hanno smesso di stare in un unico file di migliaia di righe e sono
  diventate un file ciascuna, serviva qualcosa che ne ricomponesse la mappa. Lo script la rigenera da capo ogni volta, e
  sa anche dire se la mappa salvata è rimasta indietro.
- **Due script per i commit.** Sono nati da un errore che si ripeteva: un passo fatto nell'ordine sbagliato. Lo avevamo
  scritto nelle regole, una volta e poi un'altra, e l'errore tornava. Alla fine abbiamo capito che una regola che si
  legge e si viola non sta nel posto sbagliato: sta nella forma sbagliata. Descriveva un ordine, quando serviva uno
  strumento che quell'ordine lo eseguisse da sé, e che si fermasse se i file da salvare non erano quelli attesi.
- **Le istruzioni per scrivere una decisione**, pronte per Claude Code: dove va il file, che cosa deve contenere, come si
  corregge senza riscrivere la storia.
- **Un ponte fra la chat e Claude Code**, un solo file Python senza dipendenze. Permette alla chat di affidare un lavoro
  a Claude Code sul computer e di seguirne l'esito. Su quel ponte è passata anche una parte del lavoro di questo
  studio.

La terza è questo studio, con i suoi errori raccontati per intero e i suoi successi messi in fila, perché chi costruisce
possa evitare i primi e rifare i secondi.

## Un aforisma, per finire

Il nome del progetto veniva da Ippocrate. Al medico greco si attribuisce un aforisma che, a rileggerlo oggi, sembra
scritto per questa storia: la vita è breve, l'arte è lunga, l'occasione fuggevole, l'esperienza fallace, il giudizio
difficile.

L'occasione è fuggita in otto mesi, mentre il terreno si muoveva. L'esperienza era fallace finché non l'abbiamo messa
alla prova con una regola scritta prima. Il giudizio è stato difficile, ma alla fine è arrivato in un giorno. E l'arte,
quella di costruire con questi strumenti nuovi, è davvero lunga: noi abbiamo appena cominciato a impararla.

## Per chi costruisce

- **Prima del codice, chiedetevi dove sta il valore rispetto al recinto.** Se quello che il cliente cerca sta fuori dal
  perimetro che potete permettervi, saperlo al primo mese vale più di otto mesi di lavoro ben fatto.
- **Scrivete le due strade, e accanto a ciascuna chi altro la percorre.** Noi avevamo scritto «massima utilità
  percepita» accanto alla strada che non abbiamo preso. Mancava una riga: chi la offrirà al nostro cliente?
- **Mettete in agenda la prova del generalista.** Il primo giorno e a ogni cambio di modello. Costa poche ore.
- **Cominciate il pubblico il primo mese**, con contenuti utili da soli.
- **Quando una regola viene violata due volte, trasformatela in uno strumento.** Una nota più lunga non serve: serve uno
  script che esegua l'ordine giusto e si fermi da solo.
- **Scrivete prima la regola che vi farà fermare.** Saper chiudere in un giorno, senza rimpianti, è un risultato.
- **Pubblicate quello che resta.** Un prodotto spento può ancora insegnare qualcosa, se il suo metodo e i suoi strumenti
  restano a disposizione.

---

### Riquadro — La lista del primo giorno

*Per il lettore tecnico: le domande da fare prima della prima riga di codice, con il punto in cui questo studio le
racconta.*

1. **La destinazione d'uso in una frase.** Per quello che dichiara di fare, il vostro software è un dispositivo medico?
   In Europa il punto di partenza sono il regolamento (UE) 2017/745, allegato VIII, regola 11, e le linee guida MDCG
   2019-11 sulla qualificazione del software. Sono un punto di partenza, non un parere legale (capitoli 1 e 7).
2. **Le due strade, scritte.** Quella che elabora e quella che riporta, ciascuna col suo rischio, il suo valore per il
   cliente e chi altro già la offre (questo capitolo).
3. **La prova del generalista**, con la regola in busta, rifatta a ogni cambio di modello (riquadro del capitolo 1).
4. **Il canale minimo**, attivo dal primo mese (riquadro del capitolo 9).
5. **La regola d'arresto**, scritta prima di misurare.

Gli strumenti, da pubblicare ripuliti:

| strumento | che cosa fa | nato da |
|---|---|---|
| `doc_index.py` | rigenera gli indici delle decisioni e del backlog dai file singoli; `--check` dice se gli indici salvati sono rimasti indietro | il passaggio da due documenti unici a un file per voce, luglio 2026 |
| `doc_commit.sh`, `diag_commit.sh` | eseguono i comandi di commit nell'ordine giusto, con un cancello sul numero di file attesi e uno sul perimetro dei file ammessi | un errore d'ordine nei comandi di git ripetuto più volte nonostante le note scritte, agosto 2026 |
| la skill `voce-doc` | istruzioni per Claude Code su come si scrive e si corregge una decisione o una voce di backlog | il formato file per voce |
| `cc-bridge` | server MCP in un solo file Python, senza dipendenze: la chat lancia, segue e riprende i lavori di Claude Code nel WSL del PC | ottobre 2026, al posto della coda dei briefing da lanciare a mano |

---

*Scritto a quattro mani con Claude. Le scelte, e la responsabilità di quello che c'è scritto, sono mie.*
