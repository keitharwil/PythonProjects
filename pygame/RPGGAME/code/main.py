import pygame
import sys

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
LIGHT_GRAY = (200, 200, 200)
RED = (220, 50, 50)
GREEN = (50, 220, 50)
BLUE = (50, 150, 220)
YELLOW = (255, 215, 0)

# Game states
STATE_VISUAL_NOVEL = "visual_novel"
STATE_BATTLE = "battle"
STATE_MENU = "menu"

class SpriteSheet:
    def __init__(self, image_path):
        try:
            self.sheet = pygame.image.load(image_path).convert_alpha()
            self.animations = self.parse_spritesheet()
        except:
            self.sheet = None
            self.animations = None
    
    def parse_spritesheet(self):
        # Spritesheet layout (based on your image):
        # Each row is an animation, each sprite is approximately 64x64 pixels
        sprite_width = 64
        sprite_height = 64
        
        animations = {
            'idle_down': [],
            'walk_down': [],
            'walk_left': [],
            'walk_right': [],
            'walk_up': [],
            'attack_down': [],
            'attack_left': [],
            'attack_right': [],
            'attack_up': [],
            'cast_down': [],
            'cast_left': [],
            'cast_right': [],
            'cast_up': [],
            'death': []
        }
        
        # Parse walking animations (rows 0-3)
        # Row 0: Walk down
        for i in range(8):
            rect = pygame.Rect(i * sprite_width, 0, sprite_width, sprite_height)
            animations['walk_down'].append(self.sheet.subsurface(rect))
        
        # Row 1: Walk left
        for i in range(8):
            rect = pygame.Rect(i * sprite_width, sprite_height, sprite_width, sprite_height)
            animations['walk_left'].append(self.sheet.subsurface(rect))
        
        # Row 2: Walk right
        for i in range(8):
            rect = pygame.Rect(i * sprite_width, sprite_height * 2, sprite_width, sprite_height)
            animations['walk_right'].append(self.sheet.subsurface(rect))
        
        # Row 3: Walk up
        for i in range(8):
            rect = pygame.Rect(i * sprite_width, sprite_height * 3, sprite_width, sprite_height)
            animations['walk_up'].append(self.sheet.subsurface(rect))
        
        # Row 4: Attack down (11 frames)
        for i in range(11):
            rect = pygame.Rect(i * sprite_width, sprite_height * 4, sprite_width, sprite_height)
            animations['attack_down'].append(self.sheet.subsurface(rect))
        
        # Row 5: Attack left (6 frames)
        for i in range(6):
            rect = pygame.Rect(i * sprite_width, sprite_height * 5, sprite_width, sprite_height)
            animations['attack_left'].append(self.sheet.subsurface(rect))
        
        # Row 6: Attack right (5 frames)
        for i in range(5):
            rect = pygame.Rect(i * sprite_width, sprite_height * 6, sprite_width, sprite_height)
            animations['attack_right'].append(self.sheet.subsurface(rect))
        
        # Row 7: Attack up (5 frames)
        for i in range(5):
            rect = pygame.Rect(i * sprite_width, sprite_height * 7, sprite_width, sprite_height)
            animations['attack_up'].append(self.sheet.subsurface(rect))
        
        # Row 8: Cast spell down (10 frames)
        for i in range(10):
            rect = pygame.Rect(i * sprite_width, sprite_height * 8, sprite_width, sprite_height)
            animations['cast_down'].append(self.sheet.subsurface(rect))
        
        # Row 9: Cast spell left (7 frames)
        for i in range(7):
            rect = pygame.Rect(i * sprite_width, sprite_height * 9, sprite_width, sprite_height)
            animations['cast_left'].append(self.sheet.subsurface(rect))
        
        # Row 10: Cast spell right (5 frames)
        for i in range(5):
            rect = pygame.Rect(i * sprite_width, sprite_height * 10, sprite_width, sprite_height)
            animations['cast_right'].append(self.sheet.subsurface(rect))
        
        # Row 11: Cast spell up (8 frames)
        for i in range(8):
            rect = pygame.Rect(i * sprite_width, sprite_height * 11, sprite_width, sprite_height)
            animations['cast_up'].append(self.sheet.subsurface(rect))
        
        # Row 12: Death animation (13 frames)
        for i in range(13):
            rect = pygame.Rect(i * sprite_width, sprite_height * 12, sprite_width, sprite_height)
            animations['death'].append(self.sheet.subsurface(rect))
        
        # Idle animations (first frame of each walk direction)
        animations['idle_down'] = [animations['walk_down'][0]]
        animations['idle_left'] = [animations['walk_left'][0]]
        animations['idle_right'] = [animations['walk_right'][0]]
        animations['idle_up'] = [animations['walk_up'][0]]
        
        return animations

class AnimatedSprite:
    def __init__(self, spritesheet, x, y, scale=2):
        self.spritesheet = spritesheet
        self.x = x
        self.y = y
        self.scale = scale
        self.current_animation = 'idle_down'
        self.frame_index = 0
        self.animation_speed = 0.15
        self.animation_timer = 0
        self.loop = True
        self.animation_finished = False
    
    def set_animation(self, animation_name, loop=True):
        if self.current_animation != animation_name:
            self.current_animation = animation_name
            self.frame_index = 0
            self.animation_timer = 0
            self.loop = loop
            self.animation_finished = False
    
    def update(self, dt):
        if self.spritesheet and self.spritesheet.animations:
            self.animation_timer += dt
            
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                frames = self.spritesheet.animations[self.current_animation]
                
                if self.frame_index < len(frames) - 1:
                    self.frame_index += 1
                elif self.loop:
                    self.frame_index = 0
                else:
                    self.animation_finished = True
    
    def draw(self, surface):
        if self.spritesheet and self.spritesheet.animations:
            frames = self.spritesheet.animations[self.current_animation]
            if frames:
                frame = frames[int(self.frame_index)]
                scaled_frame = pygame.transform.scale(
                    frame,
                    (int(frame.get_width() * self.scale), int(frame.get_height() * self.scale))
                )
                surface.blit(scaled_frame, (self.x, self.y))
        else:
            # Fallback if no spritesheet
            pygame.draw.circle(surface, GREEN, (int(self.x + 32), int(self.y + 32)), 30)

class Character:
    def __init__(self, name, hp, max_hp, atk, defense, sprite=None):
        self.name = name
        self.hp = hp
        self.max_hp = max_hp
        self.atk = atk
        self.defense = defense
        self.is_alive = True
        self.sprite = sprite
    
    def take_damage(self, damage):
        actual_damage = max(1, damage - self.defense)
        self.hp = max(0, self.hp - actual_damage)
        if self.hp == 0:
            self.is_alive = False
        return actual_damage
    
    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)

class VisualNovelScene:
    def __init__(self, text, character_name, next_scene=None, choices=None):
        self.text = text
        self.character_name = character_name
        self.next_scene = next_scene
        self.choices = choices or []
        self.current_char = 0
        self.text_speed = 2
        self.full_text_shown = False
    
    def update(self):
        if not self.full_text_shown:
            self.current_char = min(len(self.text), self.current_char + self.text_speed)
            if self.current_char >= len(self.text):
                self.full_text_shown = True
    
    def get_displayed_text(self):
        return self.text[:self.current_char]
    
    def skip_text(self):
        self.current_char = len(self.text)
        self.full_text_shown = True

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        pygame.display.set_caption("Visual Novel JRPG")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)
        self.state = STATE_VISUAL_NOVEL
        
        # Load spritesheet (replace with your file path)
        self.player_spritesheet = SpriteSheet('character_spritesheet.png')
        
        # Initialize scenes
        self.init_scenes()
        self.current_scene_key = "intro"
        
        # Battle system
        player_sprite = AnimatedSprite(self.player_spritesheet, 100, 150, scale=3)
        self.player = Character("Hero", 100, 100, 25, 5, sprite=player_sprite)
        self.enemy = None
        self.battle_menu_index = 0
        self.battle_log = []
        self.battle_phase = "player_turn"
        self.battle_animation_playing = False
        
    def init_scenes(self):
        self.scenes = {
            "intro": VisualNovelScene(
                "Welcome, brave hero! The kingdom is in danger. Will you help us?",
                "Elder",
                choices=[
                    ("Yes, I will help!", "accept"),
                    ("Tell me more first", "more_info")
                ]
            ),
            "accept": VisualNovelScene(
                "Excellent! A monster has been spotted nearby. Prepare for battle!",
                "Elder",
                next_scene="battle_start"
            ),
            "more_info": VisualNovelScene(
                "Dark forces have awakened. Only you can stop them!",
                "Elder",
                choices=[
                    ("I'm ready to fight!", "accept"),
                    ("I need to think about it", "intro")
                ]
            ),
            "battle_start": VisualNovelScene(
                "A wild Goblin appears! Get ready to fight!",
                "System",
                next_scene="enter_battle"
            ),
            "victory": VisualNovelScene(
                "You defeated the monster! The village is safe... for now.",
                "Elder",
                next_scene="intro"
            ),
            "defeat": VisualNovelScene(
                "You have been defeated... Try again, hero!",
                "System",
                next_scene="intro"
            )
        }
    
    def start_battle(self):
        self.state = STATE_BATTLE
        enemy_sprite = AnimatedSprite(self.player_spritesheet, 500, 150, scale=3)
        enemy_sprite.set_animation('idle_down')
        self.enemy = Character("Goblin", 60, 60, 15, 3, sprite=enemy_sprite)
        self.player.hp = self.player.max_hp
        self.player.sprite.set_animation('idle_down')
        self.battle_menu_index = 0
        self.battle_log = ["Battle started!"]
        self.battle_phase = "player_turn"
        self.battle_animation_playing = False
    
    def draw_text_box(self, text, x, y, width, height):
        pygame.draw.rect(self.screen, BLACK, (x, y, width, height))
        pygame.draw.rect(self.screen, WHITE, (x, y, width, height), 3)
        
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            if self.small_font.size(test_line)[0] < width - 20:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        if current_line:
            lines.append(' '.join(current_line))
        
        for i, line in enumerate(lines[:4]):
            text_surf = self.small_font.render(line, True, WHITE)
            self.screen.blit(text_surf, (x + 10, y + 10 + i * 30))
    
    def draw_visual_novel(self):
        self.screen.fill((40, 30, 60))
        
        # Draw character sprite in visual novel
        if self.player.sprite:
            self.player.sprite.x = 350
            self.player.sprite.y = 100
            self.player.sprite.set_animation('idle_down')
            self.player.sprite.draw(self.screen)
        
        scene = self.scenes[self.current_scene_key]
        scene.update()
        
        # Draw character name box
        pygame.draw.rect(self.screen, BLUE, (50, 350, 200, 40))
        name_text = self.font.render(scene.character_name, True, WHITE)
        self.screen.blit(name_text, (60, 360))
        
        # Draw dialogue box
        self.draw_text_box(scene.get_displayed_text(), 50, 400, 700, 150)
        
        # Draw choices if available and text is fully shown
        if scene.choices and scene.full_text_shown:
            for i, (choice_text, _) in enumerate(scene.choices):
                y_pos = 200 + i * 60
                color = YELLOW if i == self.battle_menu_index else WHITE
                pygame.draw.rect(self.screen, GRAY, (250, y_pos, 300, 50))
                pygame.draw.rect(self.screen, color, (250, y_pos, 300, 50), 3)
                choice_surf = self.small_font.render(choice_text, True, color)
                self.screen.blit(choice_surf, (270, y_pos + 15))
        
        # Draw continue prompt
        if scene.full_text_shown and not scene.choices:
            prompt = self.small_font.render("Press SPACE to continue", True, YELLOW)
            self.screen.blit(prompt, (550, 560))
    
    def draw_battle(self):
        self.screen.fill((60, 40, 40))
        
        # Update and draw sprites
        dt = self.clock.get_time() / 1000.0
        if self.player.sprite:
            self.player.sprite.update(dt)
            self.player.sprite.draw(self.screen)
            
            # Check if attack animation finished
            if self.battle_animation_playing and self.player.sprite.animation_finished:
                self.battle_animation_playing = False
                self.player.sprite.set_animation('idle_down')
        
        if self.enemy and self.enemy.sprite:
            self.enemy.sprite.update(dt)
            self.enemy.sprite.draw(self.screen)
        
        # Draw player stats
        self.draw_character_stats(self.player, 50, 350, True)
        
        # Draw enemy stats
        self.draw_character_stats(self.enemy, 500, 350, False)
        
        # Draw battle menu
        if self.battle_phase == "player_turn" and not self.battle_animation_playing:
            menu_options = ["Attack", "Magic", "Heal"]
            for i, option in enumerate(menu_options):
                y_pos = 450 + i * 50
                color = YELLOW if i == self.battle_menu_index else WHITE
                pygame.draw.rect(self.screen, GRAY, (50, y_pos, 200, 40))
                pygame.draw.rect(self.screen, color, (50, y_pos, 200, 40), 3)
                text = self.small_font.render(option, True, color)
                self.screen.blit(text, (70, y_pos + 10))
        
        # Draw battle log
        pygame.draw.rect(self.screen, BLACK, (280, 420, 480, 150))
        pygame.draw.rect(self.screen, WHITE, (280, 420, 480, 150), 2)
        for i, log in enumerate(self.battle_log[-5:]):
            log_text = self.small_font.render(log, True, WHITE)
            self.screen.blit(log_text, (290, 430 + i * 28))
    
    def draw_character_stats(self, char, x, y, is_player):
        # Character box
        color = GREEN if is_player else RED
        pygame.draw.rect(self.screen, color, (x, y, 200, 120), 3)
        
        # Name
        name_text = self.font.render(char.name, True, WHITE)
        self.screen.blit(name_text, (x + 10, y + 10))
        
        # HP bar
        hp_ratio = char.hp / char.max_hp
        pygame.draw.rect(self.screen, GRAY, (x + 10, y + 50, 180, 20))
        pygame.draw.rect(self.screen, GREEN, (x + 10, y + 50, int(180 * hp_ratio), 20))
        hp_text = self.small_font.render(f"HP: {char.hp}/{char.max_hp}", True, WHITE)
        self.screen.blit(hp_text, (x + 10, y + 80))
    
    def handle_visual_novel_input(self, event):
        scene = self.scenes[self.current_scene_key]
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not scene.full_text_shown:
                    scene.skip_text()
                elif scene.choices:
                    pass
                elif scene.next_scene:
                    if scene.next_scene == "enter_battle":
                        self.start_battle()
                    else:
                        self.current_scene_key = scene.next_scene
                        self.scenes[self.current_scene_key].current_char = 0
                        self.scenes[self.current_scene_key].full_text_shown = False
            
            elif scene.choices and scene.full_text_shown:
                if event.key == pygame.K_UP:
                    self.battle_menu_index = (self.battle_menu_index - 1) % len(scene.choices)
                elif event.key == pygame.K_DOWN:
                    self.battle_menu_index = (self.battle_menu_index + 1) % len(scene.choices)
                elif event.key == pygame.K_RETURN:
                    _, next_scene = scene.choices[self.battle_menu_index]
                    self.current_scene_key = next_scene
                    self.scenes[self.current_scene_key].current_char = 0
                    self.scenes[self.current_scene_key].full_text_shown = False
                    self.battle_menu_index = 0
    
    def handle_battle_input(self, event):
        if event.type == pygame.KEYDOWN and self.battle_phase == "player_turn" and not self.battle_animation_playing:
            if event.key == pygame.K_UP:
                self.battle_menu_index = (self.battle_menu_index - 1) % 3
            elif event.key == pygame.K_DOWN:
                self.battle_menu_index = (self.battle_menu_index + 1) % 3
            elif event.key == pygame.K_RETURN:
                self.execute_battle_action()
    
    def execute_battle_action(self):
        self.battle_animation_playing = True
        
        if self.battle_menu_index == 0:  # Attack
            self.player.sprite.set_animation('attack_down', loop=False)
            damage = self.enemy.take_damage(self.player.atk)
            self.battle_log.append(f"{self.player.name} attacks for {damage} damage!")
        elif self.battle_menu_index == 1:  # Magic
            self.player.sprite.set_animation('cast_down', loop=False)
            damage = self.enemy.take_damage(self.player.atk + 10)
            self.battle_log.append(f"{self.player.name} casts magic for {damage} damage!")
        elif self.battle_menu_index == 2:  # Heal
            self.player.sprite.set_animation('cast_down', loop=False)
            heal_amount = 20
            self.player.heal(heal_amount)
            self.battle_log.append(f"{self.player.name} heals for {heal_amount} HP!")
        
        if not self.enemy.is_alive:
            self.battle_log.append(f"{self.enemy.name} defeated!")
            pygame.time.set_timer(pygame.USEREVENT + 2, 1500, 1)
            return
        
        pygame.time.set_timer(pygame.USEREVENT + 1, 1500, 1)
    
    def enemy_turn(self):
        self.battle_phase = "enemy_turn"
        if self.enemy.sprite:
            self.enemy.sprite.set_animation('attack_down', loop=False)
        
        damage = self.player.take_damage(self.enemy.atk)
        self.battle_log.append(f"{self.enemy.name} attacks for {damage} damage!")
        
        if not self.player.is_alive:
            self.battle_log.append("You have been defeated!")
            pygame.time.set_timer(pygame.USEREVENT + 2, 1500, 1)
            return
        
        self.battle_phase = "player_turn"
    
    def end_battle(self, victory):
        pygame.time.set_timer(pygame.USEREVENT + 1, 0)
        pygame.time.set_timer(pygame.USEREVENT + 2, 0)
        if victory:
            self.current_scene_key = "victory"
        else:
            self.current_scene_key = "defeat"
        self.scenes[self.current_scene_key].current_char = 0
        self.scenes[self.current_scene_key].full_text_shown = False
        self.state = STATE_VISUAL_NOVEL
        self.player.is_alive = True
    
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.USEREVENT + 1:
                    self.enemy_turn()
                elif event.type == pygame.USEREVENT + 2:
                    victory = not self.player.is_alive == False
                    self.end_battle(victory)
                elif self.state == STATE_VISUAL_NOVEL:
                    self.handle_visual_novel_input(event)
                elif self.state == STATE_BATTLE:
                    self.handle_battle_input(event)
            
            if self.state == STATE_VISUAL_NOVEL:
                self.draw_visual_novel()
            elif self.state == STATE_BATTLE:
                self.draw_battle()
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()