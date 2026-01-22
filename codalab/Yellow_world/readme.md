YELLOW WORLD
============

## Hello World competition

This is a very simple example of competition with result submission (and how to turn it into a code submission challenge by adding an ingestion program). 
* [View the competition bundle](https://github.com/codalab/competition-examples/tree/master/codalab/Yellow_world)
* [Download the competition bundle](https://github.com/codalab/competition-examples/blob/master/codalab/Yellow_world/yellow_world_competition_bundle.zip)
* [Download the sample submission](https://github.com/codalab/competition-examples/blob/master/codalab/Yellow_world/yellow_world_sample_submission.zip)


## Result submission

This example competition looks for submissions with "Hello World!"
It is the most basic example of Codalab competitions with RESULT submission.
In this example, users select the submission shown on the leaderboard.
This example is based on the original "Hello World" example competition of Codalab and was modified and checked for version 1.5.

NOTE: we provide the zipped and unzipped competition bundle for convenience. In the competition bundle, subdirectories should be zipped files (e.g scoring _program).

## Code submission

We give an example of how code can be submitted using an ingestion program:
* upload ingestion_program.zip to My Competitions>My datasets>Create dataset (choose type: ingestion program)
* go to the editor and uncheck "Results Scoring Only", then select in the ingestion program menu the ingestion program you just uloaded.
* submit the sample code: submission_4_ingestion.zip

For another example of code submission, see the [Compute Pi](https://github.com/codalab/competition-examples/tree/master/codalab/Compute_pi) competition.

## Competition bundle

The competition bundle contains the following files:
```
reference_data.zip	    The solution to the problem
scoring_program.zip	    The program evaluating the solution
logo.jpg                    The logo
competition.yaml            The YAML configuration file
data.html	            HTML documentation pages	
evaluation.html		
overview.html	
terms_and_conditions.html
```

The [YAML file is the configuration file](https://github.com/codalab/competition-examples/blob/master/basic-competition-bundles/Yellow_world/yellow_world_competition_bundle/competition.yaml). It consist in a number of `attribute: value` pairs. For a full list of attributes, see the [Codalab competition YAML definition language](https://github.com/codalab/codalab-competitions/wiki/Organizer_Codalab-competition-YAML-definition-language).

1. **First section**: general settings and HTML pages
```
title: Example Hello World Competition
description: An example competition where submissions should output "Hello World!"
image: logo.jpg
has_registration: True
html:
    overview: overview.html
    evaluation: evaluation.html
    terms: terms_and_conditions.html
    data: data.html
```
2. **Section section**: phases (only 1 phase in this example)
```
phases:
    1:
        phasenumber: 1
        label: "First phase"
        start_date: 2013-06-30
        max_submissions: 100
        scoring_program: scoring_program.zip
        reference_data: reference_data.zip
```
3. **Third section**: leaderboard configuration
```
leaderboard:
    leaderboards:
        RESULTS: &RESULTS
            label: Results
            rank: 1
    columns:
        correct:
            leaderboard: *RESULTS
            label: correct
            rank: 1
            numeric_format: 1
```
In this case, the scoring program writes a file `scores.txt` containing:
```
correct:1
```
for the sample submission.

### Building a scoring program

This example uses Python 2.7.

`evaluate.py` - is an example that checks that the submission data matches the truth data, which is "Hello World!"

`metadata` - this is a file that instructs Codalab to execute evaluate.py.

Once these pieces are assembled they are packaged as program.zip which CodaLab can then use to evaluate the submissions for a competition.

### Building an ingestion program

To turn this result submission competition into a code submission competition, we give an example of [Ingestion Program](https://github.com/codalab/codalab/wiki/User_Building-an-Ingestion-Program-for-a-Competition).

WARNING: Code submission may result in a lot of computational load on our servers. Before doing that [contact us](mailto:codalab@chalearn.org) or learn how to [set up your own compute workers](https://github.com/codalab/codalab-competitions/wiki/User_Using-your-own-compute-workers).

* Download the example of [ingestion program](https://github.com/codalab/competition-examples/tree/master/basic-competition-bundles/Yellow_world/ingestion_program)
* Upload ingestion_program.zip to My Competitions>My datasets>Create dataset (choose type: ingestion program)
go to the editor and uncheck "Results Scoring Only", then select in the ingestion program menu the ingestion program you just uloaded.
* submit the sample code: submission_4_ingestion.zip

For another example of code submission without ingestion program, see the [Compute Pi competition](Example_compute_pi).
