from flask import Flask,redirect,url_for,render_template,request, session
from peewee import SqliteDatabase, Model, AutoField, CharField, DateField, ForeignKeyField, BooleanField
from datetime import date
import json
from flask_cors import CORS


app=Flask(__name__)
app.secret_key='kmkmnnjnjnjnjbj'
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
    


class Task(BaseModel):
    id = AutoField()
    text = CharField(max_length=25)
    user = ForeignKeyField(User, backref="tasks")
    created_at = DateField(default=date.today())

    def to_dict(self):
        return {'id':self.id,"text":self.text,"user":self.user.to_dict(),"created_at":str(self.created_at)}



# db connect
db.connect()
db.create_tables([User,Task],safe=True)



@app.route('/api/user',methods=['POST','DELETE','PATCH'])
def user_actions():
    # json {username,password}
    if request.method=='POST':
        try:
            data = json.loads(request.json)
            if len(User.filter(username=data['username'])) < 1:
                new_user = User.get_or_create(**{'username':data['username'],'password':data['password']})
                return json.dumps(f'User Created Succesfully, with id {new_user[0].id}')
            else:
                return json.dumps(f'User Already Exists')
        except ValueError as e:
            return json.dumps(f'User Creation Failed, {e}')
    # json {user_id}
    if request.method=="DELETE":
        try:
            data = json.loads(request.json)
            user = User.get_by_id(pk=data['user_id'])
            user.delete_instance(recursive=True)
            return json.dumps('User Deleted Succesfully')
        except ValueError as e:
            return json.dumps(f'User Delete Failed, {e}')
    # json {user_id, password}
    if request.method=="PATCH":
        try:
            data = json.loads(request.json)
            user = User.get_by_id(pk=data['user_id'])
            user.password = data['password']
            user.save()
            return json.dumps('User Password Updated Succesfully')
        except ValueError as e:
            return json.dumps(f'User Password Update Failed, {e}')


@app.route('/api/task',methods=['GET','POST','DELETE','PATCH'])
def task_actions():
    # json {text,user_id}
    if request.method=="POST":
        try:
            data = json.loads(request.json)
            new_task = Task.create(**{'text':data['text'],'user':User.get_by_id(pk=data['user_id'])})
            return json.dumps(f'Task Created With id {new_task.id}')
        except ValueError as e:
            return json.dumps(f'Task Create Failed, {e}')
    # json {text,task_id}
    if request.method=="PATCH":
        try:
            data = json.loads(request.json)
            task = Task.get_by_id(pk=data['task_id'])
            task.text = data['text']
            task.save()
            return json.dumps(f'Task {task.id} Updated')
        except ValueError as e:
            return json.dumps(f'Task Update Failed, {e}')
    # json {task_id}
    if request.method=="DELETE":
        try:
            data = json.loads(request.json)
            task = Task.delete_by_id(pk=data['task_id'])
            return json.dumps(f'Task {data["task_id"]} Deleted')
        except ValueError as e:
            return json.dumps(f'Task Delete Failed, {e}')
    # user_id, task_id
    if request.method=="GET":
        try:
            if request.args:
                data = dict(request.args)
                if data.get('user_id'):
                    return json.dumps([i.to_dict() for i in Task.select().join(User).where(User.id==data['user_id'])])
                if data.get('task_id'):
                    return json.dumps([i.to_dict() for i in Task.select().where(Task.id==data['task_id'])])
            else:
                return json.dumps([i.to_dict() for i in Task.filter()])
        except ValueError as e:
            return json.dumps(f'Tasks Read Failed, {e}')
        


if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(port=5000,debug=True)