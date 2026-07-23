# Import db model, check queue
import sqlite3
import time

print("3 --- WORKER STARTING; WAITING FOR JOBS")

while True:
    pending_label = "Pending"
    processing_label = "Processing"
    with sqlite3.connect("app/upload-db.db") as connection:
        cursor = connection.cursor()
        select_all_query = "SELECT * FROM Videos WHERE status = ? ORDER BY id ASC LIMIT 1"

        cursor.execute(select_all_query, (pending_label,))
        
        video_record = cursor.fetchone()

        if video_record is None:
            time.sleep(1)
            continue

        video_id, filename, status, target_size_mb = video_record

        update_to_processing_query = "UPDATE Videos SET status = ? WHERE id = ?"

        cursor.execute(update_to_processing_query, (processing_label, video_id))
        connection.commit()

        print("--- WORKER ADDED JOB TO PROCESSING ---")