import json

def load_plans():
        """Load carrier plans from JSON file."""
        try:
            with open('data/plans.json', 'r') as f:
                plans = json.load(f)
                return plans
        except Exception as e:
            raise Exception(f"Error loading carrier plans: {str(e)}")

def recommend_plan(num_lines, premium_data_needed, apple_tv_netflix, upgrade_ready, hulu_ads):
    plans = load_plans()
    valid_plans = [plan for plan in plans if (plan["premium_data"] >= premium_data_needed or plan["premium_data"] == "Unlimited") and
                   (plan["apple_tv_netflix"] == apple_tv_netflix) and
                   (plan["upgrade_ready"] == upgrade_ready) and
                   (plan["hulu_ads"] == hulu_ads) and
                   (plan["prices"][num_lines - 1] is not None)]
    
    if not valid_plans:
        unlimited_plans = [plan for plan in plans if plan["premium_data"] == "Unlimited" and plan["hulu_ads"] == hulu_ads and plan["prices"][num_lines - 1] is not None]
        if unlimited_plans:
            cheapest_plan = min(unlimited_plans, key=lambda x: x["prices"][num_lines - 1])
            return f"The cheapest unlimited data plan for {num_lines} line(s) is: {cheapest_plan['name']} for ${cheapest_plan['prices'][num_lines - 1]}"
        return "No suitable plan found."
    
    cheapest_plan = min(valid_plans, key=lambda x: x["prices"][num_lines - 1])
    return f"The cheapest suitable plan for {num_lines} line(s) is: {cheapest_plan['name']} for ${cheapest_plan['prices'][num_lines - 1]}"
