import Database as db
import Variables as var
import librosa
import os



ids = db.execute_query('SELECT id, filename FROM song WHERE duration is NULL;')

for id, filename in ids:
    file = os.path.join(var.WAV_DIR, filename)
    duration = int(librosa.get_duration(filename=file))
    print(id, filename, duration)
    db.execute_query('UPDATE song SET duration = ? WHERE id = ?', params=(duration, id))