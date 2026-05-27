import requests
data = {
    "face_match": {"status": "success", "data": {"match_score": 92}},
    "liveness": {"status": "success", "data": {"is_live": True}},
    "mask": {"status": "success", "data": {"has_mask": False}},
    "embedding": [0.12, -0.55, 0.91] * 170
}
response = requests.post('http://localhost:8000/verify', json=data)
result = response.json()
print("Trust Score:", result['trust_score'])
print("Status:", result['status'])
print("Embedding:", result['embedding'][:10], "...")