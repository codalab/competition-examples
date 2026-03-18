import json
import os
import sys
import time

import numpy as np

input_dir = '/app/input_data/'
output_dir = '/app/output/'
program_dir = '/app/program'
submission_dir = '/app/ingested_program'

sys.path.append(program_dir)
sys.path.append(submission_dir)


def get_training_data():
    X_train = np.genfromtxt(os.path.join(input_dir, 'training_data'))
    y_train = np.genfromtxt(os.path.join(input_dir, 'training_label'))
    return X_train, y_train


def get_prediction_data():
    return np.genfromtxt(os.path.join(input_dir, 'testing_data'))


def print_line():
    print('-' * 10)


def main():
    from model import Model
    print('Reading Data')
    X_train, y_train = get_training_data()
    X_test = get_prediction_data()
    print_line()
    print('Starting')
    start = time.time()
    m = Model()
    print_line()
    print('Training Model')
    m.fit(X_train, y_train)
    print_line()
    print('Running Prediction')
    prediction = m.predict(X_test)
    duration = time.time() - start
    print_line()
    print(f'Completed Prediction. Total duration: {duration}')
    np.savetxt(os.path.join(output_dir, 'prediction'), prediction)
    with open(os.path.join(output_dir, 'metadata.json'), 'w+') as f:
        json.dump({'duration': duration}, f)
    print()
    print('Ingestion Program finished. Moving on to scoring')


if __name__ == '__main__':
    main()
