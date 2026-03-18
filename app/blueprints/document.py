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
import os
from app.services.user_service import user_service
from app.blueprints.utils import (
    handle_api_error,
    success_response,
    require_json_body,
    get_current_user_or_error,
    error_response,
    allowed_file,
)
from app.utils.models_config import EMBEDDING_MODELS, LLM_MODELS
from app.services.settings_service import settings_service
from app.utils.auth import login_required, api_login_required
from app.config import Config
from app.services.document_service import document_service
from app.models.document import Document as DocumentModel
from app.services.knowledgebase_service import knowledgebase_service
from app.services.vector_service import vector_service

bp = Blueprint("document", __name__)
from app.utils.logger import get_logger

logger = get_logger(__name__)


@bp.route("/api/v1/knowledgebases/<kb_id>/documents", methods=["POST"])
@api_login_required
def api_document_load(kb_id):
    if "file" not in request.files:
        return error_response("没有文件字段", 400)
    file = request.files["file"]
    if file.filename == "":
        return error_response("没有选中任何文件", 400)
    if not allowed_file(file.filename):
        return error_response(
            f"文件类型不允许上传，只允许:{', '.join(Config.ALLOWED_EXTENSIONS)}", 400
        )
    file_data = file.read()
    if len(file_data) > Config.MAX_FILE_SIZE:
        return error_response(
            f"文件大小超过了最大的大小:{', '.join(Config.MAX_FILE_SIZE)} bytes", 400
        )
    custom_name = request.form.get("name")
    if custom_name:
        original_ext = os.path.splitext(file.filename)[1]
        if not os.path.splitext(custom_name)[1] and original_ext:
            # filename = store.pdf
            filename = custom_name + original_ext
        else:
            filename = custom_name
    else:
        filename = file.filename
    if not filename or not filename.strip():
        return error_response(f"文件名必须存在", 400)
    doc_dict = document_service.upload(kb_id, file_data, filename)
    return success_response(doc_dict)


@bp.route("/api/v1/documents/<doc_id>/process", methods=["POST"])
@handle_api_error
def api_process(doc_id):
    try:
        document_service.process(doc_id)
        return success_response({"message": "文档处理任务已经提交"})
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response("处理文档失:{str(e)}", 500)


@bp.route("/api/v1/documents/<doc_id>", methods=["DELETE"])
@handle_api_error
def api_delete(doc_id):
    try:
        current_user, err = get_current_user_or_error()
        document_service.delete(doc_id, user_id=current_user["id"])
        return success_response({"message": "文档删除成功"})
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response(f"删除文档失败:{str(e)}", 500)


@bp.route("/documents/<doc_id>/chunks")
@login_required
def document_chunks(doc_id):
    doc = document_service.get_by_id(DocumentModel, doc_id)
    if not doc:
        flash("文档不存在", "error")
        return redirect(url_for("knowledgebase.kb_list"))
    kb = knowledgebase_service.get_by_id(doc.kb_id)
    if not kb:
        flash("知识库不存在", "error")
        return redirect(url_for("knowledgebase.kb_list"))
    # 获取分块列表
    try:
        # 组合向量数据库的集合名称
        collection_name = f"kb_{doc.kb_id}"
        # 构建过滤条件，按文档ID进行过滤
        filter_dict = {"doc_id": doc_id}
        current_user, err = get_current_user_or_error()
        results = vector_service.similarity_search_with_score(
            collection_name=collection_name,
            query="",
            k=10000,
            filter=filter_dict,
            user_id=current_user["id"],
        )
        print(f"vector_service查询到的结果:{len(results)}")
        # 这个doc指的chromdb里的Document对象
        document_vectors = [doc for doc, _ in results]
        # 按chunk_index 进行排序，保证顺序和原始文档顺序是一样的
        document_vectors.sort(key=lambda d: d.metadata.get("chunk_index", 0))
        chunks_data = []
        for document_vector in document_vectors:
            chunks_data.append(
                {
                    "id": document_vector.metadata.get("id"),  # 文本分块ID
                    "content": document_vector.page_content,  # 分块的文本内容
                    "chunk_index": document_vector.metadata.get(
                        "chunk_index"
                    ),  # 分块在文档中的索引
                    "metadata": document_vector.metadata,
                }
            )
    except Exception as e:
        logger.error(f"获取分块数据失败:{e}")
        chunks_data = []
    return render_template(
        "document_chunks.html", kb=kb, document=doc.to_dict(), chunks=chunks_data
    )
