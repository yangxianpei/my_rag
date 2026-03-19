from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    redirect,
    url_for,
    session,
    g,
)
from app.services.user_service import user_service


bp = Blueprint("auth", __name__)
from app.utils.logger import get_logger

logger = get_logger(__name__)


@bp.route("/")
def home():
    return render_template("home.html")


@bp.route("/test")
def test():
    return render_template("test.html")


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password", "")
        password_confirm = request.form.get("password_confirm", "")
        email = request.form.get("email", "")
        if password != password_confirm:
            flash("两次输入的密码不一致", "error")
            return render_template("register.html")
        try:
            user_service.register(username, password, email)
            flash("用户注册成功", "success")
            return redirect(url_for("auth.home"))
        except ValueError as e:
            logger.error(f"注册失败:{str(e)}")
            flash(str(e), "error")
        except Exception as e:
            logger.error(f"注册失败:{str(e)}")
            flash("注册失败,请稍后重试", {str(e)})

    return render_template("register.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password", "")
        # 获取登录后重定向的目标页面(优先是读取表单，其次是读URL参数)
        next_url = request.form.get("next") or request.args.get("next")

        try:
            user = user_service.login(username, password)
            session["user_id"] = user["id"]
            # 设置会话为永久有效，默认是31天
            session.permanent = True
            flash("登录成功", "success")
            return redirect(next_url or url_for("auth.home"))
        except ValueError as e:
            logger.error(f"登录失败:{str(e)}")
            flash(str(e), "error")
        except Exception as e:
            logger.error(f"登录失败:{str(e)}")
            flash("登录失败,请稍后重试", "error")
    next_url = request.args.get("next")
    if session.get("user_id", ""):
        session.clear()
    return render_template("login.html", next_url=next_url)


@bp.route("/logout")
def logout():
    # 清除会话
    session.clear()
    flash("已成功退出", "success")
    return redirect(url_for("auth.home"))
