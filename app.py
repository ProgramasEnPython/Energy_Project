from flask import Flask, render_template, request, send_file, url_for
import matplotlib.pyplot as plt
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import atexit
import shutil
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Diccionario con consumo energético estimado en kWh por electrodoméstico
appliance_energy = {
"refrigerador": 600,
"televisor": 200,
"lavadora": 300,
"microondas": 100,
"Computador": 300,
"Lamparas": 200
}

"""
-Define la ruta de la página principal (raíz) de la aplicación web.
-Cuando un usuario visita esa ruta, se ejecuta la función index(), que renderiza y devuelve el 
contenido del archivo index.html como respuesta.
"""
@app.route('/')
def index():
return render_template('index.html')

@app.route('/consumo')
def consumo():
return render_template('consumo.html')

@app.route('/nosotros')
def nosotros():
return render_template('s_nosotros.html')

@app.route('/proveedores')
def proveedores():
return render_template('proveedores.html')


@app.route('/calcular', methods=['POST'])
def calcular():
appliances = request.form.getlist('appliance[]') #obtiene la lista de electrodomésticos seleccionados
quantities = request.form.getlist('quantity[]')  #obtiene la lista de cantidades correspondientes a cada electrodoméstico.
email = request.form['email']
department = request.form['department']
region = request.form['region']

total_energy = 0        #Para almacenar el consumo total de energía
appliance_data = []     #Para almacenar la energía consumida por cada electrodoméstico.

# Procesar cada electrodoméstico
for appliance, quantity in zip(appliances, quantities): #Se itera sobre las listas de electrodomésticos y sus cantidades usando zip()
    quantity = int(quantity)                            #Para cada electrodoméstico, se convierte la cantidad a un entero, se calcula su consumo energético llamando a la función calculate_energy(), y se acumula el consumo total en total_energy.
    energy = calculate_energy(appliance, quantity)
    total_energy += energy
    appliance_data.append((appliance, energy))          #La información de cada electrodoméstico se agrega a la lista appliance_data

filename = generate_chart(appliance_data)               #Se llama a la función generate_chart() para generar un gráfico basado en los datos de consumo de los electrodomésticos, y se almacena el nombre del archivo generado.

chart_url = url_for('output_file', filename=filename) #Se utiliza url_for() para crear una URL que apunta a la ruta que servirá el gráfico generado. Esto permite que la plantilla resultados.html acceda a la imagen.

send_email(email, appliance_data, total_energy, department, region)  #Se llama a la función send_email() para enviar un correo electrónico con los resultados del consumo energético y la información adicional.

""" Finalmente, se renderiza la plantilla resultados.html, pasando el consumo total de energía, la lista
    de datos de electrodomésticos y la URL del gráfico como parámetros. Esto permite que la plantilla 
    muestre los resultados al usuario."""
return render_template('resultados.html', total_energy=total_energy, appliance_data=appliance_data, chart_url=chart_url)


def calculate_energy(appliance, quantity):
"""Calcula el consumo energético en kWh basado en el electrodoméstico y su cantidad."""
return appliance_energy.get(appliance, 0) * quantity

def send_email(to_email, appliance_data, total_energy, department, region):
"""Envía un correo electrónico con el resultado del consumo energético."""
from_email = "ponercorreo@gmail.com"
from_password = "ponercontraseña"

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

# msg.attach(MIMEText(body, 'plain'))

try:
    #Crea una instancia del objeto SMTP que se conecta al servidor SMTP de Gmail en el puerto 587,
    #que es el puerto utilizado para la comunicación segura a través de TLS (Transport Layer Security)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    #Inicia la conexión segura utilizando el protocolo TLS. Esto cifra la comunicación entre el cliente y el servidor
    server.starttls()
    #Inicia sesión en el servidor SMTP utilizando las credenciales proporcionadas
    server.login(from_email, from_password)
    server.sendmail(from_email, to_email, msg.as_string())
    #Cierra la conexión con el servidor SMTP.
    server.quit()
    print("Correo enviado exitosamente!")
except Exception as e:
    print(f"Error al enviar el correo: {e}")


"""
La función generate_chart() toma un argumento appliance_data, que es una lista de tuplas. 
Cada tupla contiene el nombre de un electrodoméstico y su correspondiente consumo de energía.
"""
def generate_chart(appliance_data):
"""
Aquí se utilizan comprensiones de listas para extraer los nombres de los electrodomésticos y sus
consumos de energía en dos listas separadas: appliances y energies.
"""
appliances = [appliance for appliance, energy in appliance_data]
energies = [energy for appliance, energy in appliance_data]
"""
Se establece el estilo del gráfico como 'ggplot'.
Se configura el tamaño de la figura del gráfico a 8 pulgadas de ancho y 6 pulgadas de alto.
Se crea el gráfico de barras utilizando plt.bar(), donde los nombres de los electrodomésticos se usan 
como etiquetas del eje X y sus consumos de energía como valores del eje Y.
Las barras tienen un color azul claro (#3498db), con un borde negro y un grosor de línea de 1.5.
"""
plt.style.use('ggplot')
plt.figure(figsize=(8, 6))
bars = plt.bar(appliances, energies, color='#3498db', edgecolor='black', linewidth=1.5)

#Se añaden etiquetas a los ejes X e Y y un título al gráfico, con tamaños de fuente específicos.
plt.xlabel('Electrodoméstico', fontsize=14)
plt.ylabel('Consumo en kWh', fontsize=14)
plt.title('Consumo Energético', fontsize=16, fontweight='bold')

"""
Para cada barra, se obtiene su altura (yval), y se coloca un texto sobre la barra que muestra el valor 
del consumo en kWh.
"""
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, yval, f'{yval:.0f} kWh', va='bottom', ha='center', fontsize=14,
                color='black')

#Se establece el límite superior del eje Y para que sea un 20% mayor que el consumo máximo,
# lo que proporciona un espacio adicional en la parte superior del gráfico.
plt.ylim(0, max(energies) * 1.2)
#Se añade una cuadrícula horizontal al gráfico para facilitar la lectura de los valores.
plt.grid(axis='y', linestyle='--', alpha=0.7)


#Si no existe el directorio output, se crea.
#Se define el nombre del archivo para guardar el gráfico.
#Se utiliza plt.savefig() para guardar el gráfico en un archivo con una resolución de 300 dpi y
#ajustando los márgenes.
#Después de guardar el gráfico, se cierra la figura con plt.close() para liberar memoria.
if not os.path.exists('output'):
    os.makedirs('output')

# Generar un UUID para el nombre del archivo
unique_id = str(uuid.uuid4())
filename = f'consumo_{unique_id}.png'  # Nombre único con UUID
filepath = os.path.join('output', filename)
plt.savefig(filepath, dpi=300, bbox_inches='tight')
plt.close()
print(f"Gráfico guardado en {filepath}")

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

#Función para borrar el directorio 'output'
def clean_output_directory():
if os.path.exists('output'):
    shutil.rmtree('output')
    print("El directorio 'output' ha sido eliminado.")

#Registrar la función para que se ejecute al cerrar la app
atexit.register(clean_output_directory)

#Inicia la aplicación Flask
if __name__ == '__main__':
app.run(debug=True)
