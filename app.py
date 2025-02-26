import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai

app = Flask(__name__)

# Allow CORS only for your Netlify frontend
CORS(app, resources={
    r"/generate-definition": {"origins": "https://gregarious-custard-a60b6a.netlify.app"},
    r"/": {"origins": "https://gregarious-custard-a60b6a.netlify.app"}
}, supports_credentials=True)

# Read OpenAI API Key from environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/")
def home():
    return "🚀 Backend is live and ready!"

@app.route("/generate-definition", methods=["POST"])
def generate_definition():
    data = request.get_json()
    word = data.get("word", "").strip()

    if not word:
        return jsonify({"error": "No se proporcionó ninguna palabra"}), 400

    # Prompt with Franny Choi-style reference
    prompt = f"""
Eres una poeta que escribe definiciones de palabras en un estilo evocador, similar al de Franny Choi. Aquí tienes ejemplos de su estilo:

ESTRELLA
Significado
brillante; antigua herida que sigo hasta casa
Véase también 
chispa; extraño; escritura; aguijón
Origen
mito; 
historias de una madre; asuntos estáticos
Sueños de ser
alcanzado

FANTASMA
Significado
contorno del silencio
Véase también 
sombra; fotografía; zumbido
Origen
todas las cosas engendran sus propios opuestos
Sueños de ser
relleno, o carne

BOCA
Significado
una entrada o una salida
Véase también 
pez; babosa; puño; bazofia; cualquier sinónimo de por favor
Origen
¿qué vino primero, la espada de la herida?
Sueños de ser
el mar

MAR
Significado
frío antepasado; útero sin sangre
Véase también 
canción del corazón; canción del enjambre; canción de la sal; devorador de canciones
Origen
N/A
Sueños de ser
N/A (no sueña, solo se imagina)

Ahora, siguiendo este estilo, genera una definición poética para la palabra '{word}' en el siguiente formato:

{{
  "significado": "...",
  "vease": "...",
  "origen": "...",
  "suenos": "..."
}}

Devuelve únicamente el JSON en este formato, sin ningún texto adicional.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.8
        )

        raw_text = response.choices[0].message.content.strip()

        # Debugging: Print OpenAI raw response
        print("🔥 OpenAI Raw Response:", raw_text)

        # Try parsing the response as JSON
        try:
            definition_json = json.loads(raw_text)
        except json.JSONDecodeError:
            print("🚨 OpenAI returned an invalid JSON:", raw_text)
            return jsonify({
                "error": "OpenAI did not return valid JSON.",
                "raw": raw_text
            }), 500

        return jsonify(definition_json)

    except Exception as e:
        print("🔥 ERROR:", str(e))  # This will appear in Render logs
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)