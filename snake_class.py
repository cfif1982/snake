import random
import numpy as np

game_width=200 # width of the playing field in pixels
game_height=200 # Height of the playing field in pixels
snake_item=10 # width of the Snake cell (cell) in pixels 
apple_item=10 # Height of the Snake cell (s) in pixels
virtual_game_width = game_width // snake_item # Width of the playing field in conventional units (In cells)
virtual_game_height = game_height // snake_item # Height of the playing field in conventional units (In cells)

# colors of the body and head cells of the snake and Apple
snake_body_color = "blue"
snake_head_color = "red"
snake_frame_color = "yellow"
apple_color1 = "black"
apple_color2 = "yellow"

# snake class snake
class snake:
    def __init__(self, canvas):
        self.canvas=canvas
        self.items_list=[] # list for storing the coordinates of the snake body
        # list for storing distances from the snake's head to obstacles
        # obstacles are searched to the right, forward, and left of the snake's head
        self.lines_list=[]
        # initial coordinates of the snake's head in virtual coordinates
        self.x=10
        self.y=10
        # initial direction of movement of the snake along the axes
        self.x_nav=1 # 1 - right, -1-left, 0 - the position does not change on this axis
        self.y_nav=0 # 1 - down, -1-up, 0 - the position does not change on this axis
        self.items_count = 3 # body length of the snake
        # coordinates of the Apple relative to the snake's head
        # (the code and the circles from which it is drawn)
        self.apple = []
        self.SetNewApple() # calling the Apple creation functions
        self.apple_count = 0 # current number of apples  eaten
    
    # reset the game
    def reset(self):
        # initial coordinates of the snake's head in virtual coordinates
        self.x=10
        self.y=10
        self.x_nav=1 # 1 - right, -1-left, 0 - the position does not change on this axis
        self.y_nav=0 # 1 - down, -1-up, 0 - the position does not change on this axis
        self.items_count = 3 # body length of the snake
        self.apple_count = 0 # current number of apples eaten
        # deleting all old cells of the snake's body
        while len(self.items_list)>0:
            deleted_item = self.items_list.pop(0) # deleting the snake body from the array
            self.canvas.delete(deleted_item[2]) # erase from canvas
            self.canvas.delete(deleted_item[3])

        self.paint_item() # draw the snake cell in the initial position

        self.SetNewApple() # calling the Apple creation functions

        # returning an overview of the environment:
        # coordinates of the Apple, the distance along the axes to the obstacles from the snake's head
        return self.get_environment()

    # Installing a new Apple
    def SetNewApple(self):
        # delete the old Apple
        if len(self.apple):
            self.canvas.delete(self.apple[2])
            self.canvas.delete(self.apple[3])
        # check that the current position of the Apple does not overlap
        # on the snake's body
        check_snake_item=True # check flag
        x=0
        y=0
        while check_snake_item:
            # generated coordinates of an Apple
            x = random.randrange(game_width/snake_item)
            y = random.randrange(game_height/snake_item)
            # check whether the Apple is on the snake's body or not
            check_snake_item = False
            for item in self.items_list:
                if x == item[0] and y == item[1]: 
                    check_snake_item = True
                    break

        # draw an Apple (2 circles)
        id1 = self.canvas.create_oval(x*apple_item, y*apple_item, x*apple_item+apple_item, y*apple_item+apple_item, fill=apple_color1)
        id2 = self.canvas.create_oval(x*apple_item+2, y*apple_item+2, x*apple_item+apple_item-2, y*apple_item+apple_item-2, fill=apple_color2)

        # remember the coordinates of the Apple ID and the circles from which it is drawn (for later deletion)
        self.apple = [x,y,id1,id2]

    # draw a snake cell
    def paint_item(self):
        # if the snake is drawn, then
        # take the last element of the snake - this is the head
        if(len(self.items_list)>0): 
            last_item = self.items_list[len(self.items_list)-1]
            # need to remove the head and re-paint in its place of cell in the body of a snake
            self.canvas.delete(last_item[3]) # delete the old head
            # draw a body cell in place of the old head
            temp_id = self.canvas.create_rectangle(last_item[0]*snake_item+2, last_item[1]*snake_item+2, last_item[0]*snake_item+snake_item-2, last_item[1]*snake_item+snake_item-2, fill=snake_body_color)
            # correcting the data in the snake body array to new ones
            last_item[3] = temp_id
        # draw the head at the current coordinates
        id1 = self.canvas.create_rectangle(self.x*snake_item, self.y*snake_item, self.x*snake_item+snake_item, self.y*snake_item+snake_item, fill=snake_frame_color)
        id2 = self.canvas.create_rectangle(self.x*snake_item+2, self.y*snake_item+2, self.x*snake_item+snake_item-2, self.y*snake_item+snake_item-2, fill=snake_head_color)
        # adding the snake's head to the array of cells (coordinates of the ID and rectangles it is drawn from)
        self.items_list.append([self.x,self.y,id1,id2])

    # check the length of the snake's body
    def check_snake_length(self):
        # If the length of the snake's body is greater than the set length, then delete the last snake cell
        if len(self.items_list) >= self.items_count:
            deleted_item = self.items_list.pop(0)
            self.canvas.delete(deleted_item[2])
            self.canvas.delete(deleted_item[3])

    # check whether the snake ate the Apple or not
    def check_apple_found(self):
        # If the coordinates of the Apple and the head match, it means eaten
        if self.apple[0] == self.x and self.apple[1] == self.y:
            self.items_count +=1 # increasing the length of the snake's body
            # deleting the old Apple
            self.canvas.delete(self.apple[2])
            self.canvas.delete(self.apple[3])
            # putting a new Apple
            self.SetNewApple();
            self.apple_count +=1 # increment the Apple counter
            return True
        return False

    # check for a head - to-body collision
    def check_self_touch(self):
        # if the head coordinate coincides with the coordinate of one of the body cells
        for item in self.items_list:
            if self.x == item[0] and self.y == item[1]:
                return False
        
        return True

    # getting information about the snake's environment
    def get_environment(self):
        # Removing the old lines that show the direction of view of the snake along the axes and on the Apple
        if(len(self.lines_list)>0):
            deleted_item = self.lines_list.pop(0)
            self.canvas.delete(deleted_item[0])
            self.canvas.delete(deleted_item[1])
            self.canvas.delete(deleted_item[2])
            self.canvas.delete(deleted_item[3])

        # calculate the coordinates of the Apple relative to the snake's head
        # if you go to the right
        if self.x_nav == 1 and self.y_nav ==0:
            apple_x_offset = self.y - self.apple[1]
            apple_y_offset = self.apple[0] - self.x
            # draw a line to the found point
            line_id_a = self.canvas.create_line(self.x*snake_item, self.y*snake_item, (apple_y_offset+self.x)*snake_item, (self.y - apple_x_offset)*snake_item, dash=(4, 2), fill="black")
        # if we go left
        elif self.x_nav == -1 and self.y_nav ==0:
            apple_x_offset = self.apple[1] - self.y
            apple_y_offset = self.x - self.apple[0]
            # draw a line to the found point
            line_id_a = self.canvas.create_line(self.x*snake_item, self.y*snake_item, (self.x-apple_y_offset)*snake_item, (apple_x_offset+self.y)*snake_item, dash=(4, 2), fill="black")
        # if we go up
        elif self.x_nav == 0 and self.y_nav ==-1:
            apple_x_offset = self.apple[0] - self.x
            apple_y_offset = self.apple[1] - self.y
            # draw a line to the found point
            line_id_a = self.canvas.create_line(self.x*snake_item, self.y*snake_item, (apple_x_offset+self.x)*snake_item, (apple_y_offset+self.y)*snake_item, dash=(4, 2), fill="black")
        # if going down
        elif self.x_nav == 0 and self.y_nav ==1:
            apple_x_offset = self.x - self.apple[0]
            apple_y_offset = self.y - self.apple[1]
            # draw a line to the found point
            line_id_a = self.canvas.create_line(self.x*snake_item, self.y*snake_item, (self.x-apple_x_offset)*snake_item, (self.y-apple_y_offset)*snake_item, dash=(4, 2), fill="black")

        # determining the direction of movement
        direction=0
        # if we go right
        if self.x_nav == 1 and self.y_nav ==0:
            direction=0
        # if we go left
        elif self.x_nav == -1 and self.y_nav ==0:
            direction=1
        # if we go up
        elif self.x_nav == 0 and self.y_nav ==-1:
            direction=2
        # if we go down
        elif self.x_nav == 0 and self.y_nav ==1:
            direction=3

        # calculate the distance to the obstacles relative to the snake's head
        see_wall = 0 # flag of the obstacle in the cell being checked
        cur_distance = 1 # distance at which the check is taking place
        # initial coordinates of the cell being checked
        check_x = self.x
        check_y = self.y
        # the coordinate system will change depending on the direction of movement of the snake
        # we look to the right in the direction of movement
        while not see_wall:
            # if we go to the right
            if self.x_nav == 1 and self.y_nav ==0:
                check_x = self.x
                check_y = self.y + cur_distance
            # if we go left
            elif self.x_nav == -1 and self.y_nav ==0:
                check_x = self.x
                check_y = self.y - cur_distance
            # if we go up
            elif self.x_nav == 0 and self.y_nav ==-1:
                check_x = self.x + cur_distance
                check_y = self.y
            # if we go down
            elif self.x_nav == 0 and self.y_nav ==1:
                check_x = self.x - cur_distance
                check_y = self.y

            # if we have reached the screen borders, then we end the loop
            if check_x<0 or check_x > virtual_game_width:
                see_wall = 1
            if check_y<0 or check_y > virtual_game_height:
                see_wall = 1

            # if reached the wall, then check body
            if not see_wall:
                for item in self.items_list:
                    if check_x == item[0] and check_y == item[1]:
                        see_wall = 1
                        break

            # increasing the distance
            cur_distance +=1

        # draw a line to the found point
        line_id_r = self.canvas.create_line(self.x*snake_item, self.y*snake_item, check_x*snake_item, check_y*snake_item, dash=(4, 2), fill="blue")
        distance_right = cur_distance-1

        see_wall = 0
        cur_distance = 1
        # we look directly in the direction of movement
        while not see_wall:
            # if we go to the right
            if self.x_nav == 1 and self.y_nav ==0:
                check_x = self.x + cur_distance
                check_y = self.y
            # if we go left
            elif self.x_nav == -1 and self.y_nav ==0:
                check_x = self.x - cur_distance
                check_y = self.y
            # if we go up
            elif self.x_nav == 0 and self.y_nav ==-1:
                check_x = self.x
                check_y = self.y - cur_distance
            # if we go down
            elif self.x_nav == 0 and self.y_nav ==1:
                check_x = self.x
                check_y = self.y + cur_distance

            # if we have reached the screen borders, then we end the cycle
            if check_x<0 or check_x > virtual_game_width:
                see_wall = 1
            if check_y<0 or check_y > virtual_game_height:
                see_wall = 1

            # if you haven't reached the wall yet, then check if you have reached your body
            if not see_wall:
                for item in self.items_list:
                    if check_x == item[0] and check_y == item[1]:
                        see_wall = 1
                        break

            # increasing the distance
            cur_distance +=1

        # draw a line to the found point
        line_id_f = self.canvas.create_line(self.x*snake_item, self.y*snake_item, check_x*snake_item, check_y*snake_item, dash=(4, 2), fill="red")
        distance_front = cur_distance-1

        see_wall = 0
        cur_distance = 1
        # we look to the left in the direction of movement
        while not see_wall:
            # if we go to the right
            if self.x_nav == 1 and self.y_nav ==0:
                check_x = self.x
                check_y = self.y - cur_distance
            # if we go left
            elif self.x_nav == -1 and self.y_nav ==0:
                check_x = self.x
                check_y = self.y + cur_distance
            # if we go up
            elif self.x_nav == 0 and self.y_nav ==-1:
                check_x = self.x - cur_distance
                check_y = self.y
            # if we go down
            elif self.x_nav == 0 and self.y_nav ==1:
                check_x = self.x + cur_distance
                check_y = self.y

            # if we reached the screen borders, then we end the cycle
            if check_x<0 or check_x > virtual_game_width:
                see_wall = 1
            if check_y<0 or check_y > virtual_game_height:
                see_wall = 1

            # if you haven't reached the wall yet, then check if you have reached your body
            if not see_wall:
                for item in self.items_list:
                    if check_x == item[0] and check_y == item[1]:
                        see_wall = 1
                        break

            # increasing the distance
            cur_distance +=1

        # draw a line to the found point
        line_id_l = self.canvas.create_line(self.x*snake_item, self.y*snake_item, check_x*snake_item, check_y*snake_item, dash=(4, 2), fill="green")
        distance_left = cur_distance-1

        # adding the constructed lines to the list of lines
        self.lines_list.append([line_id_a,line_id_r, line_id_f, line_id_l])

        # return the received data (x and y of the Apple, direction of movement, distance to the obstacle in the direction of movement: right, straight, left )
        return np.array([apple_x_offset,apple_y_offset,direction, distance_right,distance_front,distance_left])

    # snake movement
    def move(self, action):
        # action=0 - turn right
        # action=1 - do not rotate
        # action=2 - turn left
        if action==0:
            # the data for turning depends on the current movement
            # if we go right
            if self.x_nav == 1 and self.y_nav ==0:
                self.x_nav = 0
                self.y_nav=1
            # if we go left
            elif self.x_nav == -1 and self.y_nav ==0:
                self.x_nav = 0
                self.y_nav=-1
            # if we go up
            elif self.x_nav == 0 and self.y_nav ==-1:
                self.x_nav = 1
                self.y_nav=0
            # if we go down
            elif self.x_nav == 0 and self.y_nav ==1:
                self.x_nav = -1
                self.y_nav=0
        elif action==2: # action=2 - turn left
            # data for turning depends on the current movement
            # if we go right
            if self.x_nav == 1 and self.y_nav ==0:
                self.x_nav = 0
                self.y_nav=-1
            # if we go left
            elif self.x_nav == -1 and self.y_nav ==0:
                self.x_nav = 0
                self.y_nav=1
            # if we go up
            elif self.x_nav == 0 and self.y_nav ==-1:
                self.x_nav = -1
                self.y_nav=0
            # if we go down
            elif self.x_nav == 0 and self.y_nav ==1:
                self.x_nav = 1
                self.y_nav=0

        # check the length of the snake
        self.check_snake_length()
        # changing the coordinates of the head
        self.x += self.x_nav
        self.y += self.y_nav

        # check whether the Apple was found
        apple_founded = self.check_apple_found()

        # check whether you have encountered your body
        # if Yes, then return: end of the game, whether the Apple was found
        if(self.check_self_touch() == False): return True, apple_founded

        # check whether the boundaries of the playing field are exceeded
        # if Yes, then return: end of game, whether the Apple was found
        if self.x <0 or self.x >= virtual_game_width or self.y <0 or self.y >= virtual_game_height:
            return True, apple_founded

        # draw the snake cell
        self.paint_item()

        # return: the game is not over, the number of apples
        return False, apple_founded

    # step of the game
    def step(self, action):
        # move the snake
        # get the result: game finished or not, Apple found or not
        end_game, apple_founded = self.move(action)

        # get data about the environment
        # relative coordinates of the Apple and the distance along the axes from the snake's head to the obstacle
        state = self.get_environment()

        #find the distance to the Apple
        apple_distance = np.sqrt(state[0]*state[0] + state[1]*state[1])

        # Reward: in a simple step
        reward = 1/apple_distance # in a simple step

        if(apple_founded): reward=self.apple_count*3 # if an Apple is found

        # If the game is over, the reward is bad
        if end_game: reward=-10


        return state, reward, end_game