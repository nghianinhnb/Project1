from app import app, dao, socket

#from controllers import User
#from controllers.User import User
#user = User()



socket.run(app, debug=True)

