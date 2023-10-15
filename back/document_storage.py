import sqlite3
import os
import datetime
from document import Document

def get_file_contents(file_path: str) -> str:
    if os.path.isfile(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                file_contents = f.read()
                return file_contents
        except Exception as e:
            print(f"Ошибка при обработке файла {file_path}: {str(e)}")

class DocumentStorage:
    def __init__(self,
                 db_path = "E:/Important/uchoba_rep/Indexation_module/back/database/documents_database.db",
                 documents_path = "E:/Important/uchoba_rep/Indexation_module/texts"
                ):
        self.db_connection = sqlite3.connect(db_path)
        self.cursor = self.db_connection.cursor()
        if len(self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='documents'").fetchall()) == 0:
            self.initialize_db()

        FILES_WITH_DATETIMES = []
        for filename in os.listdir(documents_path):
            CURR_DATETIME = datetime.datetime.today()
            FILE_CONTENTS = get_file_contents(os.path.join(documents_path, filename))
            FILES_WITH_DATETIMES.append((
                filename,
                FILE_CONTENTS,
                CURR_DATETIME.year,
                CURR_DATETIME.month,
                CURR_DATETIME.day,
                CURR_DATETIME.hour,
                CURR_DATETIME.minute
            ))
        self.cursor.executemany('INSERT INTO documents VALUES (?, ?, ?, ?, ?, ?, ?)', FILES_WITH_DATETIMES)
            
    def initialize_db(self):
        self.cursor.execute(
        '''
            CREATE TABLE documents (
                name TEXT,
                text TEXT,
                creation_year INTEGER,
                creation_month INTEGER,
                creation_day INTEGER,
                creation_hour INTEGER,
                creation_minute INTEGER
            )
        '''
        )

    def get_all_documents(self) -> list[Document]:
        return list(map(lambda dbRow: Document(
            dbRow[0],
            dbRow[1],
            datetime.datetime(dbRow[2], dbRow[3], dbRow[4], dbRow[5], dbRow[6])
        ), [row for row in self.cursor.execute('SELECT * FROM documents')]))