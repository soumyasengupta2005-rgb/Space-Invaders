import turtle, random, math, time, os

screen = turtle.Screen()
screen.setup(800, 600)
screen.bgcolor("black")
screen.title("Space Invaders")
screen.tracer(0)

score = 0
lives = 3
level = 1

if not os.path.exists("highscore.txt"):
    with open("highscore.txt", "w") as f:
        f.write("0")
with open("highscore.txt", "r") as f:
    high_score = int(f.read().strip())

pen = turtle.Turtle()
pen.hideturtle()
pen.color("white")
pen.penup()
pen.goto(-380, 260)

controls_pen = turtle.Turtle()
controls_pen.hideturtle()
controls_pen.color("gray")
controls_pen.penup()
controls_pen.goto(-380, 230)
controls_pen.write("Controls: ←/A = Left   →/D = Right   SPACE = Fire",
                   font=("Courier", 12, "normal"))

def draw_stars(num_stars=50):
    star = turtle.Turtle()
    star.hideturtle()
    star.penup()
    star.speed(0)
    colors = ["white", "red", "yellow", "lightblue"]

    for _ in range(num_stars):
        star.goto(random.randint(-390, 390), random.randint(-290, 290))
        star.dot(random.randint(2, 4), random.choice(colors))
def create_enemies(rows, cols, speed):
    enemies.clear()
    for r in range(rows):
        for c in range(cols):
            e = turtle.Turtle()
            e.shape("square")
            e.shapesize(stretch_wid=1, stretch_len=2)
            e.color(random.choice(["red", "orange", "yellow", "green", "white"]))
            e.penup()
            x = enemy_start_x + c * enemy_h_gap
            y = enemy_start_y - r * enemy_v_gap
            e.goto(x, y)
            e.dx = speed
            enemies.append(e)

def draw_hud():
    pen.clear()
    pen.write(f"Score: {score}    Lives: {lives}    Level: {level}    High Score: {high_score}",
              font=("Courier", 14, "normal"))
draw_stars()
player = turtle.Turtle()
player.shape("triangle")
player.color("cyan")
player.penup()
player.speed(0)
player.goto(0, -230)
player.setheading(90)
player_speed = 20

enemies = []
enemy_rows = 4
enemy_cols = 8
enemy_start_x = -300
enemy_start_y = 200
enemy_h_gap = 70
enemy_v_gap = 45
enemy_speed = 2


bullet = turtle.Turtle()
bullet.shape("square")
bullet.color("white")
bullet.shapesize(stretch_wid=0.2, stretch_len=0.8)
bullet.penup()
bullet.hideturtle()
bullet.speed(0)
bullet_state = "ready"
bullet_speed = 20

enemy_bullets = []
enemy_bullet_speed = 6

def move_left():
    x = player.xcor() - player_speed
    if x < -380: x = -380
    player.setx(x)

def move_right():
    x = player.xcor() + player_speed
    if x > 380: x = 380
    player.setx(x)

def fire_bullet():
    global bullet_state
    if bullet_state == "ready":
        bullet_state = "fire"
        bullet.showturtle()
        bullet.goto(player.xcor(), player.ycor() + 20)

def fire_enemy_bullet(x, y):
    b = turtle.Turtle()
    b.shape("circle")
    b.color("white")
    b.shapesize(stretch_wid=0.4, stretch_len=0.4)
    b.penup()
    b.speed(0)
    b.goto(x, y - 15)
    enemy_bullets.append(b)

screen.listen()
screen.onkeypress(move_left, "Left")
screen.onkeypress(move_right, "Right")
screen.onkeypress(move_left, "a")
screen.onkeypress(move_right, "d")
screen.onkey(fire_bullet, "space")

def is_collision(t1, t2, threshold=20):
    return math.hypot(t1.xcor() - t2.xcor(), t1.ycor() - t2.ycor()) < threshold

def clear_enemies_and_bullets():
    for e in enemies[:]:
        e.hideturtle()
        enemies.remove(e)
    for b in enemy_bullets[:]:
        b.hideturtle()
        enemy_bullets.remove(b)
    bullet.hideturtle()
    global bullet_state
    bullet_state = "ready"

def reset_level():
    clear_enemies_and_bullets()
    create_enemies(enemy_rows, enemy_cols, enemy_speed)
    player.goto(0, -230)

def show_game_over():
    # Properly reset the screen before drawing
    screen.clearscreen()
    screen.bgcolor("black")

    # Recreate turtles after clearscreen (old ones are wiped)
    over = turtle.Turtle()
    over.hideturtle()
    over.color("red")
    over.penup()
    over.goto(0, 40)
    over.write("GAME OVER", align="center", font=("Courier", 40, "bold"))

    score_turtle = turtle.Turtle()
    score_turtle.hideturtle()
    score_turtle.color("white")
    score_turtle.penup()
    score_turtle.goto(0, -40)
    score_turtle.write(f"Your Score: {score}\nHigh Score: {high_score}",
                       align="center", font=("Courier", 20, "normal"))

    time.sleep(5)
    turtle.bye()


create_enemies(enemy_rows, enemy_cols, enemy_speed)
draw_hud()
game_over = False
last_enemy_shot = time.time()

while True:
    screen.update()
    if game_over:
        time.sleep(0.1)
        continue

    if bullet_state == "fire":
        bullet.sety(bullet.ycor() + bullet_speed)
        if bullet.ycor() > 300:
            bullet.hideturtle()
            bullet_state = "ready"

    edge_hit = False
    for e in enemies:
        e.setx(e.xcor() + e.dx)
        if e.xcor() > 360 or e.xcor() < -360:
            edge_hit = True
    if edge_hit:
        for e in enemies:
            e.sety(e.ycor() - 15)
            e.dx *= -1

    for e in enemies[:]:
        if bullet_state == "fire" and is_collision(bullet, e, 25):
            bullet.hideturtle()
            bullet_state = "ready"
            e.hideturtle()
            enemies.remove(e)
            score += 10
            if score > high_score:
                high_score = score
                with open("highscore.txt", "w") as f:
                    f.write(str(high_score))
            draw_hud()
        if is_collision(player, e, 25) or e.ycor() < -220:
            lives -= 1
            draw_hud()
            if lives <= 0:
                game_over = True
                show_game_over()
            else:
                reset_level()
            break

    if enemies and time.time() - last_enemy_shot > max(0.4, 2.5 - level * 0.2):
        shooter = random.choice(enemies)
        fire_enemy_bullet(shooter.xcor(), shooter.ycor())
        last_enemy_shot = time.time()

    for eb in enemy_bullets[:]:
        eb.sety(eb.ycor() - enemy_bullet_speed)
        if eb.ycor() < -300:
            eb.hideturtle()
            enemy_bullets.remove(eb)
            continue
        if is_collision(eb, player, 15):
            eb.hideturtle()
            enemy_bullets.remove(eb)
            lives -= 1
            draw_hud()
            if lives <= 0:
                game_over = True
                show_game_over()
            else:
                reset_level()
            break

    if not enemies:
        level += 1
        enemy_speed += 0.6
        enemy_rows = min(6, enemy_rows + 1)
        enemy_cols = min(10, enemy_cols + 1)
        reset_level()
        draw_hud()

    time.sleep(1 / 60)
