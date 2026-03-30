from data.users import User
from data import db_session
from data.jobs import Jobs

db_session.global_init("db/mars_explorer.db")
data = [{'team_leader': 1,
         'job': 'bajhak',
         'work_size': 15,
         'collaborators': '2, 3',
         'is_finished': False, }, {'team_leader': 2,
                                   'job': 'rjpjem;l',
                                   'work_size': 10,
                                   'collaborators': '2, 3',
                                   'is_finished': False, }, {'team_leader': 3,
                                                             'job': 'utdfg',
                                                             'work_size': 35,
                                                             'collaborators': '2, 3',
                                                             'is_finished': False, }, {'team_leader': 4,
                                                                                       'job': 'wasdaa',
                                                                                       'work_size': 14,
                                                                                       'collaborators': '2, 3',
                                                                                       'is_finished': False, }]


def insert_jobs():
    for elem in data:
        job = Jobs()
        job.team_leader = elem['team_leader']
        job.job = elem['job']
        job.work_size = elem['work_size']
        job.collaborators = elem['collaborators']
        job.is_finished = elem['is_finished']
        db_sess = db_session.create_session()
        db_sess.add(job)
        db_sess.commit()

if __name__ == '__main__':

    insert_jobs()