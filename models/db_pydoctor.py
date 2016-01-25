# -*- coding: utf-8 -*-

db = DAL('sqlite://storage_new.sqlite')
from gluon.tools import *

def advanced_editor(field, value):
    return TEXTAREA(_id = str(field).replace('.','_'),
                    _name=field.name,
                    _class='text ckeditor',
                    value=value, _cols=80, _rows=10)


auth = Auth(globals(),db)
auth.define_tables()
crud = Crud(globals(),db)

db.define_table('persona',
                Field('sexo',requires = IS_IN_SET({'F':'Femenino', 'M':'Masculino', 'J':'Persona Jurídica'},
                                                   zero=T('Elija persona jurídica o sexo'),
                                                   error_message='debe elegir persona jurídica o sexo persona física')),
                Field('apellido',required=True,label=T('Apellido o Razón Social')),
                Field('nombre',label=T('Nombre')),
                Field('cuitcuil',required=True,label=T('CUIT/CUIL')),
                Field('domicilio',required=True,label=T('Domicilio')),
                Field('email',requires=IS_EMPTY_OR(IS_EMAIL()),label=T('E-Mail')),
                Field('observaciones','text',label=T('Observaciones')),
                Field('telefono',label=T('Teléfono')),
                Field('celular',label=T('Celular')),
                Field('fotografia','upload',requires = IS_EMPTY_OR(IS_IMAGE())),
                Field('matricula',label=T('Matrícula'),comment=T('Matrícula profesional de abogado')),
                Field('domiciliolegal',label=T('Domicilio Legal'),comment=T('Domicilio legal del abogado')),
                auth.signature,
               format='%(cuitcuil)s %(apellido)s,%(nombre)s')
db.persona.id.readable=db.persona.id.writable=False
db.persona.observaciones.widget = advanced_editor

db.define_table('fuero',
                Field('descripcion',required=True,label=T('Descripción')),
               format='%(descripcion)s')
db.fuero.id.readable=db.fuero.id.writable=False

db.define_table('instancia',
                Field('descripcion',required=True,label=T('Descripción')),
               format='%(descripcion)s')
db.instancia.id.readable=db.instancia.id.writable=False

db.define_table('juzgado',
                Field('descripcion',required=True,label=T('Descripción')),
                Field('fuero_id',db.fuero,label=T('Fuero')),
                Field('instancia_id',db.instancia,label=T('Instancia')),
                auth.signature)
db.juzgado.fuero_id.widget = SQLFORM.widgets.autocomplete(
     request, db.fuero.descripcion, id_field=db.fuero.id)
db.juzgado.instancia_id.widget = SQLFORM.widgets.autocomplete(
     request, db.instancia.descripcion, id_field=db.instancia.id)
db.juzgado.fuero_id.requires = IS_IN_DB(db,db.fuero.id,'%(descripcion)s')
db.juzgado.instancia_id.requires = IS_IN_DB(db,db.instancia.id,'%(descripcion)s')
db.juzgado.descripcion.requires = IS_NOT_IN_DB(db, 'juzgado.descripcion')
db.juzgado.id.readable=db.juzgado.id.writable=False

#Listado de tipos de proceso posibles.
db.define_table('tipoproceso',
               Field('descripcion',required=True,label=T('Descripción')),
               format='%(descripcion)s',
               singular=T('Tipo de proceso'),
               plural=T('Tipo de proceso'),)
db.fuero.id.readable=db.fuero.id.writable=False

db.define_table('expediente',
                Field('numero',requires = IS_NOT_IN_DB(db, 'expediente.numero'),label=T('Nº de expediente')),
                Field('caratula',required=True, label=T('Carátula')),
                Field('juzgado_id',db.juzgado, label=T('Juzgado o Fiscalía de origen')),
                Field('inicio','date', label=T('Fecha inicio')),
                Field('final','date', label=T('Fecha fin')),
                auth.signature,
               format='%(numero)s %(caratula)s')
db.expediente.id.readable=db.expediente.id.writable=False
db.expediente.juzgado_id.widget = SQLFORM.widgets.autocomplete(
     request, db.juzgado.descripcion, id_field=db.juzgado.id)

db.define_table('movimiento',
                Field('expediente_id',db.expediente),
                Field('estado',requires = IS_IN_SET({'P':'Procesal', 'E':'Extraprocesal'},
                                                   zero=None,
                                                   error_message='Seleccione estado del movimiento')),
                Field('titulo',required=True, label=T('Título')),
                Field('texto','text',label=T('Texto'),requires = IS_NOT_EMPTY()),
                Field('archivo','upload'),
                auth.signature,
                singular = T("Movimiento"), plural = T("Movimientos"),
               format='%(titulo)s')
db.movimiento.expediente_id.readable=db.movimiento.expediente_id.writable=False
db.movimiento.id.readable=db.movimiento.id.writable=False
db.movimiento._singular = T("Movimiento")
db.movimiento._plural = T("Movimientos")
db.movimiento.texto.widget = advanced_editor

db.define_table('agenda',
                Field('expediente_id',db.expediente),
                Field('vencimiento','datetime',label=T('Vence en')),
                Field('cumplido','datetime',label=T('Cumplido el')),
                Field('prioridad',requires = IS_IN_SET({0:'Urgente',1:'Prioritario', 2:'Importante',3:'Recordar'},
                                                   zero=1,
                                                   error_message='Elija una prioridad')),
                Field('estado',requires = IS_IN_SET({'P': T('Pendiente'), 'C':T('Cancelada'), 'R': T('Realizada')},
                                                   zero='P',
                                                   error_message=T('Establezca un estado'))),
                Field('titulo',required=True, label=T('Título')),
                Field('texto','text',label=T('Texto')),
                auth.signature)
db.agenda.expediente_id.readable=db.agenda.expediente_id.writable=False
db.agenda.id.readable=db.agenda.id.writable=False

db.define_table('parte',
                Field('expediente_id',db.expediente),
                Field('persona_id',db.persona,label=T('Persona')),
                Field('caracter',label=T('Carácter'),comment=T('Carácter en que se presenta la parte: actor, demandado, imputado, etc')),
                Field('observaciones','text'),
                auth.signature)
db.parte.expediente_id.readable=db.parte.expediente_id.writable=False
db.parte.id.readable=db.parte.id.writable=False