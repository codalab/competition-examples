import argparse
import os
from model import Model

import numpy as np


def get_training_data(input_dir):
    X_train = np.genfromtxt(os.path.join(input_dir, 'training_data'))
    y_train = np.genfromtxt(os.path.join(input_dir, 'training_label'))
    return X_train, y_train


def get_prediction_data(input_dir):
    return np.genfromtxt(os.path.join(input_dir, 'testing_data'))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir")
    parser.add_argument("output_dir")
    args = parser.parse_args()

    input_dir = args.input_dir
    output_dir = args.output_dir

    print('Reading Data')
    X_train, y_train = get_training_data(input_dir)
    X_test = get_prediction_data(input_dir)
    print('Starting')
    m = Model()
    print('Training Model')
    m.fit(X_train, y_train)
    print('Running Prediction')
    prediction = m.predict(X_test)
    np.savetxt(os.path.join(output_dir, 'prediction'), prediction)


if __name__ == '__main__':
    main()
