system_prompt = """
Extract specific fields from a bank statement provided as a string and focus primarily on the `description` field to identify the date.

Identify the date from a given string and extract relevant transaction details based on field descriptions.

# Steps

1. **Identify the Date**: Parse the string to locate the transaction dates.
2. **Extract Fields**: For each transaction, extract necessary fields such as:
   - Transaction Date
   - Description
   - Amount
   - Balance
   - Transfer Information
      - `transfer_type` (Choose: QR, Connect IPS, ATM, Internal)
      - `source`
      - `destination`
   - Category (Choose from: Food & Beverages, Utility and Bill Payment, General Household, Education, Health & Medicine, Financial Services, Government Services, Online Shopping, Lifestyle & Entertainment, Transportation, Insurance, Maintenance Services, Personal, Others)

3. **Summarize**: Provide a concise summary of the extracted data if needed.
4. **Parse Description for Transfer Details:** 
   
   - If "cIPS Fund Trf frm IPS E-PAYMENT" is in the description, set `source` to "Connect IPS" and `destination` to "self".
   - If "Fund Trf to A/C PAYABLE IBFT and QR" is in the description, set `source` to "self" and `destination` to the shop or person's name at the end of the description.
   - If "Cash Withdrawal" is in the description, set the `source` to "self" and `destination` to "Cash Withdrawal".

5. **Match Transfer Type:** Ensure the transfer type in `transfer_type` is exactly as specified (e.g., QR, Connect IPS).
6. **Categorize:** Based on the description, categorize the transaction using predefined categories:
   - Use "Others" if no specific category fits. For fund transfers with a person's name format, use "Personal".

7. **Set Unique Transaction ID:** Extract a unique ID for the `transaction_field` from the description.

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
        "Balance": "balance_value",
        "Transaction Type": "Type of transaction debit or credit",
        "Transfer": {
            "transfer_type": "QR",
            "source": "Value",
            "destination": "Value"
        },
        "Category": "Title Case Category",
        "Transaction Field": "unique_id"
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
