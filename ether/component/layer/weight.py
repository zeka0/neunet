from core import *
from ether.util.shape import *
from ether.component.initialize import init_shared

class weightLayer(layer):
    '''
    We can view weight-layer as a conv1D layer
    '''
    def __init__(self, numOfOutput, **kwargs):
        layer.__init__(self)
        self.numOfOutput = numOfOutput
        assert kwargs.has_key('weight')
        assert kwargs.has_key('bias')
        self.weightKwargs = kwargs['weight']
        self.biasKwargs = kwargs['bias']
        assert not self.weightKwargs.has_key('shape')
        self.init_bias()

    def init_weights(self):
        self.weights = init_shared(shape=self.get_weightShape(), **self.weightKwargs)

    def init_bias(self):
        self.bias = init_shared(shape=(1,), **self.biasKwargs)

    def get_weights(self):
        return self.weights

    def get_bias(self):
        return self.bias

    def get_inputShape(self):
        return self.inputShape

    def get_weightShape(self):
        return (self.get_inputShape()[1], self.numOfOutput)

    def get_outputShape(self):
        return ( self.inputShape[0], self.numOfOutput )

    def get_params(self):
        paramList = []
        paramList.append( self.get_weights() )
        paramList.append( self.get_bias() )
        return paramList

    def connect(self, *layers):
        assert len(layers) == 1
        self.inputShape = layers[0].get_outputShape()
        assert len(self.inputShape) == 2
        self.set_inputTensor( layers[0].get_outputTensor() )
        self.init_weights()
        outputTensor = self.get_inputTensor().dot( self.get_weights() ) + self.get_bias()
        self.set_outputTensor(outputTensor)