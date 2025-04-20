import config

from app import app

if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(host=config.HOST,port=config.PORT,debug=config.DEBUG)