"""Command-line log analyzer for the homework task 4."""

"""Console contact assistant with decorator-based input error handling."""

from functools import wraps


def input_error(func):
    """Translate expected handler exceptions into user-friendly messages."""
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except ValueError as exc:
            return str(exc) or "Invalid arguments."
        except IndexError:
            return "Enter user name."

    return inner


def parse_input(user_input: str) -> tuple[str, list[str]]:
    parts = user_input.strip().split()
    if not parts:
        return "", []
    return parts[0].lower(), parts[1:]


@input_error
def add_contact(args: list[str], contacts: dict[str, str]) -> str:
    if len(args) != 2:
        raise ValueError("Give me name and phone please.")
    name, phone = args
    contacts[name] = phone
    return "Contact added."


@input_error
def change_contact(args: list[str], contacts: dict[str, str]) -> str:
    if len(args) != 2:
        raise ValueError("Give me name and phone please.")
    name, phone = args
    if name not in contacts:
        raise KeyError(name)
    contacts[name] = phone
    return "Contact updated."


@input_error
def show_phone(args: list[str], contacts: dict[str, str]) -> str:
    name = args[0]  # Missing name raises IndexError for input_error.
    if len(args) != 1:
        raise ValueError("Give me only user name.")
    return contacts[name]  # Unknown contact raises KeyError.


@input_error
def show_all(args: list[str], contacts: dict[str, str]) -> str:
    if args:
        raise ValueError("The 'all' command does not take arguments.")
    if not contacts:
        return "No contacts saved."
    return "\n".join(f"{name}: {phone}" for name, phone in contacts.items())


@input_error
def say_hello(args: list[str], contacts: dict[str, str]) -> str:
    if args:
        raise ValueError("The 'hello' command does not take arguments.")
    return "How can I help you?"


@input_error
def say_goodbye(args: list[str], contacts: dict[str, str]) -> str:
    if args:
        raise ValueError("The exit command does not take arguments.")
    return "Good bye!"


def main() -> None:
    contacts: dict[str, str] = {}
    handlers = {
        "hello": say_hello,
        "add": add_contact,
        "change": change_contact,
        "phone": show_phone,
        "all": show_all,
        "close": say_goodbye,
        "exit": say_goodbye,
        "goodbye": say_goodbye,
    }

    print("Welcome to the assistant bot!")
    while True:
        try:
            command, args = parse_input(input("Enter a command: "))
        except (EOFError, KeyboardInterrupt):
            print("\nGood bye!")
            break

        if not command:
            print("Enter a command.")
            continue

        handler = handlers.get(command)
        if handler is None:
            print("Invalid command.")
            continue

        result = handler(args, contacts)
        print(result)
        if command in {"close", "exit", "goodbye"} and result == "Good bye!":
            break


if __name__ == "__main__":
    main()
