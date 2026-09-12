import random
from typing import Dict, List

CATEGORIES = ['Personal Loan', 'Home Loan', 'Auto Loan', 'Education Loan', 'Business Loan']
STATUSES = ['Submitted', 'Under Review', 'Approved', 'Rejected', 'Disbursed']

def generate_dataset(seed: int = 42, target_count: int = 45) -> List[Dict]:
    random.seed(seed)
    dataset = []
    
    # Ensure baseline coverage for every category and status combination
    for cat in CATEGORIES:
        for status in STATUSES:
            dataset.append({
                "record_id": f"REC-{len(dataset)+1:03d}",
                "category": cat,
                "status": status,
                "loan_amount_inr": random.choice([150000, 500000, 1200000, 2500000, 5000000]),
                "days_since_created": random.randint(0, 30),
                "flagged_for_fraud_review": random.random() < 0.20
            })
            
    return dataset[:target_count]

if __name__ == "__main__":
    LOAN_APPLICATIONS = generate_dataset()
    print(f"Generated {len(LOAN_APPLICATIONS)} records successfully.")
    
    # Validation report
    cat_counts = {cat: sum(1 for r in LOAN_APPLICATIONS if r["category"] == cat) for cat in CATEGORIES}
    status_counts = {st: sum(1 for r in LOAN_APPLICATIONS if r["status"] == st) for st in STATUSES}
    fraud_count = sum(1 for r in LOAN_APPLICATIONS if r["flagged_for_fraud_review"])
    fraud_pct = (fraud_count / len(LOAN_APPLICATIONS)) * 100
    
    print("\n--- Dataset Validation Report ---")
    print("Category Counts:", cat_counts)
    print("Status Counts:", status_counts)
    print(f"Fraud Review Flagged Percentage: {fraud_pct:.2f}% (Target: 10% - 30%)")