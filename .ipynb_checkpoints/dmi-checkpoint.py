import requests
import json

base_url = "https://opendataapi.dmi.dk/v2/metObs/collections/observation/items?stationId=06031&datetime=2026-01-07T00:00:00%2B02:00/.."
# {"error":"Bad Request","message":"Offset cannot be greater than 500000, it was set to: 501000","status":400}

all_features = []
next_url = base_url

while next_url:
    print(f"Fetching: {next_url}")
    r = requests.get(next_url)
    print(f"Status code: {r.status_code}")

    data = r.json()

    # Add features from this page
    features = data.get("features", [])
    all_features.extend(features)
    print(f"Length of all_features: {len(all_features)}")

    # Find the next link
    next_url = None
    for link in data.get("links", []):
        if link.get("rel") == "next":
            next_url = link.get("href")
            print(f"Next URL: {next_url}")
            break

print(f"Total features fetched: {len(all_features)}")

# ---- Extract parameters ----
params = {f["properties"]["parameterId"] for f in all_features}
print(params)
print(f"Number of parameters: {len(params)}")

# ---- Extract temp_dry and obs_date ----
temp_dry, obs_date, stat_id = [], [], []
for feature in all_features:
    props = feature["properties"]
    if props["parameterId"] == "temp_dry":
        temp_dry.append(props["value"])
        obs_date.append(props["observed"])
        stat_id.append(props["stationId"])
        print(props)

temp_obs = list(zip(temp_dry, obs_date, stat_id))
# print(temp_obs)
# print(f"Total temperature observations: {len(temp_obs)}, since min(obs_date)={min(obs_date)}, max(obs_date)={max(obs_date)}")

# ---- Save all features ----
with open("clean_features_all.txt", "w") as f:
    for feature in all_features:
        f.write(json.dumps(feature) + "\n")

# ---- Save temp_dry observations ----
with open("clean_features_temp_dry_all.txt", "w") as f:
    for temp_ob in temp_obs:
        f.write(json.dumps(temp_ob) + "\n")
        print(temp_ob)


print(f"Total temperature observations: {len(temp_obs)}, between {min(obs_date)} and {max(obs_date)}")