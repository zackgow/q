## Task 2

I've decided to go with Task 2 because
  1. I wanted to gain experience using Pennylane
  2. The problem was interesting.

I was happy to see that in Pennylane v0.8.0 they added a convenience measurement method, `qml.probs()`, that directly allows for the measurement of the computational basis states. The logic here was that the probability is already computed via a single QNode evaluation (analytically on simulators and estimated on hardware) - see the [pull request](https://github.com/XanaduAI/pennylane/pull/432). I thought it would be interesting to directly use the expectation values of the probabilities in the loss function. 

Unfortunately, I discovered that `qml.probs()` is unaffected by the number of shots - this seems to not be in the spirit of the library, since Pennylane aims to be as 'realistic to quantum hardware' as possible. My expectation was that it should be more accurate as the number of shots increased, similar to `qml.expval()`. This is disappointing, because it takes away the last point of the task, which was to do the simulations with sampling / noise. Oddly enough, `qml.sample()` does not support differentiation, even if you try to aggregate statistics on the sampling. 

Some things I experimented with and tidbits of info I learned along the way:
1. using different loss functions: MSE, cross-entropy, Wasserstein, KL-Divergence, etc. - cross-entropy worked best
2. different optimizer functions built into Pennylane: Adam, GradientDescent, etc.
3. testing out different circuit combinations of **RX** and **RY** gates across single and multiple wires
4. trying to access the internal device state for the cost functions (peaking at the amplitudes, etc.)
5. tested running circuits on Pennylane's default devices, as well as ones from Qiskit and Forest
6. `qml.probs()` isn't supported for Qiskit/Forest, so instead I experimented with Hermitian observables to determine the probabilities -- if I had more time I would re-factor and use this method.
7. pennylane-forest has a bug where you need to explicitly edit the `model` parameter on the device, else you get this error:

```python
self.model = self.device.capabilities()["model"]  #: str: circuit type, in {'cv', 'qubit'}
KeyError: 'model'
```

--------
### code and results
The code is wrapped in a `run` function that takes a dictionary of parameters as inputs. This allows us to vary the input angles, steps, optimizer, loss function, target, learning rate, shots, and gate controls - leading to faster experimentation. 

To test the code, simply edit the parameter dict and invoke `python task2.py`


If using a single parameter and one rotation gate with a **CNOT**, the optimal value approaches **pi/2**

**RX + CNOT = |00⟩ - |11⟩**

**RY + CNOT = |00⟩ + |11⟩**

Using **RX** and **RY** with a **CNOT** (in mixed orders), the results give us identical measured probabilities, though the underlying circuit state some times appears to be mixed.To illustrate:

dev._state: [0.68885002+0.15964226j,  0.+0.j,  0.+0.j,  0.68885002-0.15964226j]
 
```
 0: ──RX(0.455)──RY(1.571)──╭C──╭┤ ObservableReturnTypes.Probability[I]
 1: ────────────────────────╰X──╰┤ ObservableReturnTypes.Probability[I]
```
