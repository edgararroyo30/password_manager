"""
Methods that helps to give format to strings.
And convert other data types to string and modify it.
"""


class FormatString:

    """
    Allow auto formating for strings.
    Mainly for list -> str
    """

    def __init__(self):
        pass

    def iterate(self, argument):
        """
        Eliminate [], (), ",". " ' "
        From tuples and create a list.

        Argument:
        argument -> List
        """

        list = []
        for string in argument:
            string = str(string)
            string = string.strip("[]")
            string = string.strip("()")
            string = string.strip(",")
            string = string.strip("'")

            list.append(string)

        return list

    def iterate_first_value(self, argument):
        """
        Iterate a list with two values.
        And return only the first value.

        Argument:
        argument -> List
        """

        list = []
        for value in argument:
            value1, value2 = value
            list.append(value1)
        return list

    def iterate_second_value(self, argument):
        """
        Iterate a list with two values.
        And return only the second value.

        Argument:
        argument -> List
        """
        list = []
        for value in argument:
            value1, value2 = value
            list.append(value2)

        return list

    def format(self, string, level):
        """
        Delete elements for a listed string.
        Level represents how many elements are striped

        Arguments:
        string -> str, list
        level -> int
        """

        string = str(string)
        if level == 1:
            string = string.strip("[]")
        elif level == 2:
            string = string.strip("[]")
            string = string.strip("()")

        elif level == 3:
            string = string.strip("[]")
            string = string.strip("()")
            string = string.strip(",")

        elif level == 4:
            string = string.strip("[]")
            string = string.strip("()")
            string = string.strip(",")
            string = string.strip("'")

        elif level == 5:
            string = string.strip("[]")
            string = string.strip("()")
            string = string.strip(",")
            string = string.strip("'")
            if string[-1] == '3':
                string = string[:-4]

        return string
