import functools

from flask import redirect, session, url_for

def check_login (func):
    @functools.wraps(func)
    def wrapper(**args): # передать все именнованные аргументы в функцию
        if "userlogin" in session:
            return func(**args)
        else:
            return redirect(url_for("blueprint.login"))
    return wrapper
