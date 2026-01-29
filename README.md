# Fake News Roulette 🎰📰

Un gioco educativo che utilizza la metafora della roulette russa per insegnare a distinguere tra notizie vere e fake news in modo divertente e interattivo.

## 📋 Descrizione

Fake News Roulette è un'applicazione Python sviluppata con Pygame che combina intrattenimento ed educazione. Il giocatore deve identificare se le notizie presentate sono vere o false, affrontando penalità in stile "roulette russa" quando sbaglia.

## ✨ Caratteristiche Principali

### 1. **Roulette delle Categorie**
- La roulette gira e seleziona casualmente una categoria di notizie
- Categorie disponibili:
  - 🏛️ Politica
  - 🔬 Scienza
  - 💻 Tecnologia
  - 🏥 Salute
  - 🎬 Intrattenimento
  - 💰 Economia

### 2. **Round Interattivi**
- Ogni round presenta una notizia dalla categoria selezionata
- Il giocatore sceglie se è "VERA" o "FALSA"
- Feedback immediato con spiegazioni dettagliate e fonti verificabili

### 3. **Meccanica della Roulette Russa**
Quando il giocatore sbaglia, si attiva una penalità casuale:
- 💥 **Perdita di Punti** (-50 punti)
- 💔 **Perdita di una Vita**
- ⏸️ **Blocco Temporaneo** (10 secondi di attesa)
- ☠️ **Game Over Immediato**

### 4. **Sistema di Progressione**
- 3 vite disponibili
- Il gioco termina con 3 errori o 0 vite
- +100 punti per ogni risposta corretta
- Classifica locale dei migliori punteggi

### 5. **Database Notizie**
- File JSON con notizie reali e fake news
- Ogni notizia include:
  - Testo della notizia
  - Verità (vera/falsa)
  - Spiegazione dettagliata
  - Fonte verificabile

## 🚀 Installazione

### Prerequisiti
- Python 3.7 o superiore
- pip (gestore pacchetti Python)

### Istruzioni

1. **Clona il repository:**
```bash
git clone https://github.com/elifkili19-design/FakeNews-Roulette.git
cd FakeNews-Roulette
```

2. **Installa le dipendenze:**
```bash
pip install -r requirements.txt
```

3. **Avvia il gioco:**
```bash
python fake_news_roulette.py
```

## 🎮 Come Giocare

1. **Menu Principale:** Clicca su "INIZIA" per cominciare
2. **Roulette:** Osserva la roulette girare e selezionare una categoria
3. **Leggi la Notizia:** Leggi attentamente la notizia presentata
4. **Rispondi:** Clicca su "VERA" o "FALSA"
5. **Feedback:** Leggi la spiegazione e la fonte della notizia
6. **Continua:** Clicca "CONTINUA" per il prossimo round

### Obiettivo
Accumula il punteggio più alto possibile evitando di:
- Fare 3 errori
- Perdere tutte le 3 vite

## 📂 Struttura del Progetto

```
FakeNews-Roulette/
├── fake_news_roulette.py    # File principale del gioco
├── news_database.json        # Database delle notizie
├── requirements.txt          # Dipendenze Python
├── .gitignore               # File da ignorare in Git
├── README.md                # Documentazione
└── leaderboard.json         # Classifica (generato automaticamente)
```

## 🔧 Configurazione

### Personalizzare il Database Notizie

Il file `news_database.json` può essere modificato per aggiungere nuove notizie:

```json
{
  "categories": {
    "NuovaCategoria": [
      {
        "text": "Testo della notizia",
        "is_true": true,
        "explanation": "Spiegazione dettagliata",
        "source": "Fonte verificabile"
      }
    ]
  }
}
```

### Modificare i Parametri di Gioco

Nel file `fake_news_roulette.py` è possibile modificare:
- `SCREEN_WIDTH` e `SCREEN_HEIGHT`: Dimensioni della finestra
- `FPS`: Frame per secondo
- Vite iniziali (nella funzione `reset_game()`)
- Numero massimo di errori
- Punteggi per risposte corrette/sbagliate

## 🎨 Tecnologie Utilizzate

- **Python 3**: Linguaggio di programmazione
- **Pygame 2.5.2**: Libreria per grafica e animazioni
- **JSON**: Formato per il database delle notizie

## 🔮 Sviluppi Futuri

Il progetto è progettato per essere estendibile:
- 🌐 Modalità multiplayer
- 🔌 Integrazione con API esterne per notizie in tempo reale
- 🏆 Sistema di achievement e badge
- 📊 Statistiche dettagliate per categoria
- 🌍 Supporto multilingua
- 🎵 Effetti sonori e musica di sottofondo

## 📝 Licenza

Questo progetto è open source e disponibile per scopi educativi.

## 👥 Contributi

I contributi sono benvenuti! Per contribuire:
1. Fai un fork del progetto
2. Crea un branch per la tua feature (`git checkout -b feature/AmazingFeature`)
3. Commit delle modifiche (`git commit -m 'Add some AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Apri una Pull Request

## 🐛 Segnalazione Bug

Per segnalare bug o richiedere nuove funzionalità, apri una issue su GitHub.

## 📧 Contatti

Per domande o suggerimenti, apri una issue nel repository.

---

**Divertiti imparando a riconoscere le fake news! 🎯📰**