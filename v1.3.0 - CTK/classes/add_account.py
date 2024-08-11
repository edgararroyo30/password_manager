
from classes.format_string import FormatString
from classes.number_counter import NumberCounter


class AddAccount:

    def __init__(self):
        pass


def add_account(self, frame, account_frame, fg_color, text_color):
    """
    Add the account name to the listed account frame
    """
    counter = NumberCounter()

    for account in get_account():
        account = FormatString.format(account, 4)

        add_to_frame = AddToFrame(frame, account_frame, fg_color, text_color)
        add_to_frame.set_values(song.title())
        add_to_frame.set_display(counter.increase_counter())
