"""Flask web interface for Watson NLP emotion detection."""
import requests
from flask import Flask, render_template, request
from EmotionDetection import emotion_detector

app = Flask(__name__)


@app.route("/")
def index():
    """Render the input form."""
    return render_template("index.html")


@app.route("/emotionDetector")
def detect_emotion():
    """Analyze customer feedback and render a readable result."""
    text = request.args.get("textToAnalyze", "")
    try:
        result = emotion_detector(text)
    except (requests.RequestException, ValueError, KeyError, IndexError, TypeError):
        return "Emotion detection service is unavailable. Please try again later.", 503
    if result["dominant_emotion"] is None:
        return "Invalid text! Please try again!"
    return (
        f"For the given statement, the system response is 'anger': {result['anger']}, "
        f"'disgust': {result['disgust']}, 'fear': {result['fear']}, "
        f"'joy': {result['joy']} and 'sadness': {result['sadness']}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
