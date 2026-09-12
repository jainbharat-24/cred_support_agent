from fastmcp import FastMCP
from dataset import generate_dataset

# Initialize FastMCP server instance
mcp = FastMCP("CredSupportMCP")

# Load dataset for lookup
LOAN_APPLICATIONS = generate_dataset()

@mcp.tool()
def get_loan_status(record_id: str) -> str:
    """Check the status of a loan application via MCP tool protocol."""
    record = next((r for r in LOAN_APPLICATIONS if r["record_id"].lower() == record_id.lower()), None)
    if not record:
        return f"Error: Record ID {record_id} not found."
    return f"Record {record['record_id']} - Category: {record['category']}, Status: {record['status']}, Amount: INR {record['loan_amount_inr']}"

if __name__ == "__main__":
    print("Starting FastMCP Support Server...")
    mcp.run()