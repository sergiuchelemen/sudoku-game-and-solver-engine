from tkinter import *
import random
import easy
import medium
import hard

# root settings
root = Tk()
root.state('zoomed')
root.resizable(False, False)
root.title('Sudoku')

inputValues = []
row = [0]
column = [0]
option = 'easy'
seconds, minutes, hours = 0, 0, 0
running = False

grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]]

# frame
frame = LabelFrame(root, padx=200, pady=130, height=15, borderwidth=0)
frame.pack(ipadx=220)
message = Label(frame)


def update():
    global seconds, minutes, hours, update_time
    seconds += 1
    if seconds == 60:
        minutes += 1
        seconds = 0
    if minutes == 60:
        hours += 1
        minutes = 0
    if hours > 9:
        hours_string = f'{hours}'
    else:
        hours_string = f'0{hours}'
    if minutes > 9:
        minutes_string = f'{minutes}'
    else:
        minutes_string = f'0{minutes}'
    if seconds > 9:
        seconds_string = f'{seconds}'
    else:
        seconds_string = f'0{seconds}'
    stopwatch.config(text=hours_string + ':' + minutes_string + ':' + seconds_string)
    update_time = stopwatch.after(1000, update)


def start_stopwatch():
    global running
    if not running:
        update()
        running = True


def reset_stopwatch():
    global running
    if running:
        stopwatch.after_cancel(update_time)
        running = False
    global hours, minutes, seconds
    hours, minutes, seconds = 0, 0, 0
    stopwatch.config(text='00:00:00')


def valid_for_solve(value, row_number, col_number):
    counter_row = 0
    counter_col = 0
    counter_box = 0
    for cols in range(9):
        if value == grid[row_number][cols]:
            counter_row += 1
    for rows in range(9):
        if value == grid[rows][col_number]:
            counter_col += 1
    for rows in range(3):
        for cols in range(0, 3):
            if value == grid[rows + row_number - row_number % 3][cols + col_number - col_number % 3]:
                counter_box += 1
    if counter_row > 1 or counter_box > 1 or counter_col > 1:
        return False
    return True


def check_grid():
    for rows in range(9):
        for cols in range(9):
            if grid[rows][cols] == 0:
                continue
            elif valid_for_solve(grid[rows][cols], rows, cols) is False:
                return False
    return True


def validRow(row, num):
    for cols in range(9):
        if grid[row][cols] == num:
            return False
    return True


def validCol(col, num):
    for rows in range(9):
        if grid[rows][col] == num:
            return False
    return True


def validSquare(row, col, num):
    for rows in range(3):
        for cols in range(3):
            if grid[rows + row][cols + col] == num:
                return False
    return True


def valid(num, row, col):
    if validRow(row[0], num) is True and validCol(col[0], num) is True and validSquare(row[0] - row[0] % 3, col[0] - col[0] % 3, num) is True:
        return True
    return False


def findEmptySpace(row, column):
    for rows in range(9):
        for col in range(9):
            if grid[rows][col] == 0:
                row[0] = rows
                column[0] = col
                return True
    return False


def solveSudoku():
    row = [0]
    column = [0]
    if findEmptySpace(row, column) is False:
        return True
    for num in range(1, 10):
        if valid(num, row, column) is True:
            grid[row[0]][column[0]] = num
            if solveSudoku():
                return True
            grid[row[0]][column[0]] = 0
    return False


def solve():
    x = 0
    message.grid_forget()
    for row in range(9):
        for col in range(9):
            if not inputValues[x].get():
                grid[row][col] = 0
            else:
                grid[row][col] = int(inputValues[x].get())
            x += 1
    if check_grid() is True:
        if solveSudoku() is True:
            x = 0
            for square in range(81):
                inputValues[square].delete(0, END)
            for row in range(9):
                for col in range(9):
                    inputValues[x].insert(0, str(grid[row][col]))
                    x += 1
            message.config(text="Sudoku solved!", font=('cascadia code', 30), fg='green')
            message.grid(row=7, column=41)
        else:
            message.config(text="No solution", font=('cascadia code', 30), fg='red')
            message.grid(row=7, column=41)
    else:
        message.config(text="No solution", font=('cascadia code', 30), fg='red')
        message.grid(row=7, column=41)


def check():
    incomplete = 0
    wrong = 0
    x = 0
    for rows in range(9):
        for cols in range(9):
            if not inputValues[x].get():
                grid[rows][cols] = 0
            else:
                grid[rows][cols] = int(inputValues[x].get())
            x += 1
    for rows in range(9):
        for cols in range(9):
            if grid[rows][cols] == 0:
                incomplete = 1
    for rows in range(9):
        for cols in range(9):
            if valid_for_solve(grid[rows][cols], rows, cols) is False:
                wrong = 1
    if wrong == 0 and incomplete == 0:
        message.config(text="Sudoku solved in " + stopwatch.cget('text'), font=('cascadia code', 30), fg='green')
        message.grid(row=7, column=40, columnspan=6)
        reset_stopwatch()
    if incomplete == 1:
        message.config(text="Incomplete sudoku", font=('cascadia code', 30), fg='red')
        message.grid(row=7, column=41)
    elif wrong == 1:
        message.config(text="Wrong solution", font=('cascadia code', 30), fg='red')
        message.grid(row=7, column=41)


def levelOne():
    global option
    easyButton.config(background='gold')
    mediumButton.config(background='cornflower blue')
    hardButton.config(background='cornflower blue')
    option = 'easy'


def levelTwo():
    global option
    mediumButton.config(background='gold')
    easyButton.config(background='cornflower blue')
    hardButton.config(background='cornflower blue')
    option = 'medium'


def levelThree():
    global option
    hardButton.config(background='gold')
    easyButton.config(background='cornflower blue')
    mediumButton.config(background='cornflower blue')
    option = 'hard'


def rand():
    x = 0
    message.grid_forget()
    reset_stopwatch()
    start_stopwatch()
    if option == 'easy':
        a = random.choice(easy.M)
    elif option == 'medium':
        a = random.choice(medium.M)
    else:
        a = random.choice(hard.M)
    for square in range(81):
        inputValues[square].delete(0, END)
    for row in range(9):
        for col in range(9):
            if a[row][col] != 0:
                inputValues[x].insert(0, str(a[row][col]))
            x += 1


# characters limit for the entries
def validate(P):
    if len(P) == 0:
        return True
    elif len(P) == 1 and P.isdigit() and int(P) != 0:
        return True
    else:
        return False


validateCommand = (root.register(validate), '%P')


# generate the entry boxes
color = 'SkyBlue1'
for i in range(9):
    if 0 <= i <= 2:
        color = 'SkyBlue1'
    elif 3 <= i <= 5:
        color = 'SkyBlue3'
    else:
        color = 'SkyBlue1'
    for j in range(9):
        if j % 3 == 0:
            if color == 'SkyBlue1':
                color = 'SkyBlue3'
            else:
                color = 'SkyBlue1'
        entry = Entry(frame, width=2, borderwidth=3, justify=CENTER, background=color, font=("Cascadia Code", 45),
                      validate='key',
                      validatecommand=validateCommand)
        entry.grid(row=i, column=j, ipadx=5)
        inputValues.append(entry)


# spaces between the sudoku grid and buttons
for i in range(9):
    for j in range(10, 40):
        space = Label(frame)
        space.grid(row=i, column=j)


# buttons and text
text = Label(frame, text='Select your difficulty:', font=('cascadia code', 23))
text.grid(row=0, column=41)

randomButton = Button(frame, text='Random grid', font=('cascadia code', 25), background='cornflower blue',
                      command=rand)
randomButton.grid(row=3, column=41)

text = Label(frame, text='')
text.grid(row=4, column=41)

solveButton = Button(frame, text='Solve sudoku', font=('cascadia code', 25), background='cornflower blue', width=12,
                     command=solve)
solveButton.grid(row=4, column=41)

text = Label(frame, text='')
text.grid(row=6, column=41)

solveButton = Button(frame, text='Check', font=('cascadia code', 25), background='cornflower blue', width=12,
                     command=check)
solveButton.grid(row=5, column=41)

easyButton = Button(frame, text='Easy', font=('cascadia code', 15), width=10, background='gold',
                    command=levelOne)
easyButton.grid(row=1, column=40)

mediumButton = Button(frame, text='Medium', font=('cascadia code', 15), background='cornflower blue', width=10,
                      command=levelTwo)
mediumButton.grid(row=1, column=41)

hardButton = Button(frame, text='Hard', font=('cascadia code', 15), width=10, background='cornflower blue',
                    command=levelThree)
hardButton.grid(row=1, column=43)

stopwatch = Label(frame, text='00:00:00', font=('cascadia code', 35))
stopwatch.grid(row=8, column=41)

# run the window
root.mainloop()
