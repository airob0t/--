#coding:utf-8

f = open("problems.txt", 'r')
problem = f.read()
f.close()
#print problem

f = open("answer.txt",'w')
start = 0
i=0
answer = ''
while True:
    start = problem.find('答案',start)
    if start == -1:
        break
    end = problem.find('\n',start)
    answer += problem[start:end+1]
    print problem[start:end+1]
    i += 1
    start = end
print i
f.write(answer+'答案：2')
f.close()
