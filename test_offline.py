"""Offline contract tests; these do not measure Watson accuracy."""
import unittest
from unittest.mock import Mock, patch
import requests
from EmotionDetection import emotion_detector
from server import app

class OfflineTests(unittest.TestCase):
    def test_format_and_dominant(self):
        for dominant in ("anger", "disgust", "fear", "joy", "sadness"):
            scores = {name: 0.1 for name in ("anger", "disgust", "fear", "joy", "sadness")}
            scores[dominant] = 0.9
            response = Mock(status_code=200)
            response.json.return_value = {"emotionPredictions": [{"emotion": scores}]}
            with patch("EmotionDetection.emotion_detection.requests.post", return_value=response) as post:
                result = emotion_detector("Feedback")
                self.assertEqual(result, dict(scores, dominant_emotion=dominant))
                self.assertEqual(post.call_args.kwargs["json"], {"raw_document": {"text": "Feedback"}})
    def test_bad_request(self):
        with patch("EmotionDetection.emotion_detection.requests.post", return_value=Mock(status_code=400)):
            self.assertTrue(all(v is None for v in emotion_detector("invalid").values()))
    def test_blank(self):
        with patch("EmotionDetection.emotion_detection.requests.post") as post:
            self.assertTrue(all(v is None for v in emotion_detector(" ").values()))
            post.assert_not_called()
    def test_web_blank(self):
        response = app.test_client().get("/emotionDetector?textToAnalyze=")
        self.assertEqual(response.data.decode(), "Invalid text! Please try again!")
    def test_web_success(self):
        with patch("server.emotion_detector", return_value=dict(anger=.1, disgust=.1, fear=.1, joy=.9, sadness=.1, dominant_emotion="joy")):
            response = app.test_client().get("/emotionDetector?textToAnalyze=happy")
            self.assertIn("The dominant emotion is joy.", response.data.decode())
    def test_service_failure(self):
        with patch("server.emotion_detector", side_effect=requests.ConnectionError()):
            self.assertEqual(app.test_client().get("/emotionDetector?textToAnalyze=test").status_code, 503)
    def test_home(self):
        self.assertEqual(app.test_client().get("/").status_code, 200)

if __name__ == "__main__":
    unittest.main()
