from fastapi import FastAPI

app = FastAPI(title="Hospital Management System", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "Hospital Management System API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "hospital-management"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
