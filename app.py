from flask import Flask, jsonify;
from flask_cors import CORS;
from logging import fatal
from flask import Flask, jsonify, sessions
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://ufxgukkezqcaoi:55a11ba821bf2e02176f960b9db6eb24f6f1cafe6ef11547c839a35201f30ac9@ec2-3-227-44-84.compute-1.amazonaws.com:5432/dfu03d5e67frk"
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class usuario(db.Model):
    usuario_id = db.Column(db.Integer,primary_key=True)
    usu_password = db.Column(db.String ,nullable=True)
    usu_nombre = db.Column(db.String,nullable=True)
    usu_apellido = db.Column(db.String,nullable=True)
    usu_ubi_map_lat = db.Column(db.Float,nullable=True)
    usu_ubi_map_long = db.Column(db.Float,nullable=True)
    usu_calificacion = db.Column(db.Float,nullable=True)
    usu_npersonas = db.Column(db.Integer,nullable=True)
    usu_website = db.Column(db.String,nullable=True)
    usu_telefono = db.Column(db.String,nullable=True)
    usu_ruc_dni = db.Column(db.String,nullable=True)
    usu_descripcion = db.Column(db.String,nullable=True)
    usu_correo = db.Column(db.String,nullable=True)

    def toJSONall(self):
        usuario_json = {
            "usuario": self.usu_correo ,
            "password": self.usu_password ,
            "nombre": self.usu_nombre ,
            "apellido": self.usu_apellido , 
            "ubicacion_map_lat":self.usu_ubi_map_lat,
            "ubicacion_map_long":self.usu_ubi_map_long,
            "calificacion":self.usu_calificacion,
            "website": self.usu_website,
            "telefono": self.usu_telefono,
            "DNI_RUC": self.usu_ruc_dni,
            "descripcion_larga": self.usu_descripcion,
            "npersonas":self.usu_npersonas,            
        }
        return usuario_json

@app.route("/", methods=['GET'])
def index():
    return "HOLA MUNDO"

@app.route("/users/",methods=['GET'])
def getUsers():
    arr_users={ 
        "data":[] 
    }
    usuarios =usuario.query.all()
    for use in usuarios:
        arr_users["data"].append(use.toJSONall() )
    return jsonify(arr_users)

if __name__ == '__main__':
    app.run(debug=True)