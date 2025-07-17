class Settings:
    def __init__(self):
        self.width=1200
        self.length=800
        self.bg_color=(245,245,245)
        
        self.ship_limit=3
        self.bullet_height=15
        self.bullet_width=3
        
        self.bullet_color=(60,60,60)
        self.bullets_allowed=7
        
        self.fleet_drop_speed=10
        
        self.alien_points=50
        
              
        self.speedup_scale=1.1
        
        self.score_scale=1.5  
        
        self.initialize_dynamic_settings()
        
    def initialize_dynamic_settings(self):
        self.ship_speed=0.25
        self.bullet_speed=1.0
        self.alien_speed=0.2
        self.fleet_direction=1
        
    def increse_speed(self):
        self.ship_speed*=self.speedup_scale
        self.bullet_speed*=self.speedup_scale
        self.alien_speed*=self.speedup_scale
        
        self.alien_points=int(self.alien_points*self.score_scale)