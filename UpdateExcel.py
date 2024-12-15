import pandas as pd
import logging

# Konfigurasi logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Fungsi untuk menghasilkan data mahasiswa
def buat_data_mahasiswa(num_students):
    data = {
        'NIM': [f'NIM{i:06d}' for i in range(1, num_students + 1)],
        'Nama_Mahasiswa': [f'Nama_Mahasiswa{i}' for i in range(1, num_students + 1)],
        'Kelas_Mahasiswa': [f'Kelas_{(i - 1) // 30 % 10 + 1}' for i in range(1, num_students + 1)]
    }
    return pd.DataFrame(data)

# Jalankan fungsi untuk menghasilkan data mahasiswa dan simpan ke file Excel
if __name__ == "__main__":
    num_students = 1000000
    logging.info(f'Memulai proses pembuatan data untuk {num_students} mahasiswa')
    
    data_mahasiswa = buat_data_mahasiswa(num_students)
    
    # Menyimpan data ke file Excel
    file_path = 'DataMahasiswa.xlsx'  # Nama file Excel yang ingin diperbarui
    data_mahasiswa.to_excel(file_path, index=False)
    logging.info('Proses pembuatan data mahasiswa selesei dan berhasil disimpan dalam file DataMahasiswa.xlsx')
