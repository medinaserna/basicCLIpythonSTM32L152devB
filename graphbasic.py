import curses
import time

# Function to draw the HDD status bars
def draw_hdd_status(stdscr, statuses):
    curses.start_color()
    
    # Initialize color pairs
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)  # Red on black
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Green on black
    
    height, width = stdscr.getmaxyx()  # Get terminal size
    stdscr.clear()

    print(f"Terminal size: {height}x{width}")  # Debugging: Print terminal size

    # Rectangle (HDD) parameters
    rect_width = width // 2  # Each HDD bar will take up half the width
    rect_height = 3  # Height of each HDD bar
    start_x = width // 4  # Center the bar horizontally
    start_y = height // 10  # Start drawing from the top (with some padding)

    print(f"Drawing HDDs at x={start_x}, y={start_y}")  # Debugging: Print drawing starting position

    # Draw each HDD status bar
    for i, status in enumerate(statuses):
        # Calculate the position of the current HDD
        y_offset = start_y + i * (rect_height + 1)  # Add some space between the bars

        print(f"Drawing HDD {i+1} at y_offset={y_offset}")  # Debugging: Print HDD drawing position

        # Ensure the rectangle fits within terminal bounds
        if y_offset + rect_height > height or start_x + rect_width > width:
            continue  # Skip this rectangle if it's out of bounds

        # Draw first half (representing "On" or "Off" for the HDD)
        for y in range(rect_height):
            for x in range(rect_width):
                if status[0]:  # First half - Green if "On"
                    stdscr.attron(curses.color_pair(2))  # Green
                else:  # Red if "Off"
                    stdscr.attron(curses.color_pair(1))  # Red
                if y_offset + y < height and start_x + x < width:
                    stdscr.addch(y_offset + y, start_x + x, ' ')
                stdscr.attroff(curses.color_pair(1) | curses.color_pair(2))

        # Draw second half (representing "On" or "Off" for the HDD)
        for y in range(rect_height):
            for x in range(rect_width, width):
                if status[1]:  # Second half - Green if "On"
                    stdscr.attron(curses.color_pair(2))  # Green
                else:  # Red if "Off"
                    stdscr.attron(curses.color_pair(1))  # Red
                if y_offset + y < height and start_x + x < width:
                    stdscr.addch(y_offset + y, start_x + x, ' ')
                stdscr.attroff(curses.color_pair(1) | curses.color_pair(2))

    stdscr.refresh()

# Function to toggle the status of all HDDs
def toggle_status(statuses):
    # Toggle the status for each HDD (both halves)
    for i in range(len(statuses)):
        statuses[i][0] = not statuses[i][0]  # Toggle first half
        statuses[i][1] = not statuses[i][1]  # Toggle second half
    return statuses

# Main function
def main(stdscr):
    # Set up the window to handle resizing
    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(True)  # Make getch() non-blocking
    stdscr.timeout(100)  # Refresh the screen every 100ms

    # Initial status for 5 HDDs (all halves start off)
    statuses = [[False, False] for _ in range(5)]  # 5 HDDs, each half off

    while True:
        # Draw the HDD status bars
        draw_hdd_status(stdscr, statuses)

        # Wait for key press (non-blocking)
        key = stdscr.getch()

        if key == ord('q'):
            break  # Quit the program on 'q'
        elif key == ord('t'):
            statuses = toggle_status(statuses)  # Toggle the status of all HDDs on 't'

        time.sleep(1)  # Update every 1 second

# Start the curses application
if __name__ == '__main__':
    curses.wrapper(main)
