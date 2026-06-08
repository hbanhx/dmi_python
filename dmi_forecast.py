import requests
import json

# Aarhus 2m temperature endpoint
url = "https://opendataapi.dmi.dk/v1/forecastedr/collections/harmonie_dini_sf/position?coords=POINT(10.2039 56.1629)&crs=crs84&parameter-name=temperature-2m"

r = requests.get(url)
data = r.json()
print(f"Status code: {r.status_code}")


# Navigate into the CoverageJSON structure
values = data["domain"]["axes"]["t"]["values"]
temps_k = data["ranges"]["temperature-2m"]["values"]

# Convert Kelvin → Celsius
temps_c = [t - 273.15 for t in temps_k]

print("Aarhus hourly 2m temperature forecast:\n")
for t, temp_k, temp_c in zip(values, temps_k, temps_c):
    print(f"{t}: {temp_k:.2f} K, which is {temp_c:.2f} °C - rounded: {round(temp_c, 0)} °C")

# Pair timestamps with Celsius values
temp_obs_forecast = list(zip(values, temps_c))
print(f"Total forecast temperature observations: {len(temp_obs_forecast)}")

# Save as JSONL
with open("clean_features_forecast.txt", "w") as f:
    for feature in temp_obs_forecast:
        f.write(json.dumps(feature) + "\n")
