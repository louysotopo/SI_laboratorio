import logging
from flask import Flask, jsonify;
from flask_cors import CORS;
from logging import fatal
from flask import Flask, jsonify, sessions,request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.elements import Null

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

class producto(db.Model):
    producto_id = db.Column(db.Integer,primary_key=True)
    pro_nombre = db.Column(db.String,nullable=True)
    pro_precio = db.Column(db.String,nullable=True)
    pro_descripcion = db.Column(db.String,nullable=True)
    pro_tags_tipo = db.Column(db.String,nullable=True)
    pro_tags_var = db.Column(db.String,nullable=True)
    pro_tag_cs = db.Column(db.String,nullable=True)
    pro_calidad = db.Column(db.String,nullable=True)
    pro_tag_temporada = db.Column(db.String,nullable=True)
    pro_fecha = db.Column(db.String,nullable=True)
    pro_foto = db.Column(db.String,nullable=True)
    pro_descuento = db.Column(db.String,nullable=True)
    pro_calificacion = db.Column(db.Integer,nullable=True)
    pro_npersonas = db.Column(db.Integer,nullable=True)
    usuario_id = db.Column(db.Integer,nullable=True)
    pro_unidad = db.Column(db.String,nullable=True)

    def toJSONall(self):
        producto_json = {
            "producto_id": self.producto_id,
            "nombre": self.pro_nombre ,
            "precio_tentativo": self.pro_precio ,
            "descripcion": self.pro_descripcion ,
            "tags_tipo": self.pro_tags_tipo , 
            "tags_var":self.pro_tags_var ,
            "tags_cs":self.pro_tag_cs ,
            "calidad":self.pro_calidad ,
            "tag_temporada": self.pro_tag_temporada ,
            "fecha": self.pro_fecha ,
            "fotos": self.pro_foto ,
            "descuento": self.pro_descuento,
            "calificacion": self.pro_calidad,
            "npersonas": self.pro_npersonas,
            "usuario_id": self.usuario_id,
            "unidad": self.pro_unidad
        }
        return producto_json

@app.route("/", methods=['GET'])
def index():
    return "HOLA MUNDO"

@app.route("/login/", methods=['GET','POST'])
def login():
    data = request.json
    json_ = {
        "message":"", 
        "usuario":{}
    }
    try:
        usuario_ = usuario.query.filter_by(usu_correo=data["correo"],usu_password=data["password"]).first()
        if usuario_ == None:
            json_["message"] = "fallo"
            return jsonify(json_)
        json_["message"]= "exito"
        json_["usuario"]= usuario_.toJSONall()
    except:
        json_["message"] = "fallo"
    return jsonify(json_)


@app.route("/users/",methods=['GET','POST'])
def getUsers():
    arr_users={ 
        "data":[] 
    }
    usuarios =usuario.query.all()
    for use in usuarios:
        arr_users["data"].append(use.toJSONall() )
    return jsonify(arr_users)

@app.route("/users/add/",methods=['GET','POST'])
def addUser():
    data = request.json
    try:
        db.session.add(usuario(usu_password=data["password"],usu_nombre="",usu_apellido="",usu_ubi_map_lat= 0 ,usu_ubi_map_long=0, usu_calificacion=0, usu_npersonas= 0 , usu_website ="", usu_telefono="", usu_ruc_dni ="", usu_descripcion="", usu_correo=data["correo"] ))
        db.session.commit()
        usuario_= usuario.query.filter_by(usu_correo=data["correo"]).first()
        return jsonify(usuario_.toJSONall())
    except:
        return jsonify({"message":"Error"})

@app.route("/users/edit/",methods=['GET','POST','PUT'])
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

@app.route("/users/delete/",methods=['GET','POST','DELETE'])
def deleteUser():
    data = request.json
    try:
        usuario_ = usuario.query.filter_by(usuario_id=data["id"]).first()
        db.session.delete(usuario_)
        db.session.commit()
    except:
        return jsonify({"message":"Error"})
    return jsonify({"message":"Borrado Correctamente"})
    

@app.route("/users/detail/",methods=['GET','POST'])
def detailUser():
    data = request.json
    try:        
        usuario_ = usuario.query.filter_by(usuario_id=data["id"]).first()
        if usuario_ == None:
            return jsonify({"message":"Error al obtener usuario"})
        return jsonify(usuario_.toJSONall())
    except:
        return jsonify({"message":"Error al obtener usuario"})

@app.route("/products/",methods=['GET','POST'])
def getProducts():
    arr_products={ 
        "data":[] 
    }
    productos = producto.query.all()
    for pro in productos:
        arr_products["data"].append(pro.toJSONall() )
    return jsonify(arr_products)

@app.route("/products/add/",methods=['GET','POST'])
def addProduct():
    data = request.json
    try:
        db.session.add(producto(pro_nombre = data["nombre"],
                        pro_precio = data["precio"],
                        pro_descripcion = data["descripcion"], 
                        pro_tags_tipo = data["tags_tipo"], 
                        pro_tags_var = data["tags_var"], 
                        pro_tag_cs = data["tags_cs"], 
                        pro_calidad = data["calidad"], 
                        pro_tag_temporada = data["temporada"] , 
                        pro_fecha= data["fecha"], 
                        pro_foto = data["foto"], 
                        pro_descuento = data["descuento"], 
                        pro_calificacion = data["calificacion"], 
                        pro_npersonas = data["npersonas"], 
                        usuario_id = data["usuario_id"],
                        pro_unidad = data["unidad"]))
        db.session.commit()        
        return jsonify({"message":"OK"})
    except:
        return jsonify({"message":"Error"})

@app.route("/products/edit/",methods=['GET','POST','PUT'])
def editProduct():
    data = request.json
    try:
        producto_= producto.query.filter_by(producto_id=data["producto_id"]).first()
        producto_.pro_nombre = data["nombre"]
        producto_.pro_precio = data["precio"]
        producto_.pro_descripcion = data["descripcion"]
        producto_.pro_tags_tipo = data["tags_tipo"]
        producto_.pro_tags_var = data["tags_var"]
        producto_.pro_tag_cs = data["tags_cs"]
        producto_.pro_calidad  =  data["calidad"]
        producto_.pro_tag_temporada = data["temporada"]
        producto_.pro_fecha = data["fecha"]
        producto_.pro_foto = data["foto"]
        producto_.pro_descuento = data["descuento"]
        producto_.pro_calificacion = data["calificacion"]
        producto_.pro_npersonas = data["calificacion"]
        producto_.pro_unidad = data["unidad"]
        db.session.commit()
        return jsonify({"message":"Actualizado correctamente"})
    except:
        return jsonify({"message":"Error al actualizar"})

@app.route("/products/delete/",methods=['GET','POST','DELETE'])
def deleteProduct():
    data = request.json
    try:
        producto_ = producto.query.filter_by(producto_id=data["id"]).first()
        db.session.delete(producto_)
        db.session.commit()
    except:
        return jsonify({"message":"Error"})
    return jsonify({"message":"Borrado Correctamente"})

@app.route("/products/detail/",methods=['GET','POST'])
def detailProduct():
    data = request.json
    try:        
        producto_ = producto.query.filter_by(producto_id=data["id"]).first()
        if producto_ == None:
            return jsonify({"message":"Error al obtener producto"})
        return jsonify(producto_.toJSONall())
    except:
        return jsonify({"message":"Error al obtener producto"})

@app.route("/users/products/",methods=['GET','POST'])
def userProducts():
    data = request.json
    user_products_={ 
        "usuario":{},
        "productos":[] 
    }
    productos = producto.query.filter_by(usuario_id=data["id"])
    usuario_ = usuario.query.filter_by(usuario_id=data["id"]).first()

    user_products_["usuario"] = usuario_.toJSONall()

    for pro in productos:
        user_products_["productos"].append(pro.toJSONall())

    return jsonify(user_products_)


if __name__ == '__main__':
    app.run()