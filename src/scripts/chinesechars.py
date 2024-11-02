import random
import curses
import time

# Define a set of 1000 common Chinese characters
chinese_characters = [
    chr(i)
    for i in range(0x4E00, 0x4E00 + 1000)  # A range in the CJK Unified Ideographs block
]


def generate_random_chinese_pattern(width, height):
    # Generate a grid of random Chinese characters from the distribution
    pattern = [
        [random.choice(chinese_characters) for _ in range(width)] for _ in range(height)
    ]
    return pattern


def update_chinese_pattern(pattern, change_rate=0.1):
    height = len(pattern)
    width = len(pattern[0])

    # Determine the number of cells to change based on change_rate
    num_changes = int(change_rate * width * height)
    for _ in range(num_changes):
        # Pick a random cell to change
        row = random.randint(0, height - 1)
        col = random.randint(0, width - 1)
        pattern[row][col] = random.choice(chinese_characters)


def curses_main(stdscr):
    # Clear screen and disable cursor
    stdscr.clear()
    curses.curs_set(0)

    # Get initial terminal size
    max_height, max_width = stdscr.getmaxyx()
    height, width = (
        max_height,
        max_width // 2,
    )  # Chinese characters occupy about two terminal columns in width
    chinese_pattern = generate_random_chinese_pattern(width, height)

    try:
        while True:
            # Check terminal size each iteration
            new_height, new_width = stdscr.getmaxyx()
            new_height -= 1  # Reserve a row to avoid overflow
            new_width //= 2  # Adjust width for double-width characters

            # If the terminal was resized, regenerate the pattern
            if new_height != height or new_width != width:
                height, width = new_height, new_width
                chinese_pattern = generate_random_chinese_pattern(width, height)

            # Update a portion of the pattern
            update_chinese_pattern(chinese_pattern, change_rate=0.1)

            # Display pattern on screen
            for y, row in enumerate(chinese_pattern):
                if y < height:  # Ensure we don't exceed the current height
                    stdscr.addstr(
                        y, 0, "".join(row)
                    )  # Each row is exactly `width` characters wide

            # Refresh the screen to show updates
            stdscr.refresh()

            # 100 ms delay
            time.sleep(0.1)

    except KeyboardInterrupt:
        # Clear screen and reset cursor visibility before exiting
        curses.curs_set(1)
        stdscr.clear()
        stdscr.refresh()
        print("Animation stopped.")


try:
    curses.wrapper(curses_main)
except KeyboardInterrupt:
    print("Animation stopped.")
