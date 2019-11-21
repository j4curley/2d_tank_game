######################################
# TANK GAME                          #
# BY TREVOR WYSONG AND JAMES CURLEY  #
#######################################
###############
# HOW TO PLAY #
###############
################################################################
# Use 'w', 'a', 's', 'd' to move tank in different directions  #
# Use arrow keys to rotate top of tank                         #
# Use space to fire projectiles                                #
# Can only fire shots between time intervals                   #
# Powerups are teleport and health                             #
# Kill 10enemies to win game; 3 random maps                    #
# Avoid hitting enemies or their projectiles                   #
# Crate blocks projectiles and interacts with player           #
################################################################

##################
# IMPORT SECTION #
##################
import random
import arcade
import math
import pathlib
import time

PLAYER_SCALING = .06
PROJECTILE_SCALING = 0.05
CRATE_SCALING = .13
WEAPON_SCALING = .05
ENEMY_PROJECTILE_SCALING = 0.3
ENEMY_SCALING = .25
COUNTER = 0
PLAYERUP_SCALING = .06

def spawnEnemyAttributes(self, enemy, enemyList):
    path = pathlib.Path.cwd() / "Assets" / "enemyTank.png"
    enemy = Enemy("Tank", 10, 2, path)
    x_spawn_list = [200, 500, 775, 800, 1075, 1100]
    y_spawn_list = [300, 350, 400, 450, 500, 550, 600]
    enemy.center_x = random.choice(x_spawn_list)
    enemy.center_y = random.choice(y_spawn_list)
    enemy.angle = random.randrange(0, 360, 90)
    if enemy.angle == 0:
        enemy.change_y = -1
    if enemy.angle == 90:
        enemy.change_x = 1
    if enemy.angle == 180:
        enemy.change_y = 1
    if enemy.angle == 270:
        enemy.change_x = -1
    enemyList.append(enemy)

def spawnEnemy(self, score, playerSprite, enemyList, enemy, projectileList):
    spawn_enemy_sound = arcade.sound.load_sound(pathlib.Path.cwd() / 'Assets' / 'Sounds' / 'spawn.wav')
    if score <= 50:
        for enemy in range(5):
            if len(enemyList) < 5:
                if random.randrange(800) == 0:
                    spawnEnemyAttributes(self, enemy, enemyList)
                    spawn_enemy_sound.play()
    elif score > 50 and score <= 70:
        for enemy in range(25):
            if len(enemyList) < 6:
                if random.randrange(600) == 0:
                    spawnEnemyAttributes(self, enemy, enemyList)
                    spawn_enemy_sound.play()
    elif score > 70 and score <= 100:
        for enemy in range(25):
            if len(enemyList) < 7:
                if random.randrange(400) == 0:
                    spawnEnemyAttributes(self, enemy, enemyList)
                    spawn_enemy_sound.play()


def randomShoot(self, enemy_list, enemy_projectile_list):
    enemyprojectile = arcade.Sprite(pathlib.Path.cwd() / 'Assets' / 'bullet.png', PROJECTILE_SCALING)
    for enemy in range(len(enemy_list)):
        if random.randrange(2000) == 0:
            enemyprojectile = arcade.Sprite(pathlib.Path.cwd() / 'Assets' / 'bullet.png', PROJECTILE_SCALING)
            enemyprojectile.center_x = enemy_list[enemy].center_x - 5
            enemyprojectile.center_y = enemy_list[enemy].center_y
            if self.enemy.angle == 0:
                enemyprojectile.change_y = -1
            if self.enemy.angle == 90:
                enemyprojectile.change_x = 1
            if self.enemy.angle == 180:
                enemyprojectile.change_y = 1
            if self.enemy.angle == 270:
                enemyprojectile.change_x = -1
            enemyprojectile.change_x = -1
            enemy_projectile_list.append(enemyprojectile)
            # # if len(enemy_projectile_list) > 1:
            #     enemy_projectile_list.pop()
            # enemyprojectile_sound = arcade.sound.load_sound(pathlib.Path.cwd() / 'Assets' / 'Beep.wav')
            # enemyprojectile_sound.play()
    return enemyprojectile, enemy_projectile_list

def spawnPowerup(powerupList):
    random_powerup_List = ["Teleport" , "Health"]
    randomPowerup = random.choice(random_powerup_List)
    x_powerup_spawn_list = [195, 495, 780, 795, 1070, 1095]
    y_powerup_spawn_list = [295, 340, 390, 445, 510, 560, 610]
    if randomPowerup == "Teleport":
        path = pathlib.Path.cwd() / 'Assets'/ 'frame 3.png'
        teleportPowerup = powerUp("Teleport", path)
        teleportPowerup.center_x = random.choice(x_powerup_spawn_list)
        teleportPowerup.center_y = random.choice(y_powerup_spawn_list)
        powerupList.append(teleportPowerup)
    elif randomPowerup == "Health":
        path = pathlib.Path.cwd() / 'Assets'/ 'frame 2.png'
        healthPowerup = powerUp("Health", path)
        healthPowerup.center_x = random.choice(x_powerup_spawn_list)
        healthPowerup.center_y = random.choice(y_powerup_spawn_list)
        powerupList.append(healthPowerup)

#############################
#       ClASS SECTION       #
#############################
class Player(arcade.Sprite):
    def __init__(self):
        super().__init__(str(pathlib.Path.cwd() / 'Assets' / 'tankfilledtop.png'), PLAYER_SCALING)
        self.normal_speed = 1
        self.slow_speed = 1
        self.center_x = 150
        self.center_y = 150
        self.speed = self.normal_speed
        self.angle = 0
        self.health = 100

class Enemy(arcade.Sprite):
    def __init__(self, name, health, speed, path):
        super().__init__(str(pathlib.Path.cwd() / path), ENEMY_SCALING)
        self.name = name
        self.path = path
        self.health = health
        self.speed = speed
        self.angle = 180

    def getName(self):
        return self.name

    def getSpeed(self):
        return self.speed

    def getHealth(self):
        return self.health

class powerUp(arcade.AnimatedTimeBasedSprite):
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.time = 0
        super().__init__(str(pathlib.Path.cwd() / self.path), PLAYER_SCALING)

    def getName(self):
        return self.name

    def addHealth(self, health, desiredHealth):
        totalHealth = health + desiredHealth
        return totalHealth

class Weapon(arcade.Sprite):
    def __init__(self):
        super().__init__(str(pathlib.Path.cwd() / 'Assets' / 'tanktop.png'), PLAYER_SCALING)
        self.normal_speed = 1
        self.slow_speed = 1
        self.center_x = 150
        self.center_y = 150
        self.speed = self.normal_speed
        self.angle = 0

class Projectile(arcade.Sprite):
    def newProjectile(self):
        self.projectile = arcade.Sprite(pathlib.Path.cwd() / 'Assets' / 'bullet.png', PROJECTILE_SCALING)
        # Add the projectile to the appropriate lists
        self.projectilelist.append(self.projectile)
        # Position the projectile at the player's current location
        self.projectile.center_x = self.weapon.center_x
        self.projectile.center_y = self.weapon.center_y
        self.projectile.angle = self.weapon.angle + 90
        if self.projectile.angle == 90:
            self.projectile.change_y = 5
            self.projectile.center_y += 40
            self.projectile.center_x -= 2
        elif self.projectile.angle == 270:
            self.projectile.change_y = -5
            self.projectile.center_y -= 40
            self.projectile.center_x += 2
        elif self.projectile.angle == 0:
            self.projectile.change_x = 5
            self.projectile.center_x += 40
            self.projectile.center_y += 2
        elif self.projectile.angle == 180:
            self.projectile.change_x = -5
            self.projectile.center_x -= 40
            self.projectile.center_y -= 2

########################
# CREATE ARCADE WINDOW #
########################
class Project2Window(arcade.Window):
    def __init__(self):
        super().__init__(1280, 704, "Project 2 by James and Trevor")
        self.map1_location = pathlib.Path.cwd() / 'Assets' / 'Level 1.tmx'
        self.map2_location = pathlib.Path.cwd() / 'Assets' / 'Level 2.tmx'
        self.map3_location = pathlib.Path.cwd() / 'Assets' / 'Level 3.tmx'
        self.mapList = None
        self.ground_tiles = None
        self.walls = None
        self.player = None
        self.enemy = arcade.Sprite()
        self.weapon = None
        self.enemyprojectile = None
        self.projectile = None
        self.crate = None
        self.plist = None  #PLAYER LIST
        self.wlist = None  #WEAPON LIST
        self.enemy_list = arcade.SpriteList() #ENEMY LIST
        self.healthPowerup = None
        self.teleportPowerup = None
        self.teleport_sound = None
        self.projectilelist = None
        self.enemyprojectilelist = None
        self.powerUpList = None
        self.powerupActive = False
        self.simple_Physics1_Player: arcade.PhysicsEngineSimple = None
        self.simple_Physics_Weapon: arcade.PhysicsEngineSimple = None
        self.simple_Physics_Projectile: arcade.PhysicsEngineSimple = None
        self.simple_Physics_Enemy: arcade.PhysicsEngineSimple = None
        self.simple_Physics_Crate: arcade.PhysicsEngineSimple = None
        self.simple_Physics_Enemy: arcade.PhysicsEngineSimple = None
        self.speed = 0
        self.health = 100
        self.score = 0
        self.total_time = 0.0
        self.other_time = 0.0
        self.multiples_list = [3,6,9,12,15,18,21,24,27,30,33,36,39,42,45,48,51,54,57,60,63,66,69,72,75,78,
                               81,84,87,90,93,96,99,102,105,108,111,114,117,120]
        self.timePress = False
        self.press = 0
        self.timeList = None
        self.timeBool = None
        self.angleBool = None
        self.currentPowerup = None
        self.path = pathlib.Path.cwd() / 'Assets' / 'enemyTank.png'
        self.enemy3 = Enemy("Tank1", 10, 2, self.path)
        self.enemy_list.append(self.enemy3)
        self.enemy3.center_x = 100
        self.enemy3.center_y = 100
        self.allLists = None

    def setup(self):
        ########################
        # MAP RANDOMIZER SETUP #
        ########################
        checker = self.randomMap()
        if checker == 'Level 1':
            self.level1_map = arcade.tilemap.read_tmx(str(self.map1_location))
            self.ground_tiles = arcade.tilemap.process_layer(self.level1_map, 'Ground', 1)
            self.walls = arcade.tilemap.process_layer(self.level1_map, 'Wall', 1)
        elif checker == 'Level 2':
            self.level2_map = arcade.tilemap.read_tmx(str(self.map2_location))
            self.ground_tiles = arcade.tilemap.process_layer(self.level2_map, 'Ground', 1)
            self.walls = arcade.tilemap.process_layer(self.level2_map, 'Wall', 1)
        elif checker == 'Level 3':
            self.level3_map = arcade.tilemap.read_tmx(str(self.map3_location))
            self.ground_tiles = arcade.tilemap.process_layer(self.level3_map, 'Ground', 1)
            self.walls = arcade.tilemap.process_layer(self.level3_map, 'Wall', 1)

        ######################
        # SPRITE/LISTS SETUP #
        ######################
        self.plist = arcade.SpriteList()
        self.wlist = arcade.SpriteList()
        self.allSprites = arcade.SpriteList()
        self.walls.update()
        self.projectilelist = arcade.SpriteList()
        self.enemyprojectilelist = arcade.SpriteList()
        self.crate = arcade.Sprite(pathlib.Path.cwd() / 'Assets' / 'crate.png', CRATE_SCALING)
        self.crate.center_x = 640
        self.crate.center_y = 350
        self.player = Player()
        self.weapon = Weapon()
        self.teleport_sound = arcade.sound.load_sound(pathlib.Path.cwd() / 'Assets' / 'Sounds' / 'teleport.wav')
        self.health_sound = arcade.sound.load_sound(pathlib.Path.cwd() / 'Assets' / 'Sounds' / 'health.wav')
        self.projectile = Projectile()
        self.plist.append(self.player)
        self.wlist.append(self.weapon)
        # self.cratelist.append(self.crate)
        self.simple_Physics_Player = arcade.PhysicsEngineSimple(self.player, self.walls)
        self.simple_Physics_Weapon = arcade.PhysicsEngineSimple(self.weapon, self.walls)
        self.simple_Physics_Crate = arcade.PhysicsEngineSimple(self.crate, self.walls)
        self.simple_Physics_Enemy = arcade.PhysicsEngineSimple(self.enemy, self.walls)
        self.pathTele = pathlib.Path.cwd() / "Assets" /"frame 3.png"
        self.teleportPowerup = powerUp("Teleport", self.pathTele)
        self.teleportPowerup.center_x = 200
        self.teleportPowerup.center_y = 200
        self.powerUpList = arcade.SpriteList()
        self.powerUpList.append(self.teleportPowerup)
        self.total_time = 0.0
        self.projectile_time = 0.0
        self.counter = 0.0
        self.x_spawn_list = [200, 500, 775, 800, 1075, 1100]
        self.y_spawn_list = [300, 350, 400, 450, 500, 550, 600]
        #self.timeList = [0, 15, 30, 45, 60, 75, 90, 105, 115, 130, 145, 160, 175, 190, 205]
        self.timeList = []
        self.timeBool = False
        self.angleBool = False
        self.gameOver = False
        self.gameOver2 = False
        self.winChecker = False
        self.teleportList1 = [195, 495, 780, 795, 1070, 1095]
        self.teleportList2 = [295, 340, 390, 445, 510, 560, 610]
        self.framesThirtyList = [1800,3600,5400,7200,9000,10800,12600,14400]
        self.enemy_projectile_time_list1 = [range(60, 43200, 180)]
        self.enemy_projectile_time_list = [180, 360, 540, 720, 900, 1080, 1260]


        self.enemyAnim = arcade.AnimatedWalkingSprite()
        self.enemyAnim.stand_right_textures = []
        self.pathRun = pathlib.Path.cwd() / "Assets"/ "EnemyRun"/"run001.png"
        self.enemyAnim.stand_right_textures.append(arcade.load_texture(self.pathRun))
        self.enemyAnim.stand_left_textures = []
        self.enemyAnim.stand_left_textures.append(arcade.load_texture(self.pathRun, mirrored=True))
        self.enemyAnim.walk_right_textures = []
        self.enemyAnim.walk_right_textures.append(arcade.load_texture(pathlib.Path.cwd() / 'Assets'/ 'EnemyRun' / 'run001.png'))
        self.enemyAnim.walk_right_textures.append(arcade.load_texture(pathlib.Path.cwd() / 'Assets'/ 'EnemyRun' / 'run002.png'))
        self.enemyAnim.walk_right_textures.append(arcade.load_texture(pathlib.Path.cwd() / 'Assets'/ 'EnemyRun' / 'run003.png'))
        self.enemyAnim.walk_right_textures.append(arcade.load_texture(pathlib.Path.cwd() / 'Assets'/ 'EnemyRun' / 'run004.png'))
        self.enemyAnim.walk_right_textures.append(arcade.load_texture(pathlib.Path.cwd() / 'Assets'/ 'EnemyRun' / 'run005.png'))
        self.enemyAnim.walk_right_textures.append(arcade.load_texture(pathlib.Path.cwd() / 'Assets'/ 'EnemyRun' / 'run006.png'))
        self.enemyAnim.walk_right_textures.append(arcade.load_texture(pathlib.Path.cwd() / 'Assets'/ 'EnemyRun' / 'run007.png'))
        self.enemyAnim.walk_right_textures.append(arcade.load_texture(pathlib.Path.cwd() / 'Assets'/ 'EnemyRun' / 'run008.png'))
        self.enemyAnim.walk_left_textures = []
        self.enemyAnim.walk_left_textures.append(arcade.load_texture((pathlib.Path.cwd() / 'Assets'/ 'EnemyRun' / 'run001.png'), mirrored=True))
        self.enemyAnim.walk_left_textures.append(arcade.load_texture((pathlib.Path.cwd() / 'Assets'/ 'EnemyRun' / 'run002.png'), mirrored=True))
        self.enemyAnim.walk_left_textures.append(arcade.load_texture((pathlib.Path.cwd() / 'Assets'/ 'EnemyRun' / 'run003.png'), mirrored=True))
        self.enemyAnim.walk_left_textures.append(arcade.load_texture((pathlib.Path.cwd() / 'Assets'/ 'EnemyRun' / 'run004.png'), mirrored=True))
        self.enemyAnim.walk_left_textures.append(arcade.load_texture((pathlib.Path.cwd() / 'Assets'/ 'EnemyRun' / 'run005.png'), mirrored=True))
        self.enemyAnim.walk_left_textures.append(arcade.load_texture((pathlib.Path.cwd() / 'Assets'/ 'EnemyRun' / 'run006.png'), mirrored=True))
        self.enemyAnim.walk_left_textures.append(arcade.load_texture((pathlib.Path.cwd() / 'Assets'/ 'EnemyRun' / 'run007.png'), mirrored=True))
        self.enemyAnim.walk_left_textures.append(arcade.load_texture((pathlib.Path.cwd() / 'Assets'/ 'EnemyRun' / 'run008.png'), mirrored=True))
        self.enemyAnim.center_x = 1280 // 2
        self.enemyAnim.center_y = 704 // 2
        self.enemy_list.append(self.enemyAnim)
        self.simple_Physics_Enemy = arcade.PhysicsEngineSimple(self.enemyAnim, self.walls)
        self.allSprites = arcade.SpriteList()

        ##########################
        #       ANIM SPRITE      #
        ###########################
        coin = arcade.AnimatedTimeSprite(PLAYERUP_SCALING)
        path = pathlib.Path.cwd() / "Assets" / "powerupAnim" / "frame 1.png"
        #coin = powerUp("Teleport", path)
        coin.center_x = random.choice(self.x_spawn_list)
        coin.center_y = random.choice(self.y_spawn_list)
        coin.textures = []
        coin.textures.append(arcade.load_texture(pathlib.Path.cwd() / 'Assets'/ 'powerupAnim'/'frame 1.png'))
        coin.textures.append(arcade.load_texture(pathlib.Path.cwd() / 'Assets'/ 'powerupAnim'/'frame 2.png'))
        coin.textures.append(arcade.load_texture(pathlib.Path.cwd() / 'Assets'/ 'powerupAnim'/'frame 3.png'))
        coin.textures.append(arcade.load_texture(pathlib.Path.cwd() / 'Assets'/ 'powerupAnim'/'frame 4.png'))
        coin.textures.append(arcade.load_texture(pathlib.Path.cwd() / 'Assets'/ 'powerupAnim'/'frame 5.png'))
        coin.textures.append(arcade.load_texture(pathlib.Path.cwd() / 'Assets'/ 'powerupAnim'/'frame 6.png'))
        #coin.cur_texture_index = random.randrange(len(coin.textures))
        self.powerUpList.append(coin)
        self.allSprites.append(coin)

    ##############################
    # CHECK FOR CRATE COLLISIONS #
    ##############################
    def crateMovement(self):
        if arcade.check_for_collision(self.player, self.crate) == True:
            print("Crate)")
            self.crate.change_y = self.player.change_y + .15
            self.crate.change_x = self.player.change_x + .15
        elif arcade.check_for_collision(self.player, self.crate) == False:
            self.crate.change_x = 0
            self.crate.change_y = 0
        if arcade.check_for_collision(self.enemy, self.crate) == True:
            self.crate.change_x = self.enemy.change_x + .15
            self.crate.change_y = self.enemy.change_y + .15
        elif arcade.check_for_collision(self.player, self.crate) == False:
            self.crate.change_x = 0
            self.crate.change_y = 0

        if arcade.check_for_collision(self.crate, self.projectile) == True:
            self.projectile.kill()

    ##########################
    # RANDOMIZE MAP FUNCTION #
    ##########################
    def randomMap(self):
        mapRandomizerList = ['Level1', 'Level2', 'Level3']
        if random.choice(mapRandomizerList) == 'Level1':
            return 'Level 1'
        elif random.choice(mapRandomizerList) == 'Level2':
            return 'Level 2'
        elif random.choice(mapRandomizerList) == 'Level3':
            return 'Level 3'

    ##################################################
    # COLLISION DETECTION AND ACCOMODATION FOR WALLS #
    ##################################################
    def wallsFix(self, Sprite):
        if Sprite.center_x < 100:
            Sprite.center_x += 1
        elif Sprite.center_y < 100:
            Sprite.center_y += 1
        if Sprite.center_x > 1180:
            Sprite.center_x -= 1
        elif Sprite.center_y > 600:
            Sprite.center_y -= 1

    def wallsFixList(self, SpriteList):
        for i in range(len(SpriteList)):
            if SpriteList[i].center_x < 140:
                SpriteList[i].center_x += 1
            elif SpriteList[i].center_y < 140:
                SpriteList[i].center_y += 1
            if SpriteList[i].center_x > 1140:
                SpriteList[i].center_x -= 1
            elif SpriteList[i].center_y > 560:
                SpriteList[i].center_y -= 1


    ##############################
    # UPDATE 60 TIMES PER SECOND #
    ##############################
    def on_update(self, delta_time: float):
        self.plist.update()
        self.wlist.update()
        self.enemy_list.update()
        self.enemy_list.update_animation()
        self.crate.update()
        self.crateMovement()
        self.wallsFix(self.player)
        self.wallsFix(self.weapon)
        self.wallsFixList(self.enemy_list)
        self.wallsFix(self.crate)
        self.projectilelist.update()
        self.enemyprojectilelist.update()
        self.powerUpList.update()
        self.allSprites.update()
        self.allSprites.update_animation()
        self.simple_Physics_Player.update()
        self.simple_Physics_Weapon.update()
        self.simple_Physics_Crate.update()
        self.simple_Physics_Enemy.update()
        self.total_time += delta_time
        self.total_time1 = int(self.total_time)
        self.projectile_time += delta_time
        self.projectile_time1 = int(self.projectile_time)
        self.frames_elapsed = int(self.total_time * 60)
        randomShoot(self, self.enemy_list, self.enemyprojectilelist)
        spawnEnemy(self, self.score, self.player, self.enemy_list, self.enemy, self.projectilelist)
        #Collision from enemy to enemy
        colList = []
        for i in range(len(self.enemy_list)):
            colList = arcade.check_for_collision_with_list(self.enemy_list[i], self.enemy_list)

        if len(colList) > 0:
            self.enemy_list[i].kill()
            self.enemy.kill()

        playerPowerUp_list = \
            arcade.check_for_collision_with_list(self.player,
                                                 self.allSprites)
        for coin in playerPowerUp_list:
            coin.kill()
            self.player.health += 20
            self.health_sound.play()

        hit_list2 = \
            arcade.check_for_collision_with_list(self.player, self.enemy_list)
        if len(hit_list2) > 0:
            self.player.health-= 10
            self.player.center_x += 20
            self.player.center_y += 20
            self.weapon.center_x += 20
            self.weapon.center_y += 20

        if self.player.health <= 0:
            self.gameOver = True
        if self.player.health < 0:
            self.player.health = 0
        if self.gameOver == True:
            self.weapon.kill()
            self.player.kill()


        # for i in range(len(self.enemyprojectilelist)-1):
        #     if (self.enemyprojectilelist[i].center_x < 80 or self.enemyprojectilelist[i].center_x > 1200 or
        #         self.enemyprojectilelist[i].center_y < 80 or self.enemyprojectilelist[i].center_y > 700):
        #             self.enemyprojectilelist[i].kill()
        #             self.enemyprojectilelist[i].remove_from_sprite_lists()

        for j in range(len(self.enemy_list)-1):
            collision_list = arcade.check_for_collision(self.projectile, self.enemy_list[j])
            # Check to see if any bullet hit the enemy
            if collision_list == True:
                self.projectile.remove_from_sprite_lists()
                self.enemy_list[j].remove_from_sprite_lists()
                death_sound = arcade.sound.load_sound(pathlib.Path.cwd() / 'Assets' / 'Sounds' / 'death.wav')
                death_sound.play()
                self.score += 10
        print(len(self.enemy_list))
        print(self.score)

        ################################
        # RANDOMLY CHANGE ENEMY ANGLES #
        ################################
        for i in range(len(self.enemy_list)-1):
                if self.total_time1 % 4 == 0:
                    for i in range(len(self.enemy_list)):
                        if ((self.frames_elapsed) % (20)) == 0:
                            self.enemy_list[i].angle = random.randrange(0, 360, 90)
                            if self.enemy_list[i].angle == 0:
                                self.enemy_list[i].change_y = -.2
                            if self.enemy_list[i].angle == 90:
                                self.enemy_list[i].change_x = .2
                            if self.enemy_list[i].angle == 180:
                                self.enemy_list[i].change_y = .2
                            if self.enemy_list[i].angle == 270:
                                self.enemy_list[i].change_x = -.2
        print (self.frames_elapsed)
        print(self.total_time1)

        #################
        # SPAWN ON TIME #
        #################
        if len(self.powerUpList) > 1:
            self.powerUpList.pop()
        if self.frames_elapsed in self.framesThirtyList:
            spawnPowerup(self.powerUpList)

        if self.frames_elapsed in self.enemy_projectile_time_list:
            randomShoot(self, self.enemy_list, self.enemyprojectilelist)

        # Check for wall hit
        hit_list = \
            arcade.check_for_collision_with_list(self.projectile, self.walls)
        if len(hit_list) > 0:
            self.projectile.kill()

        #################################
        # ENEMY PHYSICS ENGINE HANDLING #
        #################################
        for i in range(len(self.enemy_list)):
            self.simple_Physics_Enemy = arcade.PhysicsEngineSimple(self.enemy_list[i], self.walls)
            self.simple_Physics_Enemy.update()

        ######################################
        # PROJECTILE PHYSICS ENGINE HANDLING #
        ######################################
        for i in range(len(self.projectilelist)):
            self.simple_Physics_Projectile = arcade.PhysicsEngineSimple(self.projectilelist[i], self.walls)
            self.simple_Physics_Projectile.update()
            if arcade.check_for_collision_with_list(self.projectilelist[i], self.walls) == True:
                print ("collision detection")
                self.projectilelist[i].kill()

        for i in range(len(self.enemyprojectilelist)):
            self.simple_Physics_Projectile = arcade.PhysicsEngineSimple(self.enemyprojectilelist[i], self.walls)
            self.simple_Physics_Projectile.update()
            if arcade.check_for_collision_with_list(self.enemyprojectilelist[i], self.walls) == True:
                print ("collision detection")
                self.enemyprojectilelist[i].kill()

        ###########################
        # ACTIVATE SPEED FUNCTION #
        ###########################
        # print(len(self.powerUpList))
        for i in range(len(self.powerUpList)):
            if arcade.check_for_collision(self.player, self.powerUpList[i])  == True:
                if self.powerUpList[i].getName() == "Teleport":
                    # print("Working!")
                    self.player.center_x = random.choice(self.teleportList1)
                    self.player.center_y = random.choice(self.teleportList2)
                    self.teleportPowerup.kill()
                    self.teleport_sound.play()


                elif self.powerUpList[i].getName() == "Health":
                    if arcade.check_for_collision(self.player, self.powerUpList[i]) == True:  # checkscol with speed powerup
                        # print("Col with health works!")
                        self.player.health += 10
                        self.powerUpList[i].kill()
                        self.health_sound.play()

        print(len(self.powerUpList))
        self.changelist = ["x", "y"]
        self.directionlist = [-1, 1]
        if random.choice(self.changelist) == 'x':
            if random.choice(self.directionlist) == -1:
                self.enemyAnim.change_x = -1
            elif random.choice(self.directionlist) == 1:
                self.enemyAnim.change_x = 1
        elif random.choice(self.changelist) == 'y':
            if random.choice(self.directionlist) == -1:
                self.enemyAnim.change_y = -1
            elif random.choice(self.directionlist) == 1:
                self.enemyAnim.change_y = 1

    ##################
    # DRAW TO SCREEN #
    ##################
    def on_draw(self):
        arcade.start_render()
        self.ground_tiles.draw()
        self.walls.draw()
        self.plist.draw()
        self.wlist.draw()
        self.enemy_list.draw()
        self.projectilelist.draw()
        self.enemyprojectilelist.draw()
        self.crate.draw()
        self.powerUpList.draw()
        self.allSprites.draw()

        # Put the text on the screen.
        playerHealth = f"Health: {self.player.health}"
        arcade.draw_text(playerHealth, 100, 100,
                         arcade.csscolor.WHITE, 18)
        playerScore = f"Score: {self.score}"
        arcade.draw_text(playerScore, 100, 120,
                         arcade.csscolor.WHITE, 18)

        # Game over text/condition
        if self.player.health <= 0:
            gameLost = f"Game Over!"
            arcade.draw_text(gameLost, 400, 352,
                         arcade.csscolor.RED, 80)

            if self.gameOver2 == False:
                game_loss_sound = arcade.sound.load_sound(pathlib.Path.cwd() / 'Assets' / 'Sounds' / 'game over.wav')
                game_loss_sound.play()
                self.gameOver2 = True

        # winning condition/text
        if self.score >= 100:
            self.score = 100
            gameWon = f"You WIN!!!"
            arcade.draw_text(gameWon, 400, 352,
                         arcade.csscolor.YELLOW, 80)
            self.player.remove_from_sprite_lists()
            self.weapon.remove_from_sprite_lists()
            if self.winChecker == False:
                game_won_sound = arcade.sound.load_sound(pathlib.Path.cwd() / 'Assets' / 'Sounds' / 'win.wav')
                game_won_sound.play()
                self.winChecker = True

    #############################
    # WHEN ' ' KEYS ARE PRESSED #
    #############################
    def on_key_press(self, key: int, modifiers: int):
        if key == arcade.key.A:
            self.player.change_x = -self.player.speed
            self.player.angle = 90
            self.weapon.change_x = -self.weapon.speed
        elif key == arcade.key.S:
            self.player.change_y = -self.player.speed
            self.player.angle = 180
            self.weapon.change_y = -self.weapon.speed
        elif key == arcade.key.W:
            self.player.change_y = self.player.speed
            self.player.angle = 0
            self.weapon.change_y = self.weapon.speed
        elif key == arcade.key.D:
            self.player.change_x = self.player.speed
            self.player.angle = -90
            self.weapon.change_x = self.weapon.speed
        elif key == arcade.key.UP:
            self.weapon.angle = 0
        elif key == arcade.key.DOWN:
            self.weapon.angle = 180
        elif key == arcade.key.LEFT:
            self.weapon.angle = 90
        elif key == arcade.key.RIGHT:
            self.weapon.angle = -90

        elif key == arcade.key.SPACE:
            if self.projectile_time1 % 6 != 0 and self.timePress == False:
                self.timePress = True
                if len(self.projectilelist) > 0:
                    self.projectilelist.pop()
                Projectile.newProjectile(self)
                projectile = arcade.sound.load_sound(pathlib.Path.cwd() / 'Assets' / 'Sounds' / 'projectile.wav')
                projectile.play()
            elif self.projectile_time1 % 6 == 0 and self.timePress == True:
                self.timePress = False
                Projectile.newProjectile(self)
                projectile = arcade.sound.load_sound(pathlib.Path.cwd() / 'Assets' / 'Sounds' / 'projectile.wav')
                projectile.play()

        #Emergency Update to get rid of bug
        self.weapon.center_x = self.player.center_x
        self.weapon.center_y = self.player.center_y

    ##############################
    # WHEN ' ' KEYS ARE RELEASED #
    ##############################
    def on_key_release(self, key: int, modifiers: int):
        if key == arcade.key.A and self.player.change_x < 0 and self.weapon.change_x < 0:
            self.player.change_x = 0
            self.weapon.change_x = 0
        elif key == arcade.key.D and self.player.change_x > 0 and self.weapon.change_x > 0:
            self.player.change_x = 0
            self.weapon.change_x = 0
        elif key == arcade.key.S and self.player.change_y < 0 and self.weapon.change_y < 0:
            self.player.change_y = 0
            self.weapon.change_y = 0
        elif key == arcade.key.W and self.player.change_y > 0 and self.weapon.change_y > 0:
            self.player.change_y = 0
            self.weapon.change_y = 0

        #Emergency update to avoid bugs
        self.weapon.center_x = self.player.center_x
        self.weapon.center_y = self.player.center_y

        # def animatedHealth(self):
        #     path = pathlib.Path.cwd()/'Assets'/'Animated Sprites'/'Spinning Orb'/'Red'
        #     self.health_sprite = \
        #         arcade.AnimatedTimeSprite(0.5, center_x = 300, center_y = 300)
        #     self.health_list = arcade.SpriteList()
        #     all_files = path.glob('*.png')
        #     textures = []
        #     for file_path in all_files:
        #         frame = arcade.load_texture(str(file_path))
        #         textures.append(frame)
        #     print(textures)
        #     self.health_sprite.textures = textures
        #     self.health_list.append(self.health_sprite)
        #     return self.health_list

if __name__ == '__main__':
    game = Project2Window()
    game.setup()
    arcade.run()