# coding=utf-8
import os
import matplotlib.pyplot as plt

log_file = './logs/train-2022-12-02@11_39_03.log'
lines = open(log_file, 'r')
losses = []
acces = []
for line in lines:
    if 'backward_time:' in line:
        loss_ = float(line.split('head/CE: ')[1].split('  ')[0])
        losses.append(loss_)
        acc = float(line.split('head/acc: ')[1].split(' ')[0])
        acces.append(acc)

plt.plot([a*100 for a in range(len(losses))], losses)    
plt.savefig('train_loss.png') 
plt.close()
plt.plot([a*100 for a in range(len(losses))], acces)  
plt.savefig('train_acc.png') 
