import re
expression = re.compile("Output:\s+(7\d+\.\d)")

with open('good_enough.csv', 'w') as w:
    w.write("CallCount,Bandwidth\n")
    matched = False
    calls = 0
    wating = False
    for line in open("good_enough.log"):
        matched = expression.search(line)
        if matched and not waiting:
            calls += 1
            bandwidth = matched.groups()[0]
            w.write("{0},{1}\n".format(calls, bandwidth))
            calls = 0
            waiting = True
            continue
        
        if matched:
           continue
        
        if "Starting" in line:
            calls = 0
            waiting = False
            continue
        calls += 1
            
