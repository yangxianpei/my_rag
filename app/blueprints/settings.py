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
from app.blueprints.utils import (
    handle_api_error,
    success_response,
    require_json_body,
    get_current_user_or_error,
)
from app.utils.models_config import EMBEDDING_MODELS, LLM_MODELS
from app.services.settings_service import settings_service

bp = Blueprint("settings", __name__)
from app.utils.logger import get_logger
from app.config import Config

logger = get_logger(__name__)


@bp.route("/settings")
def api_chat():
    return render_template("settings.html")


@bp.route("/api/v1/settings/models", methods=["GET"])
@handle_api_error
def api_get_available_models():
    return success_response(
        {"embedding_models": EMBEDDING_MODELS, "llm_models": LLM_MODELS}
    )


@bp.route("/api/v1/settings", methods=["GET"])
@handle_api_error
def api_get_settings():
    current_user, err = get_current_user_or_error()
    settings = settings_service.get(id=current_user["id"])
    return success_response(settings)


@bp.route("/api/v1/settings", methods=["PUT"])
@handle_api_error
def api_update_settings():
    data, err = require_json_body()
    if err:
        return err
    current_user, err = get_current_user_or_error()
    settings = settings_service.update(user_id=current_user["id"], data=data)
    return success_response(settings, "更新设置成功")
