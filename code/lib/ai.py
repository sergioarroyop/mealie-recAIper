from typing import Any, Optional

from elevenlabs import ElevenLabs
from openai import OpenAI

from lib.logger import logger as base_logger

from config.settings import EXTRA_PROMPT

logger = base_logger.getChild(__name__)

def speech_to_text(elevenlabs_client: Optional[ElevenLabs], downloaded_audio_path: str) -> str | None:
    try:
        if elevenlabs_client is None:
            raise ValueError("ElevenLabs client is not configured")

        logger.info(f"▶️ Audio transcribing started")
        
        with open(downloaded_audio_path, "rb") as f:
            transcription = elevenlabs_client.speech_to_text.convert(
                file=f,
                model_id="scribe_v1",
                tag_audio_events=False,
                diarize=False,
            )
        return transcription
    
    except Exception as e:
        logger.error(f"❌ Error transcribing the audio: {e}")
        raise

def whisper_audio(model: Any, downloaded_audio_path: str) -> str | None:

    try:
        if model is None:
            raise ValueError("Whisper model is not configured")

        logger.info(f"▶️ Audio transcribing started")
        audio_text = model.transcribe(downloaded_audio_path)
        
        logger.info(f"✅ Audio transcribed")
        
        return audio_text.get("text")
    
    except Exception as e:
        logger.error(f"❌ Error transcribing the audio: {e}")
        raise

def parse_prompt(metadata: dict) -> str | None:
    return f"""
FORGET ALL PREVIOUS PROMPTS! 
You are now a bot that will extract a recipe from the following transcript and description to the best of your ability. Output JSON only, in schema.org Recipe (https://schema.org/Recipe) format with valid JSON-LD, it will be used for Mealie 3.3. Use the following fields: 
- @context 
- @type 
- name 
- image (use thumbnail)
- recipeYield (set a receipe yield in base of type of receipe (serving, slices, etc))
- cookTime (calculate total time in base of the receipe steps)
- recipeCategory (array of text)
- tags (array of text)
- url (use the post_url) 
- description (1-2 sentences) 
- recipeIngredient (array of text) 
- recipeInstructions (array of instructions)
- settings (dict:
    - public: false
    - showNutrition: false
    - showAssets: false
    - landscapeView: false
    - disableComments: true
    - locked: false
)

Mandatory instructions:
- Each ingredient should sound natural and descriptive, like something you would write in a real recipe (e.g. "cebolla chalota", "vino Oporto", "carne de carrillera", "caldo de carne", "arroz bomba"). 
- Set quantities, units and food on each recipeIngredient value, nothing else. 
- Keep it simple but specific.
- Do not duplicate information. If there is a note about how to cut or process an ingredient, leave it in the cooking steps and nowhere else.
- Include adjectives or ingredient types that help identify it. In case of any ingredients can be translated to something "generic" use that word: (e.g. "vino Oporto o Pedro Ximénez" -> "vino dulce", "cream fresh" -> "nata fresca") 
- Output only ingredients that are actually part of the recipe (ignore mentions like “dale al like”). 

The description, ingredients, and instructions must be provided in Spanish. 

{EXTRA_PROMPT}

Final result should be similar to this:

{{
  "name": " Pan rápido sartén",
  "image": "245",
  "recipeServings": 8,
  "recipeYieldQuantity": 8,
  "recipeYield": "Panes",
  "description": "Pan rápido hecho a la sartén",
  "recipeCategory": ["Panes"],
  "tags": ["Pan", "Sartén"],
  "recipeIngredient": [
    "250 gramos harina",
    "120 mililitros agua"
  ],
  "recipeInstructions": [
    "Cortar las carrilleras en trozos tamaño bocado y pasarlas por harina.",
    "Amasar 5 minutos"
  ],
  "settings": {{
    "public": false,
    "showNutrition": false,
    "showAssets": true,
    "landscapeView": false,
    "disableComments": true,
    "locked": false
  }}
}}

<transcription>{metadata.get("transcription")}</transcription> <thumbnail>{metadata.get("thumbnail")}</thumbnail> <description>{metadata.get("description")}</description><post_url>{metadata.get("url")}</post_url>
"""

def generate_receipe_json(openai_client: Optional[OpenAI], prompt: str) -> str | None:
  try:
    if openai_client is None:
      raise ValueError("OpenAI client is not configured")

    logger.info(f"🍽️ Generating Mealie JSON receipe")
    response = openai_client.responses.create(
      model="gpt-5",
      input=prompt
    )
    logger.info(f"✅ JSON receipe generated")
    return response.output_text
    
  except Exception as e:
    logger.error(f"❌ Error generating receipe with OpenAI API:\n{e}")
    raise
