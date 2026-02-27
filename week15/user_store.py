# IMPORTANT: Placeholders in SQL statements use "?" instead of f"{}" --> safe from SQL injection. 
import sqlite3

''' 
Hint "Extra Comma": 
- In Python, a single value in parentheses needs that trailing comma to be recognized as a Tuple, 
  which is what SQLite requires.

Examples:
find_by_id()
- ... (id,)).fetchone()

search()
- ... (search_query,)).fetchall()
'''

class UserStore:
    def __init__(self, db_path):
        self.db_path = db_path
        self._create_table()    # Create the table automatically when the app starts.

    def _get_connection(self):
        # Helper to get a connection where rows behave like dictionaries.
        conn = sqlite3.connect(self.db_path)    # SQLite will automatically create the file if it doesn't exist yet. 
        conn.row_factory = sqlite3.Row
        return conn

    def _create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        );
        """
        with self._get_connection() as conn:    # handles closing the connection automatically.
            conn.execute(query)
            conn.commit()   # Ensure the table creation is saved.
            print(f"DEBUG: Database table 'users' is ready.")

    # returns a list of user dictionaries
    def load(self):
        with self._get_connection() as conn:
            rows = conn.execute("SELECT * FROM users").fetchall()

            if rows: 
                print(f"DEBUG: Loaded {len(rows)} users from database.")
            else:
                print("DEBUG: Loaded 0 users (Database is empty).")
            # Convert SQLite rows into a list of dictionaries for FastAPI
            return [dict(row) for row in rows]

    # returns user dict or None
    def find_by_id(self, id):
        with self._get_connection() as conn:
            row = conn.execute("SELECT * FROM users WHERE id = ?", (id,)).fetchone()
            if row:
                print(f"DEBUG: Found user: {row['name']}")
                return dict(row)
            print(f"DEBUG: User search failed. ID {id} does not exist.")
            return None

    def search(self, q):
        # We use '%' around the query to find matches anywhere in the string.
        search_query = f"%{q}"
        query = "SELECT * FROM users WHERE name LIKE ?"
        
        with self._get_connection() as conn:
            rows = conn.execute(query, (search_query,)).fetchall()
            results = [dict(row) for row in rows]

            if results:
                print(f"DEBUG: Search for '{q}' found {len(results)} results.")
            else: 
                print(f"DEBUG: SQL Search for '{q}' found {len(results)} results.")
            return results

    # replaces save() for updating users in the database.
    def update_user(self, id, updated_user):
        query = "UPDATE users SET name = ?, email = ? WHERE id = ?"
        
        with self._get_connection() as conn:
            result = conn.execute(query, (updated_user.name, updated_user.email, id))
            conn.commit()   # Saves the changes.
            # If no rows were changed, the user wasn't found
            if result.rowcount == 0:
                print(f"DEBUG: UPDATE FAILED. User ID {id} not found.")
                return None
        
        print(f"DEBUG: Successfully UPDATED user ID {id}.")
        # Return the updated user dictionary
        return {"id": id, "name": updated_user.name, "email": updated_user.email}

    def delete_user(self, id):
        query = "DELETE FROM users WHERE id = ?"
        
        with self._get_connection() as conn:
            result = conn.execute(query, (id,))
            conn.commit()   # Saves the deletion.

            # rowcount will be 1 if someone was deleted, 0 if not
            if result.rowcount > 0:
                print(f"DEBUG: Successfully DELETED user with ID {id}.")
                return True
            
        print(f"DEBUG: DELETE FAILED. User ID {id} not found.")
        return False
    
    # replaces save() for inserting users in the database.
    def add_user(self, user_in):
        query = "INSERT INTO users (name, email) VALUES (?, ?)"

        with self._get_connection() as conn:
            cursor = conn.execute(query, (user_in.name, user_in.email))
            conn.commit()   # Saves the new user permanently.
            new_id = cursor.lastrowid   # Get the ID SQLite just created.

        print(f"DEBUG: Successfully added user '{user_in.name}' with ID '{new_id}'.")
        return {"id": new_id, "name": user_in.name, "email": user_in.email}