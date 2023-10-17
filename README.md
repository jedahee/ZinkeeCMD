# Zinkee CMD
Versión de Zinkee en CMD para desarrolladores. Una nueva forma sencilla de gestionar Zinkee  a través de la consola de Windows.
![image](https://github.com/jedahee/ZinkeeCMD/assets/56111700/1e218c29-be5c-4740-8376-1a42a57e0ac8)

## Documentación
Zinkee CMD se encarga de ofrecer útiles funcionalidades para aplicar en Zinkee a través de Web Scraping, algunas de estas funcionalidades son:

1. **Listar registros**: Puedes listar tus últimos registros añadidos, o listar los registros a través de un filtro
2. **Añadir registro**: Puedes añadir un registro en Zinkee de una forma más sencilla a través de esta opción
3. **Añadir día de registros automaticamente**: En Zinkee CMD hay opciones de configuración, una de estas son las horas en las que trabajas y descansas. Pues, esta opción añade los registros automaticamente hasta completar el día (solo debes introducir el nombre de la tarea y el proyecto), fijandose en las horas añadidas a la configuración
4. **Copiar registros de un día añadido a lo largo de la semana**: Lista los registros de los últimos 7 días, ordenados por día, seleccionamos un día de los mostrados y Zinkee CMD copiará los registros de ese día seleccionada y los añadirá al día de hoy.
5. **Configurar opciones**: Puedes configurar diferentes opciones de Zinkee CMD (Nombre de usuario de Zinkee, Hora de descanso, Hora de salida...)

(Zinkee CMD inicia sesión automáticamente usando las credenciales guardadas en tu configuración)

## Pasos a seguir para usar Zinkee CMD

Para poder usar Zinkee CMD correctamente debes seguir los siguientes pasos:

1. Debes tener [Python 3](https://www.python.org/downloads/) instalado previamente en tu ordenador.
2. Debes clonar el proyecto Zinkee CMD en la ruta que quieras de tu Ordenador (Si tienes Git puedes usar el comando "git clone https://github.com/jedahee/ZinkeeCMD.git")
3. Ahora, debemos ejecutar el siguiente comando dentro de la carpeta clonada (dentro de tu_ruta_de_window/Zinkee CMD/ ):
   - **pip install -r requirements.txt**
4. Una vez instalado todos los requerimientos, debemos visualizar una carpeta llamada 'chromedriver', en esta carpeta debe ir el driver de chrome (chromedriver.exe) para que el Web Scraping funcione.
   La versión del chromedriver.exe puede variar dependiendo de la versión de Chrome que tengamos.

   Si tienes la versión de Chrome 115 o una más nueva debes pulsar sobre [el siguiente enlace](https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/118.0.5993.70/win64/chromedriver-win64.zip) para descargar Chromedriver.exe
  
   Si tienes una versión de Chrome menor a la 115 puedes descargar Chromedriver.exe desde [el siguiente enlace](https://chromedriver.chromium.org/downloads)
   ![image](https://github.com/jedahee/ZinkeeCMD/assets/56111700/deb8d77b-047d-4bc1-b0bf-b9571dbd3af8)

   Ahora, una vez tengamos descargado y ubicado chromdriver.exe, debemos moverlo dentro de la carpeta chromedriver/ (Quedando así "tu_ruta_de_window/Zinkee CMD/chromedriver/chromedriver.exe").

5. Solo nos faltaría volver a la ruta padre (a .../Zinkee CMD/), donde vemos el archivo 'main.py' y 'config.py', para ejecutar Zinkee CMD, en esta misma ruta, abre la consola y pon:
   - **python main.py** (Siempre ejecutar el archivo main.py)

Una vez hecho todos los pasos,

¡Puedes usar Zinkee CMD!

## Recomendaciones
No es recomendable activar el guardado de cookies dentro de Zinkee CMD, ya que Zinkee no guarda tus credenciales en las cookies y no te ayuda a iniciar sesión mas rápido.
De hecho, ralentiza el proceso para nada. 
Por defecto, esta función viene desactivada.

## Limitaciones
- Solo se puede usar ZinkeeCMD si tienes el navegador **Chrome** (Cualquier versión)
- Solo se puede usar ZinkeeCMD si tienes el sistema operativo **Windows** (Cualquier versión)
  
