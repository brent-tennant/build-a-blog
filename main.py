from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import desc

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:abc123@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))
    pub_date = db.Column(db.DateTime)

    def __init__(self, title, body, pub_date=None):
        self.title = title
        self.body = body
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date

# if request.args has contents, then find the id for that post and display it

@app.route('/blog', methods=['GET'])
def display_post():
    if len(request.args) != 0:
        entry_id = request.args.get("id")
        entry = Blog.query.get(entry_id)

        return render_template('entry.html', entry=entry)

    posts = Blog.query.order_by(desc(Blog.pub_date))
    return render_template('blog.html', posts=posts)

@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        entry = request.form['entry']

        if title == "" or entry == "":
            if title == "":
                title_error = "Please enter a title"
            if entry == "":
                entry_error = "Please enter a post body"
            return render_template('/newpost.html', title=title, entry=entry, entry_error=entry_error, title_error=title_error)
        else:
            post = Blog(title, entry)
            db.session.add(post)
            db.session.commit()

            entry_id = str(post.id)
            return redirect("/blog?id=" + entry_id)

    return render_template('/newpost.html')

@app.route('/')
def index():
    return redirect('/blog')

if __name__ == '__main__':
    app.run()
