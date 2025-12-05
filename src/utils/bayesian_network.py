class EnvironmentalBayesNet:
    """
    A Discrete Bayesian Network for Cardiac Environmental Stress.
    Calculates P(Stress | Temperature, Pollution)
    """
    
    def __init__(self):
        # Conditional Probability Table (CPT)
        # Key: (is_heatwave, is_polluted) -> Value: Probability of High Stress
        self.cpt_stress = {
            (True, True):   0.95,  # Worst case: Hot + Smog
            (True, False):  0.75,  # Hot only
            (False, True):  0.65,  # Smog only
            (False, False): 0.10   # Nice weather
        }

    def infer_stress_probability(self, temp, aqi):
        """
        Input: temp (Celsius), aqi (1-5 scale)
        Output: Probability of stress (0.0 to 1.0)
        """
        # Step 1: Discretize Evidence (Convert numbers to True/False states)
        # Thresholds: Temp > 30°C is Heatwave, AQI > 3 is Pollution
        is_heatwave = temp > 30.0
        is_polluted = aqi > 3      
        
        # Step 2: Bayesian Inference (Lookup)
        p_stress = self.cpt_stress.get((is_heatwave, is_polluted))
        
        return {
            "p_stress": p_stress,
            "evidence": {
                "is_heatwave": is_heatwave,
                "is_polluted": is_polluted
            }
        }

# Quick Test Block
if __name__ == "__main__":
    net = EnvironmentalBayesNet()
    # Test a hot, polluted day
    print(net.infer_stress_probability(35, 5))