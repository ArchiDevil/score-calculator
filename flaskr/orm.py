from flaskr.schema import Team, Member, Login_password, Stats

from typing import Text
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.sql.sqltypes import REAL
engine = create_engine('sqlite:///sales.db', echo = True)
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

# x = session.query(Member).all()
# session.delete(x)
#data = session.query(Member).filter_by(member_name='Alisa').first()
#session.delete(data)
#session.commit()

# # как доставать данные из таблицы
data = session.query(Member).all()
for el in data:
   print ("Name: ",el.member_name, "Factor:",el.factor, "id-command:",el.number_team)

# как доставать данные из конкретного стобца
#data1 = session.query(Member.factor).all()
#for idx, el in enumerate(data1):
#   print (f"{idx} factor: {el.factor}")

# как доставать даннные с логическим условием
#data_where = session.query(Member.factor).filter(Member.id==2).one() #all()
#print(data_where)

# как доставать даннные с условием, это как это
#result = session.query(Member).filter(Member.member_name.like('Anna%')).all()
#for el in result:
#   print ("Name: ", el.member_name, "ID: ", el.id, "Factor: ", el.factor, "Command_id: ", el.number_team)
# Почему в первом случае нужен .one, а во втором НЕТ???
