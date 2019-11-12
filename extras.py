import string, random

def table_to_html(table = [], table_type = 'table', table_class = 'table', table_header =  None,
        table_header_type =  'th',table_header_class = 'header', table_row_type = 'tr', table_row_class = 'row', 
        table_data_type = 'td', table_data_class = 'data', custom_links_class = 'link', custom_links_href = None):

    html = '<{0} class="{1}">'.format(table_type, table_class);
    if table_header is not None:
        html += '<{0} class="{1}">'.format(table_row_type, table_row_class)
        for header in table_header:
            html += '<{0} class="{1}">{2}</{0}>'.format(table_header_type, table_header_class, header.replace('_', ' '));
        html += '</{0}>'.format(table_row_type)
    for j in range(len(table)):
        if custom_links_href is not None:
            html += '<a class="{0}" href="{1}">'.format(custom_links_class, custom_links_href[j])
        else:
            html += '<{0} class="{1}">'.format(table_row_type, table_row_class);
        for i in range(len(table[j])):
            html += '<{0} class="{1}">{2}</{0}>'.format(table_data_type, table_data_class, str(table[j][i]));
        if custom_links_href is not None:
            html += '</a>';
        else:
            html += '</{0}>'.format(table_row_type);
    html += '</{0}>'.format(table_type)
    return html

def randomString(stringLength=10):
    return ''.join(random.choice(string.printable) for i in range(stringLength))

field_type = {
    0: 'DECIMAL',
    1: 'TINY',
    2: 'SHORT',
    3: 'LONG',
    4: 'FLOAT',
    5: 'DOUBLE',
    6: 'NULL',
    7: 'TIMESTAMP',
    8: 'LONGLONG',
    9: 'INT24',
    10: 'DATE',
    11: 'TIME',
    12: 'DATETIME',
    13: 'YEAR',
    14: 'NEWDATE',
    15: 'VARCHAR',
    16: 'BIT',
    246: 'NEWDECIMAL',
    247: 'INTERVAL',
    248: 'SET',
    249: 'TINY_BLOB',
    250: 'MEDIUM_BLOB',
    251: 'LONG_BLOB',
    252: 'BLOB',
    253: 'VAR_STRING',
    254: 'STRING',
    255: 'GEOMETRY' 
    }