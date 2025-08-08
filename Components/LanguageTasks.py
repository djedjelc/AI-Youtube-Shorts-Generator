import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API"))

if not client.api_key:
    raise ValueError("API key not found. Make sure it is defined in the .env file.")


# Function to extract list of (start,end)

def extract_segments(json_string):
    try:
        data = json.loads(json_string)
        segments = []
        for item in data:
            start_time = int(float(item["start"]))
            end_time = int(float(item["end"]))
            segments.append((start_time, end_time))
        return segments
    except Exception as e:
        print(f"Error in extract_segments: {e}")
        return []


system = """

En te basant sur la transcription (chaque ligne contient <start> - <end>: <texte>), sélectionne les **moments les plus intéressants** pouvant être transformés en shorts.

Retourne UNE LISTE JSON où chaque élément décrit un clip continu :
[
  {
    "start": "début en secondes",
    "end": "fin en secondes",
    "content": "texte du highlight"
  },
  ...
]

Contraintes :
• 3 extraits maximum (moins si le contenu est limité).
• Chaque extrait doit durer **60 s** ou moins.
• Ne réponds qu’avec la liste JSON, sans commentaire.
"""

User = """
Any Example
"""


def GetHighlight(Transcription):
    print("Getting Highlight from Transcription ")
    try:
        response = client.chat.completions.create(
            model="gpt-4o-2024-05-13",
            temperature=0.7,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": Transcription},
            ],
        )

        json_string = response.choices[0].message.content
        json_string = json_string.replace("json", "").replace("```", "")
        segments = extract_segments(json_string)
        return segments
    except Exception as e:
        print(f"Error in GetHighlight: {e}")
        return []


if __name__ == "__main__":
    print(GetHighlight(User))
