from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Ensure project root is importable when running this file directly from any cwd.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.database import create_user, get_user_by_username, init_db
from app.security import hash_password


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Initialize admin user for ESL demo")
    parser.add_argument("--username", default="admin", help="Admin username")
    parser.add_argument("--password", default="admin123", help="Admin password")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    init_db()

    existing = get_user_by_username(args.username)
    if existing:
        print(f"User '{args.username}' already exists (id={existing['id']}).")
        return

    user_id = create_user(args.username, hash_password(args.password))
    print(f"Created user '{args.username}' with id={user_id}.")


if __name__ == "__main__":
    main()
