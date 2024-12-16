import pyodbc
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException

router = APIRouter()

# Koneksi ke database
def create_connection():
    server = 'DESKTOP-EDJB5J1\\SQLEXPRESS'
    database = 'academic'
    conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
    return pyodbc.connect(conn_str)

# Model Pydantic untuk data mahasiswa
class Mahasiswa(BaseModel):
    NIM: str
    Nama_Mahasiswa: str
    Kelas_Mahasiswa: str

@router.post("/", response_model=Mahasiswa)
def create_mahasiswa(mahasiswa: Mahasiswa):
    conn = create_connection()
    cursor = conn.cursor()
    query = "INSERT INTO Tabel_Mahasiswa (NIM, Nama_Mahasiswa, Kelas_Mahasiswa) VALUES (?, ?, ?)"
    try:
        cursor.execute(query, (mahasiswa.NIM, mahasiswa.Nama_Mahasiswa, mahasiswa.Kelas_Mahasiswa))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()
    return mahasiswa

@router.get("/{nim}", response_model=Mahasiswa)
def read_mahasiswa(nim: str):
    conn = create_connection()
    cursor = conn.cursor()
    query = "SELECT NIM, Nama_Mahasiswa, Kelas_Mahasiswa FROM Tabel_Mahasiswa WHERE NIM = ?"
    cursor.execute(query, (nim,))
    row = cursor.fetchone()
    if row:
        mahasiswa = Mahasiswa(NIM=row[0], Nama_Mahasiswa=row[1], Kelas_Mahasiswa=row[2])
    else:
        raise HTTPException(status_code=404, detail="Data mahasiswa  tidak ditemukan")
    conn.close()
    return mahasiswa

@router.put("/{nim}", response_model=Mahasiswa)
def update_mahasiswa(nim: str, mahasiswa: Mahasiswa):
    conn = create_connection()
    cursor = conn.cursor()
    query = "UPDATE Tabel_Mahasiswa SET Nama_Mahasiswa = ?, Kelas_Mahasiswa = ? WHERE NIM = ?"
    try:
        cursor.execute(query, (mahasiswa.Nama_Mahasiswa, mahasiswa.Kelas_Mahasiswa, nim))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Data mahasiswa tidak ditemukan")
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()
    return mahasiswa

@router.delete("/{nim}", response_model=dict)
def delete_mahasiswa(nim: str):
    conn = create_connection()
    cursor = conn.cursor()
    query = "DELETE FROM Tabel_Mahasiswa WHERE NIM = ?"
    try:
        cursor.execute(query, (nim,))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Data mahasiswa tidak ditemukan")
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()
    return {"message": "Data mahasiswa selesai dihapus"}
