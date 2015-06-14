"""
This module contains a helper class for Django's field choices.
"""

from enum import Enum


class Choice(Enum):
    """
    Subclass of :class:`enum.Enum` that provides a method for building choices for Django fields and uses a string
    representation that can be used directly in model fields, lookups, etc.
    The name of the variable will be used as key for Django's choices representation, the value will be used as
    (translatable) string representation.
    An example of a Choice:
        class C(Choice):
            a = "an"
            b = "example"
        # The same thing, written as Django choices tuple:
        c = (
            ('a', "an"),
            ('b', "example"),
        )
        # If needed, the database value can be different from the attribute name (e.g. an int):
        class IntC(Choice):
            a = (0, "an")
            b = (1, "example")
        # As a tuple:
        int_c = (
            (0, "an"),
            (1, "example"),
        )
    Usage of Choice in a field definition:
        f = models.CharField(choices=C.choices(), default=C.a, max_length=1)
    Usage of Choice in a QuerySet:
        Model.objects.filter(attr=C.a)
        # The same thing when using the regular Enum API:
        Model.objects.filter(attr=C.a.value)
    Note: the `__str__` method is overridden to only output the variable name and not the class name to shorten the
    data that is stored in the database and make conversion from the database value to the Choice instance easier.
    Thus, `C.a == C(str(C.a))`.
    """

    @classmethod
    def choices(cls):
        """
        Formats this Enum as a Django choices compatible list of 2-tuples.
        Example:
            class C(Choice):
                a = "an"
                b = "example"
            C.choices() == [('a', "an"), ('b', "example")]
        Use a 2-tuple as attribute value to explicitly specify the database value:
            class IntC(Choice):
                a = (0, "an")
                b = (1, "example")
            IntC.choices() == [(0, "an"), (1, "example")]
        Values are not evaluated, so translatable strings using `ugettext` are safe to use.
        :return: A list of 2-tuples containing the name and value of each member.
        """
        choices = []

        for member in cls:
            if isinstance(member, (tuple, list)) and len(member) == 2:
                db_value, readable_name = member
            else:
                db_value = member.name
                readable_name = member.value

            choices.append((db_value, readable_name))

        return choices

    def __str__(self):
        # Return only the name to allow a choice to be used directly without the need of accessing `name` when using a
        # choice in QuerySets etc.
        return self.name

