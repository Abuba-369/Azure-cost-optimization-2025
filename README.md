# Azure-cost-optimization-2025

**Problem:**

2M+ Cosmos DB records (~600 GB, each ~300 KB).
Read-heavy, but records older than 90 days are rarely accessed.
Costs are increasing due to storage and RU consumption.


**Proposed Solution**

Hot Data (3 months) → Keep in Cosmos DB Hot Container.
Cold Data (older than 3 months) → Move to Azure Blob Storage (Cool tier).


**Migration Process (Zero Downtime, No Data Loss)**

1. Identify old records (>90 days).
2. Compress & upload to Blob Storage.
3. Delete from Hot Container.

**Benefits**

1. Drastically reduce Cosmos DB storage size & costs.
2. Blob Cool tier is much cheaper for infrequently accessed data.
3. No API changes — client apps work as-is.
4. Fast cold reads — still within seconds

<img width="1024" height="1536" alt="image" src="https://github.com/user-attachments/assets/3d0c6d65-0902-4923-baf0-efeb8e0c4820" />
