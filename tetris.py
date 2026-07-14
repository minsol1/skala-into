#
# 교육 환경 설정 및 간단한 파이썬 연습 코드
# [고급 실습] 테트리스 게임 만들기
# - 좌/우 화살표: 블록 좌우 이동
# - 위 화살표: 블록 시계방향 회전
# - 스페이스: 즉시 하단으로 떨어뜨리기 (하드 드롭)
# - 아래 화살표: 한 칸씩 아래로 이동 (소프트 드롭)
# - 한 줄이 가득 차면 해당 줄 삭제
#
# 작성일 : 2026-07-14
# 작성자 : 김민솔, SKALA
#
# 변경일 :
#
# All Rights Reserved by SK AX, SKALA
#

import random
import sys

import pygame

COLS = 10
ROWS = 20
CELL_SIZE = 30
BOARD_WIDTH = COLS * CELL_SIZE
BOARD_HEIGHT = ROWS * CELL_SIZE
SIDE_PANEL_WIDTH = 160
BOARD_OFFSET_X = SIDE_PANEL_WIDTH
SCREEN_WIDTH = SIDE_PANEL_WIDTH + BOARD_WIDTH
SCREEN_HEIGHT = BOARD_HEIGHT

PREVIEW_CELL_SIZE = 20

FALL_INTERVAL_MS = 500

BLACK = (15, 15, 15)
GRAY = (40, 40, 40)
WHITE = (230, 230, 230)

# 테트로미노 정의: 4x4 그리드 기준 좌표 목록 (기본 방향)
TETROMINOES = {
    "I": {"cells": [(0, 1), (1, 1), (2, 1), (3, 1)], "color": (0, 255, 255)},
    "O": {"cells": [(0, 1), (0, 2), (1, 1), (1, 2)], "color": (255, 255, 0)},
    "T": {"cells": [(0, 1), (1, 0), (1, 1), (1, 2)], "color": (160, 0, 240)},
    "S": {"cells": [(0, 1), (0, 2), (1, 0), (1, 1)], "color": (0, 255, 0)},
    "Z": {"cells": [(0, 0), (0, 1), (1, 1), (1, 2)], "color": (255, 0, 0)},
    "J": {"cells": [(0, 0), (1, 0), (1, 1), (1, 2)], "color": (0, 0, 255)},
    "L": {"cells": [(0, 2), (1, 0), (1, 1), (1, 2)], "color": (255, 165, 0)},
}


class Piece:
    def __init__(self, shape):
        self.shape = shape
        self.color = TETROMINOES[shape]["color"]
        self.cells = [list(cell) for cell in TETROMINOES[shape]["cells"]]
        self.row = 0
        self.col = COLS // 2 - 2

    def occupied_cells(self, row=None, col=None, cells=None):
        row = self.row if row is None else row
        col = self.col if col is None else col
        cells = self.cells if cells is None else cells
        return [(row + r, col + c) for r, c in cells]

    def rotated_cells(self):
        if self.shape == "O":
            return [list(cell) for cell in self.cells]
        # 4x4 그리드 안에서 시계방향 회전: (r, c) -> (c, 3 - r)
        return [[c, 3 - r] for r, c in self.cells]


class Board:
    def __init__(self):
        self.grid = [[None for _ in range(COLS)] for _ in range(ROWS)]

    def is_valid_position(self, cells):
        for row, col in cells:
            if col < 0 or col >= COLS or row >= ROWS:
                return False
            if row >= 0 and self.grid[row][col] is not None:
                return False
        return True

    def lock_piece(self, piece):
        for row, col in piece.occupied_cells():
            if row >= 0:
                self.grid[row][col] = piece.color

    def clear_full_lines(self):
        remaining_rows = [row for row in self.grid if any(cell is None for cell in row)]
        cleared = ROWS - len(remaining_rows)
        new_rows = [[None for _ in range(COLS)] for _ in range(cleared)]
        self.grid = new_rows + remaining_rows
        return cleared


def spawn_piece():
    shape = random.choice(list(TETROMINOES.keys()))
    return Piece(shape)


def try_move(board, piece, drow, dcol):
    cells = piece.occupied_cells(piece.row + drow, piece.col + dcol)
    if board.is_valid_position(cells):
        piece.row += drow
        piece.col += dcol
        return True
    return False


def try_rotate(board, piece):
    new_cells = piece.rotated_cells()
    cells = piece.occupied_cells(cells=new_cells)
    if board.is_valid_position(cells):
        piece.cells = new_cells
        return True
    return False


def hard_drop(board, piece):
    while try_move(board, piece, 1, 0):
        pass


def draw_next_piece_preview(screen, font, next_piece):
    label = font.render("NEXT", True, WHITE)
    screen.blit(label, (15, 15))

    origin_x, origin_y = 15, 50
    for row, col in TETROMINOES[next_piece.shape]["cells"]:
        rect = (
            origin_x + col * PREVIEW_CELL_SIZE,
            origin_y + row * PREVIEW_CELL_SIZE,
            PREVIEW_CELL_SIZE,
            PREVIEW_CELL_SIZE,
        )
        pygame.draw.rect(screen, next_piece.color, rect)
        pygame.draw.rect(screen, GRAY, rect, 1)


def draw_board(screen, board, piece, next_piece, font, score):
    screen.fill(BLACK)

    pygame.draw.rect(screen, GRAY, (0, 0, SIDE_PANEL_WIDTH, SCREEN_HEIGHT))
    draw_next_piece_preview(screen, font, next_piece)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (15, 160))

    for row in range(ROWS):
        for col in range(COLS):
            rect = (BOARD_OFFSET_X + col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            color = board.grid[row][col]
            if color:
                pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, GRAY, rect, 1)

    for row, col in piece.occupied_cells():
        if row >= 0:
            rect = (BOARD_OFFSET_X + col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, piece.color, rect)
            pygame.draw.rect(screen, GRAY, rect, 1)

    pygame.display.flip()


def draw_game_over(screen, font, score):
    screen.fill(BLACK)
    over_text = font.render("GAME OVER", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(over_text, (SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 - 20))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 + 20))
    pygame.display.flip()


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 28)

    board = Board()
    piece = spawn_piece()
    next_piece = spawn_piece()
    score = 0
    game_over = False

    fall_event = pygame.USEREVENT + 1
    pygame.time.set_timer(fall_event, FALL_INTERVAL_MS)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if game_over:
                continue

            if event.type == fall_event:
                if not try_move(board, piece, 1, 0):
                    board.lock_piece(piece)
                    score += board.clear_full_lines() * 100
                    piece = next_piece
                    next_piece = spawn_piece()
                    if not board.is_valid_position(piece.occupied_cells()):
                        game_over = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    try_move(board, piece, 0, -1)
                elif event.key == pygame.K_RIGHT:
                    try_move(board, piece, 0, 1)
                elif event.key == pygame.K_DOWN:
                    try_move(board, piece, 1, 0)
                elif event.key == pygame.K_UP:
                    try_rotate(board, piece)
                elif event.key == pygame.K_SPACE:
                    hard_drop(board, piece)
                    board.lock_piece(piece)
                    score += board.clear_full_lines() * 100
                    piece = next_piece
                    next_piece = spawn_piece()
                    if not board.is_valid_position(piece.occupied_cells()):
                        game_over = True

        if game_over:
            draw_game_over(screen, font, score)
        else:
            draw_board(screen, board, piece, next_piece, font, score)

        clock.tick(60)


if __name__ == "__main__":
    main()
