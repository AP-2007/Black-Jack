import pygame
import random
import sys

# ---------- Game Setup ----------
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blackjack Simulator")



font = pygame.font.SysFont("arial", 28)
result_font = pygame.font.SysFont("arial", 40, bold=True)  #result text

# Load background image and scale to window
background = pygame.image.load("table_bg.png").convert()  # replace with your file name [web:46]
background = pygame.transform.smoothscale(background, (WIDTH, HEIGHT))  # fit window [web:48]

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 150, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)
GOLD = (255, 215, 0)
LIGHT_BROWN = (181, 101, 29) # button color

# ---------- Card Logic ----------
suits = ["♠", "♥", "♦", "♣"]
ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
values = {
    "A": 11, "2": 2, "3": 3, "4": 4, "5": 5,
    "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
    "J": 10, "Q": 10, "K": 10
}

def create_deck():
    deck = [(rank, suit) for suit in suits for rank in ranks]
    random.shuffle(deck)
    return deck

def calculate_value(hand):
    value = sum(values[card[0]] for card in hand)
    aces = sum(1 for card in hand if card[0] == "A")
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value

# ---------- Drawing Cards ----------
def draw_hand(hand, x, y, hide_first=False):
    for i, (rank, suit) in enumerate(hand):
        card_x = x + i * 60
        card_y = y

        # Filled white card
        pygame.draw.rect(screen, WHITE, (card_x, card_y, 55, 80))

        # Thin black outline (width=1)
        pygame.draw.rect(screen, BLACK, (card_x, card_y, 55, 80), 2)  # outline [web:64][web:75]

        if hide_first and i == 0:
            pygame.draw.rect(screen, BLUE, (card_x + 3, card_y + 3, 49, 74))
        else:
            text = font.render(f"{rank}{suit}", True, BLACK)
            screen.blit(text, (card_x + 10, card_y + 20))

# ---------- Buttons ----------
def draw_button(text, x, y, w, h, color):
    pygame.draw.rect(screen, color, (x, y, w, h))
    t = font.render(text, True, BLACK)  # black text [web:63]
    screen.blit(t, (x + 10, y + 10))

def button_clicked(x, y, w, h, mouse_pos):
    return x <= mouse_pos[0] <= x + w and y <= mouse_pos[1] <= y + h

# ---------- Game State ----------
deck = create_deck()
player = []
dealer = []

game_over = False
message = ""
message_color = WHITE
player_wins = 0
player_losses = 0

def reset_game():
    global deck, player, dealer, game_over, message, message_color
    deck = create_deck()
    player = [deck.pop(), deck.pop()]
    dealer = [deck.pop(), deck.pop()]
    game_over = False
    message = ""
    message_color = WHITE

reset_game()

# ---------- Main Loop ----------
running = True
while running:
    # Draw background image
    screen.blit(background, (0, 0))  # replaces screen.fill(GREEN) [web:43]

    # Display Hands
    # Dealer: hide first card while game is not over
    draw_hand(dealer, 50, 100, hide_first=not game_over)
    draw_hand(player, 50, 400)

    # Text Values
    player_value = calculate_value(player)
    dealer_value = calculate_value(dealer) if game_over else "?"

    screen.blit(font.render(f"Player: {player_value}", True, WHITE), (50, 350))
    screen.blit(font.render(f"Dealer: {dealer_value}", True, WHITE), (50, 50))

    # Wins / Losses (top-right)
    score_text = font.render(
        f"Wins: {player_wins}  Losses: {player_losses}", True, WHITE
    )
    score_rect = score_text.get_rect(topright=(WIDTH - 20, 10))  # padding from right [web:121]
    screen.blit(score_text, score_rect)

    # Buttons (light brown, black text)
    draw_button("Hit", 600, 350, 150, 50, BROWN_LIGHT)
    draw_button("Stand", 600, 420, 150, 50, BROWN_LIGHT)
    draw_button("Restart", 600, 490, 150, 50, BROWN_LIGHT)

    # Centered result message (bigger font)
    if message:
        msg_surface = result_font.render(message, True, message_color)
        msg_rect = msg_surface.get_rect(center=(WIDTH // 2, 280))  # middle-ish [web:7]
        screen.blit(msg_surface, msg_rect)

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()

            # HIT
            if button_clicked(600, 350, 150, 50, mouse) and not game_over:
                player.append(deck.pop())
                if calculate_value(player) > 21:
                    message = "Bust! Dealer Wins."
                    message_color = RED
                    player_losses += 1
                    game_over = True

            # STAND
            if button_clicked(600, 420, 150, 50, mouse) and not game_over:
                while calculate_value(dealer) < 17:
                    dealer.append(deck.pop())

                player_val = calculate_value(player)
                dealer_val = calculate_value(dealer)

                if dealer_val > 21:
                    message = "Dealer Busts! You Win!"
                    message_color = GOLD
                    player_wins += 1
                elif dealer_val > player_val:
                    message = "Dealer Wins."
                    message_color = RED
                    player_losses += 1
                elif dealer_val < player_val:
                    message = "You Win!"
                    message_color = GOLD
                    player_wins += 1
                else:
                    message = "Push! It's a Tie."
                    message_color = WHITE
                game_over = True

            # RESTART
            if button_clicked(600, 490, 150, 50, mouse):
                reset_game()

    pygame.display.update()

pygame.quit()
sys.exit()

