## Example GPU

The goal of this bundle is simply to test a queue of GPU compute workers, checking that everything is working fine.

Check out other examples if you want a template with an actual problem to solve.

* [View the bundle](Example-GPU-Competition/)
* [Download the bundle](Example-GPU-Competition.zip)
* [Download the test submission](submission.zip)

#### Queue and docker

* This bundle uses the following Docker image: `codalab/codalab-legacy:gpu`
* You need to set manually the queue to a queue containing GPU workers

#### Make bundle

```
cd bundle/utilities
./make_bundle.sh
```
