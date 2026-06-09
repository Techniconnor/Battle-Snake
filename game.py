import random
from constants import *
from enemy_ai import EnemyAI


class Game:


    def __init__(self):
        # Create AI helpers and initialize the match.
        self.enemy_ai = EnemyAI()
        self.player_ai = EnemyAI()
        self.mode = MODE_PLAYER_VS_ENEMY
        self.reset_match()

    # =========================
    # MATCH SYSTEM
    # =========================
    def reset_match(self):
        # Reset overall match score and round completion state.
        self.player_rounds = 0
        self.enemy_rounds = 0
        self.match_over = False
        self.reset_round()

    # =========================
    # ROUND RESET
    # =========================
    def reset_round(self):
        # Starting positions for the player snake and enemy snake.
        y_center = round(HEIGHT / 2)
        margin = max(3, round(WIDTH * 0.08))

        self.snake = [
            (margin, y_center),
            (margin - 1, y_center),
            (margin - 2, y_center),
        ]
        enemy_head_x = WIDTH - margin
        self.enemy = [
            (enemy_head_x, y_center),
            (enemy_head_x + 1, y_center),
            (enemy_head_x + 2, y_center),
        ]

        # Starting movement directions for both snakes.
        self.direction = RIGHT
        self.enemy_direction = LEFT
        self.enemy_direction_locked = False

        # Spawn food on a random empty cell.
        self.food = self.spawn_food()

        # Round state flags.
        self.game_over = False
        self.direction_locked = False
        self.loser = None

        # Track length-based score for the active round.
        self.player_score = 0
        self.enemy_score = 0

        # Set enemy mistake values
        self.enemy_turn_cooldown = 0
        self.enemy_mistake_chance = 0.08

    # =========================
    # MAIN LOOP
    # =========================
    def update(self):
        # Do nothing if the current round or match has ended.
        if self.game_over or self.match_over:
            return

        # Unlock direction changes for this update cycle.
        self.direction_locked = False
        self.enemy_direction_locked = False

        if self.mode != MODE_PLAYER_VS_PLAYER:
            self.enemy_direction = self.choose_enemy_direction()

        if self.mode == MODE_COMPUTER_VS_COMPUTER:
            self.direction = self.choose_player_ai_direction()

        player_new = self._step(self.snake[0], self.direction)
        enemy_new = self._step(self.enemy[0], self.enemy_direction)

        # -------------------
        # COLLISIONS
        # -------------------
        if self.is_wall_collision(player_new):
            self.end_round("player")
            return

        if self.is_wall_collision(enemy_new):
            self.end_round("enemy")
            return

        if player_new in self.snake:
            self.end_round("player")
            return

        if enemy_new in self.enemy:
            self.end_round("enemy")
            return

        if player_new in self.enemy:
            self.end_round("player")
            return

        if enemy_new in self.snake:
            self.end_round("enemy")
            return

        if player_new == enemy_new:
            ate_food = player_new == self.food
            self.snake.insert(0, player_new)
            self.enemy.insert(0, enemy_new)

            if ate_food:
                self.food = self.spawn_food()
            else:
                self.snake.pop()
                self.enemy.pop()

            self.end_round("both")
            return

        # -------------------
        # MOVE SNAKES
        # -------------------
        self.snake.insert(0, player_new)
        self.enemy.insert(0, enemy_new)

        if player_new == self.food:
            self.food = self.spawn_food()
        else:
            self.snake.pop()

        if enemy_new == self.food:
            self.food = self.spawn_food()
        else:
            self.enemy.pop()

    # =========================
    # ROUND END
    # =========================
    def end_round(self, reason):
        self.game_over = True
        self.loser = reason

        # base scores
        player_score = len(self.snake) - 3
        enemy_score = len(self.enemy) - 3

        # crash penalty (who CAUSED the end). Makes it harder for the winner to win by ending the round.
        if reason == "player":
            player_score -= 5
        elif reason == "enemy":
            enemy_score -= 5


        self.player_score = player_score
        self.enemy_score = enemy_score

        # -------------------------
        # ROUND DECISION
        # -------------------------
        if player_score > enemy_score:
            self.player_rounds += 1
        elif enemy_score > player_score:
            self.enemy_rounds += 1
        else:
            # tie → both punished or shared loss
            self.player_rounds += 1
            self.enemy_rounds += 1

        # match check
        if self.player_rounds >= 3 or self.enemy_rounds >= 3:
            self.match_over = True

    # =========================
    # MATCH CONTROL
    # =========================
    def next_round(self):
        if self.match_over:
            self.reset_match()
        else:
            self.reset_round()

    # Choose the enemy snake direction using the EnemyAI helper.
    def choose_enemy_direction(self):
        start = self.enemy[0]
        return self.enemy_ai.choose_direction(
            start=start,
            current_direction=self.enemy_direction,
            food=self.food,
            snake=self.snake,
            enemy=self.enemy,
            mistake_chance=self.enemy_mistake_chance,
        )

    # Choose the AI direction for the player snake when both are computers.
    def choose_player_ai_direction(self):
        start = self.snake[0]
        return self.player_ai.choose_direction(
            start=start,
            current_direction=self.direction,
            food=self.food,
            snake=self.enemy,
            enemy=self.snake,
            mistake_chance=self.enemy_mistake_chance,
        )

    # Helper for movement vector math.
    @staticmethod
    def _step(position, direction):
        x, y = position
        dx, dy = direction
        return (x + dx, y + dy)

    # =========================
    # COLLISION HELPERS
    def is_wall_collision(self, pos):
        x, y = pos
        # A wall collision happens when the position leaves the grid bounds.
        return x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT

    # =========================
    # INPUT CONTROL
    # =========================
    @staticmethod
    def _is_reverse(current_direction, new_direction):
        return (current_direction[0] + new_direction[0], current_direction[1] + new_direction[1]) == (0, 0)

    def change_direction(self, new_direction, enemy=False):
        # Prevent more than one direction change in a single update cycle.
        if enemy:
            if self.enemy_direction_locked:
                return

            if self._is_reverse(self.enemy_direction, new_direction):
                return

            self.enemy_direction = new_direction
            self.enemy_direction_locked = True
        else:
            if self.direction_locked:
                return

            if self._is_reverse(self.direction, new_direction):
                return

            self.direction = new_direction
            self.direction_locked = True

    # =========================
    # FOOD
    # =========================
    def spawn_food(self):
        # Place food in a random empty space not occupied by any snake.
        occupied = set(self.snake + self.enemy)

        empty = [
            (x, y)
            for x in range(WIDTH)
            for y in range(HEIGHT)
            if (x, y) not in occupied
        ]

        return random.choice(empty)

    # =========================
    # SCORES
    # =========================
    def get_player_score(self):
        # Return how many extra cells the player snake has grown.
        return len(self.snake) - 3

    def get_enemy_score(self):
        return len(self.enemy) - 3