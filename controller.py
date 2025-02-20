import os
import uuid
from flask import Flask, render_template, request, redirect, session, flash, url_for  
from werkzeug.utils import secure_filename
from conexion import connectionBD
from route import *

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif'}

def allowed_file(filename):
    return '.' in filename and os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS

def registro_form():
    
    if request.method == "POST":
        name = request.form.get("Name")
        email = request.form.get("Mail")
        tel = request.form.get("Teléfono")
        direc = request.form.get("Dirección")
        password = request.form.get("password")
        repassword = request.form.get("Repassword")
        
        errores = []
        caracteres_permitidos_contraseña = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-!?¿¡,.@$")
        caracteres_permitidos_mail = set("abcdefghijklmnopqrstuvwxyz0123456789_-.@")
        caracteres_permitidos_txt = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz ")
        caracteres_permitidos_direc = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz 1234567890")
        caracteres_permitidos_num =set("1234567890")
        
        if not name or not email or not tel or not direc or not password or not repassword:
            print("Completa todos los campos")
            errores.append("error")
        if not all(char in caracteres_permitidos_txt for char in name):
            print("Nombre inválido")
            errores.append("error")
        if not all(char in caracteres_permitidos_direc for char in direc):
            print("Dirección inválida")
            errores.append("error")
        if not all(char in caracteres_permitidos_num for char in tel) or (len(tel)<4 or len(tel)>10):
            print("Teléfono inválido")
            errores.append("error")
        if '@' not in email or '.' not in email or not all(char in caracteres_permitidos_mail for char in email):
            print("Mail inválido")
            errores.append("error")
        if not all(char in caracteres_permitidos_contraseña for char in password) or len(password)<3:
            print("Contraseña inválida")
            errores.append("error")
        if password != repassword:
            print("Las contraseñas deben coincidir")
            errores.append("error")
        
        if len(errores)>0:
            flash("Error en el registro", "danger")
            return redirect("/home")

        connection = connectionBD()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT idusuario FROM usuario WHERE email = %s", (email,))
        if cursor.fetchone():
            flash("El email ya está registrado", "danger")
            connection.close()
            return redirect("/home")
        
        cursor.execute(
            "INSERT INTO usuario (nombre, direccion, telefono, email, clave) VALUES (%s, %s, %s, %s, %s)",
            (name, direc, tel, email, password)
        )
        connection.commit()
        cursor.execute("SELECT idusuario FROM usuario WHERE email = %s", (email,))
        idusuario = cursor.fetchone()['idusuario']
        connection.close()
        
        crear_chat_personal(idusuario)

        flash("Usuario registrado correctamente!", "success")
        return redirect("/home")

    return render_template("registro.html")


def login_form():
    
    if request.method == "POST":
        email = request.form.get("Mail")
        password = request.form.get("password")
        
        errores = []

        if not email or not password:
            print("Campos incompletos")
            return redirect("/home")

        connection = connectionBD()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuario WHERE email = %s", (email,))
        user = cursor.fetchone()
        connection.close()

        if not user:
            flash("El email no está registrado", "danger")
            return redirect("/home")

        if password != user["clave"]:
            flash("Contraseña incorrecta", "danger")
            return redirect("/home")

        session["usuario"] = user["nombre"]
        session["idusuario"] = user["idusuario"]
        flash(f"Bienvenido, {user['nombre']}!", "success")
        return redirect("/home")

    return render_template("login.html")

def logout():
    session.pop('usuario', None)
    session.pop('idusuario', None)
    flash("Sesión cerrada correctamente", "success")
    return redirect("/home")

def perfil():
    if "idusuario" not in session:
        flash("Debes iniciar sesión para acceder a tu perfil", "danger")
        return redirect("/home")

    connection = connectionBD()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT nombre, direccion, telefono, email FROM usuario WHERE idusuario = %s", (session["idusuario"],))
    usuario = cursor.fetchone()
    connection.close()
    
    username = session.get('usuario')

    return render_template("perfil.html", usuario=usuario, usuarioChecked=username)

def modificar_perfil():
    if "idusuario" not in session:
        flash("Debes iniciar sesión para modificar tu perfil", "danger")
        return redirect("/home")

    if request.method == "POST":
        name = request.form.get("Name")
        email = request.form.get("Mail")
        tel = request.form.get("Teléfono")
        direc = request.form.get("Dirección")
        clave_actual = request.form.get("ClaveActual")
        clave_nueva = request.form.get("ClaveNueva")
        clave_repetida = request.form.get("ClaveRepetida")

        errores = []
        caracteres_permitidos_contraseña = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-!?¿¡,.@$")
        caracteres_permitidos_mail = set("abcdefghijklmnopqrstuvwxyz0123456789_-.@")
        caracteres_permitidos_txt = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz ")
        caracteres_permitidos_direc = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz 1234567890")
        caracteres_permitidos_num = set("1234567890")

        # Valido si hay campos vacios
        if not name or not email or not tel or not direc:
            errores.append("Completa todos los campos obligatorios")

        # Valido el ingreso en los campos
        if not all(char in caracteres_permitidos_txt for char in name):
            errores.append("Nombre inválido")

        if not all(char in caracteres_permitidos_direc for char in direc):
            errores.append("Dirección inválida")

        if not all(char in caracteres_permitidos_num for char in tel) or (len(tel) < 4 or len(tel) > 10):
            errores.append("Teléfono inválido")

        if '@' not in email or '.' not in email or not all(char in caracteres_permitidos_mail for char in email):
            errores.append("Mail inválido")

        connection = connectionBD()
        cursor = connection.cursor(dictionary=True)

        # Verifico si el mail editado esta registrado por otro usuario
        cursor.execute("SELECT idusuario FROM usuario WHERE email = %s AND idusuario != %s", (email, session["idusuario"]))
        if cursor.fetchone():
            errores.append("El email ya está registrado por otro usuario")

        # Verifico contraseña actual y valido la nueva
        if clave_actual or clave_nueva or clave_repetida:
            cursor.execute("SELECT clave FROM usuario WHERE idusuario = %s", (session["idusuario"],))
            usuario = cursor.fetchone()

            if not clave_actual or usuario["clave"] != clave_actual:
                errores.append("La contraseña actual es incorrecta")

            if clave_nueva and (not all(char in caracteres_permitidos_contraseña for char in clave_nueva) or len(clave_nueva) < 3):
                errores.append("Contraseña inválida, debe tener al menos 3 caracteres")

            if clave_nueva != clave_repetida:
                errores.append("Las nuevas contraseñas no coinciden")

        # Si hay errores los muestro y redirijo
        if errores:
            for error in errores:
                flash(error, "danger")
            connection.close()
            return redirect("/perfil")

        # Actualizo los datos
        if clave_nueva:
            cursor.execute(
                "UPDATE usuario SET nombre = %s, direccion = %s, telefono = %s, email = %s, clave = %s WHERE idusuario = %s",
                (name, direc, tel, email, clave_nueva, session["idusuario"])
            )
        else:
            cursor.execute(
                "UPDATE usuario SET nombre = %s, direccion = %s, telefono = %s, email = %s WHERE idusuario = %s",
                (name, direc, tel, email, session["idusuario"])
            )

        connection.commit()
        connection.close()

        session["usuario"] = name
        flash("Perfil actualizado correctamente", "success")
        return redirect("/perfil")

    return redirect("/perfil")

def lista_productos(usuarioChecked = None):
    connection = connectionBD()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()
        
        return render_template("listaprods.html", productos=productos, usuarioChecked=usuarioChecked)
    except Exception as e:
        flash(f"Error al cargar los productos: {str(e)}", "danger")
        return redirect("/home")
    finally:
        cursor.close()
        connection.close()

def cargaprod(usuarioChecked = None):
    if request.method == "POST":
        
        idproducto = request.form.get("idproducto")
        nombre = request.form.get("nombre")
        descripcion = request.form.get("desc")
        precio = int(request.form.get("precio"))
        stock = int(request.form.get("stock"))
        categoria = request.form.get("categoria")
        descuento = int(request.form.get("descuento"))
        vendidos = int(request.form.get("vendidos"))
        
        errores = []
        if not nombre or not descripcion or precio < 0 or stock < 0 or not categoria or descuento < 0 or vendidos < 0:
            errores.append("Datos inválidos en el formulario")
        
        if len(errores) > 0:
            flash("Error en los datos del producto", "danger")
            return redirect("/cargaprod")
        
        connection = connectionBD()
        cursor = connection.cursor()

        try:
            if idproducto:
                
                cursor.execute("UPDATE productos SET nombre = %s, descripcion = %s, precio = %s, stock = %s, categoria = %s, descuento = %s, vendidos = %s WHERE idproducto = %s", (nombre, descripcion, precio, stock, categoria, descuento, vendidos, idproducto))

            else:
                
                cursor.execute("INSERT INTO productos (nombre, descripcion, precio, stock, categoria, descuento, vendidos) VALUES (%s, %s, %s, %s, %s, %s, %s)", (nombre, descripcion, precio, stock, categoria, descuento, vendidos))
                idproducto = cursor.lastrowid
            
            if 'imagenes' in request.files:
                imagenes = request.files.getlist('imagenes')
                for imagen in imagenes:
                    if imagen.filename != '' and allowed_file(imagen.filename):
                        extension = os.path.splitext(imagen.filename)[1]
                        nuevoNombre = f"{idproducto}_{uuid.uuid4().hex}{extension}"
                        ruta_archivo = os.path.join(app.config['UPLOAD_FOLDER'], nuevoNombre)

                        try:
                            imagen.save(ruta_archivo)
                            cursor.execute("INSERT INTO imgproductos (idproducto, rutaimg) VALUES (%s, %s)", (idproducto, nuevoNombre))
                        except Exception as e:
                            flash(f"Error al guardar la imagen {imagen.filename}: {str(e)}", "warning")
            
            connection.commit()
            flash("Producto cargado con éxito", "success")
            return redirect("/cargaprod")

        except Exception as e:
            connection.rollback()
            flash(f"Error al cargar el producto: {str(e)}", "danger")
            return redirect("/cargaprod")
        
        finally:
            cursor.close()
            connection.close()
        
        
    idproducto = request.args.get("idproducto")
    if idproducto:
        connection = connectionBD()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM productos WHERE idproducto = %s", (idproducto,))
        producto = cursor.fetchone()
        cursor.execute("SELECT rutaimg FROM imgproductos WHERE idproducto = %s", (idproducto,))
        producto['imagenes'] = cursor.fetchall()
        connection.close()
        return render_template("cargaprod.html", producto=producto, usuarioChecked=usuarioChecked)

    return render_template("cargaprod.html", usuarioChecked=usuarioChecked)

def eliminar_imagen_prod():
    idproducto = request.form.get('idproducto')
    rutaimg = request.form.get('rutaimg')
    
    if not idproducto or not rutaimg:
        flash("Datos inválidos para eliminar la imagen", "danger")
        return redirect(url_for('cargaprod_ruta', idproducto=idproducto))
    
    connection = connectionBD()
    cursor = connection.cursor()

    try:
        # Elimino el archivo de carpeta de imágenes
        ruta_archivo = os.path.join(app.config['UPLOAD_FOLDER'], rutaimg)
        if os.path.exists(ruta_archivo):
            os.remove(ruta_archivo)

        # Elimino entrada de imagen en base de datos
        cursor.execute("DELETE FROM imgproductos WHERE idproducto = %s AND rutaimg = %s", (idproducto, rutaimg))
        connection.commit()

        flash("Imagen eliminada con éxito", "success")
    except Exception as e:
        connection.rollback()
        flash(f"Error al eliminar la imagen: {e}", "danger")
    finally:
        cursor.close()
        connection.close()

    return redirect(url_for('cargaprod_ruta', idproducto=idproducto))

def eliminar_producto():
    idproducto = request.form.get("idproducto")

    if not idproducto:
        flash("No se encontró el producto a eliminar", "danger")
        return redirect("/cargaprod")

    connection = connectionBD()
    cursor = connection.cursor()

    try:
        # Elimino imagenes del producto
        cursor.execute("SELECT rutaimg FROM imgproductos WHERE idproducto = %s", (idproducto,))
        imagenes = cursor.fetchall()
        for img in imagenes:
            ruta_archivo = os.path.join(app.config['UPLOAD_FOLDER'], img[0])
            if os.path.exists(ruta_archivo):
                os.remove(ruta_archivo)

        cursor.execute("DELETE FROM imgproductos WHERE idproducto = %s", (idproducto,))
        cursor.execute("DELETE FROM productos WHERE idproducto = %s", (idproducto,))

        connection.commit()
        flash("Producto eliminado con éxito", "success")
    except Exception as e:
        connection.rollback()
        flash(f"Error al eliminar el producto: {e}", "danger")
    finally:
        cursor.close()
        connection.close()

    return redirect("/cargaprod")

def productos_carrusel():
    connection = connectionBD()
    cursor = connection.cursor(dictionary=True)

    try:
        query = """SELECT productos.idproducto, productos.nombre, productos.precio, productos.descuento, 
                          (SELECT imgproductos.rutaimg FROM imgproductos WHERE imgproductos.idproducto = productos.idproducto LIMIT 1) AS rutaimg
                   FROM productos
                   ORDER BY productos.descuento DESC LIMIT 5;"""
        cursor.execute(query)
        productos = cursor.fetchall()
        return productos
    except Exception as e:
        flash("Error al obtener productos", "danger")
        return []
    finally:
        cursor.close()
        connection.close()

def productos_galeria():
    connection = connectionBD()
    cursor = connection.cursor(dictionary=True)
    try:
        query = """SELECT productos.idproducto, productos.nombre, productos.precio, productos.descuento, productos.vendidos, 
                          (SELECT imgproductos.rutaimg FROM imgproductos WHERE imgproductos.idproducto = productos.idproducto LIMIT 1) AS rutaimg
                   FROM productos
                   ORDER BY productos.vendidos DESC LIMIT 12;"""
        cursor.execute(query)
        productos = cursor.fetchall()
        return productos
    except Exception as e:
        flash("Error al obtener productos", "danger")
        return []
    finally:
        cursor.close()
        connection.close()
        
        
def obtener_productos_filtrados(categoria=None, orden="nombre", query="", page=1):
    connection = connectionBD()
    cursor = connection.cursor(dictionary=True)
    
    productos_por_pagina = 20
    offset = (page - 1) * productos_por_pagina  # Donde se empieza paginacion

    try:
        query_sql = """
            SELECT productos.idproducto, productos.nombre, productos.descripcion, productos.precio, 
                   productos.stock, productos.categoria, productos.descuento, productos.vendidos,
                   (SELECT imgproductos.rutaimg FROM imgproductos WHERE imgproductos.idproducto = productos.idproducto LIMIT 1) AS rutaimg
            FROM productos
        """
        
        params = []
        count_params = []
        condiciones = []

        # Agrego condición para categoría
        if categoria:
            condiciones.append("productos.categoria = %s")
            params.append(categoria)
            count_params.append(categoria)

        # Agrego condición si query no está vacío
        if query:
            condiciones.append("(LOWER(productos.nombre) LIKE %s OR LOWER(productos.categoria) LIKE %s)")
            params.append(f"%{query.lower()}%")
            params.append(f"%{query.lower()}%")
            count_params.append(f"%{query.lower()}%")
            count_params.append(f"%{query.lower()}%")

        # Agrego condiciones a la query si hay alguna
        if condiciones:
            query_sql += " WHERE " + " AND ".join(condiciones)

        # Modifico ORDER BY por el valor de 'orden'
        if orden == "precio":
            query_sql += " ORDER BY productos.precio"
        else:
            query_sql += " ORDER BY productos.nombre"

        # Agrego paginación con LIMIT y OFFSET para consulta de productos
        query_sql += " LIMIT %s OFFSET %s"
        params.append(productos_por_pagina)
        params.append(offset)

        # Hago consulta de productos
        cursor.execute(query_sql, tuple(params))
        productos = cursor.fetchall()

        # Obtengo total de productos para paginación
        count_query_sql = "SELECT COUNT(*) AS total FROM productos"
        if condiciones:
            count_query_sql += " WHERE " + " AND ".join(condiciones)

        # Hago la consulta de conteo de productos sin paginación
        cursor.execute(count_query_sql, tuple(count_params))
        total_productos = cursor.fetchone()["total"]
        total_paginas = (total_productos // productos_por_pagina) + (1 if total_productos % productos_por_pagina > 0 else 0)

        # Obtengo las categorías
        cursor.execute("SELECT DISTINCT categoria FROM productos")
        categorias = cursor.fetchall()

        return productos, categorias, total_paginas

    except Exception as e:
        flash(f"Error al obtener productos: {str(e)}", "danger")
        return [], [], 1
    finally:
        cursor.close()
        connection.close()
                

def obtener_detalle_producto(idproducto):
    connection = connectionBD()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM productos WHERE idproducto = %s", (idproducto,))
        producto = cursor.fetchone()

        if producto:
            cursor.execute("SELECT rutaimg FROM imgproductos WHERE idproducto = %s", (idproducto,))
            producto["imagenes"] = [img["rutaimg"] for img in cursor.fetchall()]

        return producto

    except Exception as e:
        flash(f"Error al obtener el producto: {str(e)}", "danger")
        return None

    finally:
        cursor.close()
        connection.close()
        
        
def obtener_carrito(idusuario=None):
    if idusuario:
        connection = connectionBD()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT p.idproducto, p.nombre, p.precio, p.descuento, pc.cantidad 
            FROM productoscarrito pc
            JOIN productos p ON pc.idproducto = p.idproducto
            JOIN carritos c ON pc.idcarrito = c.idcarrito
            WHERE c.idusuario = %s AND c.comprado = 'no'
        """, (idusuario,))
        carrito = cursor.fetchall()
        connection.close()
        
        # Verifico si el carrito está vacío (no hay carritos sin comprar)
        if not carrito:
            return [], 0  # Retorno carrito vacío y total 0 si no hay carritos
        
    else:
        carrito = session.get("carrito", [])

    # Calculo total de compra
    total_compra = sum(
        (producto['precio'] - (producto['precio'] * (producto['descuento'] / 100))) * producto['cantidad']
        for producto in carrito)

    return carrito, total_compra


def agregar_al_carrito(idproducto, cantidad, idusuario=None):
    connection = connectionBD()
    cursor = connection.cursor(dictionary=True)
    
    # Verifico stock del producto
    cursor.execute("SELECT stock FROM productos WHERE idproducto = %s", (idproducto,))
    producto = cursor.fetchone()
    if not producto or producto["stock"] < cantidad:
        flash("Stock insuficiente para agregar el producto al carrito", "danger")
        connection.close()
        return redirect(url_for('carrito'))

    if idusuario:
        # Verifico si el usuario ya tiene un carrito en proceso
        cursor.execute("SELECT idcarrito FROM carritos WHERE idusuario = %s AND comprado = 'no'", (idusuario,))
        carrito = cursor.fetchone()
        
        if carrito:
            idcarrito = carrito["idcarrito"]
        else:
            # Creo carrito si el usuario si no tiene
            cursor.execute("INSERT INTO carritos (idusuario, preciotot, comprado) VALUES (%s, 0, 'no')", (idusuario,))
            connection.commit()
            idcarrito = cursor.lastrowid
        
        # Verifico si el producto está en el carrito
        cursor.execute("SELECT cantidad FROM productoscarrito WHERE idcarrito = %s AND idproducto = %s", (idcarrito, idproducto))
        prod_en_carrito = cursor.fetchone()
        
        if prod_en_carrito:
            # Actualizo la cantidad del producto (si esta en carrito)
            nueva_cantidad = prod_en_carrito["cantidad"] + cantidad
            if nueva_cantidad > producto["stock"]:
                flash("Stock insuficiente para agregar el producto al carrito", "danger")
                connection.close()
                return redirect(url_for('carrito'))
            cursor.execute("UPDATE productoscarrito SET cantidad = %s WHERE idcarrito = %s AND idproducto = %s",
                           (nueva_cantidad, idcarrito, idproducto))
        else:
            # Agrego producto 
            if cantidad > producto["stock"]:
                flash("Stock insuficiente para agregar el producto al carrito", "danger")
                connection.close()
                return redirect(url_for('carrito'))
            cursor.execute("INSERT INTO productoscarrito (idcarrito, idproducto, cantidad) VALUES (%s, %s, %s)",
                           (idcarrito, idproducto, cantidad))
        
        connection.commit()
    else:
        # Guardo en sesión si es un invitado
        carrito = session.get("carrito", [])
        item_existente = next((item for item in carrito if item["idproducto"] == idproducto), None)

        if item_existente:
            item_existente["cantidad"] += cantidad
        else:
            # Agrego productos al carrito del invitado
            cursor.execute("SELECT nombre, precio, descuento FROM productos WHERE idproducto = %s", (idproducto,))
            producto_detalle = cursor.fetchone()
            if not producto_detalle:
                flash("Producto no encontrado", "danger")
                connection.close()
                return redirect(url_for('home'))
            carrito.append({
                "idproducto": idproducto,
                "cantidad": cantidad,
                "nombre": producto_detalle["nombre"],
                "precio": producto_detalle["precio"],
                "descuento": producto_detalle["descuento"]
            })

        session["carrito"] = carrito

    connection.close()


def eliminar_del_carrito(idproducto, idusuario=None):
    if idusuario:
        connection = connectionBD()
        cursor = connection.cursor()
        cursor.execute("""
            DELETE pc FROM productoscarrito pc
            JOIN carritos c ON pc.idcarrito = c.idcarrito
            WHERE c.idusuario = %s AND pc.idproducto = %s
        """, (idusuario, idproducto))
        connection.commit()
        connection.close()
    else:
        # Elimino de la sesión si es un invitado
        carrito = session.get("carrito", [])
        session["carrito"] = [item for item in carrito if item["idproducto"] != idproducto]
        
        
def finalizar_compra(idusuario, tipoenvio):
    if not idusuario:
        flash("Debes iniciar sesión para finalizar la compra", "danger")
        return False

    # Obtengo carrito del usuario
    productos, total_compra = obtener_carrito(idusuario)
    if not productos:
        flash("Tu carrito está vacío", "danger")
        return False

    # Defino costos de envio
    envio_costos = {
        "envio": 6500,  # Costo de envío a domicilio
        "retiro": 0     # Costo de retiro en tienda
    }

    # Obtengo costo de envio segun lo que selecciono
    costo_envio = envio_costos.get(tipoenvio, 0)
    total_final = total_compra + costo_envio

    connection = connectionBD()
    cursor = connection.cursor(dictionary=True)

    try:
        # Obtengo idcarrito del usuario
        cursor.execute("SELECT idcarrito FROM carritos WHERE idusuario = %s AND comprado = 'no'", (idusuario,))
        carrito = cursor.fetchone()
        if not carrito:
            flash("No se encontró un carrito sin comprar para el usuario", "danger")
            return False

        idcarrito = carrito["idcarrito"]

        # Inserto compra
        cursor.execute(
            "INSERT INTO compras (idusuario, idcarrito, tipoenvio, estadocompra) VALUES (%s, %s, %s, %s)",
            (idusuario, idcarrito, tipoenvio, "Pendiente de pago")
        )
        idcompra = cursor.lastrowid

        # Creo chat de compra
        cursor.execute(
            "INSERT INTO chat (idusuario, idcompra) VALUES (%s, %s)",
            (idusuario, idcompra)
        )
        idchat = cursor.lastrowid  # Obtengo ID del chat que se acaba de crear
        
        # Creo mensaje por generacion de pedido
        cursor.execute(
            "INSERT INTO mensajes (idchat, idusuario, mensaje) VALUES (%s, %s, %s)",
            (idchat, 1, "¡Gracias por tu pedido! Decinos tus dudas y avisanos cuando realices tu transferencia.")
        )

        # Actualizo stock de productos y cargo productos comprados
        for producto in productos:
            cursor.execute(
                "UPDATE productos SET stock = stock - %s, vendidos = vendidos + %s WHERE idproducto = %s",
                (producto['cantidad'], producto['cantidad'], producto['idproducto'])
            )

        # Actualizo carrito a comprado y el calculo preciotot
        cursor.execute("UPDATE carritos SET comprado = 'sí', preciotot = %s WHERE idcarrito = %s", (total_final, idcarrito))

        connection.commit()
        flash("Compra finalizada con éxito", "success")
        return idcompra

    except Exception as e:
        connection.rollback()
        flash(f"Error al finalizar la compra: {str(e)}", "danger")
        return False

    finally:
        cursor.close()
        connection.close()
        
def obtener_detalles_compra(idcompra):
    conn = connectionBD()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT c.idcompra, c.idusuario, u.nombre, ch.idchat, c.tipoenvio, c.estadocompra
        FROM compras c
        LEFT JOIN usuario u ON c.idusuario = u.idusuario
        LEFT JOIN chat ch ON c.idcompra = ch.idcompra
        WHERE c.idcompra = %s
    """, (idcompra, ))
    compra = cursor.fetchone()
    cursor.close()
    conn.close()
    return compra

def obtener_productos_compra(idcompra):
    conn = connectionBD()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.nombre, p.precio, cp.cantidad, p.descuento
        FROM productos p
        JOIN productoscarrito cp ON p.idproducto = cp.idproducto
        JOIN carritos c ON cp.idcarrito = c.idcarrito
        JOIN compras co ON c.idcarrito = co.idcarrito
        WHERE co.idcompra = %s
    """, (idcompra,))
    productos = cursor.fetchall()
    cursor.close()
    conn.close()
    total_compra = sum(
        (producto['precio'] - producto['precio'] * producto['descuento'] / 100) * producto['cantidad']
        for producto in productos
    )
    return productos, total_compra

def obtener_compras_usuario(idusuario, page, estado):
    conn = connectionBD()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT c.idcompra, c.estadocompra, car.preciotot AS total, chat.idchat
        FROM compras c
        JOIN carritos car ON c.idcarrito = car.idcarrito
        LEFT JOIN chat ON c.idcompra = chat.idcompra
        WHERE c.idusuario = %s
    """
    params = [idusuario]
    if estado:
        query += " AND c.estadocompra = %s"
        params.append(estado)
    query += " ORDER BY FIELD(c.estadocompra, 'Pendiente de Pago', 'En Proceso', 'Listo para Retirar', 'En Viaje', 'Recibido') LIMIT %s OFFSET %s"
    params.extend([20, (page-1)*20])
    cursor.execute(query, params)
    compras = cursor.fetchall()
    cursor.close()
    conn.close()
    return compras if compras else []

def obtener_todas_compras(page, estado):
    conn = connectionBD()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT c.idcompra, c.estadocompra, c.tipoenvio, car.preciotot AS total, chat.idchat
        FROM compras c
        JOIN carritos car ON c.idcarrito = car.idcarrito
        LEFT JOIN chat ON c.idcompra = chat.idcompra
    """
    params = []
    if estado:
        query += " WHERE c.estadocompra = %s"
        params.append(estado)
    query += " ORDER BY FIELD(c.estadocompra, 'Pendiente de Pago', 'En Proceso', 'Listo para Retirar', 'En Viaje', 'Recibido') LIMIT %s OFFSET %s"
    params.extend([20, (page-1)*20])
    cursor.execute(query, params)
    compras = cursor.fetchall()
    cursor.close()
    conn.close()
    return compras if compras else []

def actualizar_estado_compra_bd(idcompra, nuevo_estado):
    conn = connectionBD()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE compras
        SET estadocompra = %s
        WHERE idcompra = %s
    """, (nuevo_estado, idcompra))
    conn.commit()
    cursor.close()
    conn.close()

def eliminar_compra_bd(idcompra):
    conn = connectionBD()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM compras WHERE idcompra = %s", (idcompra,))
    conn.commit()
    cursor.close()
    conn.close()
    
def obtener_estado_compra(idcompra):
    conn = connectionBD()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT estadocompra FROM compras WHERE idcompra = %s", (idcompra,))
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()
    return resultado['estadocompra'] if resultado else None

def obtener_id_carrito(idcompra):
    conn = connectionBD()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT idcarrito FROM compras WHERE idcompra = %s", (idcompra,))
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()
    return resultado['idcarrito'] if resultado else None

def eliminar_compra_bd(idcompra, idcarrito):
    conn = connectionBD()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM compras WHERE idcompra = %s", (idcompra,))
        cursor.execute("DELETE FROM carritos WHERE idcarrito = %s", (idcarrito,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        flash(f"Error al cancelar la compra: {str(e)}", "danger")
    finally:
        cursor.close()
        conn.close()
        
def crear_chat_personal(idusuario):
    conn = connectionBD()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO chat (idusuario) VALUES (%s)",
            (idusuario,)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        flash(f"Error al crear el chat personal: {str(e)}", "danger")
    finally:
        cursor.close()
        conn.close()
        
def obtener_mensajes_chat(idchat):
    conn = connectionBD()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT u.nombre as usuario, m.mensaje, m.fecha_hora
        FROM mensajes m
        JOIN usuario u ON m.idusuario = u.idusuario
        WHERE m.idchat = %s
        ORDER BY m.fecha_hora ASC
    """, (idchat,))
    mensajes = cursor.fetchall()
    cursor.close()
    conn.close()
    return mensajes

def enviar_mensaje_bd(idchat, idusuario, mensaje):
    conn = connectionBD()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO mensajes (idchat, idusuario, mensaje, fecha_hora) VALUES (%s, %s, %s, NOW())",
            (idchat, idusuario, mensaje)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        flash(f"Error al enviar el mensaje: {str(e)}", "danger")
    finally:
        cursor.close()
        conn.close()
        
def obtener_chats_usuario(idusuario):
    conn = connectionBD()
    cursor = conn.cursor(dictionary=True)

    # Obtengo chats del usuario ordenados por fecha de ultimo mensaje descendentemente
    cursor.execute("""
        SELECT 
            c.idchat, 
            c.idcompra, 
            c.idusuario, 
            MAX(m.fecha_hora) AS ultimo_mensaje_fecha,  -- Asegura que tomes la fecha más reciente
            (SELECT idusuario FROM mensajes WHERE idchat = c.idchat ORDER BY fecha_hora DESC LIMIT 1) AS ultimo_mensaje_usuario
        FROM 
            chat c
        LEFT JOIN 
            mensajes m ON c.idchat = m.idchat
        WHERE 
            c.idusuario = %s
        GROUP BY 
            c.idchat, c.idusuario, c.idcompra
        ORDER BY 
            ultimo_mensaje_fecha DESC
    """, (idusuario,))
    
    chats = cursor.fetchall()

    for chat in chats:
        chat['es_admin'] = chat['ultimo_mensaje_usuario'] == 1

    cursor.close()
    conn.close()
    return chats


def obtener_todos_chats():
    conn = connectionBD()
    cursor = conn.cursor(dictionary=True)

    # Obtengo chats ordenados por fecha de ultimo mensaje descendentemente
    cursor.execute("""
        SELECT 
            c.idchat, 
            c.idcompra, 
            c.idusuario, 
            MAX(m.fecha_hora) AS ultimo_mensaje_fecha,
            (SELECT idusuario FROM mensajes WHERE idchat = c.idchat ORDER BY fecha_hora DESC LIMIT 1) AS ultimo_mensaje_usuario, 
            u.nombre AS usuario
        FROM 
            chat c
        LEFT JOIN 
            mensajes m ON c.idchat = m.idchat
        LEFT JOIN 
            usuario u ON c.idusuario = u.idusuario
        GROUP BY 
            c.idchat, c.idusuario, c.idcompra, u.nombre
        ORDER BY 
            ultimo_mensaje_fecha DESC
    """)
    chats = cursor.fetchall()

    # Marco si el ultimo mensaje es del administrador
    for chat in chats:
        chat['es_admin'] = chat['ultimo_mensaje_usuario'] == 1

    cursor.close()
    conn.close()
    return chats



def obtener_info_chat(idchat):
    conn = connectionBD()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT idcompra FROM chat WHERE idchat = %s"
    cursor.execute(query, (idchat,))
    chat_info = cursor.fetchone()
    cursor.close()
    conn.close()
    return chat_info