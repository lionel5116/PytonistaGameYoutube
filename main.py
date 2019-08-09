from scene import *
import sound
import random

ypos = 41
#standing and walking texture
standing = Texture('plf:AlienGreen_front')
walking = [Texture('plf:AlienGreen_walk1'),Texture('plf:AlienGreen_walk2')]

class Coin(SpriteNode):
	def __init__(self,**kwargs):
		SpriteNode.__init__(self,'plf:Item_CoinGold',**kwargs)
		




class Game(Scene):
	def setup(self):
		
		#set the background of the game screen
		self.background_color = "#131fa7"  
		
		#now let's add the ground to the background at the bottom
		# A node is a fundemental building block a scene
		#nodes are organized like a tree, similar to how views and subviews work
		ground = Node(parent=self)
		x = 0
		#64 is the sprite image(sprite size), the pixel width of the file size
		while x <= self.size.w +64:
			tile = SpriteNode('plf:Ground_Dirt',position=(x,10)) #a spritenode draws a textured sprite
			#to make it visible - we are "adding a spritenode to the tree as a child of the base ground node"
			ground.add_child(tile)
			#keep added 64 pixels to the counter until it reaches the with of the screen, then break out of the loop
			x += 64
		
		#create our player sprite
		self.player = SpriteNode('plf:AlienGreen_front')
		
		#set the position of the player
		#place the player in the center of the screen at vertical (y) position 41
		self.player.position = (self.size.w / 2, 41)
		
		#anchor_point : defines the point in the sprite that corresponds to the node's postion'
		#this actually raised the sprite up a little from the it's y position (see apple's doc's on AnchorPoint')
		#A spritenode's anchor point determines which point within it's frame correspond to it's position'
		self.player.anchor_point = (0.5,0)
		
		# attach player to the ground (make it visible)
		ground.add_child(self.player)
		
		#walk_state
		self.walk_state = -1 #state at the beginning when he is just standing
		
	
	def update(self):
		if random.random() < .05:  #makes you spawn less coins
			self.spawn_coins()
			self.update_player()
	
		
	#VERY IMPORTANT, WATCH YOUR INDENTS, I HAD THIS AS PART OF THE SETUP FUNCTION, SO THE UPDATE FUNCTION WAS NOT BEING CALLED
	#let's add movement' - this is defined in the update function
	#move this call to the function above to refactor how we call the spawn coins
	def update_player(self):
		#call the spawn coins method to spawn coins
		#self.spawn_coins()
		g = gravity()
		
		#below makes the character look to left or right when moving - by manipulatin the gravity
		self.player.x_scale = ((g.x > 0) - (g.x < 0))
		
		if abs(g.y) > 0.5:
			speed = g.x * 50
			#also don't allow the character to move beyond the screen bounds - we have another example in our 
			#shipGameModified.py file
			xpos = max(0, min(self.size.w,self.player.position.x + speed))
			self.player.position = xpos , 41

		#animate the walk - evaluating the postion every 60FPS
		step = int(self.player.position.x / 40) % 2   #he is just randomozing the position with a modulus (player pos every 40 pixels)
		if step != self.walk_state:   #if the player is not just standing (not moving)
			self.player.texture = walking[step]
			
			#add some sounds to the steps
			sound.play_effect('rpg:Footstep00',0.05,1.0 + .5 * g.x)
			self.walk_state = step ##slows the walk step rate down
			
		else:
			self.player.texture = standing
		

	#add coins to our game
	
	def spawn_coins(self):
		coin = Coin(parent = self)
		coin.position = random.uniform(20,self.size.w),self.size.h-60
		#make the coins fall down from the sky
		duration = random.uniform(2,4) #random duration between 2 and 4 seconds
		coin.run_action(
			 Action.sequence(
			 	 Action.move_by(0,-1000,duration),
			 	 Action.remove()
			 	)
			)
	
	
	#let's add some laser action with the touch class'
	def touch_began(self, touch):
		#load laser sprite
		laser = SpriteNode('plf:LaserPurpleDot', 
			position=self.player.position,
			parent=self)
		
		#move the laser
		laser.run_action(Action.sequence(Action.move_by(0,1000), Action.remove()))
		
		#let's add some sound to the laser
		sound.play_effect('arcade:Explosion_7')
	

		
	

run(Game(),PORTRAIT)
