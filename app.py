# IMPORTAR
# flask
# flask_cors
# flask_sqlalchemy
# flask_marshmallow

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Crear la app
app = Flask(__name__)

# Utilizar Cors, permite el acceso al frontend
CORS(app)


# CONFIGURACIÓN A LA BASE DE DATOS DESDE app
# (SE LE INFORMA A LA APP DONDE UBICAR LA BASE DE DATOS)
                                                    # //user:password@url/nombre de la base de datos
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:''@127.0.0.1:3307/proyecto'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False 


# Crear el objeto db
# Notifica a la app que trabajará con SQLAlchemy
db = SQLAlchemy(app)

# Objeto ma permite acceder a los métodos para transformar datos
ma = Marshmallow(app)


# DEFINICIÓN DE LA TABLA A PARTIR DE UNA CLASE (Producto)
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre =db.Column(db.String(100))
    precio = db.Column(db.Integer)
    imagen = db.Column(db.String(400))

    def __init__(self,nombre,precio,imagen):
        self.nombre = nombre
        self.precio = precio 
        self.imagen = imagen

##class Ofertas(db.Model):
#    id_oferta = db.Column(db.Integer, primary_key=True)
#    oferta =db.Column(db.String(300))
    
#    def __init__(self,oferta):
#        self.oferta = oferta

#class Reserva(db.Model):
#    id_reserva = db.Column(db.Integer, primary_key=True)
#    nombre =db.Column(db.String(100))
#    apellido =db.Column(db.String(100))
#    id_oferta=db.Column(db.Integer, foreign_key=True)
#    cantidad = db.Column(db.Integer)
#    fecha = db.Column(db.Integer)

#    def __init__(self,nombre,apellido, id_oferta, cantidad, fecha):
#        self.nombre = nombre
#        self.apellido= apellido
#        self.id_oferta = id_oferta
#        self.fecha = fecha 

# CÓDIGO DE CREACIÓN DE LA TABLA
with app.app_context():
    db.create_all()


# CREAR UNA CLASE  ProductoSchema, 
# DONDE SE DEFINEN LOS CAMPOS DE LA TABLA
class ProductoSchema(ma.Schema):
    class Meta:
        fields=('id','nombre','precio','imagen')

#class OfertaSchema(ma.Schema):
#    class Meta:
#        fields=('id_oferta','oferta')


#class ReservaSchema(ma.Schema):
#    class Meta:
#        fields=('id_reserva','nombre','apellido','id_oferta','cantidad','fecha')

# CREAR DOS OBJETOS PARA TRANSFORMAR
producto_schema = ProductoSchema() # Permitir convertir un sólo dato. Ej: 1 objeto
productos_schema = ProductoSchema(many=True) # Permitir convertir un listado de datos. Ej: lista de objetos

#oferta_schema= OfertaSchema() 
#ofertas_schema= OfertaSchema(many=True)

#reserva_schema= ReservaSchema()
#reservas_schema= ReservaSchema(many=True)

# CREAR LAS RUTAS PARA: productos
# '/productos' ENDPOINT PARA MOSTRAR TODOS LOS PRODUCTOS 
# DISPONIBLES EN LA BASE DE DATOS: GET

@app.route("/productos", methods=['GET'])
def get_productos():
    # Consulta toda la info de la tabla productos
    all_productos = Producto.query.all()
    return productos_schema.jsonify(all_productos)


#@app.route("/ofertas", methods=['GET'])
#def get_ofertas():
    # Consulta toda la info de la tabla ofertas
#    all_ofertas = Ofertas.query.all()
#    return ofertas_schema.jsonify(all_ofertas)


#@app.route("/reserva", methods=['GET'])
#def get_reserva():
    # Consulta toda la info de la tabla reserva
#    all_reserva = Reserva.query.all()
#    return reservas_schema.jsonify(all_reserva)


# '/productos' ENDPOINT PARA RECIBIR DATOS: POST
@app.route('/productos', methods=['POST']) # crea ruta o endpoint
def create_producto():
    # request.json contiene el json que envio el cliente
    # Para insertar registro en la tabla de la base de datos
    # Se usará la clase Producto pasándole cada dato recibido.
    # Para agregar los cambios a la db con db.session.add(objeto)
    # Para guardar los cambios a la db con db.session.commit()
    # Entrada de datos:
 

    nombre=request.json['nombre']
    precio=request.json['precio']
    imagen=request.json['imagen']
    
    new_producto=Producto(nombre,precio,imagen)
    db.session.add(new_producto)
    db.session.commit()

    # Retornar los datos guardados en formato JSON 
    # Para ello, usar el objeto producto_schema para que convierta con                   # jsonify los datos recién ingresados que son objetos a JSON  
    return producto_schema.jsonify(new_producto)


# '/productos/<id>' ENDPOINT PARA MOSTRAR UN PRODUCTO POR ID: GET
@app.route('/productos/<id>',methods=['GET'])
def get_producto(id):
    # Consultar por id, a la clase Producto.
    #  Se hace una consulta (query) para obtener (get) un registro por id
    producto=Producto.query.get(id)

   # Retorna el JSON de un producto recibido como parámetro
   # Para ello, usar el objeto producto_schema para que convierta con                   # jsonify los datos recién ingresados que son objetos a JSON  
    return producto_schema.jsonify(producto)   


# '/productos/<id>' ENDPOINT PARA BORRAR UN PRODUCTO POR ID: DELETE
@app.route('/productos/<id>',methods=['DELETE'])
def delete_producto(id):
    # Consultar por id, a la clase Producto.
    #  Se hace una consulta (query) para obtener (get) un registro por id
    producto=Producto.query.get(id)
    
    # A partir de db y la sesión establecida con la base de datos borrar 
    # el producto.
    # Se guardan lo cambios con commit
    db.session.delete(producto)
    db.session.commit()
    
    # Devuelve un json con el registro eliminado
    # Para ello, usar el objeto producto_schema para que convierta con                     # jsonify el dato recién eliminado que son objetos a JSON  
    return producto_schema.jsonify(producto)   


# '/productos/<id>' ENDPOINT PARA MODIFICAR UN PRODUCTO POR ID: PUT
@app.route('/productos/<id>', methods=['PUT'])
def update_producto(id):
    # Consultar por id, a la clase Producto.
    #  Se hace una consulta (query) para obtener (get) un registro por id
    producto=Producto.query.get(id)
 
    #  Recibir los datos a modificar
    nombre=request.json['nombre']
    precio=request.json['precio']
   
    imagen=request.json['imagen']

    # Del objeto resultante de la consulta modificar los valores  
    producto.nombre=nombre
    producto.precio=precio
  
    producto.imagen=imagen
#  Guardar los cambios
    db.session.commit()
# Para ello, usar el objeto producto_schema para que convierta con                     # jsonify el dato recién eliminado que son objetos a JSON  
    return producto_schema.jsonify(producto)




# BLOQUE PRINCIPAL 
if __name__=='__main__':
    app.run(debug=True)