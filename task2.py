from pennylane import numpy as np
import pennylane as qml

# loss functions #
def cross_entropy(y, yhat, nonzero_term=1e-10):
    return -np.sum([y[i] * np.log(yhat[i] + nonzero_term) for i in range(len(y))])

def mse(y, yhat):
    return np.square(np.subtract(y, yhat)).mean()

# program to run task # 
def run(**params):

    dev = qml.device('default.qubit', shots=params['shots'], wires=2, analytic=False)
    opt = params['optimizer'](params['lr'])
    var = params['theta']

    # cost function # 
    def cost(var):
        res = circuit(var)
        val = params['loss'](params['target'], res)
        return val

    # circuit #
    @qml.qnode(dev)
    def circuit(var):
        if params['gate'] == 'RX':
            qml.RX(var[0], wires=0)
        if params['gate'] == 'RY':
            qml.RY(var[1], wires=0)
        if params['gate'] == 'both':
            qml.RX(var[0], wires=0)
            qml.RY(var[1], wires=0)
        qml.CNOT(wires=[0,1])
        return qml.probs(wires=[0,1]) 

    print('initial rotation parameters theta: {}'.format(var))
    print('initial probabilities: {}'.format(circuit(var)))
    print()

    for it in range(params['steps']+1):
        var = opt.step(cost, var)
        if it%25 == 0: print("Step {}: cost: {}, probabilities: {}".format(it, np.round(cost(var),6), circuit(var)))

    print()
    print('final rotation parameters theta: {}'.format(var))
    print('output probabilities:    {}'.format(circuit(var)))

    print('ending circuit state: {}'.format(dev._state))
    print(circuit.draw())
    return

theta = np.random.rand(2) * np.pi
print('value of theta: {}').format(theta)

for shot in [1, 10, 100, 1000, 10000]:
    parameters = {
        'theta': theta,
        'steps': 300,
        'lr': 0.05,
        'shots': shot,
        'gate': 'both',
        'target': [.5,0,0,.5],
        'optimizer': qml.GradientDescentOptimizer,
        'loss':cross_entropy
        }

    run(**parameters)
    print("-"*30)
    print("----- FINISHED WITH  {}  -----".format(shot))
    print("-"*30)
