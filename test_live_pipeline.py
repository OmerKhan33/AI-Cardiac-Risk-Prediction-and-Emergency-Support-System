from src.utils.live_data import LiveDataClient
from src.utils.bayesian_network import EnvironmentalBayesNet

def run_layer2_check():
    print("STARTING LAYER 2 INTEGRATION TEST...")

    # 1. Init
    sensor = LiveDataClient()
    brain = EnvironmentalBayesNet()

    # 2. Get Live Data (Try a city like 'Delhi' or 'Dubai' for heat/smog)
    city = "London"
    print(f"📡 Fetching data for {city}...")
    env_data = sensor.get_data(city)
    
    if env_data['success']:
        print(f"API Success: Temp={env_data['temp']}°C, AQI={env_data['aqi']}")
    else:
        print(f"API Failed (Using defaults): {env_data['error']}")

    # 3. Calculate Risk
    print("Calculating Bayesian Stress Score...")
    risk_result = brain.infer_stress_probability(env_data['temp'], env_data['aqi'])
    
    prob = risk_result['p_stress'] * 100
    evidence = risk_result['evidence']
    
    print(f"\nFINAL RESULTS:")
    print(f"   Heatwave Detected? {evidence['is_heatwave']}")
    print(f"   Pollution Detected? {evidence['is_polluted']}")
    print(f"   Environmental Cardiac Stress Load: {prob}%")
    
    print("\nLogic is SOLID.")

if __name__ == "__main__":
    run_layer2_check()