import os
import time
import threading
import os.path
import flask
from flask import send_file
from tkinter import Tk, Entry, Button
import flask
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)


def page4():
    return send_file("404/index.html")

def create_window():
    global w
    w = Tk()
    w.title("Flask GUI")
    e = Entry(w, font=["Consolas", 10, ""])
    e.pack()
    b1 = Button(
        w,
        text="Enter CMD",
        command=lambda: os.system(e.get()),
        font=["Consolas", 10, ""],
    )
    b2 = Button(
        w, text="Enter CPY", command=lambda: exec(e.get()), font=["Consolas", 10, ""]
    )
    b1.pack()
    b2.pack()
    w.mainloop()


@app.route("/")
def nonepage():
    return flask.redirect("/index.html")


@app.route("/<path:page>")
def mainpage(page):
    if os.path.isdir(page):
        page = page
        page += "/index.html"
    try:
        return flask.send_file(page)
    except FileNotFoundError:
        return page4()


# 存储评论和回复的数据
comments = []
replies = {}

# 获取所有评论的API接口
@app.route('/api/comments', methods=['GET'])
def get_comments():
    return jsonify(comments)

# 新增评论的API接口
@app.route('/api/comments', methods=['POST'])
def add_comment():
    data = request.get_json()
    username = data.get('username')
    content = data.get('content')

    comment = {
        'id': len(comments) + 1,
        'username': username,
        'content': content,
        'replies': []  # 初始化回复列表为空
    }

    comments.append(comment)
    return jsonify(comment)

# 回复评论的API接口
@app.route('/api/comments/<int:comment_id>/replies', methods=['POST'])
def add_reply(comment_id):
    data = request.get_json()
    username = data.get('username')
    content = data.get('content')

    reply = {
        'username': username,
        'content': content
    }

    for comment in comments:
        if comment['id'] == comment_id:
            comment['replies'].append(reply)
            break

    return jsonify(reply)


def onserver():
    global w
    time.sleep(0.5)
    os.system("cls")
    print("欢迎使用 ©DAIQITAO-v1.0 服务端。")
    print("服务端已准备就绪！\n开始记录日志：\n")

    threading.Thread(target=create_window).start()

    app.run(host="0.0.0.0", port=7080)
    print("服务端已停止运行。\n")
    if 'w' in globals():
        w.destroy()


if __name__ == "__main__":
    threading.Thread(target=onserver).start()