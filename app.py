from flask import Flask, render_template, request, redirect 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
## Need to notify our flask app where our database is stored: 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db' ## Tripple slashes absolute path. 
##Link Flask-App to the database
db = SQLAlchemy(app)

## Creating Database Model: 
class BlogPost(db.Model):
    ## First thing should create in every model is an ID:
    id = db.Column(db.Integer, primary_key = True) ## Primary_key this ID will be main distinguisher 
    title = db.Column(db.String(100), nullable = False) ## Nullable --> Field is required it cannot be null! 
    content = db.Column(db.Text, nullable = False) 
    author = db.Column(db.String(20), nullable = False, default='N/A' ) ## defualt --> If not author is provided will default to 'N/A' 
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    ##METHOD PRINT OUT WHENEVER A NEW BLOG POST IS MADE! 
    def __repr__(self):
        return 'Blog Post' + str(self.id)



##SQLALCHEMY allows us to use any database that we want!! 
## Change need to change 'sqlite' to a different database somewhere else 


@app.route("/")
def index():
    return render_template('index.html') 

@app.route("/posts",  methods = ['GET','POST'])
def posts():
    if request.method == 'POST':
        post_title = request.form['title']
        post_author = request.form['author']
        post_content = request.form['content']
        new_post = BlogPost(title=post_title , content = post_content, author = post_author)
        db.session.add(new_post)
        db.session.commit() ##Permanantly saves the data in the database!
        return redirect('/posts') ##Once the data has successfully stored in the databse redirect the user back to the defualt page!
    else:
         all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
         return render_template('post.html', posts = all_posts)

@app.route("/posts/delete/<int:id>")
def delete(id):
    post = BlogPost.query.get_or_404(id) ##Grabbing the post with the specific ID and storing into varibale "Post"
    db.session.delete(post)
    db.session.commit()
    return redirect("/posts")

@app.route("/posts/edit/<int:id>", methods = ["GET","POST"])
def edit(id):
    post = BlogPost.query.get_or_404(id)

    if (request.method == "POST"):
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', post = post)

@app.route("/posts/new", methods = ["GET","POST"])
def new_post():
    if (request.method == "POST"):
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        new_post = BlogPost(title=post_title , content = post_content, author = post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('new_post.html')


if __name__ == "__main__":
    app.run(debug=True)