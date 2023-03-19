from dotenv import load_dotenv
import os
import psycopg
import subprocess
import re
# from pprint import pprint


DEBUG = True
load_dotenv()


if __name__ == '__main__':
    regex = re.compile(r'time=(\d+\.\d+) ms')
    exit_code = subprocess.run(['ping', '-c', '3', 'google.com'], capture_output=True)
    match = regex.findall(exit_code.stdout.decode('utf-8'))
    if len(match) == 0:
        match = [0, 0, 0]
    if DEBUG:
        for i, interval in enumerate(match):
            print(f'index: {i}, interval: {float(interval)}')
    if DEBUG:
        print(exit_code.stdout.decode("utf-8"))
    query = """INSERT INTO ping(delay)
                   VALUES(%s)"""
    if DEBUG:
        print(f"os.getenv('DATABASE_DATABASE'): {os.getenv('DATABASE_DATABASE')}")
        print(f"os.getenv('DATABASE_USER'): {os.getenv('DATABASE_USER')}")
        print(f"os.getenv('DATABASE_HOST'): {os.getenv('DATABASE_HOST')}")
        print(f"os.getenv('DATABASE_PORT'): {os.getenv('DATABASE_PORT')}")
        print(f"os.getenv('DATABASE_PASSWORD'): {os.getenv('DATABASE_PASSWORD')}")

    with psycopg.connect(
            f"dbname={os.getenv('DATABASE_DATABASE')} "
            f"user={os.getenv('DATABASE_USER')} "
            f"host={os.getenv('DATABASE_HOST')} "
            f"port={os.getenv('DATABASE_PORT')} "
            f"password={os.getenv('DATABASE_PASSWORD')}") as conn:
        # Open a cursor to perform database operations
        with conn.cursor() as cur:
            for value in match:
                cur.execute(query, (value, ))
            conn.commit()
            if DEBUG:
                cur.execute("""SELECT * FROM ping
                    ORDER BY time DESC LIMIT 10;""")
                for record in cur:
                    print(record)

    if DEBUG:
        print(f'Process finished with exit code {exit_code.returncode}')
