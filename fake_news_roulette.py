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

# Colori
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

# Colori per le categorie
CATEGORY_COLORS = {
    "Politica": (230, 100, 100),
    "Scienza": (100, 150, 230),
    "Tecnologia": (150, 100, 230),
    "Salute": (100, 230, 150),
    "Intrattenimento": (230, 200, 100),
    "Economia": (230, 150, 100)
}


class Button:
    """Classe per gestire i pulsanti grafici"""
    
    def __init__(self, x: int, y: int, width: int, height: int, text: str, 
                 color: Tuple[int, int, int], text_color: Tuple[int, int, int] = WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.hover_color = tuple(min(c + 30, 255) for c in color)
        self.is_hovered = False
        
    def draw(self, screen: pygame.Surface, font: pygame.font.Font):
        """Disegna il pulsante sullo schermo"""
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, self.rect, 3, border_radius=10)
        
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
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
        """Disegna la roulette sullo schermo"""
        # Disegna i settori
        num_categories = len(self.categories)
        sector_angle = 360 / num_categories
        
        for i, category in enumerate(self.categories):
            start_angle = math.radians(i * sector_angle + self.angle)
            end_angle = math.radians((i + 1) * sector_angle + self.angle)
            
            # Colore del settore
            color = CATEGORY_COLORS.get(category, GRAY)
            
            # Disegna il settore come un poligono
            points = [(self.x, self.y)]
            for angle in [start_angle + j * 0.1 for j in range(11)]:
                px = self.x + self.radius * math.cos(angle)
                py = self.y + self.radius * math.sin(angle)
                points.append((px, py))
            
            pygame.draw.polygon(screen, color, points)
            pygame.draw.polygon(screen, BLACK, points, 2)
            
            # Disegna il testo della categoria
            mid_angle = (start_angle + end_angle) / 2
            text_distance = self.radius * 0.7
            text_x = self.x + text_distance * math.cos(mid_angle)
            text_y = self.y + text_distance * math.sin(mid_angle)
            
            # Ruota il testo
            text_surface = font.render(category, True, BLACK)
            text_rect = text_surface.get_rect(center=(text_x, text_y))
            screen.blit(text_surface, text_rect)
        
        # Disegna il cerchio esterno
        pygame.draw.circle(screen, BLACK, (self.x, self.y), self.radius, 4)
        
        # Disegna l'indicatore (triangolo in alto)
        indicator_size = 20
        indicator_points = [
            (self.x, self.y - self.radius - 30),
            (self.x - indicator_size, self.y - self.radius - 10),
            (self.x + indicator_size, self.y - self.radius - 10)
        ]
        pygame.draw.polygon(screen, RED, indicator_points)
        pygame.draw.polygon(screen, BLACK, indicator_points, 2)


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
        """Disegna l'animazione della penalità"""
        if not self.active:
            return
            
        # Sfondo semi-trasparente
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        # Animazione pulsante
        scale = 1 + 0.1 * math.sin(self.timer * 0.2)
        
        # Testo della penalità
        penalty_texts = {
            "points": "PERDITA DI PUNTI!",
            "life": "PERDITA DI UNA VITA!",
            "timeout": "BLOCCO TEMPORANEO!",
            "game_over": "GAME OVER!"
        }
        
        text = penalty_texts.get(self.penalty_type, "PENALITÀ!")
        color = RED if self.penalty_type in ["life", "game_over"] else ORANGE
        
        text_surface = font_large.render(text, True, color)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        
        # Applica scala
        scaled_surface = pygame.transform.scale(
            text_surface,
            (int(text_rect.width * scale), int(text_rect.height * scale))
        )
        scaled_rect = scaled_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(scaled_surface, scaled_rect)


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
        """Disegna il menu principale"""
        self.screen.fill(WHITE)
        
        # Titolo
        title = self.font_title.render("FAKE NEWS ROULETTE", True, RED)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title, title_rect)
        
        # Sottotitolo
        subtitle = self.font_medium.render("Impara a distinguere notizie vere da fake news!", True, DARK_GRAY)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 230))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Istruzioni
        instructions = [
            "Come giocare:",
            "1. La roulette selezionerà una categoria casuale",
            "2. Leggi la notizia e decidi se è VERA o FALSA",
            "3. Attenzione! Ogni errore attiva la roulette russa:",
            "   - Potresti perdere punti, vite o essere bloccato",
            "4. Hai 3 vite. Perdi quando finiscono o fai 3 errori"
        ]
        
        y_offset = 300
        for instruction in instructions:
            text = self.font_small.render(instruction, True, BLACK)
            self.screen.blit(text, (50, y_offset))
            y_offset += 30
            
        # Pulsanti
        mouse_pos = pygame.mouse.get_pos()
        self.btn_start.check_hover(mouse_pos)
        self.btn_quit.check_hover(mouse_pos)
        
        self.btn_start.draw(self.screen, self.font_medium)
        self.btn_quit.draw(self.screen, self.font_medium)
        
    def draw_game_ui(self):
        """Disegna l'interfaccia di gioco comune"""
        # Sfondo
        self.screen.fill(WHITE)
        
        # Score e vite in alto
        score_text = self.font_medium.render(f"Punteggio: {self.score}", True, BLUE)
        self.screen.blit(score_text, (20, 20))
        
        lives_text = self.font_medium.render(f"Vite: {'❤️ ' * self.lives}", True, RED)
        self.screen.blit(lives_text, (SCREEN_WIDTH - 250, 20))
        
        errors_text = self.font_medium.render(f"Errori: {self.errors}/3", True, ORANGE)
        self.screen.blit(errors_text, (SCREEN_WIDTH // 2 - 80, 20))
        
    def draw_spinning(self):
        """Disegna lo stato di rotazione della roulette"""
        self.draw_game_ui()
        
        # Titolo
        title = self.font_large.render("Gira la roulette!", True, DARK_GRAY)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 80))
        self.screen.blit(title, title_rect)
        
        # Disegna la roulette
        self.roulette.draw(self.screen, self.font_small)
        
        # Categoria selezionata (se non sta girando)
        if not self.roulette.spinning and self.roulette.selected_category:
            category_text = self.font_large.render(f"Categoria: {self.roulette.selected_category}", True, 
                                                   CATEGORY_COLORS.get(self.roulette.selected_category, BLACK))
            category_rect = category_text.get_rect(center=(SCREEN_WIDTH // 2, 550))
            self.screen.blit(category_text, category_rect)
            
    def draw_question(self):
        """Disegna lo stato della domanda"""
        self.draw_game_ui()
        
        if self.current_news:
            # Categoria
            category_text = self.font_medium.render(f"Categoria: {self.current_category}", True, 
                                                    CATEGORY_COLORS.get(self.current_category, BLACK))
            self.screen.blit(category_text, (50, 80))
            
            # Notizia
            news_box = pygame.Rect(50, 130, SCREEN_WIDTH - 100, 450)
            pygame.draw.rect(self.screen, LIGHT_GRAY, news_box, border_radius=10)
            pygame.draw.rect(self.screen, BLACK, news_box, 3, border_radius=10)
            
            self.draw_text_wrapped(self.current_news["text"], 70, 160, SCREEN_WIDTH - 140, 
                                 self.font_medium, BLACK)
            
            # Domanda
            question = self.font_large.render("Questa notizia è vera o falsa?", True, DARK_GRAY)
            question_rect = question.get_rect(center=(SCREEN_WIDTH // 2, 600))
            self.screen.blit(question, question_rect)
            
            # Pulsanti
            mouse_pos = pygame.mouse.get_pos()
            self.btn_true.check_hover(mouse_pos)
            self.btn_false.check_hover(mouse_pos)
            
            # Disabilita i pulsanti durante il timeout
            if self.timeout_timer > 0:
                # Mostra timer
                timeout_text = self.font_large.render(f"Bloccato: {self.timeout_timer // 60 + 1}s", True, RED)
                timeout_rect = timeout_text.get_rect(center=(SCREEN_WIDTH // 2, 670))
                self.screen.blit(timeout_text, timeout_rect)
            else:
                self.btn_true.draw(self.screen, self.font_medium)
                self.btn_false.draw(self.screen, self.font_medium)
                
    def draw_feedback(self):
        """Disegna lo stato del feedback"""
        self.draw_game_ui()
        
        if self.current_news:
            # Categoria
            category_text = self.font_medium.render(f"Categoria: {self.current_category}", True, 
                                                    CATEGORY_COLORS.get(self.current_category, BLACK))
            self.screen.blit(category_text, (50, 80))
            
            # Box per il feedback
            feedback_box = pygame.Rect(50, 130, SCREEN_WIDTH - 100, 520)
            pygame.draw.rect(self.screen, LIGHT_GRAY, feedback_box, border_radius=10)
            pygame.draw.rect(self.screen, BLACK, feedback_box, 3, border_radius=10)
            
            # Notizia originale
            self.draw_text_wrapped(self.current_news["text"], 70, 160, SCREEN_WIDTH - 140, 
                                 self.font_small, BLACK)
            
            # Spiegazione
            explanation_title = self.font_medium.render("Spiegazione:", True, BLUE)
            self.screen.blit(explanation_title, (70, 280))
            
            self.draw_text_wrapped(self.current_news["explanation"], 70, 320, SCREEN_WIDTH - 140, 
                                 self.font_small, DARK_GRAY)
            
            # Fonte
            source_title = self.font_medium.render("Fonte:", True, BLUE)
            self.screen.blit(source_title, (70, 480))
            
            self.draw_text_wrapped(self.current_news["source"], 70, 520, SCREEN_WIDTH - 140, 
                                 self.font_small, DARK_GRAY)
            
            # Pulsante continua
            mouse_pos = pygame.mouse.get_pos()
            self.btn_continue.check_hover(mouse_pos)
            self.btn_continue.draw(self.screen, self.font_medium)
            
    def draw_game_over(self):
        """Disegna la schermata di game over"""
        self.screen.fill(WHITE)
        
        # Titolo
        title = self.font_title.render("GAME OVER", True, RED)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)
        
        # Punteggio finale
        final_score = self.font_large.render(f"Punteggio Finale: {self.score}", True, BLUE)
        final_score_rect = final_score.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(final_score, final_score_rect)
        
        # Statistiche
        stats_title = self.font_medium.render("Statistiche:", True, DARK_GRAY)
        self.screen.blit(stats_title, (SCREEN_WIDTH // 2 - 100, 270))
        
        errors_stat = self.font_medium.render(f"Errori: {self.errors}", True, BLACK)
        self.screen.blit(errors_stat, (SCREEN_WIDTH // 2 - 80, 310))
        
        lives_stat = self.font_medium.render(f"Vite rimaste: {self.lives}", True, BLACK)
        self.screen.blit(lives_stat, (SCREEN_WIDTH // 2 - 130, 350))
        
        # Classifica
        leaderboard_title = self.font_large.render("CLASSIFICA", True, DARK_GRAY)
        leaderboard_rect = leaderboard_title.get_rect(center=(SCREEN_WIDTH // 2, 420))
        self.screen.blit(leaderboard_title, leaderboard_rect)
        
        y_offset = 480
        for i, entry in enumerate(self.leaderboard[:5]):
            rank_text = self.font_medium.render(f"{i+1}. {entry['score']} punti", True, BLACK)
            self.screen.blit(rank_text, (SCREEN_WIDTH // 2 - 100, y_offset))
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
