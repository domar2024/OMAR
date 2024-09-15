from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import aliased
from flask_cors import CORS

# Crear la aplicación Flask
app = Flask(__name__)

CORS(app)
# CORS(app, resources={r"/*": {"origins": "http://topdom.com"}})

# Construir la URI de la base de datos
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:c2Vd4KEY1H541xqlz5nb@161.132.40.158:3306/bd_topdom'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://c2081645_OTyM:vpzgujhmw1Vxcoc@jpawaj.com:3306/c2081645_OTyM'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/otym_api'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

# Modelos
class Rol(db.Model):
    __tablename__ = 'Tb_Rol'
    IdRol = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Rol = db.Column(db.String(50), nullable=False)
    Estatus = db.Column(db.Integer, default=1, nullable=False)

class Usuario(db.Model):
    __tablename__ = 'Tb_Usuario'
    IdUsuario = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    Usuario = db.Column(db.String(50))
    Email = db.Column(db.String(80))
    Contraseña = db.Column(db.String(80))
    Nombre = db.Column(db.String(50))
    IdRol = db.Column(db.Integer, db.ForeignKey('Tb_Rol.IdRol'))
    Estatus = db.Column(db.Integer, default=1, nullable=False)
    rol = db.relationship('Rol', backref='usuarios')

class Cliente(db.Model):
    __tablename__ = 'Tb_Clientes'
    IdCliente = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    Nombre = db.Column(db.String(50), nullable=False)
    Apellido = db.Column(db.String(50), nullable=False)
    CedulaPasaporte = db.Column(db.String(15), nullable=False)
    Nacionalidad = db.Column(db.String(50))
    Sexo = db.Column(db.String(10), nullable=False)
    EstadoCivil = db.Column(db.String(50))
    Ocupacion = db.Column(db.String(50))
    Celular = db.Column(db.String(50), nullable=False)
    Correo = db.Column(db.String(50), nullable=False)
    Calle = db.Column(db.String(50), nullable=False)
    IdSector = db.Column(db.Integer, db.ForeignKey('Tb_Sector.IdSector'), nullable=False)
    Estatus = db.Column(db.Integer, default=1, nullable=False)
    sector = db.relationship('Sector', backref='clientes')

class Agrimensor(db.Model):
    __tablename__ = 'Tb_Agrimensor'
    IdAgrimensor = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    Nombre = db.Column(db.String(50), nullable=False)
    Apellido = db.Column(db.String(50), nullable=False)
    Nacionalidad = db.Column(db.String(50))
    Cedula = db.Column(db.String(15), nullable=False)
    EstadoCivil = db.Column(db.String(50))
    Sexo = db.Column(db.String(10), nullable=False)
    Profesion = db.Column(db.String(50))
    CODIA = db.Column(db.String(50), nullable=False)
    Celular = db.Column(db.String(50), nullable=False)
    Correo = db.Column(db.String(50), nullable=False)
    Calle = db.Column(db.String(50), nullable=False)
    IdSector = db.Column(db.Integer, db.ForeignKey('Tb_Sector.IdSector'), nullable=False)
    Estatus = db.Column(db.Integer, default=1, nullable=False)
    sector = db.relationship('Sector', backref='agrimensores')

class Notario(db.Model):
    __tablename__ = 'Tb_Notario'
    IdNotario = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    Nombre = db.Column(db.String(50), nullable=False)
    Apellido = db.Column(db.String(50), nullable=False)
    Sexo = db.Column(db.String(10), nullable=False)
    NroColegiatura = db.Column(db.String(50), nullable=False)
    IdSector = db.Column(db.Integer, db.ForeignKey('Tb_Sector.IdSector'), nullable=False)
    Estatus = db.Column(db.Integer, default=1, nullable=False)
    sector = db.relationship('Sector', backref='notarios')

class DepartamentoOficina(db.Model):
    __tablename__ = 'Tb_DepartamentoOficina'
    IdDepartamentoOficina = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    DepartamentoOficina = db.Column(db.String(50), nullable=False)
    Encargado = db.Column(db.String(50))
    IdSector = db.Column(db.Integer, db.ForeignKey('Tb_Sector.IdSector'), nullable=False)
    Estatus = db.Column(db.Integer, default=1, nullable=False)
    sector = db.relationship('Sector', backref='departamentos')

class Sector(db.Model):
    __tablename__ = 'Tb_Sector'
    IdSector = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    Sector = db.Column(db.String(50), nullable=False)
    Municipio = db.Column(db.String(50), nullable=False)
    Provincia = db.Column(db.String(50), nullable=False)
    Pais=db.Column(db.String(50), nullable=False)
    Estatus = db.Column(db.Integer, default=1, nullable=False)

class DerechoSustentado(db.Model):
    __tablename__ = 'Tb_DerechoSustentado'
    IdDerechoSustentado = db.Column(db.Integer, primary_key=True)
    DerechoSustentado = db.Column(db.String(100), nullable=False)
    Estatus = db.Column(db.Integer, default=1, nullable=False)

    #declaraciones_posesion = db.relationship('DeclaracionPosesion', backref='derecho_sustentado')

    # Relación con SolicitudAutorizacion
    #solicitudes = db.relationship("SolicitudAutorizacion", backref="derecho_sustentado")

class SolicitudAutorizacion(db.Model):
    __tablename__ = 'Tb_SolicitudAutorizacion'
    IdSolicitud = db.Column(db.Integer, primary_key=True)
    IdCliente01 = db.Column(db.Integer, db.ForeignKey('Tb_Clientes.IdCliente'), nullable=False)
    IdCliente02 = db.Column(db.Integer, db.ForeignKey('Tb_Clientes.IdCliente'), nullable=False)
    IdAgrimensor = db.Column(db.Integer, db.ForeignKey('Tb_Agrimensor.IdAgrimensor'), nullable=False)
    IdNotario = db.Column(db.Integer, db.ForeignKey('Tb_Notario.IdNotario'), nullable=False)
    FechaAutorizacion = db.Column(db.Date, nullable=False)
    ActuacionTecnica = db.Column(db.String(250), nullable=False)
    Parcela = db.Column(db.String(10), nullable=False)
    DistritoCatrastal = db.Column(db.String(10), nullable=False)
    Calle = db.Column(db.String(100), nullable=False)
    IdSector = db.Column(db.Integer, db.ForeignKey('Tb_Sector.IdSector'), nullable=False)
    Area = db.Column(db.Numeric, nullable=False)
    CoordLatitud = db.Column(db.String(50))
    CoordLongitud = db.Column(db.String(50))
    CoordX=db.Column(db.String(50))
    CoordY=db.Column(db.String(50))
    FechaContratoVenta = db.Column(db.Date, nullable=False)
    IdDepartamentoOficina = db.Column(db.Integer, db.ForeignKey('Tb_DepartamentoOficina.IdDepartamentoOficina'), nullable=False)
    IdDerechoSustentado = db.Column(db.Integer, db.ForeignKey('Tb_DerechoSustentado.IdDerechoSustentado'), nullable=False)
    NroExpediente = db.Column(db.Integer)
    Enlace = db.Column(db.String(500), nullable=True)
    Estatus = db.Column(db.Integer, default=1, nullable=False)
    cliente1 = db.relationship("Cliente", foreign_keys=[IdCliente01])
    cliente2 = db.relationship("Cliente", foreign_keys=[IdCliente02])
    agrimensor = db.relationship("Agrimensor")
    notario = db.relationship("Notario")
    sector = db.relationship("Sector")
    departamento_oficina = db.relationship("DepartamentoOficina")
    derecho_sustentado = db.relationship("DerechoSustentado")
    checkSolicitud = db.Column(db.Boolean, nullable=True, default=False)

    avisos_mensura = db.relationship("AvisoMensura", back_populates="solicitud_autorizacion", cascade="all, delete-orphan")

class AvisoMensura(db.Model):
    __tablename__ = 'Tb_AvisoMensura'
    IdAvisoMensura = db.Column(db.Integer, primary_key=True, autoincrement=True)
    IdSolicitud = db.Column(db.Integer, db.ForeignKey('Tb_SolicitudAutorizacion.IdSolicitud'), nullable=False)
    FechaHoraMensura = db.Column(db.DateTime)
    FechaAutorizacion = db.Column(db.Date)
    IdDepartamentoOficina = db.Column(db.Integer, db.ForeignKey('Tb_DepartamentoOficina.IdDepartamentoOficina'), nullable=False)
    Enlace = db.Column(db.String(500), nullable=True)
    Estatus = db.Column(db.Integer, default=1, nullable=False)

    solicitud_autorizacion = db.relationship("SolicitudAutorizacion", back_populates="avisos_mensura")
    departamento_oficina = db.relationship("DepartamentoOficina")

    avisos_periodicos = db.relationship("AvisoPeriodico", back_populates="aviso_mensura", cascade="all, delete-orphan")

class AvisoPeriodico(db.Model):
    __tablename__ = 'Tb_AvisoPeriodico'
    IdAvisoPeriodico = db.Column(db.Integer, primary_key=True, autoincrement=True)
    IdAvisoMensura = db.Column(db.Integer, db.ForeignKey('Tb_AvisoMensura.IdAvisoMensura'), nullable=False)
    Enlace = db.Column(db.String(500), nullable=True)
    Estatus = db.Column(db.Integer, default=1, nullable=False)

    aviso_mensura = db.relationship("AvisoMensura", back_populates="avisos_periodicos")

    avisos_colindantes = db.relationship("AvisoColindantes", back_populates="aviso_periodico", cascade="all, delete-orphan")

class AvisoColindantes(db.Model):
    __tablename__ = 'Tb_AvisoColindantes'
    IdAvisoColindantes = db.Column(db.Integer, primary_key=True, autoincrement=True)
    IdAvisoPeriodico = db.Column(db.Integer, db.ForeignKey('Tb_AvisoPeriodico.IdAvisoPeriodico'), nullable=False)
    Enlace = db.Column(db.String(500), nullable=True)
    Estatus = db.Column(db.Integer, default=1, nullable=False)
    FechaVencimiento = db.Column(db.Date, nullable=False)

    checkMensura = db.Column(db.Boolean, nullable=True, default=False)
    checkPeriodico = db.Column(db.Boolean, nullable=True, default=False)
    checkColindantes = db.Column(db.Boolean, nullable=True, default=False)

    EnlaceProrroga = db.Column(db.String(500), nullable=True)

    aviso_periodico = db.relationship("AvisoPeriodico", back_populates="avisos_colindantes")

class CartaConformidad(db.Model):
    __tablename__ = 'Tb_CartaConformidad'
    IdConformidad = db.Column(db.Integer, primary_key=True)
    IdSolicitud = db.Column(db.Integer, nullable=False)
    IdAvisoColindantes = db.Column(db.Integer, db.ForeignKey('Tb_AvisoColindantes.IdAvisoColindantes'), nullable=False)
    Enlace = db.Column(db.String(500), nullable=True)
    Estatus = db.Column(db.Integer, default=1, nullable=False)

    aviso_colindantes = db.relationship('AvisoColindantes', backref='cartas_conformidad')
    declaraciones_posesion = db.relationship('DeclaracionPosesion', backref='carta_conformidad')

class DeclaracionPosesion(db.Model):
    __tablename__ = 'Tb_DeclaracionPosesion'
    IdDeclaracionPosesion = db.Column(db.Integer, primary_key=True)
    IdConformidad = db.Column(db.Integer, db.ForeignKey('Tb_CartaConformidad.IdConformidad'), nullable=False)
    IdDerechoSustentado = db.Column(db.Integer, db.ForeignKey('Tb_DerechoSustentado.IdDerechoSustentado'), nullable=False)
    FechaDocumentoDerecho = db.Column(db.Date)
    Enlace = db.Column(db.String(500), nullable=True)
    Estatus = db.Column(db.Integer, default=1, nullable=False)

    informe_tecnico = db.relationship('InformeTecnico', backref='declaracion_posesion')

class AreaDiferencia(db.Model):
    __tablename__ = 'Tb_AreaDiferencia'
    IdAreaDiferencia = db.Column(db.Integer, primary_key=True)
    AreaDiferencia = db.Column(db.String(100), nullable=False)
    Estatus = db.Column(db.Integer, default=1, nullable=False)

    informes_tecnicos = db.relationship('InformeTecnico', backref='area_diferencia')

class InformeTecnico(db.Model):
    __tablename__ = 'Tb_InformeTecnico'
    IdInformeTecnico = db.Column(db.Integer, primary_key=True)
    IdDeclaracionPosesion = db.Column(db.Integer, db.ForeignKey('Tb_DeclaracionPosesion.IdDeclaracionPosesion'), nullable=False)
    FechaHoraInicioMensura = db.Column(db.DateTime)
    HoraFinMesura = db.Column(db.Time)
    FechaDocumentoDerecho = db.Column(db.Date)
    IdAreaDiferencia = db.Column(db.Integer, db.ForeignKey('Tb_AreaDiferencia.IdAreaDiferencia'), nullable=False)
    AreaTotal = db.Column(db.Numeric(20,2))
    AreaDiferenciada=db.Column(db.Numeric(20,2))
    DelimitacionNorte = db.Column(db.String(100), nullable=False)
    DelimitacionSur = db.Column(db.String(100), nullable=False)
    DelimitacionOeste = db.Column(db.String(100), nullable=False)
    DelimitacionEste = db.Column(db.String(100), nullable=False)
    Enlace = db.Column(db.String(500), nullable=True)
    #Enlace_Prorroga = db.Column(db.String(500), nullable=True)
    Estatus = db.Column(db.Integer, default=1, nullable=False)
    
    NombreEquipo = db.Column(db.String(500), nullable=True)
    ModeloEquipo = db.Column(db.String(500), nullable=True)

    checkCarta = db.Column(db.Boolean, nullable=True, default=False)
    checkDeclaracion = db.Column(db.Boolean, nullable=True, default=False)
    checkInforme = db.Column(db.Boolean, nullable=True, default=False)

    UbicacionInmueble = db.Column(db.String(255), nullable=True)
    DescripcionInmueble = db.Column(db.String(255), nullable=True)

    EnlaceActaHitos = db.Column(db.String(500), nullable=True)

# Esquemas de Serialización
class RolSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Rol
        include_fk=True

class UsuarioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model=Usuario
        include_fk=True

class ClienteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model=Cliente
        include_fk=True
    Sexo = ma.String()
    Sector = ma.Nested('SectorSchema', many=False)

class AgrimensorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model=Agrimensor
        include_fk=True
    Sexo = ma.String()
    Sector = ma.Nested('SectorSchema', many=False)

class NotarioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model=Notario
        include_fk=True
    Sexo = ma.String()
    Sector = ma.Nested('SectorSchema', many=False)

class DepartamentoOficinaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DepartamentoOficina
        include_fk=True
    # Incluimos la relación con el sector
    sector = ma.Nested('SectorSchema', many=False)

class SectorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Sector

class DerechoSustentadoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DerechoSustentado

class SolicitudAutorizacionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SolicitudAutorizacion
        include_fk = True

    Cliente01 = ma.Nested(ClienteSchema)
    Cliente02 = ma.Nested(ClienteSchema)
    Agrimensor = ma.Nested(AgrimensorSchema)
    Notario = ma.Nested(NotarioSchema)
    Sector = ma.Nested(SectorSchema)
    DerechoSustentado=ma.Nested(DerechoSustentadoSchema)
    DepartamentoOficina = ma.Nested(DepartamentoOficinaSchema)
    
class AvisomensuraSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AvisoMensura
        include_fk = True

class AvisoPeriodicoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AvisoPeriodico
        include_fk = True

class AvisoColindantesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AvisoColindantes
        include_fk = True

class CartaConformidadSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CartaConformidad
        include_fk = True

class DeclaracionPosesionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DeclaracionPosesion
        include_fk = True

class AreaDiferenciaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AreaDiferencia

class InformeTecnicoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = InformeTecnico
        include_fk = True
    AreaDiferenciada = ma.Decimal()

rol_schema = RolSchema()
roles_schema = RolSchema(many=True)
usuario_schema = UsuarioSchema()
usuarios_schema = UsuarioSchema(many=True)
cliente_schema = ClienteSchema()
clientes_schema = ClienteSchema(many=True)
agrimensor_schema = AgrimensorSchema()
agrimensores_schema = AgrimensorSchema(many=True)
notario_schema = NotarioSchema()
notarios_schema = NotarioSchema(many=True)
departamento_oficina_schema = DepartamentoOficinaSchema()
departamentos_oficina_schema = DepartamentoOficinaSchema(many=True)
sector_schema = SectorSchema()
sectores_schema = SectorSchema(many=True)
solicitud_autorizacion_schema = SolicitudAutorizacionSchema()
solicitudes_autorizacion_schema = SolicitudAutorizacionSchema(many=True)
avisomensura_schema = AvisomensuraSchema()
avisomensuras_schema = AvisomensuraSchema(many=True)
aviso_periodico_schema = AvisoPeriodicoSchema()
aviso_periodicos_schema = AvisoPeriodicoSchema(many=True)
aviso_colindantes_schema = AvisoColindantesSchema()
aviso_colindantess_schema = AvisoColindantesSchema(many=True)

carta_conformidad_schema = CartaConformidadSchema()
cartas_conformidad_schema = CartaConformidadSchema(many=True)
declaracion_posesion_schema = DeclaracionPosesionSchema()
declaraciones_posesion_schema = DeclaracionPosesionSchema(many=True)
derecho_sustentado_schema=DerechoSustentadoSchema()
derechos_sustentados_schema=DerechoSustentadoSchema(many=True)
area_diferencia_schema=AreaDiferenciaSchema()
area_diferencias_schema=AreaDiferenciaSchema(many=True)
declaracion_posesion_schema=DeclaracionPosesionSchema()
declaraciones_posesion_schema=DeclaracionPosesionSchema(many=True)
informe_tecnico_schema=InformeTecnicoSchema()
informes_tecnico_schema=InformeTecnicoSchema(many=True)

# Rutas para Tb_Rol
@app.route('/roles', methods=['GET'])
def get_roles():
    try:
        roles = Rol.query.all()
        return jsonify(roles_schema.dump(roles))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/rol/<int:id>', methods=['GET'])
def get_rol(id):
    try:
        rol = Rol.query.get(id)
        if rol:
            return rol_schema.jsonify(rol)
        return jsonify({"error": "Rol no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/rol', methods=['POST'])
def add_rol():
    try:
        rol = request.json['Rol']
        estatus = request.json['Estatus']
        nuevo_rol = Rol(Rol=rol, Estatus=estatus)
        try:
            db.session.add(nuevo_rol)
            db.session.commit()
            return rol_schema.jsonify(nuevo_rol)
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/rol/<int:id>', methods=['PUT'])
def update_rol(id):
    try:
        rol = Rol.query.get(id)
        if rol:
            rol.Rol = request.json['Rol']
            rol.Estatus = request.json['Estatus']
            try:
                db.session.commit()
                return rol_schema.jsonify(rol)
            except Exception as e:
                db.session.rollback()
                return jsonify({"error": str(e)}), 400
        return jsonify({"error": "Rol no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
@app.route('/rol/<int:id>', methods=['DELETE'])
def delete_rol(id):
    try:
        rol = Rol.query.get(id)
        if Rol:
            rol.Estatus = 0 
            try:
                db.session.commit()
                return jsonify({"message": "Rol eliminado con éxito."})
            except Exception as e:
                db.session.rollback()
                return jsonify({"error": str(e)}), 400
        return jsonify({"error": "Rol no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rutas para Tb_Usuario
@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    try:
        usuarios = db.session.query(Usuario, Rol).join(Rol, Usuario.IdRol == Rol.IdRol).all()
        result = []
        for usuario, rol in usuarios:
            usuario_data = usuario_schema.dump(usuario)
            usuario_data['Rol'] = rol_schema.dump(rol)
            result.append(usuario_data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/usuario/<int:id>', methods=['GET'])
def get_usuario(id):
    try:
        usuario = db.session.query(Usuario, Rol).join(Rol, Usuario.IdRol == Rol.IdRol).filter(Usuario.IdUsuario == id).first()
        if usuario:
            usuario_data = usuario_schema.dump(usuario[0])
            usuario_data['Rol'] = rol_schema.dump(usuario[1])
            return jsonify(usuario_data)
        return jsonify({"error": "Usuario no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/usuario', methods=['POST'])
def add_usuario():
    try:
        usuario = request.json['Usuario']
        email = request.json['Email']
        contraseña = request.json['Contraseña']
        nombre = request.json['Nombre']
        id_rol = request.json['IdRol']
        estatus = request.json['Estatus']
        nuevo_usuario = Usuario(Usuario=usuario, Email=email, Contraseña=contraseña, Nombre=nombre, IdRol=id_rol, Estatus=estatus)
        try:
            db.session.add(nuevo_usuario)
            db.session.commit()
            return usuario_schema.jsonify(nuevo_usuario)
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/usuario/<int:id>', methods=['PUT'])
def update_usuario(id):
    try:
        usuario = Usuario.query.get(id)
        if usuario:
            usuario.Usuario = request.json['Usuario']
            usuario.Email = request.json['Email']
            usuario.Contraseña = request.json['Contraseña']
            usuario.Nombre = request.json['Nombre']
            usuario.IdRol = request.json['IdRol']
            usuario.Estatus = request.json['Estatus']
            try:
                db.session.commit()
                return usuario_schema.jsonify(usuario)
            except Exception as e:
                db.session.rollback()
                return jsonify({"error": str(e)}), 400
        return jsonify({"error": "Usuario no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/usuario/<int:id>', methods=['DELETE'])
def delete_usuario(id):
    try:
        usuario = Usuario.query.get(id)
        if usuario:
            usuario.Estatus = 0 
            try:
                db.session.commit()
                return jsonify({"message": "Usuario eliminado con éxito."})
            except Exception as e:
                db.session.rollback()
                return jsonify({"error": str(e)}), 400
        return jsonify({"error": "Usuario no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#Ruta para Login
@app.route('/login', methods=['POST'])
def login():
    try:
        if request.is_json:
            usuario_o_correo = request.json['usuario']
            contraseña = request.json['contraseña']
        else:
            # Si es una solicitud de formulario web
            usuario_o_correo = request.form['email']
            contraseña = request.form['password']

        # Verificar si el usuario o correo coinciden con la contraseña
        # admin@gmail.com / admin01
        user = db.session.query(Usuario, Rol).join(
            Rol, Usuario.IdRol == Rol.IdRol
        ).filter(
            (Usuario.Usuario == usuario_o_correo) | (Usuario.Email == usuario_o_correo),
            Usuario.Contraseña == contraseña,
            Usuario.Estatus == 1
        ).first()

        if user:
            usuario_data = {
                "IdUsuario": user[0].IdUsuario,
                "Usuario": user[0].Usuario,
                "Email": user[0].Email,
                "Rol": user[1].Rol,  # rol del usuario
                "message": "Login exitoso"
            }
                        
            if request.is_json:
                return jsonify(usuario_data), 200
            else:
                # Lógica para iniciar sesión en la aplicación web (por ejemplo, establecer sesiones)
                return jsonify(usuario_data), 200
        else:
            if request.is_json:
                return jsonify({"error": "Credenciales incorrectas"}), 401
            else:
                return render_template('login.html', error='Credenciales incorrectas')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rutas para Tb_Cliente
@app.route('/clientes', methods=['GET'])
def get_clientes():
    try:
        clientes = db.session.query(Cliente, Sector).join(Sector, Cliente.IdSector == Sector.IdSector).all()
        result = []
        for cliente, sector in clientes:
            cliente_data = cliente_schema.dump(cliente)
            #cliente_data['Sector'] = sector_schema.dump(sector)
            result.append(cliente_data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/cliente/<int:id>', methods=['GET'])
def get_cliente(id):
    try:
        cliente = Cliente.query.get(id)
        if cliente:
            return cliente_schema.jsonify(cliente)
        return jsonify({"error": "Cliente no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/cliente', methods=['POST'])
def add_cliente():
    try:
        nombre = request.json['Nombre']
        apellido = request.json['Apellido']
        cedula_pasaporte = request.json['CedulaPasaporte']
        nacionalidad = request.json['Nacionalidad']
        estado_civil = request.json['EstadoCivil']
        sexo=request.json['Sexo']
        ocupacion = request.json['Ocupacion']
        celular = request.json['Celular']
        correo = request.json['Correo']
        calle = request.json['Calle']
        id_sector = request.json['IdSector']
        estatus = request.json['Estatus']
        
        # Busca el sector
        sector = Sector.query.get(id_sector)
        if not sector:
            return jsonify({"error": "Sector no encontrado"}), 404
        
        nuevo_cliente = Cliente(Nombre=nombre, Apellido=apellido, CedulaPasaporte=cedula_pasaporte, Nacionalidad=nacionalidad, EstadoCivil=estado_civil, 
                                Sexo=sexo, Ocupacion=ocupacion, Celular=celular, Correo=correo, Calle=calle, IdSector=sector.IdSector, Estatus=estatus)
        try:
            db.session.add(nuevo_cliente)
            db.session.commit()
            return cliente_schema.jsonify(nuevo_cliente)
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/cliente/<int:id>', methods=['PUT'])
def update_cliente(id):
    try:
        cliente = Cliente.query.get(id)
        if cliente:
            cliente.Nombre = request.json['Nombre']
            cliente.Apellido = request.json['Apellido']
            cliente.CedulaPasaporte = request.json['CedulaPasaporte']
            cliente.Nacionalidad = request.json.get('Nacionalidad', cliente.Nacionalidad)
            cliente.EstadoCivil = request.json.get('EstadoCivil', cliente.EstadoCivil)
            cliente.Sexo=request.json.get('Sexo', cliente.Sexo)
            cliente.Ocupacion = request.json.get('Ocupacion', cliente.Ocupacion)
            cliente.Celular = request.json['Celular']
            cliente.Correo = request.json['Correo']
            cliente.Calle = request.json['Calle']
            id_sector = request.json['IdSector']
            cliente.IdSector = id_sector
            cliente.Estatus = request.json['Estatus']
            try:
                db.session.commit()
                return cliente_schema.jsonify(cliente)
            except Exception as e:
                db.session.rollback()
                return jsonify({"error": str(e)}), 400
        return jsonify({"error": "Cliente no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/cliente/<int:id>', methods=['DELETE'])
def delete_cliente(id):
    try:
        cliente = Cliente.query.get(id)
        if cliente:
            cliente.Estatus = 0 
            try:
                db.session.commit()
                return jsonify({"message": "Cliente eliminado con éxito."})
            except Exception as e:
                db.session.rollback()
                return jsonify({"error": str(e)}), 400
        return jsonify({"error": "Cliente no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rutas para Tb_Agrimensor
@app.route('/agrimensores', methods=['GET'])
def get_agrimensores():
    try:
        agrimensores = db.session.query(Agrimensor, Sector).join(Sector, Agrimensor.IdSector == Sector.IdSector).all()
        result = []
        for agrimensor, sector in agrimensores:
            agrimensor_data = agrimensor_schema.dump(agrimensor)
            #agrimensor_data['Sector'] = sector_schema.dump(sector)
            result.append(agrimensor_data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/agrimensor/<int:id>', methods=['GET'])
def get_agrimensor(id):
    try:
        agrimensor = Agrimensor.query.get(id)
        if agrimensor:
            return agrimensor_schema.jsonify(agrimensor)
        return jsonify({"error": "Agrimensor no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/agrimensor', methods=['POST'])
def add_agrimensor():
    try:
        nombre = request.json['Nombre']
        apellido = request.json['Apellido']
        nacionalidad = request.json.get('Nacionalidad', None)
        cedula = request.json['Cedula']
        estado_civil = request.json.get('EstadoCivil', None)
        sexo=request.json.get('Sexo')
        profesion = request.json.get('Profesion', None)
        codia = request.json['CODIA']
        celular = request.json['Celular']
        correo = request.json['Correo']
        calle = request.json['Calle']
        sector = request.json['Sector']
        id_sector = request.json['IdSector']
        estatus = request.json['Estatus']

        # Busca el sector
        sector = Sector.query.get(id_sector)
        if not sector:
            return jsonify({"error": "Sector no encontrado"}), 404
        
        nuevo_agrimensor = Agrimensor(
            Nombre=nombre, Apellido=apellido, Nacionalidad=nacionalidad,
            Cedula=cedula, EstadoCivil=estado_civil, Profesion=profesion, Sexo=sexo,
            CODIA=codia, Celular=celular, Correo=correo, Calle=calle,
            IdSector=sector.IdSector, Estatus=estatus
        )
        try:
            db.session.add(nuevo_agrimensor)
            db.session.commit()
            return agrimensor_schema.jsonify(nuevo_agrimensor)
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/agrimensor/<int:id>', methods=['PUT'])
def update_agrimensor(id):
    try:
        agrimensor = Agrimensor.query.get(id)
        if agrimensor:
            agrimensor.Nombre = request.json['Nombre']
            agrimensor.Apellido = request.json['Apellido']
            agrimensor.Nacionalidad = request.json.get('Nacionalidad', agrimensor.Nacionalidad)
            agrimensor.Cedula = request.json['Cedula']
            agrimensor.EstadoCivil = request.json.get('EstadoCivil', agrimensor.EstadoCivil)
            agrimensor.Sexo=request.json.get('Sexo', agrimensor.Sexo)
            agrimensor.Profesion = request.json.get('Profesion', agrimensor.Profesion)
            agrimensor.CODIA = request.json['CODIA']
            agrimensor.Celular = request.json['Celular']
            agrimensor.Correo = request.json['Correo']
            agrimensor.Calle = request.json['Calle']
            agrimensor.Sector = request.json['Sector']
            id_sector = request.json['IdSector']
            agrimensor.IdSector = id_sector
            agrimensor.Estatus = request.json['Estatus']
            try:
                db.session.commit()
                return agrimensor_schema.jsonify(agrimensor)
            except Exception as e:
                db.session.rollback()
                return jsonify({"error": str(e)}), 400
        return jsonify({"error": "Agrimensor no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/agrimensor/<int:id>', methods=['DELETE'])
def delete_agrimensor(id):
    try:
        agrimensor = Agrimensor.query.get(id)
        if agrimensor:
            agrimensor.Estatus = 0 
            try:
                db.session.commit()
                return jsonify({"message": "Agrimensor eliminado con éxito."})
            except Exception as e:
                db.session.rollback()
                return jsonify({"error": str(e)}), 400
        return jsonify({"error": "Agrimensor no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rutas para Tb_Notario
@app.route('/notarios', methods=['GET'])
def get_notarios():
    try:
        notarios = db.session.query(Notario, Sector).join(Sector, Notario.IdSector == Sector.IdSector).all()
        result = []
        for notario, sector in notarios:
            notario_data = notario_schema.dump(notario)
            #notario_data['Sector'] = sector_schema.dump(sector)
            result.append(notario_data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/notario/<int:id>', methods=['GET'])
def get_notario(id):
    try:
        notario = Notario.query.get(id)
        if notario:
            return notario_schema.jsonify(notario)
        return jsonify({"error": "Notario no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/notario', methods=['POST'])
def add_notario():
    try:
        nombre = request.json['Nombre']
        apellido = request.json['Apellido']
        id_sector = request.json['IdSector']  # ID del sector
        sexo=request.json['Sexo']
        nro_colegiatura = request.json['NroColegiatura']
        estatus = request.json['Estatus']

        # Busca el sector
        sector = Sector.query.get(id_sector)
        if not sector:
            return jsonify({"error": "Sector no encontrado"}), 404
        
        nuevo_notario = Notario(
            Nombre=nombre, Apellido=apellido, NroColegiatura=nro_colegiatura,Sexo=sexo,
            IdSector=sector.IdSector, Estatus=estatus
        )

        try:
            db.session.add(nuevo_notario)
            db.session.commit()
            return notario_schema.jsonify(nuevo_notario)
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/notario/<int:id>', methods=['PUT'])
def update_notario(id):
    try:
        notario = Notario.query.get(id)
        if notario:
            notario.Nombre = request.json['Nombre']
            notario.Apellido = request.json['Apellido']
            id_sector = request.json['IdSector']
            notario.sexo=request.json['Sexo']
            notario.IdSector = id_sector
            notario.NroColegiatura = request.json['NroColegiatura']
            notario.Estatus = request.json['Estatus']
            try:
                db.session.commit()
                return notario_schema.jsonify(notario)
            except Exception as e:
                db.session.rollback()
                return jsonify({"error": str(e)}), 400
        return jsonify({"error": "Notario no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/notario/<int:id>', methods=['DELETE'])
def delete_notario(id):
    try:
        notario = Notario.query.get(id)
        if notario:
            notario.Estatus = 0 
            try:
                db.session.commit()
                return jsonify({"message": "Notario eliminado con éxito."})
            except Exception as e:
                db.session.rollback()
                return jsonify({"error": str(e)}), 400
        return jsonify({"error": "Notario no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rutas para Tb_DepartamentoOficina
@app.route('/departamentos', methods=['GET'])
def get_departamentos():
    try:
        departamentos = db.session.query(DepartamentoOficina, Sector).join(Sector, DepartamentoOficina.IdSector == Sector.IdSector).all()
        result = []
        for departamento, sector in departamentos:
            dept_data = departamento_oficina_schema.dump(departamento)
            #dept_data['Sector'] = sector_schema.dump(sector)
            result.append(dept_data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/departamento/<int:id>', methods=['GET'])
def get_departamento(id):
    try:
        departamento = db.session.query(DepartamentoOficina, Sector).join(Sector, DepartamentoOficina.IdSector == Sector.IdSector).filter(DepartamentoOficina.IdDepartamentoOficina == id).first()
        if departamento:
            dept_data = departamento_oficina_schema.dump(departamento[0])
            #dept_data['Sector'] = sector_schema.dump(departamento[1])
            return jsonify(dept_data)
        else:
            return jsonify({"message": "Departamento no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/departamento', methods=['POST'])
def create_departamento():
    try:
        new_departamento = DepartamentoOficina(
            DepartamentoOficina=request.json['DepartamentoOficina'],
            Encargado=request.json['Encargado'],
            IdSector=request.json['IdSector'],
            Estatus=request.json['Estatus']
        )
        db.session.add(new_departamento)
        db.session.commit()
        return jsonify(departamento_oficina_schema.dump(new_departamento)), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/departamento/<int:id>', methods=['PUT'])
def update_departamento(id):
    try:
        departamento = DepartamentoOficina.query.get(id)
        if departamento:
            departamento.DepartamentoOficina = request.json['DepartamentoOficina']
            departamento.Encargado = request.json['Encargado']
            departamento.IdSector = request.json['IdSector']
            departamento.Estatus = request.json['Estatus']
            db.session.commit()
            return jsonify(departamento_oficina_schema.dump(departamento))
        else:
            return jsonify({"message": "Departamento no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/departamento/<int:id>', methods=['DELETE'])
def delete_departamento(id):
    try:
        departamento = DepartamentoOficina.query.get(id)
        if departamento:
            departamento.Estatus = 0 
            try:
                db.session.commit()
                return jsonify({"message": "Departamento eliminado con éxito."})
            except Exception as e:
                db.session.rollback()
                return jsonify({"error": str(e)}), 400
        return jsonify({"error": "Departamento no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rutas para Tb_Sector
@app.route('/sectores', methods=['GET'])
def get_sectores():
    try:
        sectores = Sector.query.all()
        return jsonify(sectores_schema.dump(sectores))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/sector/<int:id>', methods=['GET'])
def get_sector(id):
    try:
        sector = Sector.query.get(id)
        if sector:
            return jsonify(sector_schema.dump(sector))
        else:
            return jsonify({"message": "Sector no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/sector', methods=['POST'])
def create_sector():
    try:
        new_sector = Sector(
            Sector=request.json['Sector'],
            Municipio=request.json['Municipio'],
            Provincia=request.json['Provincia'],
            Pais=request.json['Pais'],
            Estatus=request.json['Estatus']
        )
        db.session.add(new_sector)
        db.session.commit()
        return jsonify(sector_schema.dump(new_sector)), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/sector/<int:id>', methods=['PUT'])
def update_sector(id):
    try:
        sector = Sector.query.get(id)
        if sector:
            sector.Sector = request.json['Sector']
            sector.Municipio = request.json['Municipio']
            sector.Provincia = request.json['Provincia']
            sector.Pais=request.json['Pais']
            sector.Estatus = request.json['Estatus']
            db.session.commit()
            return jsonify(sector_schema.dump(sector))
        else:
            return jsonify({"message": "Sector no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/sector/<int:id>', methods=['DELETE'])
def delete_sector(id):
    try:
        sector = Sector.query.get(id)
        if sector:
            sector.Estatus = 0 
            try:
                db.session.commit()
                return jsonify({"message": "Sector eliminado con éxito."})
            except Exception as e:
                db.session.rollback()
                return jsonify({"error": str(e)}), 400
        return jsonify({"error": "Sector no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rutas para Tb_SolicitudAutorizacion
@app.route('/solicitudes', methods=['GET'])
def get_solicitudes():
    try:
        cliente01_alias = aliased(Cliente)
        cliente02_alias = aliased(Cliente)
        sector_cliente01_alias = aliased(Sector)
        sector_cliente02_alias = aliased(Sector)
        sector_agrimensor_alias = aliased(Sector)
        sector_notario_alias = aliased(Sector)

        solicitudes = db.session.query(
            SolicitudAutorizacion,
            cliente01_alias,
            cliente02_alias,
            sector_cliente01_alias,
            sector_cliente02_alias,
            Agrimensor,
            sector_agrimensor_alias,
            Notario,
            sector_notario_alias,
            Sector,
            DerechoSustentado,
            DepartamentoOficina
        ).join(
            cliente01_alias, SolicitudAutorizacion.IdCliente01 == cliente01_alias.IdCliente
        ).join(
            sector_cliente01_alias, cliente01_alias.IdSector == sector_cliente01_alias.IdSector
        ).join(
            cliente02_alias, SolicitudAutorizacion.IdCliente02 == cliente02_alias.IdCliente
        ).join(
            sector_cliente02_alias, cliente02_alias.IdSector == sector_cliente02_alias.IdSector
        ).join(
            Agrimensor, SolicitudAutorizacion.IdAgrimensor == Agrimensor.IdAgrimensor
        ).join(
            sector_agrimensor_alias, Agrimensor.IdSector == sector_agrimensor_alias.IdSector
        ).join(
            Notario, SolicitudAutorizacion.IdNotario == Notario.IdNotario
        ).join(
            sector_notario_alias, Notario.IdSector == sector_notario_alias.IdSector
        ).join(
            Sector, SolicitudAutorizacion.IdSector == Sector.IdSector
        ).join(
            DerechoSustentado, SolicitudAutorizacion.IdDerechoSustentado == DerechoSustentado.IdDerechoSustentado
        ).join(
            DepartamentoOficina, SolicitudAutorizacion.IdDepartamentoOficina == DepartamentoOficina.IdDepartamentoOficina
        ).order_by(
            SolicitudAutorizacion.IdSolicitud.desc()
        ).all()

        result = []
        for solicitud, cliente1, cliente2, sector_cliente1, sector_cliente2, agrimensor, sector_agrimensor, notario, sector_notario, sector,derecho_sustentado, departamento_oficina in solicitudes:
            solicitud_data = solicitud_autorizacion_schema.dump(solicitud)
            solicitud_data['Cliente01'] = cliente_schema.dump(cliente1)
            solicitud_data['Cliente01']['Sector'] = sector_schema.dump(sector_cliente1)
            solicitud_data['Cliente02'] = cliente_schema.dump(cliente2)
            solicitud_data['Cliente02']['Sector'] = sector_schema.dump(sector_cliente2)
            solicitud_data['Agrimensor'] = agrimensor_schema.dump(agrimensor)
            solicitud_data['Agrimensor']['Sector'] = sector_schema.dump(sector_agrimensor)
            solicitud_data['Notario'] = notario_schema.dump(notario)
            solicitud_data['Notario']['Sector'] = sector_schema.dump(sector_notario)
            solicitud_data['Sector'] = sector_schema.dump(sector)
            solicitud_data['DerechoSustentado'] = derecho_sustentado_schema.dump(derecho_sustentado)
            solicitud_data['DepartamentoOficina'] = departamento_oficina_schema.dump(departamento_oficina)
            result.append(solicitud_data)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/solicitud/<int:id>', methods=['GET'])
def get_solicitud(id):
    try:
        cliente01_alias = aliased(Cliente)
        cliente02_alias = aliased(Cliente)
        sector_cliente01_alias = aliased(Sector)
        sector_cliente02_alias = aliased(Sector)
        sector_agrimensor_alias = aliased(Sector)
        sector_notario_alias = aliased(Sector)

        solicitud = db.session.query(
            SolicitudAutorizacion,
            cliente01_alias,
            cliente02_alias,
            sector_cliente01_alias,
            sector_cliente02_alias,
            Agrimensor,
            sector_agrimensor_alias,
            Notario,
            sector_notario_alias,
            Sector,
            DerechoSustentado,
            DepartamentoOficina
        ).join(
            cliente01_alias, SolicitudAutorizacion.IdCliente01 == cliente01_alias.IdCliente
        ).join(
            sector_cliente01_alias, cliente01_alias.IdSector == sector_cliente01_alias.IdSector
        ).join(
            cliente02_alias, SolicitudAutorizacion.IdCliente02 == cliente02_alias.IdCliente
        ).join(
            sector_cliente02_alias, cliente02_alias.IdSector == sector_cliente02_alias.IdSector
        ).join(
            Agrimensor, SolicitudAutorizacion.IdAgrimensor == Agrimensor.IdAgrimensor
        ).join(
            sector_agrimensor_alias, Agrimensor.IdSector == sector_agrimensor_alias.IdSector
        ).join(
            Notario, SolicitudAutorizacion.IdNotario == Notario.IdNotario
        ).join(
            sector_notario_alias, Notario.IdSector == sector_notario_alias.IdSector
        ).join(
            Sector, SolicitudAutorizacion.IdSector == Sector.IdSector
        ).join(
            DerechoSustentado, SolicitudAutorizacion.IdDerechoSustentado == DerechoSustentado.IdDerechoSustentado
        ).join(
            DepartamentoOficina, SolicitudAutorizacion.IdDepartamentoOficina == DepartamentoOficina.IdDepartamentoOficina
        ).filter(
            SolicitudAutorizacion.IdSolicitud == id
        ).order_by(
            SolicitudAutorizacion.IdSolicitud.desc()
        ).first()

        if solicitud:
            solicitud_data, cliente1, cliente2, sector_cliente1, sector_cliente2, agrimensor, sector_agrimensor, notario, sector_notario, sector, derecho_sustentado, departamento_oficina = solicitud
            result = solicitud_autorizacion_schema.dump(solicitud_data)
            result['Cliente01'] = cliente_schema.dump(cliente1)
            result['Cliente01']['Sector'] = sector_schema.dump(sector_cliente1)
            result['Cliente02'] = cliente_schema.dump(cliente2)
            result['Cliente02']['Sector'] = sector_schema.dump(sector_cliente2)
            result['Agrimensor'] = agrimensor_schema.dump(agrimensor)
            result['Agrimensor']['Sector'] = sector_schema.dump(sector_agrimensor)
            result['Notario'] = notario_schema.dump(notario)
            result['Notario']['Sector'] = sector_schema.dump(sector_notario)
            result['Sector'] = sector_schema.dump(sector)
            result['DerechoSustentado'] = derecho_sustentado_schema.dump(derecho_sustentado)
            result['DepartamentoOficina'] = departamento_oficina_schema.dump(departamento_oficina)
            return jsonify(result)
        
        return jsonify({"error": "Solicitud no encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/solicitud', methods=['POST'])
def add_solicitud():
    try:
        data = request.get_json()

        # Validar la existencia de las llaves foráneas
        cliente1 = Cliente.query.get(data['IdCliente01'])
        cliente2 = Cliente.query.get(data['IdCliente02'])
        agrimensor = Agrimensor.query.get(data['IdAgrimensor'])
        notario = Notario.query.get(data['IdNotario'])
        sector = Sector.query.get(data['IdSector'])
        departamento_oficina = DepartamentoOficina.query.get(data['IdDepartamentoOficina'])
        derecho_sustentado=DerechoSustentado.query.get(data['IdDerechoSustentado'])

        if not (cliente1 and cliente2 and agrimensor and notario and sector and departamento_oficina and derecho_sustentado):
            return jsonify({"error": "Una o más llaves foráneas no existen"}), 400

        nueva_solicitud = SolicitudAutorizacion(
            IdCliente01=data['IdCliente01'],
            IdCliente02=data['IdCliente02'],
            IdAgrimensor=data['IdAgrimensor'],
            IdNotario=data['IdNotario'],
            FechaAutorizacion=data['FechaAutorizacion'],
            ActuacionTecnica=data['ActuacionTecnica'],
            Parcela=data['Parcela'],
            DistritoCatrastal=data['DistritoCatrastal'],
            Calle=data['Calle'],
            IdSector=data['IdSector'],
            Area=data['Area'],
            CoordLatitud=data['CoordLatitud'],
            CoordLongitud=data['CoordLongitud'],
            CoordX=data['CoordX'],
            CoordY=data['CoordY'],
            FechaContratoVenta=data['FechaContratoVenta'],
            IdDepartamentoOficina=data['IdDepartamentoOficina'],
            IdDerechoSustentado = request.json['IdDerechoSustentado'],
            NroExpediente=data.get('NroExpediente'),  # Campo opcional
            Enlace=data['Enlace'],
            Estatus=data['Estatus']
        )

        db.session.add(nueva_solicitud)
        db.session.commit()

        return solicitud_autorizacion_schema.jsonify(nueva_solicitud), 201
    except Exception as e:
        db.session.rollback()  # Revertir cualquier cambio en caso de error
        return jsonify({"error": str(e)}), 500

@app.route('/solicitud/<int:id>', methods=['PUT'])
def update_solicitud(id):
    try:
        solicitud = db.session.query(SolicitudAutorizacion).filter_by(IdSolicitud=id).first()
        if solicitud:
            data = request.get_json()
            solicitud.IdCliente01 = data['IdCliente01']
            solicitud.IdCliente02 = data['IdCliente02']
            solicitud.IdAgrimensor = data['IdAgrimensor']
            solicitud.IdNotario = data['IdNotario']
            solicitud.FechaAutorizacion = data['FechaAutorizacion']
            solicitud.ActuacionTecnica = data['ActuacionTecnica']
            solicitud.Parcela = data['Parcela']
            solicitud.DistritoCatrastal = data['DistritoCatrastal']
            solicitud.Calle = data['Calle']
            solicitud.IdSector = data['IdSector']
            solicitud.Area = data['Area']
            solicitud.CoordLatitud = data['CoordLatitud']
            solicitud.CoordLongitud = data['CoordLongitud']
            solicitud.CoordX=data['CoordX']
            solicitud.CoordY=data['CoordY']
            solicitud.FechaContratoVenta = data['FechaContratoVenta']
            solicitud.IdDepartamentoOficina = data.get('IdDepartamentoOficina')
            solicitud.IdDerechoSustentado=data.get('IdDerechoSustentado')
            solicitud.NroExpediente = data.get('NroExpediente')
            solicitud.Enlace=data['Enlace']
            solicitud.Estatus = data['Estatus']
            db.session.commit()
            return solicitud_autorizacion_schema.jsonify(solicitud)
        return jsonify({"error": "Solicitud no encontrada"}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@app.route('/solicitud_enlace/<int:id>', methods=['PUT'])
def update_solicitud_enlace(id):
    try:
        solicitud = db.session.query(SolicitudAutorizacion).filter_by(IdSolicitud=id).first()
        if solicitud:
            data = request.get_json()
            solicitud.Enlace=data['Enlace']
            db.session.commit()
            return solicitud_autorizacion_schema.jsonify(solicitud)
        return jsonify({"error": "Solicitud no encontrada"}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    
@app.route('/solicitud_expediente/<int:id>', methods=['PUT'])
def update_solicitud_expediente(id):
    try:
        solicitud = db.session.query(SolicitudAutorizacion).filter_by(IdSolicitud=id).first()
        if solicitud:
            data = request.get_json()
            solicitud.NroExpediente = data.get('NroExpediente')
            db.session.commit()
            return solicitud_autorizacion_schema.jsonify(solicitud)
        return jsonify({"error": "Solicitud no encontrada"}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@app.route('/solicitud_estatus/<int:id>', methods=['PUT'])
def update_solicitud_estatus(id):
    try:
        solicitud = db.session.query(SolicitudAutorizacion).filter_by(IdSolicitud=id).first()
        if solicitud:
            data = request.get_json()
            solicitud.Estatus = data['Estatus']
            db.session.commit()
            return solicitud_autorizacion_schema.jsonify(solicitud)
        return jsonify({"error": "Solicitud no encontrada"}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@app.route('/solicitud/<int:id>', methods=['DELETE'])
def delete_solicitud(id):
    try:
        solicitud = db.session.query(SolicitudAutorizacion).filter_by(IdSolicitud=id).first()
        if solicitud:
            solicitud.Estatus = 0  # Actualización del estatus a 0 en lugar de eliminación física
            db.session.commit()
            return solicitud_autorizacion_schema.jsonify(solicitud)
        return jsonify({"error": "Solicitud no encontrada"}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    

@app.route('/solicitud_autorizacion_check_solicitud/<int:id>', methods=['PUT'])
def update_check_solicitud(id):
    data = request.get_json()
    record = SolicitudAutorizacion.query.get(id)
    if 'value' in data:
        setattr(record, 'checkSolicitud', data['value'])
        db.session.commit()
        return jsonify({ 'success': True, 'checkSolicitud': record.checkSolicitud }), 200
    return jsonify({ 'error': 'Invalid data' }), 400

# SEGUNDA ETAPA
# Rutas para Aviso de mensura
@app.route('/avisomensuras', methods=['GET'])
def get_avisomensuras():
    try:
        cliente01_alias = aliased(Cliente)
        cliente02_alias = aliased(Cliente)

        avisos = db.session.query(
            AvisoMensura,
            SolicitudAutorizacion,
            cliente01_alias,
            cliente02_alias,
            Agrimensor,
            Notario,
            Sector,
            DepartamentoOficina,
            DerechoSustentado
        ).join(
            SolicitudAutorizacion, AvisoMensura.IdSolicitud == SolicitudAutorizacion.IdSolicitud
        ).join(
            cliente01_alias, SolicitudAutorizacion.IdCliente01 == cliente01_alias.IdCliente
        ).join(
            cliente02_alias, SolicitudAutorizacion.IdCliente02 == cliente02_alias.IdCliente
        ).join(
            Agrimensor, SolicitudAutorizacion.IdAgrimensor == Agrimensor.IdAgrimensor
        ).join(
            Notario, SolicitudAutorizacion.IdNotario == Notario.IdNotario
        ).join(
            Sector, SolicitudAutorizacion.IdSector == Sector.IdSector
        ).join(
            DepartamentoOficina, AvisoMensura.IdDepartamentoOficina == DepartamentoOficina.IdDepartamentoOficina
        ).join(
            DerechoSustentado, SolicitudAutorizacion.IdDerechoSustentado == DerechoSustentado.IdDerechoSustentado
        ).all()

        result = []
        for aviso, solicitud, cliente1, cliente2, agrimensor, notario, sector, departamento, derecho  in avisos:
            aviso_data = avisomensura_schema.dump(aviso)
            solicitud_data = solicitud_autorizacion_schema.dump(solicitud)
            solicitud_data['Cliente01'] = cliente_schema.dump(cliente1)
            solicitud_data['Cliente02'] = cliente_schema.dump(cliente2)
            solicitud_data['Agrimensor'] = agrimensor_schema.dump(agrimensor)
            solicitud_data['Notario'] = notario_schema.dump(notario)
            solicitud_data['Sector'] = sector_schema.dump(sector)
            solicitud_data['DerechoSustentado'] = derecho_sustentado_schema.dump(derecho)
            aviso_data['SolicitudAutorizacion'] = solicitud_data
            aviso_data['DepartamentoOficina'] = departamento_oficina_schema.dump(departamento)
            result.append(aviso_data)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/avisomensura/<int:id>', methods=['GET'])
def get_avisomensura(id):
    try:
        cliente01_alias = aliased(Cliente)
        cliente02_alias = aliased(Cliente)

        aviso = db.session.query(
            AvisoMensura,
            SolicitudAutorizacion,
            cliente01_alias,
            cliente02_alias,
            Agrimensor,
            Notario,
            Sector,
            DepartamentoOficina,
            DerechoSustentado
        ).join(
            SolicitudAutorizacion, AvisoMensura.IdSolicitud == SolicitudAutorizacion.IdSolicitud
        ).join(
            cliente01_alias, SolicitudAutorizacion.IdCliente01 == cliente01_alias.IdCliente
        ).join(
            cliente02_alias, SolicitudAutorizacion.IdCliente02 == cliente02_alias.IdCliente
        ).join(
            Agrimensor, SolicitudAutorizacion.IdAgrimensor == Agrimensor.IdAgrimensor
        ).join(
            Notario, SolicitudAutorizacion.IdNotario == Notario.IdNotario
        ).join(
            Sector, SolicitudAutorizacion.IdSector == Sector.IdSector
        ).join(
            DepartamentoOficina, AvisoMensura.IdDepartamentoOficina == DepartamentoOficina.IdDepartamentoOficina
        ).join(
            DerechoSustentado, SolicitudAutorizacion.IdDerechoSustentado == DerechoSustentado.IdDerechoSustentado
        ).filter(AvisoMensura.IdAvisoMensura == id).first()

        if aviso:
            aviso_data = avisomensura_schema.dump(aviso[0])
            solicitud_data = solicitud_autorizacion_schema.dump(aviso[1])
            solicitud_data['Cliente01'] = cliente_schema.dump(aviso[2])
            solicitud_data['Cliente02'] = cliente_schema.dump(aviso[3])
            solicitud_data['Agrimensor'] = agrimensor_schema.dump(aviso[4])
            solicitud_data['Notario'] = notario_schema.dump(aviso[5])
            solicitud_data['Sector'] = sector_schema.dump(aviso[6])
            solicitud_data['DerechoSustentado'] = derecho_sustentado_schema.dump(aviso[8])
            aviso_data['SolicitudAutorizacion'] = solicitud_data
            aviso_data['DepartamentoOficina'] = departamento_oficina_schema.dump(aviso[7])
            return jsonify(aviso_data)
        else:
            return jsonify({"message": "Aviso Mensura no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/avisomensura', methods=['POST'])
def add_avisomensura():
    try:
        data = request.get_json()
        nuevo_aviso = AvisoMensura(
            IdSolicitud=data['IdSolicitud'],
            FechaHoraMensura=data['FechaHoraMensura'],
            FechaAutorizacion=data['FechaAutorizacion'],
            IdDepartamentoOficina=data['IdDepartamentoOficina'],
            Enlace=data['Enlace'],
            Estatus=data.get('Estatus', 1)
        )
        db.session.add(nuevo_aviso)
        db.session.commit()
        return avisomensura_schema.jsonify(nuevo_aviso), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/avisomensura/<int:id>', methods=['PUT'])
def update_avisomensura(id):
    try:
        data = request.get_json()
        aviso = AvisoMensura.query.get_or_404(id)
        
        aviso.IdSolicitud = data.get('IdSolicitud', aviso.IdSolicitud)
        aviso.FechaHoraMensura = data.get('FechaHoraMensura', aviso.FechaHoraMensura)
        aviso.FechaAutorizacion = data.get('FechaAutorizacion', aviso.FechaAutorizacion)
        aviso.IdDepartamentoOficina = data.get('IdDepartamentoOficina', aviso.IdDepartamentoOficina)
        aviso.Enlace=data['Enlace']
        aviso.Estatus = data.get('Estatus', aviso.Estatus)
        
        db.session.commit()
        return avisomensura_schema.jsonify(aviso)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/avisomensura_enlace/<int:id>', methods=['PUT'])
def update_avisomensura_enlace(id):
    try:
        data = request.get_json()
        aviso = AvisoMensura.query.get_or_404(id)
        
        aviso.Enlace=data['Enlace']
        
        db.session.commit()
        return avisomensura_schema.jsonify(aviso)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@app.route('/avisomensura_estatus/<int:id>', methods=['PUT'])
def update_avisomensura_estatus(id):
    try:
        data = request.get_json()
        aviso = AvisoMensura.query.get_or_404(id)
        
        aviso.Estatus = data.get('Estatus', aviso.Estatus)
        
        db.session.commit()
        return avisomensura_schema.jsonify(aviso)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@app.route('/avisomensura/<int:id>', methods=['DELETE'])
def delete_avisomensura(id):
    try:
        aviso = db.session.query(AvisoMensura).filter_by(IdAvisoMensura=id).first()
        if aviso:
            aviso.Estatus = 0  # Actualización del estatus a 0 en lugar de eliminación física
            db.session.commit()
            return avisomensura_schema.jsonify(aviso)
        return jsonify({"error": "AvisoMensura no encontrado"}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# Rutas para Aviso de periodico
@app.route('/avisosperiodicos', methods=['GET'])
def get_avisos_periodicos():
    try:
        cliente01_alias = aliased(Cliente)
        cliente02_alias = aliased(Cliente)

        avisos = db.session.query(
            AvisoPeriodico,
            AvisoMensura,
            SolicitudAutorizacion,
            cliente01_alias,
            cliente02_alias,
            Agrimensor,
            Notario,
            Sector,
            DepartamentoOficina,
            DerechoSustentado
        ).join(
            AvisoMensura, AvisoPeriodico.IdAvisoMensura == AvisoMensura.IdAvisoMensura
        ).join(
            SolicitudAutorizacion, AvisoMensura.IdSolicitud == SolicitudAutorizacion.IdSolicitud
        ).join(
            cliente01_alias, SolicitudAutorizacion.IdCliente01 == cliente01_alias.IdCliente
        ).join(
            cliente02_alias, SolicitudAutorizacion.IdCliente02 == cliente02_alias.IdCliente
        ).join(
            Agrimensor, SolicitudAutorizacion.IdAgrimensor == Agrimensor.IdAgrimensor
        ).join(
            Notario, SolicitudAutorizacion.IdNotario == Notario.IdNotario
        ).join(
            Sector, SolicitudAutorizacion.IdSector == Sector.IdSector
        ).join(
            DepartamentoOficina, AvisoMensura.IdDepartamentoOficina == DepartamentoOficina.IdDepartamentoOficina
        ).join(
            DerechoSustentado, SolicitudAutorizacion.IdDerechoSustentado == DerechoSustentado.IdDerechoSustentado
        ).all()

        result = []
        for aviso_periodico, aviso_mensura, solicitud, cliente1, cliente2, agrimensor, notario, sector, departamento, derecho in avisos:
            aviso_periodico_data = aviso_periodico_schema.dump(aviso_periodico)
            aviso_periodico_data['AvisoMensura'] = avisomensura_schema.dump(aviso_mensura)
            solicitud_data = solicitud_autorizacion_schema.dump(solicitud)
            solicitud_data['Cliente01'] = cliente_schema.dump(cliente1)
            solicitud_data['Cliente02'] = cliente_schema.dump(cliente2)
            solicitud_data['Agrimensor'] = agrimensor_schema.dump(agrimensor)
            solicitud_data['Notario'] = notario_schema.dump(notario)
            solicitud_data['Sector'] = sector_schema.dump(sector)
            solicitud_data['DerechoSustentado'] = derecho_sustentado_schema.dump(derecho)
            aviso_periodico_data['SolicitudAutorizacion'] = solicitud_data
            aviso_periodico_data['DepartamentoOficina'] = departamento_oficina_schema.dump(departamento)
            result.append(aviso_periodico_data)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/avisoperiodico/<int:id>', methods=['GET'])
def get_avisoperiodico(id):
    try:
        # Alias para manejar clientes
        cliente01_alias = aliased(Cliente)
        cliente02_alias = aliased(Cliente)

        aviso = db.session.query(
            AvisoPeriodico,
            AvisoMensura,
            SolicitudAutorizacion,
            cliente01_alias,
            cliente02_alias,
            Agrimensor,
            Notario,
            Sector,
            DepartamentoOficina,
            DerechoSustentado
        ).join(
            AvisoMensura, AvisoPeriodico.IdAvisoMensura == AvisoMensura.IdAvisoMensura
        ).join(
            SolicitudAutorizacion, AvisoMensura.IdSolicitud == SolicitudAutorizacion.IdSolicitud
        ).join(
            cliente01_alias, SolicitudAutorizacion.IdCliente01 == cliente01_alias.IdCliente
        ).join(
            cliente02_alias, SolicitudAutorizacion.IdCliente02 == cliente02_alias.IdCliente
        ).join(
            Agrimensor, SolicitudAutorizacion.IdAgrimensor == Agrimensor.IdAgrimensor
        ).join(
            Notario, SolicitudAutorizacion.IdNotario == Notario.IdNotario
        ).join(
            Sector, SolicitudAutorizacion.IdSector == Sector.IdSector
        ).join(
            DepartamentoOficina, AvisoMensura.IdDepartamentoOficina == DepartamentoOficina.IdDepartamentoOficina
        ).join(
            DerechoSustentado, SolicitudAutorizacion.IdDerechoSustentado == DerechoSustentado.IdDerechoSustentado
        ).filter(AvisoPeriodico.IdAvisoPeriodico == id).first()

        if aviso:
            aviso_periodico_data = aviso_periodico_schema.dump(aviso[0])
            aviso_periodico_data['AvisoMensura'] = avisomensura_schema.dump(aviso[1])
            
            solicitud_data = solicitud_autorizacion_schema.dump(aviso[2])
            solicitud_data['Cliente01'] = cliente_schema.dump(aviso[3])
            solicitud_data['Cliente02'] = cliente_schema.dump(aviso[4])
            solicitud_data['Agrimensor'] = agrimensor_schema.dump(aviso[5])
            solicitud_data['Notario'] = notario_schema.dump(aviso[6])
            solicitud_data['Sector'] = sector_schema.dump(aviso[7])
            solicitud_data['DerechoSustentado'] = derecho_sustentado_schema.dump(aviso[8])
            aviso_periodico_data['SolicitudAutorizacion'] = solicitud_data
            aviso_periodico_data['DepartamentoOficina'] = departamento_oficina_schema.dump(aviso[8])

            return jsonify(aviso_periodico_data)
        else:
            return jsonify({"message": "Aviso Periodico no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/avisoperiodico', methods=['POST'])
def add_avisoperiodico():
    try:
        data = request.get_json()
        nuevo_aviso = AvisoPeriodico(
            IdAvisoMensura=data['IdAvisoMensura'],
            Estatus=data.get('Estatus', 1),
            Enlace=data.get('Enlace')
        )
        db.session.add(nuevo_aviso)
        db.session.commit()
        return aviso_periodico_schema.jsonify(nuevo_aviso), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/avisoperiodico/<int:id>', methods=['PUT'])
def update_avisoperiodico(id):
    try:
        data = request.get_json()
        aviso = AvisoPeriodico.query.get_or_404(id)
        
        aviso.IdAvisoMensura = data.get('IdAvisoMensura', aviso.IdAvisoMensura)
        aviso.Estatus = data.get('Estatus', aviso.Estatus)
        aviso.Enlace=data.get('Enlace', aviso.Enlace)

        db.session.commit()
        return aviso_periodico_schema.jsonify(aviso)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/avisoperiodico_enlace/<int:id>', methods=['PUT'])
def update_avisoperiodico_enlace(id):
    try:
        data = request.get_json()
        aviso = AvisoPeriodico.query.get_or_404(id)
        
        aviso.Enlace=data.get('Enlace', aviso.Enlace)

        db.session.commit()
        return aviso_periodico_schema.jsonify(aviso)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@app.route('/avisoperiodico_estatus/<int:id>', methods=['PUT'])
def update_avisoperiodico_estatus(id):
    try:
        data = request.get_json()
        aviso = AvisoPeriodico.query.get_or_404(id)
        
        aviso.Estatus = data.get('Estatus', aviso.Estatus)

        db.session.commit()
        return aviso_periodico_schema.jsonify(aviso)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/avisoperiodico/<int:id>', methods=['DELETE'])
def delete_avisoperiodico(id):
    try:
        aviso = db.session.query(AvisoPeriodico).filter_by(IdAvisoPeriodico=id).first()
        if aviso:
            aviso.Estatus = 0  # Actualización del estatus a 0 en lugar de eliminación física
            db.session.commit()
            return aviso_periodico_schema.jsonify(aviso)
        return jsonify({"error": "AvisoPeriodico no encontrado"}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# Rutas para comunicacion a los colindates
@app.route('/avisoscolindantes', methods=['GET'])
def get_avisos_colindantes():
    try:
        # Crear alias para las tablas involucradas en las uniones
        cliente01_alias = aliased(Cliente)
        cliente02_alias = aliased(Cliente)
        sector_cliente01_alias = aliased(Sector)
        sector_cliente02_alias = aliased(Sector)
        sector_agrimensor_alias = aliased(Sector)
        sector_notario_alias = aliased(Sector)

        # Consulta con INNER JOIN de las tablas relacionadas
        avisos = db.session.query(
            AvisoColindantes,
            AvisoPeriodico,
            AvisoMensura,
            SolicitudAutorizacion,
            cliente01_alias,
            cliente02_alias,
            sector_cliente01_alias,
            sector_cliente02_alias,
            Agrimensor,
            sector_agrimensor_alias,
            Notario,
            Sector,
            sector_notario_alias,
            DepartamentoOficina,
            DerechoSustentado
        ).join(
            AvisoPeriodico, AvisoColindantes.IdAvisoPeriodico == AvisoPeriodico.IdAvisoPeriodico
        ).join(
            AvisoMensura, AvisoPeriodico.IdAvisoMensura == AvisoMensura.IdAvisoMensura
        ).join(
            SolicitudAutorizacion, AvisoMensura.IdSolicitud == SolicitudAutorizacion.IdSolicitud
        ).join(
            cliente01_alias, SolicitudAutorizacion.IdCliente01 == cliente01_alias.IdCliente
        ).join(
            sector_cliente01_alias, cliente01_alias.IdSector == sector_cliente01_alias.IdSector
        ).join(
            cliente02_alias, SolicitudAutorizacion.IdCliente02 == cliente02_alias.IdCliente
        ).join(
            sector_cliente02_alias, cliente02_alias.IdSector == sector_cliente02_alias.IdSector
        ).join(
            Agrimensor, SolicitudAutorizacion.IdAgrimensor == Agrimensor.IdAgrimensor
        ).join(
            sector_agrimensor_alias, Agrimensor.IdSector == sector_agrimensor_alias.IdSector
        ).join(
            Notario, SolicitudAutorizacion.IdNotario == Notario.IdNotario
        ).join(
            sector_notario_alias, Notario.IdSector == sector_notario_alias.IdSector
        ).join(
            Sector, SolicitudAutorizacion.IdSector == Sector.IdSector
        ).join(
            DepartamentoOficina, AvisoMensura.IdDepartamentoOficina == DepartamentoOficina.IdDepartamentoOficina
        ).join(
            DerechoSustentado, SolicitudAutorizacion.IdDerechoSustentado == DerechoSustentado.IdDerechoSustentado
        ).order_by(
            AvisoColindantes.IdAvisoColindantes.desc()
        ).all()

        result = []
        for aviso_colindantes, aviso_periodico, aviso_mensura, solicitud, cliente1, sector_cliente1, cliente2, sector_cliente2, agrimensor, sector_agrimensor, notario, sector, sector_notario, departamento, derecho  in avisos:
            aviso_colindantes_data = aviso_colindantes_schema.dump(aviso_colindantes)
            aviso_colindantes_data['AvisoPeriodico'] = aviso_periodico_schema.dump(aviso_periodico)
            aviso_colindantes_data['AvisoMensura'] = avisomensura_schema.dump(aviso_mensura)
            solicitud_data = solicitud_autorizacion_schema.dump(solicitud)
            solicitud_data['Cliente01'] = cliente_schema.dump(cliente1)
            solicitud_data['Cliente01']['Sector'] = sector_schema.dump(sector_cliente1)
            solicitud_data['Cliente02'] = cliente_schema.dump(cliente2)
            solicitud_data['Cliente02']['Sector'] = sector_schema.dump(sector_cliente2)
            solicitud_data['Agrimensor'] = agrimensor_schema.dump(agrimensor)
            solicitud_data['Agrimensor']['Sector'] = sector_schema.dump(sector_agrimensor)
            solicitud_data['Notario'] = notario_schema.dump(notario)
            solicitud_data['Notario']['Sector'] = sector_schema.dump(sector_notario)
            solicitud_data['Sector'] = sector_schema.dump(sector)
            solicitud_data['DerechoSustentado'] = derecho_sustentado_schema.dump(derecho)
            aviso_colindantes_data['SolicitudAutorizacion'] = solicitud_data
            aviso_colindantes_data['DepartamentoOficina'] = departamento_oficina_schema.dump(departamento)
            result.append(aviso_colindantes_data)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/avisocolindantes/<int:id>', methods=['GET'])
def get_avisocolindantes(id):
    try:
        # Crear alias para las tablas involucradas en las uniones
        cliente01_alias = aliased(Cliente)
        cliente02_alias = aliased(Cliente)
        sector_cliente01_alias = aliased(Sector)
        sector_cliente02_alias = aliased(Sector)
        sector_agrimensor_alias = aliased(Sector)
        sector_notario_alias = aliased(Sector)

        # Consulta con INNER JOIN de las tablas relacionadas y filtro por ID
        aviso = db.session.query(
            AvisoColindantes,
            AvisoPeriodico,
            AvisoMensura,
            SolicitudAutorizacion,
            cliente01_alias,
            cliente02_alias,
            sector_cliente01_alias,
            sector_cliente02_alias,
            Agrimensor,
            sector_agrimensor_alias,
            Notario,
            sector_notario_alias,
            Sector,
            DepartamentoOficina,
            DerechoSustentado
        ).join(
            AvisoPeriodico, AvisoColindantes.IdAvisoPeriodico == AvisoPeriodico.IdAvisoPeriodico
        ).join(
            AvisoMensura, AvisoPeriodico.IdAvisoMensura == AvisoMensura.IdAvisoMensura
        ).join(
            SolicitudAutorizacion, AvisoMensura.IdSolicitud == SolicitudAutorizacion.IdSolicitud
        ).join(
            cliente01_alias, SolicitudAutorizacion.IdCliente01 == cliente01_alias.IdCliente
        ).join(
            sector_cliente01_alias, cliente01_alias.IdSector == sector_cliente01_alias.IdSector
        ).join(
            cliente02_alias, SolicitudAutorizacion.IdCliente02 == cliente02_alias.IdCliente
        ).join(
            sector_cliente02_alias, cliente02_alias.IdSector == sector_cliente02_alias.IdSector
        ).join(
            Agrimensor, SolicitudAutorizacion.IdAgrimensor == Agrimensor.IdAgrimensor
        ).join(
            sector_agrimensor_alias, Agrimensor.IdSector == sector_agrimensor_alias.IdSector
        ).join(
            Notario, SolicitudAutorizacion.IdNotario == Notario.IdNotario
        ).join(
            sector_notario_alias, Notario.IdSector == sector_notario_alias.IdSector
        ).join(
            Sector, SolicitudAutorizacion.IdSector == Sector.IdSector
        ).join(
            DepartamentoOficina, AvisoMensura.IdDepartamentoOficina == DepartamentoOficina.IdDepartamentoOficina
        ).join(
            DerechoSustentado, SolicitudAutorizacion.IdDerechoSustentado == DerechoSustentado.IdDerechoSustentado
        ).filter(
            AvisoColindantes.IdAvisoColindantes == id
        ).order_by(
            AvisoColindantes.IdAvisoColindantes.desc()
        ).first()

        if aviso:
            aviso_colindantes_data = aviso_colindantes_schema.dump(aviso[0])
            aviso_colindantes_data['AvisoPeriodico'] = aviso_periodico_schema.dump(aviso[1])
            aviso_colindantes_data['AvisoMensura'] = avisomensura_schema.dump(aviso[2])
            solicitud_data = solicitud_autorizacion_schema.dump(aviso[3])
            solicitud_data['Cliente01'] = cliente_schema.dump(aviso[4])
            solicitud_data['Cliente01']['Sector'] = sector_schema.dump(aviso[6])  # sector_cliente01_alias
            solicitud_data['Cliente02'] = cliente_schema.dump(aviso[5])
            solicitud_data['Cliente02']['Sector'] = sector_schema.dump(aviso[7])  # sector_cliente02_alias

            solicitud_data['Agrimensor'] = agrimensor_schema.dump(aviso[8])
            solicitud_data['Agrimensor']['Sector'] = sector_schema.dump(aviso[9])  # sector_agrimensor_alias

            solicitud_data['Notario'] = notario_schema.dump(aviso[10])
            solicitud_data['Notario']['Sector'] = sector_schema.dump(aviso[11])  # sector_notario_alias
            solicitud_data['Sector'] = sector_schema.dump(aviso[12])
            solicitud_data['DerechoSustentado'] = derecho_sustentado_schema.dump(aviso[14])
            aviso_colindantes_data['SolicitudAutorizacion'] = solicitud_data
            aviso_colindantes_data['DepartamentoOficina'] = departamento_oficina_schema.dump(aviso[13])

            return jsonify(aviso_colindantes_data)
        else:
            return jsonify({"message": "Aviso Colindantes no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/avisocolindantes', methods=['POST'])
def add_avisocolindantes():
    try:
        data = request.get_json()
        nuevo_aviso = AvisoColindantes(
            IdAvisoPeriodico=data['IdAvisoPeriodico'],
            Estatus=data.get('Estatus', 1),
            Enlace=data.get('Enlace'),
            FechaVencimiento=data.get('FechaVencimiento'),
            #checkMensura=data.get('checkMensura', False),
            #checkPeriodico=data.get('checkPeriodico', False),
            #checkColindante=data.get('checkColindante', False)
        )
        db.session.add(nuevo_aviso)
        db.session.commit()
        return aviso_colindantes_schema.jsonify(nuevo_aviso), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/avisocolindantes/<int:id>', methods=['PUT'])
def update_avisocolindantes(id):
    try:
        data = request.get_json()
        aviso = AvisoColindantes.query.get_or_404(id)
        
        aviso.IdAvisoPeriodico = data.get('IdAvisoPeriodico', aviso.IdAvisoPeriodico)
        aviso.Estatus = data.get('Estatus', aviso.Estatus)
        aviso.Enlace=data.get('Enlace',aviso.Enlace)
        aviso.FechaVencimiento = data.get('FechaVencimiento',aviso.FechaVencimiento)
        #aviso.checkMensura = data.get('checkMensura', aviso.checkMensura)
        #aviso.checkPeriodico = data.get('checkPeriodico', aviso.checkPeriodico)
        #aviso.checkColindante = data.get('checkColindante', aviso.checkColindante)
        db.session.commit()
        return aviso_colindantes_schema.jsonify(aviso)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/avisocolindantes_enlace/<int:id>', methods=['PUT'])
def update_avisocolindantes_enlace(id):
    try:
        data = request.get_json()
        aviso = AvisoColindantes.query.get_or_404(id)
        
        aviso.Enlace=data.get('Enlace',aviso.Enlace)

        db.session.commit()
        return aviso_colindantes_schema.jsonify(aviso)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@app.route('/avisocolindantes_estatus/<int:id>', methods=['PUT'])
def update_avisocolindantes_estatus(id):
    try:
        data = request.get_json()
        aviso = AvisoColindantes.query.get_or_404(id)
        
        aviso.Estatus = data.get('Estatus', aviso.Estatus)

        db.session.commit()
        return aviso_colindantes_schema.jsonify(aviso)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/avisocolindantes/<int:id>', methods=['DELETE'])
def delete_avisocolindantes(id):
    try:
        aviso = db.session.query(AvisoColindantes).filter_by(IdAvisoColindantes=id).first()
        if aviso:
            aviso.Estatus = 0  # Actualización del estatus a 0 en lugar de eliminación física
            db.session.commit()
            return aviso_colindantes_schema.jsonify(aviso)
        return jsonify({"error": "Aviso de colindantes no encontrado"}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400



@app.route('/aviso_colindante_enlace_prorroga/<int:id>', methods=['PUT'])
def update_aviso_colindante_enlace_prorroga(id):
    try:
        #informe_tecnico = db.session.query(InformeTecnico).filter_by(IdInformeTecnico=id).first()
        aviso = db.session.query(AvisoColindantes).filter_by(IdAvisoColindantes=id).first()
        if aviso:
            data = request.get_json()
            aviso.EnlaceProrroga=data['EnlaceProrroga']
            db.session.commit()
            return aviso_colindantes_schema.jsonify(aviso), 200
        
        return jsonify({"error": "Aviso Colindantes no encontrado"}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


@app.route('/aviscolindantes_check_mensura/<int:id>', methods=['PUT'])
def update_check_mensura(id):
    data = request.get_json()
    record = AvisoColindantes.query.get(id)
    if 'value' in data:
        setattr(record, 'checkMensura', data['value'])
        db.session.commit()
        return jsonify({ 'success': True, 'checkMensura': record.checkMensura }), 200
    return jsonify({ 'error': 'Invalid data' }), 400

@app.route('/aviscolindantes_check_periodico/<int:id>', methods=['PUT'])
def update_check_periodico(id):
    data = request.get_json()
    record = AvisoColindantes.query.get(id)
    if 'value' in data:
        setattr(record, 'checkPeriodico', data['value'])
        db.session.commit()
        return jsonify({ 'success': True, 'checkPeriodico': record.checkPeriodico }), 200
    return jsonify({ 'error': 'Invalid data' }), 400

@app.route('/aviscolindantes_check_colindantes/<int:id>', methods=['PUT'])
def update_check_colindantes(id):
    data = request.get_json()
    record = AvisoColindantes.query.get(id)
    if 'value' in data:
        setattr(record, 'checkColindantes', data['value'])
        db.session.commit()
        return jsonify({ 'success': True, 'checkColindantes': record.checkColindantes }), 200
    return jsonify({ 'error': 'Invalid data' }), 400


# TERCERA ETAPA
# Rutas para Carta de conformidad
@app.route('/conformidades', methods=['GET'])
def get_conformidades():
    try:
        # Crear alias para las tablas involucradas en las uniones
        cliente01_alias = aliased(Cliente)
        cliente02_alias = aliased(Cliente)

        # Consulta con INNER JOIN de las tablas relacionadas
        cartas_conformidad = db.session.query(
            CartaConformidad,
            AvisoColindantes,
            AvisoPeriodico,
            AvisoMensura,
            SolicitudAutorizacion,
            cliente01_alias,
            cliente02_alias,
            Agrimensor,
            Notario,
            Sector,
            DepartamentoOficina
        ).join(
            AvisoColindantes, CartaConformidad.IdAvisoColindantes == AvisoColindantes.IdAvisoColindantes
        ).join(
            AvisoPeriodico, AvisoColindantes.IdAvisoPeriodico == AvisoPeriodico.IdAvisoPeriodico
        ).join(
            AvisoMensura, AvisoPeriodico.IdAvisoMensura == AvisoMensura.IdAvisoMensura
        ).join(
            SolicitudAutorizacion, AvisoMensura.IdSolicitud == SolicitudAutorizacion.IdSolicitud
        ).join(
            cliente01_alias, SolicitudAutorizacion.IdCliente01 == cliente01_alias.IdCliente
        ).join(
            cliente02_alias, SolicitudAutorizacion.IdCliente02 == cliente02_alias.IdCliente
        ).join(
            Agrimensor, SolicitudAutorizacion.IdAgrimensor == Agrimensor.IdAgrimensor
        ).join(
            Notario, SolicitudAutorizacion.IdNotario == Notario.IdNotario
        ).join(
            Sector, SolicitudAutorizacion.IdSector == Sector.IdSector
        ).join(
            DepartamentoOficina, AvisoMensura.IdDepartamentoOficina == DepartamentoOficina.IdDepartamentoOficina
        ).all()

        result = []
        for carta, aviso_colindantes, aviso_periodico, aviso_mensura, solicitud, cliente1, cliente2, agrimensor, notario, sector, departamento in cartas_conformidad:
            carta_data = carta_conformidad_schema.dump(carta)
            aviso_colindantes_data = aviso_colindantes_schema.dump(aviso_colindantes)
            aviso_colindantes_data['AvisoPeriodico'] = aviso_periodico_schema.dump(aviso_periodico)
            aviso_colindantes_data['AvisoMensura'] = avisomensura_schema.dump(aviso_mensura)
            solicitud_data = solicitud_autorizacion_schema.dump(solicitud)
            solicitud_data['Cliente01'] = cliente_schema.dump(cliente1)
            solicitud_data['Cliente02'] = cliente_schema.dump(cliente2)
            solicitud_data['Agrimensor'] = agrimensor_schema.dump(agrimensor)
            solicitud_data['Notario'] = notario_schema.dump(notario)
            solicitud_data['Sector'] = sector_schema.dump(sector)
            aviso_colindantes_data['SolicitudAutorizacion'] = solicitud_data
            aviso_colindantes_data['DepartamentoOficina'] = departamento_oficina_schema.dump(departamento)
            carta_data['AvisoColindantes'] = aviso_colindantes_data
            result.append(carta_data)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/conformidad/<int:id>', methods=['GET'])
def get_conformidad(id):
    try:
        # Crear alias para las tablas involucradas en las uniones
        cliente01_alias = aliased(Cliente)
        cliente02_alias = aliased(Cliente)

        # Consulta con INNER JOIN de las tablas relacionadas y filtro por ID
        carta_conformidad = db.session.query(
            CartaConformidad,
            AvisoColindantes,
            AvisoPeriodico,
            AvisoMensura,
            SolicitudAutorizacion,
            cliente01_alias,
            cliente02_alias,
            Agrimensor,
            Notario,
            Sector,
            DepartamentoOficina
        ).join(
            AvisoColindantes, CartaConformidad.IdAvisoColindantes == AvisoColindantes.IdAvisoColindantes
        ).join(
            AvisoPeriodico, AvisoColindantes.IdAvisoPeriodico == AvisoPeriodico.IdAvisoPeriodico
        ).join(
            AvisoMensura, AvisoPeriodico.IdAvisoMensura == AvisoMensura.IdAvisoMensura
        ).join(
            SolicitudAutorizacion, AvisoMensura.IdSolicitud == SolicitudAutorizacion.IdSolicitud
        ).join(
            cliente01_alias, SolicitudAutorizacion.IdCliente01 == cliente01_alias.IdCliente
        ).join(
            cliente02_alias, SolicitudAutorizacion.IdCliente02 == cliente02_alias.IdCliente
        ).join(
            Agrimensor, SolicitudAutorizacion.IdAgrimensor == Agrimensor.IdAgrimensor
        ).join(
            Notario, SolicitudAutorizacion.IdNotario == Notario.IdNotario
        ).join(
            Sector, SolicitudAutorizacion.IdSector == Sector.IdSector
        ).join(
            DepartamentoOficina, AvisoMensura.IdDepartamentoOficina == DepartamentoOficina.IdDepartamentoOficina
        ).filter(CartaConformidad.IdConformidad == id).first()

        if carta_conformidad:
            carta_data = carta_conformidad_schema.dump(carta_conformidad[0])
            aviso_colindantes_data = aviso_colindantes_schema.dump(carta_conformidad[1])
            aviso_colindantes_data['AvisoPeriodico'] = aviso_periodico_schema.dump(carta_conformidad[2])
            aviso_colindantes_data['AvisoMensura'] = avisomensura_schema.dump(carta_conformidad[3])
            solicitud_data = solicitud_autorizacion_schema.dump(carta_conformidad[4])
            solicitud_data['Cliente01'] = cliente_schema.dump(carta_conformidad[5])
            solicitud_data['Cliente02'] = cliente_schema.dump(carta_conformidad[6])
            solicitud_data['Agrimensor'] = agrimensor_schema.dump(carta_conformidad[7])
            solicitud_data['Notario'] = notario_schema.dump(carta_conformidad[8])
            solicitud_data['Sector'] = sector_schema.dump(carta_conformidad[9])
            aviso_colindantes_data['SolicitudAutorizacion'] = solicitud_data
            aviso_colindantes_data['DepartamentoOficina'] = departamento_oficina_schema.dump(carta_conformidad[10])
            carta_data['AvisoColindantes'] = aviso_colindantes_data

            return jsonify(carta_data)
        else:
            return jsonify({"error": "Carta de Conformidad no encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/conformidad', methods=['POST'])
def add_conformidad():
    try:
        data = request.get_json()
        nueva_carta = CartaConformidad(
            IdSolicitud=data['IdSolicitud'],
            IdAvisoColindantes=data['IdAvisoColindantes'],
            Estatus=data.get('Estatus', 1),
            Enlace=data.get('Enlace')
        )
        
        db.session.add(nueva_carta)
        db.session.commit()
        return carta_conformidad_schema.jsonify(nueva_carta), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/conformidad/<int:id>', methods=['PUT'])
def update_conformidad(id):
    try:
        carta_conformidad = db.session.query(CartaConformidad).filter_by(IdConformidad=id).first()
        if carta_conformidad:
            data = request.get_json()
            carta_conformidad.IdSolicitud = data['IdSolicitud']
            carta_conformidad.IdAvisoColindantes = data['IdAvisoColindantes']
            carta_conformidad.Enlace=data['Enlace']
            db.session.commit()
            return carta_conformidad_schema.jsonify(carta_conformidad)
        
        return jsonify({"error": "Carta Conformidad no encontrada"}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@app.route('/conformidad_enlace/<int:id>', methods=['PUT'])
def update_conformidad_enlace(id):
    try:
        carta_conformidad = db.session.query(CartaConformidad).filter_by(IdConformidad=id).first()
        if carta_conformidad:
            data = request.get_json()
            carta_conformidad.Enlace=data['Enlace']
            db.session.commit()
            return carta_conformidad_schema.jsonify(carta_conformidad)
        
        return jsonify({"error": "Carta Conformidad no encontrada"}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    
@app.route('/conformidad_estatus/<int:id>', methods=['PUT'])
def update_conformidad_estatus(id):
    try:
        carta_conformidad = db.session.query(CartaConformidad).filter_by(IdConformidad=id).first()
        if carta_conformidad:
            data = request.get_json()
            carta_conformidad.Estatus=data.get('Estatus', carta_conformidad.Estatus)
            db.session.commit()
            return carta_conformidad_schema.jsonify(carta_conformidad)
        
        return jsonify({"error": "Carta Conformidad no encontrada"}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    
@app.route('/conformidad/<int:id>', methods=['DELETE'])
def delete_conformidad(id):
    try:
        carta_conformidad = db.session.query(CartaConformidad).filter_by(IdConformidad=id).first()
        if carta_conformidad:
            carta_conformidad.Estatus = 0
            db.session.commit()
            return carta_conformidad_schema.jsonify(carta_conformidad)
        
        return jsonify({"error": "Carta Conformidad no encontrada"}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# Rutas para Declaracion de posesion
@app.route('/declaraciones_posesion', methods=['GET'])
def get_declaraciones_posesion():
    try:
        # Crear alias para las tablas relacionadas con CartaConformidad
        cliente01_alias = aliased(Cliente)
        cliente02_alias = aliased(Cliente)

        # Consulta con INNER JOIN de las tablas relacionadas
        declaraciones_posesion = db.session.query(
            DeclaracionPosesion,
            CartaConformidad,
            DerechoSustentado,
            AvisoColindantes,
            AvisoPeriodico,
            AvisoMensura,
            SolicitudAutorizacion,
            cliente01_alias,
            cliente02_alias,
            Agrimensor,
            Notario,
            Sector,
            DepartamentoOficina
        ).join(
            CartaConformidad, DeclaracionPosesion.IdConformidad == CartaConformidad.IdConformidad
        ).join(
            DerechoSustentado, DeclaracionPosesion.IdDerechoSustentado == DerechoSustentado.IdDerechoSustentado
        ).join(
            AvisoColindantes, CartaConformidad.IdAvisoColindantes == AvisoColindantes.IdAvisoColindantes
        ).join(
            AvisoPeriodico, AvisoColindantes.IdAvisoPeriodico == AvisoPeriodico.IdAvisoPeriodico
        ).join(
            AvisoMensura, AvisoPeriodico.IdAvisoMensura == AvisoMensura.IdAvisoMensura
        ).join(
            SolicitudAutorizacion, AvisoMensura.IdSolicitud == SolicitudAutorizacion.IdSolicitud
        ).join(
            cliente01_alias, SolicitudAutorizacion.IdCliente01 == cliente01_alias.IdCliente
        ).join(
            cliente02_alias, SolicitudAutorizacion.IdCliente02 == cliente02_alias.IdCliente
        ).join(
            Agrimensor, SolicitudAutorizacion.IdAgrimensor == Agrimensor.IdAgrimensor
        ).join(
            Notario, SolicitudAutorizacion.IdNotario == Notario.IdNotario
        ).join(
            Sector, SolicitudAutorizacion.IdSector == Sector.IdSector
        ).join(
            DepartamentoOficina, AvisoMensura.IdDepartamentoOficina == DepartamentoOficina.IdDepartamentoOficina
        ).filter(
            DeclaracionPosesion.Estatus == 1
        ).all()

        result = []
        for declaracion, conformidad, derecho, aviso_colindantes, aviso_periodico, aviso_mensura, solicitud, cliente1, cliente2, agrimensor, notario, sector, departamento in declaraciones_posesion:
            declaracion_data = declaracion_posesion_schema.dump(declaracion)
            conformidad_data = carta_conformidad_schema.dump(conformidad)
            aviso_colindantes_data = aviso_colindantes_schema.dump(aviso_colindantes)
            aviso_colindantes_data['AvisoPeriodico'] = aviso_periodico_schema.dump(aviso_periodico)
            aviso_colindantes_data['AvisoMensura'] = avisomensura_schema.dump(aviso_mensura)
            solicitud_data = solicitud_autorizacion_schema.dump(solicitud)
            solicitud_data['Cliente01'] = cliente_schema.dump(cliente1)
            solicitud_data['Cliente02'] = cliente_schema.dump(cliente2)
            solicitud_data['Agrimensor'] = agrimensor_schema.dump(agrimensor)
            solicitud_data['Notario'] = notario_schema.dump(notario)
            solicitud_data['Sector'] = sector_schema.dump(sector)
            aviso_colindantes_data['SolicitudAutorizacion'] = solicitud_data
            aviso_colindantes_data['DepartamentoOficina'] = departamento_oficina_schema.dump(departamento)
            conformidad_data['AvisoColindantes'] = aviso_colindantes_data
            declaracion_data['CartaConformidad'] = conformidad_data
            declaracion_data['DerechoSustentado'] = derecho_sustentado_schema.dump(derecho)
            result.append(declaracion_data)

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/declaracion_posesion/<int:id>', methods=['GET'])
def get_declaracion_posesion(id):
    try:
        # Crear alias para las tablas relacionadas con CartaConformidad
        cliente01_alias = aliased(Cliente)
        cliente02_alias = aliased(Cliente)

        # Consulta con INNER JOIN de las tablas relacionadas y filtro por ID
        declaracion_posesion = db.session.query(
            DeclaracionPosesion,
            CartaConformidad,
            DerechoSustentado,
            AvisoColindantes,
            AvisoPeriodico,
            AvisoMensura,
            SolicitudAutorizacion,
            cliente01_alias,
            cliente02_alias,
            Agrimensor,
            Notario,
            Sector,
            DepartamentoOficina
        ).join(
            CartaConformidad, DeclaracionPosesion.IdConformidad == CartaConformidad.IdConformidad
        ).join(
            DerechoSustentado, DeclaracionPosesion.IdDerechoSustentado == DerechoSustentado.IdDerechoSustentado
        ).join(
            AvisoColindantes, CartaConformidad.IdAvisoColindantes == AvisoColindantes.IdAvisoColindantes
        ).join(
            AvisoPeriodico, AvisoColindantes.IdAvisoPeriodico == AvisoPeriodico.IdAvisoPeriodico
        ).join(
            AvisoMensura, AvisoPeriodico.IdAvisoMensura == AvisoMensura.IdAvisoMensura
        ).join(
            SolicitudAutorizacion, AvisoMensura.IdSolicitud == SolicitudAutorizacion.IdSolicitud
        ).join(
            cliente01_alias, SolicitudAutorizacion.IdCliente01 == cliente01_alias.IdCliente
        ).join(
            cliente02_alias, SolicitudAutorizacion.IdCliente02 == cliente02_alias.IdCliente
        ).join(
            Agrimensor, SolicitudAutorizacion.IdAgrimensor == Agrimensor.IdAgrimensor
        ).join(
            Notario, SolicitudAutorizacion.IdNotario == Notario.IdNotario
        ).join(
            Sector, SolicitudAutorizacion.IdSector == Sector.IdSector
        ).join(
            DepartamentoOficina, AvisoMensura.IdDepartamentoOficina == DepartamentoOficina.IdDepartamentoOficina
        ).filter(
            DeclaracionPosesion.IdDeclaracionPosesion == id,
            DeclaracionPosesion.Estatus == 1
        ).first()

        if declaracion_posesion:
            declaracion_data = declaracion_posesion_schema.dump(declaracion_posesion[0])
            conformidad_data = carta_conformidad_schema.dump(declaracion_posesion[1])
            aviso_colindantes_data = aviso_colindantes_schema.dump(declaracion_posesion[3])
            aviso_colindantes_data['AvisoPeriodico'] = aviso_periodico_schema.dump(declaracion_posesion[4])
            aviso_colindantes_data['AvisoMensura'] = avisomensura_schema.dump(declaracion_posesion[5])
            solicitud_data = solicitud_autorizacion_schema.dump(declaracion_posesion[6])
            solicitud_data['Cliente01'] = cliente_schema.dump(declaracion_posesion[7])
            solicitud_data['Cliente02'] = cliente_schema.dump(declaracion_posesion[8])
            solicitud_data['Agrimensor'] = agrimensor_schema.dump(declaracion_posesion[9])
            solicitud_data['Notario'] = notario_schema.dump(declaracion_posesion[10])
            solicitud_data['Sector'] = sector_schema.dump(declaracion_posesion[11])
            aviso_colindantes_data['SolicitudAutorizacion'] = solicitud_data
            aviso_colindantes_data['DepartamentoOficina'] = departamento_oficina_schema.dump(declaracion_posesion[12])
            conformidad_data['AvisoColindantes'] = aviso_colindantes_data
            declaracion_data['CartaConformidad'] = conformidad_data
            declaracion_data['DerechoSustentado'] = derecho_sustentado_schema.dump(declaracion_posesion[2])

            return jsonify(declaracion_data), 200
        else:
            return jsonify({"error": "Declaración de Posesión no encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/declaracion_posesion', methods=['POST'])
def add_declaracion_posesion():
    try:
        data = request.get_json()
        nueva_declaracion = DeclaracionPosesion(
            IdConformidad=data['IdConformidad'],
            IdDerechoSustentado=data['IdDerechoSustentado'],
            FechaDocumentoDerecho=data.get('FechaDocumentoDerecho'),
            Estatus=data.get('Estatus', 1),
            Enlace=data.get('Enlace')
        )
        
        db.session.add(nueva_declaracion)
        db.session.commit()
        return declaracion_posesion_schema.jsonify(nueva_declaracion), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/declaracion_posesion/<int:id>', methods=['PUT'])
def update_declaracion_posesion(id):
    try:
        declaracion_posesion = db.session.query(DeclaracionPosesion).filter_by(IdDeclaracionPosesion=id).first()
        if declaracion_posesion:
            data = request.get_json()
            declaracion_posesion.IdConformidad = data['IdConformidad']
            declaracion_posesion.IdDerechoSustentado = data['IdDerechoSustentado']
            declaracion_posesion.FechaDocumentoDerecho = data.get('FechaDocumentoDerecho')
            declaracion_posesion.Enlace=data.get('Enlace')
            db.session.commit()
            return declaracion_posesion_schema.jsonify(declaracion_posesion), 200
        
        return jsonify({"error": "Declaración de Posesión no encontrada"}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@app.route('/declaracion_posesion_enlace/<int:id>', methods=['PUT'])
def update_declaracion_posesion_enlace(id):
    try:
        declaracion_posesion = db.session.query(DeclaracionPosesion).filter_by(IdDeclaracionPosesion=id).first()
        if declaracion_posesion:
            data = request.get_json()
            declaracion_posesion.Enlace=data.get('Enlace')
            db.session.commit()
            return declaracion_posesion_schema.jsonify(declaracion_posesion), 200
        
        return jsonify({"error": "Declaración de Posesión no encontrada"}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    
@app.route('/declaracion_posesion_estatus/<int:id>', methods=['PUT'])
def update_declaracion_posesion_estatus(id):
    try:
        declaracion_posesion = db.session.query(DeclaracionPosesion).filter_by(IdDeclaracionPosesion=id).first()
        if declaracion_posesion:
            data = request.get_json()
            declaracion_posesion.Enlace=data.get('Estatus',declaracion_posesion.Estatus)
            db.session.commit()
            return declaracion_posesion_schema.jsonify(declaracion_posesion), 200
        
        return jsonify({"error": "Declaración de Posesión no encontrada"}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    
@app.route('/declaracion_posesion/<int:id>', methods=['DELETE'])
def delete_declaracion_posesion(id):
    try:
        declaracion_posesion = db.session.query(DeclaracionPosesion).filter_by(IdDeclaracionPosesion=id).first()
        if declaracion_posesion:
            declaracion_posesion.Estatus = 0
            db.session.commit()
            return declaracion_posesion_schema.jsonify(declaracion_posesion), 200
        
        return jsonify({"error": "Declaración de Posesión no encontrada"}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# Rutas para Informe Tecnico
@app.route('/informes_tecnicos', methods=['GET'])
def get_informes_tecnicos():
    try:
        # Crear alias para las tablas relacionadas con CartaConformidad
        cliente01_alias = aliased(Cliente)
        cliente02_alias = aliased(Cliente)
        sector_cliente01_alias = aliased(Sector)
        sector_cliente02_alias = aliased(Sector)
        sector_agrimensor_alias = aliased(Sector)
        sector_notario_alias = aliased(Sector)

        # Consulta con INNER JOIN de las tablas relacionadas
        informes_tecnicos = db.session.query(
            InformeTecnico,
            DeclaracionPosesion,
            AreaDiferencia,
            CartaConformidad,
            DerechoSustentado,
            AvisoColindantes,
            AvisoPeriodico,
            AvisoMensura,
            SolicitudAutorizacion,
            cliente01_alias,
            cliente02_alias,
            sector_cliente01_alias,
            sector_cliente02_alias,
            Agrimensor,
            sector_agrimensor_alias,
            Notario,
            sector_notario_alias,
            Sector,
            DepartamentoOficina
        ).join(
            DeclaracionPosesion, InformeTecnico.IdDeclaracionPosesion == DeclaracionPosesion.IdDeclaracionPosesion
        ).join(
            AreaDiferencia, InformeTecnico.IdAreaDiferencia == AreaDiferencia.IdAreaDiferencia
        ).join(
            CartaConformidad, DeclaracionPosesion.IdConformidad == CartaConformidad.IdConformidad
        ).join(
            DerechoSustentado, DeclaracionPosesion.IdDerechoSustentado == DerechoSustentado.IdDerechoSustentado
        ).join(
            AvisoColindantes, CartaConformidad.IdAvisoColindantes == AvisoColindantes.IdAvisoColindantes
        ).join(
            AvisoPeriodico, AvisoColindantes.IdAvisoPeriodico == AvisoPeriodico.IdAvisoPeriodico
        ).join(
            AvisoMensura, AvisoPeriodico.IdAvisoMensura == AvisoMensura.IdAvisoMensura
        ).join(
            SolicitudAutorizacion, AvisoMensura.IdSolicitud == SolicitudAutorizacion.IdSolicitud
        ).join(
            cliente01_alias, SolicitudAutorizacion.IdCliente01 == cliente01_alias.IdCliente
        ).join(
            sector_cliente01_alias, cliente01_alias.IdSector == sector_cliente01_alias.IdSector
        ).join(
            cliente02_alias, SolicitudAutorizacion.IdCliente02 == cliente02_alias.IdCliente
        ).join(
            sector_cliente02_alias, cliente02_alias.IdSector == sector_cliente02_alias.IdSector
        ).join(
            Agrimensor, SolicitudAutorizacion.IdAgrimensor == Agrimensor.IdAgrimensor
        ).join(
            sector_agrimensor_alias, Agrimensor.IdSector == sector_agrimensor_alias.IdSector
        ).join(
            Notario, SolicitudAutorizacion.IdNotario == Notario.IdNotario
        ).join(
            sector_notario_alias, Notario.IdSector == sector_notario_alias.IdSector
        ).join(
            Sector, SolicitudAutorizacion.IdSector == Sector.IdSector
        ).join(
            DepartamentoOficina, AvisoMensura.IdDepartamentoOficina == DepartamentoOficina.IdDepartamentoOficina
        ).filter(
            InformeTecnico.Estatus == 1
        ).order_by(
            InformeTecnico.IdInformeTecnico.desc()
        ).all()

        result = []
        for informe, declaracion, area, conformidad, derecho, aviso_colindantes, aviso_periodico, aviso_mensura, solicitud, cliente1, sector_cliente1, cliente2, sector_cliente2, agrimensor, sector_agrimensor, notario, sector_notario, sector, departamento in informes_tecnicos:
            informe_data = informe_tecnico_schema.dump(informe)
            declaracion_data = declaracion_posesion_schema.dump(declaracion)
            conformidad_data = carta_conformidad_schema.dump(conformidad)
            aviso_colindantes_data = aviso_colindantes_schema.dump(aviso_colindantes)
            aviso_colindantes_data['AvisoPeriodico'] = aviso_periodico_schema.dump(aviso_periodico)
            aviso_colindantes_data['AvisoMensura'] = avisomensura_schema.dump(aviso_mensura)

            solicitud_data = solicitud_autorizacion_schema.dump(solicitud)
            solicitud_data['Cliente01'] = cliente_schema.dump(cliente1)
            solicitud_data['Cliente01']['Sector'] = sector_schema.dump(sector_cliente1)
            solicitud_data['Cliente02'] = cliente_schema.dump(cliente2)
            solicitud_data['Cliente02']['Sector'] = sector_schema.dump(sector_cliente2)
            solicitud_data['Agrimensor'] = agrimensor_schema.dump(agrimensor)
            solicitud_data['Agrimensor']['Sector'] = sector_schema.dump(sector_agrimensor)
            solicitud_data['Notario'] = notario_schema.dump(notario)
            solicitud_data['Notario']['Sector'] = sector_schema.dump(sector_notario)
            solicitud_data['Sector'] = sector_schema.dump(sector)

            aviso_colindantes_data['SolicitudAutorizacion'] = solicitud_data
            aviso_colindantes_data['DepartamentoOficina'] = departamento_oficina_schema.dump(departamento)

            conformidad_data['AvisoColindantes'] = aviso_colindantes_data

            declaracion_data['CartaConformidad'] = conformidad_data
            declaracion_data['DerechoSustentado'] = derecho_sustentado_schema.dump(derecho)
            informe_data['DeclaracionPosesion'] = declaracion_data
            informe_data['AreaDiferencia'] = area_diferencia_schema.dump(area)

            result.append(informe_data)

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/informe_tecnico/<int:id>', methods=['GET'])
def get_informe_tecnico(id):
    try:
        # Crear alias para las tablas relacionadas con CartaConformidad
        cliente01_alias = aliased(Cliente)
        cliente02_alias = aliased(Cliente)
        sector_cliente01_alias = aliased(Sector)
        sector_cliente02_alias = aliased(Sector)
        sector_agrimensor_alias = aliased(Sector)
        sector_notario_alias = aliased(Sector)

        # Consulta con INNER JOIN de las tablas relacionadas y filtro por ID
        informe_tecnico = db.session.query(
            InformeTecnico,
            DeclaracionPosesion,
            AreaDiferencia,
            CartaConformidad,
            DerechoSustentado,
            AvisoColindantes,
            AvisoPeriodico,
            AvisoMensura,
            SolicitudAutorizacion,
            cliente01_alias,
            cliente02_alias,
            sector_cliente01_alias,
            sector_cliente02_alias,
            Agrimensor,
            sector_agrimensor_alias,
            Notario,
            sector_notario_alias,
            Sector,
            DepartamentoOficina
        ).join(
            DeclaracionPosesion, InformeTecnico.IdDeclaracionPosesion == DeclaracionPosesion.IdDeclaracionPosesion
        ).join(
            AreaDiferencia, InformeTecnico.IdAreaDiferencia == AreaDiferencia.IdAreaDiferencia
        ).join(
            CartaConformidad, DeclaracionPosesion.IdConformidad == CartaConformidad.IdConformidad
        ).join(
            DerechoSustentado, DeclaracionPosesion.IdDerechoSustentado == DerechoSustentado.IdDerechoSustentado
        ).join(
            AvisoColindantes, CartaConformidad.IdAvisoColindantes == AvisoColindantes.IdAvisoColindantes
        ).join(
            AvisoPeriodico, AvisoColindantes.IdAvisoPeriodico == AvisoPeriodico.IdAvisoPeriodico
        ).join(
            AvisoMensura, AvisoPeriodico.IdAvisoMensura == AvisoMensura.IdAvisoMensura
        ).join(
            SolicitudAutorizacion, AvisoMensura.IdSolicitud == SolicitudAutorizacion.IdSolicitud
        ).join(
            cliente01_alias, SolicitudAutorizacion.IdCliente01 == cliente01_alias.IdCliente
        ).join(
            sector_cliente01_alias, cliente01_alias.IdSector == sector_cliente01_alias.IdSector
        ).join(
            cliente02_alias, SolicitudAutorizacion.IdCliente02 == cliente02_alias.IdCliente
        ).join(
            sector_cliente02_alias, cliente02_alias.IdSector == sector_cliente02_alias.IdSector
        ).join(
            Agrimensor, SolicitudAutorizacion.IdAgrimensor == Agrimensor.IdAgrimensor
        ).join(
            sector_agrimensor_alias, Agrimensor.IdSector == sector_agrimensor_alias.IdSector
        ).join(
            Notario, SolicitudAutorizacion.IdNotario == Notario.IdNotario
        ).join(
            sector_notario_alias, Notario.IdSector == sector_notario_alias.IdSector
        ).join(
            Sector, SolicitudAutorizacion.IdSector == Sector.IdSector
        ).join(
            DepartamentoOficina, AvisoMensura.IdDepartamentoOficina == DepartamentoOficina.IdDepartamentoOficina
        ).filter(
            InformeTecnico.IdInformeTecnico == id,
            InformeTecnico.Estatus == 1
        ).order_by(
            InformeTecnico.IdInformeTecnico
        ).first()

        if informe_tecnico:
            informe_data = informe_tecnico_schema.dump(informe_tecnico[0])
            declaracion_data = declaracion_posesion_schema.dump(informe_tecnico[1])
            conformidad_data = carta_conformidad_schema.dump(informe_tecnico[3])
            aviso_colindantes_data = aviso_colindantes_schema.dump(informe_tecnico[5])
            aviso_colindantes_data['AvisoPeriodico'] = aviso_periodico_schema.dump(informe_tecnico[6])
            aviso_colindantes_data['AvisoMensura'] = avisomensura_schema.dump(informe_tecnico[7])
            solicitud_data = solicitud_autorizacion_schema.dump(informe_tecnico[8])

            # Agregar datos de cliente y sus sectores
            solicitud_data['Cliente01'] = cliente_schema.dump(informe_tecnico[9])
            solicitud_data['Cliente01']['Sector'] = sector_schema.dump(informe_tecnico[11])  # sector_cliente01_alias

            solicitud_data['Cliente02'] = cliente_schema.dump(informe_tecnico[10])
            solicitud_data['Cliente02']['Sector'] = sector_schema.dump(informe_tecnico[12])  # sector_cliente02_alias

            # Agregar datos del agrimensor y su sector
            solicitud_data['Agrimensor'] = agrimensor_schema.dump(informe_tecnico[13])
            solicitud_data['Agrimensor']['Sector'] = sector_schema.dump(informe_tecnico[14])  # sector_agrimensor_alias

            # Agregar datos del notario y su sector
            solicitud_data['Notario'] = notario_schema.dump(informe_tecnico[15])
            solicitud_data['Notario']['Sector'] = sector_schema.dump(informe_tecnico[16])  # sector_notario_alias

            solicitud_data['Sector'] = sector_schema.dump(informe_tecnico[17])  # Sector general

            aviso_colindantes_data['SolicitudAutorizacion'] = solicitud_data
            aviso_colindantes_data['DepartamentoOficina'] = departamento_oficina_schema.dump(informe_tecnico[18])
            conformidad_data['AvisoColindantes'] = aviso_colindantes_data
            declaracion_data['CartaConformidad'] = conformidad_data
            declaracion_data['DerechoSustentado'] = derecho_sustentado_schema.dump(informe_tecnico[4])
            informe_data['DeclaracionPosesion'] = declaracion_data
            informe_data['AreaDiferencia'] = area_diferencia_schema.dump(informe_tecnico[2])

            return jsonify(informe_data), 200

        return jsonify({"error": "Informe Técnico no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/informe_tecnico', methods=['POST'])
def add_informe_tecnico():
    try:
        data = request.get_json()
        nuevo_informe = InformeTecnico(
            IdDeclaracionPosesion=data['IdDeclaracionPosesion'],
            FechaHoraInicioMensura=data.get('FechaHoraInicioMensura'),
            HoraFinMesura=data.get('HoraFinMesura'),
            FechaDocumentoDerecho=data.get('FechaDocumentoDerecho'),
            IdAreaDiferencia=data['IdAreaDiferencia'],
            AreaTotal=data.get('AreaTotal'),
            AreaDiferenciada=data.get('AreaDiferenciada'),
            DelimitacionNorte=data['DelimitacionNorte'],
            DelimitacionSur=data['DelimitacionSur'],
            DelimitacionOeste=data['DelimitacionOeste'],
            DelimitacionEste=data['DelimitacionEste'],
            Enlace=data['Enlace'],
            UbicacionInmueble=data['UbicacionInmueble'],
            DescripcionInmueble=data['DescripcionInmueble'],

            NombreEquipo=data['NombreEquipo'],
            ModeloEquipo=data['ModeloEquipo']
        )
        
        db.session.add(nuevo_informe)
        db.session.commit()
        return informe_tecnico_schema.jsonify(nuevo_informe), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/informe_tecnico/<int:id>', methods=['PUT'])
def update_informe_tecnico(id):
    try:
        informe_tecnico = db.session.query(InformeTecnico).filter_by(IdInformeTecnico=id).first()
        if informe_tecnico:
            data = request.get_json()
            informe_tecnico.IdDeclaracionPosesion = data['IdDeclaracionPosesion']
            informe_tecnico.FechaHoraInicioMensura = data.get('FechaHoraInicioMensura')
            informe_tecnico.HoraFinMesura = data.get('HoraFinMesura')
            informe_tecnico.FechaDocumentoDerecho = data.get('FechaDocumentoDerecho')
            informe_tecnico.IdAreaDiferencia = data['IdAreaDiferencia']
            informe_tecnico.AreaTotal = data.get('AreaTotal')
            informe_tecnico.AreaDiferenciada = data.get('AreaDiferenciada')
            informe_tecnico.DelimitacionNorte = data['DelimitacionNorte']
            informe_tecnico.DelimitacionSur = data['DelimitacionSur']
            informe_tecnico.DelimitacionOeste = data['DelimitacionOeste']
            informe_tecnico.DelimitacionEste = data['DelimitacionEste']
            informe_tecnico.Enlace=data['Enlace']
            #informe_tecnico.Enlace_Prorroga=data['Enlace_Prorroga']

            informe_tecnico.UbicacionInmueble = data['UbicacionInmueble']
            informe_tecnico.DescripcionInmueble = data['DescripcionInmueble']

            informe_tecnico.EnlaceActaHitos=data['EnlaceActaHitos']
            db.session.commit()
            return informe_tecnico_schema.jsonify(informe_tecnico), 200
        
        return jsonify({"error": "Informe Técnico no encontrado"}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@app.route('/informe_tecnico_enlace/<int:id>', methods=['PUT'])
def update_informe_tecnico_enlace(id):
    try:
        informe_tecnico = db.session.query(InformeTecnico).filter_by(IdInformeTecnico=id).first()
        if informe_tecnico:
            data = request.get_json()
            informe_tecnico.Enlace=data['Enlace']
            db.session.commit()
            return informe_tecnico_schema.jsonify(informe_tecnico), 200
        
        return jsonify({"error": "Informe Técnico no encontrado"}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

"""
@app.route('/informe_tecnico_enlace_prorroga/<int:id>', methods=['PUT'])
def update_informe_tecnico_enlace_prorroga(id):
    try:
        informe_tecnico = db.session.query(InformeTecnico).filter_by(IdInformeTecnico=id).first()
        if informe_tecnico:
            data = request.get_json()
            informe_tecnico.Enlace_Prorroga=data['Enlace_Prorroga']
            db.session.commit()
            return informe_tecnico_schema.jsonify(informe_tecnico), 200
        
        return jsonify({"error": "Informe Técnico no encontrado"}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
"""

@app.route('/informe_tecnico_enlace_acta/<int:id>', methods=['PUT'])
def update_informe_tecnico_enlace_acta(id):
    try:
        informe_tecnico = db.session.query(InformeTecnico).filter_by(IdInformeTecnico=id).first()
        if informe_tecnico:
            data = request.get_json()
            informe_tecnico.EnlaceActaHitos=data['EnlaceActaHitos']
            db.session.commit()
            return informe_tecnico_schema.jsonify(informe_tecnico), 200
        
        return jsonify({"error": "Informe Técnico no encontrado"}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


@app.route('/informe_tecnico_estatus/<int:id>', methods=['PUT'])
def update_informe_tecnico_estatus(id):
    try:
        informe_tecnico = db.session.query(InformeTecnico).filter_by(IdInformeTecnico=id).first()
        if informe_tecnico:
            data = request.get_json()
            informe_tecnico.Estatus=data['Estatus']
            db.session.commit()
            return informe_tecnico_schema.jsonify(informe_tecnico), 200
        
        return jsonify({"error": "Informe Técnico no encontrado"}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    
@app.route('/informe_tecnico/<int:id>', methods=['DELETE'])
def delete_informe_tecnico(id):
    try:
        informe_tecnico = db.session.query(InformeTecnico).filter_by(IdInformeTecnico=id).first()
        if informe_tecnico:
            informe_tecnico.Estatus = 0
            db.session.commit()
            return informe_tecnico_schema.jsonify(informe_tecnico), 200
        
        return jsonify({"error": "Informe Técnico no encontrado"}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400



#CHECKS INFORME TECNICO
@app.route('/informe_tecnico_check_carta/<int:id>', methods=['PUT'])
def update_check_carta(id):
    data = request.get_json()
    record = InformeTecnico.query.get(id)
    if 'value' in data:
        setattr(record, 'checkCarta', data['value'])
        db.session.commit()
        return jsonify({ 'success': True, 'checkCarta': record.checkCarta }), 200
    return jsonify({ 'error': 'Invalid data' }), 400


@app.route('/informe_tecnico_check_declaracion/<int:id>', methods=['PUT'])
def update_check_declaracion(id):
    data = request.get_json()
    record = InformeTecnico.query.get(id)
    if 'value' in data:
        setattr(record, 'checkDeclaracion', data['value'])
        db.session.commit()
        return jsonify({ 'success': True, 'checkDeclaracion': record.checkDeclaracion }), 200
    return jsonify({ 'error': 'Invalid data' }), 400


@app.route('/informe_tecnico_check_informe/<int:id>', methods=['PUT'])
def update_check_informe(id):
    data = request.get_json()
    record = InformeTecnico.query.get(id)
    if 'value' in data:
        setattr(record, 'checkInforme', data['value'])
        db.session.commit()
        return jsonify({ 'success': True, 'checkInforme': record.checkInforme }), 200
    return jsonify({ 'error': 'Invalid data' }), 400

# Adicionales para TERCERA ETAPA
# Derechos Sustentados
@app.route('/derechos_sustentados', methods=['GET'])
def get_derechos_sustentados():
    try:
        derechos_sustentados = DerechoSustentado.query.filter_by().all()
        return derechos_sustentados_schema.jsonify(derechos_sustentados), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/derecho_sustentado/<int:id>', methods=['GET'])
def get_derecho_sustentado(id):
    try:
        derecho_sustentado = DerechoSustentado.query.filter_by(IdDerechoSustentado=id).first()
        if derecho_sustentado:
            return derecho_sustentado_schema.jsonify(derecho_sustentado), 200
        return jsonify({"error": "Derecho Sustentado no encontrado"}), 
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Area Diferencia
@app.route('/area_diferencias', methods=['GET'])
def get_area_diferencias():
    try:
        areas_diferencias = AreaDiferencia.query.filter_by().all()
        return area_diferencias_schema.jsonify(areas_diferencias), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/area_diferencia/<int:id>', methods=['GET'])
def get_area_diferencia(id):
    try:
        area_diferencia = AreaDiferencia.query.filter_by(IdAreaDiferencia=id).first()
        if area_diferencia:
            return area_diferencia_schema.jsonify(area_diferencia), 200
        return jsonify({"error": "Derecho Sustentado no encontrado"}), 
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# INICIO
@app.route('/', methods=['GET'])
def index():
    #return render_template('inicio.html')
    return jsonify({'message': 'Bienvenido a mi API, para consultas, comunicate con el administrador.'})

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)
    #app.run(debug=True)
