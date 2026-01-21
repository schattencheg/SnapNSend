import sqlite3
from typing import Optional
from contextlib import contextmanager
from ..models.user import User


class DatabaseManager:
    def __init__(self, db_path: str = "users.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        """Initialize the database and create tables if they don't exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Create users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    user_name TEXT UNIQUE NOT NULL,
                    user_mail TEXT UNIQUE NOT NULL,
                    created_at TEXT NOT NULL
                )
            ''')

            conn.commit()

    @contextmanager
    def get_connection(self):
        """Context manager for database connections."""
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()

    def create_user(self, user: User) -> bool:
        """Insert a new user into the database."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    '''INSERT INTO users (id, user_name, user_mail, created_at)
                       VALUES (?, ?, ?, ?)''',
                    (
                        str(user.id), user.user_name, user.user_mail,
                        user.created_at.isoformat()
                    )
                )
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            # This occurs if user_name or user_mail already exists
            # (due to UNIQUE constraint)
            return False

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Retrieve a user by their ID."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''SELECT id, user_name, user_mail, created_at
                   FROM users WHERE id = ?''',
                (user_id,)
            )
            row = cursor.fetchone()

            if row:
                from datetime import datetime
                return User(
                    id=row[0],
                    user_name=row[1],
                    user_mail=row[2],
                    created_at=datetime.fromisoformat(row[3])
                )
            return None

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Retrieve a user by their username."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''SELECT id, user_name, user_mail, created_at
                   FROM users WHERE user_name = ?''',
                (username,)
            )
            row = cursor.fetchone()

            if row:
                from datetime import datetime
                return User(
                    id=row[0],
                    user_name=row[1],
                    user_mail=row[2],
                    created_at=datetime.fromisoformat(row[3])
                )
            return None

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Retrieve a user by their email."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''SELECT id, user_name, user_mail, created_at
                   FROM users WHERE user_mail = ?''',
                (email,)
            )
            row = cursor.fetchone()

            if row:
                from datetime import datetime
                return User(
                    id=row[0],
                    user_name=row[1],
                    user_mail=row[2],
                    created_at=datetime.fromisoformat(row[3])
                )
            return None

    def user_exists_with_email(self, email: str) -> bool:
        """Check if a user exists with the given email."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT 1 FROM users WHERE user_mail = ?', (email,)
            )
            return cursor.fetchone() is not None

    def user_exists_with_username(self, username: str) -> bool:
        """Check if a user exists with the given username."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT 1 FROM users WHERE user_name = ?', (username,)
            )
            return cursor.fetchone() is not None

    def get_all_users(self) -> list[User]:
        """Retrieve all users from the database."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT id, user_name, user_mail, created_at FROM users'
            )
            rows = cursor.fetchall()

            users = []
            for row in rows:
                from datetime import datetime
                users.append(User(
                    id=row[0],
                    user_name=row[1],
                    user_mail=row[2],
                    created_at=datetime.fromisoformat(row[3])
                ))
            return users
