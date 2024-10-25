from flask import Flask, render_template, request, redirect, send_file, url_for
import matplotlib.pyplot as plt
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import atexit
import shutil
import uuid
from flask_mail import Mail, Message
import math

app = Flask(__name__)

# Configuración de Flask-Mail para Gmail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'inforpotenciasolar@gmail.com'  # Cambia por nuestra dirección de correo
app.config['MAIL_PASSWORD'] = 'Potenciasolar2024'  # Cambia por nuestra contraseña
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

# Diccionario con consumo energético estimado en kWh por electrodoméstico por mes
appliance_energy = {
    "refrigerador": 45,
    "televisor": 6,
    "lavadora": 7,
    "microondas": 4,
    "computador": 10,
    "lamparas": 15,
    "videojuegos": 7,
    "cafetera": 4,
    "licuadora": 0.5,
    "plancha de ropa": 15,
    "plancha de pelo": 1.5,
    "secador": 11,
    "aspiradora": 1.5,
    "sonido en casa": 6
}

"""
-Define la ruta de la página principal (raíz) de la aplicación web.
-Cuando un usuario visita esa ruta, se ejecuta la función index(), que renderiza y devuelve el 
contenido del archivo index.html como respuesta.
"""


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contacto.html')
def contacto():
    return render_template('contacto.html')


@app.route('/s_nosotros.html')
def s_nosotros():
    return render_template('s_nosotros.html')


@app.route('/consumo.html')
def consumo():
    return render_template('consumo.html')


@app.route('/proveedores.html')
def proveedores():
    return render_template('proveedores.html')


@app.route('/datosantioquia.html')
def datosantioquia():
    return render_template('datosantioquia.html')


@app.route('/ayudas.html')
def ayudas():
    return render_template('ayudas.html')


@app.route('/calcular', methods=['POST'])
def calcular():
    appliances = request.form.getlist('appliance[]')  # obtiene la lista de electrodomésticos seleccionados
    quantities = request.form.getlist(
        'quantity[]')  # obtiene la lista de cantidades correspondientes a cada electrodoméstico.
    email = request.form['email']
    department = request.form['department']
    region = request.form['region']
    area_disponible = float(request.form.get('area_disponible'))

    # Obtener el tipo de gráficos seleccionados por el usuario
    chart_types = request.form.getlist('chart_type[]')

    total_energy = 0  # Para almacenar el consumo total de energía
    appliance_data = []  # Para almacenar la energía consumida por cada electrodoméstico.

    # Procesar cada electrodoméstico
    for appliance, quantity in zip(appliances,
                                   quantities):  # Se itera sobre las listas de electrodomésticos y sus cantidades usando zip()
        quantity = int(
            quantity)  # Para cada electrodoméstico, se convierte la cantidad a un entero, se calcula su consumo energético llamando a la función calculate_energy(), y se acumula el consumo total en total_energy.
        energy = calculate_energy(appliance, quantity)
        total_energy += energy
        appliance_data.append(
            (appliance, energy))  # La información de cada electrodoméstico se agrega a la lista appliance_data

    # Generar gráficos según lo que seleccione el usuario
    chart_filenames = []  # Lista para almacenar los nombres de los archivos de gráficos

    if 'bar' in chart_types:
        bar_chart = generate_chart(appliance_data, chart_type='bar')
        chart_filenames.append(bar_chart)

    if 'line' in chart_types:
        line_chart = generate_chart(appliance_data, chart_type='line')
        chart_filenames.append(line_chart)

    if 'pie' in chart_types:
        pie_chart = generate_chart(appliance_data, chart_type='pie')
        chart_filenames.append(pie_chart)

    chart_urls = [url_for('output_file', filename=filename) for filename in chart_filenames]

    send_email(email, appliance_data, total_energy, department,
               region)  # Se llama a la función send_email() para enviar un correo electrónico con los resultados del consumo energético y la información adicional.

    #    Cálculo de paneles solares
    # Parámetros para los paneles solares
    potencia_panel = 0.550  # Potencia en kW (550 W)
    horas_exposicion = 6  # Horas promedio de exposición diaria en Antioquia
    rendimiento = 1.25  # Factor de rendimiento
    area_panel = 2.2  # Área de un panel solar (m²)

    # Calcular consumo diario
    consumo_diario = total_energy / 30

    # Calcular el número de paneles necesarios
    paneles_necesarios = math.ceil(consumo_diario / (potencia_panel * horas_exposicion * rendimiento))

    # Calcular el área total necesaria para los paneles
    area_total = paneles_necesarios * area_panel

    """ Finalmente, se renderiza la plantilla resultados.html, pasando el consumo total de energía, la lista
        de datos de electrodomésticos y la URL del gráfico como parámetros. Esto permite que la plantilla 
        muestre los resultados al usuario."""
    # Comparar área total con el área disponible
    if area_total > area_disponible:
        # Si el área disponible es menor, se muestra una advertencia al usuario
        return render_template('resultados.html', total_energy=total_energy, appliance_data=appliance_data,
                               chart_urls=chart_urls,
                               paneles_necesarios=paneles_necesarios,
                               area_total=area_total,
                               area_disponible=area_disponible,
                               area_insuficiente=True)  # Indica que el área es insuficiente
    else:
        # Si el área disponible es suficiente, se continúa normalmente
        return render_template('resultados.html', total_energy=total_energy, appliance_data=appliance_data,
                               chart_urls=chart_urls,
                               paneles_necesarios=paneles_necesarios,
                               area_total=area_total,
                               area_disponible=area_disponible,
                               area_insuficiente=False)  # No hay problema con el área


@app.route('/contacto', methods=['POST'])
def enviar_contacto():
    # Obtener los datos del formulario
    nombre = request.form['nombre']
    correo = request.form['correo']
    telefono = request.form['telefono']
    comentarios = request.form['comentarios']

    # Crear el mensaje de correo
    msg = Message('Nuevo mensaje de contacto de Potencia Solar',
                  sender='inforpotenciasolar@gmail.com',  # Remitente (cambiar esto por nuestro correo)
                  recipients=['soportepotenciasolar@gmail.com'])  # Destinatario (debe ser otro correo)

    # Cuerpo del mensaje
    msg.body = f"""
    Has recibido un nuevo mensaje de contacto:

    Nombre: {nombre}
    Correo: {correo}
    Teléfono: {telefono}

    Comentarios:
    {comentarios}
    """

    # Enviar el correo
    mail.send(msg)

    return redirect(url_for('index'))  # Redirigir al inicio


def calculate_energy(appliance, quantity):
    """Calcula el consumo energético en kWh basado en el electrodoméstico y su cantidad."""
    return appliance_energy.get(appliance, 0) * quantity


def send_email(to_email, appliance_data, total_energy, department, region):
    """Envía un correo electrónico con el resultado del consumo energético."""
    from_email = "inforpotenciasolar@gmail.com"
    from_password = "Potenciasolar2024"

    # Crear el mensaje
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = 'Consumo Energético'

    body = f'El consumo total de energía es de {total_energy} kWh.\n\n'
    body += f'Departamento: {department}\nRegión: {region}\n\n'
    body += 'Detalles por electrodoméstico:\n'

    for appliance, energy in appliance_data:
        body += f'{appliance}: {energy} kWh\n'

    msg.attach(MIMEText(body, 'plain'))

    try:
        # Crea una instancia del objeto SMTP que se conecta al servidor SMTP de Gmail en el puerto 587,
        # que es el puerto utilizado para la comunicación segura a través de TLS (Transport Layer Security)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        # Inicia la conexión segura utilizando el protocolo TLS. Esto cifra la comunicación entre el cliente y el servidor
        server.starttls()
        # Inicia sesión en el servidor SMTP utilizando las credenciales proporcionadas
        server.login(from_email, from_password)
        server.sendmail(from_email, to_email, msg.as_string())
        # Cierra la conexión con el servidor SMTP.
        server.quit()
        print("Correo enviado exitosamente!")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")


"""
La función generate_chart() toma un argumento appliance_data, que es una lista de tuplas. 
Cada tupla contiene el nombre de un electrodoméstico y su correspondiente consumo de energía.
"""


def generate_chart(appliance_data, chart_type='bar'):
    appliances = [appliance for appliance, energy in appliance_data]
    energies = [energy for appliance, energy in appliance_data]

    plt.style.use('ggplot')
    plt.figure(figsize=(4, 4))

    if chart_type == 'bar':
        bars = plt.bar(appliances, energies, color='#3498db', edgecolor='black', linewidth=1.5)
        plt.xlabel('Electrodoméstico', fontsize=14)
        plt.ylabel('Consumo en kWh', fontsize=14)
        plt.title('Consumo Energético - Barra', fontsize=16, fontweight='bold')
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, yval, f'{yval:.0f} kWh', va='bottom', ha='center', fontsize=14, color='black')

    elif chart_type == 'line':
        plt.plot(appliances, energies, marker='o', color='#3498db', linewidth=2)
        plt.xlabel('Electrodoméstico', fontsize=14)
        plt.ylabel('Consumo en kWh', fontsize=14)
        plt.title('Consumo Energético - Línea', fontsize=16, fontweight='bold')

    elif chart_type == 'pie':
        plt.pie(energies, labels=appliances, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
        plt.title('Consumo Energético - Torta', fontsize=16, fontweight='bold')

    # Guardar el gráfico en un archivo PNG único
    if not os.path.exists('output'):
        os.makedirs('output')

    unique_id = str(uuid.uuid4())
    filename = f'consumo_{chart_type}_{unique_id}.png'
    filepath = os.path.join('output', filename)
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()

    return filename


"""
La función output_file() es responsable de manejar las solicitudes para acceder a archivos de imagen que 
han sido generados por la aplicación. Cuando un usuario solicita una imagen a través de 
la URL /output/<filename>, la función toma el nombre del archivo y lo envía al navegador del cliente para 
su visualización. Esto es útil para mostrar gráficos generados por Matplotlib en una página web, permitiendo 
que se integren fácilmente en las plantillas HTML.
"""


@app.route('/output/<filename>')
def output_file(filename):
    return send_file(os.path.join('output', filename))


# Función para borrar el directorio 'output'
def clean_output_directory():
    if os.path.exists('output'):
        shutil.rmtree('output')
        print("El directorio 'output' ha sido eliminado.")


# Registrar la función para que se ejecute al cerrar la app
atexit.register(clean_output_directory)

# Inicia la aplicación Flask
if __name__ == '__main__':
    app.run(debug=True)
