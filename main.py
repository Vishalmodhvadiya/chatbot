from sys import exception
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google.genai.errors import ClientError
from app.services.gemini_service import get_gemini_response
from pydantic import BaseModel 

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins =["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_methods =["*"],
    allow_headers=["*"],
)
class ChatRequest(BaseModel):
    message: str
    session_id: str

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        reply = await get_gemini_response(request.message, request.session_id)
        return {"reply": reply}
    except ClientError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Gemini API error: {exc}"
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        ) from exc

@app.delete("/chat/{session_id}")
async def delete_session(session_id: str):
    try :  
        return {"message": f"session{session_id} deleted successfully"}
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="internal server error"
        )from exc
    
@app.get("/chat")
async def root():
    return 