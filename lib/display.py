"""
Display of information to player.

These are the functions which show the player what is happening in the game.
"""

from __future__ import print_function
import buy_menu
import data_constructor
import datetime
import json
import os
import placement
import printer
import time
import update
# DEBUG
# import pdb

try:
    input = raw_input
except NameError:
    pass


def store_data(data):
    """Purrsist the data."""
    # DEBUG
    # pdb.set_trace()
    data_file = os.getcwd() + '/var/data.json'
    with open(data_file, 'w') as f:
        json.dump(data, f)


def load_data():
    """Load the data."""
    data_file = os.getcwd() + '/var/data.json'
    with open(data_file, 'r') as f:
        data = json.load(f)
    return data


def prep_data_on_close(data):
    """Prepare data for game exit."""
    store_data(data)


def banner():
    """Welcome banner."""
    print("             {.RED}_{.ENDC}".format(printer.PColors, printer.PColors))
    print("            {.RED}| |                    _{.ENDC}".format(printer.PColors, printer.PColors))
    print(" {.YELLOW}____  _____| |  _ ___     _____ _| |_  ___ _   _ ____  _____{.ENDC}".format(printer.PColors, printer.PColors))
    print("{.GREEN}|  _ \| ___ | |_/ ) _ \   (____ (_   _)/___) | | |    \| ___ |{.ENDC}".format(printer.PColors, printer.PColors))
    print("{.BLUE}| | | | ____|  _ ( |_| |  / ___ | | |_|___ | |_| | | | | ____|{.ENDC}".format(printer.PColors, printer.PColors))
    print("{.PURPLE}|_| |_|_____)_| \_)___/   \_____|  \__|___/|____/|_|_|_|_____){.ENDC}\n".format(printer.PColors, printer.PColors))


"""
TODO: this should be remade but where we just take the time diff
and do itterative deletions to it until we get to some minimal
amt and store it, rather than this time left precomputation
"""


def compute_interactions(data):
    """Compute cat interactions."""
    cur_time = datetime.datetime.now()
    time_since = (cur_time - data["start"]).total_seconds()
    if time_since < data["food_remaining"]:
        data["food_remaining"] -= time_since
        return compute_with_food(time_since)
    else:
        time_w_food = data["food_remaining"]
        time_wo_food = time_since - time_w_food
        data["food_remaining"] = 0
        return compute_with_food(time_w_food)
    return compute


def desc_yard(data):
    """Describe current yard situation."""
    toys = [item for item in data["yard"]]
    printer.p(
        data["prefix"], "You have {0} total spaces on your lawn".format(6))
    # TODO: have this reflect size
    for toy in toys:
        occupants = toy["occupant"] or ["no one"]
        printer.p(
            data["prefix"], "You have a {0} being used by {1}".format(
                toy["name"], ", and ".join(occupants)))


def check_status(data):
    """Check status of items in yard."""
    placement.list_yard_items(data)


def collect_money(data):
    """Collect money left by cats."""
    if len(data["pending_money"]) == 0:
        printer.p("{.YELLOW}[$$$$$$]{.ENDC}".format(
            printer.PColors,
            printer.PColors), "Sorry, no cats have left you anything")
        return
    for i in range(len(data["pending_money"])):
        money = data["pending_money"].pop()
        printer.p("{.GREEN}[$$$$$$]{.ENDC}".format(
            printer.PColors,
            printer.PColors), "Yes! {0} left you {1} fish!".format(
            money[0], str(money[1])))
        data["s_fish"] += money[1]


def print_help(data):
    """Print the game help."""
    temp = "{.HELP}[Help!]{.ENDC}".format(
        printer.PColors, printer.PColors)
    printer.p(temp, "Welcome to Neko Atsume!")
    printer.p(temp, "In this game cats come to visit you and you feed them")
    printer.p(temp, "it's pretty cool, so you should play more")


def quit(data):
    """Quit the game."""
    data["want_to_play"] = False
    printer.p("{.BLUE}[Goodbye!]{.ENDC}".format(
        printer.PColors, printer.PColors), "Saving game! See you later!")
    prep_data_on_close(data)


def main():
    """Main game function."""
    try:
        data = load_data()
        data = update.update(data)
    except:
        # print(sys.exc_info())
        data_constructor.build_data()
        data = load_data()
    data["want_to_play"] = True
    data["start"] = time.time()
    actions = {"quit": quit,
               "look": check_status,
               "shop": buy_menu.menu,
               "yard": placement.menu,
               "collect money": collect_money,
               "check food": placement.check_food,
               "help": print_help}
    banner()
    data["prefix"] = "{.BLUE}[Welcome!]{.ENDC}".format(
        printer.PColors, printer.PColors)
    check_status(data)
    data["prefix"] = "[Main Menu]"
    while data["want_to_play"] is True:
        data["prefix"] = "{.MAIN}[Main Menu]{.ENDC}".format(
            printer.PColors, printer.PColors)
        printer.prompt(data["prefix"], actions.keys())
        inp = input("{0} Choose an action! ".format(data["prefix"]))
        # pdb.set_trace()
        if inp in actions:
            actions[inp](data)
            continue
        else:
            printer.invalid(data["prefix"])
