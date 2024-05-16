import time
import pygame
import sys


class player:
    def __init__(self, name, score):
        self.name = name
        self.score = score


class defaultPlayer(player):
    def __init__(self, color, score):
        self.name = "Default"
        self.score = score
        self.color = color


class board:
    def set_board(self, board):
        for i in range(8):
            for j in range(8):
                self.board[i][j] = board[i][j]

    def __init__(self):
        self.empty_cell = '-'
        self.dx = [-1, -1, -1, 0, 0, 1, 1, 1]
        self.dy = [-1, 0, 1, -1, 1, -1, 0, 1]
        self.board = []
        for i in range(8):
            self.board.append([])
            for _ in range(8):
                self.board[i].append(self.empty_cell)
        self.board[3][3] = 'W'
        self.board[3][4] = 'B'
        self.board[4][3] = 'B'
        self.board[4][4] = 'W'
        self.turn = 0
        self.real_colors = {'B': 'Black', 'W': 'White'}

    def handle_board_after_move(self):
        for i in range(8):
            for j in range(8):
                if isinstance(self.board[i][j], int):
                    self.board[i][j] = self.empty_cell

    def empty_visit(self):
        for i in range(8):
            for j in range(8):
                self.visit[i][j] = False

    def is_valid(self, row, col):
        return row >= 0 and row < 8 and col >= 0 and col < 8

    def check_move(self, row, col, player, count=0):
        for i in range(8):
            x = row + self.dx[i]
            y = col + self.dy[i]
            count = 0
            while self.is_valid(x, y) and self.board[x][y] != player.color and self.board[x][y] != self.empty_cell and not isinstance(self.board[x][y], int):
                x += self.dx[i]
                y += self.dy[i]
                count += 1
            if self.is_valid(x, y) and (self.board[x][y] == self.empty_cell or isinstance(self.board[x][y], int)) and count > 0:
                if self.board[x][y] == self.empty_cell:
                    self.board[x][y] = count
                else:
                    self.board[x][y] += count

    def get_available_moves(self, player):
        isThereAnyMove = False
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == player.color:
                    self.check_move(i, j, player)
        for i in range(8):
            for j in range(8):
                if isinstance(self.board[i][j], int):
                    isThereAnyMove = True
                    break
        return isThereAnyMove

    def print_board(self):
        for i in range(8):
            for j in range(8):
                print(self.board[i][j], end=' | ')
            print()
            for _ in range(8):
                print('-', end=' - ')
            print()

    def make_move(self, row, col, player, secondPlayer):
        if isinstance(self.board[row][col], int):
            self.board[row][col] = player.color
            player.score += 1
            for i in range(8):
                x = row + self.dx[i]
                y = col + self.dy[i]
                while self.is_valid(x, y) and self.board[x][y] != player.color and not isinstance(self.board[x][y], int) and self.board[x][y] != self.empty_cell:
                    x += self.dx[i]
                    y += self.dy[i]
                if self.is_valid(x, y) and self.board[x][y] == player.color:
                    x = row + self.dx[i]
                    y = col + self.dy[i]

                    while self.is_valid(x, y) and self.board[x][y] != player.color and not isinstance(self.board[x][y], int) and self.board[x][y] != self.empty_cell:
                        player.score += 1
                        secondPlayer.score -= 1
                        self.board[x][y] = player.color
                        x += self.dx[i]
                        y += self.dy[i]

            return True
        else:
            return False

    def printGui(self, screen, plus):
        for i in range(8):
            for j in range(8):
                pygame.draw.rect(screen, (0, 133, 100), pygame.Rect(plus +
                                                                    j * 100, i * 100, 100, 100))
                pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(plus +
                                                                j * 100, i * 100, 100, 100), 1)

                if isinstance(self.board[i][j], int):
                    screen.blit(pygame.font.SysFont(
                        'Arial', 30).render(str(self.board[i][j]), True, (0, 0, 0)), (plus + j * 100 + 42, i * 100 + 35))
                    pygame.draw.circle(
                        screen, (0, 0, 0), (plus + j * 100 + 50, i * 100 + 50), 40, 1)
                if self.board[i][j] == 'B':
                    pygame.draw.circle(
                        screen, (0, 0, 0), (plus + j * 100 + 50, i * 100 + 50), 40)
                elif self.board[i][j] == 'W':
                    pygame.draw.circle(
                        screen, (255, 255, 255), (plus + j * 100 + 50, i * 100 + 50), 40)


class boardEvaluation:
    def __init__(self, board, player):
        self.board = board
        self.player = player
        self.evalBoard = [[100, -30, 6, 2, 2, 6, -30, 100],
                          [-30, -50, 0, 0, 0, 0, -50, -30],
                          [6, 0, 0, 0, 0, 0, 0, 6],
                          [2, 0, 0, 3, 3, 0, 0, 2],
                          [2, 0, 0, 3, 3, 0, 0, 2],
                          [6, 0, 0, 0, 0, 0, 0, 6],
                          [-30, -50, 0, 0, 0, 0, -50, -30],
                          [100, -30, 6, 2, 2, 6, -30, 100]]

    def evaluate(self):
        score = 0
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == self.player.color:
                    score += self.evalBoard[i][j]
        return score


class aiPlayer(player):
    def __init__(self, color, score, difficulty):
        self.name = "AI"
        self.score = score
        self.color = color
        self.difficulty = difficulty

    def getBestMove(self, currentBoard, depth, alpha, beta, isMaximizingPlayer, currentPlayer, secondPlayer, first=True):
        # i have to handle the other bases cases
        # in case of depth = 0
        # in case of no moves available
        # in case of end of the game

        if depth == 0:
            return boardEvaluation(currentBoard.board, currentPlayer).evaluate()
        if isMaximizingPlayer:
            bestVal = -10000000000
            finalBoard = None
            for i in range(8):
                for j in range(8):
                    if isinstance(currentBoard.board[i][j], int):
                        newBoard = board()
                        newBoard.set_board(currentBoard.board)
                        if newBoard.make_move(i, j, currentPlayer, secondPlayer):
                            newBoard.handle_board_after_move()
                            if newBoard.get_available_moves(secondPlayer):
                                value = self.getBestMove(
                                    newBoard, depth - 1, alpha, beta, False, secondPlayer, currentPlayer,  False)
                                if first:
                                    if value > bestVal:
                                        bestVal = value
                                        newBoard.handle_board_after_move()
                                        finalBoard = board()
                                        finalBoard.set_board(newBoard.board)

                                bestVal = max(bestVal, value)
                                alpha = max(alpha, bestVal)
                                if beta <= alpha:
                                    return bestVal
                            else:
                                value = boardEvaluation(
                                    newBoard.board, currentPlayer).evaluate()
                                if first:
                                    if value > bestVal:
                                        bestVal = value
                                        newBoard.handle_board_after_move()
                                        finalBoard = board()
                                        finalBoard.set_board(newBoard.board)
                                bestVal = max(bestVal, value)
                                alpha = max(alpha, bestVal)
                                if beta <= alpha:
                                    return bestVal

            if first:
                return finalBoard
            else:
                return bestVal
        else:
            bestVal = 10000000000
            for i in range(8):
                for j in range(8):
                    if isinstance(currentBoard.board[i][j], int):
                        newBoard = board()
                        newBoard.set_board(currentBoard.board)
                        if newBoard.make_move(i, j, currentPlayer, secondPlayer):
                            if newBoard.get_available_moves(secondPlayer):
                                value = self.getBestMove(
                                    newBoard, depth - 1, alpha, beta, True, secondPlayer, currentPlayer,  False)
                                bestVal = min(bestVal, value)
                                beta = min(beta, bestVal)
                                if beta <= alpha:
                                    return bestVal  # pruning
                            else:
                                value = boardEvaluation(
                                    newBoard.board, currentPlayer).evaluate()
                                if first:
                                    if value > bestVal:
                                        bestVal = value
                                        newBoard.handle_board_after_move()
                                        finalBoard = board()
                                        finalBoard.set_board(newBoard.board)
                                bestVal = min(bestVal, value)
                                beta = min(beta, bestVal)
                                if beta <= alpha:
                                    return bestVal  # pruning
            return bestVal

    def makeMove(self, board, secondPlayer):
        # write the minimax algorithm and alpha beta pruning here
        bestMove = self.getBestMove(
            board, self.difficulty, -10000000000, 10000000000, True, self,  secondPlayer, True)
        self.score = 0
        secondPlayer.score = 0
        board.set_board(bestMove.board)
        for i in range(8):
            for j in range(8):
                self.score += 1 if bestMove.board[i][j] == self.color else 0
                secondPlayer.score += 1 if bestMove.board[i][j] == secondPlayer.color else 0
        print("AI has made a move")

        return bestMove


class game:
    def __init__(self, player1, player2, board):
        self.board = board
        self.player1 = player1
        self.player2 = player2

    def play(self):
        player = self.player1
        while not self.board.check_end():
            print("Player: ", player.color)
            if self.board.check_end():
                if not self.board.check_tie():
                    print("Tie!")
                else:
                    print("Winner is: ", self.board.check_win())
                break
            self.board.get_available_moves(player)
            self.board.print_board()
            if isinstance(player, aiPlayer):
                print("AI is making move")
                player.makeMove(self.board)
                if player == self.player1:
                    player = self.player2
                else:
                    player = self.player1
            else:
                row = int(input("Enter row: "))
                col = int(input("Enter col: "))
                if self.board.make_move(row, col, player):
                    if player == self.player1:
                        player = self.player2
                    else:
                        player = self.player1
                else:
                    print("Invalid move!")
            self.board.handle_board_after_move()

        print("Game over!")


class Button:
    def __init__(self, x, y, width, height, text, color, screen):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.screen = screen

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        self.screen.blit(text_surface, text_rect)


class guiGame:
    def welcomePage(self):
        button1 = Button(480, 220, 250, 100, "Easy",
                         (255, 255, 255), self.screen)

        button2 = Button(480, 370, 250, 100, "Medium",
                         (255, 255, 255), self.screen)

        button3 = Button(480, 520, 250, 100, "Hard",
                         (255, 255, 255), self.screen)
        self.screen.blit(self.gameText.render(
            "Hello in Othello Game Project", True, (255, 255, 255)), (450, 100))
        self.screen.blit(self.gameText.render(
            "Choose Ai level to start", True, (255, 255, 255)), (480, 150))
        button1.draw()
        button2.draw()
        button3.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if start button is clicked
                if button1.rect.collidepoint(event.pos):
                    self.currentPage = 1
                    self.player2 = aiPlayer('W', 2, 1)
                    self.player1 = defaultPlayer('B', 2)
                    self.players = [self.player1, self.player2]
                elif button2.rect.collidepoint(event.pos):
                    self.currentPage = 1
                    self.player2 = aiPlayer('W', 2, 3)
                    self.player1 = defaultPlayer('B', 2)
                    self.players = [self.player1, self.player2]
                elif button3.rect.collidepoint(event.pos):
                    self.currentPage = 1
                    self.player2 = aiPlayer('W', 2, 5)
                    self.player1 = defaultPlayer('B', 2)
                    self.players = [self.player1, self.player2]

        pygame.display.flip()

    def gamePage(self):
        self.screen.fill((0, 0, 0))
        player = self.players[self.current]
        if self.playing:
            player = self.players[self.current]
            self.board.handle_board_after_move()

            if not self.board.get_available_moves(player):
                if self.players[0].score == 0 or self.players[1].score == 0:
                    # one player has no moves available
                    self.playing = False
                    if self.players[0].score > self.players[1].score:
                        print("Winner is: ", self.players[0].color)
                        self.winner = self.players[0]
                    else:
                        self.winner = self.players[1]
                        print("Winner is: ", self.players[1].color)
                self.current = 1 - self.current
                print("No moves available for: ", player.color)

            self.board.printGui(self.screen, self.width - 800)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and self.playing and isinstance(player, defaultPlayer):
                pos = pygame.mouse.get_pos()
                x = pos[1] // 100
                y = (pos[0] - (self.width - 800)) // 100

                if isinstance(self.board.board[x][y], int):
                    # row, col
                    self.board.make_move(
                        x, y, player, self.players[1 - self.current])
                    self.current = 1 - self.current
            if event.type == pygame.QUIT:
                self.running = False
        if self.players[0].score + self.players[1].score == 64 and self.playing:
            if self.players[0].score > self.players[1].score:
                self.winner = self.players[0]
            elif self.players[0].score < self.players[1].score:
                self.winner = self.players[1]

            self.playing = False

        self.board.printGui(self.screen, self.width - 800)
        if not self.playing:
            if self.winner:
                self.screen.blit(self.gameText.render("Winner is: " + self.board.real_colors[self.winner.color],
                                                      True, (255, 255, 255)), (100, 100))
            else:
                self.screen.blit(self.gameText.render(
                    "Tie!", True, (255, 255, 255)), (100, 100))
        else:
            self.screen.blit(self.gameText.render("Current Player: " + player.color,
                                                  True, (255, 255, 255)), (100, 200))
        self.screen.blit(self.gameText.render(self.board.real_colors[self.players[0].color] + " Score: " + str(self.players[0].score), True, (255, 255, 255)),
                         (100, 300))
        self.screen.blit(self.gameText.render(self.board.real_colors[self.players[1].color] + " Score: " + str(self.players[1].score), True, (255, 255, 255)),
                         (100, 400))

        pygame.display.update()
        if isinstance(player, aiPlayer) and self.board.get_available_moves(player):
            player.makeMove(self.board, self.players[1 - self.current])
            self.current = 1 - self.current

    def __init__(self):
        self.player1 = None
        self.player2 = None
        self.board = None
        self.current = 0
        self.players = []
        self.screen = None
        self.winner = None
        self.playing = True
        self.currentPage = 0
        self.width = 1200
        self.height = 800
        self.running = True
        self.gameText = None

    def play(self):
        self.board = board()
        self.player1 = defaultPlayer('B', 2)
        self.player2 = defaultPlayer('W', 2)

        # case
        # player1 = aiPlayer('B', 2, 2)
        # player2 = aiPlayer('W', 2, 1)
        # causes player 1 to win with taking all positions
        # and the other player has no moves available

        # case
        # player1 = aiPlayer('B', 2, 5)
        # player2 = aiPlayer('W', 2, 3)
        # white wins

        pygame.init()
        self.gameText = pygame.font.SysFont('Arial', 30)
        self.players = [self.player1, self.player2]

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Othello")

        self.running = True
        self.player = self.players[self.current]

        while self.running:
            if self.currentPage == 0:
                self.welcomePage()
            elif self.currentPage == 1:
                self.gamePage()
        pygame.quit()


if __name__ == "__main__":
    g = guiGame()
    g.play()
