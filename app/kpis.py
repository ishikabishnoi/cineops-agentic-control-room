def get_schedule_kpis(data):
    scheduled = sum(r["scenes_scheduled"] for r in data)
    completed = sum(r["scenes_completed"] for r in data)

    completion_rate = round((completed / scheduled) * 100, 1) if scheduled else 0
    delay_percent = round(100 - completion_rate, 1)

    latest_days_remaining = data[0]["days_remaining"] if data else None

    return {
        "scheduled_scenes": scheduled,
        "completed_scenes": completed,
        "completion_rate": completion_rate,
        "delay_percent": delay_percent,
        "days_remaining": latest_days_remaining
    }




def get_budget_kpis(data):
     
     variances = [r["budget_variance_percent"] for r in data if r["budget_variance_percent"] 
                  is not None] 
     
     avg_variance = round(sum(variances) / len(variances), 1) if variances else 0 

     max_variance = round(max(variances), 1) if variances else 0 

     return { "average_variance_percent": avg_variance,
              "max_variance_percent": max_variance,
              "records_analyzed": len(variances)
                  }
# sample = {"scheduled_scenes": 120, 
#           "completed_scenes": 98,
#           "planned_budget": 100000,
#           "actual_budget": 104200 }
# print(get_schedule_kpis(sample))
# print(get_budget_kpis(sample))       #wrote this for temporary testing 




def detect_primary_constraint(schedule_kpis, budget_kpis):
    time_score = 0
    budget_score = 0

    # Schedule pressure
    if schedule_kpis["completion_rate"] < 80:
        time_score += 2

    if schedule_kpis["delay_percent"] > 20:
        time_score += 2

    if schedule_kpis.get("days_remaining") is not None: 
        if schedule_kpis["days_remaining"] <= 7: time_score += 2
        elif schedule_kpis["days_remaining"] <= 14: time_score += 1

    # Budget pressure
    if budget_kpis["average_variance_percent"] > 5:
        budget_score += 2

    if budget_kpis["max_variance_percent"] > 20:
        budget_score += 1

    if time_score > budget_score:
        return "SCHEDULE", time_score, budget_score
    elif budget_score > time_score:
        return "BUDGET", time_score, budget_score
    else:
        return "BALANCED", time_score, budget_score