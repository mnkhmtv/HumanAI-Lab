import argparse
import requests
import random
import names

# pip install names

BASE_URL = "http://localhost:8000"

# How this will be used
## to create
# python script.py --num_users 10 --min_age 18 --max_age 30
## to delete all
# python script.py --delete_all

# NOTE: for this task use requests library

def create_user(name, age, graduated):
    # TODO: create a user
    user_data = {"name": name, "age": age, "graduated": graduated}
    response = requests.post(f"{BASE_URL}/users", json=user_data)
    
    if response.status_code == 200:
        print(f"User created: {response.json()}")
    else:
        print(f"Failed to create user: {response.text}")


def delete_user(user_id):
    response = requests.delete(f"{BASE_URL}/users/{user_id}")
    
    if response.status_code == 200:
        print(f"Deleted user {user_id}")
    else:
        print(f"Failed to delete user {user_id}: {response.text}")

def delete_all_users():
    # TODO: Get all users and
    # call delete_user() for every user if status_code is success
    response = requests.get(f"{BASE_URL}/users")
    
    if response.status_code == 200:
        users = response.json()
        for user in users:
            delete_user(user["id"])
    else:
        print(f"Failed to fetch users: {response.text}")



def main(num_users, min_age, max_age):
    for _ in range(num_users):
        name = names.get_full_name()
        age = random.randint(min_age, max_age)
        graduated = random.choice([True, False])
        create_user(name, age, graduated)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate users and send requests to FastAPI endpoint."
    )

    # TODO: parse the following args --num_users, --min_age and --max_age with defauls 10, 18 and 30 respectively
    parser.add_argument("--num_users", type=int, default=10, help="Number of users to create")
    parser.add_argument("--min_age", type=int, default=18, help="Minimum age")
    parser.add_argument("--max_age", type=int, default=30, help="Maximum age")
    parser.add_argument("--delete_all", action="store_true", help="Delete all users from the system")
    
    args = parser.parse_args()

    if args.min_age > args.max_age:
        print("Error: min_age should be less than or equal to max_age")
    elif args.delete_all:
        delete_all_users()
    else:
        main(args.num_users, args.min_age, args.max_age)