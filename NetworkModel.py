from keras.layers import Input, Conv2D, BatchNormalization, MaxPooling2D, Flatten, Dense, Activation, Dropout
from keras.layers import Lambda, concatenate, AveragePooling2D, Add
from keras.models import Model
from keras.regularizers import l2
from keras import backend as K

class BuildNetworkModel:

    def __init__(self):
        print("\n Loading Network Model...")

    # Define the convolution layer
    def conv2d_bn(self, x, filter_size, kernel_size, padding_type, activation_type):
        weight=5e-4
        x = Conv2D(filters=filter_size, kernel_size=kernel_size, kernel_regularizer=l2(weight), padding=padding_type, activation='linear')(x)
        x = BatchNormalization(axis=-1)(x)
        x = Activation(activation_type)(x)
        return x
    
    # Define the Maxpool Layers
    def maxpool_2d(self, x, pool_size, stride_size, padding_type):
        if stride_size is None:
            stride_size = pool_size
        x = MaxPooling2D(pool_size=(pool_size, pool_size), strides=(stride_size, stride_size), padding=padding_type)(x)
        return x

    """
    Build a VGG like sequential network
    """
    def buildSequentialModel(self, inputsize, num_classes):
        input_layer = Input((64, 64, 3))
        # First block of conv2d -> Maxpool layers
        net = self.conv2d_bn(input_layer, filter_size=64, kernel_size=3, padding_type='same', activation_type='elu')
        net = self.conv2d_bn(net, filter_size=64, kernel_size=3, padding_type='same', activation_type='elu')
        net = self.maxpool_2d(net, pool_size=2, stride_size=2, padding_type='same')
        # Third block of conv2d -> MaxPool layers
        net = self.conv2d_bn(net, filter_size=128, kernel_size=3, padding_type='same', activation_type='elu')
        net = self.conv2d_bn(net, filter_size=128, kernel_size=3, padding_type='same', activation_type='elu')
        net = self.maxpool_2d(net, pool_size=2, stride_size=2, padding_type='same')
        # Fourth block of conv2d -> MaxPool layers
        net = self.conv2d_bn(net, filter_size=256, kernel_size=3, padding_type='same', activation_type='elu')
        net = self.conv2d_bn(net, filter_size=256, kernel_size=3, padding_type='same', activation_type='elu')
        net = self.conv2d_bn(net, filter_size=256, kernel_size=3, padding_type='same', activation_type='elu')
        net = self.maxpool_2d(net, pool_size=2, stride_size=2, padding_type='same')
        # Fifth block of conv2d -> MaxPool layers
        net = self.conv2d_bn(net, filter_size=512, kernel_size=3, padding_type='same', activation_type='elu')
        net = self.conv2d_bn(net, filter_size=512, kernel_size=3, padding_type='same', activation_type='elu')
        net = self.conv2d_bn(net, filter_size=512, kernel_size=3, padding_type='same', activation_type='elu')
        net = self.maxpool_2d(net, pool_size=2, stride_size=2, padding_type='same')
        # Flatten layer
        net = Flatten()(net)
        net = Dense(4096, activation='elu')(net)
        net = Dropout(0.5)(net)
        net = Dense(4096, activation='elu')(net)
        net = Dropout(0.5)(net)        
        net = Dense(num_classes, activation='softmax')(net) 

        # Create the complete model
        model = Model(inputs=input_layer, outputs=net)    
        return model 

    """
    Build an Inception v4 type non-sequential network
    """       
    #def buildInceptionModel(self, inputsize, num_classes)    

if __name__ == '__main__':
    #input and output layer parameters
    input_size = (64, 64, 3)
    num_classes = 200   

    # Calling the network building class
    buildNetwork = BuildNetworkModel()    
    seq_model = buildNetwork.buildSequentialModel(input_size, num_classes)    
    seq_model.summary()


