import sqlite3
from extras import field_type

class SqlResponse:
    def __init__(self, headers, table):
        self.headers = headers or []
        self.table = table or []

    def get_headers(self):
        return self.headers;

    def get_table(self):
        return self.table;

    def get_row(self, index):
        return self.table[index];

    def remove_row(self, index):
        self.table.remove(index)

    def get_column(self, header):
        index = self.headers.index(header)
        column = [];
        for i in range(len(self.table)):
            column.append(self.table[i][index])
        return column;

    def remove_column(self, header):
        index = self.headers.index(header)
        self.headers.remove(header)
        print("INDEX: ", index)
        column = [];
        for i in range(len(self.table)):
            column.append(self.table[i].pop(index))
        return column;

def sql_response_from_cursor(cursor):
    data = cursor.fetchall();
    table = [];
    headers = []
    types = []
    for i in cursor.description:
        headers.append(i[0]);
        types.append(i[1]);
    for tc in range(len(data)):
        row = []
        is_timestamp = types[tc] == field_type[7];
        for tr in data[tc]:
            if is_timestamp:
                tr = tr.strftime('%b %d %Y at %I:%M %p');
            row.append(tr);
        table.append(row);
    return SqlResponse(headers, table)