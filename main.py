import uvicorn
# from pyngrok import ngrok

if __name__ == "__main__":
  uvicorn.run("server.api:app", host="0.0.0.0", port=3000, reload=True)
