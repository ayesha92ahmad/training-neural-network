import numpy as np


class TwoLayersNN (object):
    """" TwoLayersNN classifier """

    def __init__ (self, inputDim, hiddenDim, outputDim):
        self.params = dict()
        self.params['w1'] = None
        self.params['b1'] = None
        self.params['w2'] = None
        self.params['b2'] = None
        #########################################################################
        # TODO: 20 points                                                       #
        # - Generate a random NN weight matrix to use to compute loss.          #
        # - By using dictionary (self.params) to store value                    #
        #   with standard normal distribution and Standard deviation = 0.0001.  #
        #########################################################################
        sigma =0.0001
        self.params['w1'] = sigma * np.random.randn(inputDim,hiddenDim)
        self.params['w2'] = sigma * np.random.randn(hiddenDim,outputDim)
        #choose b1 and b2
        self.params['b1'] = np.zeros(hiddenDim)
        self.params['b2'] = np.zeros(outputDim)
        #########################################################################
        #                       END OF YOUR CODE                                #
        #########################################################################

    def calLoss (self, x, y, reg):
        """
        TwoLayersNN loss function
        D: Input dimension.
        C: Number of Classes.
        N: Number of example.

        Inputs:
        - x: A numpy array of shape (batchSize, D).
        - y: A numpy array of shape (N,) where value < C.
        - reg: (float) regularization strength.

        Returns a tuple of:
        - loss as single float.
        - gradient with respect to each parameter (w1, b1, w2, b2)
        """
        loss = 0.0
        grads = dict()
        grads['w1'] = None
        grads['b1'] = None
        grads['w2'] = None
        grads['b2'] = None
        #############################################################################
        # TODO: 40 points                                                           #
        # - Compute the NN loss and store to loss variable.                         #
        # - Compute gradient for each parameter and store to grads variable.        #
        # - Use Leaky RELU Activation alpha = 0.01 at hidden and output neurons     #
        # - Use Softmax loss
        # Note:                                                                     #
        # - Use L2 regularization                                                   #
        # Hint:                                                                     #
        # - Do forward pass and calculate loss value                                #
        # - Do backward pass and calculate derivatives for each weight and bias     #
        #############################################################################
        w1, b1 = self.params['w1'], self.params['b1']
        w2, b2 = self.params['w2'], self.params['b2']
        z = x.dot(w1) + b1
        #Leaky RELU
        z = np.maximum(0.01*z, z)
        s = z.dot(w2) + b2
        #Leaky RELU
        s= np.maximum(0.01*s,s)
        if y is None:
            return s
        s_ = s - np.max(s, axis = 1).reshape(-1,1)
        p = np.exp(s_)/np.sum(np.exp(s_), axis = 1).reshape(-1,1)
        #Softmax loss
        loss = -np.sum(np.log(p[np.arange(x.shape[0]), y]))
        loss /= x.shape[0]
        #L2 regularization
        loss +=   reg * (np.sum(w1 * w1) + np.sum(w2 * w2))

        #backward pass
        ds = p.copy()
        ds[np.arange(x.shape[0]), y] -= 1
        ds /= x.shape[0]
        grads['w2'] = z.T.dot(ds) + 2 * reg * w2
        grads['b2'] = np.sum(ds, axis = 0)

        dh = ds.dot(w2.T)
        dh_ReLu = (z > 0) * dh
        grads['w1'] = x.T.dot(dh_ReLu) + 2 * reg * w1
        grads['b1'] = np.sum(dh_ReLu, axis = 0)


        #############################################################################
        #                          END OF YOUR CODE                                 #
        #############################################################################

        return loss, grads

    def train (self, x, y, lr=5e-3, reg=5e-3, iterations=100, batchSize=200, decay=0.95, verbose=False):
        """
        Train this linear classifier using stochastic gradient descent.
        D: Input dimension.
        C: Number of Classes.
        N: Number of example.

        Inputs:
        - x: training data of shape (N, D)
        - y: output data of shape (N, ) where value < C
        - lr: (float) learning rate for optimization.
        - reg: (float) regularization strength.
        - iter: (integer) total number of iterations.
        - batchSize: (integer) number of example in each batch running.
        - verbose: (boolean) Print log of loss and training accuracy.

        Outputs:
        A list containing the value of the loss function at each training iteration.
        """

        # Run stochastic gradient descent to optimize W.
        lossHistory = []
        for i in range(iterations):
            xBatch = None
            yBatch = None
            #########################################################################
            # TODO: 10 points                                                       #
            # - Sample batchSize from training data and save to xBatch and yBatch   #
            # - After sampling xBatch should have shape (batchSize, D)              #
            #                  yBatch (batchSize, )                                 #
            # - Use that sample for gradient decent optimization.                   #
            # - Update the weights using the gradient and the learning rate.        #
            #                                                                       #
            # Hint:                                                                 #
            # - Use np.random.choice                                                #
            #########################################################################
            num_train = np.random.choice(x.shape[0], batchSize)
            xBatch = x[num_train]
            yBatch = y[num_train]
            loss, grads = self.calLoss(xBatch,yBatch,reg)
            lossHistory.append(loss)
            #update weight and learning rate
            self.params['w2'] += - lr * grads['w2']
            self.params['b2'] += - lr * grads['b2']
            self.params['w1'] += - lr * grads['w1']
            self.params['b1'] += - lr * grads['b1']

            #########################################################################
            #                       END OF YOUR CODE                                #
            #########################################################################
            # Decay learning rate
            lr *= decay
            # Print loss for every 100 iterations
            if verbose and i % 100 == 0 and len(lossHistory) is not 0:
                print ('Loop {0} loss {1}'.format(i, lossHistory[i]))

        return lossHistory

    def predict (self, x,):
        """
        Predict the y output.

        Inputs:
        - x: training data of shape (N, D)

        Returns:
        - yPred: output data of shape (N, ) where value < C
        """
        yPred = np.zeros(x.shape[0])
        ###########################################################################
        # TODO: 10 points                                                         #
        # -  Store the predict output in yPred                                    #
        ###########################################################################

        h = np.maximum(0, x.dot(self.params['w1']) + self.params['b1'])
        scores = h.dot(self.params['w2']) + self.params['b2']
        yPred = np.argmax(scores, axis=1)
        ###########################################################################
        #                           END OF YOUR CODE                              #
        ###########################################################################
        return yPred


    def calAccuracy (self, x, y):
        acc = 0
        ###########################################################################
        # TODO: 10 points                                                         #
        # -  Calculate accuracy of the predict value and store to acc variable    #
        ###########################################################################
        yPred = self.predict(x)
        acc = np.mean(y == yPred)*100

        ###########################################################################
        #                           END OF YOUR CODE                              #
        ###########################################################################
        return acc
