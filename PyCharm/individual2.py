import json
import sys
import jsonschema

# JSON Schema, описывающая структуру данных для маршрутов
ROUTE_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "start_point": {"type": "string"},
            "end_point": {"type": "string"},
            "route_number": {"type": "integer"}
        },
        "required": ["start_point", "end_point", "route_number"]
    }
}

def load_routes(file_name):
    try:
        with open(file_name, 'r') as f:
            routes = json.load(f)
            validate_routes(routes)  # Валидация загруженных данных
            return routes
    except FileNotFoundError:
        return []

def validate_routes(routes):
    validator = jsonschema.Draft7Validator(ROUTE_SCHEMA)
    errors = list(validator.iter_errors(routes))
    if errors:
        for error in errors:
            print(error.message)

# Остальной код остается без изменений

def main():
    file_name = "routes.json"  # Имя файла для сохранения/загрузки данных
    routes = load_routes(file_name)

    while True:
        command = input(">>> ").lower()

        if command == 'exit':
            break
        elif command == 'add':
            add_route(routes)
        elif command == 'list':
            list_routes(routes)
        elif command.startswith('select '):
            # Разбить команду на части для выделения номера маршрута.
            parts = command.split(' ', maxsplit=1)

            try:
                # Получить требуемый номер маршрута.
                selected_route_number = int(parts[1])
                select_route(routes, selected_route_number)
            except ValueError:
                print("Ошибка: введите целое число после 'select'.")
        elif command == 'help':
            help_command()
        elif command == 'save':
            save_routes(file_name, routes)
            print(f"Данные сохранены в файл '{file_name}'.")
        else:
            print(f"Неизвестная команда {command}", file=sys.stderr)

if __name__ == '__main__':
    main()
