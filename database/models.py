import os
from sqlalchemy import Column, Date, Numeric, String
from flask_sqlalchemy import SQLAlchemy

database_path = os.environ['DATABASE_URL']
if database_path.startswith("postgres://"):
  database_path = database_path.replace("postgres://", "postgresql://", 1)

# database_name = 'postgres'
# database_path = "postgresql://{}:{}@{}/{}".format(
#     "postgres", "root", "localhost:5432", database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    with app.app_context():
      app.config["SQLALCHEMY_DATABASE_URI"] = database_path
      app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
      db.app = app
      db.init_app(app)
      db.create_all()

'''
Movie
That has the title and release date
'''
class Movie(db.Model):  
  __tablename__ = 'Movie'

  id = Column(db.Integer, primary_key=True)
  title = Column(String)
  release_date = Column(Date)

  def __init__(self, title, release_date):
    self.title = title
    self.release_date = release_date

  def insert(self):
    db.session.add(self)
    db.session.commit()

  def update(self, title, release_date):
    self.title = title
    self.release_date = release_date
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'title': self.title,
      'release_date': self.release_date}

'''
Actor
That has the name, age and gender
'''
class Actor(db.Model):  
  __tablename__ = 'Actor'

  id = Column(db.Integer, primary_key=True)
  name = Column(String)
  age = Column(Numeric)
  gender = Column(String)
  

  def __init__(self, name, age, gender):
    self.name = name
    self.age = age
    self.gender = gender

  def insert(self):
    db.session.add(self)
    db.session.commit()

  def update(self, name, age, gender):
    self.name = name
    self.age = age
    self.gender = gender
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'age': self.age,
      'gender': self.gender}
