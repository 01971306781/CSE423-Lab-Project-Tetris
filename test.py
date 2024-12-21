from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math
import time
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
            # points.append((x, -y))  # Reflect over the x-axis
            # points.append((-x, y))  # Reflect over the y-axis
            # points.append((-x, -y)) # Reflect over both axes

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





def iterate():
    glViewport(0, 0, 768, 1024)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-384, 384, -512, 512, 0, 1)
    glMatrixMode (GL_MODELVIEW)
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
        self.tetromino = [[0,400],[0,366],[0,332],[0,298]]

    def draw(self):
        for i in self.tetromino:
            box(i[0],i[1])

    def descend(self):
        for i in self.tetromino:
            i[1]-=5


tetro = Tetromino()

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
    # if key==b'a':
    #     x1 -= 15
    #     x2 -= 15
    #     if x2 <= -384:
    #         x2 = 384
    #         x1 = x2 - 30
        
    # if key==b'd':
    #     x1 += 15 + (score/5)
    #     x2 += 15 + (score/5)
    #     if x1 >= 384:
    #         x1 = -384
    #         x2 = x1 + 30
    # if key==b' ':
    #     draw_laser((x1+x2)/2)
    pass


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
            # draw_ship()
            # draw_circle()
            tetro.draw()
            tetro.descend()
            # draw_laser()
        draw_controls()
    else:
        draw_controls()
        show_game_over_screen()
    glutSwapBuffers()



glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(768, 1024) #window size 768×1024
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"OpenGL Coding Practice") #window name
glutDisplayFunc(showScreen)
glutIdleFunc(animate) 
# glutKeyboardFunc(keyboardListener)
glutMouseFunc(mouseListener)
glutMainLoop() 