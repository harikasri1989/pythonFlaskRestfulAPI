from flaskext.mysql import MySQL
from app import app

mysql = MySQL()

app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']='test'
app.config['MYSQL_DATABASE_DB']='testdata'
app.config['MYSQK_DATABASE_HOST']='localhost'

mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()