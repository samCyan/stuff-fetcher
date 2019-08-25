import copy

def dict_clean(_dict):
    res = []
    for k,v in _dict.items():
        res.append("{} = '{}'".format(k, v))
    return ','.join(res)


def insertion_by_dict(cur, table, _dict):
    d = copy.deepcopy(_dict)
    d = {k: v for k, v in d.items() if v is not None}
    columns = ', '.join(d.keys())
    placeholders = ', '.join('?' * len(d))
    sql = 'INSERT INTO {} ({}) VALUES ({})'.format(table, columns, placeholders)
    cur.execute(sql, tuple(d.values()))

def get_all(cur, table):
    sql = 'SELECT * FROM {}'.format(table)
    cur.execute(sql)
    return cur.fetchall()

# right now support only string key value pairs
def update_table_with(cur, table, update_dict, where_dict):
    sql = 'UPDATE {} SET {} WHERE {}'.format(table, dict_clean(update_dict), dict_clean(where_dict))
    return cur.execute(sql)

