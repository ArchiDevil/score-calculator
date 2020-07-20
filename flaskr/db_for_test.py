from flaskr.schema import Member, Stats, LoginPassword

def fill_db(session):
    # как добавлять значения в таблицу
    session.add_all([
        LoginPassword(userlogin="good",
                       userpassword="pbkdf2:sha256:150000$dFGNPY9B$b17f13b33dc62b0ca95126c6a100fad9b15d7cf73072dfe6b289833b1199bb41",
                       id_command=3),
        LoginPassword(userlogin="bad",
                       userpassword="pbkdf2:sha256:150000$6hzyuS0V$beab9a20230e3eb2555fa66c0d6666fdb0dba8bf60e272f7d29414c5e555ed9d",
                       id_command=2)
    ])
    # добавленные значения нужно заливать
    session.commit()

    session.add_all([
        Member(member_name="Anna", factor="0.2", number_team=1),
        Member(member_name="Alisa", factor="0.3", number_team=1),
        Member(member_name="Sasha", factor="0.4", number_team=2),
        Member(member_name="Stepan", factor="0.5", number_team=2),
        Member(member_name="Tasha", factor="0.6", number_team=3),
        Member(member_name="Tomas", factor="0.7", number_team=3),
    ])
    session.commit()

    session.add_all([
        Stats(team_id=1, sprint_name="Ollala", result=15),
        Stats(team_id=1, sprint_name="Oppapa", result=45),
    ])
    session.commit()
