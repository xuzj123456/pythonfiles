# coding=utf-8
from configuration import *

def run(schema, engine):
    table_names = engine.table_names()
    for table in table_names:
        result = engine.execute("SELECT * FROM {0}.{1};".format(schema, table)).fetchall()
        df = pd.DataFrame(result)

        md = sqlalchemy.MetaData()
        table_ = sqlalchemy.Table(table, md, autoload=True, autoload_with=engine)
        df.columns = [str(c).split('.')[1] for c in table_.c]

        if 'data' not in os.listdir('.\\'):
            os.mkdir('.\\data')

        if schema not in os.listdir('.\\data'):
            os.mkdir('.\\data\\'+schema)
        df.to_csv('.\\data\\'+schema+'\\'+table+'.csv', encoding='gbk', index=False)


if __name__ == '__main__':
    schemas = ['factors']
    for s in schemas:
        engine = \
            create_engine('mysql+mysqldb://root:13579@localhost:3306/{0}?charset=utf8'.format(s))
        run(s, engine)
