import random
from collections import deque
from constants import *


class EnemyAI:
    def __init__(self, width=WIDTH, height=HEIGHT):
        self.width = width
        self.height = height
        # handle a short delay when food respawns
        self._target_food = None
        self._pending_food = None
        self._food_delay = 0

    def choose_direction(self, start, current_direction, food, snake, enemy, mistake_chance=0.08):
        directions = [RIGHT, LEFT, DOWN, UP]

        # if this is the first call, lock in the current food target
        if self._target_food is None:
            self._target_food = food

        # if food has changed, start a short delay before switching targets
        if food != self._target_food and self._food_delay == 0:
            self._pending_food = food
            self._food_delay = 3

        # while delaying, continue acting on the old food target
        if self._food_delay > 0:
            food_to_use = self._target_food
            self._food_delay -= 1
            if self._food_delay == 0:
                self._target_food = self._pending_food
                self._pending_food = None
        else:
            food_to_use = food
            self._target_food = food

        # defaults for best move/score
        best_move = current_direction
        best_score = -9999

        # combine occupied cells to avoid
        blocked = set(snake + enemy)

        opponent_head = snake[0] if snake else None
        current_opponent_dist = (
            abs(start[0] - opponent_head[0]) + abs(start[1] - opponent_head[1])
            if opponent_head
            else float("inf")
        )

        survival_weight = 0.0
        if current_opponent_dist <= 5:
            survival_weight = 3.0
        elif current_opponent_dist <= 8:
            survival_weight = 1.5

        # attempt to find a path to the food
        path_to_food = self.find_path(start, food_to_use, blocked) or []

        for dx, dy in directions:
            # prevent reversing direction into self
            ex, ey = current_direction
            if (ex + dx, ey + dy) == (0, 0):
                continue

            nx, ny = start[0] + dx, start[1] + dy
            next_pos = (nx, ny)

            # reject moves outside the board
            if nx < 0 or nx >= self.width or ny < 0 or ny >= self.height:
                continue

            # avoid immediate collisions with bodies
            if next_pos in blocked:
                continue

            # compute a simple heuristic score for this move
            score = 0

            # closer to food is better, but only if the food is reachable
            if path_to_food:
                dist_food = abs(food_to_use[0] - nx) + abs(food_to_use[1] - ny)
                score -= dist_food * 2
            else:
                score -= 1

            # prefer moves that have more free space (flood fill)
            space = self.flood_fill(next_pos, blocked)
            score += space * 2.0

            # penalize hard dead-ends unless the food is directly there
            safe_exits = self.get_safe_neighbor_count(next_pos, blocked)
            if safe_exits == 0 and next_pos != food_to_use:
                continue
            if safe_exits == 1 and next_pos != food_to_use:
                score -= 12
            elif safe_exits == 2:
                score -= 4

            # prefer moves that keep the enemy away from close walls
            score += self.wall_distance(next_pos) * 0.8

            # survival bias when opponent is close
            if opponent_head and survival_weight > 0:
                opp_dist = abs(opponent_head[0] - nx) + abs(opponent_head[1] - ny)
                score += opp_dist * survival_weight
                if current_opponent_dist <= 3 and opp_dist <= current_opponent_dist:
                    score -= 10
                if current_opponent_dist <= 2 and opp_dist <= 1:
                    score -= 16

            # avoid moves that lead into narrow corridors when not seeking food
            if safe_exits <= 2 and next_pos != food_to_use:
                score -= 3

            # encourage following a safe shortest path to the food when one exists
            if path_to_food and next_pos in path_to_food:
                score += 4

            # add a bit of randomness to avoid ties
            score += random.uniform(-1, 1)

            # slight bias to move forward
            score += 1

            if score > best_score:
                best_score = score
                best_move = (dx, dy)

        if best_score <= -999:
            return self.safe_move(start, current_direction, snake, enemy)

        # probability of making a mistake increases with snake length
        pressure = len(snake) / 20
        if random.random() < mistake_chance + pressure * 0.002:
            return current_direction

        return best_move

    def find_path(self, start, target, blocked):
        # Find shortest path from start to target avoiding blocked
        queue = deque([start])
        came_from = {start: None}

        while queue:
            current = queue.popleft()
            if current == target:
                # reconstruct path when target reached
                path = []
                while current is not None:
                    path.append(current)
                    current = came_from[current]
                return list(reversed(path))

            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = current[0] + dx, current[1] + dy
                nxt = (nx, ny)

                # skip visited or invalid positions
                if nxt in came_from:
                    continue
                if nx < 0 or nx >= self.width or ny < 0 or ny >= self.height:
                    continue
                if nxt in blocked:
                    continue

                came_from[nxt] = current
                queue.append(nxt)

        # no path found
        return []

    def flood_fill(self, start, blocked):
        # count reachable tiles from start avoiding blocked cells
        queue = deque([start])
        visited = {start}

        while queue:
            x, y = queue.popleft()
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = x + dx, y + dy
                nxt = (nx, ny)

                # skip visited or out-of-bounds or blocked
                if nxt in visited:
                    continue
                if nx < 0 or nx >= self.width or ny < 0 or ny >= self.height:
                    continue
                if nxt in blocked:
                    continue

                visited.add(nxt)
                queue.append(nxt)

        # return number of reachable tiles
        return len(visited)

    def get_safe_neighbor_count(self, position, blocked):
        count = 0
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = position[0] + dx, position[1] + dy
            nxt = (nx, ny)
            if nx < 0 or nx >= self.width or ny < 0 or ny >= self.height:
                continue
            if nxt in blocked:
                continue
            count += 1
        return count

    def wall_distance(self, position):
        x, y = position
        return min(x, y, self.width - 1 - x, self.height - 1 - y)

    def safe_move(self, head, current_direction, snake, enemy):
        # choose the safest adjacent move based on free space and avoidance
        directions = [RIGHT, LEFT, DOWN, UP]
        ex, ey = current_direction
        best_move = current_direction
        best_score = -9999

        for dx, dy in directions:
            if (ex + dx, ey + dy) == (0, 0):
                continue

            nx, ny = head[0] + dx, head[1] + dy
            next_pos = (nx, ny)
            if nx < 0 or nx >= self.width or ny < 0 or ny >= self.height:
                continue
            if next_pos in snake or next_pos in enemy:
                continue

            space = self.flood_fill(next_pos, set(snake + enemy))
            score = space + self.wall_distance(next_pos) * 0.5
            if score > best_score:
                best_score = score
                best_move = (dx, dy)

        return best_move

        for dx, dy in directions:
            # prevent reverse
            if (ex + dx, ey + dy) == (0, 0):
                continue

            nx, ny = head[0] + dx, head[1] + dy
            # skip invalid or occupied positions
            if nx < 0 or nx >= self.width or ny < 0 or ny >= self.height:
                continue
            if (nx, ny) in snake or (nx, ny) in enemy:
                continue

            return (dx, dy)

        # if no safe move, keep current
        return current_direction