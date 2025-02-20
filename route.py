import os
from flask import Flask, render_template, request, redirect, session, flash, url_for, send_from_directory
from werkzeug.utils import secure_filename
from conexion import connectionBD
from controller import *

app = Flask(__name__)

def route(app):
    @app.route("/")
    @app.route("/home")
    def home():
        username = session.get('usuario')
        carrusel = productos_carrusel()
        galeria = productos_galeria()
        return render_template('home.html', usuarioChecked=username, carrusel = carrusel, galeria = galeria)
    
    @app.route('/login', methods=["GET", "POST"])
    def login():
        return login_form()

    @app.route('/registro', methods=["GET", "POST"])
    def registro():
        return registro_form()
    
    @app.route("/perfil")
    def perfil_ruta():
        return perfil()

    @app.route("/perfil/modificar", methods=["POST"])
    def modificar_perfil_ruta():
        return modificar_perfil()

    
    @app.route("/logout", methods=["GET", "POST"])
    def logout_ruta():
        return logout()
    
    @app.route("/cargaprod", methods=["GET", "POST"])
    def cargaprod_ruta():
        username = session.get('usuario')
        user_id = session.get('idusuario')
        if not username or user_id != 1:
            flash("No tenés permisos para esta acción", "danger")
            return redirect('/home')
        return cargaprod(usuarioChecked=username)
    
    @app.route('/eliminar-imagen', methods=['POST'])
    def eliminar_imagen():
        username = session.get('usuario')
        user_id = session.get('idusuario')
        if not username or user_id != 1:
            flash("No tenés permisos para esta acción", "danger")
            return redirect('/home')
        return eliminar_imagen_prod()
    
    @app.route('/eliminar-producto', methods=['POST'])
    def eliminar_producto_ruta():
        username = session.get('usuario')
        user_id = session.get('idusuario')
        if not username or user_id != 1:
            flash("No tenés permisos para esta acción", "danger")
            return redirect('/home')
        return eliminar_producto()
    
    @app.route('/uploads/<filename>')
    def uploads(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    
    @app.route('/productos')
    def visualizar_productos():
        username = session.get('usuario')
        categoria = request.args.get('categoria', default=None, type=str)
        orden = request.args.get('orden', default="nombre", type=str)
        query = request.args.get('q', default='', type=str)
        page = request.args.get('page', default=1, type=int)

        productos, categorias, total_paginas = obtener_productos_filtrados(categoria, orden, query, page)

        return render_template(
            "productos.html", 
            productos=productos, 
            categorias=categorias, 
            categoria_seleccionada=categoria, 
            orden_seleccionado=orden, 
            usuarioChecked=username,
            page=page,
            total_paginas=total_paginas
        )
    
    @app.route('/productos/<int:idproducto>')
    def producto_detalle(idproducto):
        username = session.get('usuario')
        producto = obtener_detalle_producto(idproducto)

        if not producto:
            flash("El producto no existe", "danger")
            return redirect(url_for('visualizar_productos'))

        return render_template("producto_detalle.html", producto=producto, usuarioChecked=username)
    
    @app.route("/carrito")
    def carrito():
        idusuario = session.get("idusuario")
        username = session.get('usuario')
        productos, total_compra = obtener_carrito(idusuario)
        return render_template("carrito.html", productos=productos, total_compra=total_compra, usuarioChecked=username)

    @app.route("/agregar_al_carrito", methods=["POST"])
    def agregar_carrito():
        idproducto = int(request.form["idproducto"])
        cantidad = int(request.form["cantidad"])
        idusuario = session.get("idusuario")
        agregar_al_carrito(idproducto, cantidad, idusuario)
        return redirect(url_for("carrito"))

    @app.route("/eliminar_del_carrito/<int:idproducto>")
    def eliminar_carrito(idproducto):
        idusuario = session.get("idusuario")
        eliminar_del_carrito(idproducto, idusuario)
        return redirect(url_for("carrito"))
    
    @app.route("/finalizar_compra", methods=["POST"])
    def finalizar_compra_ruta():
        idusuario = session.get("idusuario")
        tipoenvio = request.form.get("tipoenvio")

        if not idusuario:
            flash("Debes iniciar sesión para finalizar la compra", "danger")
            return redirect(url_for('carrito'))

        idcompra = finalizar_compra(idusuario, tipoenvio)
        if idcompra:
            return redirect(url_for('compra', idcompra=idcompra))
        else:
            return redirect(url_for('carrito'))
        
    @app.route('/compra/<int:idcompra>')
    def compra(idcompra):
        idusuario = session.get('idusuario')
        username = session.get('usuario')
        compra = obtener_detalles_compra(idcompra)
        productos, total_compra = obtener_productos_compra(idcompra)

        if not compra:
            flash("La compra no existe", "danger")
            return redirect(url_for('home'))
        if compra['idusuario'] != idusuario:
            if idusuario != 1:
                flash("No tienes permisos para ver esta compra", "danger")
                return redirect(url_for('home'))

        return render_template("compra.html", compra=compra, productos=productos, total_compra=total_compra, usuarioChecked=username)
    
    @app.route('/compras', methods=['GET'])
    def compras():
        page = request.args.get('page', 1, type=int)
        estado = request.args.get('estado', '', type=str)
        idusuario = session.get('idusuario')
        username = session.get('usuario')
        
        if not idusuario:
            flash("Debes iniciar sesión para ver tus compras", "danger")
            return redirect(url_for('login'))

        if idusuario == 1:
            compras = obtener_todas_compras(page, estado)
        else:
            compras = obtener_compras_usuario(idusuario, page, estado)

        return render_template('listacompras.html', compras=compras, page=page, estado=estado, usuarioChecked=username)


    @app.route('/actualizar_estado_compra/<int:idcompra>', methods=['POST'])
    def actualizar_estado_compra(idcompra):
        if session.get('idusuario') != 1:
            flash("No tienes permisos para realizar esta acción", "danger")
            return redirect(url_for('compras'))

        nuevo_estado = request.form.get('nuevo_estado')
        actualizar_estado_compra_bd(idcompra, nuevo_estado)
        if request.form.get('comprita'):
            flash("Estado actualizado correctamente", "success")
            return redirect(url_for('compra', idcompra=idcompra))
        return redirect(url_for('compras'))
    
    @app.route('/cancelar_compra/<int:idcompra>', methods=['POST'])
    def cancelar_compra(idcompra):
        if session.get('idusuario') != 1:
            flash("No tienes permisos para realizar esta acción", "danger")
            return redirect(url_for('compras'))

        estado_compra = obtener_estado_compra(idcompra)
        if estado_compra == 'Recibido':
            flash("No puedes cancelar una compra en estado 'Recibido'", "danger")
            return redirect(url_for('compras'))
        
        idcarrito = obtener_id_carrito(idcompra)
        
        eliminar_compra_bd(idcompra, idcarrito)
        flash("Compra cancelada correctamente", "success")
        return redirect(url_for('compras'))
    
    @app.route('/chat')
    def chat():
        idusuario = session.get('idusuario')
        if not idusuario:
            flash("Debes iniciar sesión para acceder al chat", "danger")
            return redirect(url_for('home'))

        if idusuario == 1:
            chats = obtener_todos_chats()
        else:
            chats = obtener_chats_usuario(idusuario)
            
        return render_template('chat.html', idcompra=None, mensajes=[], chats=chats, usuarioChecked=session.get('usuario'))

    
    @app.route('/chat/<int:idchat>')
    def ver_chat(idchat):
        idusuario = session.get('idusuario')
        
        if not idusuario:
            flash("Debes iniciar sesión para acceder al chat", "danger")
            return redirect(url_for('home'))

        chat_info = obtener_info_chat(idchat)

        if not chat_info:
            flash("El chat no existe", "danger")
            return redirect(url_for('chat'))

        idcompra = chat_info.get("idcompra")

        mensajes = obtener_mensajes_chat(idchat)

        if idusuario == 1:
            chats = obtener_todos_chats()
        else:
            chats = obtener_chats_usuario(idusuario)

        return render_template('chat.html', idcompra=idcompra, idchat=idchat, mensajes=mensajes, chats=chats, usuarioChecked=session.get('usuario'))

    
    @app.route('/enviar_mensaje/<int:idchat>', methods=['POST'])
    def enviar_mensaje(idchat):
        idusuario = session.get('idusuario')
        if not idusuario:
            flash("Debes iniciar sesión para enviar mensajes", "danger")
            return redirect(url_for('login'))

        mensaje = request.form.get('mensaje')
        if mensaje:
            enviar_mensaje_bd(idchat, idusuario, mensaje)
        return redirect(url_for('ver_chat', idchat=idchat))

