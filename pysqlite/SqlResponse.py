import sqlite3
from extras import field_type
from datetime import datetime
from tabulate import tabulate


class SqlRow:
    def __init__(self, headers, row):
        self.headers = headers;
        self.row = row;
    def get(self, header):
        index = self.headers.index(header);
        return self.row[index];
    def __getitem__(self, item):
        return self.get(item);
    def __str__(self):
        return tabulate([self.row], self.headers, 'orgtbl');

class SqlResponse:
    def __init__(self, headers, table):
        self.headers = headers or []
        self.table = table or []

    def get_headers(self):
        return self.headers;

    def get_table(self):
        return self.table;

    def get_row(self, index):
        return SqlRow(self.headers, self.table[index]);

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

    def __len__(self):
        return len(self.table);

    def __str__(self):
        return tabulate(self.table, self.headers, 'orgtbl');


def sql_response_from_cursor(cursor):
    data = cursor.fetchall();
    table = [];
    headers = []
    for i in cursor.description:
        headers.append(i[0]);
    for tc in range(len(data)):
        row = []
        for tr in data[tc]:
            if isinstance(tr, (datetime)):
                tr = tr.strftime('%b %d %Y at %I:%M %p');
            row.append(tr);
        table.append(row);
    return SqlResponse(headers, table)