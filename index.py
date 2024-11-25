import json
from emailCreator import Email
from invisibleFriendsSorter import InvisibleFriendsSorter
from constants import ONLY_CIRCULAR_SORT
import random


def main():
    try:
        with open("participants.json", "r", encoding="utf-8") as f:
            participants = json.load(f)
    except FileNotFoundError:
        print("File not found")
        return None

    if not validate_participants(participants):
        return None

    sortings = create_invisible_friends(participants)

    for sorting in sortings:
        giver_first_name = sorting["giver_name"].split(" ")[0]
        email = Email(sorting["giver_email"], giver_first_name, sorting["receiver"])
        email.create_email()
        email.send_email()


def create_invisible_friends(participants):
    invisible_friends = []

    if not ONLY_CIRCULAR_SORT:
        sorter = InvisibleFriendsSorter(participants)
        invisible_friends = sorter.get_invisible_friends()
    else:
        isCircularSort = False
        tries = 0
        while not isCircularSort:
            tries += 1
            sorter = InvisibleFriendsSorter(participants)
            invisible_friends = sorter.get_invisible_friends()
            isCircularSort, sorting_result = sorter.check_circular_sort()

        print("\ntries:", tries)
        print("\n# friends:", len(invisible_friends))

    # shuffled again so you don't see sending order 
    return random.shuffle(invisible_friends)


def validate_participants(participants):
    for participant in participants:
        if (
            "email" not in participant
            or participant["email"] == ""
            or "name" not in participant
            or participant["name"] == ""
        ):
            print(f"All objects in JSON must include name and email. Cannot continue.")
            return False

    return True


if __name__ == "__main__":
    main()
