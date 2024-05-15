import numpy as np
import matplotlib.pyplot as plt
from GeneticAlgorithm import AlgoritmoGenetico


# declaramos la matriz interna
matriz_interna = np.empty((4, 4), dtype=object)



num_chromosomes = 4#numero de cromosomas de la matriz
max_value_verde = 0x00FF00
min_value_verde = 0x009900

array = np.array([], dtype=int)
cromosomaMutado = np.array([])
matrizGrandeFinal = [[[ [0] for k in range(1)]for j in range(5)]for i in range (5)]
matrizGrandeInicial = [[[ [0] for k in range(1)]for j in range(5)]for i in range (5)]
arrayFin = np.array([])
arrayIni = np.array([])
populationPrueba = np.array([])

 
col = 0
ren = 0
for i in range(1,26):#SE REPITE 25 QUE ES EL TOTAL DE LA MATRIZ DE 3 DIMANESIONES 5X5
    population = np.random.randint(min_value_verde, max_value_verde + 1, size=(num_chromosomes, 4))#crea la matriz 4x4 random de 4 individuos
    populationPrueba = np.array(population)
    
    ag = AlgoritmoGenetico(population)#llamo al algoritmo que se repita 25 veces con una nueva poblacion por cuadrito osea 25 veces
    
    generations = 0#el numero de generaciones que han pasado
    while True:
        #IF PARA QUE SALGA DEL WHILE DESPUES DE 50 GENERACIONES
        if generations >=50:
        #    print("No se encontró una solución satisfactoria después de " + str(i))
            break
        
        ag.run()
        
        
        generations += 1
        
    array = np.array(ag.cromosomas)
    
    
    #convierto la poblacion incial en hexadecimal
    #_----------------------------------------------------------------------------------------------
    array_hex1 = np.empty(populationPrueba.shape, dtype="<U7")
     # Recorrer el array de números enteros y convertirlos a cadenas hexadecimales
    for i in range(populationPrueba.shape[0]):
        for j in range(populationPrueba.shape[1]):
            # Convertir el número entero a una cadena hexadecimal con el prefijo "0x"
            hexa = hex(populationPrueba[i,j])
            # Eliminar el prefijo "0x" y añadir el símbolo "#" al principio
            #hexa = "#" + hexa[2:]
            hexa =  hexa[2:]
            # Rellenar con ceros a la izquierda si es necesario
            hexa = hexa.zfill(6)
            # Guardar la cadena hexadecimal en el array_hex
            hexa = "#" + hexa[0:]
            
            array_hex1[i,j] = hexa
            cromosomaInicial = np.array(array_hex1)
            #cromosomaMutado ES EL CROMOSOMA MUTADO FINAAAAL------------------------------------
            
     #_----------------------------------------------------------------------------------------------
    
    #EN ESTA PARTE CONVIERTO EL ARRAY DE ENTEROS A LOS CROMOSOMAS
    #_----------------------------------------------------------------------------------------------
    array_hex2 = np.empty(array.shape, dtype="<U7")
     # Recorrer el array de números enteros y convertirlos a cadenas hexadecimales
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            # Convertir el número entero a una cadena hexadecimal con el prefijo "0x"
            hexa = hex(array[i,j])
            # Eliminar el prefijo "0x" y añadir el símbolo "#" al principio
            #hexa = "#" + hexa[2:]
            hexa =  hexa[2:]
            # Rellenar con ceros a la izquierda si es necesario
            hexa = hexa.zfill(6)
            # Guardar la cadena hexadecimal en el array_hex
            hexa = "#" + hexa[0:]
            
            array_hex2[i,j] = hexa
            cromosomaMutado = np.array(array_hex2)
            
            
    if col < 5:
        matrizGrandeFinal[ren][col] = cromosomaMutado
        matrizGrandeInicial[ren][col] = cromosomaInicial
        col += 1
    else:
        ren += 1
        col = 0
        
        matrizGrandeFinal[ren][0] = cromosomaMutado
        matrizGrandeInicial[ren][col] = cromosomaInicial
        col += 1
        
arrayFin = np.array(matrizGrandeFinal)
arrayFin = np.reshape(arrayFin, (5,5,16))

arrayIni = np.array(matrizGrandeInicial)
arrayIni = np.reshape(arrayIni, (5,5,16))

#---------------------------------------------------------------------------------------------------
matriz_principal = np.array(arrayFin)
matriz_inicial = np.array(arrayIni)

#IMPLEMENTACION VISUAL DE LA GRAFICA EN MATLIBPLOP
# Función para dibujar una celda
def dibujar_celda(ax, x, y, color, celda):
    ax.add_patch(plt.Rectangle((x, y), celda, celda, color=color))


# Configuración de la cuadrícula
fila_principal = matriz_principal.shape[0]
columna_principal = matriz_principal.shape[1]
filas_internas = 4#matriz_interna.shape[0]
columnas_internas = 4#matriz_interna.shape[1]
tamaño_celdaPrincipal = 70
tamaño_celdaInterna = tamaño_celdaPrincipal / max(filas_internas, columnas_internas)

# Crear una figura y ejes de Matplotlib

fig, ax,  = plt.subplots()

# dibujar cuadricula principal
for fila in range(fila_principal):
    for columna in range(columna_principal):
        x_inicio = -tamaño_celdaPrincipal * columna_principal / 2 + columna * tamaño_celdaPrincipal
        y_inicio = tamaño_celdaPrincipal * fila_principal / 2 - fila * tamaño_celdaPrincipal
        # dibujar_celda(ax,x_inicio, y_inicio, "white", tamaño_celdaPrincipal)  # Colorear la celda
        #coloMatriz()
        # # Dibujar la cuadrícula interna
        posHex = 0
        for fila_inter in range(filas_internas):
            #for columna_inter in range(columnas_internas):
            for columna_inter in range(columnas_internas):
                x_inicio_interno = x_inicio - tamaño_celdaInterna / 20 + columna_inter * tamaño_celdaInterna
                y_inicio_interno = y_inicio + tamaño_celdaInterna / 20 - fila_inter * tamaño_celdaInterna

              
                # dibujar_celda(ax, x_inicio_interno, y_inicio_interno,matriz_principal[fila][fila_inter][columna_inter],
                #               tamaño_celdaInterna)  # Colorear la celda
                dibujar_celda(ax, x_inicio_interno, y_inicio_interno,matriz_principal[fila][columna][posHex],
                              tamaño_celdaInterna)  # Colorear la celda
                posHex += 1
                
          
# Configurar límites y ejes
ax.set_xlim(0, tamaño_celdaPrincipal * columna_principal)
ax.set_ylim(0, tamaño_celdaPrincipal * fila_principal * filas_internas)


# Mostrar la figura

plt.axis('equal')
plt.axis('off')  # Ocultar los ejes
plt.title('Generacion ' + str(generations ))
#plt.show()
#---------------------------------------------------------------------------------------------------
# Configuración de la cuadrícula PARA LA POBLACION INICIAL
fila_principal = matriz_inicial.shape[0]
columna_principal = matriz_inicial.shape[1]
filas_internas = 4#matriz_interna.shape[0]
columnas_internas = 4#matriz_interna.shape[1]
tamaño_celdaPrincipal = 70
tamaño_celdaInterna = tamaño_celdaPrincipal / max(filas_internas, columnas_internas)

# Crear una figura y ejes de Matplotlib

fig2, ax2 = plt.subplots()

# dibujar cuadricula principal
for fila in range(fila_principal):
    for columna in range(columna_principal):
        x_inicio = -tamaño_celdaPrincipal * columna_principal / 2 + columna * tamaño_celdaPrincipal
        y_inicio = tamaño_celdaPrincipal * fila_principal / 2 - fila * tamaño_celdaPrincipal
       
        # # Dibujar la cuadrícula interna
        posHex = 0
        for fila_inter in range(filas_internas):
            for columna_inter in range(columnas_internas):
                x_inicio_interno = x_inicio - tamaño_celdaInterna / 20 + columna_inter * tamaño_celdaInterna
                y_inicio_interno = y_inicio + tamaño_celdaInterna / 20 - fila_inter * tamaño_celdaInterna

              
                dibujar_celda(ax2, x_inicio_interno, y_inicio_interno,matriz_inicial[fila][columna][posHex],
                              tamaño_celdaInterna)  # Colorear la celda
                posHex += 1
                
            
ax2.set_xlim(0, tamaño_celdaPrincipal * columna_principal)
ax2.set_ylim(0, tamaño_celdaPrincipal * fila_principal * filas_internas)

# Mostrar la figura
plt.axis('equal')
plt.axis('off')  # Ocultar los ejes
plt.title('Poblacion inicial')
plt.show()
