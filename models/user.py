def get_user_by_id(user_id):
    conn = get_connection()
    user = conn.execute(
        "SELECT * FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()
    conn.close()
    return dict(user) if user else None


def update_user(user_id, name, email):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE users SET name = ?, email = ? WHERE id = ?",
        (name, email, user_id)
    )
    conn.commit()
    affected = cur.rowcount
    conn.close()
    return affected


def delete_user(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM users WHERE id = ?",
        (user_id,)
    )
    conn.commit()
    affected = cur.rowcount
    conn.close()
    return affected
