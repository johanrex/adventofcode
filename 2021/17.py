#input = 'target area: x=20..30, y=-10..-5' #example
# target_x = (20, 30)
# target_y = (-10, -5)

#input = 'target area: x=153..199, y=-114..-75' #real
target_x = (153, 199)
target_y = (-114, -75)


def step(pos_x, pos_y, vel_x, vel_y):

    pos_x += vel_x
    pos_y += vel_y

    if vel_x > 0:
        vel_x -= 1
    elif vel_x < 0:
        vel_x += 1

    vel_y -= 1

    return (pos_x, pos_y, vel_x, vel_y)


all_highest_y = -1000
sum_hits = 0

for start_vel_x in range(200):
    for start_vel_y in range(-200, 200):

        vel_x = start_vel_x
        vel_y = start_vel_y

        pos_x = 0
        pos_y = 0
        highest_y = -1000

        while True:
            pos_x, pos_y, vel_x, vel_y = step(pos_x, pos_y, vel_x, vel_y)

            if pos_y > highest_y:
                highest_y = pos_y
            if (
                target_x[0] <= pos_x <= target_x[1] and
                target_y[0] <= pos_y <= target_y[1]
            ):
                sum_hits += 1

                if highest_y > all_highest_y:
                    all_highest_y = highest_y
                break
            elif pos_x > target_x[1]:
                break
            elif pos_y < target_y[0]:
                break

print('part 1. highest y:', all_highest_y)
print('part 2:', sum_hits)
