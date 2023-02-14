import pygame
import sys
import time
from solver import Sudoku
import random


pygame.init()

# var pour la taille de l'interface et de ses composants
cell_size = 50
minor_grid_size = 1
major_grid_size = 3
buffer = 5
button_height = 50
button_width = 125
button_border = 2
width = cell_size*9 + minor_grid_size*6 + major_grid_size*4 + buffer*2
height = cell_size*9 + minor_grid_size*6 + \
    major_grid_size*4 + button_height + buffer*3 + button_border*2
size = width, height
white = 255, 255, 255
black = 0, 0, 0
gray = 200, 200, 200
green = 0, 175, 0
red = 200, 0, 0
inactive_btn = '#03989e'
active_btn = '#00c2cb'


pygame.display.set_caption('Sudoku')


class RectCell(pygame.Rect):

    def __init__(self, left, top, row, col):
        super().__init__(left, top, cell_size, cell_size)
        self.row = row
        self.col = col


def create_cells():

    cells = [[] for _ in range(9)]

    # Set attributes for for first RectCell
    row = 0
    col = 0
    left = buffer + major_grid_size
    top = buffer + major_grid_size

    while row < 9:
        while col < 9:
            cells[row].append(RectCell(left, top, row, col))

            # Update attributes for next RectCell
            left += cell_size + minor_grid_size
            if col != 0 and (col + 1) % 3 == 0:
                left = left + major_grid_size - minor_grid_size
            col += 1

        # Update attributes for next RectCell
        top += cell_size + minor_grid_size
        if row != 0 and (row + 1) % 3 == 0:
            top = top + major_grid_size - minor_grid_size
        left = buffer + major_grid_size
        col = 0
        row += 1

    return cells


def draw_grid():


    lines_drawn = 0
    pos = buffer + major_grid_size + cell_size
    while lines_drawn < 6:
        pygame.draw.line(screen, black, (pos, buffer),
                         (pos, width-buffer-1), minor_grid_size)
        pygame.draw.line(screen, black, (buffer, pos),
                         (width-buffer-1, pos), minor_grid_size)


        lines_drawn += 1


        pos += cell_size + minor_grid_size
        if lines_drawn % 2 == 0:
            pos += cell_size + major_grid_size


    for pos in range(buffer+major_grid_size//2, width, cell_size*3 + minor_grid_size*2 + major_grid_size):
        pygame.draw.line(screen, black, (pos, buffer),
                         (pos, width-buffer-1), major_grid_size)
        pygame.draw.line(screen, black, (buffer, pos),
                         (width-buffer-1, pos), major_grid_size)


def fill_cells(cells, board):

    font = pygame.font.Font(None, 36)

    # remplir la grille
    for row in range(9):
        for col in range(9):
            if board.board[row][col].value is None:
                continue

            if not board.board[row][col].editable:
                font.bold = True
                text = font.render(f'{board.board[row][col].value}', 1, black)

            # affichage de la bonne reponse en vert et la mauvaise en rouge
            else:
                font.bold = False
                if board.check_move(board.board[row][col], board.board[row][col].value):
                    text = font.render(
                        f'{board.board[row][col].value}', 1, green)
                else:
                    text = font.render(
                        f'{board.board[row][col].value}', 1, red)

            # center les valeurs de chaque case
            xpos, ypos = cells[row][col].center
            textbox = text.get_rect(center=(xpos, ypos))
            screen.blit(text, textbox)


def draw_button(left, top, width, height, border, color, border_color, text):
# creation des bouttons
    pygame.draw.rect(
        screen,
        border_color,
        (left, top, width+border*2, height+border*2),
    )

    button = pygame.Rect(
        left+border,
        top+border,
        width,
        height
    )
    pygame.draw.rect(screen, color, button)

    # parametre du texte des bouttons
    font = pygame.font.Font(None, 26)
    text = font.render(text, 1, black)
    xpos, ypos = button.center
    textbox = text.get_rect(center=(xpos, ypos))
    screen.blit(text, textbox)

    return button


def draw_board(active_cell, cells, game):
#parametres de la grille et des cases
    draw_grid()
    if active_cell is not None:
        pygame.draw.rect(screen, gray, active_cell)

    #remplissage des cases
    fill_cells(cells, game)


def visual_solve(game, cells):
#affichage du solver
    #trouver la premiere cases vide
    cell = game.get_empty_cell()

    # si cell == faux grille complete
    if not cell:
        return True

    # essaie de chaque possibilité
    for val in range(1, 10):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # remplir la case avec la valeur
        cell.value = val

        # Cellule de contour modifiée en rouge
        screen.fill(white)
        draw_board(None, cells, game)
        cell_rect = cells[cell.row][cell.col]
        pygame.draw.rect(screen, red, cell_rect, 5)
        pygame.display.update([cell_rect])
        time.sleep(0.05)

        # Vérification  de la valeur
        if not game.check_move(cell, val):
            cell.value = None
            continue

       # Si tous les appels récursifs renvoient True la grille est résolue
        screen.fill(white)
        pygame.draw.rect(screen, green, cell_rect, 5)
        draw_board(None, cells, game)
        pygame.display.update([cell_rect])
        if visual_solve(game, cells):
            return True
        cell.value = None
    screen.fill(white)
    pygame.draw.rect(screen, white, cell_rect, 5)
    draw_board(None, cells, game)
    pygame.display.update([cell_rect])
    return False


def check_sudoku(sudoku):

    # verification que toute les cases sont valides
    if sudoku.get_empty_cell():
        raise ValueError('Game is not complete')

    # Will hold values for each row, column, and box
    row_sets = [set() for _ in range(9)]
    col_sets = [set() for _ in range(9)]
    box_sets = [set() for _ in range(9)]

    # Check all rows, columns, and boxes contain no duplicates
    for row in range(9):
        for col in range(9):
            box = (row // 3) * 3 + col // 3
            value = sudoku.board[row][col].value

            # Check if number already encountered in row, column, or box
            if value in row_sets[row] or value in col_sets[col] or value in box_sets[box]:
                return False

            # Add value to corresponding set
            row_sets[row].add(value)
            col_sets[col].add(value)
            box_sets[box].add(value)

    # All rows, columns, and boxes are valid
    return True

from random import shuffle
import copy


#generation de la grille
class SudokuGenerator:


    def __init__(self, grid=None):
        self.counter = 0

        self.path = []
    #remplir notre grille avec des 0
        if grid:
            if len(grid[0]) == 9 and len(grid) == 9:
                self.grid = grid
                self.original = copy.deepcopy(grid)
                self.solve_input_sudoku()
        else:

            self.grid = [[0 for i in range(9)] for j in range(9)]
            self.generate_puzzle()
            self.original = copy.deepcopy(self.grid)


    def solve_input_sudoku(self):

        self.generate_solution(self.grid)
        return

    def generate_puzzle(self):

        self.generate_solution(self.grid)
        return

    def print_grid(self, grid_name=None):
        if grid_name:
            print(grid_name)
        for row in self.grid:
            print(row)
        return

    def test_sudoku(self, grid):
        for row in range(9):
            for col in range(9):
                num = grid[row][col]

                grid[row][col] = 0
                if not self.valid_location(grid, row, col, num):
                    return False
                else:

                    grid[row][col] = num
        return True

    def num_used_in_row(self, grid, row, number):

        if number in grid[row]:
            return True
        return False

    def num_used_in_column(self, grid, col, number):

        for i in range(9):
            if grid[i][col] == number:
                return True
        return False

    def num_used_in_subgrid(self, grid, row, col, number):

        sub_row = (row // 3) * 3
        sub_col = (col // 3) * 3
        for i in range(sub_row, (sub_row + 3)):
            for j in range(sub_col, (sub_col + 3)):
                if grid[i][j] == number:
                    return True
        return False

    def valid_location(self, grid, row, col, number):

        if self.num_used_in_row(grid, row, number):
            return False
        elif self.num_used_in_column(grid, col, number):
            return False
        elif self.num_used_in_subgrid(grid, row, col, number):
            return False
        return True

    def find_empty_square(self, grid):

        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    return (i, j)
        return

    def solve_puzzle(self, grid):

        for i in range(0, 81):
            row = i // 9
            col = i % 9
            # trouver la prochaine cases vide
            if grid[row][col] == 0:
                for number in range(1, 10):
                    # verification du respect des regles du soduku
                    if self.valid_location(grid, row, col, number):
                        grid[row][col] = number
                        if not self.find_empty_square(grid):
                            self.counter += 1
                            break
                        else:
                            if self.solve_puzzle(grid):
                                return True
                break
        grid[row][col] = 0
        return False

    def generate_solution(self, grid):

        number_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for i in range(0, 81):
            row = i // 9
            col = i % 9
            # trouver les case a replir
            if grid[row][col] == 0:
                shuffle(number_list)
                for number in number_list:
                    if self.valid_location(grid, row, col, number):
                        self.path.append((number, row, col))
                        grid[row][col] = number
                        if not self.find_empty_square(grid):
                            return True
                        else:
                            if self.generate_solution(grid):
                                # si la grille est complete
                                return True
                break
        grid[row][col] = 0
        return False

    def get_non_empty_squares(self, grid):

        non_empty_squares = []
        for i in range(len(grid)):
            for j in range(len(grid)):
                if grid[i][j] != 0:
                    non_empty_squares.append((i, j))
        shuffle(non_empty_squares)
        return non_empty_squares

new_puzzle = SudokuGenerator()


def play():

    easy = new_puzzle.grid
    game = Sudoku(easy)
    cells = create_cells()
    active_cell = None
    solve_rect = pygame.Rect(
        buffer,
        height-button_height - button_border*2 - buffer,
        button_width + button_border*2,
        button_height + button_border*2
    )

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()


            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()

                #clique sur  le button reinitialiser
                if reset_btn.collidepoint(mouse_pos):
                    game.reset()

                # clique sur le button resoudre
                if solve_btn.collidepoint(mouse_pos):
                    screen.fill(white)
                    active_cell = None
                    draw_board(active_cell, cells, game)
                    reset_btn = draw_button(
                        width - buffer - button_border*2 - button_width,
                        height - button_height - button_border*2 - buffer,
                        button_width,
                        button_height,
                        button_border,
                        inactive_btn,
                        black,
                        'Réinitialiser'
                    )
                    solve_btn = draw_button(
                        width - buffer*2 - button_border*4 - button_width*2,
                        height - button_height - button_border*2 - buffer,
                        button_width,
                        button_height,
                        button_border,
                        inactive_btn,
                        black,
                        'Résoudre '
                    )
                    pygame.display.flip()
                    visual_solve(game, cells)


                active_cell = None
                for row in cells:
                    for cell in row:
                        if cell.collidepoint(mouse_pos):
                            active_cell = cell

                # verification si des cases sont vides
                if active_cell and not game.board[active_cell.row][active_cell.col].editable:
                    active_cell = None


            if event.type == pygame.KEYUP:
                if active_cell is not None:

                    # choix de la case a remplir
                    if event.key == pygame.K_0 or event.key == pygame.K_KP0:
                        game.board[active_cell.row][active_cell.col].value = 0
                    if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                        game.board[active_cell.row][active_cell.col].value = 1
                    if event.key == pygame.K_2 or event.key == pygame.K_KP2:
                        game.board[active_cell.row][active_cell.col].value = 2
                    if event.key == pygame.K_3 or event.key == pygame.K_KP3:
                        game.board[active_cell.row][active_cell.col].value = 3
                    if event.key == pygame.K_4 or event.key == pygame.K_KP4:
                        game.board[active_cell.row][active_cell.col].value = 4
                    if event.key == pygame.K_5 or event.key == pygame.K_KP5:
                        game.board[active_cell.row][active_cell.col].value = 5
                    if event.key == pygame.K_6 or event.key == pygame.K_KP6:
                        game.board[active_cell.row][active_cell.col].value = 6
                    if event.key == pygame.K_7 or event.key == pygame.K_KP7:
                        game.board[active_cell.row][active_cell.col].value = 7
                    if event.key == pygame.K_8 or event.key == pygame.K_KP8:
                        game.board[active_cell.row][active_cell.col].value = 8
                    if event.key == pygame.K_9 or event.key == pygame.K_KP9:
                        game.board[active_cell.row][active_cell.col].value = 9
                    if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                        game.board[active_cell.row][active_cell.col].value = None

        screen.fill(white)

        # dessin de la grille
        draw_board(active_cell, cells, game)

        # creation des bouttons
        reset_btn = draw_button(
            width - buffer - button_border*2 - button_width,
            height - button_height - button_border*2 - buffer,
            button_width,
            button_height,
            button_border,
            inactive_btn,
            black,
            'Réinitialiser'
        )
        solve_btn = draw_button(
            width - buffer*2 - button_border*4 - button_width*2,
            height - button_height - button_border*2 - buffer,
            button_width,
            button_height,
            button_border,
            inactive_btn,
            black,
            'Résoudre'
        )

        # la souris sur un des bouttons
        if reset_btn.collidepoint(pygame.mouse.get_pos()):
            reset_btn = draw_button(
                width - buffer - button_border*2 - button_width,
                height - button_height - button_border*2 - buffer,
                button_width,
                button_height,
                button_border,
                active_btn,
                black,
                'Réinitialiser'
            )
        if solve_btn.collidepoint(pygame.mouse.get_pos()):
            solve_btn = draw_button(
                width - buffer*2 - button_border*4 - button_width*2,
                height - button_height - button_border*2 - buffer,
                button_width,
                button_height,
                button_border,
                active_btn,
                black,
                'Résoudre '
            )

        # verifier si la grille est complete
        if not game.get_empty_cell():
            if check_sudoku(game):
                font = pygame.font.Font(None, 36)
                text = font.render('       Félicitations !! ', 1,black )
                textbox = text.get_rect(center=(solve_rect.center))
                screen.blit(text, textbox)

        pygame.display.flip()

print('Veuillez choisir le niveau de difficulté \n 1 : Facile \n 2 : Moyen  \n 3 : Difficle \n' )
niveau =(input('reponse : '))
while niveau != '1' and niveau != '2' and niveau != 'd' :
    print('Veuillez choisir le niveau de difficulté \n 1 : Facile \n 2 : Moyen  \n 3 : Difficle \n')
    niveau = input('reponse :')
niveau=int(niveau)
if niveau == 1 :
    supp=35
elif niveau == 2 :
    supp = 45
else: supp = 55


for i in range(supp):
    # indice aléatoire du nombre a effacer
    ligne = random.randrange(9)
    col = random.randrange(9)
    # boucle de controle
    while new_puzzle.grid[ligne][col]==0 :
        ligne = random.randrange(9)
        col = random.randrange(9)
    new_puzzle.grid[ligne][col]=0
screen = pygame.display.set_mode(size)
if __name__ == '__main__':
    play()

