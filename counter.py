from enum import Enum, auto


class AutoName(Enum):
    """Automatically sets an enum value to be its name when using auto()"""

    def _generate_next_value_(name, start, count, last_values):
        return name


class Status(AutoName):
    """Enum for different counter types"""
    increment = auto()
    decrement = auto()
    value = auto()
    next_value = auto()
    previous_value = auto()
    reset = auto()


class Meta(type):
    """Meta class for setting an attribute on class definition"""

    def counter():
        x = 0

        def inner(status):
            nonlocal x
            return_value = None
            if status == Status.increment:
                x += 1
                return_value = x
            elif status == Status.decrement:
                x -= 1
                return_value = x
            elif status == Status.value:
                return_value = x
            elif status == Status.next_value:
                return_value = x + 1
            elif status == Status.previous_value:
                return_value = x - 1
            elif status == Status.reset:
                x = 0
                return_value = x
            else:
                raise ValueError("counter status must be a Status Enum with one of the following values: {}".format(
                    ", ".join([x.value for x in Status])))
            return return_value

        return inner

    def __new__(self, class_name, bases, attrs):
        attrs['call_counter'] = self.counter()
        return type(class_name, bases, attrs)


class ClassProperty(property):
    """Subclass property to make classmethod properties possible"""

    def __get__(self, instance, owner):
        return self.fget.__get__(None, owner)(owner)


class Counter(metaclass=Meta):
    """Class for keeping track of an infinitely counting number"""

    def __init__(self):
        raise NotImplementedError("Cannot create instance of {0}".format(self.__class__.__name__))

    @ClassProperty
    def increment(cls):
        return cls.call_counter(Status.increment)

    @ClassProperty
    def decrement(cls):
        return cls.call_counter(Status.decrement)

    @ClassProperty
    def value(cls):
        return cls.call_counter(Status.value)

    @ClassProperty
    def next_value(cls):
        return cls.call_counter(Status.next_value)

    @ClassProperty
    def previous_value(cls):
        return cls.call_counter(Status.previous_value)

    @ClassProperty
    def reset(cls):
        return cls.call_counter(Status.reset)
