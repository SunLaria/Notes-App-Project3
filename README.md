# Notes App
Save Your Notes, Manage Users via Admin Panel

## How To Use
- **Create Note**: Double-click on an empty space.
- **Delete Note**: Double-click on the note.
- **Admin Panel**: Exclusive access for admin users.
  - Create, delete, and reset passwords for users.
  - Access statistics.

## Setup
### Docker:
```bash
docker run -p 5000:5000 docker.io/randomg1/notes-app-project3:latest
```

### Locally:
```
git clone https://github.com/SunLaria/Notes-App-Project3.git
cd Notes-App-Project3
python -m pip install -r requirements.txt
python app.py
```

## Running the App
Navigate to:
- [http://localhost:5000/](http://localhost:5000/)
- [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

## Additional Information
- **Language**: Python
- **ORM**: Peewee
- **Frontend**: ReactJS, HTML, CSS
- **Backend**: Flask
- **Session Management**: Flask-Login
- **API Requests**: Axios