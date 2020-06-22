import PySimpleGUI as sg 
import random

# {---------------------------------------------------------------------------------}
# {------------------------------ CLASE CASILLA ------------------------------------}
# {---------------------------------------------------------------------------------}

class Casilla():
    def __init__(self, contenido='', tamaño=None, color='#FFFFFF', clave=None, ocupado=False):
        self._contenido = contenido
        self._tamaño = tamaño
        self._color = color
        self._key = clave
        self._ocupado = ocupado
        self._diseño = sg.Button(self._contenido,key=self._key, pad=(0,0), size=self._tamaño, button_color=('black',self._color),disabled_button_color=('black',self._color), disabled=self._ocupado)

    def getKey(self):
        return self._key

    def getDiseño(self):
        return self._diseño

    def habilitar(self):
        self._ocupado = False

    def deshabilitar(self):
        self._ocupado = True

    def setContenido(self,dato):
        self._contenido = dato
    
    def setColor(self,color):
        self._color = color

# {---------------------------------------------------------------------------------}
# {------------------------------ CLASE TABLERO ------------------------------------}
# {---------------------------------------------------------------------------------}

class Tablero:
    def __init__(self,tamaño=0,casilas_especiales=None):
        self._tamaño = tamaño
        self._casillas_especiales = casilas_especiales
        self._lista_casillas = []
        self._layout = self._armar()
          
    def getLayout(self):
        return self._layout

    def getKeysCasillas(self):
        lista_keys = []
        for casilla in self._lista_casillas:
            lista_keys.append(casilla.getKey())
        return lista_keys

    def _armar(self):
        layout = [] 
        for i in range(1, self._tamaño + 1):
            fila_casillas = []
            for j in range(1, self._tamaño + 1):
                especial = False
                key = str(i)+"-"+str(j)
                for clave in self._casillas_especiales:
                    if(key in self._casillas_especiales[clave][0]):
                        casilla = Casilla(clave=key,tamaño=(3,1), contenido=clave, color=self._casillas_especiales[clave][1], ocupado=True) #casilla especial
                        especial = True
                if not especial:
                    casilla = Casilla(clave=key,tamaño=(3,1), ocupado=True) #casilla normal
                fila_casillas.append(casilla.getDiseño())
                self._lista_casillas.append(casilla)  
            layout.append(fila_casillas)
        return layout

    def habilitar(self, pantalla_juego):
        for casilla in self._lista_casillas:
            pantalla_juego[casilla.getKey()].Update(disabled=False)
            casilla.habilitar()
    
    def deshabilitar(self, pantalla_juego):
        for casilla in self._lista_casillas:
            pantalla_juego[casilla.getKey()].Update(disabled=True)
            casilla.deshabilitar()

    def insertar(self,dato,key,pantalla_juego):
        pantalla_juego[key].Update(dato, button_color=('white','#684225'), disabled_button_color=('white','#684225'))
        aux = key.split('-')
        self._lista_casillas[((int(aux[1])-1)+(int(aux[0])-1)*self._tamaño)].setContenido(dato)
        self._lista_casillas[((int(aux[1])-1)+(int(aux[0])-1)*self._tamaño)].setColor('#684225')

# {---------------------------------------------------------------------------------}
# {--------------------------- CLASE FILA DE FICHAS --------------------------------}
# {---------------------------------------------------------------------------------}

class FilaFichas():
    def __init__(self, cant_fichas=7, key_add=None, letras=None):
        self._cant_fichas = cant_fichas
        self._key_add = key_add
        self._letras = letras 
        self._ficha_selected = [False,None]
        self._fila_fichas = []
        self._layout = self._armar() 
        
    def _armar(self):
        layout = []
        for i in range(1,8):
            key = self._key_add +'-'+ str(i)
            if (self._key_add == 'FJ'):
                ficha = Casilla(clave=key, tamaño=(6,2),contenido=self._letras[i-1]) # fichas del jugador
            else:
                ficha = Casilla(clave=key, tamaño=(6,2), ocupado=True) # fichas de la maquina
            self._fila_fichas.append(ficha)
            layout.append(ficha.getDiseño())     
        return [layout]
    
    def habilitarFila(self, pantalla_juego):
        for ficha in self._fila_fichas:
            pantalla_juego[ficha.getKey()].Update(disabled=False)
            ficha.habilitar()

    def deshabilitarFila(self, pantalla_juego):
        for ficha in self._fila_fichas:
            pantalla_juego[ficha.getKey()].Update(disabled=True)
            ficha.deshabilitar()

    def deshabilitarFicha(self, pantalla_juego):
        pantalla_juego[self._ficha_selected[1]].Update('', disabled=True,button_color=('black','#CCCCCC'))
        aux = self._ficha_selected[1].split('-')
        self._fila_fichas[int(aux[1])-1].deshabilitar()
        self._fila_fichas[int(aux[1])-1].setColor('#CCCCCC')

    def getLayout(self):
        return self._layout

    def getKeysFila(self):
        lista_keys = []
        for ficha in self._fila_fichas:
            lista_keys.append(ficha.getKey())
        return lista_keys

    def marcarFichaSelected(self,pantalla_juego,key):
        self._ficha_selected[0] = True
        self._ficha_selected[1] = key       
        aux = key.split('-')
        self._fila_fichas[int(aux[1])-1].setColor("#5fefaa")
        pantalla_juego[key].Update(button_color=('black',"#5fefaa"))

    def desmarcarFichaSelected(self,pantalla_juego):
        pantalla_juego[self._ficha_selected[1]].Update(button_color=('black','white'))
        aux = self._ficha_selected[1].split('-')
        self._fila_fichas[int(aux[1])-1].setColor("white")
        self._ficha_selected[0] = False

    def hayFichaSelected(self):
        return self._ficha_selected[0]

    def getFichaSelected(self):
        return self._ficha_selected[1]



# {---------------------------------------------------------------------------------}
# {--------------------------- CLASE BOLSA DE FICHAS -------------------------------}
# {---------------------------------------------------------------------------------}

class BolsaFichas():
    def __init__(self, bolsa_fichas):
        self._bolsa_fichas = bolsa_fichas

    def letras_random(self, cantidad):
        letras = list(self._bolsa_fichas.keys())
        string_letras=''
        for i in letras:
            string_letras=string_letras+(i*self._bolsa_fichas[i]['cantidad'])
        lista_letras=[]
        for x in range(0,cantidad):
            letra_elegida = random.choice(string_letras)
            lista_letras.append(letra_elegida)
            self._bolsa_fichas[letra_elegida]['cantidad']=self._bolsa_fichas[letra_elegida]['cantidad']-1
        return lista_letras
    
    


        
