from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time
import numpy as np
x1 =-15
x2 = 15
y1 = -475
y2 = -380
obstacle = []
laser = []
lives = 3
score = 0
misses = 0
state = True
paused = False
desired_fps = 60  # Target FPS
frame_time = 1 / desired_fps  # Time per frame
previous_time = time.time()

def draw_points(x, y, z=1):
    glPointSize(z) #pixel size. by default 1 thake
    glBegin(GL_POINTS)
    glVertex2f(x,y) #jekhane show korbe pixel
    glEnd()

def draw_lines(x,y):

    def midpoint_line_8_way(x0, y0, x1, y1):
        points = []

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1

        def plot_point(x, y):
            points.append((x, y))


        if dx > dy:
            d = 2 * dy - dx
            dE = 2 * dy
            dNE = 2 * (dy - dx)

            x, y = x0, y0
            plot_point(x, y)
            
            while x < x1:
                x += 1
                if d < 0:
                    d += dE
                else:
                    y += 1 * sy
                    d += dNE
                plot_point(x, y)
        else:
            d = 2 * dx - dy
            dN = 2 * dx
            dNE = 2 * (dx - dy)

            x, y = x0, y0
            plot_point(x, y)
            
            while y < y1:
                y += 1
                if d < 0:
                    d += dN
                else:
                    x += 1 * sx
                    d += dNE
                plot_point(x, y)

        return points
    
    points = midpoint_line_8_way(x[0], x[1], y[0], y[1])
    for i in points:
        draw_points(i[0], i[1],3)


def draw_random_texture(x, y):
        """
        Draws random dots inside a 15x15 brick using NumPy for better performance.
        """
        num_dots = np.random.randint(5, 11)  # Random number of dots between 5 and 10
        dot_offsets = np.random.randint([-14, 0], [15, 15], (num_dots, 2))  # Generate offsets
        for offset in dot_offsets:
            draw_points(x + offset[0], y + offset[1])

def draw_bricks(x_start, y_start, y_end, direction=True, row_offset=15):
    """
    Draws two rows of bricks where the second row is offset to create a staggered pattern.
    Each brick is 15x15 in size.
    """
    if direction:
        for y in range(y_start, y_end, 30):  # Increment by 30 to leave space for two rows
        # First row of bricks
            for x in range(x_start, x_start + 90, 30):  # Adjust x to control brick count
                draw_lines((x - 15, y), (x + 15, y))      # Top horizontal line
                draw_lines((x - 15, y + 15), (x + 15, y + 15))  # Bottom horizontal line
                draw_lines((x - 15, y), (x - 15, y + 15))  # Left vertical line
                draw_lines((x + 15, y), (x + 15, y + 15))  # Right vertical line
                draw_random_texture(x, y)  # Add random texture inside the brick

            # Second row of bricks with an offset
            for x in range(x_start + row_offset, x_start + 90 + row_offset, 30):
                draw_lines((x - 15, y + 15), (x + 15, y + 15))  # Top horizontal line
                draw_lines((x - 15, y + 30), (x + 15, y + 30))  # Bottom horizontal line
                draw_lines((x - 15, y + 15), (x - 15, y + 30))  # Left vertical line
                draw_lines((x + 15, y + 15), (x + 15, y + 30))  # Right vertical line
                draw_random_texture(x, y + 15)  # Add random texture inside the brick
    
    else:
       for y in range(y_start, y_end, 30):  # Increment by 30 to leave space for two rows
    # First row of bricks
            for x in range(x_start, x_start - 90, -30):  # Decrement x to extend bricks to the left
                draw_lines((x + 15, y), (x - 15, y))      # Top horizontal line
                draw_lines((x + 15, y + 15), (x - 15, y + 15))  # Bottom horizontal line
                draw_lines((x + 15, y), (x + 15, y + 15))  # Left vertical line
                draw_lines((x - 15, y), (x - 15, y + 15))  # Right vertical line
                draw_random_texture(x, y)  # Add random texture inside the brick

            # Second row of bricks with an offset
            for x in range(x_start + row_offset, x_start - 90 - row_offset, -30):
                draw_lines((x - 15, y + 15), (x + 15, y + 15))  # Top horizontal line
                draw_lines((x - 15, y + 30), (x + 15, y + 30))  # Bottom horizontal line
                draw_lines((x - 15, y + 15), (x - 15, y + 30))  # Left vertical line
                draw_lines((x + 15, y + 15), (x + 15, y + 30))  # Right vertical line
                draw_random_texture(x, y + 15)  # Add random texture inside the brick



def draw_template():
    """
    Draws the rectangular frame (borders) of the Tetris game screen.
    """
    # Vertical borders
    draw_bricks(-369, -480, 301, False)  # Left border
    draw_bricks(359, -480, 301)   # Right border

    # # Horizontal borders
    # # draw_bricks(329, 497, 512)    # Top border
    # # draw_bricks(-369, 497, 512)    # Top border
    draw_bricks(-450, -512, -497)  # Bottom border
    draw_bricks(-90, -512, -497)  # Bottom border
    draw_bricks(-180, -512, -497)  # Bottom border
    draw_bricks(-270, -512, -497)  # Bottom border
    draw_bricks(-360, -512, -497)  # Bottom border
    
    draw_bricks(0, -512, -497)  # Bottom border
    draw_bricks(90, -512, -497)  # Bottom border
    draw_bricks(180, -512, -497)  # Bottom border
    draw_bricks(270, -512, -497)  # Bottom border
    draw_bricks(360, -512, -497)  # Bottom border


    draw_bricks(-450, 497, 512)  # Bottom border
    draw_bricks(-90,  497, 512)  # Bottom border
    draw_bricks(-180,  497, 512)  # Bottom border
    draw_bricks(-270,  497, 512)  # Bottom border
    draw_bricks(-360,  497, 512)  # Bottom border
    
    draw_bricks(0,  497, 512)  # Bottom border
    draw_bricks(90,  497, 512)  # Bottom border
    draw_bricks(180,  497, 512)  # Bottom border
    draw_bricks(270,  497, 512)  # Bottom border
    draw_bricks(360,  497, 512)  # Bottom border


    # draw_bricks(0, 327,  361)  # Bottom border
    draw_bricks(90, 331,  361)  # Bottom border
    draw_bricks(180, 331,  361)  # Bottom border
    draw_bricks(270, 331,  361)  # Bottom border
    draw_bricks(360, 331, 361)  # Bottom border 

    draw_bricks(-360, 331,  361)  # Bottom border
    draw_bricks(-180, 331,  361)  # Bottom border
    draw_bricks(-270, 331,  361)  # Bottom border   
    draw_bricks(-450, 331, 361)  # Bottom border 

    



def iterate():
    """
    Sets up the viewport and projection for rendering the game screen.
    """
    glViewport(0, 0, 768, 1024)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-384, 384, -512, 512, -1, 1)  # Adjusted glOrtho as per frame needs
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()




def draw_controls():
    glColor3f(94/255, 119/255, 138/255)
    y = 480
    x = -300
    x1 = -300 + 20
    draw_lines((x,y-10),(x1,y))
    draw_lines((x1,y-20),(x1,y))
    draw_lines((x,y-10),(x1,y-20))

    glColor3f(0, 1, 0)
    draw_lines((-5,y-20),(-5,y))
    draw_lines((5,y-20),(5,y))

    glColor3f(1, 0, 0)
    draw_lines((-x,y-20),(-x1,y))
    draw_lines((-x1,y-20),(-x,y))


def display_text(x, y, text, font):

    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))


def show_game_over_screen():
    """
    Display the Game Over screen with the final score.
    """
    global score,misses, lives
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(-320, 320, -240, 240, -1, 1)  # Set orthographic projection for overlay
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glColor3f(1, 1, 1)  # Set text color to white

    # Display "Game Over"
    display_text(-100, 50, "GAME OVER", GLUT_BITMAP_TIMES_ROMAN_24)

    # Display the score
    display_text(-100, -50, f"Your Score: {score}", GLUT_BITMAP_TIMES_ROMAN_24)
    display_text(-100, -75, f"Your Misses: {misses}", GLUT_BITMAP_TIMES_ROMAN_24)
    display_text(-100, -100, f"Your Lives: {lives}", GLUT_BITMAP_TIMES_ROMAN_24)

    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()
    glutSwapBuffers()



def draw_square(radius, x_center, y_center):
    x1= x_center - radius
    x2= x_center + radius
    y1= y_center - radius
    y2= y_center + radius
    # global score
    glColor3f(176/255, 190/255, 197/255)
    draw_lines((x1,y1),(x1,y2))
    draw_lines((x2,y1),(x2,y2))
    draw_lines((x1,y1),(x2,y1))
    draw_lines((x1,y2),(x2,y2))
    


def draw_circle(x_center=0,y_center=400,x=15):

    global previous_time
    start_time = time.time()
    glColor3f(176/255, 190/255, 197/255)
    def midpoint_circle(radius, x_center, y_center):
        x = 0
        y = radius
        d = 1 - radius
        points = []

        def plot_circle_points(x_center, y_center, x, y):
            points.extend([
                (x_center + x, y_center + y),
                (x_center - x, y_center + y),
                (x_center + x, y_center - y),
                (x_center - x, y_center - y),
                (x_center + y, y_center + x),
                (x_center - y, y_center + x),
                (x_center + y, y_center - x),
                (x_center - y, y_center - x)
            ])

        plot_circle_points(x_center, y_center, x, y)
        while x < y:
            x += 1
            if d < 0:
                d += 2 * x + 1
            else:
                y -= 1
                d += 2 * (x - y) + 1
            plot_circle_points(x_center, y_center, x, y)

        return points

    global obstacle
    global laser
    global score
    global lives
    global state

    # Create a new circle at the top if no circles or if the last circle has passed midpoint
    # if not obstacle or all(circle[1] <= 0 for circle in obstacle):
    #     x_center = random.choice(range(-320, 320, 50))
    #     y_center = 400
    #     radius = x-2
    #     obstacle.append([x_center, y_center, radius])
    radius = x
    # for circle in obstacle[:]:  # Iterate over a copy to allow safe removal
    #     x_center, y_center, radius = circle
    #     y_center -= max((score//50),2)  # Move the circle downward
    #     circle[1] = y_center  # Update the y-coordinate

    #     # Remove the circle if it has reached the bottom of the screen
    #     if y_center <= -512:
    #         obstacle.remove(circle)
    #         lives -= 1
    #         if lives <= 0:
    #             state = False
    #             draw_controls()
    #             show_game_over_screen()
    #         continue
        # for laser_line in laser:
        #     if line_circle_collision([laser_line[0], laser_line[1], laser_line[0], laser_line[1] + 10], [x_center, y_center, radius]):
        #         score += radius
        #         obstacle.remove(circle)
        #         laser.remove(laser_line)
        # Draw the circle using midpoint algorithm
    points = midpoint_circle(radius-2, x_center, y_center)
    for point in points:
        draw_points(point[0], point[1],3)
    draw_square(radius, x_center, y_center)

    elapsed_time = time.time() - start_time
    remaining_time = frame_time - elapsed_time
    if remaining_time > 0:
        time.sleep(remaining_time)


def box(x_center=0,y_center=400,x=15):
    draw_circle(x_center,y_center,x)


class Tetromino():
    def __init__(self):

        self.tetromino = np.array([
            [[2, 399], [2, 367], [2, 335], [2, 303]],
            [[2, 399], [2, 367], [2, 335], [34, 335]],
            [[-30, 335], [2, 367], [2, 335], [34, 335]],
            [[-30, 367], [2, 367], [-30, 335], [2, 335]]
        ])

        self.tetromino = self.tetromino[np.random.randint(0, self.tetromino.shape[0])]

    def draw(self):
        for i in self.tetromino:
            box(i[0],i[1])

    def descend(self):
        for i in self.tetromino:
            i[1]-=32

    def translate(self,key):
        temp = True
        if key.lower() == 'a':
            for i in self.tetromino:
                if i[0] <= -318:
                    temp = False
                    break
            if temp:
                self.tetromino = [[(i[0]-32),i[1]] for i in self.tetromino]
        elif key.lower() == 'd':
            for i in self.tetromino:
                if i[0] >= 322:
                    temp = False
                    break
            if temp:
                self.tetromino = [[(i[0]+32),i[1]] for i in self.tetromino]
        else:
            # self.tetromino = [[min((i[0]+32),322),i[1]] for i in self.tetromino]
            pass
    
    def rotate(self):
        """Rotate the tetromino continuously by 90° clockwise around its center."""
        # Ensure tetromino is a NumPy array
        self.tetromino = np.array(self.tetromino)

        # The center of rotation is the third block of the tetromino
        center = np.array(self.tetromino[2])

        # Define the 90° clockwise rotation matrix
        rotation_matrix = np.array([[0, -1], [1, 0]])

        # Translate tetromino to origin (center), apply rotation, and translate back
        translated = self.tetromino - center
        rotated = np.dot(translated, rotation_matrix.T)
        self.tetromino = (rotated + center).astype(int)


    def fall(self,x):
        d = min([(i[1]-x[(i[0]//32)]) for i in self.tetromino ])
        for i in self.tetromino:
            i[1] -= d





class Tetris():                       
    def __init__(self):
        self.matrix = np.full((24,21),None)  
        self.horizon = np.full(43,-465)          # 43 column
        self.state = True
        # for i in range(21):
        #     for j in range(24):
        #         self.matrix[j][i] = ((-318 + (32*i)),(-465 + (32*j)))
    def draw(self):
        for i in self.matrix:
            for j in i:
                if j is None or (np.array_equal(j, np.array(None))):  
                    continue
                box(j[0], j[1])



    def check(self):
        for i in self.tetro.tetromino:
            if self.horizon[i[0]//32] >= i[1]:
                self.state = True
        if self.state == True:
            for i in self.tetro.tetromino:
                if self.horizon[i[0]//32] < i[1]:
                    self.horizon[i[0]//32] = i[1]+32
                    print(self.horizon[i[0]//32])
                self.matrix[i[1]//32][i[0]//32] = [(i[0]-1//32),(i[1]-1//32)]

    def point(self):
        global point
        c = 0
        for i in range(len(self.matrix)):
            if None in self.matrix[i]:
                self.matrix[i] = [[self.matrix[i][j][0],(self.matrix[i][j][1] - (c * 32))] if self.matrix[i][j] is not None else None for j in range(len(self.matrix[i]))]

                continue
            else:
                self.matrix[i] = [None for i in self.matrix[i]]
                c +=1

                
        np.roll(self.matrix, shift=c, axis=0)
        self.horizon = [i-(c*32) for i in self.horizon]
        point += c*10
                

                

    def play(self):
        if self.state == True:
            self.tetro = Tetromino()
            self.state = False
        
        # for i in tetro.tetromino:
        #     if i[1]
        self.tetro.draw()
        self.point()
        self.check()
        self.tetro.descend()
        
        self.draw()




game = Tetris()

tetro = Tetromino()

# for i in tetro.tetromino:
#     if i[1]



def mouseListener(button, con, x, y):	#/#/x, y is the x-y of the screen (2D)
    global state, paused, obstacle, laser, score, lives, misses
    if button==GLUT_LEFT_BUTTON:
        if(con == GLUT_DOWN): 
 # 		// 2 times?? in ONE click? -- solution is checking DOWN or UP
            c_X, c_y = x - 384, 512 - y
            if (-310 <= c_X <= -270 ) & ( 450 <= c_y <= 470) :
                obstacle = []  # Clear all circles
                laser = []     # Clear all lasers
                score = 0      # Reset the score
                state = False  # Reset game-over state
                paused = False
                lives = 3
                misses = 0 
                state = True
            
            if (-15 <= c_X <= 15 ) & ( 450 <= c_y <= 470) :
                if paused:
                    paused = False
                else:
                    paused = True

            if (270 <= c_X <= 310) & ( 450 <= c_y <= 470) :
                state = False
                draw_controls()
                show_game_over_screen()
        pass




def keyboardListener(key, x, y):

    # global x1
    # global x2
    # global score
    if key==b'a':
        game.tetro.translate('a')
        
    if key==b'd':
        game.tetro.translate('d')
    if key==b'w':
        game.tetro.rotate()

    if key==b's':
        game.tetro.fall(game.horizon)
    


    glutPostRedisplay()
def animate():
    glutPostRedisplay()  

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    glColor3f(1.0, 1.0, 0.0) #konokichur color set (RGB)
    #call the draw methods here
    global state
    global paused
    
    if state:
        if paused:
            # Show "Paused" overlay when the game is paused
            glMatrixMode(GL_PROJECTION)
            glPushMatrix()
            glLoadIdentity()
            glOrtho(-320, 320, -240, 240, -1, 1)
            glMatrixMode(GL_MODELVIEW)
            glPushMatrix()
            glLoadIdentity()

            glColor3f(1, 1, 1)  # White text
            display_text(-50, 0, "PAUSED", GLUT_BITMAP_TIMES_ROMAN_24)
            display_text(-100, -50, f"Your Score: {score}", GLUT_BITMAP_TIMES_ROMAN_24)
            display_text(-100, -75, f"Your Misses: {misses}", GLUT_BITMAP_TIMES_ROMAN_24)
            display_text(-100, -100, f"Your Lives: {lives}", GLUT_BITMAP_TIMES_ROMAN_24)

            glMatrixMode(GL_PROJECTION)
            glPopMatrix()
            glMatrixMode(GL_MODELVIEW)
            glPopMatrix()
        else: 
            draw_template()
            game.play()
            # box(x_center=-320,y_center=300,x=15)
            # box(x_center=+324,y_center=300,x=15)

            # box(x_center=-320,y_center=-465,x=15)
            # box(x_center=+324,y_center=-465,x=15)
            # for i in range(-318,325,32):
            #     for j in range(-465,300,32):
            #         box(x_center=i,y_center=j,x=15)

            for i in range(-318,325,32):                # grid
                draw_lines((i,-465),(i,300))
            for j in range(-465,300,32):
                draw_lines((-318,j),(325,j))

            # tetro.draw()
            # tetro.descend()

            # draw_lines((-320-16,-465-16),(324+16,-465-16))
            # draw_lines((-320-16,-465-16),(-320-16,300+16))
            # draw_lines((324+16,-465-16),(324+16,300+16))


        draw_controls()
    else:
        draw_controls()
        show_game_over_screen()
    glutSwapBuffers()



glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(768, 1024) #window size 768×1024
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"Tetris") #window name
glutDisplayFunc(showScreen)
glutIdleFunc(animate) 
glutKeyboardFunc(keyboardListener)
glutMouseFunc(mouseListener)
glutMainLoop() 
