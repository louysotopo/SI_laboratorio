from flask import Flask, jsonify;
from flask_cors import CORS;
from logging import fatal
from flask import Flask, jsonify, sessions,request
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
            "usuario_id": self.usuario_id,
            "correo": self.usu_correo ,
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

@app.route("/users/add/",methods=['GET'])
def detalleUser():
    data = request.json
    try:
        db.session.add(usuario(usu_password=data["password"],usu_nombre="",usu_apellido="",usu_ubi_map_lat= 0 ,usu_ubi_map_long=0, usu_calificacion=0, usu_npersonas= 0 , usu_website ="", usu_telefono="", usu_ruc_dni ="", usu_descripcion="", usu_correo=data["correo"] ))
        db.session.commit() 
        return jsonify({"message":"Registrado correctamente"})
    except:
        return jsonify({"message":"Error"})

@app.route("/users/edit/",methods=['GET'])
def editUser():
    data = request.json
    try:
        usuario_= usuario.query.filter_by(usuario_id=data["usuario_id"]).first()
        usuario_.usu_correo = data["correo"]
        usuario_.usu_password = data["password"]
        usuario_.usu_nombre = data["nombre"]
        usuario_.usu_apellido = data["apellido"]
        usuario_.usu_ubi_map_lat = data["ubicacion_map_lat"]
        usuario_.usu_ubi_map_long = data["ubicacion_map_long"]
        usuario_.usu_calificacion  =  data["calificacion"]
        usuario_.usu_website = data["website"]
        usuario_.usu_telefono = data["telefono"]
        usuario_.usu_ruc_dni = data["DNI_RUC"]
        usuario_.usu_descripcion = data["descripcion_larga"]
        usuario_.usu_npersonas = data["npersonas"]
        db.session.commit()
        return jsonify({"message":"Actualizado correctamente"})
    except:
        return jsonify({"message":"Error al actualizar"})

if __name__ == '__main__':
    app.run(debug=True)