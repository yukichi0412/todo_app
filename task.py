"""
タスクの取得、新規追加、編集、削除
"""

from datetime import date, datetime
from flask import Blueprint, flash, redirect, render_template, request, url_for, session
from flask.blueprints import Blueprint
from werkzeug.exceptions import abort
from auth import login_required
from db import get_db

bp = Blueprint('task', __name__, url_prefix='/task')

@bp.route('/')
@login_required
def index_task():
    """
    #タスクの一覧を取得する
    """

    #DBと接続
    db = get_db()

    #タスクのデータを取得
    user_id = session.get('user_id')
    tasks = db.execute(
        'SELECT * FROM task WHERE user_id = ? ORDER BY task_id DESC', (user_id)
    ).fetchall()

    #タスク一覧画面へ遷移
    return render_template('tasks/index_task.html',
                            tasks=tasks,
                            title='ログイン',
                            year=datetime.now().year)

@bp.route('/create_task', methods=('GET', 'POST'))
@login_required
def create_task():
    """
    GET :タスク登録画面に遷移
    POST:タスク登録処理を実施
    """
    if request.method == 'GET':
        #タスク登録画面に遷移
        return render_template('tasks/create_task.html',
                                title='タスクの追加',
                                year=datetime.now().year)
    
    #タスク登録処理

    #ユーザーIDを取得
    user_id = session.get('user_id')

    #登録フォームから送られてきた値を取得
    title = request.form['title']
    detail = request.form['detail']
    due = request.form['due']

    #DBと接続
    db = get_db()

    #エラーチェック
    error_message = None

    if not title:
        error_message = 'タスク名の入力は必須です'
    elif not due:
        error_message = '期日の入力は必須です'

    if error_message is not None:
        #エラーがあれば、それを画面に表示させる
        flash(error_message, category='alert alert-danger')
        return redirect(url_for('task.create_task'))
    
    #エラーがなければテーブルに登録する
    db.execute(
        'INSERT INTO task (user_id, title, detail, due) VALUES (?, ?, ?, ?)',
        (user_id, title, detail, due)
    )

    db.commit()

    #タスク一覧画面へ遷移
    flash('タスクが追加されました', category='alert alert-info')
    return redirect(url_for('task.index_task'))

@bp.route('/<int:task_id>/update_task', methods=('GET', 'POST'))
@login_required
def update_task(task_id):
    #GET :タスク更新画面に遷移
    #POST:タスク更新処理を実施
    pass

@bp.route('/<int:task_id>/delete_task', methods=('GET', 'POST'))
def delete_book(task_id):
    #GET :タスク削除確認画面に遷移
    #POST:タスク削除処理を実施
    pass

def get_task_and_check(task_id):
    #タスクの取得と存在チェックのための関数
    pass

