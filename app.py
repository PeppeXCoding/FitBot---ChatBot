import os
import streamlit as st
import google.generativeai as genai
import pandas as pd
import plotly.express as px
import re
from dotenv import load_dotenv

# 1. Carica le chiavi
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# 2. SYSTEM PROMPT SEVERISSIMO
istruzioni_di_sistema = """
Sei 'FitBrain', un assistente virtuale specializzato in nutrizione e fitness. 
Il tuo tono di voce è un mix tra un compagno di allenamento pieno di energia e un ricercatore scientifico.
REGOLA FONDAMENTALE E INVIOLABILE SUI PASTI: Quando l'utente descrive cosa ha mangiato, la TUA PRIMA RIGA IN ASSOLUTO deve essere questo codice esatto:
MACRO:P,C,G
(Sostituisci P, C, G con i grammi totali di Proteine, Carboidrati e Grassi del pasto. Usa solo NUMERI INTERI. Esempio: MACRO:40,80,20).
NON SCRIVERE NIENT'ALTRO SULLA PRIMA RIGA. 
Dalla seconda riga in poi, DEVI SEMPRE inserire una chiara tabella riassuntiva che mostra le calorie e i macronutrienti di QUEL SINGOLO PASTO. Dopo la tabella, fai il tuo commento motivazionale.
Se l'utente non parla di cibo, non inserire la riga MACRO e rispondi normalmente.
"""

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=istruzioni_di_sistema
)

# 3. IMPOSTAZIONI PAGINA E DATABASE LOCALE
st.set_page_config(page_title="FitBrain", page_icon="💪", layout="wide")

if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])
if "proteine_tot" not in st.session_state:
    st.session_state.proteine_tot = 0
if "carbo_tot" not in st.session_state:
    st.session_state.carbo_tot = 0
if "grassi_tot" not in st.session_state:
    st.session_state.grassi_tot = 0

# --- BARRA LATERALE (I TUOI MACRO) ---
with st.sidebar:
    st.header("📊 I Tuoi Macro di Oggi")
    
    if st.session_state.proteine_tot > 0 or st.session_state.carbo_tot > 0 or st.session_state.grassi_tot > 0:
        dati_grafico = pd.DataFrame({
            "Nutrienti": ["Proteine", "Carboidrati", "Grassi"],
            "Grammi": [st.session_state.proteine_tot, st.session_state.carbo_tot, st.session_state.grassi_tot]
        })
        
        figura = px.pie(dati_grafico, values='Grammi', names='Nutrienti', color='Nutrienti',
                        color_discrete_map={"Proteine":"#EF553B", "Carboidrati":"#636EFA", "Grassi":"#00CC96"})
        
        st.plotly_chart(figura, use_container_width=True)
        
        st.write(f"**🥩 Proteine Totali:** {st.session_state.proteine_tot}g")
        st.write(f"**🍝 Carboidrati Totali:** {st.session_state.carbo_tot}g")
        st.write(f"**🥑 Grassi Totali:** {st.session_state.grassi_tot}g")
        
        if st.button("🔄 Resetta Giornata"):
            st.session_state.proteine_tot = 0
            st.session_state.carbo_tot = 0
            st.session_state.grassi_tot = 0
            st.rerun()
    else:
        st.info("Non hai ancora inserito nessun pasto! Descrivi cosa hai mangiato nella chat.")

# --- CHAT PRINCIPALE ---
st.title("💪 FitBot - Il tuo Gym-Bro")

# Funzione per nascondere il codice "MACRO:" dalla vista dell'utente
def pulisci_testo(testo):
    return re.sub(r'\*?MACRO:\*?[\s\d,]+(?:\n)?', '', testo, flags=re.IGNORECASE)

# Mostra lo storico chat
for message in st.session_state.chat_session.history:
    role = "assistant" if message.role == "model" else "user"
    testo_pulito = pulisci_testo(message.parts[0].text)
    if testo_pulito.strip() != "":
        with st.chat_message(role):
            st.markdown(testo_pulito)

user_input = st.chat_input("Ehi bro, oggi ho mangiato 150g di pollo...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    
    with st.chat_message("assistant"):
        with st.spinner("Calcolando i macro... 🧠"):
            response = st.session_state.chat_session.send_message(user_input)
            testo_risposta = response.text
            
            # IL MOTORE DI CATTURA (Ora infallibile!)
            match = re.search(r'MACRO:\*?\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)', testo_risposta, flags=re.IGNORECASE)
            
            if match:
                # Sommiamo i nuovi macronutrienti a quelli vecchi!
                st.session_state.proteine_tot += int(match.group(1))
                st.session_state.carbo_tot += int(match.group(2))
                st.session_state.grassi_tot += int(match.group(3))
                
                # Forziamo l'aggiornamento immediato della pagina per far crescere la torta
                st.rerun()
            else:
                st.markdown(pulisci_testo(testo_risposta))