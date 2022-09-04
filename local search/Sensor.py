import subprocess
from subprocess import Popen, PIPE, STDOUT

def evaluateState(x):
    # use these lines to send input to objective function :
    p = Popen(['ObjectiveFunction/objectiveFunction.exe'], stdout=PIPE, stdin=PIPE, stderr=PIPE, text=True)
    output = p.communicate(input=(str(x)))[0]
    return float(output)
