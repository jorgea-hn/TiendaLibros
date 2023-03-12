from flask import Flask,render_template,request,redirect,url_for
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect

app=Flask(__name__)

csrf= CSRFProtect()
db=MySQL(app)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login", methods=["GET","POST"])
def login():
    print(request.method)
    if request.method=='POST':
        if request.form['usuario']=="admin" and request.form["password"]=="1234":
        # print(request.form['usuario'])
        # print(request.form['password'])
            return redirect(url_for('index'))
        else:
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')

@app.route("/libros")
def listar_libros():
    try:
        cursor=db.connection.cursor()
        # sql = "SELECT isbn, titulo, anoedicion FROM libro ORDER BY titulo ASC"
        sql = "SELECT LIB.isbn, LIB.titulo, LIB.anoedicion, LIB.precio, AUT.apellidos, AUT.nombres FROM libro LIB  JOIN autor AUT ON LIB.autor_id = AUT.id ORDER BY LIB.titulo ASC"
        cursor.execute(sql)
        data=cursor.fetchall()
        data={
            "libros":data
        }
        #print(data)
        #return "OK. Numero de libros: {0}".format(len(data))
        return render_template("listado_libros.html", data=data)
    except Exception as ex:
        raise Exception(ex)


def pagina_no_encontrada(error):
    return render_template("errores/404.html"),404


def inicializar_app(config):
    app.config.from_object(config)
    csrf.init_app(app)
    app.register_error_handler(404,pagina_no_encontrada)
    return app