"""
Legacy main.py - This file is kept for backward compatibility.
For new development, use: python run.py or uvicorn app.main:app --reload
"""
import uvicorn

if __name__ == "__main__":
    # Redirect to new app structure
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
