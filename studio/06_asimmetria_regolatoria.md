# 6. L'asimmetria regolatoria

## Il coltello e il bisturi

Un coltello da cucina e un bisturi possono avere una lama molto simile. Eppure per la legge sono due oggetti diversi.
Il bisturi è venduto per operare: è un dispositivo medico, e prima di arrivare in sala deve dimostrare di essere
sicuro. Il coltello è venduto per tagliare il pane, e nessuno gli chiede niente, nemmeno se un giorno qualcuno lo
usasse per incidere. La legge non guarda la lama. Guarda la promessa scritta sulla scatola.

Con il software funziona allo stesso modo, ed è il motivo, il secondo, per cui abbiamo spento IP. Questo capitolo
racconta come una stessa frase possa essere una normale risposta o l'uscita di un dispositivo medico, a seconda di chi
la scrive. E perché, per chi costruisce uno strumento specializzato, questa differenza pesa più di qualunque riga di
codice.

## Una frase, due destini

Torniamo a una delle domande del test raccontato nel primo capitolo. Un paziente di 82 anni, 58 chili, in fibrillazione
atriale, prende un anticoagulante, l'apixaban, alla dose piena. Ha una polmonite, e il medico vorrebbe dargli un
antibiotico. Come si regola?

Il foglio ufficiale del farmaco contiene la risposta, ma non scritta per quel paziente. Dice che la dose si dimezza
quando ricorrono almeno due condizioni su tre: età di almeno 80 anni, peso fino a 60 chili, un certo valore della
creatinina. Il nostro paziente ne ha due. Quindi la sua dose è sbagliata.

ChatGPT ha fatto proprio questo: ha preso la regola, l'ha applicata all'età e al peso, e ha concluso che la dose andava
ridotta. È la risposta di un collega esperto.

Ora immaginiamo la stessa frase, parola per parola, scritta da IP: «per questo paziente di 82 anni e 58 chili la dose è
2,5 milligrammi due volte al giorno». Quel martedì di novembre, quando abbiamo deciso di spegnere, l'abbiamo scritto
così nella voce del registro: è una risposta di un'IA generalista se la scrive ChatGPT, un dispositivo medico di classe
IIa se la scrive IP.

Stesse parole, stessa utilità per il medico. Due destini legali.

## Che cosa guarda la legge

Per il regolamento europeo sui dispositivi medici, che cosa sia un software lo decide anzitutto la sua destinazione
d'uso: l'uso a cui lo destina il fabbricante, secondo quello che scrive sull'etichetta, nelle istruzioni, e anche nel
materiale promozionale.

Un considerando del regolamento, cioè una delle premesse che spiegano come leggerlo, lo dice in modo esplicito: il
software destinato a finalità generali, anche se usato in un contesto sanitario, non è un dispositivo medico. E la Corte
di giustizia, in una sentenza del 2017, ha aggiunto che non basta l'uso in un contesto medico: serve che la finalità,
definita dal fabbricante, sia specificamente medica.

ChatGPT, come l'abbiamo letto noi, è un software a finalità generali. Il suo produttore non lo dichiara destinato a
diagnosi o terapia. Milioni di persone lo usano per scrivere lettere, tradurre, programmare; alcuni medici lo usano per
chiedere una dose. L'uso del medico non cambia la promessa sulla scatola.

IP, invece, era uno strumento dichiarato per il medico. Fin dalla prima pagina, il destinatario era lui. E quella
dichiarazione, che per noi era semplicemente onestà, per la legge era il primo elemento della qualificazione.

## Di qua dal confine: riportare

Dentro il recinto c'è spazio, e più di quanto si pensi. Nella stessa sentenza del 2017, fra gli esempi di software
che non sono dispositivi medici, la Corte ne porta due che sembrano scritti per noi: uno che indica al medico il nome del generico corrispondente al farmaco che
vuole prescrivere, e uno che segnala le controindicazioni scritte dal produttore nel foglio del farmaco. Il confine
passa più in là: diventa dispositivo il software che crea o modifica le informazioni mediche, per esempio calcolando o
confrontando dati con dei riferimenti, per dare informazioni su un determinato paziente.

È su questa linea che IP è stato costruito, e il capitolo 5 lo racconta per intero. Nel caso dell'apixaban, IP poteva
mostrare la regola del foglio ufficiale: le tre condizioni, la dose ridotta, la sezione da cui venivano. Il passo
successivo, metterle accanto all'età e al peso di quel paziente e dire «la dose è sbagliata», era quello che ci era
vietato. Lo lasciavamo al medico.

Le linee guida europee sulla qualificazione del software, del resto, mettono fra gli esempi di dispositivo medico
proprio questo: un software che analizza i dati di un singolo paziente per suggerire aggiustamenti della dose, o
segnalare interazioni, nei pazienti con insufficienza renale.

## Le parole sono già una dichiarazione

C'è un dettaglio che chi costruisce tende a sottovalutare, e che a noi ha insegnato molto. La destinazione d'uso non
sta solo nei documenti tecnici: sta anche nel materiale promozionale. Per questa legge il marketing non è un mondo a
parte. È una dichiarazione.

Nelle prime pagine del sito, scritte quando IP era ancora un esperimento, fra le domande d'esempio c'era «Cosa
prescrivere per il diabete tipo 2». E l'immagine che accompagnava i link condivisi diceva «Decision support clinico».
Per noi erano parole innocenti, il modo comune di presentare uno strumento per medici. Per la legge erano quasi la
definizione di dispositivo medico.

Le abbiamo tolte, e abbiamo fatto di più: nelle nostre regole interne è entrato un elenco di parole vietate.
«Supporto alla decisione», «cosa prescrivere per…», «raccomanda», «consiglia», «personalizzato per il paziente»,
«calcola la dose», «diagnosi differenziale». Da allora i testi pubblici, dal sito al whitepaper, si confrontavano con quell'elenco. In ottobre anche l'immagine dei link condivisi è
cambiata, e da allora diceva un'altra cosa: «Consultazione farmacologica su fonti AIFA per il medico italiano». È la frase che descriveva
davvero quello che IP faceva, e anche quella che lo teneva di qua dal confine.

## Di là dal confine: certificarsi

Che cosa sarebbe successo, se avessimo deciso di attraversarlo? Come l'abbiamo letto noi, un software che fornisce
informazioni usate per decidere una terapia parte dalla classe IIa, e per i farmaci più delicati, come gli
anticoagulanti, la classe potrebbe salire. Vuol dire un organismo notificato, un sistema di qualità, una valutazione
clinica, la sorveglianza dopo l'immissione sul mercato e la vigilanza sugli incidenti.

Il memo che avevamo preparato in agosto lo diceva con una frase che a rileggerla oggi suona come un verdetto: il
vincolo non è il costo iniziale, è il carico permanente. Non è un progetto che si chiude, è una funzione dell'impresa
che non si sospende quando c'è da sviluppare. E i tempi, come racconto nel capitolo 7, si contano in anni.

Mettere sul mercato un dispositivo medico senza marcatura, poi, ha un prezzo scritto nella legge italiana: una sanzione
che parte da oltre ventiquattromila euro, ridotta di un terzo per le microimprese. Ma per un'impresa piccola il conto
vero è un altro, e lo racconto nel capitolo 7: quanto costerebbe difendersi.

## Dall'altra parte del tavolo

Quel martedì, davanti ai punteggi, l'ho messa così: portare IP al livello di ChatGPT ci avrebbe esposti legalmente,
mentre ChatGPT, che non è dichiarato dispositivo medico, ha dietro di sé avvocati da mille dollari l'ora. È da quella frase che i motivi dello spegnimento sono diventati due: il test, e l'asimmetria.

Non è un'accusa. La regola ha una sua logica: se contasse l'uso e non la promessa, ogni foglio di calcolo aperto in un
ambulatorio sarebbe un dispositivo medico, e nessun software generale potrebbe più entrare in un ospedale. Ma per chi
costruisce uno strumento specializzato, la stessa regola ha una conseguenza precisa. Specializzarsi, dichiarando il
medico come destinatario, vuol dire entrare nel regime che il generalista evita. Il generalista può essere più utile
proprio perché promette meno.

E il terreno, anche qui, si muove. Il 22 aprile 2026, negli Stati Uniti, il produttore di ChatGPT ha aperto gratis ai
medici e ai farmacisti verificati una versione pensata per il lavoro clinico, e ha detto di voler arrivare ad altri
paesi col tempo. Che cosa succederebbe se una versione così arrivasse in Europa, con un destinatario medico dichiarato,
non lo sappiamo, e non spetta a noi dirlo.

Lo stesso vale per l'altra domanda che ci siamo fatti. La sentenza della Corte di giustizia del luglio 2026, che
ritorna nel capitolo 7, dice che la dichiarazione del fabbricante è importante ma non è l'unico elemento, e che conta anche che
cosa il prodotto fa davvero. Le parole sono necessarie, ma non bastano. Un giorno qualcuno potrebbe chiedersi che cosa
fa davvero un'IA generalista quando un medico le chiede una dose. Non sappiamo se e quando succederà. Sappiamo che,
fino a quel giorno, l'asimmetria è un fatto del mercato, e che chi costruisce deve metterla nel conto prima di
scegliere il proprio terreno.

Noi l'abbiamo messa nel conto all'ottavo mese. È il secondo motivo per cui IP si è spento.

## Per chi costruisce

- **Scrivete la destinazione d'uso in una frase, prima del codice**, e rileggetela con le parole della norma:
  diagnosi, prevenzione, monitoraggio, previsione, prognosi, trattamento, attenuazione di una malattia. Se una di queste
  parole descrive il vostro prodotto, siete già dentro la domanda.
- **Trattate il marketing come una dichiarazione legale.** Sito, esempi, anteprime dei link, slide: tutto concorre alla
  destinazione d'uso. Tenete un elenco di parole vietate e passateci ogni testo nuovo.
- **Distinguete riportare una regola da applicarla.** Mostrare le condizioni per ridurre una dose è consultazione;
  applicarle al paziente e concludere è il passo che, per uno strumento dichiarato medico, cambia regime.
- **Mettete nel conto il prezzo della specializzazione.** In un settore regolato, dichiarare un destinatario
  professionale può portarvi nel regime che il generalista evita. Il generalista può dare la risposta più utile proprio
  perché promette meno.
- **Seguite che cosa dichiarano i generalisti, e quando.** Una loro versione per professionisti può cambiare il vostro
  mercato in un giorno.
- **Non usate l'asimmetria come scudo.** Le parole sono necessarie ma non bastano: il comportamento del sistema deve
  dire la stessa cosa delle vostre pagine.

---

### Riquadro — La prova della destinazione d'uso, per rifarla

*Per il lettore tecnico: i passi che rifarei il primo giorno, con le fonti. È la nostra lettura dei testi al novembre
2026, non un parere legale.*

1. **La frase.** Chi usa il prodotto, che cosa fa, a che scopo. Una riga.
2. **Il confronto con la definizione.** Reg. (UE) 2017/745, art. 2 punto 1: è dispositivo il software destinato a
   «diagnosi, prevenzione, monitoraggio, previsione, prognosi, trattamento o attenuazione di malattie».
3. **L'inventario delle dichiarazioni.** Art. 2 punto 12: la destinazione d'uso si legge nelle indicazioni del
   fabbricante «sull'etichetta, nelle istruzioni per l'uso o nel materiale o nelle dichiarazioni di promozione o
   vendita». Raccogliete tutto: pagine, esempi, anteprime dei link, slide, post.
4. **Il lessico vietato.** Il nostro, con le parole da usare al loro posto: «supporto alla decisione» → «consultazione
   documentale»; «cosa prescrivere per X» → «farmaci autorizzati per X secondo RCP»; «raccomanda», «consiglia»,
   «suggerisce la terapia» → «riporta», «cita»; «calcola la dose» → «riporta la posologia autorizzata»;
   «personalizzato per il paziente» → da togliere, non sostituire; «diagnosi differenziale» → fuori perimetro, si
   rifiuta la domanda. Ogni testo nuovo ci passa sopra.
5. **I passi di decisione** delle linee guida MDCG 2019-11 (rev. 1, giugno 2025) e, se siete dentro, la
   classificazione con la regola 11 dell'Allegato VIII.
6. **La prova sul sistema.** Fate al prodotto una domanda con i dati di un paziente («metformina, eGFR 40») e guardate
   se riporta l'intera regola o sceglie la riga di quel paziente. La seconda è selezione sul paziente, qualunque cosa
   dicano i vostri termini d'uso.
7. **La prova sul generalista.** Fate la stessa domanda a un'IA generalista. Se la risposta che serve al vostro cliente
   è quella che applica la regola al paziente, il valore sta fuori dal vostro recinto.

**Le fonti, in ordine**

| fonte | che cosa dice, in breve | data |
|---|---|---|
| Reg. (UE) 2017/745, considerando 19 | il software destinato a finalità generali, «anche se utilizzato in un contesto sanitario», non è un dispositivo medico | 2017 |
| Reg. (UE) 2017/745, art. 2 punti 1 e 12 | la definizione di dispositivo medico; la destinazione d'uso secondo le indicazioni del fabbricante, compreso il materiale promozionale | 2017 |
| Corte di giustizia, C-329/16, *Snitem e Philips France*, punto 24 | non basta l'uso in un contesto medico: la finalità definita dal fabbricante deve essere specificamente medica | 7/12/2017 |
| idem, punto 26 | non sono dispositivi: il software che indica il generico corrispondente, quello che segnala le controindicazioni scritte dal produttore | 7/12/2017 |
| idem, punto 33 | è dispositivo il software che crea o modifica informazioni mediche, per esempio calcolando o confrontando dati con riferimenti, per un determinato paziente | 7/12/2017 |
| MDCG 2019-11 rev. 1, Annex I, c.1 | esempio di dispositivo: «MDSW that analyse patient-specific data to suggest dosage adjustments or flag potential drug interactions for patients with kidney impairments» | giugno 2025 |
| Reg. (UE) 2017/745, Allegato VIII, regola 11 | software per decisioni diagnostiche o terapeutiche: almeno classe IIa | 2017 |
| Corte di giustizia, C-427/24 | la destinazione d'uso dichiarata è un elemento importante, non l'unico; contano anche le funzioni oggettive | 2/7/2026 |
| D.Lgs. 137/2022, art. 27 | immissione sul mercato in violazione dell'art. 5 MDR: da 24.200 a 145.000 €; riduzione di un terzo per le microimprese (c. 48) | 2022 |
| OpenAI, «Making ChatGPT better for clinicians» | versione per il lavoro clinico, gratis per medici, infermieri di pratica avanzata, assistenti medici e farmacisti verificati negli Stati Uniti; altri paesi «over time» | 22/4/2026 |

---

*Scritto a quattro mani con Claude. Le scelte, e la responsabilità di quello che c'è scritto, sono mie.*
