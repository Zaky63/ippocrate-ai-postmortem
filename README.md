# ippocrate.ai, un post-mortem

*Scritto a quattro mani con Claude. Le scelte, e la responsabilità di quello che c'è scritto, sono mie.*

ippocrate.ai era un assistente per i medici di famiglia italiani: rispondeva alle domande sui farmaci in linguaggio
normale, citando la fonte di ogni frase. Ci ho lavorato di sera e di notte per otto mesi, da marzo a novembre 2026, con
due intelligenze artificiali: una chat che progettava con me e Claude Code che lavorava sul codice e sul server. Il 24
novembre 2026 l'ho spento.

Questo repository raccoglie lo studio che racconta perché, e che cosa ho imparato, insieme agli strumenti che il metodo
di lavoro ha prodotto. È scritto per chi costruisce software con l'intelligenza artificiale, soprattutto da solo o
quasi: per evitare i miei errori e rifare, se servono, le cose che hanno funzionato.

Si comincia dall'[articolo zero](studio/00_articolo_zero.md), che presenta la serie in pochi minuti.

## Lo studio

0. [Ho spento il mio prodotto dopo otto mesi. Vi racconto perché, e che cosa ho imparato](studio/00_articolo_zero.md)
1. [Perché abbiamo spento ippocrate.ai](studio/01_perche_abbiamo_spento.md)
2. [Un'azienda di una persona e due Claude](studio/02_una_persona_e_due_claude.md)
3. [Dai PDF alle risposte](studio/03_dai_pdf_alle_risposte.md)
4. [Le citazioni inventate](studio/04_le_citazioni_inventate.md)
5. [Riportare, non elaborare](studio/05_riportare_non_elaborare.md)
6. [L'asimmetria regolatoria](studio/06_asimmetria_regolatoria.md)
7. [Che cosa chiede la legge a chi fa software, oggi](studio/07_che_cosa_chiede_la_legge.md)
8. [Quanto costa](studio/08_quanto_costa.md)
9. [Prima il prodotto, poi i medici](studio/09_prima_il_prodotto_poi_i_medici.md)
10. [Cosa rifarei, e cosa lasciamo](studio/10_cosa_rifarei_e_cosa_lasciamo.md)

Ogni capitolo ha tre parti: il racconto; «Per chi costruisce», con le lezioni da rifare e quelle da evitare; un
riquadro tecnico, con le cifre esatte e, quando si può, la ricetta per rifare quello che abbiamo fatto.

## Gli strumenti

Nella cartella [`strumenti/`](strumenti/README.md), con una prova in cinque minuti su una cartella d'esempio:

- **`doc_index.py`**: rigenera gli indici delle decisioni e del backlog, e dice se quelli salvati sono rimasti indietro;
- **`doc_commit.sh`** e **`diag_commit.sh`**: fanno i commit dei documenti e dei referti nell'ordine giusto, e si
  fermano se i file da salvare non sono quelli attesi;
- **`skill/voce-doc/`**: le istruzioni per Claude Code su come si scrive una decisione;
- **`cc-bridge/`**: il ponte che permette alla chat di affidare un lavoro a Claude Code sul computer e di seguirne
  l'esito.

## Licenze

Il testo dello studio è distribuito con la licenza [Creative Commons Attribuzione 4.0 Internazionale](LICENSE)
(CC BY 4.0): si può riprendere e adattare, anche per scopi commerciali, citando la fonte. Il codice in `strumenti/` è
distribuito con la [licenza MIT](strumenti/LICENSE).

## Un'avvertenza

Lo studio racconta un progetto e la lettura che ne abbiamo dato. Le parti sulle norme dicono come le abbiamo lette
noi: non sono un parere legale. Le parti sui farmaci raccontano che cosa rispondevano due sistemi a una certa data:
non sono indicazioni cliniche. Per un farmaco fa fede l'RCP pubblicato dall'AIFA.
