#ALGORITMO GENETICO EN PYTHON
import numpy as np
class AlgoritmoGenetico:
    def __init__(self, poblacion_inicial):
        self.cromosomas = poblacion_inicial
        self.parentPos = np.array([])
        #el crosspoint debe de ser de los genes de cromosoma -1 osea abcd 4 - 3, lo dejare estatico pero puedo cambiarlo luego para el proeycto 
      
        self.nRandom = np.array([])

 
    #f(x) = ((a + 2b + 3c + 4d) - 30)
    def objectiveFunction(self):
        F_obj = np.zeros(self.cromosomas.shape[0])
        for i in range(self.cromosomas.shape[0]):
            #F_obj[i] = abs((self.cromosomas[i,0] + (self.cromosomas[i,1] * 2) + (self.cromosomas[i,2] * 3) + (self.cromosomas[i,3] * 4)) - 30)#MINIMIZAR 
            F_obj[i] = (self.cromosomas[i,0] + (self.cromosomas[i,1] * 2) + (self.cromosomas[i,2] * 3) + (self.cromosomas[i,3] * 4)) - 30
        return F_obj
        
    #PASO 3: FUNCION FITNESS
    def fitnessFunction(self):
        #Fitness[1] = 1 / (1+F_obj[1]) EJEMPLO
        functionResult = self.objectiveFunction()
        Fitness = np.zeros(functionResult.shape)
        total = 0
        
        for i in range(self.cromosomas.shape[0]):
            #Fitness[i] = 1 / (1+functionResult[i])#MINIMZAR 
            Fitness[i] = functionResult[i]
            total += Fitness[i]
                        
        return Fitness, total
    

    def probabilityFunction(self):
        #P[i] = Fitness[i] / Total EJEMPLO
        #fitness = self.fitnessFunction#minimizar creo
        fitness = self.fitnessFunction()[0]
        total = self.fitnessFunction()[1]
        P = np.zeros(fitness.shape)
        for i in range(self.cromosomas.shape[0]):
             P[i] = fitness[i] / total
        return P

    def probabilityComulative(self):
        p = self.probabilityFunction()
        #C[i] = 0.1254 + n
        C = np.zeros(p.shape)
        C[0] = p[0]
        for i in range(self.cromosomas.shape[0]):
            C[i] = p[i]
            C[i] = C[i-1] + p[i]
        
        return C
     

    def comparacionesRandom(self):
        NewChromosome = np.zeros(self.cromosomas.shape)
        self.nRandom = np.random.rand(self.cromosomas.shape[0])
        #for hasta el tamaño de los cromosomas
        for i in range(len(self.cromosomas)):
            
            #En esta parte se hace los cambios con los individuos mas fuertes
            for j in range(len(self.probabilityComulative()) - 1):
             if self.nRandom[i] > self.probabilityComulative()[j] and self.nRandom[i] < self.probabilityComulative()[j+1]:
                NewChromosome[i] = self.cromosomas[j+1]
               
                
            if self.nRandom[i] < self.probabilityComulative()[0]:
                NewChromosome[i] = self.cromosomas[0]
              
           
        # Convertir NewChromosome al tipo de datos de self.cromosomas
        NewChromosome = NewChromosome.astype(self.cromosomas.dtype)

        #guardar los nuevos cambios de los nuevos cromosomas a la poblacion inicial
        np.copyto(self.cromosomas, NewChromosome)
       
        
        
    #EN ESTE PUNTO AHORA SIGUE LO DE SELECCIONAR NUEVOS RANDOMS PARA SACAR LA NUEVA GENERACION
    def seleccionar_padres(self):

        pc = .30
        k = 0
        i = 0
    
        self.nRandom = np.random.rand(len(self.cromosomas))
        
        tam = 0
        for j in range(len(self.nRandom)):
             if self.nRandom[j] <= pc:
                tam += 1
            
        self.parentPos = np.empty(tam)
        
        
        while k < len(self.cromosomas):
            #este lo activo cuando ya los reemplzae con random
        # self.nRandom[k] = np.random.rand
          if self.nRandom[k] <= pc:
            self.parentPos[i] = k
            #AQUI GUARDO EN PARENT POSITION K QUE ES LA POSICION DEL CROMOSOMA QUE FUE MENOR DE .25(PC)
            # parent[k] = k
            i = i + 1# LE VOY AUMENTANDO AL INDICE SI EL IF HIZO MATCH, PARA SEGUIR GUARDANDO EN PARENT
            
          k = k + 1

        #APARTIR DE AQUI SELECCIONAREMOS CUAL ES EL PUNTO DE CRUZE ENTRE LAS POSICIONES
        
        self.crossPoint = np.empty(len(self.parentPos))
        for i in range(len(self.parentPos)):
            # se genera de 1 a cromosomas -1 que seria abcd son 4 -1 son 3, NO PONGO -1 PORQUE COMO EMPIEZA EN 1 Y LA POSICION CUENTA COMO 0 SE EQUILIBRA
            primer_arreglo = self.cromosomas[0]
            self.crossPoint[i] = np.random.randint(1, primer_arreglo.shape[0])
           
            

        
    #recibe dos parametros la posicion de los cromosomas seleccionados y los puntos de cruze
    #tambien se requeriran los cromosomas
    def crossoverPoints(self):
        pos = self.parentPos
        point = self.crossPoint
        
        if len(pos) <= 1:
            return
   
        self.cromosomas = self.cromosomas.astype(int)
        pos = pos.astype(int)
        # Crear una copia temporal del arreglo porque si guardo en el principal los siguientes cruces tomaran 
        # los nuevos datos envez de los anteriores
        temp = np.copy(self.cromosomas)
        #lo qu hago es que para cada self.cromosomas que tomo de point(posiciones de self.cromosomass) le extraigo cada gen que seria abcd, son diferentes ifs, 
        # en caso de que el punto de cruce sea 1 pues solo tomara 1 y los otros 3 del otro array, si son 2 pues toma 2 del primero y 2 del otro, y si sonn 3 
        # pues toma 3 del primero y 1 del otro primer cruce  Chromosome[1] >< Chromosome[4]
        
        for i in range(len(pos)):
            gen = np.array([])
            gen = np.append(gen, self.cromosomas.item(pos[i],0))
            punto = point
            punto = punto.astype(int)
            lenGen = self.cromosomas[0]
            
            source = 1
            for j in range(1,lenGen.shape[0]):# -1 porque en la ultimia posicion se va a regresar, CREO QUE AQUI LO 
                #SVOY A CAMBIAR HASTA EL TAMANO DE LOS GENES OSEA ABCD
                    if i == len(punto) - 1:#si es igual a la ultima psosicion regresa a comparar la primera
                        if j != point[i]:
                          gen = np.append(gen, self.cromosomas.item(pos[i],j))
                        else:
                          gen = np.append(gen, self.cromosomas.item(pos[0],j))
                          
                    elif source < point[i]:#AQUI LE TENGO QUE CAMBIAR ENTRO DENUEVO
                        gen = np.append(gen, self.cromosomas.item(pos[i],j))
                    else:
                        gen = np.append(gen, self.cromosomas.item(pos[i+1],j))
                        
                    source += 1
                        
                        #Entro las veces necesarias    
            temp[pos[i]] = gen;   
      
        
        #MUEVO MI ARREGLO COPIA AL PRINCIPAL PARA REFLEJAR LOS CAMBIOS
        self.cromosomas = temp
        return self.cromosomas
 
   
    def mutationPoints(self):
        #VALIDACION PARA EL ALGORITMO GENETICO
        #le pondre 20%, genra un numero aleatorio si es mayor o igual a 2 no lo ejecuta
        #porque hay un 20% de que salga 1 o 2, porque son numeros del 1 al 10
        number = np.random.randint(1, 11)
        if number < 1:
            return
        #------------------------------------------------------------------------
        #AQUI COMIENZA LO DE LA MUTACION
        #MAS ADELANTE PUEDO SACAR ESTO PARA HACER LOS PUNTOS DEPENDIENDO DE OTRA ESTRUCTURA
        #total_gen = number_of_gen_in_Chromosome * number of population
        #total_gen = 4 * 6           
        
        lenGen = self.cromosomas[0]
        
        total_gen = lenGen.shape[0] * self.cromosomas.shape[0]
        
        
        number_of_mutations = 0.1 * total_gen

        #------------------------------------------------------------------------
        #para poder iterar en number_of lo converitmos a int para que redonde el numero de mutaciones
        number_of_mutations = int(number_of_mutations)
        arrPosition = np.array([])
        arrCambios = np.array([])
        
        for i in range(number_of_mutations):
            #Este random es la posicion de la poblacion que se reemplazara
            Rposition = np.random.randint(1,total_gen + 1)
            arrPosition = np.append(arrPosition, Rposition)
            
            #Este random es el numero por el cual se reemplazara
            #RANDOMS DE COLORES VERDES HEXAS
            Rcambio = np.random.randint(0x009900,0x00FF00)
            arrCambios = np.append(arrCambios, Rcambio)
            
            #AQUI HAGO EL INTERCAMBIO EN LA POSICION SELECCIONADA
            np.put(self.cromosomas,Rposition-1, Rcambio)
        return self.cromosomas, arrPosition, arrCambios, number_of_mutations
    
    def run(self):
        self.objectiveFunction()
        self.fitnessFunction()
        self.probabilityFunction()
        self.probabilityComulative()
      #  self.comparacionesRandom()# DESACTIVE ESTO PORQUE AL HACER LA COMPARACION CONVERGIA DEMASIADO RAPIDO EL ALGORITMO
        self.seleccionar_padres()
        self.crossoverPoints()
        self.mutationPoints()
    
        
    
    