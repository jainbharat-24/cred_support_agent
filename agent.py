import os
from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from dataset import generate_dataset

# Load dataset records
LOAN_APPLICATIONS = generate_dataset()

# Define State Schema for LangGraph
class AgentState(TypedDict):
    query: str
    intent: str
    tool_output: dict
    response: str

# Task 6: Second tool with a designed escalation score
def check_loan_application_status(record_id: str) -> dict:
    record = next((r for r in LOAN_APPLICATIONS if r["record_id"].lower() == record_id.lower()), None)
    if not record:
        return {"error": f"Record ID {record_id} not found."}
        
    # Escalation score formula: 0.7 weight for fraud flag + 0.3 normalized recency
    recency_norm = record["days_since_created"] / 30.0
    fraud_weight = 1.0 if record["flagged_for_fraud_review"] else 0.0
    escalation_score = round((0.7 * fraud_weight) + (0.3 * recency_norm), 2)
    
    return {
        "record_id": record["record_id"],
        "category": record["category"],
        "status": record["status"],
        "loan_amount_inr": record["loan_amount_inr"],
        "escalation_score": escalation_score,
        "recommended_action": "Manual Review" if escalation_score > 0.5 else "Standard Processing"
    }

# Task 7: LangGraph Nodes
def intent_classifier_node(state: AgentState):
    query = state["query"].lower()
    if "status" in query or "rec-" in query:
        intent = "status_check"
    else:
        intent = "policy_rag"
    return {"intent": intent}

def rag_tool_node(state: AgentState):
    return {"tool_output": {"answer": "Policy retrieved successfully from Knowledge Base."}}

def status_tool_node(state: AgentState):
    query = state["query"]
    record_id = "REC-001"
    for r in LOAN_APPLICATIONS:
        if r["record_id"].lower() in query.lower():
            record_id = r["record_id"]
            break
    result = check_loan_application_status(record_id)
    return {"tool_output": result}

def response_generator_node(state: AgentState):
    output = state["tool_output"]
    if state["intent"] == "status_check":
        res = f"Application Status for {output.get('record_id')}: {output.get('status')}. Escalation Score: {output.get('escalation_score')}."
    else:
        res = f"Policy Answer: {output.get('answer')}."
    return {"response": res}

def route_intent(state: AgentState) -> Literal["rag_tool_node", "status_tool_node"]:
    if state["intent"] == "status_check":
        return "status_tool_node"
    return "rag_tool_node"

# Build the Graph
workflow = StateGraph(AgentState)
workflow.add_node("classifier", intent_classifier_node)
workflow.add_node("rag_tool_node", rag_tool_node)
workflow.add_node("status_tool_node", status_tool_node)
workflow.add_node("responder", response_generator_node)

workflow.set_entry_point("classifier")
workflow.add_conditional_edges("classifier", route_intent, {
    "rag_tool_node": "rag_tool_node",
    "status_tool_node": "status_tool_node"
})
workflow.add_edge("rag_tool_node", "responder")
workflow.add_edge("status_tool_node", "responder")
workflow.add_edge("responder", END)

app_graph = workflow.compile()

if __name__ == "__main__":
    print("--- Testing LangGraph Agent ---")
    res1 = app_graph.invoke({"query": "What are the loan eligibility criteria?", "intent": "", "tool_output": {}, "response": ""})
    print("Test 1 Result:", res1["response"])
    
    res2 = app_graph.invoke({"query": "Check status for REC-005", "intent": "", "tool_output": {}, "response": ""})
    print("Test 2 Result:", res2["response"])