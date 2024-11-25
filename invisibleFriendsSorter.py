import json
import random


class InvisibleFriendsSorter:

    def __init__(self, participants):
        self.participants = participants
        self.invisible_friends = []
        self.first_friend = None

    def get_invisible_friends(self):
        sorted_friends = None
        while sorted_friends == None:
            try:
                sorted_friends = self.sort_invisible_friends()
            except Exception as e:
                print("Error:", e, "Retrying")
        return sorted_friends

    def sort_invisible_friends(self):
        # participants names
        available_receivers = [participant["name"] for participant in self.participants]

        # make sure if participants doesn't have blacklist to add blacklist=[]
        for participant in self.participants:
            if "blacklist" not in participant:
                participant["blacklist"] = []

        # random positions then sort blacklist by who has more receivers
        random.shuffle(self.participants)
        self.participants.sort(key=lambda x: len(x["blacklist"]), reverse=True)

        for i in range(0, len(self.participants)):
            participant = self.participants[i]

            possible_receivers = [
                receiver
                for receiver in available_receivers
                if receiver not in participant["blacklist"]
                and receiver not in participant["name"]
            ]

            if possible_receivers == []:
                raise Exception("No possible receivers.")

            receiver = random.choice(possible_receivers)

            available_receivers.remove(receiver)

            self.invisible_friends.append(
                {
                    "giver_email": participant["email"],
                    "giver_name": participant["name"],
                    "receiver": receiver,
                }
            )

        self.check_circular_sort()

        return self.invisible_friends

    def check_circular_sort(self):
        self.sorting_result = ""
        ARROW = "     |"

        def add_to_text(text):
            self.sorting_result += f"\n{text}"

        friends_to_print = self.invisible_friends.copy()
        current = friends_to_print.pop(0)

        add_to_text(current["giver_name"])
        add_to_text(ARROW)
        add_to_text(current["receiver"])
        isCircularSort = True

        while len(friends_to_print) > 0:
            # find the friend in friends to print that has the givername of currentfriend receiver
            current = next(
                (
                    friend
                    for friend in friends_to_print
                    if friend["giver_name"] == current["receiver"]
                ),
                None,
            )
            if current == None:
                isCircularSort = False
                add_to_text("     -")
                current = friends_to_print.pop(0)
                add_to_text(current["giver_name"])
            else:
                add_to_text(ARROW)
                add_to_text(current["receiver"])
                friends_to_print.remove(current)

        return isCircularSort, self.sorting_result


if __name__ == "__main__":

    # get participants from the JSON file
    with open("participants.json", "r", encoding="utf-8") as f:
        participants = json.load(f)

    isCircularSort = False
    sorting_result = ""
    tries = 0

    while not isCircularSort:
        tries += 1
        print("\ntry", tries)
        invisible_friends = InvisibleFriendsSorter(participants)
        friends = invisible_friends.get_invisible_friends()
        isCircularSort, sorting_result = invisible_friends.check_circular_sort()
        print("\nsorting:", sorting_result)

    print("\nsorting:", sorting_result)
    print("\ntries", tries)
