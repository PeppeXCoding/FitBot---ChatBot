# 💪 FitBot - Your AI Gym Bro

A Python and Streamlit-powered virtual assistant that tracks your daily meals, visualizes your macronutrients, and motivates you like a true workout partner! 

Whether you need a detailed table of your macros or scientifically-backed advice for your next gym session, FitBot is here to spot you.

## 🛠️ How to run FitBot locally

Follow these simple steps to get your AI assistant up and running on your machine:

1. **Get the code:** Clone this repository or download the ZIP file.
2. **Install dependencies:** Open your terminal in the project folder and run:
   ```bash
   pip install streamlit google-generativeai pandas plotly python-dotenv
   ```
3. **Set up your API Key:**
   - Get a free API key from [Google AI Studio](https://aistudio.google.com/).
   - Create a file named exactly `.env` in the root folder of the project.
   - Add this single line inside the file: `GEMINI_API_KEY=your_api_key_here`
4. **Start the workout!** Run the app by typing:
   ```bash
   streamlit run app.py
   ```
Created by: Madeo Giuseppe
