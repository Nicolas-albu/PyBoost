from io import TextIOWrapper


def toml_dump(obj: dict, file: TextIOWrapper) -> None:
    if not file.write:
        raise TypeError('You can only dump an object to a file descriptor')

    for key, value in obj.items():
        file.write(f'{key} = "{value}"\n')
