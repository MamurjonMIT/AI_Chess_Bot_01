import pygame
import sys
import chess
from minimax import minimax

pygame.init()
WIDTH, HEIGHT = 480, 480
SQ_SIZE = WIDTH // 8
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minimax Chess Bot")

WHITE = (240, 217, 181)
BROWN = (181, 136, 99)

PIECES = {}
for color in ['w', 'b']:
    for piece in ['p', 'n', 'b', 'r', 'q', 'k']:
        PIECES[color + piece] = pygame.transform.scale(
            pygame.image.load(f"images/{color}{piece}.png"), (SQ_SIZE, SQ_SIZE))

def draw_board(board):
    for rank in range(8):
        for file in range(8):
            color = WHITE if (rank + file) % 2 == 0 else BROWN
            pygame.draw.rect(SCREEN, color, pygame.Rect(file*SQ_SIZE, rank*SQ_SIZE, SQ_SIZE, SQ_SIZE))

            square = chess.square(file, 7 - rank)
            piece = board.piece_at(square)
            if piece:
                color = 'w' if piece.color == chess.WHITE else 'b'
                SCREEN.blit(PIECES[color + piece.symbol().lower()], (file*SQ_SIZE, rank*SQ_SIZE))

def get_clicked_square(pos):
    x, y = pos
    file = x // SQ_SIZE
    rank = 7 - (y // SQ_SIZE)
    return chess.square(file, rank)

def main():
    board = chess.Board()
    clock = pygame.time.Clock()
    selected_square = None
    player_color = None

    font = pygame.font.SysFont(None, 36)
    selecting = True
    while selecting:
        SCREEN.fill((0, 0, 0))
        text1 = font.render("Press W to play White", True, (255, 255, 255))
        text2 = font.render("Press B to play Black", True, (255, 255, 255))
        SCREEN.blit(text1, (100, HEIGHT // 3))
        SCREEN.blit(text2, (100, HEIGHT // 2))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player_color = chess.WHITE
                    selecting = False
                elif event.key == pygame.K_b:
                    player_color = chess.BLACK
                    selecting = False

    running = True
    while running:
        draw_board(board)
        pygame.display.flip()
        clock.tick(60)

        if board.is_game_over():
            print("Game Over:", board.result())
            pygame.time.wait(5000)
            running = False
            continue

        turn = board.turn
        is_player_turn = (turn == player_color)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if is_player_turn and event.type == pygame.MOUSEBUTTONDOWN:
                square = get_clicked_square(pygame.mouse.get_pos())
                if selected_square is None:
                    piece = board.piece_at(square)
                    if piece and piece.color == player_color:
                        selected_square = square
                else:
                    move = chess.Move(selected_square, square)
                    if move in board.legal_moves:
                        board.push(move)
                        selected_square = None
                    else:
                        selected_square = None

        if not is_player_turn and not board.is_game_over():
            _, best_move = minimax(board, depth=3, alpha=-float('inf'), beta=float('inf'), maximizing_player=not player_color)
            if best_move:
                board.push(best_move)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
