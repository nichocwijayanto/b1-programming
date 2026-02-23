login_attempts = [
    ("alice", "success"),
    ("bob", "failed"),
    ("bob", "failed"),
    ("charlie", "success"),
    ("bob", "failed"),
    ("alice", "failed")
]

failed_counts = {}

for user, attempt in login_attempts : 
    if attempt == "failed" :
        failed_counts[user] = failed_counts.get(user, 0) + 1

        if failed_counts[user] >= 3 :
            print(f"Checking login attempts...ALERT: User \'{user}\' has 3 failed login attempts.")
            print("Security check complete!")