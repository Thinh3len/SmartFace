from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fraud_engine import calculate_trust_score, get_decision, get_reasons
from mock_data import MOCK_CASES

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.post("/verify")
async def verify(data: dict):
    try:
        score = calculate_trust_score(data)
        decision, icon, status = get_decision(score)
        return {"success": True, "decision": decision, "trust_score": score, "status": status, "icon": icon, "reasons": get_reasons(data), "embedding": data.get('embedding')}
    except Exception as e:
        return {"success": False, "decision": "FAIL", "error": str(e)}

@app.get("/mock/{case}")
async def mock(case: str):
    return MOCK_CASES.get(case, {"error": "Not found"})

@app.get("/health")
async def health():
    return {"status": "ok"}