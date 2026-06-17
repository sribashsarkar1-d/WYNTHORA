from fastapi import FastAPI
import uvicorn

app = FastAPI(title="AI Services API")

@app.get("/api/ai/health")
def health_check():
    return {"status": "AI Services Engine is running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
