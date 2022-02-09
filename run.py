from app import app, dao, socket


socket.run(app, debug=True)

