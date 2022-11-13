##----------------------NÃO ALTERAR----------------------##
from controller import Robot, Motor, DistanceSensor

TIME_STEP = 32
MAX_SPEED = 12*0.75


#Listas de equipamentos do robo - CADA DEVICE DEVE TER UMA INSTANCE VINCULADA
#Devices sao os equipamentos dentro do robo
DEVICES = ['left wheel motor', 'right wheel motor', 'ds10', 'ds9', 'us1', 'us2', 'us3']
#Instances são os nomes das instancias de cada device EM ORDEM
INSTANCES = ['left_wheel', 'right_wheel', 'left_infra_red', 'right_infra_red', 'ultrassound_right', 'ultrassound_front', 'ultrassound_left']


#abordagem por maquina de estados
class stateMachine:
    def __init__(self, robot):
        self.robot = robot
        self.state = 'DEFAULT'
        
        #faz um dicionario com as instancias e devices
        self.devices = dict(zip(INSTANCES, DEVICES))
        for x in self.devices.keys():
            if 'wheel' in x: #encontrando uma variavel de motor
                vars()[x] = self.robot.getDevice(self.devices[x]) #cria a variavel com o nome colocado na lista INSTANCES
                self.devices[x] = vars()[x]
                
                self.devices[x].setPosition(float('inf')) #inicializa o motor
                self.devices[x].setVelocity(0.0)
                
            elif 'infra_red' in x or 'ultrassound' in x: #faz o mesmo com sensores
                vars()[x] = self.robot.getDevice(self.devices[x])
                self.devices[x] = vars()[x]
                
                self.devices[x].enable(TIME_STEP)
                
                
    def process(self): #processamento dos estados
        default = 'Error in Machine State' #mensagem de erro
        
        #"switch case" do python
        return getattr(self, 'case_' + str(self.state), lambda: default)()
        
    def case_FORWARD(self): #andar para frente
        self.devices['left_wheel'].setVelocity(MAX_SPEED)
        self.devices['right_wheel'].setVelocity(MAX_SPEED)

    def case_BACK(self): #andar para tras
        self.devices['left_wheel'].setVelocity(-MAX_SPEED)
        self.devices['right_wheel'].setVelocity(-MAX_SPEED)
        
    def case_LEFT(self): #virar para a direita
        self.devices['left_wheel'].setVelocity(-MAX_SPEED)
        self.devices['right_wheel'].setVelocity(MAX_SPEED)
        
    def case_RIGHT(self): #virar para a esquerda
        self.devices['left_wheel'].setVelocity(MAX_SPEED)
        self.devices['right_wheel'].setVelocity(-MAX_SPEED)




if __name__ == '__main__':
    
    robot = stateMachine(Robot()) #cria a maquina de estados
    """
    #Definindo os motores
    roda_esquerda = robot.getDevice("left wheel motor") #Motor esquerdo
    roda_direita = robot.getDevice("right wheel motor") #Motor direito
    roda_esquerda.setPosition(float('inf'))
    roda_direita.setPosition(float('inf'))
    roda_esquerda.setVelocity(0.0)
    roda_direita.setVelocity(0.0)
    
    #Definindo os sensores infravermelhos inferiores
    infraL = robot.getDevice("ds10") #Sensor infravermelho inferior esquerdo
    infraR = robot.getDevice("ds9") #Sensor infravermelho inferior direito
    infraL.enable(TIME_STEP)
    infraR.enable(TIME_STEP)
    
    #Definindos os sensores ultrassônicos
    us01 = robot.getDevice("us1") #Sensor ultrassônico lateral esquerdo
    us02 = robot.getDevice("us2") #Sensor ultrassônico fronta
    us03 = robot.getDevice("us3") #Sensor ultrassônico lateral direito
    us01.enable(TIME_STEP)
    us02.enable(TIME_STEP)
    us03.enable(TIME_STEP)
    """
    
    right_speed = 0.75 * MAX_SPEED
    left_speed = 0.75 * MAX_SPEED
    
    turning = 0
    num = 0
    esq = 0
    straight = 0
    dir = 0
    right = 0 
    left = 0
    
    last_instruction = 0 #usado para organizar o tempo de execucao das instrucoes
    
    
    ##-------------------------------------------------------##
    while robot.robot.step(TIME_STEP) != -1: #Insira dentro desse laço while o código que rodará continuamente (estilo loop do arduino)
        
        current_time = robot.robot.getTime()
        infraL_value = robot.devices['left_infra_red'].getValue()
        infraR_value = robot.devices['right_infra_red'].getValue()
        ultra_direita = robot.devices['ultrassound_right'].getValue()
        ultra_frente = robot.devices['ultrassound_front'].getValue()
        ultra_esquerda = robot.devices['ultrassound_left'].getValue()
          
        
        if infraL_value > 2000 or infraR_value > 2000: #batendo na linha, ele vira
            last_instruction = current_time
            robot.state = 'RIGHT' #atualiza o estado
        elif current_time - last_instruction > 0.5: #se nao encontrou a linha em 500ms, segue pra frente
            robot.state = 'FORWARD'
        print(f'current_time - last_instruction: {current_time-last_instruction}')
        
        
        
        robot.process() #processa o estado
        
        
        
        #parte antiga do codigo
        """
        if turning != 1:
            if infraL_value > 2000 or infraR_value > 2000:  # verifica se os sensores estão na linha branca
                turning = 1
        
        
        if turning == 0:  # faz o robo andar reto
            roda_esquerda.setVelocity(left_speed)
            roda_direita.setVelocity(right_speed)
                
                
        if turning == 1 and num < 18:  # faz o robo girar, creio que uns 150º
                
            roda_esquerda.setVelocity(left_speed)
            roda_direita.setVelocity(-right_speed)
            num += 1
        else:  # reseta as variaveis de giro e angulacao
             num = 0
             turning = 0
             
             
        if left != 1:  # faz com que o robo vire para a esquerda se o sensor detectar algo
            if ultra_esquerda > 1000:
                left = 1  # foi necessario outra variavel de controle, pois quando eu tentei usar a mesma o robo viro uma beyblade
         
        if left == 1 and esq < 5:  # faz o robo girar so um pouco, para que ele fique de frente com o outro
            roda_esquerda.setVelocity(left_speed)
            roda_direita.setVelocity(-right_speed)
            esq += 1
        else:  # reseta a variavel de giro e angulacao
            esq = 0
            left = 0
            
        
        if right != 1:  # é um movimento espelhado do giro para a esquerda
            if ultra_direita > 1000:
                right = 1
         
        if right == 1 and dir < 5:
            roda_esquerda.setVelocity(-left_speed)
            roda_direita.setVelocity(right_speed)
            dir += 1
        else:
            dir = 0
            right = 0
            """
    
