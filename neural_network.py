# Neural Network (one layered)- 3.12.2018

import sys
import numpy as np
from neuronLayer import * 

class neuralNetwork:

	def __init__(self, inputArr):
		#numNeurons is the number of neurons in that layer
		#inputArr is the array of outputs of the previous layer, or the input data at the input layer
		self.inputLayer = neuronLayer(len(inputArr), inputArr);
		self.neuronLayerArr = [];
		self.inputArr = inputArr;
		self.neuronLayerArr.append(self.inputLayer);

	#this constructor only creates a blank array, assuming that neurons will be injected separately	
	def __init__(self):
		self.neuronLayerArr = [];		
		
	def addNeuronLayer(self, neuronLayer):
		self.neuronLayerArr.append(neuronLayer);

	def getNeuronLayerAtIdx(self, idx):
		return self.neuronLayerArr[idx];

	def getNeuronLayerArr(self):
		return self.neuronLayerArr;

	#this method returns the hypothesis for a given input
	def getOutputArr(self, inputArr):
		#return output without bias unit
		outputArr = np.delete(self.propagateForward(inputArr,len(self.neuronLayerArr)-1),0);
		return np.around(outputArr,3);
		
	def propagateForward(self, inputArr, idx):		
		if idx<=0:
			return self.neuronLayerArr[0].getOutputArr(inputArr);
		else:
			return self.neuronLayerArr[idx].getOutputArr(self.propagateForward(inputArr, idx-1));
			
	def propagateBack(self, expectedPoint):
		networkError = []; #used to hold delta values for each layer
		for i in range (0, len(self.neuronLayerArr)):
			networkError.append(0);
		hypothesis = self.getOutputArr(expectedPoint.getInputArr());
		lastLayerIdx = len(self.neuronLayerArr)-1# len starts from 1, not 0
		print('__________\nHypothesis for '+str(expectedPoint.getInputArr())+' : '+str(hypothesis));
		print('Expected Output for '+str(expectedPoint.getInputArr())+' : '+str(expectedPoint.getOutput()));

		networkError[lastLayerIdx] = hypothesis - expectedPoint.getOutput();# these don't include bias terms
		self.neuronLayerArr[lastLayerIdx].addToNetError(networkError[lastLayerIdx]);
		print('Error for '+str(expectedPoint.getInputArr())+' : '+str(networkError[lastLayerIdx]));

		for i in range (len(self.neuronLayerArr)-2 , 1): #loop covers all hidden layers
			#supply networkError on (i+1)th layer to i'th layer
			networkError[i] = self.neuronLayerArr[i].updateBackPropError(networkError[i+1]);
			#updateBackPropError returns the error vector of that layer to the network level matrix, 
			#and adds the error of that training example to net error array of that layer
			
		return networkError;

	def resetAllLayerErrors(self):
		for layer in self.neuronLayerArr:
			layer.resetNetError();

	def updateModel(self, dataset):
		i=0
		m=len(dataset.getData())
		while i<100:		
			for layer in self.neuronLayerArr:
				layer.updateNeurons(m);
				i=i+1;
			self.computeNetError(dataset);

	def computeNetError(self, dataset):
		self.resetAllLayerErrors();#incremental computations shouldn't stack
		for point in dataset.getData():
			self.propagateBack(point)#this is the training example
		i=0
		for layer in self.neuronLayerArr:
			print('Net error of layer '+str(i)+' over all examples: '+str(layer.netError));
			i=i+1;
		print('__________________________________________________')