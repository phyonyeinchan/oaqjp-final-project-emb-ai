"""Call the Watson NLP emotion service."""
import requests

URL = ("https://sn-watson-emotion.labs.skills.network/v1/"
       "watson.runtime.nlp.v1/NlpService/EmotionPredict")
HEADERS = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}


def emotion_detector(text_to_analyze):
    """Return emotion scores and the highest scoring emotion."""
    empty = dict.fromkeys(("anger", "disgust", "fear", "joy", "sadness",
                           "dominant_emotion"))
    if not isinstance(text_to_analyze, str) or not text_to_analyze.strip():
        return empty
    response = requests.post(URL, json={"raw_document": {"text": text_to_analyze}},
                             headers=HEADERS, timeout=30)
    if response.status_code == 400:
        return empty
    response.raise_for_status()
    emotions = response.json()["emotionPredictions"][0]["emotion"]
    result = {name: emotions[name] for name in
              ("anger", "disgust", "fear", "joy", "sadness")}
    result["dominant_emotion"] = max(result, key=result.get)
    return result
