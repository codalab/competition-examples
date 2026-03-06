# ------------------------------
# Dummy Model Submission
# This is a dummy model for the participants to understand the structure of the code i.e.
# - required functions in the Model class
# - inputs and outputs of the functions
# ------------------------------

class Model:
    """
    This is a model class to be submitted by the participants in their submission.

    This class should consists of the following functions
    1) init : 
        takes 2 arguments get_train_set and systematics. It can be used for intiializing variables, classifier etc.
    2) fit : 
        takes no arguments
        can be used to train a classifier
    3) predict: 
        takes 1 argument: test set
        can be used to get predictions of the test set.
        returns a dictionary

    Note:   Add more methods if needed e.g. save model, load pre-trained model etc.
            It is the participant's responsibility to make sure that the submission 
            class is named "Model" and that its constructor arguments remains the same.
            The ingestion program initializes the Model class and calls fit and predict methods

            When you add another file with the submission model e.g. a trained model to be loaded and used,
            load it in the following way:

            # get to the model directory (your submission directory)
            model_dir = os.path.dirname(os.path.abspath(__file__))

            your trained model file is now in model_dir, you can load it from here
    """

    def __init__(self, get_train_set=None, systematics=None):
        """
        Model class constructor

        Params:
            get_train_set (callable, optional): 
                A function that returns a dictionary with data, labels, weights, detailed_labels and settings.
            
            systematics (callable, optional): 
                A function that can be used to get a dataset with systematics added.
        

        Returns:
            None
        
        """
        pass

    def fit(self):
        """
        Params:
            None

        Functionality:
            This function can be used to train a model. You can ignore this function if you already have a pre-trained model. 

        Returns:
            None
        """
        pass

    def predict(self, test_set):
        """
        Params:
            test_set (dict): A dictionary containing the test data, and weights

        Functionality:
            this function can be used for predictions using the test sets

        Returns:
            dict: a dictionary with the following keyskeys
                - 'mu_hat': The predicted value of mu.
                - 'delta_mu_hat': The uncertainty in the predicted value of mu.
                - 'p16': The lower bound of the 16th percentile of mu.
                - 'p84': The upper bound of the 84th percentile of mu.

        """

        return {
            "mu_hat": 1,
            "delta_mu_hat": 0.1,
            "p16": 1.0,
            "p84": 1.0
        }
