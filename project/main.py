from flask import Blueprint, render_template, request, url_for, flash, redirect
from flask_login import login_required, current_user
from werkzeug.exceptions import abort
from . import db
import sqlite3

main = Blueprint('main', __name__)

def get_db_connection():
    conn = sqlite3.connect('project\database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@main.route('/posts')
def posts():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('posts.html', posts=posts)

@main.route('/posts/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post, curr_email=current_user.email)

@main.route('/posts/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        curr_email = current_user.email

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content, email) VALUES (?, ?, ?)',
                         (title, content, curr_email))
            conn.commit()
            conn.close()
            return redirect(url_for('main.posts'))
    return render_template('create.html')

@main.route('/posts/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(post_id):
    post = get_post(post_id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?, modified = CURRENT_TIMESTAMP'
                         ' WHERE id = ?',
                         (title, content, post_id))
            conn.commit()
            conn.close()
            return redirect(url_for('main.posts'))

    return render_template('edit.html', post=post)

@main.route('/posts/<int:post_id>/delete', methods=['POST'])
@login_required
def delete(post_id):
    post = get_post(post_id)

    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (post_id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('main.posts'))