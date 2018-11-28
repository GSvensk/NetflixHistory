from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from init import app, db

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)
#postgres://oahgefuyjsvlfw:3091468ced69d00e2b861e50f69c89dbdbe5543e04f0fb0b18574fafd31f8f7b@ec2-54-75-231-3.eu-west-1.compute.amazonaws.com:5432/dd1ca7tqpk39v8

if __name__ == '__main__':
    manager.run()