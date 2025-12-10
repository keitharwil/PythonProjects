import pygame
import sys
import json
import os
import random
from pathlib import Path
from os.path import join

# --- IMPORT SPRITESHEET HELPER ---
try:
    from spritesheet import Spritesheet
except ImportError:
    print("Warning: spritesheet.py not found. Player sprites will not load.")
    Spritesheet = None

pygame.init()

# --- CONSTANTS ---
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
RED = (220, 50, 50)
GREEN = (50, 220, 50)
BLUE = (50, 150, 220)
YELLOW = (255, 215, 0)
PURPLE = (150, 50, 220)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)

ATB_MAX = 100
ATB_BAR_WIDTH = 80
ATB_BAR_HEIGHT = 8

# Zones
ZONE_UPPER = "High"
ZONE_MID = "Mid"
ZONE_LOWER = "Low"

# Game States
STATE_START = "start_menu"
STATE_HUB = "hub"
STATE_STATS = "stats_menu"
STATE_SHOP = "shop"
STATE_DUNG_SELECT = "dungeon_select"
STATE_BATTLE = "battle"
STATE_VICTORY = "victory"
STATE_GAME_OVER = "game_over"
STATE_SAVE_MENU = "save_menu"

BATTLE_MAIN = "main_menu"
BATTLE_ATTACK_SELECT = "attack_select"
BATTLE_SKILLS = "skills_menu"
BATTLE_ITEM_SELECT = "item_select"

# --- HELPER CLASSES ---

class FloatingText:
    def __init__(self, text, x, y, color, size=40):
        self.text = str(text)
        self.x = x
        self.y = y
        self.color = color
        self.timer = 1.5 
        self.font = pygame.font.Font(None, size)
        self.dy = -1 
        self.alpha = 255

    def update(self, dt):
        self.y += self.dy * (dt * 60) 
        self.timer -= dt
        if self.timer < 0.5:
            self.alpha = max(0, int(255 * (self.timer / 0.5)))

    def draw(self, surface):
        if self.timer > 0:
            txt_surf = self.font.render(self.text, True, self.color)
            txt_surf.set_alpha(self.alpha)
            outline = self.font.render(self.text, True, BLACK)
            outline.set_alpha(self.alpha)
            surface.blit(outline, (self.x + 2, self.y + 2))
            surface.blit(txt_surf, (self.x, self.y))

# --- SPRITE CLASSES ---

class SpriteSheetAnimations:
    def __init__(self):
        self.animations = {}
        if Spritesheet:
            try:
                self.sheet = Spritesheet(
                    filepath=Path(join("assets", "WarriorMan-Sheet.png")),
                    sprite_size=(80, 64),
                    spacing=(0, 0),
                    scale=(256, 256) 
                )
                self.animations = self.parse_spritesheet()
            except Exception as e:
                print(f"Error loading spritesheet: {e}")

    def parse_spritesheet(self):
        anim = {}
        anim['idle_down'] = self.sheet.get_sprites([(0, i) for i in range(8)])
        anim['attack_down'] = self.sheet.get_sprites([(11, i) for i in range(8)])
        anim['cast_down'] = self.sheet.get_sprites([(13, i) for i in range(13)])
        anim['death'] = self.sheet.get_sprites([(26, i) for i in range(7)])
        return anim

class AnimatedSprite:
    """For the Player (Uses Spritesheet)"""
    def __init__(self, animation_manager, x, y):
        self.manager = animation_manager
        self.x = x
        self.y = y
        self.current_animation = 'idle_down'
        self.frame_index = 0
        self.animation_speed = 0.1
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
        if self.manager and self.manager.animations and self.current_animation in self.manager.animations:
            self.animation_timer += dt
            frames = self.manager.animations[self.current_animation]
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                if self.frame_index < len(frames) - 1:
                    self.frame_index += 1
                elif self.loop:
                    self.frame_index = 0
                else:
                    self.animation_finished = True
    
    def draw(self, surface):
        rect = pygame.Rect(self.x - 40, self.y - 40, 80, 80)
        if self.manager and self.manager.animations and self.current_animation in self.manager.animations:
            frames = self.manager.animations[self.current_animation]
            idx = int(self.frame_index) % len(frames)
            frame = frames[idx]
            rect = frame.get_rect(center=(self.x, self.y))
            surface.blit(frame, rect)
        else:
            pygame.draw.rect(surface, GREEN, rect)
        return rect

class StaticSprite:
    """For Enemies (Uses Single Image)"""
    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y
        # FORCE INT: Pygame sometimes crashes if these are floats
        self.rect = self.image.get_rect(center=(int(x), int(y)))
        self.animation_finished = True 

    def set_animation(self, animation_name, loop=True):
        pass

    def update(self, dt):
        pass

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        return self.rect
# --- RPG CLASSES ---
class Skill:
    def __init__(self, name, cost, power, type="damage", element="physical"):
        self.name = name; self.cost = cost; self.power = power; self.type = type
        self.element = element

class Character:
    def __init__(self, name, hp, mp, atk, defense, is_player=False, char_type="Human"):
        self.name = name
        self.max_hp = hp; self.hp = hp
        self.max_mp = mp; self.mp = mp
        self.atk = atk; self.defense = defense
        self.is_alive = True; self.is_player = is_player
        self.sprite = None
        self.char_type = char_type 
        
        self.level = 1; self.exp = 0; self.exp_to_next = 100; self.gold = 0
        self.potions = 3
        self.mana_potions = 1 
        
        self.atb = 0
        self.speed = 20
        
        self.skills = []
        if is_player:
            self.skills.append(Skill("Heal", 10, 30, "heal", "magic"))
            self.skills.append(Skill("Fireball", 15, 2.0, "damage", "magic"))


    def take_damage(self, damage):
        actual = max(0, damage - self.defense)
        self.hp = max(0, self.hp - actual)
        if self.hp == 0: self.is_alive = False
        return actual
    
    def heal(self, amount): self.hp = min(self.max_hp, self.hp + amount)
    
    def gain_exp(self, amount):
        if not self.is_player: return False
        self.exp += amount
        leveled = False
        while self.exp >= self.exp_to_next:
            self.exp -= self.exp_to_next; self.level += 1; self.max_hp += 20; self.max_mp += 10
            self.hp = self.max_hp; self.mp = self.max_mp; self.atk += 5; self.defense += 2
            self.speed += 2
            leveled = True
        return leveled

    def to_dict(self): 
        return {
            "name": self.name, "max_hp": self.max_hp, "hp": self.hp, 
            "max_mp": self.max_mp, "mp": self.mp, "atk": self.atk, 
            "defense": self.defense, "level": self.level, "exp": self.exp, 
            "exp_to_next": self.exp_to_next, "gold": self.gold, 
            "potions": self.potions, "mana_potions": self.mana_potions,
            "speed": self.speed
        }
    
    def load_from_dict(self, d): 
        self.name = d["name"]; self.max_hp = d["max_hp"]; self.hp = d["hp"]
        self.max_mp = d.get("max_mp", 50); self.mp = d.get("mp", 50)
        self.atk = d["atk"]; self.defense = d["defense"]
        self.level = d["level"]; self.exp = d["exp"]; self.exp_to_next = d["exp_to_next"]
        self.gold = d["gold"]; self.potions = d["potions"]
        self.mana_potions = d.get("mana_potions", 0)
        self.speed = d.get("speed", 20)

def generate_enemy(level):
    types = [
        "Slime", "Goblin", "Skeleton", "Orc", "Demon",
        "Golem", "Chimera", "Dark Knight", "Dragon", "Demon Lord"
    ]
    idx = min(level-1, 9)
    c_type = types[idx]
    
    hp = 30 + (level * level * 5)
    atk = 5 + (level * 6)
    defense = level * 3
    speed = 15 + (level * 3)
    
    if c_type == "Golem": defense *= 2; speed -= 5
    if c_type == "Chimera": speed += 15; hp = int(hp * 0.8)
    if c_type == "Dark Knight": defense += 10; hp += 50
    if c_type == "Dragon": hp += 150; atk += 10
    if c_type == "Demon Lord": hp = 1500; atk = 70; speed = 50; defense = 20
    
    enemy = Character(c_type, hp, 0, atk, defense, is_player=False, char_type=c_type)
    enemy.speed = speed
    enemy.exp_reward = 20 + (level*25); enemy.gold_reward = 10 + (level*20)
    return enemy

# --- GAME CLASS ---
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.WIDTH, self.HEIGHT = self.screen.get_size()
        pygame.display.set_caption("RPG ATB System")
        self.clock = pygame.time.Clock()
        
        self.title_font = pygame.font.Font(None, int(self.HEIGHT * 0.12))
        self.font = pygame.font.Font(None, int(self.HEIGHT * 0.05))
        self.small_font = pygame.font.Font(None, int(self.HEIGHT * 0.03))
        
        # Load Player Animations
        self.anim_manager = SpriteSheetAnimations()
        
        # Load Main Backgrounds
        self.bg_start = self.load_background("bg_start.png")
        self.bg_hub = self.load_background("bg_hub.png")
        self.bg_battle_default = self.load_background("bg_battle.png") # The default fallback
        self.bg_shop = self.load_background("bg_shop.png")

        # --- LOAD BATTLE BACKGROUNDS PER ENEMY ---
        # 1. Configuration: Map Enemy Name to Filename
        self.battle_bg_config = {
            "Slime": "bg_forest.png",
            "Goblin": "bg_forest.png",
            "Skeleton": "bg_graveyard.png",
            "Orc": "bg_forest.png",
            "Demon": "bg_castle_entrance.png",
            "Golem": "bg_mountains.png",
            "Chimera": "bg_mountains.png",
            "Dark Knight": "bg_demon_castle.png",
            "Dragon": "bg_dragon_lair.png",
            "Demon Lord": "bg_demon_castle.png"
        }
        
        # 2. Load them into memory
        self.battle_backgrounds = {}
        self.load_all_battle_backgrounds()

        self.current_battle_bg = self.bg_battle_default # Variable for the current active BG

        # Load Enemy Images (Static)
        self.enemy_images = self.load_enemy_images()

        self.state = STATE_START
        self.player = Character("Hero", 100, 50, 20, 5, is_player=True)
        self.current_dungeon_depth = 1
        self.active_battle_level = 1
        self.enemy = None
        
        self.menu_index = 0
        self.is_saving = False
        self.battle_menu_state = BATTLE_MAIN
        self.screen_shake_duration = 0
        self.red_flash_alpha = 0
        self.victory_data = {}
        
        self.is_battle_active = False 
        self.is_player_turn_ready = False 
        
        self.enemy_blocked_zones = []
        self.demon_barrier_active = False
        self.mechanic_timer = 0
        self.mechanic_interval = 3.0
        self.floating_texts = []
        
        self.mouse_click_pos = None
        self.key_pressed_enter = False

    def load_background(self, filename):
        try:
            path = Path(join("assets", filename))
            if path.exists():
                img = pygame.image.load(path).convert()
                return pygame.transform.scale(img, (self.WIDTH, self.HEIGHT))
        except:
            pass
        return None

    def load_all_battle_backgrounds(self):
        """Loads specific backgrounds per enemy based on config"""
        print("--- LOADING BATTLE BACKGROUNDS ---")
        for enemy_type, filename in self.battle_bg_config.items():
            bg = self.load_background(filename)
            if bg:
                self.battle_backgrounds[enemy_type] = bg
                print(f"Loaded BG for {enemy_type}: {filename}")
            else:
                print(f"BG missing for {enemy_type} ({filename}), using default.")

    def load_enemy_images(self):
        """Loads static enemy images or creates fallbacks"""
        print("--- LOADING ENEMY ASSETS ---")
        names = ["Slime", "Goblin", "Skeleton", "Orc", "Demon", "Golem", "Chimera", "Dark Knight", "Dragon", "Demon Lord"]
        images = {}
        
        if not os.path.exists("assets"):                                                                                        
            print("WARNING: 'assets' folder not found. Creating fallbacks.")

        for name in names:
            filename = f"{name}.png"
            path = Path(join("assets", filename))
            loaded = False
            
            try:
                if path.exists():
                    img = pygame.image.load(path).convert_alpha()
                    scale = 0.8
                    w, h = img.get_width() * scale, img.get_height() * scale
                    images[name] = pygame.transform.scale(img, (w, h))
                    loaded = True
                    print(f"Loaded: {filename}")
                else:
                    print(f"Missing: {filename} (Using Fallback)")
            except Exception as e:
                print(f"Error loading {filename}: {e}")

            if not loaded:
                surf = pygame.Surface((150, 150))
                random.seed(name) 
                color = (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))
                surf.fill(color)
                pygame.draw.rect(surf, WHITE, (0,0,150,150), 5)
                txt = self.small_font.render(name, True, WHITE)
                surf.blit(txt, (75 - txt.get_width()//2, 75 - txt.get_height()//2))
                images[name] = surf
                
        return images
    
    def reset_game(self):
        self.player = Character("Hero", 100, 50, 20, 5, is_player=True)
        self.current_dungeon_depth = 1
        self.state = STATE_HUB

    def get_save_path(self, slot): return f"savegame_{slot}.json"
    def save_game(self, slot):
        data = {"player": self.player.to_dict(), "dungeon_unlocked": self.current_dungeon_depth}
        try:
            with open(self.get_save_path(slot), 'w') as f: json.dump(data, f)
        except: pass
    def load_game(self, slot):
        path = self.get_save_path(slot)
        if not os.path.exists(path): return False
        try:
            with open(path, 'r') as f:
                data = json.load(f)
            self.player.load_from_dict(data["player"])
            self.current_dungeon_depth = data.get("dungeon_unlocked", 1)
            self.player.is_alive = True 
            if self.player.hp <= 0: self.player.hp = 1
            self.state = STATE_HUB
            return True
        except: return False

    def spawn_popup(self, text, color, x, y):
        offset_x = 40; offset_y = -50 
        popup = FloatingText(text, x + offset_x, y + offset_y, color)
        self.floating_texts.append(popup)

    def update_atb(self, dt):
        if not self.is_battle_active: return

        if self.player.atb < ATB_MAX:
            self.player.atb += self.player.speed * dt
            if self.player.atb >= ATB_MAX:
                self.player.atb = ATB_MAX
                self.is_player_turn_ready = True
                self.menu_index = 0
                self.battle_menu_state = BATTLE_MAIN

        if self.enemy.atb < ATB_MAX and self.enemy.is_alive:
            self.enemy.atb += self.enemy.speed * dt
            if self.enemy.atb >= ATB_MAX:
                self.enemy.atb = 0 
                self.enemy_attack_trigger()

    def update_battle_mechanics(self, dt):
        for txt in self.floating_texts[:]:
            txt.update(dt)
            if txt.timer <= 0: self.floating_texts.remove(txt)

        if self.state == STATE_BATTLE and self.enemy and self.enemy.is_alive:
            self.mechanic_timer -= dt
            
            if self.mechanic_timer <= 0:
                c_type = self.enemy.char_type
                zones = [ZONE_UPPER, ZONE_MID, ZONE_LOWER]

                # --- 1. SET NEXT TIMER DURATION ---
                # Default for Goblin/Orc/etc is 3.0 seconds
                next_time = 3.0
                
                # Demon Lord gets a random time between 6 and 10 seconds
                if c_type == "Demon Lord":
                    next_time = random.uniform(10.0, 15.0)
                
                self.mechanic_timer = next_time

                # --- 2. APPLY MECHANICS ---
                if c_type in ["Goblin", "Chimera"]: 
                    self.enemy_blocked_zones = [random.choice(zones)]
                
                elif c_type in ["Orc", "Dark Knight", "Dragon"]:
                    open_spot = random.choice(zones)
                    self.enemy_blocked_zones = [z for z in zones if z != open_spot]
                
                elif c_type == "Demon Lord":
                    # If barrier is down, restore it
                    if not self.demon_barrier_active:
                        self.demon_barrier_active = True
                        # Clear blocked zones because Barrier provides total immunity
                        self.enemy_blocked_zones = []
                        if self.enemy.sprite:
                            self.spawn_popup("BARRIER RESTORED!", PURPLE, self.enemy.sprite.x, self.enemy.sprite.y)
                    else:
                        # If barrier is already active, we can shuffle his physical guard behind the barrier
                        # or just leave it. Let's make him change stance behind the barrier:
                        open_spot = random.choice(zones)
                        self.enemy_blocked_zones = [z for z in zones if z != open_spot]

    def handle_input(self):
        self.mouse_click_pos = None
        self.key_pressed_enter = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.USEREVENT + 2: self.trigger_victory_screen()
            
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: self.mouse_click_pos = event.pos

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z: self.key_pressed_enter = True
                
                if self.state == STATE_START:
                    if event.key == pygame.K_UP: self.menu_index = (self.menu_index - 1) % 3
                    if event.key == pygame.K_DOWN: self.menu_index = (self.menu_index + 1) % 3

                elif self.state == STATE_HUB:
                    if event.key == pygame.K_UP: self.menu_index = (self.menu_index - 1) % 6
                    if event.key == pygame.K_DOWN: self.menu_index = (self.menu_index + 1) % 6
                
                elif self.state == STATE_DUNG_SELECT:
                    if event.key == pygame.K_x: self.state = STATE_HUB
                    if event.key == pygame.K_UP: self.menu_index = (self.menu_index - 1) % 10
                    if event.key == pygame.K_DOWN: self.menu_index = (self.menu_index + 1) % 10
                
                elif self.state == STATE_SHOP:
                    if event.key == pygame.K_x: self.state = STATE_HUB
                    if event.key == pygame.K_UP: self.menu_index = (self.menu_index - 1) % 3
                    if event.key == pygame.K_DOWN: self.menu_index = (self.menu_index + 1) % 3

                elif self.state == STATE_SAVE_MENU:
                    if event.key == pygame.K_x: self.state = STATE_START 
                    if event.key == pygame.K_UP: self.menu_index = (self.menu_index - 1) % 3
                    if event.key == pygame.K_DOWN: self.menu_index = (self.menu_index + 1) % 3

                elif self.state == STATE_BATTLE and self.is_player_turn_ready:
                    limit = 4
                    if self.battle_menu_state == BATTLE_ATTACK_SELECT: limit = 3
                    elif self.battle_menu_state == BATTLE_SKILLS: limit = len(self.player.skills)
                    elif self.battle_menu_state == BATTLE_ITEM_SELECT: limit = 2
                    
                    if event.key == pygame.K_UP: self.menu_index = (self.menu_index - 1) % limit
                    if event.key == pygame.K_DOWN: self.menu_index = (self.menu_index + 1) % limit
                    
                    if event.key == pygame.K_x:
                        if self.battle_menu_state != BATTLE_MAIN:
                            self.battle_menu_state = BATTLE_MAIN; self.menu_index = 0

    def draw_button(self, text, x, y, index, active_color, inactive_color, font=None):
        if font is None: font = self.font
        is_selected = (self.menu_index == index)
        color = active_color if is_selected else inactive_color
        prefix = "> " if is_selected else "  "
        surf = font.render(prefix + text, True, color)
        rect = surf.get_rect(topleft=(x, y))
        self.screen.blit(surf, rect)
        mouse_pos = pygame.mouse.get_pos()
        if rect.collidepoint(mouse_pos):
            if self.menu_index != index: self.menu_index = index 
            if self.mouse_click_pos is not None: return True 
        if is_selected and self.key_pressed_enter: return True
        return False

    def start_battle(self, level):
        self.state = STATE_BATTLE
        self.active_battle_level = level
        self.enemy = generate_enemy(level)
        
        # --- SELECT BATTLE BACKGROUND ---
        # Look up the enemy type in our loaded backgrounds map.
        # If found, use it. If not, fallback to self.bg_battle_default.
        self.current_battle_bg = self.battle_backgrounds.get(self.enemy.char_type, self.bg_battle_default)

        self.floating_texts = []
        self.is_battle_active = True
        self.is_player_turn_ready = False
        self.player.atb = 0
        self.enemy.atb = 0
        self.battle_menu_state = BATTLE_MAIN
        self.menu_index = 0
        self.enemy_blocked_zones = []
        self.demon_barrier_active = False
        zones = [ZONE_UPPER, ZONE_MID, ZONE_LOWER]
        c_type = self.enemy.char_type
        if c_type in ["Goblin", "Chimera"]: self.enemy_blocked_zones = [random.choice(zones)]
        elif c_type in ["Orc", "Dark Knight", "Dragon"]:
            open_spot = random.choice(zones)
            self.enemy_blocked_zones = [z for z in zones if z != open_spot]
        elif c_type in ["Demon", "Demon Lord"]: self.demon_barrier_active = True
        self.mechanic_timer = self.mechanic_interval
        
        # Player is Animated Sprite
        self.player.sprite = AnimatedSprite(self.anim_manager, self.WIDTH * 0.25, self.HEIGHT * 0.6)
        self.player.sprite.set_animation("idle_down")
        
        # Enemy is Static Sprite (Using loaded image)
        enemy_img = self.enemy_images.get(c_type, self.enemy_images["Slime"]) # Fallback to Slime if missing
        self.enemy.sprite = StaticSprite(enemy_img, self.WIDTH * 0.75, self.HEIGHT * 0.55)

    def end_player_turn(self):
        self.player.atb = 0
        self.is_player_turn_ready = False
        self.battle_menu_state = BATTLE_MAIN
        self.is_battle_active = True 

    def execute_attack(self, zone):
        self.is_battle_active = False 
        if self.player.sprite: self.player.sprite.set_animation("attack_down", loop=False)
        damage_mult = 1.0
        popup_txt = ""; popup_col = WHITE
        c_type = self.enemy.char_type
        if c_type == "Slime": damage_mult = 1.2; popup_txt = "WEAK! "; popup_col = YELLOW
        elif c_type in ["Skeleton", "Golem"]: damage_mult = 0.0; popup_txt = "IMMUNE"; popup_col = GRAY
        elif c_type in ["Demon", "Demon Lord"]:
            if self.demon_barrier_active: damage_mult = 0.0; popup_txt = "BARRIER"; popup_col = PURPLE
            else: 
                if c_type == "Demon Lord" and zone in self.enemy_blocked_zones: damage_mult = 0.2; popup_txt = "BLOCKED"; popup_col = GRAY
                else: damage_mult = 1.0
        elif c_type in ["Goblin", "Orc", "Chimera", "Dark Knight", "Dragon"]:
            if zone in self.enemy_blocked_zones: damage_mult = 0.2; popup_txt = "BLOCKED"; popup_col = GRAY
            else: damage_mult = 1.5; popup_txt = "WEAK! "; popup_col = YELLOW
        raw_dmg = int(self.player.atk * damage_mult)
        dmg = self.enemy.take_damage(raw_dmg)
        if dmg > 0: popup_txt += str(dmg)
        elif popup_txt == "": popup_txt = "0"
        if self.enemy.sprite: self.spawn_popup(popup_txt, popup_col, self.enemy.sprite.x, self.enemy.sprite.y)
        if damage_mult > 0 and dmg > 0: self.add_screen_shake(0.2, 5)
        self.check_win()
        self.end_player_turn()

    def execute_skill(self, skill):
        if self.player.mp < skill.cost:
            if self.player.sprite: self.spawn_popup("NO MP!", BLUE, self.player.sprite.x, self.player.sprite.y)
            return
        self.is_battle_active = False
        self.player.mp -= skill.cost
        if self.player.sprite: self.player.sprite.set_animation("cast_down", loop=False)
        if skill.type == "heal":
            self.player.heal(skill.power)
            if self.player.sprite: self.spawn_popup(f"+{skill.power} HP", GREEN, self.player.sprite.x, self.player.sprite.y)
            self.check_win()
            self.end_player_turn()
            return
        damage = int(self.player.atk * skill.power)
        popup_txt = ""; popup_col = WHITE
        c_type = self.enemy.char_type
        if c_type in ["Skeleton", "Golem"] and skill.element == "magic":
            damage = int(damage * 2.0); popup_txt = "CRIT! "; popup_col = YELLOW; self.add_screen_shake(0.5, 15)
        if c_type in ["Demon", "Demon Lord"] and skill.element == "magic":
            if self.demon_barrier_active:
                self.demon_barrier_active = False; popup_txt = "SHATTERED! "; popup_col = RED; self.add_screen_shake(0.5, 15)
        dmg = self.enemy.take_damage(damage)
        popup_txt += str(dmg)
        if self.enemy.sprite: self.spawn_popup(popup_txt, popup_col, self.enemy.sprite.x, self.enemy.sprite.y)
        self.add_screen_shake(0.4, 10)
        self.check_win()
        self.end_player_turn()

    def execute_potion(self):
        if self.player.potions > 0:
             self.player.potions -= 1
             self.player.heal(50)
             if self.player.sprite: self.spawn_popup("+50 HP", GREEN, self.player.sprite.x, self.player.sprite.y)
             self.check_win()
             self.end_player_turn()
        else:
             if self.player.sprite: self.spawn_popup("NO POTIONS", GRAY, self.player.sprite.x, self.player.sprite.y)

    def execute_mana_potion(self):
        if self.player.mana_potions > 0:
             self.player.mana_potions -= 1
             self.player.mp = min(self.player.max_mp, self.player.mp + 30)
             if self.player.sprite: self.spawn_popup("+30 MP", BLUE, self.player.sprite.x, self.player.sprite.y)
             self.check_win()
             self.end_player_turn()
        else:
             if self.player.sprite: self.spawn_popup("NO MP POTIONS", GRAY, self.player.sprite.x, self.player.sprite.y)

    def check_win(self):
        if not self.enemy.is_alive:
             self.is_battle_active = False 
             # Enemy is static, no animation change needed
             self.add_screen_shake(0.8, 25)
             self.add_red_flash(255)
             pygame.time.set_timer(pygame.USEREVENT + 2, 1500, 1) 

    def trigger_victory_screen(self):
        if self.active_battle_level == self.current_dungeon_depth:
            if self.current_dungeon_depth < 10: self.current_dungeon_depth += 1
        self.player.gold += self.enemy.gold_reward
        leveled = self.player.gain_exp(self.enemy.exp_reward)
        self.victory_data = {"gold": self.enemy.gold_reward, "exp": self.enemy.exp_reward, "leveled": leveled}
        self.state = STATE_VICTORY
        if self.player.sprite: self.player.sprite.set_animation("idle_down")

    def enemy_attack_trigger(self):
        # Enemy is static, no animation call needed, maybe a shake?
        dmg = self.player.take_damage(self.enemy.atk)
        if self.player.sprite: self.spawn_popup(str(dmg), RED, self.player.sprite.x, self.player.sprite.y)
        self.add_red_flash(150)
        self.add_screen_shake(0.3, 10)
        if not self.player.is_alive:
            self.is_battle_active = False
            if self.player.sprite: self.player.sprite.set_animation("death", loop=False)
            return

    def add_screen_shake(self, d, i): self.screen_shake_duration = d; self.screen_shake_intensity = i
    def add_red_flash(self, a): self.red_flash_alpha = a
    
    def draw_hp_bar(self, surface, sprite_rect, current, max_val, color):
        if not sprite_rect: return
        bar_w, bar_h = 100, 10
        x = sprite_rect.centerx - bar_w // 2
        y = sprite_rect.top - 20 
        ratio = current / max_val
        pygame.draw.rect(surface, GRAY, (x, y, bar_w, bar_h))
        pygame.draw.rect(surface, color, (x, y, int(bar_w * ratio), bar_h))
        pygame.draw.rect(surface, WHITE, (x, y, bar_w, bar_h), 2)
    
    def draw_atb_bar(self, surface, sprite_rect, current, max_val):
        if not sprite_rect: return
        x = sprite_rect.centerx - ATB_BAR_WIDTH // 2
        y = sprite_rect.bottom + 10 
        ratio = current / max_val
        bar_color = CYAN
        if current >= max_val: bar_color = YELLOW
        pygame.draw.rect(surface, DARK_GRAY, (x, y, ATB_BAR_WIDTH, ATB_BAR_HEIGHT))
        pygame.draw.rect(surface, bar_color, (x, y, int(ATB_BAR_WIDTH * ratio), ATB_BAR_HEIGHT))
        pygame.draw.rect(surface, WHITE, (x, y, ATB_BAR_WIDTH, ATB_BAR_HEIGHT), 1)

    def draw_battle_hint(self):
        if not self.enemy or not self.enemy.is_alive: return
        hint = ""; color = WHITE
        c_type = self.enemy.char_type
        if c_type == "Slime": hint = "The Slime wobbles... Vulnerable everywhere."; color = CYAN
        elif c_type == "Goblin": blocked = self.enemy_blocked_zones[0]; hint = f"Goblin blocks {blocked.upper()}!"; color = YELLOW
        elif c_type in ["Orc", "Dark Knight", "Dragon"]:
            all_zones = [ZONE_UPPER, ZONE_MID, ZONE_LOWER]
            open_zone = [z for z in all_zones if z not in self.enemy_blocked_zones][0]
            if open_zone.upper() == "HIGH":
                hint = f"Heavy Guard! HEAD exposed!"; color = ORANGE
            if open_zone.upper() == "MID":
                hint = f"Heavy Guard! TORSO exposed!"; color = ORANGE
            if open_zone.upper() == "LOW":
                hint = f"Heavy Guard! LEGS exposed!"; color = ORANGE
        elif c_type == "Chimera": blocked = self.enemy_blocked_zones[0]; hint = f"The Chimera guards {blocked.upper()} with its tail!"; color = ORANGE
        elif c_type in ["Skeleton", "Golem"]: hint = "Armor is too thick...."; color = GRAY
        elif c_type in ["Demon", "Demon Lord"]:
            if self.demon_barrier_active: hint = "Dark Shield Active!"; color = PURPLE
            else: 
                if c_type == "Demon Lord":
                    all_zones = [ZONE_UPPER, ZONE_MID, ZONE_LOWER]
                    open_zone = [z for z in all_zones if z not in self.enemy_blocked_zones][0]
                    if open_zone.upper() == "HIGH":
                        hint = f"Barrier Down! He guards fast! His HEAD is exposed!"; color = RED
                    if open_zone.upper() == "MID":
                        hint = f"Barrier Down! He guards fast! His TORSO is exposed!"; color = RED
                    if open_zone.upper() == "LOW":
                        hint = f"Barrier Down! He guards fast! His LEGS are exposed!"; color = RED
                else: hint = "Shield Shattered! Attack now!"; color = RED
        if hint:
            lbl = self.font.render(hint, True, color)
            bg_rect = lbl.get_rect(center=(self.WIDTH//2, 80))
            pygame.draw.rect(self.screen, BLACK, bg_rect.inflate(30, 10))
            pygame.draw.rect(self.screen, WHITE, bg_rect.inflate(30, 10), 2)
            self.screen.blit(lbl, bg_rect)

    def draw_battle(self):
        # --- DRAW BATTLE BACKGROUND ---
        # If the specific BG for this enemy exists, use it.
        # Otherwise, fall back to default or a solid color.
        if self.current_battle_bg:
            ox = random.randint(-self.screen_shake_intensity, self.screen_shake_intensity) if self.screen_shake_duration > 0 else 0
            oy = random.randint(-self.screen_shake_intensity, self.screen_shake_intensity) if self.screen_shake_duration > 0 else 0
            self.screen.blit(self.current_battle_bg, (ox, oy))
        else: 
            self.screen.fill((40, 20, 20))

        self.draw_battle_hint()
        p_rect = None; e_rect = None
        if self.player.sprite: p_rect = self.player.sprite.draw(self.screen)
        if self.enemy.sprite: e_rect = self.enemy.sprite.draw(self.screen)
        
        if p_rect and self.player.is_alive: 
            self.draw_hp_bar(self.screen, p_rect, self.player.hp, self.player.max_hp, GREEN)
            self.draw_atb_bar(self.screen, p_rect, self.player.atb, ATB_MAX)
        
        if e_rect and self.enemy.is_alive: 
            self.draw_hp_bar(self.screen, e_rect, self.enemy.hp, self.enemy.max_hp, RED)
            # Draw Enemy Name
            name_surf = self.small_font.render(self.enemy.name, True, WHITE)
            outline_surf = self.small_font.render(self.enemy.name, True, BLACK)
            name_rect = name_surf.get_rect(midtop=(e_rect.centerx, e_rect.bottom - 40))
            self.screen.blit(outline_surf, (name_rect.x + 2, name_rect.y + 2))
            self.screen.blit(name_surf, name_rect)
        
        for txt in self.floating_texts: txt.draw(self.screen)

        ui_y = self.HEIGHT - 250
        pygame.draw.rect(self.screen, BLACK, (0, ui_y, self.WIDTH, 250))
        pygame.draw.rect(self.screen, WHITE, (0, ui_y, self.WIDTH, 250), 3)
        self.screen.blit(self.font.render(f"{self.player.name} (Lv.{self.player.level})", True, WHITE), (50, ui_y + 30))
        self.screen.blit(self.font.render(f"MP: {self.player.mp}/{self.player.max_mp}", True, BLUE), (50, ui_y + 80))
        self.screen.blit(self.font.render(f"Potions: {self.player.potions}", True, YELLOW), (50, ui_y + 130))
        self.screen.blit(self.font.render(f"Mana Pots: {self.player.mana_potions}", True, CYAN), (50, ui_y + 165))
        
        menu_x = self.WIDTH // 2 - 100
        
        # Only draw menu if player turn is ready
        if self.is_player_turn_ready and self.is_battle_active:
            if self.battle_menu_state == BATTLE_MAIN:
                opts = ["Attack", "Skills", "Items", "Flee"]
                for i, o in enumerate(opts):
                    # We check return value. If True, action taken.
                    if self.draw_button(o, menu_x, ui_y + 30 + i*50, i, YELLOW, GRAY):
                        if i == 0: 
                            self.battle_menu_state = BATTLE_ATTACK_SELECT
                            self.menu_index = 1
                        elif i == 1: 
                            self.battle_menu_state = BATTLE_SKILLS
                            self.menu_index = 0
                        elif i == 2: 
                            self.battle_menu_state = BATTLE_ITEM_SELECT
                            self.menu_index = 0
                        elif i == 3: 
                            self.state = STATE_HUB
                        # CRITICAL FIX: Break loop so we don't process other buttons with the new index
                        break 

            elif self.battle_menu_state == BATTLE_ATTACK_SELECT:
                self.screen.blit(self.small_font.render("SELECT ZONE (X to BACK)", True, WHITE), (menu_x, ui_y + 10))
                opts = ["High Strike", "Mid Strike", "Low Strike"]
                zones = [ZONE_UPPER, ZONE_MID, ZONE_LOWER]
                for i, o in enumerate(opts):
                    if self.draw_button(o, menu_x, ui_y + 40 + i*50, i, ORANGE, GRAY):
                        self.execute_attack(zones[i])
                        break # Break loop

            elif self.battle_menu_state == BATTLE_SKILLS:
                self.screen.blit(self.small_font.render("SELECT SKILL (X to BACK)", True, WHITE), (menu_x, ui_y + 10))
                for i, sk in enumerate(self.player.skills):
                    color = YELLOW
                    if self.player.mp < sk.cost: color = DARK_GRAY
                    if self.draw_button(f"{sk.name} ({sk.cost} MP)", menu_x, ui_y + 40 + i*50, i, color, GRAY):
                        self.execute_skill(sk)
                        break # Break loop
            
            elif self.battle_menu_state == BATTLE_ITEM_SELECT:
                self.screen.blit(self.small_font.render("SELECT ITEM (X to BACK)", True, WHITE), (menu_x, ui_y + 10))
                
                # Health Potion Button
                hp_txt = f"Health Potion ({self.player.potions})"
                if self.draw_button(hp_txt, menu_x, ui_y + 40, 0, GREEN, GRAY):
                    self.execute_potion()
                
                # Mana Potion Button
                mp_txt = f"Mana Potion ({self.player.mana_potions})"
                if self.draw_button(mp_txt, menu_x, ui_y + 90, 1, BLUE, GRAY):
                    self.execute_mana_potion()

        if self.red_flash_alpha > 0:
            flash = pygame.Surface((self.WIDTH, self.HEIGHT))
            flash.fill(RED); flash.set_alpha(int(self.red_flash_alpha))
            self.screen.blit(flash, (0,0))

    def draw_victory_screen(self):
        self.screen.fill((0, 50, 0))
        title = self.title_font.render("VICTORY!", True, YELLOW)
        self.screen.blit(title, (self.WIDTH//2 - title.get_width()//2, self.HEIGHT * 0.2))
        gold_txt = self.font.render(f"Gold Gained: {self.victory_data['gold']}", True, WHITE)
        exp_txt = self.font.render(f"Experience: {self.victory_data['exp']}", True, WHITE)
        self.screen.blit(gold_txt, (self.WIDTH//2 - gold_txt.get_width()//2, self.HEIGHT * 0.4))
        self.screen.blit(exp_txt, (self.WIDTH//2 - exp_txt.get_width()//2, self.HEIGHT * 0.5))
        if self.victory_data['leveled']:
            lvl_txt = self.font.render("LEVEL UP! Stats Increased!", True, GREEN)
            self.screen.blit(lvl_txt, (self.WIDTH//2 - lvl_txt.get_width()//2, self.HEIGHT * 0.6))
        if self.draw_button("Continue", self.WIDTH//2 - 100, self.HEIGHT * 0.8, 0, YELLOW, GRAY, font=self.small_font): self.state = STATE_HUB

    def draw_game_over(self):
        self.screen.fill(BLACK)
        title = self.title_font.render("GAME OVER", True, RED)
        self.screen.blit(title, (self.WIDTH//2 - title.get_width()//2, self.HEIGHT * 0.3))
        sub = self.font.render("You have fallen in battle...", True, WHITE)
        self.screen.blit(sub, (self.WIDTH//2 - sub.get_width()//2, self.HEIGHT * 0.5))
        if self.draw_button("Load Game", self.WIDTH//2 - 100, self.HEIGHT * 0.7, 0, YELLOW, GRAY, font=self.small_font):
             self.is_saving = False; self.state = STATE_SAVE_MENU

    def draw_stats_screen(self):
        if self.bg_hub: self.screen.blit(self.bg_hub, (0,0))
        overlay = pygame.Surface((self.WIDTH, self.HEIGHT))
        overlay.fill(BLACK); overlay.set_alpha(200)
        self.screen.blit(overlay, (0,0))
        title = self.title_font.render("HERO STATISTICS", True, WHITE)
        self.screen.blit(title, (self.WIDTH//2 - title.get_width()//2, 100))
        p = self.player
        stats = [
            f"Name: {p.name}", f"Level: {p.level}", f"EXP: {p.exp} / {p.exp_to_next}", 
            f"HP: {p.hp} / {p.max_hp}", f"MP: {p.mp} / {p.max_mp}", f"Attack: {p.atk}", 
            f"Defense: {p.defense}", f"Speed: {p.speed}", f"Gold: {p.gold}", 
            f"HP Potions: {p.potions}", f"MP Potions: {p.mana_potions}"
        ]
        start_y = 250
        for i, s in enumerate(stats):
            txt = self.font.render(s, True, YELLOW if i % 2 == 0 else WHITE)
            self.screen.blit(txt, (self.WIDTH//2 - 200, start_y + i * 50))
        if self.draw_button("Return", self.WIDTH//2 - 50, self.HEIGHT - 100, 0, GRAY, WHITE, font=self.small_font): self.state = STATE_HUB

    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000.0
            if self.screen_shake_duration > 0: self.screen_shake_duration -= dt
            if self.red_flash_alpha > 0: self.red_flash_alpha -= dt * 300
            
            if self.state == STATE_BATTLE:
                self.update_atb(dt)
                self.update_battle_mechanics(dt)
                if self.player.sprite: 
                    self.player.sprite.update(dt)
                    if self.player.sprite.animation_finished and self.player.sprite.current_animation in ["attack_down", "cast_down"]:
                        self.player.sprite.set_animation("idle_down")
                if self.enemy.sprite: 
                    self.enemy.sprite.update(dt)
                    # Enemy is static, no animation check needed
                if not self.player.is_alive and self.player.sprite and self.player.sprite.animation_finished:
                     pygame.time.delay(1000)
                     self.state = STATE_GAME_OVER
            
            self.handle_input()
            
            if self.state == STATE_START:
                if self.bg_start: self.screen.blit(self.bg_start, (0,0))
                else: self.screen.fill(BLACK)
                t = self.title_font.render("HERO'S JOURNEY", True, YELLOW)
                self.screen.blit(t, (self.WIDTH//2 - t.get_width()//2, self.HEIGHT * 0.2))
                opts = ["New Game", "Load Game", "Quit"]
                for i, o in enumerate(opts):
                    if self.draw_button(o, self.WIDTH//2 - 100, self.HEIGHT * 0.5 + i*60, i, YELLOW, GRAY):
                        if i == 0: self.reset_game()
                        elif i == 1: self.is_saving = False; self.state = STATE_SAVE_MENU
                        elif i == 2: pygame.quit(); sys.exit()

            elif self.state == STATE_HUB:
                if self.bg_hub: self.screen.blit(self.bg_hub, (0,0))
                else: self.screen.fill((30, 30, 40))
                self.screen.blit(self.title_font.render("Village", True, WHITE), (100, 100))
                ops = ["Enter Dungeon", "Shop", "Heal (10g)", "Stats", "Save", "Quit"]
                for i, o in enumerate(ops):
                    if self.draw_button(o, 100, 300 + i*60, i, CYAN, GRAY):
                        if i == 0: self.menu_index = 0; self.state = STATE_DUNG_SELECT
                        elif i == 1: self.state = STATE_SHOP
                        elif i == 2: 
                             if self.player.gold >= 10: self.player.gold -= 10; self.player.heal(999); self.player.mp = self.player.max_mp
                        elif i == 3: self.state = STATE_STATS
                        elif i == 4: self.is_saving = True; self.state = STATE_SAVE_MENU
                        elif i == 5: self.state = STATE_START
                stats = f"HP:{self.player.hp} | Gold:{self.player.gold}"
                self.screen.blit(self.small_font.render(stats, True, YELLOW), (20, 20))

            elif self.state == STATE_STATS: self.draw_stats_screen()
            
            elif self.state == STATE_DUNG_SELECT:
                self.screen.fill(BLACK)
                self.screen.blit(self.title_font.render("Select Demon Castle Floor", True, RED), (100, 100))
                for i in range(10):
                    level_num = i + 1
                    is_locked = level_num > self.current_dungeon_depth
                    txt = f"Level {level_num} [LOCKED]" if is_locked else f"Level {level_num}"
                    color = DARK_GRAY if is_locked else (RED if self.menu_index == i else GRAY)
                    x = 100 if i < 5 else 600
                    y = 300 + (i % 5) * 60
                    if self.draw_button(txt, x, y, i, RED, color):
                         if not is_locked: self.start_battle(level_num)

            elif self.state == STATE_SHOP:
                if self.bg_shop: self.screen.blit(self.bg_shop, (0,0))
                else: self.screen.fill((50, 40, 20))
                self.screen.blit(self.title_font.render("SHOP", True, YELLOW), (100, 50))
                ops = [
                    f"Health Potion (50g) [{self.player.potions}]", 
                    f"Mana Potion (50g) [{self.player.mana_potions}]", 
                    f"Upgrade Sword (200g) [{self.player.atk}]"
                ]
                for i, o in enumerate(ops):
                    if self.draw_button(o, 100, 300 + i*80, i, GREEN, GRAY):
                        # Health Pot
                        if i == 0 and self.player.gold >= 50: self.player.gold -= 50; self.player.potions += 1
                        # Mana Pot
                        elif i == 1 and self.player.gold >= 50: self.player.gold -= 50; self.player.mana_potions += 1
                        # Upgrade Sword
                        elif i == 2 and self.player.gold >= 200: self.player.gold -= 200; self.player.atk += 5

            elif self.state == STATE_SAVE_MENU:
                self.screen.fill((20, 20, 50))
                title_txt = "SAVE GAME" if self.is_saving else "LOAD GAME"
                self.screen.blit(self.title_font.render(title_txt, True, WHITE), (100, 50))
                for i in range(3):
                    if self.draw_button(f"Slot {i+1}", 100, 300 + i*80, i, PURPLE, GRAY):
                        if self.is_saving: self.save_game(i); self.state = STATE_HUB
                        else: 
                            if self.load_game(i): self.state = STATE_HUB

            elif self.state == STATE_BATTLE: self.draw_battle()
            elif self.state == STATE_VICTORY: self.draw_victory_screen()
            elif self.state == STATE_GAME_OVER: self.draw_game_over()
            pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()