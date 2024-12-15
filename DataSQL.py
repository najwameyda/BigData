import pyodbc
import pandas as pd
import logging
import time
from concurrent.futures import ThreadPoolExecutor

# Konfigurasi logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.FileHandler("insert_log.log", mode='w'), logging.StreamHandler()])

# Fungsi untuk membuat koneksi ke database
def create_connection():
    server = 'DESKTOP-EDJB5J1\\SQLEXPRESS'
    database = 'academic'
    conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
    logging.info('Membuat koneksi ke database SQL Server')
    return pyodbc.connect(conn_str)

# Fungsi untuk memasukkan data mahasiswa ke tabel SQL secara batch kecil
def insert_data_in_sql(conn, dataframe):
    cursor = conn.cursor()
    data = [tuple(row) for row in dataframe.itertuples(index=False, name=None)]
    query = "INSERT INTO Tabel_Mahasiswa (NIM, Nama_Mahasiswa, Kelas_Mahasiswa) VALUES (?, ?, ?)"
    
    try:
        for row in data:
            cursor.execute(query, (row[0], row[1], row[2]))  # row[0] untuk NIM, row[1] untuk Nama_Mahasiswa, row[2] untuk Kelas_Mahasiswa
            logging.info(f"Memasukkan NIM: {row[0]}, Nama: {row[1]}, Kelas: {row[2]}")
        conn.commit()
    except Exception as e:
        logging.error(f"Error saat memasukkan data mahasiswa: {e}")

def process_batch(start_index, end_index, data_mahasiswa):
    batch_df = data_mahasiswa.iloc[start_index:end_index]
    conn = create_connection()
    insert_data_in_sql(conn, batch_df)
    conn.close()
    logging.info(f'Batch mulai dari index {start_index} sampai {end_index} berhasil diproses')

if __name__ == "__main__":
    logging.info('Memulai proses memasukkan data mahasiswa')
    data_mahasiswa = pd.read_excel('DataMahasiswa.xlsx')  # Membaca file Excel yang diperbarui

    batch_size = 100  # Ukuran batch 100 baris
    num_batches = len(data_mahasiswa) // batch_size + 1

    start_time = time.time()

    try:
        with ThreadPoolExecutor(max_workers=4) as executor:  # Menggunakan 4 thread
            futures = []
            for i in range(num_batches):
                start_index = i * batch_size
                end_index = min((i + 1) * batch_size, len(data_mahasiswa))
                futures.append(executor.submit(process_batch, start_index, end_index, data_mahasiswa))
            
            for future in futures:
                future.result()
        
        end_time = time.time()
        logging.info(f"Semua data mahasiswa berhasil dimasukkan ke dalam database SQL. Waktu yang dibutuhkan: {end_time - start_time} detik")
    except Exception as e:
        logging.error(f"Terjadi kesalahan: {e}")
