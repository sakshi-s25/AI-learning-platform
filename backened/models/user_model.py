from database.database import get_connection

def create_user(name, email, password):
    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute("""
          INSERT INTO users (name, email, password)
          VALUES (?, ?, ?)
        """, (name, email, password))

        connection.commit()
        user_id = cursor.lastrowid

        return {
            "success": True,
            "user_id": user_id
        }

    except Exception as error:
        return {
            "success": False,
            "message": str(error)
        }

    finally:
        connection.close()

def get_user_by_email(email):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM users WHERE email = ?

    """, (email,))
    user = cursor.fetchone()
    connection.close()
    return user

def get_user_by_id(user_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM users WHERE id = ?

    """, (user_id,))
    user = cursor.fetchone()
    connection.close()
    return user

def update_user_profile(
        user_id,
        skills,
        learning_goal,
        study_time
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE users
        SET skills = ?,
           learning_goal = ?,
           study_time = ?
        WHERE id = ?

    """, (
        skills,
        learning_goal,
        study_time,
        user_id
    ))
    connection.commit()
    connection.close()
    return True