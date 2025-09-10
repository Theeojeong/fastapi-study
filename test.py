todo_data = {

    1: {
        "id": 1,
        "contents": "one",
        "is_done": True
    },
    
    2: {
        "id": 2,
        "contents": "two",
        "is_done": False
    },
    
    3: {
        "id": 3,
        "contents": "three",
        "is_done": False
    }
}

todo_data.pop(1)

print(todo_data)
