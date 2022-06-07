from flask import Flask, jsonify, request, Blueprint
from flask_mysqldb import MySQL

from config import config

app = Flask(__name__)

connection = MySQL(app)

@app.route('/tareas', methods=['POST'])
def agregar_tarea():
    try:
        cursor = connection.connection.cursor()
        sql = "INSERT INTO Tareas(id_tarea, tarea, id_usuario) VALUES ('{0}', '{1}', '{2}')".format(request.json['id_tarea'],request.json['tarea'],request.json['id_usuario'])
        cursor.execute(sql)
        connection.connection.commit()
        return jsonify({'mensaje': "Tarea Agregada"})
    except Exception as e:
        print(e)
        return jsonify({'mensaje':"Error"})

        
@app.route('/tareas/<id>', methods=['PUT'])
def editar_tarea(id):
    try:
        cursor = connection.connection.cursor()
        sql = "UPDATE Tareas SET tarea = '{0}', id_usuario = '{1}' WHERE id_tarea = '{2}'".format(request.json['tarea'],request.json['id_usuario'],id)
        cursor.execute(sql)
        connection.connection.commit()
        return jsonify({'mensaje': "Tarea Editada"})
    except Exception as e:
        print(e)
        return jsonify({'mensaje':"Error"})

@app.route('/tareas/<id>', methods=['DELETE'])
def eliminar_tarea(id):
    try:
        cursor = connection.connection.cursor()
        sql = "DELETE FROM Tareas WHERE id_tarea = '{0}'".format(id)
        cursor.execute(sql)
        connection.connection.commit()
        return jsonify({'mensaje': "Tarea Eliminada"})
    except Exception as e:
        print(e)
        return jsonify({'mensaje':"Error"})

@app.route('/tareas', methods=['GET'])
def list_tareas():
    try:
        cursor = connection.connection.cursor()
        sql = "SELECT * FROM Tareas"
        cursor.execute(sql)
        data = cursor.fetchall()
        tareas = []
        for fila in data:
            tarea = {'id_tarea':fila[0], 'tarea':fila[1], 'id_usuario':fila[2]}
            tareas.append(tarea)
        return jsonify({'tareas':tareas, 'mensaje':"Tareas Listadas"})
    except Exception as e:
        print(e)
        return jsonify({'mensaje':"Error"})

@app.route('/tareas/<id>', methods=['GET'])
def listar_tarea_id(id):
    try:
        cursor = connection.connection.cursor()
        sql = "SELECT * FROM Tareas WHERE id_tarea = '{0}'".format(id)
        cursor.execute(sql)
        data = cursor.fetchone()
        if data != None:
            tarea = {'id_tarea':data[0], 'tarea':data[1], 'id_usuario':data[2]}
            return jsonify({'tarea':tarea, 'mensaje': "Tarea encontrada"})
        else:
            return jsonify({'mensaje': "Tarea no encontrada"})
    except Exception as e:
        print(e)
        return jsonify({'mensaje':"Error"})

def error_404(error):
    return "Pagina no encontrada", 404

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404,error_404)
    app.run()