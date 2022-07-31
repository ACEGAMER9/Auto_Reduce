import random
import csv

for i in range(10000):
    m = random.randint(30,100)
    r = random.randint(0,1)
    t = random.randint(17,42)
    h = random.randint(30,100)
    if (m <= 80 and t >= 25 and h >= 60 and r == 0) or (m <= 80 and r == 0):
                    data = [m, t, h, r, int(1)]

                    with open('rambutan.csv', 'a', encoding='UTF8', newline='') as f:
                        writer = csv.writer(f)
                        # write the data
                        writer.writerow(data)
                        f.close()
                        print(i)
    else:
                    data = [m, t, h, r, int(0)]

                    with open('rambutan.csv', 'a', encoding='UTF8', newline='') as f:
                        writer = csv.writer(f)
                        # write the data
                        writer.writerow(data)
                        f.close()
                        print(i)
                    
 
