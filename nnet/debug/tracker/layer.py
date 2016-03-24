from nnet.util.util import nnetController
import theano

class layerTracker(nnetController):
    def __init__(self, nnet):
        nnetController.__init__(self)
        self.set_owner(nnet)
        self.layerFuns = dict()
        self.layerOutputs = dict()

    def get_track_layers(self):
        if not hasattr(self, 'trackLayers'):
            self.trackLayers = []
        return self.trackLayers

    def add_track_layers(self, *layers):
        for layer in layers:
            assert layer in self.get_layers()
        self.get_track_layers().extend(layers)

    def init_layerFuns(self):
        for layer in self.get_track_layers():
            self.layerFuns[layer] = theano.function(inputs=[self.get_inputTensor()], outputs=layer.get_outputTensor())
            self.layerOutputs[layer] = []

    def track_once(self, inputValue):
        for layer in self.get_track_layers():
            self.layerOutputs[layer].append( self.layerFuns[layer](inputValue) )

    def print_info(self, maxCycles=3):
        for i in xrange(3):
            print 'Ouputs in cycle ', i
            for layer in self.get_track_layers():
                print 'Layer: ', layer
                print self.layerOutputs[layer][i]

class layerTrackOptimizer(layerTracker):
    def __init__(self, nnet, opt):
        layerTracker.__init__(self, nnet)
        self.optmizer = opt
        self.optmizer.set_owner(nnet)

    def set_owner(self, nnet):
        '''
        Can't reset nnet
        '''
        assert self.nnet == nnet

    def train_once(self, attr, tar):
        self.optmizer.train_once(attr, tar)
        self.track_once(attr)