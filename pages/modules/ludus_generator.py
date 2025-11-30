import random
from typing import List, Tuple, Dict

def generate_word_search(words: List[str], grid_size: int = 12) -> Tuple[List[List[str]], Dict[str, List[Tuple[int, int]]]]:
    """
    Generate a word search grid with the given words.
    
    Args:
        words: List of words to hide in the grid
        grid_size: Size of the grid (grid_size x grid_size)
    
    Returns:
        Tuple of (grid, word_positions)
        - grid: 2D list of characters
        - word_positions: Dict mapping word to list of (row, col) positions
    """
    # Initialize empty grid
    grid = [['' for _ in range(grid_size)] for _ in range(grid_size)]
    word_positions = {}
    
    # Directions: (row_delta, col_delta)
    directions = [
        (0, 1),   # Horizontal right
        (1, 0),   # Vertical down
        (1, 1),   # Diagonal down-right
        (-1, 1),  # Diagonal up-right
    ]
    
    def can_place_word(word: str, row: int, col: int, direction: Tuple[int, int]) -> bool:
        """Check if word can be placed at given position and direction"""
        dr, dc = direction
        
        for i, char in enumerate(word):
            r, c = row + i * dr, col + i * dc
            
            # Out of bounds
            if not (0 <= r < grid_size and 0 <= c < grid_size):
                return False
            
            # Cell already occupied by different letter
            if grid[r][c] != '' and grid[r][c] != char:
                return False
        
        return True
    
    def place_word(word: str, row: int, col: int, direction: Tuple[int, int]):
        """Place word in the grid and record positions"""
        dr, dc = direction
        positions = []
        
        for i, char in enumerate(word):
            r, c = row + i * dr, col + i * dc
            grid[r][c] = char.upper()
            positions.append((r, c))
        
        word_positions[word] = positions
    
    # Place words
    for word in words:
        placed = False
        attempts = 0
        max_attempts = 100
        
        while not placed and attempts < max_attempts:
            # Random starting position
            row = random.randint(0, grid_size - 1)
            col = random.randint(0, grid_size - 1)
            direction = random.choice(directions)
            
            if can_place_word(word, row, col, direction):
                place_word(word, row, col, direction)
                placed = True
            
            attempts += 1
    
    # Fill empty cells with random letters
    vowels = 'AEIOU'
    consonants = 'BCDFGLMNPRSTVX'
    
    for i in range(grid_size):
        for j in range(grid_size):
            if grid[i][j] == '':
                # Mix of vowels and consonants
                grid[i][j] = random.choice(vowels if random.random() < 0.4 else consonants)
    
    return grid, word_positions
