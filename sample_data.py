import random

with open('data/pred_train','w') as f1:
  with open('data/y_train','w') as f2:
    for i in range(10000):
      y = random.randint(0,1)
      pred = random.random()*0.5 * y + random.random()*0.5
      f1.write('%s\n' % pred)
      f2.write('%s\n' % y)
with open('data/pred_test','w') as f1:
    for i in range(100):
      pred = random.random()*0.5 * y + random.random()*0.5
      f1.write('%s\n' % pred)
