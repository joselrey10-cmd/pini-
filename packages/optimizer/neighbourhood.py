class Neighbourhood:
    def neighbours(self, solution, max_neighbours: int = 200):
        generated = 0
        total = len(solution.sessions)

        for first in range(total):
            for second in range(first + 1, total):
                if generated >= max_neighbours:
                    return
                yield solution.with_swapped_sessions(first, second)
                generated += 1
