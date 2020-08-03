def guardar_partida(datos):
    import pickle
    import os
    dir_actual = os.getcwd()
    ubicacion_archivo = (dir_actual+'\\Data\\Files\\'+'partidaguardada.obj')
    f = open(ubicacion_archivo,'wb')
    pickle.dump(datos,f)
    f.close()

def hay_partida_guardada():
    import pickle
    import os
    dir_actual = os.getcwd()
    ubicacion_archivo = (dir_actual+'\\Data\\Files\\'+'partidaguardada.obj')
    f = open(ubicacion_archivo,'rb')
    datos = pickle.load(f)
    f.close()
    return datos[0]

def obtener_datos():
    import pickle
    import os
    dir_actual = os.getcwd()
    ubicacion_archivo = (dir_actual+'\\Data\\Files\\'+'partidaguardada.obj')
    f = open(ubicacion_archivo,'rb')
    datos = pickle.load(f)
    nivel = datos.pop()
    f.close()
    return [nivel,datos]

def continuar_partida():
    from Windows import windowPartidaGuardada

    window = windowPartidaGuardada.hacer_ventana()
    event, values = window.read()
    continuar = event == '-SI-'
    window.close()

    return continuar

def eliminar_partida():
    import pickle
    import os
    dir_actual = os.getcwd()
    ubicacion_archivo = (dir_actual+'\\Data\\Files\\'+'partidaguardada.obj')
    f = open(ubicacion_archivo,'wb')
    pickle.dump([False],f)
    f.close()


