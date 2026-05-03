import os
import json

password = "admin123"
api_key = "sk-1234567890abcdef"

def get_user(id):
    users = {"1": "Himanshi", "2": "John", "3": "Sara"}
    return users[id]

def divide(a, b):
    return a/b

def read_file(filename):
    f = open(filename)
    data = f.read()
    return data

def save_user_data(data):
    query = "SELECT * FROM users WHERE id = " + data
    return query

def calculate_average(numbers):
    total = 0
    for i in range(len(numbers)):
        total = total + numbers[i]
    avg = total / len(numbers)
    return avg

if __name__ == "__main__":
    print(get_user("1"))
    print(divide(10, 0))
    print(calculate_average([]))