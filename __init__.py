# -- coding: utf-8 --
import os
import sys
from flask import Flask

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY = "dev",
    DATABASE = os.path.join(app.instance_path,"todo_app2.sqlite"),
)

#アプリケーションコンテキストが終了したときに
#毎回DBを切断する
from db import close_db
app.teardown_appcontext(close_db)

#インデックスページの読み込み
import views

#ログイン機能の追加
import auth
app.register_blueprint(auth.bp)

#タスク管理機能の追加
import task
app.register_blueprint(task.bp)

