
import requests
import json

from lib.logger import logger as base_logger

from config.settings import MEALIE_API_URL, MEALIE_TOKEN

logger = base_logger.getChild(__name__)

def create_receipe(json_receipe: str) -> bool | None:
    try:
        mealie_api = MEALIE_API_URL + "/api/recipes/create/html-or-json"
        
        parsed_json = json.loads(json_receipe)
        escaped_json = json.dumps(parsed_json, ensure_ascii=False)
        
        payload = {
            "data": escaped_json,
            "includeTags": True
        }
        headers = {
            "Authorization": f"Bearer {MEALIE_TOKEN}",
            "Content-Type": "application/json",
            "User-Agent": "Mealie-Reciper"
        }
        
        body = json.dumps(payload, ensure_ascii=False)
        
        resp = requests.post(
            url=mealie_api,
            data=body,
            headers=headers
        )
        if resp.status_code != 201:
            logger.error(f"🙁 Error creating Mealie receipe:\n{resp.json()}\n{json_receipe}")
            return False
        else:
            receipe_url = f"{MEALIE_API_URL}/g/home/r/{resp.json()}"
            logger.info(f"🎉 Mealie receipe was successfully created! {MEALIE_API_URL}/g/home/r/{resp.json()}")
            return receipe_url
    except Exception as e:
        logger.error(f"❌ There was an issue creating mMeali receipe\n{e}")
        raise
    
    