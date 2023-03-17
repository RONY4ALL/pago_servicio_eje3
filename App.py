from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'b64b8nqmxb1ttbufoxjg-mysql.services.clever-cloud.com'
app.config['MYSQL_USER'] = 'up1hh0qi2xsonjuq'
app.config['MYSQL_PASSWORD'] = 'a5nRziQvat1I7BeZ22np'
app.config['MYSQL_DB'] = 'b64b8nqmxb1ttbufoxjg'
mysql = MySQL(app)


@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT pago.id_pago, servicio.nom_servicio, metodo_pago.nom_met_pago, pago.nom_cliente, pago.documento, pago.valor_pagar, pago.fecha_hora FROM pago JOIN servicio ON pago.id_servicio = servicio.id_servicio JOIN metodo_pago ON pago.id_met_pago = metodo_pago.id_met_pago')
    data = cur.fetchall()
    return render_template('index.html', Pagos=data)


@app.route('/add_venta', methods=['POST'])
def add_venta():
    if request.method == 'POST':
        id_servicio = request.form['id_servicio']
        id_met_pago = request.form['id_met_pago']
        nom_cliente = request.form['nom_cliente']
        documento = request.form['documento']
        valor_pagar = request.form['valor_pagar']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO pago (id_servicio, id_met_pago, nom_cliente ,documento, valor_pagar, fecha_hora) VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)',
                    (id_servicio, id_met_pago, nom_cliente, documento, valor_pagar))
        mysql.connection.commit()
        return redirect(url_for('Index'))


@app.route('/edit_ventas/<id>')
def get_ventas(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM pago WHERE id_pago = {0}'.format(id))
    data = cur.fetchall()
    return render_template('edit.html', Pagos=data[0])


@app.route('/update/<id>', methods=['POST'])
def update_venta(id):
    if request.method == 'POST':
        id_servicio = request.form['id_servicio']
        id_met_pago = request.form['id_met_pago']
        nom_cliente = request.form['nom_cliente']
        documento = request.form['documento']
        valor_pagar = request.form['valor_pagar']
        cur = mysql.connection.cursor()
        cur.execute(""" UPDATE pago SET id_servicio = %s, id_met_pago = %s, nom_cliente = %s, documento = %s, valor_pagar = %s, fecha_hora = CURRENT_TIMESTAMP WHERE id_pago = {0} """.format(id),
                    (id_servicio, id_met_pago, nom_cliente, documento, valor_pagar))
        mysql.connection.commit()
        return redirect(url_for('Index'))


@app.route('/delete/<string:id>')
def delete_venta(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM pago WHERE id_pago = {0}'.format(id))
    mysql.connection.commit()
    return redirect(url_for('Index'))


if __name__ == '__main__':
    app.run(port=3306, debug=True)
