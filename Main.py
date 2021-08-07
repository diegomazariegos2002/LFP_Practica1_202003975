#importando la librería para leer archivos.
from os import error
from tkinter import filedialog, Tk
import sys
from tkinter.constants import FALSE, FIRST

listaCaracteres = []
reporte = ''''''
nombreCurso=""
lista_Estudiantes_Punteos = []
lista_Parametros = []

#====================================Declarando función para abrir un archivo========================================
def abrirArchivo():
    Tk().withdraw()
    archivo = filedialog.askopenfile(
        title = "Seleccionar un archivo LFP",
        initialdir = "./",
        filetypes= (
            ("archivos LFP", "*.lfp"),
            ("todos los archivos", "*.*")
        )
    )
    if archivo is None:
        print('No se seleccionó ningun archivo\n')
        return None
    else:
        texto = archivo.read()
        archivo.close()
        print('Lectura exitosa\n')
        return texto

#Función que se encarga de leer la lista de caracteres extraída del documento y asignar los valores a cada variable 
#del nombre del curso, de la lista de estudiantes y de la lista de parametros.
def asignacion_Variables(listaCaracteres):
    #Se declaran las variables globales ya que en python una variable siempre se considera local de forma predeterminada
    #Entonces le decimos al programa que la variables son de ámbito global.
    global nombreCurso
    global lista_Estudiantes_Punteos
    global lista_Parametros
    
    nombreCurso = ""
    lista_Estudiantes_Punteos = []
    lista_Parametros = []
    contador = 0
    nombreEntreComillas = False
    punteoEntreSignos = False
    nombreEstudiante = ""
    punteoEstudiante = ""
    inicioParametros = False
    parametro = ""

    #Recorrido para el nombre del Curso
    for elemento in listaCaracteres:
        #Hasta que no se encuentre el signo igual se agregaran los caracteres encontrados a nombreCurso.
        if elemento[0] is not str("="):
            contador = contador + 1
            nombreCurso = nombreCurso + elemento[0]
        #Cuando se encuentre el signo "=" se eleminaran los caracteres del nombre del curso.
        else:
            while(contador >= 0):
                contador = contador - 1
                del listaCaracteres[0]
            break
    contador = 0
    #Recorrido para los estudiantes y sus punteos
    for elemento in listaCaracteres:
        contador += 1
        #extrayendo el nombre del estudiante
        if elemento[0] is str('"') and nombreEntreComillas == False:
            nombreEntreComillas = True
        elif elemento[0] is str('"') and nombreEntreComillas == True:
            nombreEntreComillas = False  
        elif nombreEntreComillas == True:
            nombreEstudiante = nombreEstudiante + elemento[0]
        #Extrayendo el punteo del estudiante
        if elemento[0] is str(';'):
            punteoEntreSignos = True
        elif elemento[0] is str(">"):
            punteoEntreSignos = False
            lista_Estudiantes_Punteos.append([nombreEstudiante, float(punteoEstudiante)])
            nombreEstudiante=""
            punteoEstudiante = ""         
        elif punteoEntreSignos == True:
            punteoEstudiante = punteoEstudiante + elemento[0]
        #Extrayendo los parametros
        if elemento[0] is str(',') and inicioParametros == True:
            lista_Parametros.append(parametro)
            parametro=""
        elif inicioParametros == True:
            parametro = parametro + elemento[0]
        if elemento == listaCaracteres[-1] and inicioParametros == True and contador >= len(listaCaracteres):
            lista_Parametros.append(parametro)
            parametro=""
        if elemento[0] is str('}'):
            inicioParametros = True
    
#==========================================Crear estructura reporte===================================================    
def crearReporte():
    global nombreCurso
    global lista_Estudiantes_Punteos
    global lista_Parametros
    global reporte

    #Inicio del reporte
    reporte = f'''                                              ========REPORTE DEL CURSO========
                                            Nombre del curso: {nombreCurso}
                                            Número de estudiantes en el curso: {len(lista_Estudiantes_Punteos)}
                                    ----------Listado de Estudiantes en el curso----------'''
    for i in lista_Estudiantes_Punteos:
        reporte += "\n" + f'''                                                       {i[0]}'''
    #Parte de los parametros
    reporte += "\n" + "                                      -------------Operaciones requeridas-------------"
    for i in lista_Parametros:
        if i == "ASC":
            reporte += "\n"+"Lista ordenada de forma ascendente"
            for i in asc(lista_Estudiantes_Punteos):
                reporte += "\n" + f"    Estudiante: {i[0]} punteo {i[1]}"
            reporte += "\n" + "--------------------------------------------"
        if i == "DESC":
            reporte += "\n" + "Lista ordenada de forma descendente"
            for i in desc(lista_Estudiantes_Punteos):
                reporte += "\n" + f"    Estudiante: {i[0]} punteo {i[1]}"
            reporte += "\n" + "--------------------------------------------"
        if i == "AVG":
            reporte += "\n" + f"    El promedio de las notas de todos los estudiantes es de: {avg()}"
        if i == "MIN":
            reporte += "\n" + f"    La nota mínima del curso es: {min()[1]} y el estudiante con esa nota es: {min()[0]}"
        if i == "MAX":
            reporte += "\n" + f"    La nota máxima del curso es: {max()[1]} y el estudiante con esa nota es: {max()[0]}"
        if i == "APR":
            reporte += "\n" + f"    El número de estudiantes que aprobaron es de: {apr()} "
        if i == "REP":
            reporte += "\n" + f"    El número de estudiantes que reprobaron es de: {rep()}"

#==========================================Funciones de los parametros===================================================

#Función para obtener el número de estudiantes aprobados en el curso
def apr():
    global lista_Estudiantes_Punteos
    conteoAprobados = 0
    for i in lista_Estudiantes_Punteos:
        if i[1] >= 61:
            conteoAprobados+=1
    return conteoAprobados

#Función para obtener el número de estudiantes reprobados en el curso
def rep():
    global lista_Estudiantes_Punteos
    conteoReprobados = 0
    for i in lista_Estudiantes_Punteos:
        if i[1] < 61:
            conteoReprobados+=1
    return conteoReprobados

#Función del promedio de notas
def avg():
    global lista_Estudiantes_Punteos
    sumaPunteos = 0
    for i in lista_Estudiantes_Punteos:
        sumaPunteos += i[1]
    promedioNotas = sumaPunteos/len(lista_Estudiantes_Punteos)
    return promedioNotas

#Función para obtener la nota mínima de los estudiantes del curso
def min():
    global lista_Estudiantes_Punteos
    notaMinima = []
    numero = lista_Estudiantes_Punteos[0][1] 
    for i in lista_Estudiantes_Punteos:
        if numero >= i[1]:
            numero = i[1]
            notaMinima = i
    return(notaMinima)

#Función para obtener la nota máxima de los estudiantes del curso
def max():
    global lista_Estudiantes_Punteos
    notaMaxima = []
    numero = lista_Estudiantes_Punteos[0][1] 
    for i in lista_Estudiantes_Punteos:
        if numero <= i[1]:
            numero = i[1]
            notaMaxima = i
    return(notaMaxima)

#Función para ordenar ascendentemente la lista de estudiantes
def asc(lista):
    izquierda = []
    centro = []
    derecha = []
    if len(lista) > 1:
        pivote = lista[0][1]
        for i in lista:
            if i[1] < pivote:
                izquierda.append(i)
            elif i[1] == pivote:
                centro.append(i)
            elif i[1] > pivote:
                derecha.append(i)
        #print(izquierda+["-"]+centro+["-"]+derecha)
        return asc(izquierda)+centro+asc(derecha)
    else:
        return lista
    
#Función para ordenar descendentemente la lista de estudiantes
def desc(lista):
    izquierda = []
    centro = []
    derecha = []
    if len(lista) > 1:
        pivote = lista[0][1]
        for i in lista:
            if i[1] > pivote:
                izquierda.append(i)
            elif i[1] == pivote:
                centro.append(i)
            elif i[1] < pivote:
                derecha.append(i)
        #print(izquierda+["-"]+centro+["-"]+derecha)
        return desc(izquierda)+centro+desc(derecha)
    else:
        return lista

#==========================================REPORTE EN HTML==========================================================

#Función para crear un reporte del curso en formato html 
def crearReporteHTML():
    global nombreCurso
    global lista_Estudiantes_Punteos
    global lista_Parametros

    reporteHtml = '''<!doctype html>
        <html lang="en">

        <head>
        <!-- Required meta tags -->
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <!-- Bootstrap CSS -->
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">

        <title>Reporte del curso</title>
        </head>

        <body style="background-color: lightseagreen;">
        <div class="container-fluid container p-3 my-3 bg-dark text-white">
        <div class="row">
        <div class="col-12" style="text-align: center; ">
            <h1>REPORTE DEL CURSO</h1>
        </div>
        </div>
        </div>
        <div class="container-fluid" style="background-color: rgb(255, 255, 255);">
        <div class="row justify-content-md-center">
        <div>
            <h3>Nombre del curso: '''
    reporteHtml += nombreCurso
    reporteHtml += '''</h3>
      </div>
        </div>
        <div class="row justify-content-md-center">
      <div>
        <h3>Numero de estudiantes en el curso: '''
    reporteHtml += str(len(lista_Estudiantes_Punteos))
    reporteHtml += '''</h3>
      </div>
     </div>
     <div class="row justify-content-md-center">
      <div class="col-md-auto">
        <h2 style="text-decoration: underline tomato;">Listado de estudiantes</h2>
      </div>
        </div>
        <div class="row justify-content-md-center">
      <div class="col-md-auto">
        <table class="table table-bordered table-striped text-center table-hover table-responsive"
          style="text-align: center; width: 600px;">
          <thead>
            <tr class="table-dark">
              <th>#</th>
              <th>Estudiante</th>
              <th>Punteo</th>
            </tr>
          </thead>
          <tbody>'''

    contador = 1
    for i in lista_Estudiantes_Punteos:
        if i[1] >= 61:
            reporteHtml += f'''<tr>
            <td class="table-success">{contador}</td>
            <td class="table-success">{i[0]}</td>
            <td class="table-info">{i[1]}</td>
            </tr>'''
        else:
            reporteHtml += f'''<tr>
            <td class="table-success">{contador}</td>
            <td class="table-success">{i[0]}</td>
            <td class="table-danger">{i[1]}</td>
            </tr>'''
        contador += 1

    reporteHtml += '''
          </tbody>
        </table>
      </div>
     </div>
     <div class="row justify-content-md-center">
      <div class="col-md-auto">
        <h2 style="text-decoration: underline tomato;">Operaciones solicitadas</h2>
      </div>
        </div>
        '''
    for i in lista_Parametros:
        if i == "ASC":
            reporteHtml += '''<div class="row justify-content-md-center">
            <div class="col-md-auto">
            <h2 style="text-decoration: underline slateblue;">Listado de estudiantes de forma ascendente</h2>
             </div>
            </div>
            <div class="row justify-content-md-center">
            <div class="col-md-auto">
            <table class="table table-bordered table-striped text-center table-hover table-responsive"
            style="text-align: center; width: 600px;">
            <thead>
            <tr class="table-dark">
              <th>#</th>
              <th>Estudiante</th>
              <th>Punteo</th>
            </tr>
          </thead>
          <tbody>'''

            contador = 1
            for i in asc(lista_Estudiantes_Punteos):
                if i[1] >= 61:
                    reporteHtml += f'''<tr>
                <td class="table-success">{contador}</td>
                <td class="table-success">{i[0]}</td>
                <td class="table-info">{i[1]}</td>
                </tr>'''
                else:
                    reporteHtml += f'''<tr>
                <td class="table-success">{contador}</td>
                <td class="table-success">{i[0]}</td>
                <td class="table-danger">{i[1]}</td>
                </tr>'''
                contador += 1

            reporteHtml += '''
             </tbody>
                </table>
                </div>
                </div>'''                
        if i == "DESC":
            reporteHtml += '''<div class="row justify-content-md-center">
            <div class="col-md-auto">
            <h2 style="text-decoration: underline slateblue;">Listado de estudiantes de forma descendente</h2>
            </div>
            </div>
            <div class="row justify-content-md-center">
            <div class="col-md-auto">
            <table class="table table-bordered table-striped text-center table-hover table-responsive"
            style="text-align: center; width: 600px;">
            <thead>
            <tr class="table-dark">
              <th>#</th>
              <th>Estudiante</th>
              <th>Punteo</th>
            </tr>
          </thead>
          <tbody>'''

            contador = 1
            for i in desc(lista_Estudiantes_Punteos):
                if i[1] >= 61:
                    reporteHtml += f'''<tr>
            <td class="table-success">{contador}</td>
            <td class="table-success">{i[0]}</td>
            <td class="table-info">{i[1]}</td>
            </tr>'''
                else:
                    reporteHtml += f'''<tr>
            <td class="table-success">{contador}</td>
            <td class="table-success">{i[0]}</td>
            <td class="table-danger">{i[1]}</td>
            </tr>'''
                contador += 1

            reporteHtml += '''
          </tbody>
            </table>
            </div>
            </div>'''
        if i == "AVG":
            reporteHtml += "\n" + f'''    <div class="row justify-content-md-center">
            <div>
            <h3>El promedio de las notas de todos los estudiantes es de: {avg()}</h3>
            </div>
            </div>'''
        if i == "MIN":
            reporteHtml += "\n" + f'''    <div class="row justify-content-md-center">
            <div>
            <h3>La nota minima del curso es: {min()[1]} y el estudiante con esa nota es: {min()[0]}</h3>
            </div>
            </div> '''
        if i == "MAX":
            reporteHtml += "\n" + f'''    <div class="row justify-content-md-center">
            <div>
            <h3>La nota maxima del curso es: {max()[1]} y el estudiante con esa nota es: {max()[0]}</h3>
            </div>
            </div> '''
        if i == "APR":
            reporteHtml += "\n" + f'''    <div class="row justify-content-md-center">
            <div>
            <h3>El numero de estudiantes que aprobaron es de: {apr()}</h3>
            </div>
            </div>  '''
        if i == "REP":
            reporteHtml += "\n" + f'''    <div class="row justify-content-md-center">
            <div>
            <h3>El numero de estudiantes que reprobaron es de: {rep()}</h3>
            </div>
            </div>'''
    reporteHtml += '''
        </div>
        <div class="container-fluid container p-3 my-3 bg-dark text-white">
        <div class="row">
        <div class="col-12" style="text-align: center; ">
        <h1></h1>
        </div>
        </div>
        </div>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM"
        crossorigin="anonymous"></script>
        </body>

        </html>'''
    archivo = open("Reporte del curso.html","w")
    archivo.write(reporteHtml)
    archivo.close()

#======================================================FUNCIÓN MAIN==================================================
#Programa de inicio
if __name__ == "__main__":
    while(True):
        #imprimiendo el menú.
        print("Bienvenido Usuario")
        print('''===================MENÚ=================
        1. Cargar archivo
        2. Mostrar reporte en consola
        3. Exportar reporte
        4. Salir
===================MENÚ=================''')
        #verificando que opción se escogió.
        try:
            opcion = int(input("Escoga una opción para continuar: "))
            if opcion == 1:
                listaCaracteres = []

                print("usted ha escogido la opción 1 Cargar archivo.")
                input("Presione Enter para continuar....")
                #Parte de la lectura del archivo.
                txt = abrirArchivo()
                palabraEntreComillas = False
                if txt is not None: 
                    #print(txt)
                    if(len(txt) > 0):
                        for c in txt:
                            if c == '\n':
                                #Se ignora este caracter
                                    #print(str(ord(c)) + ' - \\n')
                                pass
                            elif c == '"' and palabraEntreComillas == False:
                                auxL = [str(c)]
                                listaCaracteres.append(auxL)
                                #Si no se tiene una palabra entre comillas y aparece una comilla quiere decir
                                #que se esta empezando una palabra entre comillas.
                                palabraEntreComillas = True
                            
                            elif c == '"' and palabraEntreComillas == True:
                                auxL = [str(c)]
                                listaCaracteres.append(auxL)
                                #Si se tiene una palabra entre comillas y aparece una comilla quiere decir
                                #que se esta terminando una palabra entre comillas
                                palabraEntreComillas = False

                            elif c == ' ' and palabraEntreComillas == False:
                                #Se ignora este caracter siempre y cuando no se tenga una palabra entre comillas
                                    #print(str(ord(c)) + ' - `space`')
                                pass
                            else:
                                auxL = [str(c)]
                                listaCaracteres.append(auxL)
                        asignacion_Variables(listaCaracteres)
                        crearReporte()
                        input("Presione Enter para continuar....")
                    else:
                        print('No hay texto para analizar\n')
                else:
                    print('No se pudo analizar la entrada\n')
            elif opcion == 2:
                print("usted ha escogido la opción 2 Mostrar reporte en consola.")
                print(reporte)
                input("Presione Enter para continuar....")
            elif opcion == 3:
                print("usted ha escogido la opción 3 Exportar reporte.")
                crearReporteHTML()
                print("Exportación realizada con éxito!!!")
                input("Presione Enter para continuar....")
            elif opcion == 4:                
                print("usted ha escogido la opción 4 Salir.")
                input("Presione Enter para salir....")
                break
            else:
                print("Ingrese una opción válida del menú.")
                input("Presione Enter para continuar....")
        except Exception as e:
            print(f"Error ingrese una opción válida (número) {e}")
            print("Error inesperado:", sys.exc_info()[0])
            input("Presione Enter para continuar....")

