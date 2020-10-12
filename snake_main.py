from tkinter import *
import time
import random
from snake_class import *
from dqn_class import *

GameStart = True # while true - the program is running
MaxApple = 0 # maximum number of apples eaten in a single game
CurentApple=0 # current number of apples eaten in the game
# the size of the program window
window_width=400
window_height=200

# creating a program window
tk=Tk()
tk.title('Snake')
tk.resizable(0,0)
tk.wm_attributes('-topmost', 1)

# draw interface
#*************************************
canvas = Canvas(tk, width=window_width, height=window_height)
canvas.pack()
canvas.create_rectangle(0, 0, game_width, game_height,outline="white", fill="white")
CurTrialLabel = Label(text="Try:")
CurTrialLabel.place(x=210, y=20)
lblCurTrial = Label(text="0")
lblCurTrial.place(x=270, y=20)
CurStepLabel = Label(text="Move:")
CurStepLabel.place(x=210, y=40)
lblCurStep = Label(text="0")
lblCurStep.place(x=270, y=40)

MaxAppleLabel = Label(text="Max of apples:")
MaxAppleLabel.place(x=210, y=60)
lblMaxApple = Label(text="0")
lblMaxApple.place(x=290, y=60)

CurAppleLabel = Label(text="Apples:")
CurAppleLabel.place(x=210, y=80)
lblCurApple = Label(text="0")
lblCurApple.place(x=290, y=80)

RewardLabel = Label(text="Reward:")
RewardLabel.place(x=210, y=100)
lblReward = Label(text="0")
lblReward.place(x=290, y=100)
tk.update()
#*************************************

snake=snake(canvas) # create the object of the game 

trials = 1000 # number of runs of the game
trial_len = 100# number of moves per game

dqn_agent = DQN() # creating a neural network agent

# stop execution of the program
def end_game():
    global GameStart
    GameStart = False

# stop the game (calling the end_game function)
tk.protocol("WM_DELETE_WINDOW", end_game)

# main program loop
while GameStart:
    # making a series of trials games
    for trial in range(trials):
        if not GameStart: break; # if the Program window is closed, we interrupt the loop

        # displaying the value of the current series of games in the program window
        lblCurTrial.configure(text=str(trial+1))

        CurentApple = 0 # reset the current number of apples
        loss=0.0 # reset the value of the loss function
        total_reward = 0.0 # reset the total reward 

        cur_state = snake.reset().reshape(1, 6) # reset the current state of the environment

        # making trial_len steps
        for step in range(trial_len):
            if not GameStart: break; # if the Program window is closed, we interrupt the loop

            # output the value of the current step to the program window
            lblCurStep.configure(text=str(step+1))

            action = dqn_agent.act(cur_state) # get the action 

            new_state, reward, done = snake.step(action) #performing the action

            total_reward += reward # increase the total reward

            # increase the counter
            if snake.apple_count>MaxApple: MaxApple=snake.apple_count

            lblCurApple.configure(text=str(snake.apple_count)) #update the output counters
            lblMaxApple.configure(text=str(MaxApple)) #update the output counters
            lblReward.configure(text=str(reward)) #update the reward display for a step

            new_state = new_state.reshape(1, 6) # updating the form

            dqn_agent.remember(cur_state, action, reward, new_state, done) # storing data for training

            loss +=dqn_agent.replay() # training the network

            cur_state = new_state # the new state of the environment becomes the current state

            # draw game layouts
            tk.update_idletasks()
            tk.update()

            if done: # if hit a wall, then end the current game
                break

        # After each game, reduce the value of dqn_agent.epsilon
        if dqn_agent.epsilon > dqn_agent.epsilon_min:
            dqn_agent.epsilon -= dqn_agent.epsilon_decay

        #output game data to the console
        print("trial: {}, steps: {}, epsilon: {}, loss: {}, apple: {}, reward: {}".format(trial, step, dqn_agent.epsilon, loss,snake.apple_count, total_reward))
        if trial % 100 == 0:
            dqn_agent.save_model("trial-{}.model".format(trial))

    # After completing the entire series of games - end the program
    GameStart = False