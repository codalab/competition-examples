import json
import sys
import subprocess
import timeit


# Default place codalab puts the output dir volume
sys.path.append("/app/output")
from solution import pisano_period


# To track memory we have to install a helper
print("Pip installing memory profiler")
subprocess.call(['pip', 'install', 'memory_profiler'])
from memory_profiler import memory_usage


print("Running pisano period functions...")


def test():
    assert pisano_period(1) == 0
    assert pisano_period(8) == 12
    assert pisano_period(5) == 20
    assert pisano_period(11) == 10
    assert pisano_period(4) == 6
    assert pisano_period(6) == 24
    assert pisano_period(7) == 16


# Scoring .. why not just run ingestion next to scoring program?! or just from scoring program!?
mem = memory_usage((test))[0]
cpu = timeit.timeit(test, number=10)

print("Got through all assertions just fine pops!")

with open("/app/output/ingestion_results.json", "w") as f:
    output = {
        "mem": mem,
        "cpu": cpu,
    }
    print(f"Writing ingestion_results output... {output}")
    f.write(json.dumps(output))
