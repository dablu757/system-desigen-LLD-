def print_number(lowest: int, highest: int):
    print("== Job Processing Started ==")

    if lowest > highest:
        raise ValueError("lowest must be <= highest")

    for x in range(lowest, highest + 1):
        print(x)

    print("== END ==")

    return {
        "status": "completed",
        "range": [lowest, highest]
    }

