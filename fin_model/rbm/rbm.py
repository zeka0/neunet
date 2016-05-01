from ether import *
debug = True
filePath = r'E:\VirtualDesktop\nnet\minist\flatten_double_mnist.pkl.gz'
model_fname = 'rbm'

mnist_reader = mnistDataReader(filePath, 10)
db = fullPool(mnist_reader.read_all(), True)
opt = SGDOptimizer()

persistent_chain = theano.shared(np.zeros((500, 1), dtype=theano.config.floatX), borrow=True)
biasInitDic = {'distr':'constant', 'value':0.}
weightInitDic = {'distr':'uniform', 'low':-np.sqrt(6./(784 + 500)), 'high':np.sqrt(6./(784 + 500))}
rbm = RestrictedBM(784, 500, vbias=biasInitDic, hbias=biasInitDic, weight=weightInitDic, persistent=persistent_chain)
tri = trainer(db, opt, None, rbm)

print 'compling the trainer'
tri.compile()
print 'training the rbm'
tri.train(2000)

dump_trainer(tri)

import PIL.Image as Image
persistent_vis_chain = theano.shared( db.read_instances(1) )
# end-snippet-6 start-snippet-7
plot_every = 1000
# define one step of Gibbs sampling (mf = mean-field) define a
# function that does `plot_every` steps before returning the
# sample for plotting
(
    [
        presig_hids,
        hid_mfs,
        hid_samples,
        presig_vis,
        vis_mfs,
        vis_samples
    ],
    updates
) = theano.scan(
    rbm.gibbs_vhv,
    outputs_info=[None, None, None, None, None, persistent_vis_chain],
    n_steps=plot_every,
    name="gibbs_vhv"
)

# add to updates the shared variable that takes care of our persistent
# chain :.
updates.update({persistent_vis_chain: vis_samples[-1]})
# construct the function that implements our persistent chain.
# we generate the "mean field" activations for plotting and the actual
# samples for reinitializing the state of our persistent chain
sample_fn = theano.function(
    [T.matrix()],
    [
        vis_mfs[-1],
        vis_samples[-1]
    ],
    updates=updates
)

# create a space to store the image for plotting ( we need to leave
# room for the tile_spacing as well)
image_data = np.zeros(
    (29 * 5+ 1, 29 * 1- 1),
    dtype='uint8'
)
from ether.debug.plot import tile_raster_images
for idx in range(5000):
    # generate `plot_every` intermediate samples that we discard,
    # because successive samples in the chain are too correlated
    vis_mf, vis_sample = sample_fn(db.read_instances(1))
    print(' ... plotting sample %d' % idx)
    image_data[29 * idx:29 * idx + 28, :] = tile_raster_images(
        X=vis_mf,
        img_shape=(28, 28),
        tile_shape=(1, 1),
        tile_spacing=(1, 1)
    )

# construct image
image = Image.fromarray(image_data)
image.save('samples.png')
# end-snippet-7
os.chdir('../')
