system_prompt = """
Extract specific fields from a bank statement provided in an Excel file for a given date.

Follow these steps to parse the Excel file and extract the required data.

# Steps

1. **Open the Excel File**: Access the provided Excel file containing the bank statement.
2. **Identify the Date**: Locate the column that contains the transaction dates.
3. **Filter by Date**: Extract transactions that match the specified date.
4. **Extract Fields**: For each transaction, extract the necessary fields such as:
   - Transaction Date
   - Description
   - Amount
   - Balance
   - transfer
      -  transfer_type
      - source
      - destination

5. **Summarize**: Provide a concise summary of the extracted data if needed.
6. Based on the description if there is cIPS Fund Trf frm IPS E-PAYMENT in the description then the source field inside the transfer will be Connect IPS and the destination will be self as the amount is being transferred to our account.
Similary if there is Fund Trf to A/C PAYABLE IBFT and QR in the description then the source will be self and the destination will be shop name or person name mentioned in the at the end of the description.
Also if there is Cash Withdrawl  in the description the source will be self and destination will be Cash Withdrawal

Also in the transfer_type use QR , connect IPS or any appropriate type based on the description.
if the fund transfer has a person's name with the format Fund Trf to Person's name then the  category will be Personal.

If there is direct transfer to another personal bank account similar to Fund Trf to NABIL BANK LTD then use the category as PERSONAL.

In the category section based on the description use categories such as FOOD, ENTERTAINMENT, CLOTHES, TRANSPORTATION, INTERNET, PHONE, PERSONAL, OTHERS. Only use the category value from these options only.

Also the transaction_field should be an unique id which can be found in the description
# Output Format

Provide the extracted information in a structured format, preferably JSON:
- A JSON array where each transaction is an object with keys corresponding to the extracted fields.

Example JSON structure:
```json
[
    {
        "Transaction Date": "YYYY-MM-DD",
        "Description": "Sample Description",
        "Amount": "amount_value",
        "Balance": "balance_value"
        "Transaction Type": "Type of transaction debit or credit"

    }
]
```

# Notes

- Ensure that the date format in the output matches the standard format specified (YYYY-MM-DD).
- Handle discrepancies or errors in data entries gracefully, such as missing fields or incorrect formats.
- If the statement contains multiple transactions for the given date, include each one in the output.
"""


response_format = {
    "type": "json_schema",
    "json_schema": {
        "name": "transaction_schema",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "The date of the transaction.",
                },
                "description": {
                    "type": "string",
                    "description": "A description of the transaction.",
                },
                "type_of_transaction": {
                    "type": "string",
                    "description": "The type of transaction (e.g., debit, credit).",
                },
                "amount": {
                    "type": "number",
                    "description": "The amount involved in the transaction.",
                },
                "balance": {
                    "type": "number",
                    "description": "The account balance after the transaction.",
                },
                "category": {
                    "type": "string",
                    "description": "Category related to the transaction (Food, Entertainment, Clothes etc.)",
                },
                "transaction_id": {
                    "type": "string",
                    "description": "A unique transaction ID",
                },
                "transfer": {
                    "type": "object",
                    "description": "Details of the transfer if applicable.",
                    "properties": {
                        "transfer_type": {
                            "type": "string",
                            "description": "Type of transfer, QR, ATM or Internal",
                        },
                        "source": {
                            "type": "string",
                            "description": "The source account of the transfer.",
                        },
                        "destination": {
                            "type": "string",
                            "description": "The destination account of the transfer.",
                        },
                    },
                    "required": ["source", "destination", "transfer_type"],
                    "additionalProperties": False,
                },
            },
            "required": [
                "date",
                "description",
                "type_of_transaction",
                "amount",
                "balance",
                "transfer",
                "category",
                "transaction_id",
            ],
            "additionalProperties": False,
        },
    },
}
