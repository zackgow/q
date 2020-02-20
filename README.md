## Task 2

I've decided to go with Task 2 because
  1. I wanted to gain experience using Pennylane
  2. The problem was interesting.

I was happy to see that in Pennylane v0.8.0 they added a convenience measurement method, `qml.probs()`, that directly allows for the measurement of the computational basis states. The logic here was that the probability is already computed via a single QNode evaluation (analytically on simulators and estimated on hardware) - see the [pull request](https://github.com/XanaduAI/pennylane/pull/432). I thought it would be interesting to directly use the expectation values of the probabilities in the loss function. 

Unfortunately, I discovered that `qml.probs()` is unaffected by the number of shots - this seems to not be in the spirit of the library, since Pennylane aims to be as 'realistic to quantum hardware' as possible. My expectation was that it should be more accurate as the number of shots increased, similar to `qml.expval()`. This is disappointing, because it takes away the last point of the task, which was to do the simulations with sampling / noise. Oddly enough, `qml.sample()` does not support differentiation, even if you try to aggregate statistics on the sampling. 

Some things I experimented with and tidbits of info I learned along the way:
1. using different loss functions: MSE, cross-entropy, Wasserstein, KL-Divergence, etc. - cross-entropy worked best
2. different optimizer functions built into Pennylane: Adam, GradientDescent, etc.
3. trying to access the internal device state for the cost functions (peaking at the amplitudes, etc.)
4. tested running circuits on Pennylane's default devices, as well as ones from Qiskit and Forest
5. `qml.probs()` isn't supported for Qiskit/Forest, so instead I experimented with Hermitian observables to determine the probabilities -- if I had more time I would re-factor and use this method.
6. pennylane-forest has a bug where you need to explicitly edit the `model` parameter on the device, else you get this error:

```python
self.model = self.device.capabilities()["model"]  #: str: circuit type, in {'cv', 'qubit'}
KeyError: 'model'
```
