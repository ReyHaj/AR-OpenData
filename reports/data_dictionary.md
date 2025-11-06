# Data Dictionary
| Column | Type | Description | Example | Notes |
|-------|------|-------------|---------|-------|
| ARID | string/int | Unique invoice id | AR-1001 | |
| Customer | string | Customer name | Acme Corp | |
| InvoiceDate | date | Invoice issue date | 2025-01-15 | yyyy-mm-dd |
| DueDate | date | Due date | 2025-02-14 | |
| ReceivedDate | date | Payment received date | 2025-02-10 | may be blank |
| Amount | float | Invoice amount | 1250.00 | currency per file |
| Currency | string | Currency code | USD | |
| Status | string | Payment status | Paid/Unpaid/Partial | |
| Terms | string | Payment terms | Net 30 | |
