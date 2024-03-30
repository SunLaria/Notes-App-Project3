from flask import Flask, redirect, url_for, render_template, request, session
from peewee import SqliteDatabase, Model, AutoField, CharField, DateField, ForeignKeyField, BooleanField
from datetime import date
import json
from flask_cors import CORS
from flask_login import LoginManager, login_user, logout_user, login_required,  current_user


app = Flask(__name__)
app.secret_key = 'kmkmnnjnjnjnjbj'
CORS(app)


db = SqliteDatabase('app.db')


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):

    id = AutoField()
    username = CharField(max_length=25)
    password = CharField(max_length=25)
    created_at = DateField(default=date.today())
    authenticated = BooleanField(default=False)
    admin = BooleanField(default=False)

    def to_dict(self):
        return {'id': self.id, "username": self.username, "admin": self.admin, "created_at": str(self.created_at)}

    def is_active(self):
        return True

    def get_id(self):
        return str(self.id)

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False

    def is_admin(self):
        return self.admin

    def validate(self):
        if self.username == "" or self.username == " ":
            raise ValueError("Username Cannot Be empty or contain spaces")
        if self.password == "" or self.password == " ":
            raise ValueError("Password Cannot Not Be empty or contain spaces")

    def save(self, *args, **kwargs):
        self.validate()
        super().save(*args, **kwargs)


class Note(BaseModel):
    id = AutoField()
    text = CharField(max_length=25, null=True)
    user = ForeignKeyField(User, backref="Notes")
    created_at = DateField(default=date.today())

    def to_dict(self):
        return {'id': self.id, "text": self.text, "user": self.user.to_dict(), "created_at": str(self.created_at)}


# db connect
db.connect()
db.create_tables([User, Note], safe=True)


# user-login setup
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    return redirect('/login')


@app.route("/login", methods=["GET", "POST"])
def user_login():
    if request.method == "GET":
        if current_user.is_authenticated:
            return redirect("/")
        else:
            return render_template("login.html")
    if request.method == "POST":
        user = User.filter(
            username=request.form['username'], password=request.form['password'])
        if len(user) > 0:
            user[0].authenticated = True
            user[0].save()
            login_user(user[0])
            return redirect("/")
        else:
            return redirect("/login")
    else:
        return redirect("/login")


@app.route("/logout")
@login_required
def user_logout():
    user = current_user
    user.authenticated = False
    user.save()
    logout_user()
    return redirect("/login")


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template('register.html')
    if request.method == "POST":
        try:
            if len(User.filter(username=request.form['username'])) < 1:
                new_user = User.get_or_create(
                    **{'username': request.form['username'], 'password': request.form['password']})
                return redirect("/login")
            else:
                return redirect('/register')
        except:
            return redirect("/register")


@app.route("/admin", methods=['GET'])
@login_required
def admin():
    if request.method == "GET":
        if current_user.is_admin():
            return render_template("admin.html")
        else:
            return redirect("/")


@app.route("/", methods=['GET'])
@login_required
def home():
    return render_template("home.html", admin=current_user.is_admin(), user_id=current_user.id)


@app.route('/api/user', methods=['GET', 'POST', 'DELETE', 'PATCH'])
@login_required
def user_actions():
    if current_user.is_admin():
        # json {username,password}
        if request.method == 'POST':
            try:
                data = request.json
                if len(User.filter(username=data['username'])) < 1:
                    new_user = User.get_or_create(
                        **{'username': data['username'], 'password': data['password'], 'admin': True if data['admin'] == "True" else False})
                    return json.dumps({'result': f'User Created Successfully, with id {new_user[0].id}'})
                else:
                    return json.dumps({'result': f'User Already Exists'})
            except ValueError as e:
                return json.dumps({'result': f'User Creation Failed, {e}'})
        # json {user_id}
        if request.method == "DELETE":
            try:
                data = request.args
                user = User.get_by_id(pk=data['user_id'])
                user.delete_instance(recursive=True)
                return json.dumps({'result': 'User Deleted Successfully'})
            except ValueError as e:
                return json.dumps({'result': f'User Delete Failed, {e}'})
        # json {user_id, password}
        if request.method == "PATCH":
            try:
                data = request.json
                user = User.get_by_id(pk=data['user_id'])
                user.password = data['password']
                user.save()
                return json.dumps({'result': 'User Password Updated Successfully'})
            except ValueError as e:
                return json.dumps({'result': f'User Password Update Failed, {e}'})

        if request.method == "GET":
            try:
                if request.args:
                    data = dict(request.args)
                    if data.get('all') == "users":
                        return json.dumps([i.to_dict() for i in User.select()])
                    if data.get('all') == "notes":
                        return json.dumps([i.to_dict() for i in Note.select()])

            except ValueError as e:
                return json.dumps({'result': f'Failed to achieve users, {e}'})


@app.route('/api/note', methods=['GET', 'POST', 'DELETE', 'PATCH'])
@login_required
def Note_actions():
    # json {text,user_id}
    if request.method == "POST":
        try:
            data = request.json
            new_note = Note.create(
                **{'text': data['text'], 'user': User.get_by_id(pk=data['user_id'])})
            return json.dumps({'result': f'Note Created With id {new_note.id}'})
        except ValueError as e:
            return json.dumps({'result': f'Note Create Failed, {e}'})
    # json {text,note_id}
    if request.method == "PATCH":
        try:
            data = request.json
            note = Note.get_by_id(pk=data['note_id'])
            note.text = data['text']
            note.save()
            return json.dumps({'result': f'Note {note.id} Updated'})
        except ValueError as e:
            return json.dumps({'result': f'Note Update Failed, {e}'})
    # json {note_id}
    if request.method == "DELETE":
        try:
            data = request.args
            note = Note.delete_by_id(pk=data['note_id'])
            return json.dumps({'result': f'Note {data["note_id"]} Deleted'})
        except ValueError as e:
            return json.dumps({'result': f'Note Delete Failed, {e}'})
    # user_id, Note_id
    if request.method == "GET":
        try:
            if request.args:
                data = dict(request.args)
                if data.get('user_id'):
                    return json.dumps([i.to_dict() for i in Note.select().join(User).where(User.id == data['user_id'])])
                if data.get('note_id'):
                    return json.dumps([i.to_dict() for i in Note.select().where(Note.id == data['note_id'])])
            else:
                return json.dumps([i.to_dict() for i in Note.filter()])
        except ValueError as e:
            return json.dumps({'result': f'Notes Read Failed, {e}'})


if __name__ == '__main__':
    # DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(port=5000, debug=True)
