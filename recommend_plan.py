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
    valid_plans = []

    for plan in plans:
        # Check if plan has required number of lines
        if plan["prices"][num_lines - 1] is None:
            continue

        # Handle data comparison
        data_requirement_met = (
            plan["premium_data"] == "Unlimited" or
            (isinstance(plan["premium_data"], (int, float)) and plan["premium_data"] >= premium_data_needed)
        )

        # Check all conditions
        if (data_requirement_met and
            plan["apple_tv_netflix"] == apple_tv_netflix and
            plan["upgrade_ready"] == upgrade_ready and
            plan["hulu_ads"] == hulu_ads):
            valid_plans.append(plan)

    if not valid_plans:
        # Try finding unlimited plans if no valid plans found
        unlimited_plans = [
            plan for plan in plans 
            if plan["premium_data"] == "Unlimited" and 
            plan["hulu_ads"] == hulu_ads and 
            plan["prices"][num_lines - 1] is not None
        ]
        if unlimited_plans:
            cheapest_plan = min(unlimited_plans, key=lambda x: x["prices"][num_lines - 1])
            return f"The cheapest unlimited data plan for {num_lines} line(s) is: {cheapest_plan['name']} for ${cheapest_plan['prices'][num_lines - 1]}"
        return "No suitable plan found."

    cheapest_plan = min(valid_plans, key=lambda x: x["prices"][num_lines - 1])
    return f"The cheapest suitable plan for {num_lines} line(s) is: {cheapest_plan['name']} for ${cheapest_plan['prices'][num_lines - 1]}"