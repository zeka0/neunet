from ether.component.layer import *

class nnet(object):
    '''
    Provide a general interface to components
    Unlike previously-designed nnet, this one makes it possible for outsiders to initialize the net for it
    Providing a better control over the layers
    It's considered as a great advantage because you may now pre-train layers with greater ease
    '''
    def __init__(self, layers):
        self.set_layers( layers )
        self.targetTensor=T.vector()

    def set_layers(self, layers):
        '''
        The layers must be pre-set before the nnet is put into use
        '''
        self.layers = layers

    def get_layers(self):
        return self.layers

    def get_params(self):
        '''
        Returns weights in ascending order of the layers
        Will be deprecated in the future
        '''
        params=[]
        for i in range(1, len(self.layers)): #Skip inputLayer
            if self.get_layers()[i].has_trainableParams():
                params.extend(self.layers[i].get_params()) #Add paras in specific-order
        return params

    def predict(self, attrVec):
        outputFunc = self.get_outputFunction()
        return outputFunc(attrVec)

    def get_inputTensor(self):
        return self.layers[0].get_inputTensor()

    def get_outputTensor(self):
        return self.layers[-1].get_outputTensor()

    def get_targetTensor(self):
        return self.targetTensor

    def get_outputFunction(self):
        if not hasattr(self, 'outputFunction'):
            self.outputFunction=theano.function(inputs=[self.get_inputTensor()], outputs=self.get_outputTensor())
        return self.outputFunction

    def get_layerOutputTensors(self):
        li = []
        for layer in self.layers:
            li.append(layer.get_outputTensor())
        return li
