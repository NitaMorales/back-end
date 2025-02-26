import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai

app = Flask(__name__)
CORS(app, resources={
    r"/generate-definition": {"origins": "https://gregarious-custard-a60b6a.netlify.app"},
    r"/": {"origins": "https://gregarious-custard-a60b6a.netlify.app"}
}, supports_credentials=True)

# Lee la clave de OpenAI desde la variable de entorno (no la incluyas en el código)
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/")
def home():
    return "¡Backend funcionando con OpenAI y formato Franny Choi!"

@app.route("/generate-definition", methods=["POST"])
def generate_definition():
    data = request.get_json()
    word = data.get("word", "").strip()

    if not word:
        return jsonify({"error": "No se proporcionó ninguna palabra"}), 400

    # Prompt con ejemplo de Franny Choi y la estructura requerida
    prompt = f"""
Eres una poeta al estilo de Franny Choi.
[ESTRELLA
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
pez: babosa; puño; bazofia; cualquier sinónimo de por favor
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
N/A (no sueña, solo se 
imagina)]

Ahora, para la palabra '{word}', describe su:
- significado ("significado")
- véase también ("vease")
- origen ("origen")
- sueños de ser ("suenos")

En forma breve, evocadora y relacionada específicamente con '{word}'.

Devuelve ÚNICAMENTE un JSON con la estructura:

{{
  "significado": "...",
  "vease": "...",
  "origen": "...",
  "suenos": "..."
}}

Sin texto adicional fuera de este JSON.
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # o "gpt-4" si lo tienes disponible
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.8  # Ajusta para mayor o menor creatividad
        )

        raw_text = response.choices[0].message.content.strip()

        # Parseamos la respuesta como JSON
        try:
            definition_json = json.loads(raw_text)
        except json.JSONDecodeError:
            return jsonify({
                "error": "La IA no devolvió un JSON válido.",
                "raw": raw_text
            }), 500

        return jsonify(definition_json)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)