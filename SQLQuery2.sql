SELECT TOP 20
    ID_Mahasiswa,
    NIM,
    Nama_Mahasiswa,
    Kelas_Mahasiswa,
    [1] AS Kalkulus,
    [2] AS Algoritma_dan_Pemrograman,
    [3] AS Statistika_dan_Probabilitas,
    [4] AS Matematika,
    [5] AS Struktur_Data,
    [6] AS Grafik_Komputer,
    [7] AS Jaringan_Komputer,
    [8] AS Pemrograman_Web,
    [9] AS Sistem_Basis_Data,
    [10] AS Bahasa_Inggris
FROM
(
    SELECT 
        m.ID_Mahasiswa,
        m.NIM,
        m.Nama_Mahasiswa,
        m.Kelas_Mahasiswa,
        n.ID_MataKuliah,
        n.Nilai
    FROM
        Tabel_Mahasiswa m
    JOIN
        Tabel_Nilai n ON m.ID_Mahasiswa = n.ID_Mahasiswa
) AS SourceTable
PIVOT
(
    MAX(Nilai)
    FOR ID_MataKuliah IN ([1], [2], [3], [4], [5], [6], [7], [8], [9], [10])
) AS PivotTable
ORDER BY 
    ID_Mahasiswa;
