#importando la librería para leer archivos.
from tkinter import filedialog, Tk

listaT=[]

#declarando función para abrir un archivo.
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

if __name__ != '__main__':
    print(f"Se esta ejecutando una librería no el programa principal")
else:
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
                    #Si no se tiene una palabra entre comillas y aparece una comilla quiere decir
                    #que se esta empezando una palabra entre comillas.
                    palabraEntreComillas = True
                
                elif c == '"' and palabraEntreComillas == True:
                    #Si se tiene una palabra entre comillas y aparece una comilla quiere decir
                    #que se esta terminando una palabra entre comillas
                    palabraEntreComillas = False

                elif c == ' ' and palabraEntreComillas == False:
                    #Se ignora este caracter siempre y cuando no se tenga una palabra entre comillas
                        #print(str(ord(c)) + ' - `space`')
                    pass
                else:
                    auxL = [ord(c), str(c)]
                    listaT.append(auxL)
            for elemento in listaT:
                print('Ascii: ' + str(elemento[0]) + ' - Caracter: ' + str(elemento[1]))
        else:
            print('No hay texto para analizar\n')
    else:
        print('No se pudo analizar la entrada\n')