"""
Fake News Roulette - Un gioco educativo per imparare a distinguere notizie vere da fake news
"""

import pygame
import json
import random
import math
import os
from typing import List, Dict, Tuple, Optional

# Inizializzazione Pygame
pygame.init()

# Costanti
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

# Colori - Enhanced palette
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 50, 50)
GREEN = (50, 200, 50)
BLUE = (50, 120, 220)
YELLOW = (255, 215, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)
ORANGE = (255, 165, 0)

# Enhanced colors
GRADIENT_TOP = (240, 248, 255)  # Alice Blue
GRADIENT_BOTTOM = (176, 224, 230)  # Powder Blue
BUTTON_SHADOW = (80, 80, 80)
TEXT_SHADOW = (100, 100, 100)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
BRONZE = (205, 127, 50)

# Colori per le categorie - Enhanced with gradients
CATEGORY_COLORS = {
    "Politica": (230, 100, 100),
    "Scienza": (100, 150, 230),
    "Tecnologia": (150, 100, 230),
    "Salute": (100, 230, 150),
    "Intrattenimento": (230, 200, 100),
    "Economia": (230, 150, 100)
}

# Darker versions for gradients
CATEGORY_COLORS_DARK = {
    "Politica": (180, 70, 70),
    "Scienza": (70, 110, 180),
    "Tecnologia": (110, 70, 180),
    "Salute": (70, 180, 110),
    "Intrattenimento": (180, 160, 70),
    "Economia": (180, 110, 70)
}


def draw_gradient_rect(surface: pygame.Surface, rect: pygame.Rect, color_top: Tuple[int, int, int], 
                       color_bottom: Tuple[int, int, int], border_radius: int = 0):
    """Disegna un rettangolo con gradiente verticale"""
    for y in range(rect.height):
        ratio = y / rect.height
        color = tuple(int(color_top[i] * (1 - ratio) + color_bottom[i] * ratio) for i in range(3))
        pygame.draw.line(surface, color, (rect.x, rect.y + y), (rect.x + rect.width, rect.y + y))
    
    if border_radius > 0:
        # Smooth corners with alpha blending
        s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.rect(s, (*color_top, 0), s.get_rect(), border_radius=border_radius)
        surface.blit(s, rect.topleft, special_flags=pygame.BLEND_RGBA_MIN)


def draw_text_with_shadow(surface: pygame.Surface, text: str, font: pygame.font.Font, 
                          pos: Tuple[int, int], color: Tuple[int, int, int], 
                          shadow_color: Tuple[int, int, int] = TEXT_SHADOW, 
                          shadow_offset: int = 3, center: bool = True):
    """Disegna testo con ombra per migliore leggibilità"""
    # Ombra
    shadow_surf = font.render(text, True, shadow_color)
    if center:
        shadow_rect = shadow_surf.get_rect(center=(pos[0] + shadow_offset, pos[1] + shadow_offset))
    else:
        shadow_rect = shadow_surf.get_rect(topleft=(pos[0] + shadow_offset, pos[1] + shadow_offset))
    surface.blit(shadow_surf, shadow_rect)
    
    # Testo principale
    text_surf = font.render(text, True, color)
    if center:
        text_rect = text_surf.get_rect(center=pos)
    else:
        text_rect = text_surf.get_rect(topleft=pos)
    surface.blit(text_surf, text_rect)
    
    return text_rect


def draw_rounded_rect_with_shadow(surface: pygame.Surface, rect: pygame.Rect, color: Tuple[int, int, int],
                                  border_radius: int = 10, shadow_offset: int = 5):
    """Disegna un rettangolo arrotondato con ombra"""
    # Ombra
    shadow_rect = rect.copy()
    shadow_rect.x += shadow_offset
    shadow_rect.y += shadow_offset
    shadow_surf = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)
    pygame.draw.rect(shadow_surf, (*BUTTON_SHADOW, 100), shadow_surf.get_rect(), border_radius=border_radius)
    surface.blit(shadow_surf, shadow_rect.topleft)
    
    # Rettangolo principale
    pygame.draw.rect(surface, color, rect, border_radius=border_radius)


def draw_gradient_background(surface: pygame.Surface):
    """Disegna uno sfondo con gradiente moderno"""
    width, height = surface.get_size()
    for y in range(height):
        ratio = y / height
        color = tuple(int(GRADIENT_TOP[i] * (1 - ratio) + GRADIENT_BOTTOM[i] * ratio) for i in range(3))
        pygame.draw.line(surface, color, (0, y), (width, y))


class Button:
    """Classe per gestire i pulsanti grafici con effetti migliorati"""
    
    def __init__(self, x: int, y: int, width: int, height: int, text: str, 
                 color: Tuple[int, int, int], text_color: Tuple[int, int, int] = WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.hover_color = tuple(min(c + 40, 255) for c in color)
        self.color_dark = tuple(max(c - 30, 0) for c in color)
        self.is_hovered = False
        self.press_offset = 0
        
    def draw(self, screen: pygame.Surface, font: pygame.font.Font):
        """Disegna il pulsante con effetti 3D e ombra"""
        color = self.hover_color if self.is_hovered else self.color
        
        # Calcola offset per effetto pressione
        offset = 3 if self.is_hovered else 0
        draw_rect = self.rect.copy()
        draw_rect.y += offset
        
        # Disegna ombra
        if not self.is_hovered:
            shadow_rect = draw_rect.copy()
            shadow_rect.y += 5
            shadow_surf = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(shadow_surf, (*BUTTON_SHADOW, 120), shadow_surf.get_rect(), border_radius=10)
            screen.blit(shadow_surf, shadow_rect.topleft)
        
        # Gradiente per il pulsante
        gradient_surf = pygame.Surface((draw_rect.width, draw_rect.height), pygame.SRCALPHA)
        for y in range(draw_rect.height):
            ratio = y / draw_rect.height
            grad_color = tuple(int(color[i] * (1 - ratio * 0.3) + self.color_dark[i] * (ratio * 0.3)) for i in range(3))
            pygame.draw.line(gradient_surf, grad_color, (0, y), (draw_rect.width, y))
        
        # Applica il gradiente
        temp_surf = pygame.Surface((draw_rect.width, draw_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(temp_surf, WHITE, temp_surf.get_rect(), border_radius=10)
        gradient_surf.blit(temp_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
        screen.blit(gradient_surf, draw_rect.topleft)
        
        # Bordo
        pygame.draw.rect(screen, BLACK, draw_rect, 3, border_radius=10)
        
        # Highlight in alto per effetto 3D
        highlight_rect = pygame.Rect(draw_rect.x + 5, draw_rect.y + 5, draw_rect.width - 10, draw_rect.height // 4)
        highlight_surf = pygame.Surface((highlight_rect.width, highlight_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(highlight_surf, (*WHITE, 60), highlight_surf.get_rect(), border_radius=8)
        screen.blit(highlight_surf, highlight_rect.topleft)
        
        # Testo con ombra
        draw_text_with_shadow(screen, self.text, font, draw_rect.center, self.text_color, 
                            shadow_offset=2, center=True)
        
    def check_hover(self, mouse_pos: Tuple[int, int]):
        """Verifica se il mouse è sopra il pulsante"""
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
    def is_clicked(self, mouse_pos: Tuple[int, int]) -> bool:
        """Verifica se il pulsante è stato cliccato"""
        return self.rect.collidepoint(mouse_pos)


class Roulette:
    """Classe per gestire la roulette delle categorie"""
    
    def __init__(self, x: int, y: int, radius: int, categories: List[str]):
        self.x = x
        self.y = y
        self.radius = radius
        self.categories = categories
        self.angle = 0
        self.spinning = False
        self.spin_speed = 0
        self.target_angle = 0
        self.selected_category = None
        
    def start_spin(self):
        """Inizia la rotazione della roulette"""
        self.spinning = True
        # Velocità iniziale casuale
        self.spin_speed = random.uniform(20, 30)
        # Angolo target casuale
        rotations = random.randint(3, 6)
        self.target_angle = self.angle + (360 * rotations) + random.uniform(0, 360)
        
    def update(self):
        """Aggiorna la rotazione della roulette"""
        if self.spinning:
            # Decelerazione graduale
            self.angle += self.spin_speed
            self.spin_speed *= 0.97
            
            # Ferma quando la velocità è molto bassa
            if self.spin_speed < 0.1:
                self.spinning = False
                self.angle = self.angle % 360
                # Determina la categoria selezionata
                sector_size = 360 / len(self.categories)
                # L'indicatore è in alto, quindi usiamo l'angolo opposto
                index = int(((360 - self.angle + 90) % 360) / sector_size) % len(self.categories)
                self.selected_category = self.categories[index]
                
    def draw(self, screen: pygame.Surface, font: pygame.font.Font):
        """Disegna la roulette con effetti 3D e ombra"""
        # Ombra della roulette
        shadow_offset = 8
        shadow_surf = pygame.Surface((self.radius * 2 + 40, self.radius * 2 + 40), pygame.SRCALPHA)
        pygame.draw.circle(shadow_surf, (*BUTTON_SHADOW, 80), 
                         (self.radius + 20, self.radius + 20), self.radius + 5)
        screen.blit(shadow_surf, (self.x - self.radius - 20 + shadow_offset, 
                                 self.y - self.radius - 20 + shadow_offset))
        
        # Disegna i settori con gradiente
        num_categories = len(self.categories)
        sector_angle = 360 / num_categories
        
        for i, category in enumerate(self.categories):
            start_angle = math.radians(i * sector_angle + self.angle)
            end_angle = math.radians((i + 1) * sector_angle + self.angle)
            
            # Colori del settore (chiaro e scuro per gradiente)
            color = CATEGORY_COLORS.get(category, GRAY)
            color_dark = CATEGORY_COLORS_DARK.get(category, DARK_GRAY)
            
            # Disegna il settore con gradiente radiale
            for radius_step in range(20):
                ratio = radius_step / 20
                current_radius = self.radius * (0.2 + 0.8 * ratio)
                grad_color = tuple(int(color[j] * (1 - ratio * 0.4) + color_dark[j] * (ratio * 0.4)) 
                                 for j in range(3))
                
                points = [(self.x, self.y)]
                for angle in [start_angle + k * 0.1 for k in range(11)]:
                    px = self.x + current_radius * math.cos(angle)
                    py = self.y + current_radius * math.sin(angle)
                    points.append((px, py))
                
                if len(points) > 2:
                    pygame.draw.polygon(screen, grad_color, points)
            
            # Bordo del settore
            points = [(self.x, self.y)]
            for angle in [start_angle + j * 0.05 for j in range(21)]:
                px = self.x + self.radius * math.cos(angle)
                py = self.y + self.radius * math.sin(angle)
                points.append((px, py))
            pygame.draw.polygon(screen, BLACK, points, 3)
            
            # Disegna il testo della categoria con ombra
            mid_angle = (start_angle + end_angle) / 2
            text_distance = self.radius * 0.65
            text_x = self.x + text_distance * math.cos(mid_angle)
            text_y = self.y + text_distance * math.sin(mid_angle)
            
            # Testo con outline per migliore leggibilità
            text_surface = font.render(category, True, WHITE)
            outline_surface = font.render(category, True, BLACK)
            
            # Disegna outline
            for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                outline_rect = outline_surface.get_rect(center=(text_x + dx, text_y + dy))
                screen.blit(outline_surface, outline_rect)
            
            # Disegna testo principale
            text_rect = text_surface.get_rect(center=(text_x, text_y))
            screen.blit(text_surface, text_rect)
        
        # Cerchio centrale decorativo
        pygame.draw.circle(screen, GOLD, (self.x, self.y), 30)
        pygame.draw.circle(screen, BLACK, (self.x, self.y), 30, 4)
        pygame.draw.circle(screen, YELLOW, (self.x, self.y), 20)
        pygame.draw.circle(screen, BLACK, (self.x, self.y), 20, 2)
        
        # Disegna il cerchio esterno con effetto metallico
        for i in range(4):
            radius_offset = self.radius + i
            alpha = 255 - i * 40
            pygame.draw.circle(screen, BLACK, (self.x, self.y), radius_offset, 2)
        
        # Disegna l'indicatore migliorato (triangolo in alto)
        indicator_size = 25
        indicator_points = [
            (self.x, self.y - self.radius - 35),
            (self.x - indicator_size, self.y - self.radius - 10),
            (self.x + indicator_size, self.y - self.radius - 10)
        ]
        
        # Ombra indicatore
        shadow_points = [(p[0] + 2, p[1] + 2) for p in indicator_points]
        pygame.draw.polygon(screen, BUTTON_SHADOW, shadow_points)
        
        # Gradiente per l'indicatore
        pygame.draw.polygon(screen, (255, 80, 80), indicator_points)
        pygame.draw.polygon(screen, RED, indicator_points)
        pygame.draw.polygon(screen, BLACK, indicator_points, 3)
        
        # Highlight sull'indicatore
        highlight_point = (self.x, self.y - self.radius - 28)
        pygame.draw.circle(screen, (255, 150, 150), highlight_point, 5)


class PenaltyAnimation:
    """Gestisce l'animazione della penalità in stile roulette russa"""
    
    def __init__(self):
        self.active = False
        self.penalty_type = None
        self.timer = 0
        self.duration = 120  # 2 secondi a 60 FPS
        
    def start(self, penalty_type: str):
        """Inizia l'animazione della penalità"""
        self.active = True
        self.penalty_type = penalty_type
        self.timer = 0
        
    def update(self):
        """Aggiorna l'animazione"""
        if self.active:
            self.timer += 1
            if self.timer >= self.duration:
                self.active = False
                
    def draw(self, screen: pygame.Surface, font_large: pygame.font.Font, font_medium: pygame.font.Font):
        """Disegna l'animazione della penalità con effetti migliorati"""
        if not self.active:
            return
            
        # Sfondo semi-trasparente con pulsazione
        alpha = int(180 + 40 * math.sin(self.timer * 0.3))
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(alpha)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        # Box centrale per la penalità
        box_width = 700
        box_height = 250
        penalty_box = pygame.Rect(SCREEN_WIDTH // 2 - box_width // 2, 
                                  SCREEN_HEIGHT // 2 - box_height // 2, 
                                  box_width, box_height)
        
        # Animazione pulsante per il box
        scale = 1 + 0.08 * math.sin(self.timer * 0.25)
        scaled_box = pygame.Rect(
            penalty_box.centerx - int(penalty_box.width * scale / 2),
            penalty_box.centery - int(penalty_box.height * scale / 2),
            int(penalty_box.width * scale),
            int(penalty_box.height * scale)
        )
        
        # Ombra del box
        shadow_box = scaled_box.copy()
        shadow_box.x += 10
        shadow_box.y += 10
        shadow_surf = pygame.Surface((shadow_box.width, shadow_box.height), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surf, (*BUTTON_SHADOW, 150), shadow_surf.get_rect(), border_radius=20)
        screen.blit(shadow_surf, shadow_box.topleft)
        
        # Box principale con gradiente
        draw_rounded_rect_with_shadow(screen, scaled_box, (40, 40, 40), border_radius=20, shadow_offset=0)
        
        # Testo della penalità con icone
        penalty_data = {
            "points": ("💸 PERDITA DI PUNTI! 💸", ORANGE),
            "life": ("💔 PERDITA DI UNA VITA! 💔", RED),
            "timeout": ("⏸️  BLOCCO TEMPORANEO! ⏸️", ORANGE),
            "game_over": ("💀 GAME OVER! 💀", RED)
        }
        
        text, color = penalty_data.get(self.penalty_type, ("⚠️  PENALITÀ! ⚠️", ORANGE))
        
        # Testo principale con scala e ombra
        text_scale = 1 + 0.12 * math.sin(self.timer * 0.2)
        
        # Ombra del testo
        shadow_surf = font_large.render(text, True, BLACK)
        shadow_rect = shadow_surf.get_rect(center=(scaled_box.centerx + 4, scaled_box.centery - 20 + 4))
        screen.blit(shadow_surf, shadow_rect)
        
        # Testo principale
        text_surface = font_large.render(text, True, color)
        text_rect = text_surface.get_rect(center=(scaled_box.centerx, scaled_box.centery - 20))
        
        # Applica scala con rotazione leggera
        angle = math.sin(self.timer * 0.15) * 5
        scaled_surface = pygame.transform.rotozoom(text_surface, angle, text_scale)
        scaled_rect = scaled_surface.get_rect(center=text_rect.center)
        screen.blit(scaled_surface, scaled_rect)
        
        # Sottotesto decorativo
        if self.penalty_type == "points":
            subtext = "-50 punti"
        elif self.penalty_type == "life":
            subtext = "❤️ → 🖤"
        elif self.penalty_type == "timeout":
            subtext = "10 secondi di attesa"
        elif self.penalty_type == "game_over":
            subtext = "Partita terminata"
        else:
            subtext = "Risposta errata!"
            
        subtext_surf = font_medium.render(subtext, True, WHITE)
        subtext_rect = subtext_surf.get_rect(center=(scaled_box.centerx, scaled_box.centery + 50))
        screen.blit(subtext_surf, subtext_rect)
        
        # Bordo luminoso pulsante
        border_alpha = int(150 + 100 * math.sin(self.timer * 0.4))
        border_surf = pygame.Surface((scaled_box.width, scaled_box.height), pygame.SRCALPHA)
        pygame.draw.rect(border_surf, (*color, border_alpha), border_surf.get_rect(), 6, border_radius=20)
        screen.blit(border_surf, scaled_box.topleft)


class FakeNewsRoulette:
    """Classe principale del gioco"""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Fake News Roulette")
        self.clock = pygame.time.Clock()
        
        # Font
        self.font_small = pygame.font.Font(None, 24)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_large = pygame.font.Font(None, 64)
        self.font_title = pygame.font.Font(None, 72)
        
        # Carica il database delle notizie
        self.load_news_database()
        
        # Stato del gioco
        self.state = "menu"  # menu, spinning, question, feedback, penalty, game_over
        self.score = 0
        self.lives = 3
        self.errors = 0
        self.current_category = None
        self.current_news = None
        self.feedback_timer = 0
        self.timeout_timer = 0
        
        # Componenti
        categories = list(self.news_database["categories"].keys())
        self.roulette = Roulette(SCREEN_WIDTH // 2, 300, 200, categories)
        self.penalty_animation = PenaltyAnimation()
        
        # Pulsanti
        self.create_buttons()
        
        # Leaderboard
        self.leaderboard = self.load_leaderboard()
        
    def load_news_database(self):
        """Carica il database delle notizie dal file JSON"""
        try:
            with open("news_database.json", "r", encoding="utf-8") as f:
                self.news_database = json.load(f)
        except FileNotFoundError:
            print("Errore: file news_database.json non trovato!")
            pygame.quit()
            exit(1)
            
    def load_leaderboard(self) -> List[Dict]:
        """Carica la classifica da file"""
        if os.path.exists("leaderboard.json"):
            try:
                with open("leaderboard.json", "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return []
        return []
        
    def save_leaderboard(self):
        """Salva la classifica su file"""
        with open("leaderboard.json", "w", encoding="utf-8") as f:
            json.dump(self.leaderboard, f, indent=2)
            
    def add_to_leaderboard(self, score: int):
        """Aggiunge un punteggio alla classifica"""
        self.leaderboard.append({"score": score})
        self.leaderboard.sort(key=lambda x: x["score"], reverse=True)
        self.leaderboard = self.leaderboard[:10]  # Mantieni solo i top 10
        self.save_leaderboard()
        
    def create_buttons(self):
        """Crea i pulsanti per l'interfaccia"""
        # Pulsanti del menu
        self.btn_start = Button(SCREEN_WIDTH // 2 - 100, 400, 200, 60, "INIZIA", GREEN)
        self.btn_quit = Button(SCREEN_WIDTH // 2 - 100, 480, 200, 60, "ESCI", RED)
        
        # Pulsanti per le risposte
        self.btn_true = Button(SCREEN_WIDTH // 2 - 250, 650, 200, 60, "VERA", GREEN)
        self.btn_false = Button(SCREEN_WIDTH // 2 + 50, 650, 200, 60, "FALSA", RED)
        
        # Pulsante per continuare
        self.btn_continue = Button(SCREEN_WIDTH // 2 - 100, 700, 200, 50, "CONTINUA", BLUE)
        
        # Pulsante per tornare al menu
        self.btn_menu = Button(SCREEN_WIDTH // 2 - 100, 650, 200, 50, "MENU", BLUE)
        
    def reset_game(self):
        """Resetta il gioco per una nuova partita"""
        self.score = 0
        self.lives = 3
        self.errors = 0
        self.current_category = None
        self.current_news = None
        self.state = "spinning"
        self.roulette.start_spin()
        
    def select_random_news(self):
        """Seleziona una notizia casuale dalla categoria corrente"""
        if self.current_category:
            category_news = self.news_database["categories"][self.current_category]
            self.current_news = random.choice(category_news)
            
    def apply_penalty(self):
        """Applica una penalità casuale per una risposta sbagliata"""
        penalties = ["points", "life", "timeout", "game_over"]
        # Pesi per le penalità (più probabilità per punti e timeout)
        weights = [40, 25, 30, 5]
        
        penalty = random.choices(penalties, weights=weights)[0]
        
        if penalty == "points":
            self.score = max(0, self.score - 50)
        elif penalty == "life":
            self.lives -= 1
        elif penalty == "timeout":
            self.timeout_timer = 600  # 10 secondi a 60 FPS
        elif penalty == "game_over":
            self.lives = 0
            
        self.penalty_animation.start(penalty)
        
    def check_game_over(self) -> bool:
        """Verifica se il gioco è finito"""
        return self.lives <= 0 or self.errors >= 3
        
    def draw_text_wrapped(self, text: str, x: int, y: int, max_width: int, font: pygame.font.Font, color: Tuple[int, int, int]):
        """Disegna testo con word wrap"""
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            test_surface = font.render(test_line, True, color)
            if test_surface.get_width() <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
            
        for i, line in enumerate(lines):
            text_surface = font.render(line, True, color)
            self.screen.blit(text_surface, (x, y + i * 30))
            
    def draw_menu(self):
        """Disegna il menu principale con grafica migliorata"""
        # Sfondo con gradiente
        draw_gradient_background(self.screen)
        
        # Box decorativo per il titolo
        title_box = pygame.Rect(SCREEN_WIDTH // 2 - 450, 80, 900, 180)
        draw_rounded_rect_with_shadow(self.screen, title_box, (255, 255, 255), border_radius=20, shadow_offset=8)
        pygame.draw.rect(self.screen, BLACK, title_box, 4, border_radius=20)
        
        # Titolo con effetto
        draw_text_with_shadow(self.screen, "FAKE NEWS ROULETTE", self.font_title, 
                            (SCREEN_WIDTH // 2, 140), RED, shadow_offset=4)
        
        # Sottotitolo con icona
        subtitle_text = "🎯 Impara a distinguere notizie vere da fake news!"
        draw_text_with_shadow(self.screen, subtitle_text, self.font_medium, 
                            (SCREEN_WIDTH // 2, 210), DARK_GRAY, shadow_offset=2)
        
        # Box per le istruzioni
        instr_box = pygame.Rect(80, 270, SCREEN_WIDTH - 160, 180)
        draw_rounded_rect_with_shadow(self.screen, instr_box, (255, 255, 255), border_radius=15, shadow_offset=6)
        pygame.draw.rect(self.screen, BLUE, instr_box, 3, border_radius=15)
        
        # Istruzioni con icone
        instructions = [
            "🎮 Come giocare:",
            "1️⃣  La roulette selezionerà una categoria casuale",
            "2️⃣  Leggi la notizia e decidi se è VERA o FALSA",
            "3️⃣  Attenzione! Ogni errore attiva la roulette russa:",
            "    💥 Potresti perdere punti, vite o essere bloccato",
            "4️⃣  Hai 3 vite ❤️  Perdi quando finiscono o fai 3 errori"
        ]
        
        y_offset = 290
        for instruction in instructions:
            text = self.font_small.render(instruction, True, BLACK)
            self.screen.blit(text, (100, y_offset))
            y_offset += 28
            
        # Pulsanti
        mouse_pos = pygame.mouse.get_pos()
        self.btn_start.check_hover(mouse_pos)
        self.btn_quit.check_hover(mouse_pos)
        
        self.btn_start.draw(self.screen, self.font_medium)
        self.btn_quit.draw(self.screen, self.font_medium)
        
    def draw_game_ui(self):
        """Disegna l'interfaccia di gioco comune con grafica migliorata"""
        # Sfondo con gradiente
        draw_gradient_background(self.screen)
        
        # Barra superiore con informazioni
        header_rect = pygame.Rect(0, 0, SCREEN_WIDTH, 70)
        header_surf = pygame.Surface((SCREEN_WIDTH, 70), pygame.SRCALPHA)
        pygame.draw.rect(header_surf, (*WHITE, 220), header_surf.get_rect())
        self.screen.blit(header_surf, (0, 0))
        pygame.draw.line(self.screen, BLUE, (0, 70), (SCREEN_WIDTH, 70), 3)
        
        # Score con icona e box
        score_box = pygame.Rect(10, 10, 250, 50)
        draw_rounded_rect_with_shadow(self.screen, score_box, BLUE, border_radius=10, shadow_offset=3)
        score_text = f"💰 Punteggio: {self.score}"
        draw_text_with_shadow(self.screen, score_text, self.font_medium, 
                            (score_box.centerx, score_box.centery), WHITE, shadow_offset=2)
        
        # Vite con icone e box
        lives_box = pygame.Rect(SCREEN_WIDTH - 260, 10, 250, 50)
        draw_rounded_rect_with_shadow(self.screen, lives_box, RED, border_radius=10, shadow_offset=3)
        lives_text = f"{'❤️ ' * self.lives}{'🖤 ' * (3 - self.lives)}"
        draw_text_with_shadow(self.screen, lives_text, self.font_medium, 
                            (lives_box.centerx, lives_box.centery), WHITE, shadow_offset=2)
        
        # Errori con box centrale
        errors_box = pygame.Rect(SCREEN_WIDTH // 2 - 100, 10, 200, 50)
        draw_rounded_rect_with_shadow(self.screen, errors_box, ORANGE, border_radius=10, shadow_offset=3)
        errors_text = f"⚠️  Errori: {self.errors}/3"
        draw_text_with_shadow(self.screen, errors_text, self.font_medium, 
                            (errors_box.centerx, errors_box.centery), WHITE, shadow_offset=2)
        
    def draw_spinning(self):
        """Disegna lo stato di rotazione della roulette con grafica migliorata"""
        self.draw_game_ui()
        
        # Titolo con animazione
        title_text = "🎰 Gira la roulette! 🎰"
        draw_text_with_shadow(self.screen, title_text, self.font_large, 
                            (SCREEN_WIDTH // 2, 100), DARK_GRAY, shadow_offset=3)
        
        # Disegna la roulette
        self.roulette.draw(self.screen, self.font_small)
        
        # Categoria selezionata (se non sta girando) con box decorativo
        if not self.roulette.spinning and self.roulette.selected_category:
            cat_box = pygame.Rect(SCREEN_WIDTH // 2 - 250, 520, 500, 70)
            cat_color = CATEGORY_COLORS.get(self.roulette.selected_category, BLACK)
            draw_rounded_rect_with_shadow(self.screen, cat_box, cat_color, border_radius=15, shadow_offset=5)
            pygame.draw.rect(self.screen, BLACK, cat_box, 4, border_radius=15)
            
            category_text = f"✨ Categoria: {self.roulette.selected_category} ✨"
            draw_text_with_shadow(self.screen, category_text, self.font_large, 
                                (SCREEN_WIDTH // 2, 555), WHITE, shadow_offset=2)
            
    def draw_question(self):
        """Disegna lo stato della domanda con grafica migliorata"""
        self.draw_game_ui()
        
        if self.current_news:
            # Categoria con badge
            cat_badge = pygame.Rect(50, 85, 300, 45)
            cat_color = CATEGORY_COLORS.get(self.current_category, BLACK)
            draw_rounded_rect_with_shadow(self.screen, cat_badge, cat_color, border_radius=10, shadow_offset=3)
            pygame.draw.rect(self.screen, BLACK, cat_badge, 3, border_radius=10)
            
            category_text = f"📰 {self.current_category}"
            draw_text_with_shadow(self.screen, category_text, self.font_medium, 
                                (cat_badge.centerx, cat_badge.centery), WHITE, shadow_offset=2)
            
            # Box notizia migliorato
            news_box = pygame.Rect(50, 145, SCREEN_WIDTH - 100, 430)
            draw_rounded_rect_with_shadow(self.screen, news_box, WHITE, border_radius=15, shadow_offset=8)
            pygame.draw.rect(self.screen, BLUE, news_box, 4, border_radius=15)
            
            # Icona decorativa
            icon_text = "📄"
            icon_surf = self.font_large.render(icon_text, True, BLUE)
            self.screen.blit(icon_surf, (70, 155))
            
            self.draw_text_wrapped(self.current_news["text"], 120, 170, SCREEN_WIDTH - 180, 
                                 self.font_medium, BLACK)
            
            # Domanda con stile
            question_box = pygame.Rect(SCREEN_WIDTH // 2 - 350, 590, 700, 55)
            draw_rounded_rect_with_shadow(self.screen, question_box, YELLOW, border_radius=12, shadow_offset=4)
            pygame.draw.rect(self.screen, BLACK, question_box, 3, border_radius=12)
            
            draw_text_with_shadow(self.screen, "❓ Questa notizia è vera o falsa? ❓", self.font_large, 
                                (SCREEN_WIDTH // 2, 617), BLACK, shadow_offset=2)
            
            # Pulsanti
            mouse_pos = pygame.mouse.get_pos()
            self.btn_true.check_hover(mouse_pos)
            self.btn_false.check_hover(mouse_pos)
            
            # Disabilita i pulsanti durante il timeout
            if self.timeout_timer > 0:
                # Mostra timer con animazione
                timeout_box = pygame.Rect(SCREEN_WIDTH // 2 - 150, 660, 300, 60)
                draw_rounded_rect_with_shadow(self.screen, timeout_box, RED, border_radius=10, shadow_offset=4)
                pygame.draw.rect(self.screen, BLACK, timeout_box, 3, border_radius=10)
                
                timeout_text = f"⏸️  Bloccato: {self.timeout_timer // 60 + 1}s"
                draw_text_with_shadow(self.screen, timeout_text, self.font_large, 
                                    (SCREEN_WIDTH // 2, 690), WHITE, shadow_offset=2)
            else:
                self.btn_true.draw(self.screen, self.font_medium)
                self.btn_false.draw(self.screen, self.font_medium)
                
    def draw_feedback(self):
        """Disegna lo stato del feedback con grafica migliorata"""
        self.draw_game_ui()
        
        if self.current_news:
            # Categoria badge
            cat_badge = pygame.Rect(50, 85, 300, 45)
            cat_color = CATEGORY_COLORS.get(self.current_category, BLACK)
            draw_rounded_rect_with_shadow(self.screen, cat_badge, cat_color, border_radius=10, shadow_offset=3)
            pygame.draw.rect(self.screen, BLACK, cat_badge, 3, border_radius=10)
            
            category_text = f"📰 {self.current_category}"
            draw_text_with_shadow(self.screen, category_text, self.font_medium, 
                                (cat_badge.centerx, cat_badge.centery), WHITE, shadow_offset=2)
            
            # Box per il feedback con gradiente
            feedback_box = pygame.Rect(50, 145, SCREEN_WIDTH - 100, 510)
            draw_rounded_rect_with_shadow(self.screen, feedback_box, WHITE, border_radius=15, shadow_offset=8)
            pygame.draw.rect(self.screen, GREEN, feedback_box, 4, border_radius=15)
            
            # Icona risultato
            result_icon = "✅" if self.score > 0 else "❌"
            icon_surf = self.font_large.render(result_icon, True, GREEN if self.score > 0 else RED)
            self.screen.blit(icon_surf, (70, 155))
            
            # Notizia originale
            self.draw_text_wrapped(self.current_news["text"], 120, 165, SCREEN_WIDTH - 180, 
                                 self.font_small, BLACK)
            
            # Sezione spiegazione con box
            expl_header = pygame.Rect(70, 295, SCREEN_WIDTH - 180, 35)
            pygame.draw.rect(self.screen, BLUE, expl_header, border_radius=8)
            draw_text_with_shadow(self.screen, "💡 Spiegazione:", self.font_medium, 
                                (expl_header.centerx, expl_header.centery), WHITE, shadow_offset=1)
            
            self.draw_text_wrapped(self.current_news["explanation"], 85, 345, SCREEN_WIDTH - 210, 
                                 self.font_small, DARK_GRAY)
            
            # Sezione fonte con box
            source_header = pygame.Rect(70, 520, SCREEN_WIDTH - 180, 35)
            pygame.draw.rect(self.screen, ORANGE, source_header, border_radius=8)
            draw_text_with_shadow(self.screen, "📚 Fonte:", self.font_medium, 
                                (source_header.centerx, source_header.centery), WHITE, shadow_offset=1)
            
            self.draw_text_wrapped(self.current_news["source"], 85, 570, SCREEN_WIDTH - 210, 
                                 self.font_small, DARK_GRAY)
            
            # Pulsante continua
            mouse_pos = pygame.mouse.get_pos()
            self.btn_continue.check_hover(mouse_pos)
            self.btn_continue.draw(self.screen, self.font_medium)
            
    def draw_game_over(self):
        """Disegna la schermata di game over con grafica migliorata"""
        # Sfondo con gradiente
        draw_gradient_background(self.screen)
        
        # Box principale
        main_box = pygame.Rect(SCREEN_WIDTH // 2 - 450, 50, 900, 700)
        draw_rounded_rect_with_shadow(self.screen, main_box, WHITE, border_radius=20, shadow_offset=10)
        pygame.draw.rect(self.screen, RED, main_box, 5, border_radius=20)
        
        # Titolo
        draw_text_with_shadow(self.screen, "💀 GAME OVER 💀", self.font_title, 
                            (SCREEN_WIDTH // 2, 120), RED, shadow_offset=4)
        
        # Punteggio finale con box decorativo
        score_box = pygame.Rect(SCREEN_WIDTH // 2 - 300, 180, 600, 80)
        draw_rounded_rect_with_shadow(self.screen, score_box, GOLD, border_radius=15, shadow_offset=5)
        pygame.draw.rect(self.screen, BLACK, score_box, 4, border_radius=15)
        
        final_score_text = f"🏆 Punteggio Finale: {self.score}"
        draw_text_with_shadow(self.screen, final_score_text, self.font_large, 
                            (SCREEN_WIDTH // 2, 220), WHITE, shadow_offset=3)
        
        # Box statistiche
        stats_box = pygame.Rect(SCREEN_WIDTH // 2 - 250, 280, 500, 100)
        draw_rounded_rect_with_shadow(self.screen, stats_box, LIGHT_GRAY, border_radius=12, shadow_offset=4)
        pygame.draw.rect(self.screen, BLUE, stats_box, 3, border_radius=12)
        
        stats_title_surf = self.font_medium.render("📊 Statistiche", True, BLUE)
        self.screen.blit(stats_title_surf, (SCREEN_WIDTH // 2 - 80, 295))
        
        errors_stat = self.font_medium.render(f"❌ Errori: {self.errors}", True, BLACK)
        self.screen.blit(errors_stat, (SCREEN_WIDTH // 2 - 70, 330))
        
        lives_stat = self.font_medium.render(f"❤️  Vite rimaste: {self.lives}", True, BLACK)
        self.screen.blit(lives_stat, (SCREEN_WIDTH // 2 - 110, 360))
        
        # Classifica con box
        leaderboard_box = pygame.Rect(SCREEN_WIDTH // 2 - 300, 400, 600, 230)
        draw_rounded_rect_with_shadow(self.screen, leaderboard_box, (255, 250, 205), border_radius=15, shadow_offset=5)
        pygame.draw.rect(self.screen, GOLD, leaderboard_box, 4, border_radius=15)
        
        draw_text_with_shadow(self.screen, "🏅 CLASSIFICA TOP 5 🏅", self.font_large, 
                            (SCREEN_WIDTH // 2, 430), DARK_GRAY, shadow_offset=2)
        
        # Medaglie per i primi tre
        medals = ["🥇", "🥈", "🥉"]
        y_offset = 475
        for i, entry in enumerate(self.leaderboard[:5]):
            medal = medals[i] if i < 3 else f"{i+1}."
            rank_text = f"{medal} {entry['score']} punti"
            
            # Highlight per il punteggio corrente
            if entry['score'] == self.score and i == 0:
                highlight_rect = pygame.Rect(SCREEN_WIDTH // 2 - 180, y_offset - 5, 360, 32)
                pygame.draw.rect(self.screen, YELLOW, highlight_rect, border_radius=8)
            
            text_surf = self.font_medium.render(rank_text, True, BLACK)
            text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, y_offset + 10))
            self.screen.blit(text_surf, text_rect)
            y_offset += 35
            
        # Pulsante menu
        mouse_pos = pygame.mouse.get_pos()
        self.btn_menu.check_hover(mouse_pos)
        self.btn_menu.draw(self.screen, self.font_medium)
        
    def handle_menu_events(self, event):
        """Gestisce gli eventi nel menu"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.btn_start.is_clicked(mouse_pos):
                self.reset_game()
            elif self.btn_quit.is_clicked(mouse_pos):
                return False
        return True
        
    def handle_question_events(self, event):
        """Gestisce gli eventi durante la domanda"""
        if event.type == pygame.MOUSEBUTTONDOWN and self.timeout_timer == 0:
            mouse_pos = pygame.mouse.get_pos()
            
            user_answer = None
            if self.btn_true.is_clicked(mouse_pos):
                user_answer = True
            elif self.btn_false.is_clicked(mouse_pos):
                user_answer = False
                
            if user_answer is not None:
                correct_answer = self.current_news["is_true"]
                
                if user_answer == correct_answer:
                    # Risposta corretta
                    self.score += 100
                    self.state = "feedback"
                    self.feedback_timer = 180  # 3 secondi
                else:
                    # Risposta sbagliata
                    self.errors += 1
                    self.state = "penalty"
                    self.apply_penalty()
                    
    def handle_feedback_events(self, event):
        """Gestisce gli eventi durante il feedback"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.btn_continue.is_clicked(mouse_pos):
                if self.check_game_over():
                    self.add_to_leaderboard(self.score)
                    self.state = "game_over"
                else:
                    self.state = "spinning"
                    self.roulette.start_spin()
                    
    def handle_game_over_events(self, event):
        """Gestisce gli eventi nella schermata di game over"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.btn_menu.is_clicked(mouse_pos):
                self.state = "menu"
                
    def run(self):
        """Loop principale del gioco"""
        running = True
        
        while running:
            # Gestione eventi
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                if self.state == "menu":
                    running = self.handle_menu_events(event)
                elif self.state == "question":
                    self.handle_question_events(event)
                elif self.state == "feedback":
                    self.handle_feedback_events(event)
                elif self.state == "game_over":
                    self.handle_game_over_events(event)
                    
            # Aggiornamenti
            if self.state == "spinning":
                self.roulette.update()
                if not self.roulette.spinning:
                    self.current_category = self.roulette.selected_category
                    self.select_random_news()
                    # Piccola pausa prima di mostrare la domanda
                    self.feedback_timer = 60  # 1 secondo
                    if self.feedback_timer > 0:
                        self.feedback_timer -= 1
                        if self.feedback_timer == 0:
                            self.state = "question"
                            
            elif self.state == "question":
                if self.timeout_timer > 0:
                    self.timeout_timer -= 1
                    
            elif self.state == "penalty":
                self.penalty_animation.update()
                if not self.penalty_animation.active:
                    if self.check_game_over():
                        self.add_to_leaderboard(self.score)
                        self.state = "game_over"
                    else:
                        self.state = "feedback"
                        self.feedback_timer = 180
                        
            # Rendering
            if self.state == "menu":
                self.draw_menu()
            elif self.state == "spinning":
                self.draw_spinning()
            elif self.state == "question":
                self.draw_question()
            elif self.state == "feedback":
                self.draw_feedback()
            elif self.state == "penalty":
                self.draw_question()  # Mostra la domanda sotto
                self.penalty_animation.draw(self.screen, self.font_title, self.font_large)
            elif self.state == "game_over":
                self.draw_game_over()
                
            pygame.display.flip()
            self.clock.tick(FPS)
            
        pygame.quit()


def main():
    """Funzione principale"""
    game = FakeNewsRoulette()
    game.run()


if __name__ == "__main__":
    main()
