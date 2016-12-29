from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from moments import moments, db
from config import SQLALCHEMY_DATABASE_URI

moments.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI


migrate = Migrate(moments, db)

manager = Manager(moments)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
