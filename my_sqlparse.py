import sqlparse


# # Split a string containing two SQL statements:
# raw = 'select * from foo; select * from bar;'
# statements = sqlparse.split(raw)
# print(statements)
#
# # Format the first statement and print it out:
# first = statements[0]
# print(sqlparse.format(first, reindent=True, keyword_case='upper'))
#
#
# # Parsing a SQL statement:
# parsed = sqlparse.parse('select * from foo')[0]
# print(parsed.tokens) # [<DML 'select' at 0x7f22c5e15368>, <Whitespace ' ' at 0x7f22c5e153b0>, <Wildcard '*' … ]


# def extract_table_and_columns(query):
#     # Проанализировать SQL-запрос
#     parsed = sqlparse.parse(query)
#     # print(parsed)
#     tables = []
#     columns = []
#     # Извлечь таблицы и колонки
#     # __import__("pprint").pprint(parsed[0].tokens)
#     for token in parsed[0].tokens:
#         if isinstance(token, sqlparse.sql.IdentifierList):
#             for identifier in token.get_identifiers():
#                 print(token, token.get_identifiers())
#                 # if "." in identifier.get_real_name():
#                 #     # Это колонка (table.column)
#                 #     columns.append(identifier.get_real_name())
#                 # else:
#                 #     # Это таблица
#                 #     tables.append(identifier.get_real_name())
#     return tables, columns
#
# def main():
#     sql_query = """
#         SELECT users.id, users.name, orders.order_id, COALSECE(orders.order_date, 'HELLO')
#         FROM users JOIN orders ON users.id = orders.user_id WHERE users.country = 'USA';
#         """
#     tables, columns = extract_table_and_columns(sql_query)
#     print("Tables:")
#     print(tables)
#     print("\nColumns:")
#     print(columns)
#
# if __name__ == "__main__":
#     main()


import sqlparse
import re

# Ваш SQL-запрос
sql_query = """
WITH t1 as (
    select 1 as id, '2' as name
)

SELECT users.id AS id, orders.order_id AS order_id, COALESCE(orders.order_date, 'HELLO') AS some_column
    , hex(to_binary(super_key, "utf-8")) as new_key
    , md5(CONCAT_WS(";",
        HEX(
            to_binary(super_key, "utf-8"))
             )) as new_key2

    , cast(any_col as STRING) as any_col
    , CONCAT_WS(";", col1, col2, col3) as col_x
FROM users JOIN orders ON users.id = orders.user_id WHERE users.country = 'USA';
"""

parsed = sqlparse.parse(sql_query)[0]

columns = {}
for token in parsed.tokens:
    if isinstance(token, sqlparse.sql.IdentifierList):
        columns = token.get_identifiers()
        break


result_dict = {}
for column in columns:
    match = re.search(r'hex\s*\(\s*to_binary', str(column), flags=re.IGNORECASE)
    print(bool(match), column)
    alias = column.get_alias() or column.get_name()
    expression = str(column)

    # Если выражение состоит только из имени поля, используем его же
    if len(expression.split()) == 1:
        result_dict[alias] = alias
    else:
        result_dict[alias] = expression.strip()

print('\n', result_dict)
