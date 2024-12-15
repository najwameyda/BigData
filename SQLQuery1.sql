-- Mengisi data nilai secara otomatis
DECLARE @max_mahasiswa_id INT = (SELECT MAX(ID_Mahasiswa) FROM Tabel_Mahasiswa);
DECLARE @max_matakuliah_id INT = (SELECT MAX(ID_MataKuliah) FROM Tabel_MataKuliah);
DECLARE @i INT = 1;
DECLARE @j INT;
DECLARE @nilai INT;

WHILE @i <= @max_mahasiswa_id
BEGIN
    SET @j = 1;
    WHILE @j <= @max_matakuliah_id
    BEGIN
        -- Membuat nilai secara otomatis dengan penambahan acak antara 50 hingga 100
        SET @nilai = 50 + ABS(CHECKSUM(NEWID()) % 51);
        INSERT INTO Tabel_Nilai (ID_Mahasiswa, ID_MataKuliah, Nilai) VALUES (@i, @j, @nilai);
        SET @j = @j + 1;
    END
    SET @i = @i + 1;
END
