# 3. Dai PDF alle risposte

## Novemila libretti

Tutti conoscono il bugiardino, il foglietto piegato dentro la scatola di un farmaco. Pochi sanno che ha un fratello
maggiore, scritto per il medico: il Riassunto delle Caratteristiche del Prodotto, l'RCP. È un documento lungo,
tecnico, e ha una virtù preziosa: è costruito sempre allo stesso modo. La posologia sta alla sezione 4.2, le
controindicazioni alla 4.3, le interazioni alla 4.5, la gravidanza alla 4.6. Per ogni farmaco autorizzato in Italia,
l'AIFA ne pubblica uno.

Immaginate una biblioteca con più di novemila di questi documenti, uno per ogni medicinale: tre gigabyte e mezzo di
PDF. Un medico fa una domanda, e in pochi secondi bisogna trovare il paragrafo giusto, nel documento giusto, e
mostrarglielo con la fonte accanto. In una frase, è tutta l'architettura di IP.

Questo capitolo racconta come una biblioteca di PDF è diventata quasi mezzo milione di frammenti pronti per essere
cercati. E risponde alla domanda che mi sono fatto più spesso in quei mesi: come fai a sapere che quei frammenti sono
giusti?

## Due magazzini

I dati di IP stavano in due magazzini diversi, ciascuno con il suo mestiere.

Nel primo c'erano i dati strutturati dell'AIFA: il nome di ogni confezione, il codice AIC, il principio attivo, la
classe di rimborso, lo stato di commercializzazione, le carenze, le Note che limitano la prescrizione, i piani
terapeutici. Arrivavano da fonti diverse, con ritmi diversi: le carenze ogni notte, alcuni elenchi ogni settimana,
l'anagrafica ogni mese. Ogni flusso aveva il suo programma, lanciato da un orologio sul server, e ogni flusso scriveva
i suoi campi. A novembre questo magazzino contava più di trentottomila confezioni.

Nel secondo magazzino c'era il testo: i fogli ufficiali tagliati in frammenti, ciascuno trasformato in una sequenza di
numeri che ne rappresenta il significato, così che una domanda possa trovare i frammenti che le somigliano. Accanto,
due raccolte separate: le linee guida italiane e, fino a novembre, gli abstract degli articoli scientifici.

Il primo magazzino diceva che cosa è un farmaco; il secondo, che cosa dice il suo foglio. La risposta li usava
entrambi.

## Leggere un PDF carattere per carattere

La parte più difficile, e più sottovalutata, è la prima: leggere un PDF. Un PDF non è un testo. È un disegno di
lettere messe in certe posizioni sulla pagina, e il testo bisogna ricostruirlo.

La catena lo faceva pagina per pagina, in un ordine preciso. Prima prendeva i caratteri, uno per uno, con le loro
posizioni. Poi la tipografia: grassetto, corsivo, apici, pedici. Sembra un dettaglio estetico, e non lo è. In alcuni
fogli, letti senza tipografia, «10⁹/L» diventava «109/L»: un apice perso, e un numero completamente diverso. La
correzione è stata una delle condizioni per aprire le schede ai motori di ricerca.

Poi gli spazi. Le due librerie che usavamo per leggere i PDF non erano d'accordo su dove cadessero gli spazi fra le
parole. Il codice allineava le loro letture lettera per lettera, aggiungeva uno spazio solo dove la seconda ne vedeva
uno, e ne toglieva uno solo se la prima l'aveva inventato. Se le lettere non tornavano identiche, la pagina restava
com'era, e la cosa si contava.

Poi le tabelle, che nei fogli dei farmaci sono ovunque: le dosi per la funzione renale, le interazioni, gli effetti
indesiderati per frequenza. Il codice cercava le regioni con le righe disegnate e le leggeva riga per riga. Dove non
poteva verificare la griglia, non la indovinava: dichiarava la tabella al medico e ne salvava un'immagine, da mostrare
accanto al testo. A novembre le immagini delle tabelle erano più di trentasettemila, per oltre seimila medicinali.

Infine le pulizie: la riga che ogni pagina porta in fondo, i numeri di pagina, il testo standard sulla segnalazione
degli effetti indesiderati che ogni foglio ripete uguale. E il riconoscimento della struttura: un solo PDF può
contenere più RCP, uno per forma farmaceutica, e le sezioni si riconoscono dai loro titoli canonici, quelli che ogni
RCP porta nello stesso ordine.

## Il frammento

A quel punto il testo di ogni sezione si tagliava in frammenti. Una sezione corta diventava un frammento solo; una
lunga si divideva per frasi, oppure per unità intere quando conteneva tabelle: una tabella che stava in un frammento
non si spezzava mai a metà.

Ogni frammento portava in testa una piccola etichetta: il principio attivo, il nome del medicinale, la sezione e,
se serviva, «parte 2 di 3». Così, anche estratto da solo, diceva che cos'era. E portava con sé la sua provenienza:
l'impronta del PDF da cui veniva e la versione del codice che l'aveva prodotto.

Nell'ultima ricostruzione, di novembre, dai 9.186 PDF sono usciti 520.766 frammenti. Togliendo quelli identici, perché
lo stesso testo compariva in due forme dello stesso documento, ne sono rimasti 489.705. Undici documenti non ne hanno
prodotto nessuno, e per ciascuno c'era scritto il motivo: sette senza sezioni riconoscibili come RCP, tre fatti solo
di etichettatura, uno illeggibile. Undici su più di novemila, ognuno con la sua spiegazione: è il genere di numero che
lascia dormire tranquilli.

## I vettori

L'ultimo passo trasformava ogni frammento in un vettore: una sequenza di 1.024 numeri che ne rappresenta il
significato. Lo faceva un modello aperto, multilingue, che girava sulla scheda grafica del mio computer. A giugno
avevamo lasciato gli embedding a pagamento di un grande fornitore per questo modello: da allora trasformare una domanda
in vettore non costava più niente.

Sul mio PC la lettura dei PDF durava circa un'ora e mezza, i vettori circa tre ore. Una ricostruzione intera del corpus
stava in una notte.

E c'era una regola che considero fra le migliori del progetto: la collezione in servizio non si tocca mai. Ogni
ricostruzione nasceva in una collezione nuova, con la data nel nome; il programma si rifiutava di partire se la
destinazione era quella in servizio, e non cancellava mai niente. Solo quando la nuova aveva passato i suoi controlli
si spostava il servizio su di lei, cambiando una riga di configurazione. La vecchia restava lì, pronta per tornare
indietro.

## Come fai a sapere che sono giusti?

Quasi mezzo milione di frammenti non si rileggono a mano. Allora come si fa a fidarsi?

La prima risposta è arrivata in agosto, con la ricostruzione completa del corpus. Cinque problemi misurati, diversi
fra loro, portavano tutti alla stessa conclusione: alcune etichette delle forme non erano pubblicabili, le etichette
dei frammenti si erano stratificate nel tempo, e lo stesso ingresso non dava sempre la stessa uscita. Non si potevano
rattoppare uno per uno. Abbiamo deciso di rifare tutto da capo, con una regola scritta nella decisione: i controlli
fermano, non degradano. Se un controllo è rosso, ci si ferma; non si va avanti «con qualche avvertenza».

La seconda risposta è un controllo prima della parte costosa. La documentazione della catena lo dice così: tre ore di
scheda grafica su una lettura sbagliata sono tre ore perse. Prima di calcolare i vettori, la lettura nuova si
confrontava con quella precedente. Se erano cambiati solo alcuni PDF, tutti gli altri medicinali dovevano risultare
identici, frammento per frammento e immagine per immagine. Se era cambiato il codice, il confronto si progettava
insieme alla decisione che lo cambiava, dicendo prima che cosa doveva restare uguale e che cosa poteva cambiare.

La terza è una fotografia congelata. Per le tabelle avevamo scelto ventisei medicinali, più di novecento pagine, e ne
avevamo congelato l'uscita, come in una fotografia. Ogni modifica del codice delle tabelle si confrontava con quella fotografia, e
ricongelarla era una decisione mia, mai automatica.

La quarta è la batteria di domande dopo ogni aggiornamento del server. All'inizio la facevamo girare quando lo
chiedevo io. A luglio, dopo un errore che c'era già prima, un aggiornamento senza batteria ci ha tolto il punto di
riferimento, e per un giorno il sospetto è caduto sulla modifica sbagliata. Da allora la batteria è obbligatoria.

E la quinta, la più semplice: guardare. I conteggi verdi non bastano. Dopo una serie di giri fatti in autonomia,
fermavo il lavoro e chiedevo di vedere esempi veri: una tabella, una pagina, una riga. La chat, del resto, poteva
guardare da sola le pagine dei PDF come immagini e confrontarle con il testo estratto, e lo faceva.

C'è una lezione che viene proprio da questi controlli, e mi sembra la più preziosa. A settembre una delle fotografie
congelate portava un'etichetta di versione sbagliata. Se ne è accorto un solo strumento, per una ragione tutta sua; il
controllo principale era uscito verde. Era la terza volta in due giorni che una rete di sicurezza risultava esistere
per caso, e in un punto solo. Una rete che esiste per caso non è una rete: è fortuna. È il senso del motto del
progetto: per costruzione, non per fortuna.

## Dalla domanda alla risposta

Il resto del viaggio è più breve da raccontare, perché i capitoli 4 e 5 lo hanno già fatto. La domanda del medico
arrivava al server. Quando poteva, il codice la riconosceva da sé e andava dritto al documento; altrimenti un modello
ne faceva un piano. Poi si cercavano i frammenti, filtrati per i medicinali giusti, si prendevano dal primo magazzino i
dati strutturati, si componeva la risposta. Prima di arrivare al medico, la risposta passava i controlli delle
citazioni. E sotto, sempre, le fonti: il documento, la sezione, il codice del medicinale.

## Gli studi, dal vivo

C'era una fonte che, a un certo punto, è uscita dai magazzini: la letteratura scientifica.

In primavera avevamo copiato in casa circa duecentomila riassunti di articoli da PubMed, l'archivio pubblico della
letteratura biomedica che la biblioteca nazionale di medicina degli Stati Uniti mette a disposizione di tutti. Li
cercavamo come i frammenti degli RCP, per somiglianza di significato, e il modello li usava per arricchire le risposte
sulle malattie.

Da lontano funzionava. Da vicino, aveva tre difetti. Il primo: l'archivio era fermo. Tutti i riassunti erano stati
scaricati a metà aprile, e il programma che doveva aggiornarli non era mai stato scritto; per IP, un articolo uscito a
maggio non esisteva. Il secondo: una ricerca per somiglianza senza una soglia trova sempre qualcosa, anche quando non
c'è niente di pertinente. A una domanda sulla terapia dello scompenso cardiaco arrivavano tre analisi di
costo-efficacia: studi veri, sul tema giusto, che però a un medico con un paziente davanti non servono. Il terzo, il più
serio: quei riassunti il modello li rielaborava nella risposta. E un riassunto scritto da un modello non riporta,
elabora: è proprio il confine del capitolo 5.

A metà novembre la chat ha proposto di rovesciare il problema. Invece di tenere una copia, chiedere a PubMed nel
momento della domanda: come un bibliotecario che, invece di abbonarsi a tutte le riviste, telefona alla biblioteca
centrale. PubMed ha un'interfaccia pubblica fatta apposta. Prima di decidere l'abbiamo misurata: ottantacinque
chiamate, nessun errore, meno di un secondo per avere l'elenco. Visti i numeri, ho scritto: «facciamolo: dal vivo».

Il resto lo faceva il codice, senza modelli. A PubMed un nome italiano non trova nulla: il bisoprololo si cerca come
«Bisoprolol», e non sempre nel vocabolario con cui PubMed indicizza gli articoli. Così il codice traduceva il nome
del farmaco o della malattia con due tabelle, generate da uno script e verificate su PubMed riga per riga. A PubMed
partiva solo quella chiave, con i filtri sul tipo di studio: mai il testo scritto dal medico, mai un dato del
paziente. Un test lo controllava, parola per parola.

Al medico arrivava un indice, non un riassunto. Per ogni articolo il titolo, il tipo di studio (solo studi
randomizzati, revisioni sistematiche e meta-analisi; fuori le analisi economiche), la rivista, l'anno e il
collegamento; sopra l'elenco, la chiave usata, la data della ricerca e un pulsante per rifarla su PubMed. Il pannello
si apriva accanto a ogni medicinale della risposta, sotto l'elenco dei farmaci per una malattia, oppure rispondeva a
una domanda diretta, «studi su…».

Restava un ostacolo: i titoli sono in inglese, e spesso dicono poco. Così sotto ogni titolo abbiamo messo una riga in
italiano che dice di che cosa tratta lo studio: la domanda, la popolazione, l'intervento, il tipo di studio. Nessun
numero, nessun risultato, nessuna conclusione. Prima abbiamo messo a confronto, su cinquanta articoli, quattro versioni
scritte da tre modelli diversi; ho scelto quella di Claude Sonnet, che diceva di più senza mai dire che cosa lo studio
avesse trovato. Sotto una meta-analisi sullo scompenso, nella prova, si leggeva: «Revisione sistematica e meta-analisi
in rete di studi randomizzati che confronta diverse terapie farmacologiche e loro combinazioni nello scompenso cardiaco
con frazione di eiezione ridotta, considerando mortalità per tutte le cause e anni di vita guadagnati».

Il dettaglio che conta è quando quelle righe venivano scritte: prima. Più di dodicimila, in un colpo solo, dal mio
computer, per meno di venti dollari; poi conservate in una tabella, da aggiornare ogni mese per gli articoli nuovi.
Nel servizio nessun modello veniva chiamato: il codice leggeva la riga dalla tabella, come leggeva il titolo. E ogni
riga portava, ben visibile, il segno «IA».

PubMed dal vivo è entrato in servizio il 18 novembre. Sei giorni dopo IP si è spento. Il pannello lo vedeva solo chi
aveva un accesso professionale, che ai medici non era ancora stato aperto: l'abbiamo usato soltanto noi. È un successo
tecnico che nessun medico ha fatto in tempo a provare, e lo racconto per questo: chi costruisce qualcosa di simile può
partire da qui, senza passare dall'archivio.

Le linee guida italiane sono rimaste in casa, e per loro andava bene così. Ne avevamo caricate otto, quelle del
Sistema nazionale linee guida dedicate a problemi della medicina generale: il diabete di tipo 2, la malattia renale
cronica, l'obesità, l'ipotiroidismo, il dolore cronico, il disturbo da uso di alcol, l'infezione da Helicobacter, la
multimorbilità. Un cancello nel codice le lasciava entrare in una risposta solo per la loro malattia; fuori da quelle
otto, nessuna linea guida. Il medico le trovava fra le fonti, con il titolo e il collegamento. Dopo giugno non le
abbiamo più aggiornate, ma non c'era niente da aggiornare: per la medicina generale il portale non aveva pubblicato
nulla di nuovo. Non tutto era pulito, va detto: a volte al modello arrivavano frammenti doppi, o fatti di sola
bibliografia, e la correzione era ancora in lista quando IP si è spento.

Col senno di poi, è la domanda da fare a ogni fonte il primo giorno: quanto spesso cambia? Una fonte che cambia ogni
giorno, e ha una ricerca pubblica, si interroga al momento. Una che cambia di rado si può tenere in casa, purché si
sappia quando la si è copiata.

## Che cosa resta

Di tutto IP, la catena dei documenti è forse la parte che si riusa più facilmente. Chiunque lavori con documenti
ufficiali in PDF, norme tecniche, contratti, schede di sicurezza, incontra gli stessi problemi: i caratteri, gli
spazi, la tipografia, le tabelle, la struttura, la provenienza. E le stesse soluzioni funzionano: leggere carattere
per carattere, non indovinare ciò che non si può verificare, dare a ogni pezzo un'etichetta e un'impronta, non toccare
mai ciò che è in servizio, controllare prima della parte costosa.

Novemila documenti, quasi mezzo milione di frammenti, ricostruiti in una notte su un computer di casa. Per una persona
sola, la sera, mi sembra ancora un piccolo prodigio.

## Per chi costruisce

- **Leggete i PDF carattere per carattere, tipografia compresa.** Un apice perso cambia un numero.
- **Non indovinate le tabelle.** Se la griglia non si può verificare, dichiaratela e mostrate l'immagine della regione.
- **Date a ogni frammento un'etichetta e un'impronta**: che cosa è, da quale documento viene, quale versione del codice
  l'ha prodotto.
- **Contate ciò che esce, e date un motivo a ciò che manca**, scelto da un elenco chiuso.
- **Non toccate mai la collezione in servizio.** Costruite accanto, controllate, spostate il servizio con una riga di
  configurazione, tenete la vecchia.
- **Mettete il controllo prima della parte costosa.** Tre ore di calcolo su un ingresso sbagliato sono tre ore perse.
- **Congelate una fotografia dell'uscita attesa** e confrontate ogni modifica con lei.
- **Fate girare la batteria dopo ogni aggiornamento**, sempre, non solo quando qualcuno la chiede.
- **Guardate esempi veri, non solo conteggi.**
- **Chiedete a ogni fonte quanto spesso cambia.** Se cambia ogni giorno e ha una ricerca pubblica, interrogatela al
  momento; se cambia di rado, tenetela in casa, con la data della copia.
- **Una ricerca per somiglianza senza soglia trova sempre qualcosa.** Fate entrare una fonte solo attraverso una chiave
  che sapete mostrare all'utente.
- **Alla fonte esterna mandate solo la chiave**, mai il testo dell'utente, e scrivete il test che fallirebbe se
  succedesse.
- **Il testo dell'IA, quando potete, scrivetelo prima**: scelto su un campione, conservato, segnato come IA. Nel
  servizio non resta un modello da sorvegliare.
- **I controlli fermano, non degradano.** E una rete che esiste per caso non è una rete.

---

### Riquadro — La catena, per rifarla

*Per il lettore tecnico: i passi, le regole e i numeri dell'ultima ricostruzione. Le librerie e i modelli sono quelli
che usavamo noi; il metodo vale anche con altri.*

**I passi**

| passo | dove | durata (giri di ottobre) | che cosa | si ferma se |
|---|---|---|---|---|
| 1. preparazione | PC | minuti | precondizioni; la lettura precedente messa al riparo come termine di confronto | una precondizione manca |
| 2. lettura (fase A) | PC, CPU, dieci parti in parallelo | circa 1 h 30 (5.461 e 5.778 s) | PDF → frammenti, registro delle forme, immagini delle tabelle | uscita diversa da 0; frammenti oltre 512 token o errori non classificati diversi da 0 |
| 3. cancello prima della GPU | PC | minuti | confronto con la lettura precedente | qualunque differenza non attesa |
| 4. vettori | PC, GPU | circa 3 h (171,5 e 184,5 min) | frammenti → collezione nuova | destinazione uguale alla collezione in servizio; numero dei punti diverso dal numero dei frammenti |
| 5. cancelli dopo i vettori | PC | minuti | controlli sulla collezione nuova e sulle basi perse | rosso |
| 6. referto e messa in servizio | PC e server | — | referto nel repository; cambio della collezione servita in configurazione, riavvio | — |

**Ogni pagina, in ordine**: caratteri uno per uno (pdfium), via i caratteri ruotati, riparazione di legature e
codici; tipografia (grassetto, corsivo, apici, pedici); tabelle (prima le regioni rigate, poi al più un corridoio);
spazi riallineati lettera per lettera con una seconda libreria (fitz), solo dove le lettere coincidono; emissione delle
tabelle, con l'immagine della regione per i blocchi dichiarati; pulizie (riga AIFA in fondo alla pagina, numeri di
pagina, testo standard di farmacovigilanza del §4.8); reinnesto delle tabelle nel testo.

**Il frammento**: una sezione fino a 480 token è un frammento solo; oltre, per frasi o per unità intere (una tabella
che sta in un frammento non si divide); limite rigido 512 token, misurati con il tokenizzatore del modello. Prefisso:
`principio attivo (marchio) — §n titolo [· sotto-titolo] [(parte k/n)]`. Provenienza: impronta sha1 del PDF, versione
del codice di lettura con la versione del contratto delle tabelle.

**Il vettore**: `intfloat/multilingual-e5-large` a revisione fissata, sulla GPU, lotti da 64, testo `"passage: " +
frammento`, vettori normalizzati a 1.024 dimensioni; collezione Qdrant a distanza coseno, HNSW m 16 / ef 100; l'id di
ogni punto è la posizione del frammento nella lettura; a fine corsa il numero dei punti deve essere il numero dei
frammenti. Ripresa dopo una caduta, solo se l'impronta dei file della lettura è la stessa.

**I numeri dell'ultima ricostruzione**

| che cosa | valore |
|---|---|
| PDF degli RCP, uno per medicinale | 9.186, 3,5 GB |
| medicinali letti con esito positivo | 9.185 |
| frammenti grezzi | 520.766 |
| frammenti tolti perché identici | 31.061 |
| frammenti, e punti nella collezione servita | 489.705 |
| medicinali senza frammenti, con il motivo | 11: 7 senza sezioni RCP, 3 solo etichettatura, 1 PDF illeggibile |
| immagini delle tabelle | 37.678, per 6.427 medicinali |
| versione del contratto delle tabelle | 2.14 |
| confezioni nel magazzino dei dati strutturati | 38.467 (censimento del 3/11/2026) |
| frammenti delle linee guida / abstract scientifici | 1.900 / 204.810 (idem) |

**I controlli**: cancello prima della GPU (medicinali con PDF invariato identici, frammento per frammento e immagine
per immagine); fotografia congelata delle tabelle (26 medicinali, 949 pagine), ricongelabile solo con decisione
esplicita; batteria di domande obbligatoria dopo ogni aggiornamento che tocca la risposta; esempi veri guardati, non
solo conteggi.

**Gli studi e le linee guida**

| che cosa | valore |
|---|---|
| archivio PubMed, fino al 18/11/2026 | 204.810 abstract, scaricati il 15 e 16 aprile 2026; ricerca per somiglianza senza soglia, in quattro strategie della risposta; gli abstract nel prompt |
| PubMed dal vivo, dal 18/11/2026 | E-utilities di NCBI (ESearch ed ESummary), con una cache; pannello «Letteratura» per l'accesso professionale |
| misura dal server, 17/11/2026 | 85 chiamate, 0 errori; mediana 232 ms per la ricerca, 475 ms per i dati degli articoli |
| la query | solo termini delle due tabelle (principi attivi, col campo `MeSH Terms` o `nm` scelto riga per riga; condizioni, col descrittore) più filtri fissi: studi randomizzati, revisioni sistematiche, meta-analisi, studi sull'uomo, niente studi economici, una finestra di anni |
| il test | ogni parola alfabetica di ogni query deve venire dalle tabelle o dal modulo; nessun indirizzo porta il testo del medico |
| righe in italiano | 12.146 articoli distinti (i primi 10 per principio attivo e i primi 5 per condizione, su 2.103 chiavi), scritte da Claude Sonnet 5.5 con l'API a lotti, a metà prezzo: 17,56 USD; «di che cosa tratta», al più 25 parole nel prompt, nessun numero né risultato; scartate se vuote, oltre 45 parole o con 6 parole consecutive dell'abstract |
| aggiornamento delle righe | ogni mese dal PC, solo per gli articoli nuovi; stima: circa 700 posti nuovi al mese, circa 1 USD |
| linee guida SNLG | 8, con un cancello di perimetro per condizione; 1.900 frammenti (censimento del 3/11/2026); caricate a maggio, vettori di giugno; frammenti doppi o di sola bibliografia in correzione |

---

*Scritto a quattro mani con Claude. Le scelte, e la responsabilità di quello che c'è scritto, sono mie.*
