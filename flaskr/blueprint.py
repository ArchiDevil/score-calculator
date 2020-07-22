from typing import List

from flask import (
    Blueprint, redirect, render_template, request, session, url_for, abort
)
from werkzeug.security import check_password_hash

from flaskr.calculation import calculate_points, predict_points
from flaskr.db import get_db
from flaskr.decorators import check_login
from flaskr.schema import Stats, create_db, LoginPassword, Team, Member

bp = Blueprint('blueprint', __name__, url_prefix='/team')


@bp.route('/tables')
@check_login
def tables():
    with get_db() as sess:
        # Найти имена и факторы всех участников вошедшей команды
        infa_about_members: List[Member] = sess.query(Member).filter(Member.number_team == session["id_command"]).all()
        infa_about_stats = sess.query(Stats).filter(Stats.team_id==session["id_command"]).all()

    if len(infa_about_members)==0:
        return render_template("blueprint/members.html",
                           print_members=infa_about_members,
                           print_stats=infa_about_stats,
                           button_start="False",
                           button_finish="False")
    if len(infa_about_members)!=0 and len(infa_about_stats)==0:
        return render_template("blueprint/members.html",
                           print_members=infa_about_members,
                           print_stats=infa_about_stats,
                           button_start="False",
                           button_finish="True")

    return render_template("blueprint/members.html",
                           print_members=infa_about_members,
                           print_stats=infa_about_stats,
                           button_start="True",
                           button_finish="True")

#button_start="False" if not infa_about_stats or not infa_about_members else "True")


@bp.route('/members/delete/<int:member_id>')
@check_login
def delete_member(member_id):
    with get_db() as sess:
        if sess.query(Member.id).filter(Member.id==member_id).first() is None:
            abort(403)
        data = sess.query(Member).filter(Member.id==member_id).one()
        sess.delete(data)
        sess.commit()
    return redirect(url_for("blueprint.tables"))


@bp.route('/sprint/delete/<int:sprint_id>')
@check_login
def delete_sprint(sprint_id):
    with get_db() as sess:
        if sess.query(Stats.id).filter(Stats.id==sprint_id).first() is None:
            abort(403)
        data = sess.query(Stats).filter(Stats.id==sprint_id).one()
        sess.delete(data)
        sess.commit()
    return redirect(url_for("blueprint.tables"))


@bp.route('/addmember', methods=["GET", "POST"])
@check_login
def addmember():
    if request.method == "GET":
        return render_template("blueprint/addmember.html")

    # POST
    if "username" not in request.form:
        abort(403)
    if "userfactor" not in request.form:
        abort(403)

    new_name = request.form["username"]
    if not new_name:
        return render_template("blueprint/addmember.html", marker=0)

    new_factor = request.form["userfactor"]
    try:
        new_factor = float(new_factor)
    except:
        return render_template("blueprint/addmember.html", marker=0)

    if new_factor > 1.0 or new_factor <= 0.0:
        return render_template("blueprint/addmember.html", marker=0)

    with get_db() as sess:
        sess.add_all([
            Member(member_name=new_name, factor=new_factor, number_team=session["id_command"]),
        ])
        sess.commit()

    return redirect(url_for("blueprint.tables"))


@bp.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("blueprint/login.html")

    # POST
    if "userlogin" not in request.form:
        abort(403)
    if "userpassword" not in request.form:
        abort(403)

    potential_login = request.form["userlogin"]
    potential_password = request.form["userpassword"]

    with get_db() as sess:
        data: LoginPassword = sess.query(LoginPassword).filter(LoginPassword.userlogin==potential_login).first()

    if data is not None:
        h_pas = data.userpassword
        if check_password_hash(h_pas, potential_password):
            # Возьмем id_command и сохраним его в session
            value_command = data.id_command
            session["id_command"] = value_command
            session["userlogin"] = potential_login
            if "remember" in request.form:
                session.permanent = True
            return redirect(url_for("blueprint.tables"))

        # выдать сообщение что неправильный пароль
        return render_template("blueprint/login.html", att="wrong")

    # Такой логин не найден, сообщение - неправильный логин
    return render_template("blueprint/login.html", att="wrong")


@bp.route('/finish', methods=["GET", "POST"])
@check_login
def finish():
    with get_db() as sess:
        name_members = sess.query(Member).filter(Member.number_team==session["id_command"]).all()
        factors=sess.query(Member.factor).filter(Member.number_team==session["id_command"]).all()

    array_factors=[]
    for index in range(0, len(factors)):
        array_factors.append(factors[index][0])

    if request.method == "GET":
        if not name_members:
            abort(403)
        else:
            return render_template("blueprint/finish.html",
                               print_members_finish=name_members)

    # POST
    answer = render_template("blueprint/finish.html",
                             print_members_finish=name_members,
                             check="False")

    if "real_number" not in request.form:
        abort(403)
    if "name_last_sprint" not in request.form:
        abort(403)
    if "working_days" not in request.form:
        abort(403)

    real_score = request.form["real_number"]
    name = request.form["name_last_sprint"]
    totaldays = request.form["working_days"]

    # проверяем что данные введены корректно
    try:
        real_score = int(real_score)
        if real_score <= 0:
            return answer

        totaldays = int(totaldays)
        if totaldays <= 0:
            return answer
    except:
        return answer

    number_members = len(list(name_members))
    missing_r_array = {}  # пустой словарь
    for i in range(1, number_members+1):
        name_key = "missing_days" + str(i)
        if name_key not in request.form:
            abort(403)
        missing_r_array[name_key] = request.form[name_key]
        try:
            missing_r_array[name_key] = int(missing_r_array[name_key])
        except:
            return answer

        if int(missing_r_array[name_key]) > int(totaldays) or int(missing_r_array[name_key])<0:
            return answer

    if not missing_r_array:
        return answer

    with get_db() as sess:
        if calculate_points(real_score, totaldays, missing_r_array.values())!=False:
            ideal_score = calculate_points(real_score, totaldays, missing_r_array.values())
            sess.add_all([
                Stats(team_id=session["id_command"], sprint_name=name, result=ideal_score),
                ])
            sess.commit()
            return redirect(url_for("blueprint.tables"))
        else:
            return render_template("blueprint/finish.html",
                             print_members_finish=name_members,
                             calculate="False")


@bp.route('/start', methods=["GET", "POST"])
@check_login
def start():
    with get_db() as sess:
        name_members = sess.query(Member).filter(Member.number_team==session["id_command"]).all()
        sprints = sess.query(Stats.result).filter(Stats.team_id==session["id_command"]).all()
        factors=sess.query(Member.factor).filter(Member.number_team==session["id_command"]).all()
        #raise RuntimeError(len(list(sprints)))

    array_factors=[]
    for index in range(0, len(factors)):
        array_factors.append(factors[index][0])
    #raise RuntimeError(len(factors), array_factors, type(array_factors), type(array_factors[0]))

    answer = render_template("blueprint/start.html",
                             print_members_start=name_members,
                             check_start="False",
                             button_append="False" if not name_members else "True")

    if request.method == "GET":
        if not name_members or not sprints:
            abort(403)
        else:
            return render_template("blueprint/start.html",
                                print_members_start=name_members,
                                button_append="False" if not name_members else "True")

    # POST
    if not name_members or not sprints:
        abort(403)

    if "workdays" not in request.form:
        #raise RuntimeError("errorworkdays")
        abort(403)
    workdays = request.form["workdays"]
    try:
        workdays = int(workdays)
        if workdays <= 0:
            return answer
    except:
        return answer

    # members = len(list(name_members))  # - количество участников команды
    members = len(name_members)
    missing_r_dict = {}  # пустой словарь
    for i in range(1, members+1):
        #raise RuntimeError("Miss?")
        name_key = "missing_days" + str(i)
        if name_key not in request.form:
            abort(403)
        missing_r_dict[name_key] = request.form[name_key]
        try:
            missing_r_dict[name_key] = int(missing_r_dict[name_key])
        except:
            return answer
        if missing_r_dict[name_key] > workdays or missing_r_dict[name_key] < 0:
            return answer

    if not missing_r_dict:
        return answer

    sprints_count = len(sprints) # все норм
    array_ideal_points = []
    if sprints_count == 0:
        abort(403)

    if sprints_count >= 4:
        for index in range(sprints_count-4, sprints_count):
            array_ideal_points.append(sprints[index])
    else:
        for index in range(0, sprints_count): # что такое i?
            array_ideal_points.append(sprints[index])
    array=[]
    for el in array_ideal_points:
        array.append(el[0])

    #raise RuntimeError(array)
    perfect_point = predict_points(array, workdays,
                                   missing_r_dict.values())

    return render_template("blueprint/start.html",
                           result="success",
                           print_members_start=name_members,
                           infa=perfect_point,
                           button_append="False" if not name_members else "True")
