import tensorflow as tf
import os

from Agent import get_agent_actions_table
from BpEnv import BpEnv

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import time

from PiRL import rule_table
from antlr4.CommonTokenStream import CommonTokenStream
from antlr4.StdinStream import StdinStream

from PiRL.GrammarParser import MetaGrammarLexer
from PiRL.GrammarParser.MetaGrammarParser import MetaGrammarParser
from PiRL.ProgramGen.ParseTreeGenerator import getProgTree

from PiRL.TFCodegen.TFCodegen import TFCodegen
from PiRL.ProgramGen.SketchBuilderVisitor import SketchBuilderVisitor
from PiRL.TFCodegen.CodegenFns import trainable_map, input_map
from PiRL.TFCodegen import CodegenFns
from PiRL.TFCodegen.TFCodegen import callGraph

# Parameters
lr = 0.005
episodes = 1000
tb_writer = tf.summary.create_file_writer(f"./runs/{time.time()}")

# Loading pre-trained model 
env = BpEnv(100)
states = env.observation_space.shape
actions = env.action_space.n

Q = get_agent_actions_table()

# Parsing the given sketch
lexer = MetaGrammarLexer.MetaGrammarLexer(StdinStream())
token_stream = CommonTokenStream(lexer)
parser = MetaGrammarParser(token_stream)
tree = parser.sketch()
tree.accept(SketchBuilderVisitor())

# Generating a random program from the sketch
tree = getProgTree(rule_table.start, 20)
print("=================Generated Program==============")
for leaf in tree.leaves():
    print(leaf.data.name, end=' ')
print()

# Optimizing the program
optimiser = tf.keras.optimizers.Adam(learning_rate=lr)

# Training
for ep in range(episodes):
    if ep % 50 == 0 and ep > 0:
        print("Final generated variables:", trainable_map)
    # Resetting stuff
    bp_err = env.reset()
    bp_err_list = [0]
    done = False
    loss = 0

    with tf.GradientTape() as g:
        batch_size = 0
        while not done:
            bp_err_list.append(bp_err)
            inputData = {
                "h1": bp_err_list[-1],
                "h2": sum(bp_err_list),
                "h3": bp_err_list[-2] - bp_err_list[-1]
            }

            # Target model value
            time = env.get_time()
            rnd = env.get_rnd()
            label = Q[rnd][time]
            # Adding to loss
            CodegenFns.g = g
            train_fn = TFCodegen(tree.get_node(tree.root), tree)
            val = callGraph(train_fn, inputData)
            loss += (label - val) ** 2

            # Selecting an action
            action = env.action_space.sample()

            # Next frame please
            bp_err, reward, done, _ = env.step(label)

            batch_size += 1

        loss /= batch_size

    sources = [item[1] for item in trainable_map.items()]
    grads = g.gradient(loss, sources)
    optimiser.apply_gradients(zip(grads, sources))

    print("Episode:", ep, "Loss:", loss)
    with tb_writer.as_default():
        tf.summary.scalar("loss", loss[0], ep)

    # Calculating the reward for the current program
    bp_err_ = env.reset()
    bp_err_list = [0]
    done = False
    cum_reward = 0
    tf.config.run_functions_eagerly(True)
    while not done:
        bp_err_list.append(bp_err_)
        inputData = {
            "h1": bp_err_list[-1],
            "h2": sum(bp_err_list),
            "h3": bp_err_list[-2] - bp_err_list[-1]
        }
        train_fn = TFCodegen(tree.get_node(tree.root), tree)
        action = callGraph(train_fn, inputData)
        action = action.numpy().round().astype(int)[0]

        bp_err_, reward, done, _ = env.step(action)
        cum_reward += reward

    print("Avg Reward of the program:", cum_reward / 193)

    with tb_writer.as_default():
        tf.summary.scalar("Cumulative Reward", cum_reward, ep)

print("Final generated variables:", trainable_map)
