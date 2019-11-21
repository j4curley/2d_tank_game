########################
# TANK GAME            #
# BY TREVOR AND JAMES  #
########################
###############
# HOW TO PLAY #
# #############
################################################################
# Use 'w', 'a', 's', 'd' to move tank in different directions  #
# Use arrow keys to rotate top of tank                         #
# Use space to fire projectiles                                #
# Powerups are speed and health                                #
# Kill enemies to win game; 3 random maps                      #
################################################################

##################
# IMPORT SECTION #
##################
import random
import arcade
import math
import pathlib
import time

PLAYER_SCALING = .08
PROJECTILE_SCALING = 0.05
CRATE_SCALING = .13
WEAPON_SCALING = .05
ENEMY_PROJECTILE_SCALING = 0.3
ENEMY_SCALING = 1
COUNTER = 0

def spawnEnemy(enemy, enemyList):
    x_spawn_list = [200, 500, 775, 800, 1075, 1100]
    y_spawn_list = [300, 350, 400, 450, 500, 550, 600]
    enemy.center_x = random.choice(x_spawn_list)
    enemy.center_y = random.choice(y_spawn_list)
    enemy.angle = random.randrange(0, 360, 90)
    if enemy.angle == 0:
        enemy.change_y = 2
    if enemy.angle == 90:
        enemy.change_x = -2
    if enemy.angle == 180:
        enemy.change_y = -2
    if enemy.angle == 270:
        enemy.change_x = 2

    enemyList.append(enemy)

def spawnPowerup(powerupList):
    random_powerup_List = ["Speed" , "Health"]
    randomPowerup = random.choice(random_powerup_List)
    x_powerup_spawn_list = [195, 495, 780, 795, 1070, 1095]
    y_powerup_spawn_list = [295, 340, 390, 445, 510, 560, 610]
    if randomPowerup == "Speed":
        speedPowerup = powerUp("Speed", "Assets/frame 3.png")
        speedPowerup.center_x = random.choice(x_powerup_spawn_list)
        speedPowerup.center_y = random.choice(y_powerup_spawn_list)
        powerupList.append(speedPowerup)
    elif randomPowerup == "Health":
        healthPowerup = powerUp("Health", "Assets/frame 2.png")
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
        self.health = 50

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

    def addSpeed(self, current_speed, addedSpeed):
        totalSpeed = current_speed + addedSpeed
        return totalSpeed

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
        self.enemy = None
        self.weapon = None
        self.projectile = None
        self.crate = None
        self.plist = None  #PLAYER LIST
        self.wlist = None  #WEAPON LIST
        self.elist = None  #ENEMY LIST
        self.healthPowerup = None
        self.speedPowerup = None
        self.projectilelist = None
        self.powerUpList = None
        self.powerupActive = False
        self.simple_Physics1_Player: arcade.PhysicsEngineSimple = None
        self.simple_Physics_Weapon: arcade.PhysicsEngineSimple = None
        self.simple_Physics_Projectile: arcade.PhysicsEngineSimple = None
        self.simple_Physics_Enemy: arcade.PhysicsEngineSimple = None
        self.simple_Physics_Crate: arcade.PhysicsEngineSimple = None
        self.speed = 0
        self.health = 50
        self.total_time = 0.0
        self.timeList = None
        self.timeBool = None
        self.currentPowerup = None


    def setup(self):
        ########################
        # MAP RANDOMIZER SETUP #
        ########################
        checker = self.randomMap()
        print(checker)
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
        self.elist = arcade.SpriteList()
        self.projectilelist = arcade.SpriteList()
        self.crate = arcade.Sprite(pathlib.Path.cwd() / 'Assets' / 'crate.png', CRATE_SCALING)
        self.crate.center_x = 640
        self.crate.center_y = 350
        self.player = Player()
        self.weapon = Weapon()
        self.enemy = Enemy("Tank1", 10, 2, "Assets/enemyTank.png")
        spawnEnemy(self.enemy, self.elist)
        self.projectile = Projectile()
        self.plist.append(self.player)
        self.wlist.append(self.weapon)
        self.elist.append(self.enemy)
        # self.cratelist.append(self.crate)
        self.simple_Physics_Player = arcade.PhysicsEngineSimple(self.player, self.walls)
        self.simple_Physics_Weapon = arcade.PhysicsEngineSimple(self.weapon, self.walls)
        self.simple_Physics_Crate = arcade.PhysicsEngineSimple(self.crate, self.walls)
        self.speedPowerup = powerUp("Speed", "Assets/frame 3.png")
        self.speedPowerup.center_x = 200
        self.speedPowerup.center_y = 200
        self.powerUpList = arcade.SpriteList()
        self.powerUpList.append(self.speedPowerup)

        #arcade.schedule(self.spawnPowerup(), 10)
        self.total_time = 0.0
        #self.timeList = [0, 15, 30, 45, 60, 75, 90, 105, 115, 130, 145, 160, 175, 190, 205]
        self.timeList = []
        self.timeBool = False

    ##############################
    # CHECK FOR CRATE COLLISIONS #
    ##############################
    def crateMovement(self):
        if arcade.check_for_collision(self.player, self.crate) == True:
            self.crate.change_x = self.player.change_x + 1
            self.crate.change_y = self.player.change_y + 1
        elif arcade.check_for_collision(self.player, self.crate) == False:
            self.crate.change_x = 0
            self.crate.change_y = 0
        if arcade.check_for_collision(self.enemy, self.crate) == True:
            self.crate.change_x = self.player.change_x + .15
            self.crate.change_y = self.player.change_y + .15
        elif arcade.check_for_collision(self.player, self.crate) == False:
            self.crate.change_x = 0
            self.crate.change_y = 0

        if arcade.check_for_collision_with_list(self.crate, self.projectilelist) == True:
            self.projectile.kill()
        elif arcade.check_for_collision_with_list(self.crate, self.projectilelist) == False:
            self.crate.change_x = 0

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

    ##############################
    # UPDATE 60 TIMES PER SECOND #
    ##############################
    def on_update(self, delta_time: float):
        self.plist.update()
        self.wlist.update()
        self.elist.update()
        self.crate.update()
        self.crateMovement()
        self.projectilelist.update()
        self.powerUpList.update()
        self.simple_Physics_Player.update()
        self.simple_Physics_Weapon.update()
        self.simple_Physics_Crate.update()
        self.total_time += delta_time
        self.total_time1 = int(self.total_time)

        ##########################
        # SPAWN POWERUPS ON TIME #
        ##########################
        if self.timeBool == False:
            if self.total_time1 == 5:
                spawnPowerup(self.powerUpList)
                self.timeBool = True
        elif self.total_time1 == 10 and self.timeBool == True:
            spawnPowerup(self.powerUpList)
            self.timeBool = False
        elif self.total_time1 == 15 and self.timeBool == False:
            spawnPowerup(self.powerUpList)
            self.timeBool = True
        elif self.total_time1 == 20 and self.timeBool == True:
            spawnPowerup(self.powerUpList)

        ######################################
        # PROJECTILE PHYSICS ENGINE HANDLING #
        ######################################
        for i in range(len(self.projectilelist)):
            self.simple_Physics_Projectile = arcade.PhysicsEngineSimple(self.projectilelist[i], self.walls)
            self.simple_Physics_Projectile.update()
            self.position = self.projectilelist[i].position
        # for i in range(len(self.projectilelist)):
        #     print(self.projectilelist[0].position)
        #     if self.projectilelist[i].position == self.position:
        #         self.projectilelist[i].remove_from_sprite_lists()


        ###########################
        # ACTIVATE SPEED FUNCTION #
        ###########################
        print(self.player.health)
        print(len(self.powerUpList))
        for i in range(len(self.powerUpList)-1):
            if arcade.check_for_collision(self.player, self.powerUpList[i])  == True:
                if self.powerUpList[i].getName() == "Speed":
                    print("Working!")
                    self.player.speed = self.speedPowerup.addSpeed(1, 3)
                    self.weapon.speed = self.speedPowerup.addSpeed(1, 3)
                    #self.speedPowerup.kill()
                    self.powerupActive = True

                elif self.powerUpList[i].getName() == "Health":
                    if arcade.check_for_collision(self.player, self.powerUpList[i]) == True:  # checkscol with speed powerup
                        print("Col with health works!")
                        self.player.health += 10
                        self.powerUpList[i].kill()
                        print("Health" , self.player.health)
                else:
                    print("Why isnt this detecting the powerup????")

            if (arcade.get_distance_between_sprites(self.player, self.powerUpList[i]) > 300) and self.powerupActive == True:
                self.powerupActive = False
                self.powerUpList[i].kill()

            if self.powerupActive == False:
                self.player.speed = 1
                self.weapon.speed = 1

    ##################
    # DRAW TO SCREEN #
    ##################
    def on_draw(self):
        arcade.start_render()
        self.ground_tiles.draw()
        self.walls.draw()
        self.plist.draw()
        self.wlist.draw()
        self.elist.draw()
        self.projectilelist.draw()
        self.crate.draw()
        self.powerUpList.draw()
        # Put the text on the screen.
        playerHealth = f"Health: {self.player.health}"
        arcade.draw_text(playerHealth, 100, 100,
                         arcade.csscolor.WHITE, 18)

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
            Projectile.newProjectile(self)

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
