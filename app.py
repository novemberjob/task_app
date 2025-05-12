from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(80), nullable=False)
    complete = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f"<MyTask {self.id}>"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        current_task = request.form["content"]
        new_task = MyTask(content=current_task)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")
            return f"Error: {e}"
    else:
        tasks = MyTask.query.order_by(MyTask.created_at).all()   
        return render_template("index.html", tasks=tasks)

if __name__ in "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)