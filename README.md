# FitBot---ChatBot
A chat-bot that will help you to trace your daily meals and your gym progress. You can ask for a table of macronutrients but also for help with gym exercise and wellness.
# 💪 FitBot - Il tuo GymBro

Un assistente virtuale in Python e Streamlit che calcola i tuoi macronutrienti e ti motiva come un vero compagno di allenamento!

## 🛠️ Come far partire l'app sul tuo PC

Per far funzionare FitBot in locale, segui questi semplici passaggi:

1. **Scarica il progetto:** Clona questo repository o scarica il file ZIP.
2. **Installa le dipendenze:** Apri il terminale nella cartella del progetto e scrivi:
   `pip install streamlit google-generativeai pandas plotly python-dotenv`
3. **Configura l'API Key:**
   - Vai su [Google AI Studio](https://aistudio.google.com/) e ottieni una chiave API gratuita.
   - Crea un file chiamato esattamente `.env` nella cartella principale del progetto.
   - Scrivi dentro il file: `GEMINI_API_KEY=la_tua_chiave_qui`
4. **Avvia l'allenamento!** Nel terminale, esegui il comando:
   `streamlit run app.py`