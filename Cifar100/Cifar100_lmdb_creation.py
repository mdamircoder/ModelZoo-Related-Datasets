import os
import cPickle

import numpy as np
import sklearn
import sklearn.linear_model
from sklearn.cross_validation import train_test_split

import lmdb
import sys
sys.path.append("/path/to/caffe/python")
import caffe

def unpickle(file):
	""" unpickle the data """
	fo = open(file, 'rb')
	dict = cPickle.load(fo)
	fo.close()
	return dict

def shuffle_data(data, labels):
	data, _, labels, _ = sklearn.cross_validation.train_test_split(data, labels, test_size=0.0, random_state=42)
	return data, labels

def load_data(train_file):
	"""  load the train and test data"""
	d = unpickle(train_file)
	data = d['data']
    	#coarse_labels = d['coarse_labels']
	fine_labels = d['fine_labels']
	length = len(d['fine_labels'])

	data, labels = shuffle_data(
        	data,
        	#np.array(zip(coarse_labels, fine_labels))
        	np.array(fine_labels)
	)
    	#coarse_labels, fine_labels = zip(*labels.tolist())
    	return (
		data.reshape(length, 3, 32, 32),
        	#np.array(coarse_labels),
		labels
	)

if __name__=='__main__':
	cifar_python_directory = os.path.abspath("/home/Downloads/datas/cifar-100-python")
	# path to the cifar-100-python format data (download from online)

    	#meta=unpickle(os.path.join(cifar_python_directory, 'meta'))
    	#fine_label_names=meta['fine_label_names']
    	#print(fine_label_names)

	print("Converting...")
	cifar_caffe_directory = os.path.abspath("cifar100_train_lmdb")
	if not os.path.exists(cifar_caffe_directory):
		X,  y_f  = load_data(os.path.join(cifar_python_directory, 'train'))
		Xt, yt_f = load_data(os.path.join(cifar_python_directory, 'test'))

		print("Data is fully loaded, now truly converting.")

		env = lmdb.open(cifar_caffe_directory, map_size=50000*1000*5)
		txn = env.begin(write=True)
		count = 0
		for i in range(X.shape[0]):
			datum = caffe.io.array_to_datum(X[i], y_f[i])
			str_id = '{:08}'.format(count)
			txn.put(str_id, datum.SerializeToString())

			count+=1
			if count%1000==0:
				print('already handled with {} pictures'.format(count))
				txn.commit()
				txn = env.begin(write=True)
		txn.commit()
		env.close()

		env = lmdb.open('cifar100_test_lmdb', map_size=10000*1000*5)
		txn = env.begin(write=True)
		count = 0
		for i in range(Xt.shape[0]):
			datum = caffe.io.array_to_datum(Xt[i], yt_f[i])
			str_id = '{:08}'.format(count)
			txn.put(str_id, datum.SerializeToString())

			count+=1
			if count%1000==0:
				print('already handled with {} pictures'.format(count))
				txn.commit()
				txn = env.begin(write=True)
		txn.commit()
		env.close()
	else:
		print("Conversion was already done. Did not convert twice.")

