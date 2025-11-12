import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from bson.objectid import ObjectId

from database import db, create_document, get_documents
from schemas import Project, ContactMessage

app = FastAPI(title="Portfolio API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Portfolio API is running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
                response["connection_status"] = "Connected"
            except Exception as e:
                response["database"] = f"⚠️ Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️ Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:120]}"
    return response

# Seed a few demo projects on first call if empty
@app.post("/api/seed")
def seed_projects():
    try:
        count = db["project"].count_documents({}) if db else 0
        if count == 0:
            samples = [
                {
                    "title": "Neon Motion Landing",
                    "subtitle": "Framer Motion + Tailwind",
                    "description": "Experimental landing page with fluid scroll-based animations and glassmorphism.",
                    "tags": ["react", "framer-motion", "tailwind"],
                    "image_url": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?q=80&w=1200&auto=format&fit=crop",
                    "demo_url": "https://example.com/demo1",
                    "repo_url": "https://github.com/example/repo1",
                    "featured": True
                },
                {
                    "title": "AI Chat Orchestrator",
                    "subtitle": "FastAPI + LangGraph",
                    "description": "Multi-agent chat with tools, memory, and streaming UI.",
                    "tags": ["python", "fastapi", "ai"],
                    "image_url": "https://images.unsplash.com/photo-1518779578993-ec3579fee39f?q=80&w=1200&auto=format&fit=crop",
                    "demo_url": "https://example.com/demo2",
                    "repo_url": "https://github.com/example/repo2",
                    "featured": False
                },
                {
                    "title": "E-commerce Headless UI",
                    "subtitle": "Next.js Storefront",
                    "description": "Headless commerce with product search, cart, and payments.",
                    "tags": ["nextjs", "stripe", "mongodb"],
                    "image_url": "https://images.unsplash.com/photo-1545235617-9465d2a55698?q=80&w=1200&auto=format&fit=crop",
                    "demo_url": "https://example.com/demo3",
                    "repo_url": "https://github.com/example/repo3",
                    "featured": False
                }
            ]
            for item in samples:
                create_document("project", item)
        return {"seeded": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/projects")
def list_projects(tag: Optional[str] = None):
    try:
        filter_q = {"tags": {"$in": [tag]}} if tag else {}
        docs = get_documents("project", filter_q)
        # Convert ObjectId to string
        for d in docs:
            if isinstance(d.get("_id"), ObjectId):
                d["_id"] = str(d["_id"])
        # Featured first
        docs.sort(key=lambda x: (not x.get("featured", False), x.get("title", "")))
        return {"items": docs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class ContactIn(ContactMessage):
    pass

@app.post("/api/contact")
def submit_contact(payload: ContactIn):
    try:
        insert_id = create_document("contactmessage", payload)
        return {"ok": True, "id": insert_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
