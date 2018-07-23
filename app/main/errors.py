from flask import render_template, request, jsonify
from . import main

@main.app_errorhandler(404)
def page_not_found(e):    
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = jsonify({'error': '未找到'})
        response.status_code = 404
        return response
    return render_template('404.html'),404

@main.app_errorhandler(500)
def internal_server_error(e):
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = jsonify({'error': '内部服务器错误'})
        response.status_code = 500
        return response
    return render_template('500.html'),500

@main.app_errorhandler(403)
def forbidden(e):
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = jsonify({'error': '禁止访问'})
        response.status_code = 403
        return response
    return render_template('403.html'),403
