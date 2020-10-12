import random
import numpy as np

from keras.models import Sequential
from keras.layers import Dense, Flatten, Activation
from keras.optimizers import Adam

class DQN:
    def __init__(self):
        self.memory = [] # array of experience for learning
        # coefficients for training
        self.gamma = 0.85
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = (1.0 - self.epsilon_min) / 1000
        self.learning_rate = 0.005
        self.tau = .125

        self.model = self.create_model() # creating the model itself
    
    # Creating the model
    def create_model(self):
        # we get 5 numbers as input: coordinates of the Apple and 3 distances to the obstacle
        # on vokhod we get 3 numbers: turn right, don't turn, turn left
        model   = Sequential()
        model.add(Dense(10, input_dim=6, activation="relu"))
        model.add(Dense(10, activation="relu"))
        model.add(Dense(3))
        model.compile(loss="mean_squared_error", optimizer=Adam(lr=self.learning_rate))
        model.summary()
        return model

    # get the action being performed
    def act(self, state):
        self.epsilon = max(self.epsilon_min, self.epsilon) # take the max Epsilon value
        # randomly (depending on Epsilon) choose: either a random action, or predict using the model
        if np.random.random() < self.epsilon:
            return random.randint(0,2)
        return np.argmax(self.model.predict(state)[0])

    # remember the current situation in the array of experiences
    def remember(self, state, action, reward, new_state, done):
        self.memory.append([state, action, reward, new_state, done])

    # training the model
    def replay(self):
        batch_size = 32 # of the batch size for training
        # If there is not enough data for training, then we do not train
        if len(self.memory) < batch_size:
            return 0.0

        # taking a random set of data from the experience for training
        samples = np.array(random.sample(self.memory, batch_size))

        # I will not call the model training for each element from the examples separately
        # This greatly slows down the process
        # Instead, I make a set of lists from training data. And then I train them all at once
        # model - it works faster this way

        # Create a null list
        state=np.zeros((batch_size,6)) # for initial States of the environment
        action=np.zeros((batch_size), dtype = np.int8) # for actions taken
        reward=np.zeros((batch_size)) # for the reward received for these actions
        new_state=np.zeros((batch_size,6)) # for new environment States
        done=np.zeros((batch_size)) # for the game completion flag

        # sorting through items from the training kit and filling out lists
        i=0
        for sample in samples:
            state[i], action[i], reward[i], new_state[i], done[i] = sample
            i +=1

        # selecting actions for the current state
        Y_state = self.model.predict(state)

        # find out the future reward:
        # choose actions for the new state
        Y_new_state = self.model.predict(new_state)

        # taking the best action for the new state
        Q_future=np.max(Y_new_state, axis=1).reshape(batch_size,1)

        # iterating over the received data for training
        # changing the table based on remuneration
        for i in range(batch_size):
            if done[i]:
                Y_state[i,action[i]] = reward[i]
            else:
                Y_state[i,action[i]] = reward[i] + Q_future[i] * self.gamma 


        # training the model on the received data
        cur_loss = self.model.train_on_batch(state,Y_state) 
        
        return cur_loss

    # saving the model
    def save_model(self, fn):
        self.model.save(fn)