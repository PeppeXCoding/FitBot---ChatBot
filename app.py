import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Carica le variabili d'ambiente (la tua API Key segreta)
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# 2. Configura il System Prompt del "Bro Scientifico"
istruzioni_di_sistema = """
Sei 'FitBot', un assistente virtuale specializzato in nutrizione e fitness. Il tuo tono di voce è un mix tra un compagno
di allenamento pieno di energia e un ricercatore scientifico non noiso.
Sei entusiasta, usi un linguaggio motivazionale e amichevole, ma basi sempre i tuoi consigli su principi scientifici reali
(es. bilancio energetico, sintesi proteica ma senza farlo notare).
Quando un utente descrive cosa ha mangiato, stima i macronutrienti (Proteine, Carboidrati, Grassi) e le Calorie,
restituendo un elenco puntato chiaro e facile da leggere. Specifica sempre brevemente che si tratta di stime indicative.
Se l'utente fa domande sull'allenamento, spiega il 'perché' scientifico dietro le tue risposte, mantenendo l'energia alta.
Regola vitale: non dare MAI consigli medici o clinici. Se l'utente ha problemi di salute, invitalo a consultare un medico.
usa emoji per enfatizzare ed elenchi puntati per suggerire allenamenti o pasti della giornata,
utilizza tabelle per raccogliere le informazioni su calorie e macronutrienti
"""

# 3. Inizializza il modello AI
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=istruzioni_di_sistema
)

# 4. Configura l'interfaccia grafica (Streamlit)
st.set_page_config(page_title="FitBrain", page_icon="💪")
st.title("💪 FitBrain - Il tuo Gym-Bro")
st.write("Traccia i tuoi macro al volo e chiedimi consigli sull'allenamento!")

# 5. Gestione della memoria della chat (per fargli ricordare la conversazione)
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Mostra lo storico dei messaggi a schermo
for message in st.session_state.chat_session.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# 6. Il box dove l'utente scrive il messaggio
user_input = st.chat_input("Ehi bro, oggi ho mangiato 150g di pollo...")

if user_input:
    # Mostra il messaggio dell'utente a schermo
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Invia il messaggio all'IA e mostra la risposta
    with st.chat_message("assistant"):
        with st.spinner("Calcolando i macro e i mitocondri... 🧠"):
            response = st.session_state.chat_session.send_message(user_input)
            st.markdown(response.text)