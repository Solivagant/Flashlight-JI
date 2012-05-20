from fl.Level import * #@UnusedWildImport
from fl.items.Bullet import * #@UnusedWildImport
from fl.gameobject.Crosshair import * #@UnusedWildImport
from fl.gameobject.Player import * #@UnusedWildImport
from fl.gameobject.Wall import * #@UnusedWildImport
from fl.gameobject.Life import * #@UnusedWildImport
from fl.gfx.Padlib import * #@UnusedWildImport
from fl.gfx.Text import * #@UnusedWildImport
from fl.globals import * #@UnusedWildImport
from fl.inputListener import * #@UnusedWildImport
from pygame.locals import * #@UnusedWildImport
from fl.items.LaserRifle import * #@UnusedWildImport
from fl.items.Weapon2 import * #@UnusedWildImport
from fl.gameobject.Enemy import Enemy
from fl.ai.FSM import SimpleFSM
from fl.items.RPG import RPG

"""Gestor de Jogo
   1 - creation(): inicializa todos os arrays, grupos de sprites, superficies e 
                   demais variaveis necessarias para o jogo
   2 - update() recebe inputs (teclado e rato) e altera o estado dos objectos do jogo
   2 - render() desenha os objectos do jogo no frame corrente
"""
class Game(object):
    """constructor do game, recebe um ecra"""
    def __init__(self, screen):
        #Este screen eh o ecra criado no Menu
        self.screen = screen
        self.creation()
        
    """inicializa todos os arrays, grupos de sprites, superficies e demais variaveis necessarias para o jogo"""
    def creation(self):
        #Relogio, importante para o refresh rate do jogo
        self.clock = pygame.time.Clock()
        
        #Stat
        self.correctTime = 0
        self.realTime = 0
        self.Weapon = Weapon2((280,25))
        self.life = Life((950,25))
        self.text_effect = 0
        self.client = None
        self.lights_off = True
        #variavel para saber quem matou este player
        self.killer = ""
        self.dead = False
        self.name = "DefaultName"
        self.skin = "player_five"
        self.status = Text((0,0), "", 1, None, (255,255,255))
        #Mira
        self.crosshair = crosshair((10, 10))
         
        #Grupos de Sprites das Balas, Jogadores
        self.bullets = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        
        #Listas de objectos a desenhar no ecra
        self.drawableObjects = []               #objectos a desenhar debaixo a sombra
        self.drawableObjectsSpritesLights = []  #objectos a desenhar por cima da sombra
        self.drawableTextLights = []            #texto a desenhar por cima da sombra
        self.toDelete = []                      #objectos a apagar no ciclo corrente
        
        self.isMulti =  False
        self.msg = None
        self.SEND_MESSAGE = False
        
        #Guardar a ultima mensagem de som enviada
        self.LastMsgInfo = [Text((0,0), "", 40, None, RED), 0]
       

        #Iniciar o input listener
        self.input = inputListener()
        
        #Criacao das superficies que permitem o desenho de sombras
        self.create_light_surfaces()
        
        #Exibir o cursor do rato (nao e a mira)
        pygame.mouse.set_visible(1)
    
        

    def stat(self):
        return [str(self.player.get_name()),str(self.player.playersKilled()),str(self.player.totalBullet()),str(self.correctTime),"*****"]

    
    """recebe inputs (teclado e rato) e altera o estado dos objectos do jogo"""
    def update(self):       
        
        #Espera 60 milisegundos (framerate de 60)
        self.clock.tick(60)

        #Vai buscar os inputs mais recentes
        self.input.get_events()
        
        if self.input.toQuit == True:
            if self.isMulti == True:
                self.msg = "e"
                self.SEND_MESSAGE = True
                quit()
            else:
                quit()
                
            

        #Se carregaram no Escape, vai para o menu
        if self.input.pressed(K_ESCAPE):
            return GAME_ESCAPE
        
        if self.input.pressed(K_TAB):
            return GAME_STAT
       
        #DEBUG: Tecla para avancar para o segundo nivel
        if self.input.pressed(K_0):
            self.unload_level()
            self.load_level("level2")
            
        #Contem a mira sempre a mesma distancia do player e faz update a sua posicao
        if self.player.dead == False:
            self.crosshair_constrain()
            self.crosshair.update_position()
        
        #Retirar da lista dos objectos a desenhar todos os que estiverem na lista toDelete
        for item in self.items:
            if item.toDelete == True:
                item.position = (-1,-1)
                item.update_position()
        
        #Reset a lista toDelete
        self.toDelete = []
        
        #Faz update a todos os sprites a desenhar, aos players e as balas
        
        self.bullets.update()  

        for sprite in self.drawableObjects:
            sprite.update()   
        
        #Se o jogador desta maquina disparar, cria uma Bullet e adiciona-a ao grupo das balas
        for player in self.players:
            player.update()
            if player == self.player:
                player.do_actions(self.input)
            elif self.isMulti == False:
                self.do_player_movement(player)            
            if player.is_firing == True and player.dead != True:
                if player == self.player:     
                    self.bullets.add(player.get_weapon().new_bullet((player.shootingPosition[0], player.shootingPosition[1]), (self.crosshair.position), player.name))
                elif self.isMulti == False:
                    if player.direction == LEFT:
                        self.bullets.add(player.get_weapon().new_bullet((player.position[0]-32, player.position[1]), (player.position[0]-100, player.position[1]), player.name))
                    else:
                       self.bullets.add(player.get_weapon().new_bullet((player.position[0]+32, player.position[1]), (player.position[0]+100, player.position[1]), player.name))                        
                else:
                    self.bullets.add(player.get_weapon().new_bullet((player.shootingPosition[0], player.shootingPosition[1]), (player.remoteCrosshair), player.name))

            player.update_position()
        self.do_player_movement(self.player)
        #Tratar das colisoes entre todos os objectos em jogo
        self.do_collisions()
        
        #Efeito visual de fadeout, por agora comentado
        self.fade_out()
     
        self.update_network()

        #Faz update ao ecra
        pygame.display.update()
        
        if self.player.dead:
            self.time_off = self.time_off + 1
            if self.time_off > 50:
                self.respawn_player()
                
        return GAME_CONTINUE
             
    """desenha os objectos do jogo no frame corrente"""
    def render(self):
        #Desenha a imagem de fundo no ecra, na posicao 0,0
        self.screen.blit(self.bgImage, (0, 0))
        
        #Altera a posicao do foco luminoso para se centrar na posicao do player
        self.s1.change_position(self.player.position)

        #Limpa a superficie da intensidade de luz
        self.light_intensity_surf.fill((0, 0, 0))
  
        #Desenha as sombras, com atencao aos Occluders (bloqueadores da luz, por ex: paredes)
        WillDrawShadow = True
        for o in self.Occluders:
            if o.collidepoint(self.player.position):
                WillDrawShadow = False
                break
        if WillDrawShadow:
            self.s1.draw(self.light_intensity_surf)

        #Efeito visual que torna a escuridao em penumbra (e possivel ver alguma coisa nas sombras)
        self.light_intensity_surf.blit(self.ambient_light_surface,(0,0),special_flags=BLEND_ADD)
    
     
  
        """TUDO O QUE ESTAH ENTRE A LINHA SEGUINTE..."""
        self.screen.blit(self.bgImage, (0, 0))
        
        #Limpa e desenha todos os sprites na lista drawableObjects                
        for sprite in self.drawableObjects:
            sprite.clear(self.screen, self.bgImage)
            sprite.draw(self.screen)
        for item in self.items:
            if item.toDelete == False:
                pygame.sprite.RenderPlain(item).clear(self.screen, self.bgImage)
                pygame.sprite.RenderPlain(item).draw(self.screen)
        self.bullets.clear(self.screen, self.bgImage)
        self.bullets.draw(self.screen)
        self.players.clear(self.screen, self.bgImage)
        for player in self.players:
            player.render()
        self.players.draw(self.screen)   
                  
        """... E ESTA, EH O QUE APARECE SOH QUANDO A LUZ LHE TOCA, ou seja, as sombras sao desenhadas em cima"""
        
        """DESLIGAR AS LUZES: COMENTAR AS LINHAS SEGUINTES..."""        
        if self.lights_off == True:
            if self.darkness == 1:
                if self.player.direction == RIGHT:
                    self.light_intensity_surf.blit(self.light_falloff_surfaceRight, [self.player.position[0] - 110, self.player.position[1] - 110], special_flags=BLEND_MULT)
                elif self.player.direction == LEFT:
                    self.light_intensity_surf.blit(self.light_falloff_surfaceLeft, [self.player.position[0] - 110, self.player.position[1] - 110], special_flags=BLEND_MULT) 
            else:
                self.light_intensity_surf.blit(self.light_falloff_surface, [self.player.position[0] - 110, self.player.position[1] - 110], special_flags=BLEND_MULT) 
                                               
            #Desenha uma superficie com um circulo branco para indicar o tamanho da luz
            self.screen.blit(self.light_intensity_surf, (0, 0), special_flags=BLEND_MULT)
            """DESLIGAR AS LUZES:...ATE AQUI""" 
            self.light_intensity_surf.blit(self.ambient_light_surface,(0,0),special_flags=BLEND_MULT)
    
        #Sprites sempre visiveis em cima da luz, associados a vida e ao texto
        for sprite in self.drawableObjectsSpritesLights:
            sprite.clear(self.screen, self.bgImage)
            sprite.draw(self.screen)
        
        #Desenha o texto
        for text in self.drawableTextLights:
            self.screen.blit(text.get_name(),text.get_position())
        
        #Update ao relogio:
        #self.realTime = self.realTime +  1
        #if self.realTime % 15 == 0:
        #    self.correctTime = self.correctTime + 1  
        #    self.TimeGame.change_text(self.correctTime)
        #self.screen.blit(self.TimeGame.get_name(),self.TimeGame.get_position())
        
        # Desenha o reload
        if self.player.get_reload() == 1:
            self.screen.blit(self.ReloadWeapon.get_name(),self.ReloadWeapon.get_position())    
            
        #Mensagens de sons
        if self.numbers_players() > 1:
            printMessage = self.message_info()          
            self.screen.blit(printMessage.get_name(),printMessage.get_position())
                 
        #Mensagens de status
        printMessage = self.status         
        self.screen.blit(printMessage.get_name(),printMessage.get_position())
                    
        
        #Desenha a mira
        if self.player.dead == False:
            pygame.sprite.RenderPlain(self.crosshair).draw(self.screen)
  

        #Update ao display
        pygame.display.flip()

    """mantem a crosshair a uma distancia fixa do player"""
    def crosshair_constrain(self):
        #Obter a posicao do rato
        mouse_pos = pygame.mouse.get_pos()
        #Obter a posicao do player
        player_pos = self.player.position

        #Calcular a distancia entre o rato e o player
        dist = distance(mouse_pos, player_pos)

        #Colocar a crosshair no quadrante cima a direita
        if(player_pos[0] > mouse_pos[0] and player_pos[1] > mouse_pos[1]):
            self.crosshair.position[0] = player_pos[0] - (100 * math.sin((player_pos[0] - mouse_pos[0]) / dist))
            self.crosshair.position[1] = player_pos[1] - (100 * math.sin((player_pos[1] - mouse_pos[1]) / dist))
            self.player.shootingPosition[0] = player_pos[0] - (32 * math.sin((player_pos[0] - mouse_pos[0]) / dist))
            self.player.shootingPosition[1] = player_pos[1] - (32 * math.sin((player_pos[1] - mouse_pos[1]) / dist))

        #Colocar a crosshair no quadrante baixo a direita
        if(player_pos[0] < mouse_pos[0] and player_pos[1] > mouse_pos[1]):
            self.crosshair.position[0] = player_pos[0] + (100 * math.sin((mouse_pos[0] - player_pos[0]) / dist))
            self.crosshair.position[1] = player_pos[1] - (100 * math.sin((player_pos[1] - mouse_pos[1]) / dist))
            self.player.shootingPosition[0] = player_pos[0] + (32 * math.sin((mouse_pos[0] - player_pos[0]) / dist))
            self.player.shootingPosition[1] = player_pos[1] - (32 * math.sin((player_pos[1] - mouse_pos[1]) / dist))

        #Colocar a crosshair no quadrante cima a esquerda
        if(player_pos[0] > mouse_pos[0] and player_pos[1] < mouse_pos[1]):
            self.crosshair.position[0] = player_pos[0] - (100 * math.sin((player_pos[0] - mouse_pos[0]) / dist))
            self.crosshair.position[1] = player_pos[1] + (100 * math.sin((mouse_pos[1] - player_pos[1]) / dist))
            self.player.shootingPosition[0] = player_pos[0] - (32 * math.sin((player_pos[0] - mouse_pos[0]) / dist))
            self.player.shootingPosition[1] = player_pos[1] + (32 * math.sin((mouse_pos[1] - player_pos[1]) / dist))

        #Colocar a crosshair no quadrante baixo a esquerda
        if(player_pos[0] < mouse_pos[0] and player_pos[1] < mouse_pos[1]):
            self.crosshair.position[0] = player_pos[0] + (100 * math.sin((mouse_pos[0] - player_pos[0]) / dist))
            self.crosshair.position[1] = player_pos[1] + (100 * math.sin((mouse_pos[1] - player_pos[1]) / dist))
            self.player.shootingPosition[0] = player_pos[0] + (32 * math.sin((mouse_pos[0] - player_pos[0]) / dist))
            self.player.shootingPosition[1] = player_pos[1] + (32 * math.sin((mouse_pos[1] - player_pos[1]) / dist))

    """carregamento do nivel a partir do nome do ficheiro"""       
    def load_level(self, filename):
        self.level = Level(filename)
        
        for bg_tile in self.level.getBGTiles():
            self.drawableObjects.append(pygame.sprite.RenderPlain(bg_tile)) 
        
        #Passar os items, occluders, paredes e imagem de fundo para o objecto nivel no gestor de jogo
        self.items = self.level.getItems()
        self.Occluders = self.level.getOccluders()
        
        self.walls = self.level.getWalls()
        self.wallsStart = len(self.drawableObjects)
        for wall in self.walls:
            self.drawableObjects.append(pygame.sprite.RenderPlain(wall))
        self.wallsEnd = len(self.drawableObjects)
        
        self.ladders = self.level.getLadders()
        for ladder in self.ladders:
            self.drawableObjects.append(pygame.sprite.RenderPlain(ladder))           
                    
        self.s1 = Shadow(110, [1, 1], self.Occluders, (255, 255, 255), 255)
        
        self.bgImage = self.level.bg
        
        self.respawn = self.level.respawn
    
    """descarregamento das paredes e dos items do nivel"""   
    def unload_level(self):
        self.drawableObjects.__delslice__(self.wallsStart, self.wallsEnd)          
        self.drawableObjects.__delslice__(self.itemsStart, self.itemsEnd) 
        
    """tratar as colisoes entre os objectos do jogo"""    
    def do_collisions(self):
        #testa as colisoes de players com balas
        player_bullets = pygame.sprite.groupcollide(self.players, self.bullets, 0,1)

        for player, bullet in player_bullets.iteritems():
            if self.player == player:
                #decrementar a vida deste player local
                player.dec_life(bullet[0].damage)
                self.life.loseLife(bullet[0].damage)    
                if player.dead == True:
                    self.time_off = 0
                    self.killer = bullet[0].owner
            elif self.isMulti == False and bullet[0].owner == self.player.name:
                player.dec_life(bullet[0].damage)
                if player.dead == True:
                    self.players.remove(player)
                    
        player_bullets = pygame.sprite.groupcollide(self.walls, self.bullets, 0, 1)
        
        #colisoes de jogadores com items, ou seja, quando o player apanha um item.           
        for item in self.items:
            if self.isMulti == True:
                if pygame.sprite.collide_rect(self.player, item):
                    if not self.toDelete.__contains__(item):
                        if item.getName() != "Portal" and item.getName() != "Portal2":
                            item.toDelete = True
                            if self.player.dead != True:
                                self.player.pickup(self.attribute_item(item))
                        if item.getName() == "Portal":
                            self.player.position[0] = 704
                            self.player.position[1] = 71
            elif self.isMulti == False:
                for player in self.players:
                    if pygame.sprite.collide_rect(player, item):
                        if item.getName() != "Portal" and item.getName() != "Portal2" and player == self.player:
                            item.toDelete = True
                            if self.player.dead != True:
                                self.player.pickup(self.attribute_item(item))                        
                        if item.getName() == "Portal":
                            player.position[0] = 704
                            player.position[1] = 71
                
                    
    """TODO: melhorar esta funcao de atribuicao de items para atribuir mais items (criar novos tipos)"""
    def attribute_item(self, item):
        #depende do tipo do item
        #se for caixa vermelha: da vida
         
        #se for caixa whatever: melhora a arma
            #se ele tiver o fato tal, melhora tal arma
         
        #se for caixa verde: atribui um fato ao calhas

        if random.random() > 0.5:
            self.Weapon.changeweapon(0)
            if self.isMulti:
                self.client.treatOutgoing("301+" + self.player.name + "+" + str(item.position[0]) + "+"+  str(item.position[1]) + "+" + "RPG")
            return RPG()
        else:
            self.Weapon.changeweapon(1)
            if self.isMulti:
                self.client.treatOutgoing("301+" + self.player.name + "+" + str(item.position[0]) + "+"+  str(item.position[1]) + "+" + "LaserRifle")
            return LaserRifle()
        
    """criacao das superficies a usar para as luzes e sombras"""
    def create_light_surfaces(self):
        self.darkness = 150
        self.light_falloff_surface = load_image("lightsplash.png", "res/img").convert()
        self.light_falloff_surfaceRight = load_image("lightbeam.png", "res/img").convert()
        self.light_falloff_surfaceLeft = pygame.transform.flip(self.light_falloff_surfaceRight,1,0)        
        self.light_intensity_surf = pygame.Surface(Screen).convert()
        self.ambient_light_surface = pygame.Surface(Screen)
        self.ambient_light_surface.fill((self.darkness, self.darkness, self.darkness))            
        self.light = load_image("light.png", "res/img")      
    
    """efeito visual de fade out da imagem, bom para comecar os niveis"""                                 
    def fade_out(self):
        if self.darkness != 1:
            self.ambient_light_surface = pygame.Surface(Screen)
            if self.darkness - 4 > 0:
                self.darkness -= 4
            else:
                self.darkness = 1
            self.ambient_light_surface.fill((self.darkness, self.darkness, self.darkness))  
            
            
    # Numero de jogadores online
    def numbers_players(self): 
        return len(self.players)  
    
    def message_info(self):
        messages = ["Tap", "BLAM", "Whoosh", "trakkk","WTF"]
        self.XDist = 20
        self.YDist = -8            
        
        for player in self.players:
            
            if self.player == player:
                player1_pos =  player.get_position()
                
            if self.player.dead != True:             
                for player2 in self.players:
    
                    #verificar se os dois players estao proximos (nao fazer este check caso nenhum dos players seja o jogador local)
                    if player != player2 and self.player != player2:
                        
                        player2_pos =  player2.get_position()
                        player2_backup = [player2.backupPosX, player2.backupPosY]
                        
                        #Distance between local player and adversaries on the X Axis
                        self.playerDist = math.fabs(player1_pos[0] - player2_pos[0])
                        
                        #Distance between local player and adversaries on the Y Axis
                        self.playerDistY = math.fabs(player1_pos[1] - player2_pos[1])
                        
                        #Verificar se o Jogador esta no campo de visao
                        self.vision = self.calcVision(player1_pos[0], player1_pos[1], player2_pos[0], player2_pos[1], player.get_direction())
                        
                        #Check in X and Y
                        #Close Distance Check
                        if player2.is_moving() and self.playerDist < 160 and self.playerDistY < 170 and self.vision:
                            if player2.jumping:
                                self.LastMsgInfo = [Text((player2_pos[0]+self.XDist, player2_pos[1]+self.YDist), messages[2], 40, None, RED), 0]
                                return Text((player2_pos[0]+self.XDist, player2_pos[1]+self.YDist), messages[2], 40, None, RED)
                            if player2.is_firing == 1:
                                self.LastMsgInfo = [Text((player2_pos[0]+self.XDist, player2_pos[1]+self.YDist), messages[1], 40, None, RED), 0]
                                return Text((player2_pos[0]+self.XDist, player2_pos[1]+self.YDist), messages[1], 40, None, RED) 
                            if not player2.jumping and player2.is_firing == 0:
                                self.LastMsgInfo = [Text((player2_pos[0]+self.XDist, player2_pos[1]+self.YDist), messages[0], 40, None, RED), 0]
                                return Text((player2_pos[0]+self.XDist, player2_pos[1]+self.YDist), messages[0], 40, None, RED)
                            
                        #Medium Distance Check
                        if player2.is_moving() and self.playerDist < 250 and self.playerDist >= 110 and self.playerDistY < 170:
                            if player2.jumping:
                                self.LastMsgInfo = [Text((player2_pos[0]+self.XDist, player2_pos[1]+self.YDist), messages[2], 30, None, RED), 0]
                                return Text((player2_pos[0]+self.XDist, player2_pos[1]+self.YDist), messages[2], 30, None, RED)
                            if player2.is_firing == 1:
                                self.LastMsgInfo = [Text((player2_pos[0]+self.XDist, player2_pos[1]+self.YDist), messages[1], 30, None, RED), 0]
                                return Text((player2_pos[0]+self.XDist, player2_pos[1]+self.YDist), messages[1], 30, None, RED)
                            if not player2.jumping and player2.is_firing == 0:
                                self.LastMsgInfo = [Text((player2_pos[0]+self.XDist, player2_pos[1]+self.YDist), messages[0], 30, None, RED), 0]
                                return Text((player2_pos[0]+self.XDist, player2_pos[1]+self.YDist), messages[0], 30, None, RED)
                            
                        #Large Distance Check    
                        if player2.is_moving() and self.playerDist < 350 and self.playerDist >= 250 and self.playerDistY < 170:
                            if player2.jumping:
                                self.LastMsgInfo = [Text((player2_pos[0]+self.XDist, player2_pos[1]+self.YDist), messages[2], 20, None, RED), 0]
                                return Text((player2_pos[0]+self.XDist, player2_pos[1]+self.YDist), messages[2], 20, None, RED)
                            if player2.is_firing == 1:
                                self.LastMsgInfo = [Text((player2_pos[0]+self.XDist, player2_pos[1]+self.YDist), messages[1], 20, None, RED), 0]
                                return Text((player2_pos[0]+self.XDist, player2_pos[1]+self.YDist), messages[1], 20, None, RED)
                            if not player2.jumping and player2.is_firing == 0:
                                self.LastMsgInfo = [Text((player2_pos[0]+self.XDist, player2_pos[1]+self.YDist), messages[0], 20, None, RED), 0]
                                return Text((player2_pos[0]+self.XDist, player2_pos[1]+self.YDist), messages[0], 20, None, RED)
                        
                        
                        
                        #Tratar de Ouvir Disparos a distancia
                        if player2.is_firing == 1 and self.playerDist < 160 and self.vision and self.playerDistY < 170:
                            self.LastMsgInfo = [Text((player2_pos[0]+self.XDist, player2_pos[1]+self.YDist), messages[1], 70, None, WHITE), 0]
                            return Text((player2_pos[0]+self.XDist, player2_pos[1]+self.YDist), messages[1], 70, None, WHITE)
                                        
                        if player2.is_firing == 1 and self.playerDist < 250 and self.playerDist >= 110 and self.playerDistY < 170:
                            self.LastMsgInfo = [Text((player2_pos[0]+self.XDist, player2_pos[1]+self.YDist), messages[1], 55, None, WHITE), 0]
                            return Text((player2_pos[0]+self.XDist, player2_pos[1]+self.YDist), messages[1], 55, None, WHITE)
                        
                        if player2.is_firing == 1 and self.playerDist < 350 and self.playerDist >= 250 and self.playerDistY < 170:
                            self.LastMsgInfo = [Text((player2_pos[0]+self.XDist, player2_pos[1]+self.YDist), messages[1], 35, None, WHITE), 0]
                            return Text((player2_pos[0]+self.XDist, player2_pos[1]+self.YDist), messages[1], 35, None, WHITE)
                        
        
        if self.LastMsgInfo[1] < 8:
            self.LastMsgInfo[1] = self.LastMsgInfo[1] + 1
            return self.LastMsgInfo[0]
        else:
            return Text((0,0), "", 1, None, (255,255,255))
        
                    
        #return Text((player2_pos[0]+self.XDist, player2_pos[1]+self.YDist), "", 19, None, (255, 255, 255)) 
        
     
    def calcVision(self, posX, posY, play2posX, play2posY, direction):
        self.newPosY= posY-55
        if direction == LEFT:
            self.newPosX = posX-16
            if play2posX > self.newPosX and play2posX < self.newPosX + 110 and play2posY > self.newPosY and play2posY < self.newPosY + 110:
                return True
        if direction == RIGHT:
            self.newPosX = posX+16
            if play2posX < self.newPosX and play2posX > self.newPosX + 110 and play2posY > self.newPosY and play2posY < self.newPosY + 110:
                return True
        return False
        
                       
                    
    def do_player_movement(self, player):
        # for player in self.players:
        player.backupPosition()

        if player.movement[2] != NONE:  
            if player.movement[2] == LEFT:
                player.move(-player.movement[0], 0)#movimento (actions)
                self.do_wall_collisions(player)    

            elif player.movement[2] == RIGHT:
                player.move(player.movement[0], 0) #movimento (actions)
                self.do_wall_collisions(player)
            
            elif player.movement[2] == UP and player.OnTheGround == True and player.jumping != True:
                player.jumping = True
                player.OnTheGround = False
                if player.movement[1] < 0:
                    player.jumpingHorz = -1
                if player.movement[1] > 0:
                    player.jumpingHorz = 1
                player.moveX = 0
                player.moveY = 0
                player.bla = 0

        if player.jumping == True:
            jumpHeight = JUMP_HEIGHT - player.bla
            player.move(player.jumpingHorz, -jumpHeight)
            player.bla = player.bla + 0.5
            if player.bla > JUMP_HEIGHT:
                player.jumping = False
                self.bla = JUMP_HEIGHT

            self.do_wall_collisions(player)
        
        elif player.OnTheGround == False and player.jumping == False:
            jumpHeight = JUMP_HEIGHT - player.bla
            player.move(player.jumpingHorz, jumpHeight)
            if player.bla > 0:
                player.bla = player.bla - 0.5
            self.do_wall_collisions(player)
            
        if player.OnTheGround == True:
            #Inicializa variavel
            player.bla = 0

        player.reset_movement()

    def do_wall_collisions(self, player):
        #colisoes de jogadores com paredes
        player.OnTheGround = False
        for wall in self.walls:
            if pygame.sprite.collide_rect(player, wall):
                if player.jumping == True:
                    if player.moveY < 0:
                        player.position[1] = player.backupPosY
                        
                    elif player.moveY > 0: #Estou em cima duma parede  
          
                        player.position[1] = player.backupPosY

                        player.jumping = False
                        player.jumpingHorz = 0
                    elif player.moveX > 0: #Bati no lado esquerdo duma parede

                        player.position[0] = wall.position[0]-WALL_WIDTH+1
                        player.jumping = False
                        #player.jumpingHorz = 0
                    elif player.moveX < 0: #Bati no lado direito duma parede
      
                        player.position[0] = wall.position[0]+WALL_WIDTH+1
                        player.jumping = False                  
                        
                if player.jumping == False:
                    if player.moveY < 0:
                        #print " colisao cabeca"
                        player.jumping = False
                        player.jumpingHorz = 0
                        player.position[1] = wall.position[1]+WALL_HEIGHT
                    elif player.moveY > 0: #Estou em cima duma parede
                        player.position[1] = wall.position[1]-WALL_HEIGHT+4
                        player.OnTheGround = True
                        player.jumping = False
                        player.jumpingHorz = 0

                    else:
                        if player.moveX > 0: #Bati no lado esquerdo duma parede
                            #print " colisao esquerda"              
                            if self.isMulti == False:
                                player.hitWall = True
                            player.position[0] = wall.position[0]-WALL_WIDTH
                        if player.moveX < 0: #Bati no lado direito duma parede
                            #print " colisao direita"
                            if self.isMulti == False:
                                player.hitWall = True   
                            player.position[0] = wall.position[0]+WALL_WIDTH-1
        player.update_position()
        
    def creation_UI(self):
        self.drawableTextLights.append(Text((32, 14), str(self.player.get_name()).upper(), 19, "PressStart.ttf", (34, 51, 85)))
        self.drawableTextLights.append(Text((30, 12), str(self.player.get_name()).upper(), 19, "PressStart.ttf", (171, 208, 239)))
        
        self.drawableTextLights.append(Text((232, 14), "[", 19, "PressStart.ttf", (34, 51, 85)))       
        self.drawableTextLights.append(Text((230, 12), "[", 19, "PressStart.ttf", (255, 255, 255)))
        self.drawableTextLights.append(Text((312, 14), "]", 19, "PressStart.ttf", (34, 51, 85)))       
        self.drawableTextLights.append(Text((310, 12), "]", 19, "PressStart.ttf", (255, 255, 255)))        
        self.drawableTextLights.append(Text((502, 14), "TIME:", 19, "PressStart.ttf", (34, 51, 85)))        
        self.drawableTextLights.append(Text((500, 12), "TIME:", 19, "PressStart.ttf", (255, 255, 255)))
        
        self.TimeGame = Text((592, 14), "0", 19, "PressStart.ttf", (34, 51, 85))
        self.TimeGame = Text((590, 12), "0", 19, "PressStart.ttf", (255, 255, 255))
        
        self.ReloadWeapon = Text((332, 14), "[R]ELOAD!", 19, "PressStart.ttf", (255, 0, 0))
        
        self.drawableTextLights.append(Text((774, 14), "HEALTH:", 19, "PressStart.ttf", (34, 51, 85)))
        self.drawableTextLights.append(Text((772, 12), "HEALTH:", 19, "PressStart.ttf", (255, 255, 255)))
           
        self.drawableObjectsSpritesLights.append(pygame.sprite.RenderPlain(self.life))
        self.drawableObjectsSpritesLights.append(pygame.sprite.RenderPlain(self.Weapon))

    """inicializa as listas de objectos a desenhar e apagar"""  
    def initialize_lists(self):
        #Listas de objectos a desenhar no ecra
        self.drawableObjects = []               #objectos a desenhar debaixo a sombra
        self.drawableObjectsSpritesLights = []  #objectos a desenhar por cima da sombra
        self.drawableTextLights = []            #texto a desenhar por cima da sombra
        self.toDelete = []                      #objectos a apagar no ciclo corrente
    
    """cria n especificado de inimigos controlados pelo computador"""    
    def creation_AI(self, number_of_AI):
        if(number_of_AI >= 1):                
            self.enem1 = Enemy([], 200, 100, "player_six", "Papao1", SimpleFSM())
            self.players.add(self.enem1)
        if(number_of_AI >= 2): 
            self.enem2 = Enemy([], 300, 100, "player_four", "Papao2", SimpleFSM())
            self.players.add(self.enem2)
        if(number_of_AI >= 3): 
            self.enem3 = Enemy([], 400, 100, "player_five", "Papao3", SimpleFSM())
            self.players.add(self.enem3)
        if(number_of_AI == 4): 
            self.enem4 = Enemy([], 500, 100, "player_two", "Papao4", SimpleFSM())
            self.players.add(self.enem4)
       
    def getPlayer(self):
        return self.player
    
    def update_network(self):
        self.SEND_MESSAGE = True
        if self.player.dead == False:
            self.msg = "200+" + self.player.name + "+" + str(self.player.position[0]) + "+" + str(self.player.position[1]) + "+" +  str(self.player.frameCurrent) + "+" +  str(self.player.direction) + "+"+ str(self.player.is_firing) + "+" + str(self.crosshair.position[0]) + "+" + str(self.crosshair.position[1]) + "+" + str(self.player.shootingPosition[0]) + "+" + str(self.player.shootingPosition[1]) + "+" + str(self.player.is_moving())
        else:
            self.msg = "105+" + self.player.name + "+" + self.killer
            self.die(self.killer)
            
            
    def creation_player(self, skin="player_five", name="Joaquim"):
        self.name = name
        self.skin = skin
        self.player = Player([K_a, K_d, K_z, K_w, 1,K_r,2], 100, 100, skin, name) 
        self.players.add(self.player)
        self.creation_UI()        

    def set_client(self, client):
        self.client = client
        
    def die(self, killer):
        text = "You were shot down by " + killer + ". Better luck next time..."
        self.status = Text((200,600), text, 44, None, RED)
        self.crosshair = None
        self.player.position[0] = -1
        self.player.position[1] = -1
        self.player.update_position()
        self.light_falloff_surfaceRight = load_image("lightsplash.png", "res/img").convert()
   
    def respawn_player(self):
        self.life = Life((950,25))
        self.time_off = 0
        self.killer = ""
        self.player.position[0] = 100
        self.player.position[1] = 100
        self.player.update_position()
        self.player.life = 100
        self.life = Life((950,25))
        self.drawableObjectsSpritesLights.append(pygame.sprite.RenderPlain(self.life))
        self.player.dead = False
        self.crosshair = crosshair((10, 10))
        self.status = Text((0,0), "", 1, None, (255,255,255))
        if self.isMulti:
            self.client.treatOutgoing("160+"+self.player.name+"+"+self.player.skin+"+pos")
        self.light_falloff_surfaceRight = load_image("lightbeam.png", "res/img").convert()      
    
                