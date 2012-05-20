

## Definicao do codigo de mensagens de connexao 

# IMPORTANTE !!!! Os 3 primeiros caracteres da mensagem sao reservados para o Code Number!
# para que depois seja possivel processar estes devidamente !!!

# Mudar Esta funcao de Sitio!
def transformToString(score):
        
    stringresult = ""
        
    for s in score:
        if not len(stringresult):
            stringresult = s[0] + "+" + str(s[1])
        else:
            stringresult = stringresult + "+" + s[0] + "+" + str(s[1])
            
    return stringresult 

class MsgConnect(object):
    
    def __init__(self, timer, score, level):
        self.code = 100
        self.timer = timer
        self.score = transformToString(score)
        print self.score
        self.level = level
        
        
    def toString(self):
        stringfinal = str(self.code) + "+" + str(self.timer) + "+" + self.score + "+" + self.level
        return stringfinal
 
class MsgNewPlayer(object):
    
    def __init__(self, name, avatar, pos):
        self.code = 101
        self.name = name
        self.avatar = avatar
        self.pos = pos
        #self.pos =  transformToString(pos)
        
    def toString(self):
        stringfinal = str(self.code) + "+" + self.name + "+" + self.avatar + "+" + self.pos
        return stringfinal

## Definicao da estrutura de codigos de Accao mid game !!

class MsgAction(object):
    
    def __init__(self, playerId, pos, weaponId):
        self.code = 200
        self.playerId = playerId
        self.pos = self.transformToString(pos)
        self.weaponId = weaponId
        
    def toString(self):
        stringfinal = str(self.code) + "-" + str(self.playerId) + "-" + self.pos + "-" + str(self.weaponId)
        return stringfinal

class MsgScoreUpdate(object):
    
    def __init__(self, timer, score):
        self.code = 201
        self.timer = timer
        self.score = self.transformToString(score)
        
    def toString(self):
        stringfinal = str(self.code) + "-" + str(self.timer) + "-" + self.score
        return stringfinal
    
class MsgItemPickup(object):
    
    def __init__(self, timer, score):
        self.code = 201
        self.timer = timer
        self.score = self.transformToString(score)
        
    def toString(self):
        stringfinal = str(self.code) + "-" + str(self.timer) + "-" + self.score
        return stringfinal

## Codigo de mudanca de mapa  

class MsgMapChange(object):
    
    def __init__(self, newmap, timer, maxKill):
        self.code = 300
        self.newmap = newmap
        self.timer = timer
        self.maxKill = maxKill
        
    def toString(self):
        stringfinal = str(self.code) + "-" + self.newmap + "-" + str(self.timer) + "-" + str(self.maxKill)
        return stringfinal

class MsgAllReady(object):
    
    def __init(self):
        self.code = 301
    
    def toString(self):
        return str(self.code)
