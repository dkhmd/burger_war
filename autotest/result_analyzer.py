#!/usr/bin/env python2
# -*- coding: utf-8 -*-


# Analyze automated test results
# Specify the path of .log file to "path" in main function
# Create a folder called graph and save the result


import matplotlib.pyplot as plt
import os


class fight_result:

    def __init__(self):
        self.my_score = []
        self.enemy_score = []
        self.result = []
        self.result_onekillwin = []
        self.result_onekilllose = []
        self.commit_seq = []

    def set_commit_seq(self):
        self.commit_seq.append(len(self.result))

    def add_score(self, me, enemy):
        self.my_score.append(me)
        self.enemy_score.append(enemy)
        if me > enemy:
            self.result.append(1)
        else:
            self.result.append(0)

        # summarize 1kill result
        if me > enemy+10:
            self.result_onekillwin.append(1)
        else:
            self.result_onekillwin.append(0)
        if me+10 < enemy:
            self.result_onekilllose.append(1)
        else:
            self.result_onekilllose.append(0)

    def my_average(self):
        return sum(self.my_score)/len(self.my_score)

    def enemy_average(self):
        return sum(self.enemy_score)/len(self.enemy_score)

    def winning_rate(self):
        return float(sum(self.result))/float(len(self.result))

    def onekillwin_rate(self):
        return float(sum(self.result_onekillwin))/float(len(self.result_onekillwin))

    def onekilllose_rate(self):
        return float(sum(self.result_onekilllose))/float(len(self.result_onekilllose))
    
    def transition(self, num):
        winning_rate_transition = []
        my_point_transtion = []
        enemy_point_transtion = []

        for i in range(0, len(self.result), num):
            winning_rate_transition.append(
                float(sum(self.result[i:i+num]))/float(len(self.result[i:i+num])))
            my_point_transtion.append(
                float(sum(self.my_score[i:i+num]))/float(len(self.result[i:i+num])))
            enemy_point_transtion.append(
                float(sum(self.enemy_score[i:i+num]))/float(len(self.result[i:i+num])))

        return winning_rate_transition, my_point_transtion, enemy_point_transtion

    def commit_transition(self):
        start = 0
        winning_rate_transition = []
        my_point_transtion = []
        enemy_point_transtion = []
        for i in self.commit_seq:
            winning_rate_transition.append(
                float(sum(self.result[start:i+1]))/float(i-start))
            my_point_transtion.append(
                sum(self.my_score[start:i+1])/float(i-start))
            enemy_point_transtion.append(
                sum(self.enemy_score[start:i+1])/float(i-start))
            start = i
        return winning_rate_transition, my_point_transtion, enemy_point_transtion

    def plot(self, seq, name):
        (winning_rate, my_point, enemy_point) = self.transition(seq)
        fig = plt.figure()
        self.rate = fig.add_subplot(1, 2, 1)
        self.plot_winning_rate(winning_rate, seq)
        self.score = fig.add_subplot(1, 2, 2)
        self.plot_points(my_point, enemy_point, seq)

        save_path = 'autotest/graph/'
        if not os.path.isdir(save_path):
            os.makedirs(save_path)
        plt.savefig(save_path+name+'.png')
        plt.close()

    def plot_points(self, my_point, enemy_point, seq):
        number = range(0, len(self.result), seq)
        self.score = plt.plot(number, my_point)
        self.score = plt.plot(number, enemy_point)
        self.score = plt.title('score every '+str(seq)+' games')
        self.score = plt.xlabel("number of games")
        self.score = plt.ylabel("score")
        self.score = plt.legend(["my score", "enemy_score", "commit"])
        self.plot_commit_timing(self.score)
        self.score = plt.ylim([0, 20])

    def plot_winning_rate(self, winning_rate, seq):
        number = range(0, len(self.result), seq)
        self.rate = plt.plot(number, winning_rate)
        self.rate = plt.title('winning rate every '+str(seq)+' games')
        self.rate = plt.xlabel("number of games")
        self.rate = plt.ylabel(["winning rate", "commit"])
        self.plot_commit_timing(self.rate)
        self.rate = plt.ylim([0, 1.1])

    def plot_commit_timing(self, fig):
        for i in self.commit_seq:
            fig = plt.vlines(i, 0, 20, colors='red', linestyles='dashed')


def main():
    path = 'autotest/result-20200810.log'
    # path = 'autotest/result.log'
    f = open(path)
    data = f.readlines()
    cheese = fight_result()
    teriyaki = fight_result()
    clubhouse = fight_result()

    for line in data[2:-1]:
        if 'commit' in line:
            print('detect commit')
            cheese.set_commit_seq()
            teriyaki.set_commit_seq()
            clubhouse.set_commit_seq()
            continue

        result = line.split(',')
        if len(result) != 7:
            print('error line')
            continue

        if int(result[1]) == 1:
            cheese.add_score(float(result[4]), float(result[5]))
        elif int(result[1]) == 2:
            teriyaki.add_score(float(result[4]), float(result[5]))
        elif int(result[1]) == 3:
            clubhouse.add_score(float(result[4]), float(result[5]))
        else:
            print('unknown enemy')
            continue

    print('-------------------------------------------------------------')
    print('              vs cheese    vs teriyaki    vs clubhouse')
    print('winning rate: '+'{:.2f}'.format(cheese.winning_rate()).rjust(len('vs cheese'))+'    '
          + '{:.2f}'.format(teriyaki.winning_rate()
                            ).rjust(len('vs teriyaki'))+'    '
          + '{:.2f}'.format(clubhouse.winning_rate()).rjust(len('vs clubhouse')))

    print('onekill win : '+'{:.2f}'.format(cheese.onekillwin_rate()).rjust(len('vs cheese'))+'    '
          + '{:.2f}'.format(teriyaki.onekillwin_rate()
                            ).rjust(len('vs teriyaki'))+'    '
          + '{:.2f}'.format(clubhouse.onekillwin_rate()).rjust(len('vs clubhouse')))

    print('onekill lose: '+'{:.2f}'.format(cheese.onekilllose_rate()).rjust(len('vs cheese'))+'    '
          + '{:.2f}'.format(teriyaki.onekilllose_rate()
                            ).rjust(len('vs teriyaki'))+'    '
          + '{:.2f}'.format(clubhouse.onekilllose_rate()).rjust(len('vs clubhouse')))

    print('my_score:     '+'{:.2f}'.format(cheese.my_average()).rjust(len('vs cheese'))+'    '
          + '{:.2f}'.format(teriyaki.my_average()
                            ).rjust(len('vs teriyaki'))+'    '
          + '{:.2f}'.format(clubhouse.my_average()).rjust(len('vs clubhouse')))

    print('enemy_score:  '+'{:.2f}'.format(cheese.enemy_average()).rjust(len('vs cheese'))+'    '
          + '{:.2f}'.format(teriyaki.enemy_average()
                            ).rjust(len('vs teriyaki'))+'    '
          + '{:.2f}'.format(clubhouse.enemy_average()).rjust(len('vs clubhouse')))
    print('\nnumber of games: '+str(len(cheese.result)))

    cheese.plot(5, 'vs_cheese')
    teriyaki.plot(5, 'vs_teriyaki')
    clubhouse.plot(5, 'vs_clubhouse')


if __name__ == "__main__":
    main()
