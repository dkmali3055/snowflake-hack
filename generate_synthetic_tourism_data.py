import pandas as pd
import random
import numpy as np

random.seed(42)
np.random.seed(42)

# --- Table 1: cultural_routes ---
route_ids = list(range(1, 11))  # 10 routes

route_names = [
    "Heritage Trail",
    "Spice Route",
    "Temple Odyssey",
    "Folk Art Journey",
    "Classical Dance Path",
    "Handicraft Circuit",
    "Sacred Rivers Route",
    "Mountain Monuments Trail",
    "Coastal Culture Loop",
    "Desert Caravan Route"
]

states_list = [
    "Rajasthan", "Kerala", "Uttar Pradesh", "Gujarat", "Maharashtra",
    "Tamil Nadu", "Karnataka", "Madhya Pradesh", "Odisha", "West Bengal",
    "Punjab", "Bihar", "Haryana", "Assam", "Chhattisgarh",
    "Jharkhand", "Himachal Pradesh", "Telangana", "Andhra Pradesh", "Goa"
]

art_forms_list = [
    "Kathakali", "Madhubani Painting", "Warli Art", "Bharatanatyam", 
    "Kalaripayattu", "Pattachitra", "Odissi Dance", "Folk Music", 
    "Carpet Weaving", "Block Printing"
]

def random_subset(lst, min_len=2, max_len=5):
    length = random.randint(min_len, max_len)
    return random.sample(lst, length)

cultural_routes_data = []
for route_id, name in zip(route_ids, route_names):
    states_involved = random_subset(states_list, 2, 5)
    art_forms = random_subset(art_forms_list, 1, 3)
    description = (
        f"A cultural route passing through {', '.join(states_involved)} "
        f"showcasing art forms like {', '.join(art_forms)}."
    )
    cultural_routes_data.append({
        "route_id": route_id,
        "name": name,
        "states_involved": "|".join(states_involved),  # pipe-separated list
        "art_forms": "|".join(art_forms),  # pipe-separated list
        "description": description
    })

df_routes = pd.DataFrame(cultural_routes_data)

# --- Table 2: tourism_stats ---
regions = states_list  # reuse states as regions
years = list(range(2014, 2024))  # 10 years

tourism_stats_data = []
for region in regions:
    base_visitors = random.randint(500_000, 15_000_000)
    for year in years:
        # simulate some year-over-year variation (+/- 15%)
        variation = random.uniform(0.85, 1.15)
        visitor_count = int(base_visitors * variation)
        tourism_stats_data.append({
            "region": region,
            "year": year,
            "visitor_count": visitor_count
        })

df_tourism = pd.DataFrame(tourism_stats_data)

# --- Table 3: geo_data ---
districts = [
    "Jaipur", "Thiruvananthapuram", "Lucknow", "Ahmedabad", "Mumbai",
    "Chennai", "Bengaluru", "Bhopal", "Bhubaneswar", "Kolkata",
    "Amritsar", "Patna", "Chandigarh", "Guwahati", "Raipur",
    "Ranchi", "Shimla", "Hyderabad", "Visakhapatnam", "Panaji"
]

# Approximate latitudes and longitudes (randomized a bit around city center)
base_coords = {
    "Jaipur": (26.9124, 75.7873),
    "Thiruvananthapuram": (8.5241, 76.9366),
    "Lucknow": (26.8467, 80.9462),
    "Ahmedabad": (23.0225, 72.5714),
    "Mumbai": (19.0760, 72.8777),
    "Chennai": (13.0827, 80.2707),
    "Bengaluru": (12.9716, 77.5946),
    "Bhopal": (23.2599, 77.4126),
    "Bhubaneswar": (20.2961, 85.8245),
    "Kolkata": (22.5726, 88.3639),
    "Amritsar": (31.6340, 74.8723),
    "Patna": (25.5941, 85.1376),
    "Chandigarh": (30.7333, 76.7794),
    "Guwahati": (26.1445, 91.7362),
    "Raipur": (21.2514, 81.6296),
    "Ranchi": (23.3441, 85.3096),
    "Shimla": (31.1048, 77.1734),
    "Hyderabad": (17.3850, 78.4867),
    "Visakhapatnam": (17.6868, 83.2185),
    "Panaji": (15.4909, 73.8278)
}

geo_data_list = []
for district in districts:
    lat, lon = base_coords[district]
    # add small random noise to simulate district variations
    lat += np.random.uniform(-0.05, 0.05)
    lon += np.random.uniform(-0.05, 0.05)
    geo_data_list.append({
        "district": district,
        "latitude": round(lat, 6),
        "longitude": round(lon, 6)
    })

df_geo = pd.DataFrame(geo_data_list)

# Save CSV files
df_routes.to_csv("cultural_routes.csv", index=False)
df_tourism.to_csv("tourism_stats.csv", index=False)
df_geo.to_csv("geo_data.csv", index=False)

print("✅ Generated CSVs: cultural_routes.csv, tourism_stats.csv, geo_data.csv")
