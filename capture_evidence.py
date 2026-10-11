"""Run in the Skills Network lab to capture authentic submission evidence."""
from pathlib import Path
import subprocess
import sys
from EmotionDetection import emotion_detector

out = Path("evidence")
out.mkdir(exist_ok=True)
for filename, import_line in [
    ("2b_application_creation", "from EmotionDetection.emotion_detection import emotion_detector"),
    ("3b_formatted_output_test", "from EmotionDetection.emotion_detection import emotion_detector"),
    ("4b_packaging_test", "from EmotionDetection import emotion_detector"),
]:
    print(import_line)
    result = emotion_detector("I am so happy I am doing this.")
    content = import_line + "\n" + repr(result) + "\n"
    (out / (filename + ".txt")).write_text(content)
    print(result)
for filename, command in [
    ("5b_unit_testing_result", [sys.executable, "-m", "unittest", "-v", "test_emotion_detection.py"]),
    ("8b_static_code_analysis", [sys.executable, "-m", "pylint", "server.py"]),
]:
    completed = subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    (out / (filename + ".txt")).write_text(completed.stdout)
    print(completed.stdout)
    if completed.returncode:
        raise SystemExit(completed.returncode)
