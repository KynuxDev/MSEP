from deepface import DeepFace
import cv2
import os
import requests
import numpy as np

class VisualCortex:
    def __init__(self):
        os.environ['DEEPFACE_HOME'] = ".deepface"

    def analyze_face(self, image_source):
        try:
            if image_source.startswith("http"):
                resp = requests.get(image_source, stream=True).raw
                img_array = np.asarray(bytearray(resp.read()), dtype="uint8")
                img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
                img_path = "temp_face_scan.jpg"
                cv2.imwrite(img_path, img)
            else:
                img_path = image_source

            print(f"[VisualCortex] Running Neural Net on: {image_source}")
            analysis = DeepFace.analyze(
                img_path=img_path, 
                actions=['age', 'gender', 'emotion', 'race'],
                enforce_detection=False,
                silent=True
            )
            
            if image_source.startswith("http") and os.path.exists(img_path):
                os.remove(img_path)

            if isinstance(analysis, list):
                result = analysis[0]
            else:
                result = analysis

            return {
                "status": "MATCH",
                "biometrics": {
                    "age": result.get('age'),
                    "gender": result.get('dominant_gender'),
                    "emotion": result.get('dominant_emotion'),
                    "race": result.get('dominant_race')
                },
                "confidence": result.get('face_confidence', 'N/A')
            }

        except Exception as e:
            return {
                "status": "FAILED",
                "error": str(e)
            }

    def verify_match(self, img1_path, img2_path):
        try:
            result = DeepFace.verify(img1_path, img2_path)
            return {
                "match": result["verified"],
                "similarity": 1 - result["distance"]
            }
        except Exception as e:
            return {"error": str(e)}


