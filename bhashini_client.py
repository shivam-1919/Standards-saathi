"""
Bhashini Udyat / ULCA Client for Standards Saathi
Integrates National Language Translation Mission (NLTM) AI models for:
- Neural Machine Translation (IndicTrans2)
- Text-to-Speech (IndicTTS)
- Automatic Speech Recognition (IndicASR)
"""

import os
import base64
import requests
from typing import Optional, Dict, Any
from dotenv import load_dotenv

load_dotenv()

class BhashiniClient:
    CONFIG_URL = "https://meity-auth.ulcacontrib.org/ulca/apis/v0/model/getModelsPipeline"
    DEFAULT_PIPELINE_ID = "64392f96daac500b55c543cd"

    def __init__(self, user_id: Optional[str] = None, api_key: Optional[str] = None, inference_key: Optional[str] = None):
        self.user_id = user_id or os.getenv("BHASHINI_USER_ID", "").strip()
        self.api_key = api_key or os.getenv("BHASHINI_API_KEY", "").strip()
        self.inference_key = inference_key or os.getenv("BHASHINI_INFERENCE_KEY", "").strip()
        self._service_cache: Dict[str, Dict[str, Any]] = {}

    @property
    def is_configured(self) -> bool:
        return bool(self.user_id and self.api_key and self.inference_key)

    def _get_pipeline_config(self, task_type: str, source_lang: str, target_lang: Optional[str] = None) -> Dict[str, Any]:
        cache_key = f"{task_type}_{source_lang}_{target_lang}"
        if cache_key in self._service_cache:
            return self._service_cache[cache_key]

        headers = {
            "userID": self.user_id,
            "ulcaApiKey": self.api_key,
            "Content-Type": "application/json"
        }

        task_config: Dict[str, Any] = {"taskType": task_type}
        if task_type == "translation":
            task_config["config"] = {
                "language": {
                    "sourceLanguage": source_lang,
                    "targetLanguage": target_lang
                }
            }
        elif task_type in ["tts", "asr"]:
            task_config["config"] = {
                "language": {
                    "sourceLanguage": source_lang
                }
            }

        payload = {
            "pipelineTasks": [task_config],
            "pipelineRequestConfig": {
                "pipelineId": self.DEFAULT_PIPELINE_ID
            }
        }

        resp = requests.post(self.CONFIG_URL, json=payload, headers=headers, timeout=12)
        resp.raise_for_status()
        data = resp.json()

        service_id = data["pipelineResponseConfig"][0]["config"][0]["serviceId"]
        callback_url = data["pipelineInferenceAPIEndPoint"]["callbackUrl"]
        key_name = data["pipelineInferenceAPIEndPoint"]["inferenceApiKey"]["name"]
        key_val = data["pipelineInferenceAPIEndPoint"]["inferenceApiKey"]["value"] or self.inference_key

        result = {
            "service_id": service_id,
            "callback_url": callback_url,
            "key_name": key_name,
            "key_value": key_val
        }
        self._service_cache[cache_key] = result
        return result

    def translate(self, text: str, source_lang: str = "en", target_lang: str = "hi") -> str:
        """
        Translate text using Bhashini IndicTrans2 model.
        """
        if not text or not text.strip() or source_lang == target_lang:
            return text

        if not self.is_configured:
            return text

        try:
            cfg = self._get_pipeline_config("translation", source_lang, target_lang)
            headers = {
                cfg["key_name"]: cfg["key_value"],
                "Authorization": self.inference_key,
                "Content-Type": "application/json"
            }

            payload = {
                "pipelineTasks": [
                    {
                        "taskType": "translation",
                        "config": {
                            "language": {
                                "sourceLanguage": source_lang,
                                "targetLanguage": target_lang
                            },
                            "serviceId": cfg["service_id"]
                        }
                    }
                ],
                "inputData": {
                    "input": [{"source": text}]
                }
            }

            res = requests.post(cfg["callback_url"], json=payload, headers=headers, timeout=18)
            res.raise_for_status()
            res_json = res.json()
            return res_json["pipelineResponse"][0]["output"][0]["target"]
        except Exception as e:
            # Return original text gracefully on network timeout/error
            print(f"[Bhashini Translation Error]: {e}")
            return text

    def text_to_speech(self, text: str, lang: str = "hi", gender: str = "female") -> Optional[bytes]:
        """
        Synthesize speech audio from text using Bhashini IndicTTS.
        Returns raw audio bytes (WAV/MP3).
        """
        if not text or not text.strip() or not self.is_configured:
            return None

        try:
            cfg = self._get_pipeline_config("tts", lang)
            headers = {
                cfg["key_name"]: cfg["key_value"],
                "Authorization": self.inference_key,
                "Content-Type": "application/json"
            }

            payload = {
                "pipelineTasks": [
                    {
                        "taskType": "tts",
                        "config": {
                            "language": {"sourceLanguage": lang},
                            "serviceId": cfg["service_id"],
                            "gender": gender
                        }
                    }
                ],
                "inputData": {
                    "input": [{"source": text}]
                }
            }

            res = requests.post(cfg["callback_url"], json=payload, headers=headers, timeout=20)
            res.raise_for_status()
            base64_audio = res.json()["pipelineResponse"][0]["audio"][0]["audioContent"]
            return base64.b64decode(base64_audio)
        except Exception as e:
            print(f"[Bhashini TTS Error]: {e}")
            return None


# Global singleton instance
bhashini_client = BhashiniClient()
