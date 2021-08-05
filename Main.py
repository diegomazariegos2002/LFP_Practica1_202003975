#importando la librería para leer archivos.
from os import error
from tkinter import filedialog, Tk
import sys
from tkinter.constants import FALSE, FIRST

listaCaracteres = []
reporte = ""

#Declarando función para abrir un archivo.
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

#Creación del reporte
def crearReporte(listaCaracteres):
    nombreCurso = ""
    contador = 0
    lista_Estudiantes_Punteos = []
    nombreEntreComillas = False
    punteoEntreSignos = False
    nombreEstudiante = ""
    punteoEstudiante = ""
    lista_Parametros = []
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
        if elemento == listaCaracteres[-1] and inicioParametros == True:
            lista_Parametros.append(parametro)
            parametro=""
        if elemento[0] is str('}'):
            inicioParametros = True
    
    print(nombreCurso)
    print(lista_Estudiantes_Punteos)
    print(lista_Parametros)

    #Manejo de parametros
        



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
                        crearReporte(listaCaracteres)
                    else:
                        print('No hay texto para analizar\n')
                else:
                    print('No se pudo analizar la entrada\n')
            elif opcion == 2:
                print("usted ha escogido la opción 2 Mostrar reporte en consola.")
                input("Presione Enter para continuar....")
            elif opcion == 3:
                print("usted ha escogido la opción 3 Exportar reporte.")
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
            input("Presione Enter para continuar....")

