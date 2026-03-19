import json

char_count = 0

with open("/app/input/solution.py", "r") as f:
    for c in f.read():
        char_count += 1

scores = json.loads(open("/app/input/ingestion_results.json", "r").read())

# We should now have ingestion_output["mem"] and ingestion_output["cpu"], add "char_count"

scores["char_count"] = char_count

# We need to write to /app/output/scores.json with our leaderboard columns and such
with open("/app/output/scores.json", "w") as f:
    print(f"Writing scores... {scores}")
    f.write(json.dumps(scores))
