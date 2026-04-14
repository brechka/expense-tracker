import uvicorn
from src.config import PORT, HOST

if __name__ == "__main__":
    print(f"Server listening on port {PORT}")
    uvicorn.run("src.main:app", host=HOST, port=PORT, reload=True)
