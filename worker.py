# Import db model, check queue
import sqlite3
import time
from app.queue_store import queue

print("Worker is acting and waiting for jobs...")

while True:
    if not queue:
        time.sleep(1)
        continue

    # pop off ID in list
    curr_video_id = queue.pop(0)

    with sqlite3.connect("app/upload-db.db") as connection:
        cursor = connection.cursor()
        select_all_query = "SELECT * FROM Videos WHERE id = ?"

        cursor.execute(select_all_query, (curr_video_id,))
        
        video_record = cursor.fetchone()

        print((f"Currently read Row ID: ", {video_record}))