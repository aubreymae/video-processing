# Import db model, check queue
import sqlite3
import time
import subprocess, os

print("3 --- WORKER STARTING; WAITING FOR JOBS")

pending_label = "Pending"
processing_label = "Processing"
completed_label = "Completed"
failed_label = "Failed"

def safe_remove(file_path):
    try:
        if os.path.exists(file_path):
            os.remove(uploads_path)
            print(f"--- DELETED INPUT FILE {filename} ---")
    except Exception as e:
        print(f"Cannot delete input file; file is missing.")

while True:
    with sqlite3.connect("app/upload-db.db") as connection:
        cursor = connection.cursor()

        # Get pending job
        select_query = "SELECT * FROM Videos WHERE status = ? ORDER BY id ASC LIMIT 1"
        cursor.execute(select_query, (pending_label, ))
        video_record = cursor.fetchone()

        if video_record is None:
            time.sleep(1)
            continue

        video_id, filename, status, target_size_mb = video_record

        # Transition to processing
        update_status_query = "UPDATE Videos SET status = ? WHERE id = ?"
        cursor.execute(update_status_query, (processing_label, video_id))
        connection.commit()
        print(f"--- WORKER STARTED JOB {video_id} ---")

        try:
            input_file_path = f"app/uploads/"
            output_file_path = f"app/processed/"

            uploads_path = os.path.join(input_file_path, filename)
            processed_path = os.path.join(output_file_path, f"compressed_{video_id}{os.path.splitext(filename)[1]}")

            if os.path.exists(uploads_path) is False:
                raise Exception("Input file path cannot find original video.")

            # CLI command
            command = [
                "ffmpeg",
                "-i", uploads_path,
                "-y",
                processed_path
            ]

            result = subprocess.run(command, capture_output=True, text=True, check=True)

            # Transition to completed
            cursor.execute(update_status_query, (completed_label, video_id))
            connection.commit()
            print(f"--- WORKER COMPLETED JOB {video_id} ---")

            safe_remove(uploads_path)

        except Exception as e:
            # Transition to failed if work crashes
            cursor.execute(update_status_query, (failed_label, video_id))
            connection.commit()
            print(f"--- WORKER FAILED JOB {video_id}: {e} ---")

            safe_remove(processed_path)