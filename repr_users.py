from data.users import User
from data import db_session

if False:
    name_db = 'db/mars_explorer.db'
else:
    name_db = input()
db_session.global_init(name_db)
db_sess = db_session.create_session()
for user in db_sess.query(User).all():
    if user.address == 'module_1':
        print(user)