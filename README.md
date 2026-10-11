# AI-Based Emotion Detection Web Application

Author: Dr Phyo Nyein Chan

Final project for AI-Based Web Application Development and Deployment. This Flask application analyzes customer feedback using the IBM Watson NLP EmotionPredict service and returns anger, disgust, fear, joy, sadness, and dominant_emotion.

## Features

- EmotionDetection Python package
- Formatted emotion scores and dominant emotion
- Five live Watson classification tests
- Blank-input and HTTP 400 handling
- Flask interface on port 5000
- Service failure handling

## Run in the Skills Network lab

```bash
python3 -m pip install -r requirements.txt
python3 capture_evidence.py
python3 server.py
```

Open port 5000 with Launch Application.

## Validation

The supplied Skills Network screenshots show five live Watson tests passing, server.py pylint score 10.00/10, successful web analysis with joy as the dominant emotion, and blank input displaying `Invalid text! Please try again!`. Seven additional offline contract tests passed during preparation; they use mocked HTTP responses.

The Watson endpoint requires access from an appropriate lab environment. capture_evidence.py saves actual terminal results into evidence/. Screenshots are captured separately from the running application.
