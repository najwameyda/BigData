import uvicorn
from fastapi import FastAPI
from DataCRUD import router as mahasiswa_router

app = FastAPI()

# Tambahkan router untuk endpoint mahasiswa
app.include_router(mahasiswa_router, prefix="/mahasiswa", tags=["mahasiswa"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
