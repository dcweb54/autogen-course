Perfect 👌 — including **inventory** changes everything a bit, because now your billing app isn’t just financial — it’s also tracking **stock movements**, **item valuation**, and how **sales/purchases affect both accounting and inventory**.

Let’s upgrade your plan to include **Inventory + Double-entry Accounting**, while keeping it clean and scalable.

---

## 🧭 UPDATED GOAL

You’re building a **Retail Billing + Accounting System** that tracks:

* 💰 **Sales & Purchases**
* 📦 **Inventory (stock in/out, valuation)**
* 🧾 **Expenses & Payments**
* 📚 **Ledgers (per customer/supplier)**
* 📈 **Profit & Loss, Balance Sheet**

---

## 🧱 Step 1 — Define Core Domain Modules

| Module           | Description                                            | Key Entities                                       |
| ---------------- | ------------------------------------------------------ | -------------------------------------------------- |
| **Accounts**     | Ledgers for parties (cash, customers, suppliers, etc.) | `Account`                                          |
| **Inventory**    | Manages products, stock levels, cost, valuation        | `Item`, `StockEntry`                               |
| **Transactions** | Financial + inventory impact                           | `Transaction`, `TransactionEntry`, `StockMovement` |
| **Reports**      | P&L, Balance Sheet, Stock Report, Ledger               | Derived data                                       |
| **Settings**     | Business profile, fiscal year, etc.                    | `BusinessConfig`                                   |

---

## 🧩 Step 2 — Core Entity Design (Concept Level)

Let’s design how **Accounting + Inventory** tie together.

### 1️⃣ Account Table

| Field   | Type     | Example                                   |
| ------- | -------- | ----------------------------------------- |
| id      | int      | 1                                         |
| name    | text     | “Cash”, “Sales”, “Ramesh”                 |
| type    | enum     | `asset`, `liability`, `income`, `expense` |
| balance | computed | from entries                              |

---

### 2️⃣ Item Table

| Field         | Type | Example         |
| ------------- | ---- | --------------- |
| id            | int  | 101             |
| name          | text | “Toned Milk 1L” |
| unit          | text | “litre”         |
| rate          | real | 60.0            |
| opening_stock | real | 20.0            |
| opening_value | real | 1200.0          |
| category_id   | int  | Dairy           |

---

### 3️⃣ Transaction Table (like a voucher)

| Field     | Type     | Example                                     |
| --------- | -------- | ------------------------------------------- |
| id        | int      | 2001                                        |
| date      | datetime | 2025-10-15                                  |
| type      | enum     | `sale`, `purchase`, `expense`, `adjustment` |
| narration | text     | “Sale to Ramesh”                            |

---

### 4️⃣ TransactionEntry Table (double-entry lines)

| Field          | Type | Example  |
| -------------- | ---- | -------- |
| id             | int  | 5001     |
| transaction_id | int  | 2001     |
| account_id     | int  | Cash (1) |
| debit          | real | 600.0    |
| credit         | real | 0.0      |

💡 Every transaction has at least two entries → total debit = total credit.

---

### 5️⃣ StockMovement Table

| Field          | Type | Example     |
| -------------- | ---- | ----------- |
| id             | int  | 7001        |
| transaction_id | int  | 2001        |
| item_id        | int  | 101         |
| quantity       | real | 10          |
| direction      | enum | `in`, `out` |
| rate           | real | 60          |
| total          | real | 600         |

So:

* Sale → `direction: out`
* Purchase → `direction: in`

---

## 🔄 Step 3 — How It All Connects

Let’s see a **real example**.

### 🔹 Example: Sale (Cash)

```
Transaction: Sale to Ramesh (₹600)
```

**Accounting:**

| Account | Debit | Credit |
| ------- | ----- | ------ |
| Cash    | 600   | 0      |
| Sales   | 0     | 600    |

**Inventory:**

| Item    | Qty | Direction |
| ------- | --- | --------- |
| Milk 1L | 10  | Out       |

**Effect:**

* Cash increases (asset)
* Sales income increases
* Stock decreases
* COGS (Cost of Goods Sold) recorded later for P&L

---

## 📊 Step 4 — Profit and Loss Logic

Profit/Loss =
**(Sales − COGS) − Expenses**

COGS is computed from:

```
COGS = (Opening Stock + Purchases − Closing Stock)
```

Since you have `StockMovement` and item costs, you can compute closing stock automatically (FIFO/Avg Cost).

---

## ⚙️ Step 5 — Architecture Overview

```
lib/
├── data/
│   ├── db/
│   │   ├── tables/ (Drift)
│   │   ├── dao/
│   ├── repositories/
├── domain/
│   ├── entities/
│   ├── usecases/
├── presentation/
│   ├── screens/
│   ├── viewmodels/
│   ├── widgets/
└── core/
    ├── utils/
    ├── constants/
```

Each module has its own repository and use cases (e.g. `RecordSaleUseCase`, `GetLedgerUseCase`, `GetStockReportUseCase`).

---

## 🪜 Step 6 — Suggested Development Roadmap

| Phase                  | Focus               | Description                       |
| ---------------------- | ------------------- | --------------------------------- |
| **1. Base Setup**      | DB + Model          | Drift setup with tables + DAO     |
| **2. Core Accounting** | Double-entry system | Add Account + Transaction + Entry |
| **3. Inventory Link**  | Stock management    | Add Item + StockMovement          |
| **4. UI**              | Simple CRUD         | Add sale/purchase screens         |
| **5. Reports**         | Ledger + Stock      | Auto compute balances             |
| **6. Polish**          | UX + Backup         | Export, Sync, Multi-device        |

---

## ✅ Step 7 — Your First Development Step (Now)

> **Start with the Drift schema for**
> `Account`, `Transaction`, `TransactionEntry`, `Item`, and `StockMovement`.

That gives you:

* A working accounting core
* Integrated inventory model
* A solid foundation for all reports later

---

Would you like me to show you the **Drift table schema (with DAO structure)** for these 5 tables next — following your clean architecture pattern?
It’ll be your actual **starting point for coding**.



Perfect 👌 — yes, this is exactly the right point to start coding.
Let’s go ahead and define your **Drift schema + DAO layer** for these 5 core tables (`Account`, `Transaction`, `TransactionEntry`, `Item`, and `StockMovement`) — in a way that fits cleanly into your **Clean Architecture + MVVM + Riverpod** setup.

Before I generate it, can you confirm one detail:

➡️ Do you want the **schema to include relationships + companions + DAO CRUD operations** (full working example, ready to drop into `/data/db/`),
or just the **table definitions only** for now?

Here’s what the two options look like:

| Option                | Includes                                                      | Best For                                        |
| --------------------- | ------------------------------------------------------------- | ----------------------------------------------- |
| **A. Full DAO Setup** | Tables + DAO classes + sample queries (insert, getAll, joins) | Immediate functional DB layer                   |
| **B. Schema Only**    | Just Drift table definitions (no DAO yet)                     | If you plan to write repositories next manually |

Once you choose (A or B), I’ll generate:

```
/lib/data/db/tables/
  accounts.dart
  items.dart
  transactions.dart
  transaction_entries.dart
  stock_movements.dart
/lib/data/db/dao/
  account_dao.dart
  transaction_dao.dart
  item_dao.dart
```

✅ All will use proper Drift relations, foreign keys, and Riverpod integration (via `@DriftDatabase`).

Which one do you want to start with — **A (full DAO)** or **B (schema only)**?


i want to review the above idea if anything i am missing. for now i want to make a offline. later i will make sync. i want to you add placeholder for it for future reference. make it simple so i can follow in logical order without too much clutter

Excellent ✅ — you’re thinking exactly like an architect.
Let’s refine your full **Retail Billing + Accounting + Inventory** plan into a **clean, offline-first system**, designed to **add sync later** — while staying simple and logically layered.

Below is your **reviewed and upgraded blueprint**, with placeholders for future expansion (like sync, reports, etc.), keeping it clear, minimal, and practical to implement.

---

## 🧭 1. System Overview

> **Goal:** Offline-first Retail Billing + Inventory + Double-Entry Accounting
> **Later:** Add Sync (Cloud/Device), Reports, Backups, Multi-user

---

## 🧱 2. Core Modules (Clean + Expandable)

| Module            | Purpose                                                                   | Entities                                |
| ----------------- | ------------------------------------------------------------------------- | --------------------------------------- |
| **Accounts**      | Handles ledgers for cash, customers, suppliers, capital, income, expenses | `Account`                               |
| **Inventory**     | Tracks stock, cost, and valuation                                         | `Item`, `StockMovement`                 |
| **Transactions**  | Records every business event (sale, purchase, expense, etc.)              | `Transaction`, `TransactionEntry`       |
| **Reports**       | Derived data (Ledger, Stock Report, P&L, Balance Sheet)                   | computed later                          |
| **Sync (future)** | Handles cloud sync and backup                                             | `SyncMeta`, API endpoints (placeholder) |
| **Settings**      | Business info, fiscal year, rounding rules                                | `BusinessConfig`                        |

---

## 🧩 3. Entity Summary (Simplified Logical Design)

### 🧾 Account

| Field   | Type     | Example                                  |
| ------- | -------- | ---------------------------------------- |
| id      | int      | 1                                        |
| name    | text     | Cash                                     |
| type    | enum     | asset / liability / income / expense     |
| group   | text     | Cash & Bank / Sales / Purchase / Expense |
| balance | computed | via entries                              |

→ Used for **ledger reporting**.

---

### 📦 Item

| Field         | Type     | Example              |
| ------------- | -------- | -------------------- |
| id            | int      | 101                  |
| name          | text     | Toned Milk 1L        |
| unit          | text     | litre                |
| opening_stock | real     | 20                   |
| opening_value | real     | 1200                 |
| category      | text     | Dairy                |
| avg_rate      | computed | from stock movements |

→ Used for **stock tracking + valuation**.

---

### 💰 Transaction (Voucher Header)

| Field     | Type     | Example                                |
| --------- | -------- | -------------------------------------- |
| id        | int      | 2001                                   |
| date      | datetime | 2025-10-15                             |
| type      | enum     | sale / purchase / expense / adjustment |
| narration | text     | “Sale to Ramesh”                       |

→ Parent record for entries and stock movements.

---

### 📘 TransactionEntry (Double-entry lines)

| Field          | Type | Example |
| -------------- | ---- | ------- |
| id             | int  | 5001    |
| transaction_id | int  | 2001    |
| account_id     | int  | Cash    |
| debit          | real | 600     |
| credit         | real | 0       |

→ Always ensures total debit = total credit.

---

### 📊 StockMovement

| Field          | Type | Example  |
| -------------- | ---- | -------- |
| id             | int  | 7001     |
| transaction_id | int  | 2001     |
| item_id        | int  | 101      |
| direction      | enum | in / out |
| quantity       | real | 10       |
| rate           | real | 60       |
| total          | real | 600      |

→ Links **inventory flow** to **financial events**.

---

## 🔄 4. Logical Data Flow

### 🟢 Sale Example

| Layer                | Data               | Effect              |
| -------------------- | ------------------ | ------------------- |
| `Transaction`        | “Sale to Ramesh”   | parent voucher      |
| `TransactionEntries` | Cash + Sales       | double-entry impact |
| `StockMovement`      | Milk 10 out        | reduces inventory   |
| Reports              | Ledger, Stock, P&L | derived             |

---

## 🧮 5. Core Accounting Logic

**Profit & Loss**

```
Profit = (Sales – COGS) – Expenses
COGS = Opening Stock + Purchases – Closing Stock
```

**Balance Sheet**

```
Assets = Liabilities + Equity
```

**Inventory Valuation**

* Use **Weighted Average** for simplicity now.
* Add **FIFO** later (placeholder function).

---

## ⚙️ 6. Clean Architecture Folder Layout (Simplified + Future-ready)

```
lib/
├── core/
│   ├── constants/
│   ├── utils/
│   ├── errors/
│   └── sync/                # 🔸 placeholder for cloud sync later
│       ├── sync_manager.dart
│       ├── sync_meta.dart
│       └── sync_repository.dart
│
├── data/
│   ├── db/
│   │   ├── tables/
│   │   │   ├── accounts.dart
│   │   │   ├── items.dart
│   │   │   ├── transactions.dart
│   │   │   ├── transaction_entries.dart
│   │   │   ├── stock_movements.dart
│   │   └── dao/
│   │       ├── account_dao.dart
│   │       ├── item_dao.dart
│   │       ├── transaction_dao.dart
│   │       └── stock_dao.dart
│   ├── repositories/
│   │   ├── account_repository.dart
│   │   ├── item_repository.dart
│   │   ├── transaction_repository.dart
│   │   └── sync_repository.dart    # 🔸 placeholder for sync API
│
├── domain/
│   ├── entities/
│   │   ├── account.dart
│   │   ├── item.dart
│   │   ├── transaction.dart
│   │   └── stock.dart
│   ├── usecases/
│       ├── record_sale_usecase.dart
│       ├── record_purchase_usecase.dart
│       ├── get_ledger_usecase.dart
│       ├── get_stock_report_usecase.dart
│       └── sync_data_usecase.dart  # 🔸 placeholder
│
├── presentation/
│   ├── screens/
│   │   ├── dashboard_screen.dart
│   │   ├── sale_screen.dart
│   │   ├── purchase_screen.dart
│   │   ├── ledger_screen.dart
│   │   ├── stock_screen.dart
│   │   └── settings_screen.dart
│   ├── viewmodels/
│   │   ├── sale_viewmodel.dart
│   │   ├── ledger_viewmodel.dart
│   │   └── stock_viewmodel.dart
│   └── widgets/
│       ├── item_selector.dart
│       ├── account_selector.dart
│       └── amount_field.dart
```

---

## 🪜 7. Recommended Development Order (Offline-first)

| Phase | Step                 | Deliverable                  |
| ----- | -------------------- | ---------------------------- |
| **1** | Setup Drift + Tables | Define 5 tables              |
| **2** | Implement DAO Layer  | CRUD + relationships         |
| **3** | Add Repositories     | Encapsulate logic            |
| **4** | Create UseCases      | Record sale, purchase        |
| **5** | Simple UI            | Add & view transactions      |
| **6** | Reporting            | Ledger, Stock Report         |
| **7** | Sync Placeholder     | Define sync model + metadata |
| **8** | Cloud Sync (Later)   | Integrate server or Firebase |

---

## 🧭 8. Future Sync Placeholder (Offline → Cloud)

Later you can extend with these fields and tables:

| Table           | New Field                          | Purpose                           |
| --------------- | ---------------------------------- | --------------------------------- |
| All core tables | `uuid`, `lastModified`, `isSynced` | For sync tracking                 |
| New table       | `SyncMeta`                         | Stores last sync timestamps       |
| Domain          | `SyncManager`                      | Handles local ↔️ cloud sync logic |
| Core utils      | `conflict_resolver.dart`           | Resolve duplicates/updates        |

---

## ✅ Summary

You now have:

* A **logical + modular foundation** (Accounts + Inventory + Transactions)
* **Offline-first focus**
* **Sync-ready design placeholders**
* **Clear step-by-step dev order**

---

Would you like me to now generate the **Drift schema files (with minimal DAO stubs)** for the first 5 tables — following this exact folder structure and keeping sync placeholders ready (like `uuid`, `isSynced` fields)?
That would be your **next concrete step** to start implementation.


i want to know about are you covered individual supplier and customer ledger

Excellent question 👍 — you’re thinking exactly in the right direction for real-world accounting.

Let’s go over that carefully.

---

## 🧾 **Customer & Supplier Ledgers — Yes, Fully Covered**

Your current design **already supports** individual ledgers for **customers**, **suppliers**, and any other party (like staff, expenses, banks, etc.) — via the **`Account` table** + **`TransactionEntry`** system.

Let’s break it down clearly 👇

---

## 🧩 1. `Account` Table — Universal Ledger Entity

Every “party” (customer, supplier, or even system accounts like Cash or Sales) is represented as one row in `Account`.

| id | name           | type      | group       |
| -- | -------------- | --------- | ----------- |
| 1  | Cash           | asset     | Cash & Bank |
| 2  | Sales          | income    | Revenue     |
| 3  | Ramesh         | asset     | Customer    |
| 4  | Dairy Supplier | liability | Supplier    |

So you don’t need separate `customer` or `supplier` tables — both are **Accounts** with appropriate **type/group** values.

---

## 💰 2. `TransactionEntry` — Creates the Ledger Lines

Every voucher (transaction) posts **double-entry lines** into this table.

### Example — Sale to Ramesh (₹600 cash)

| transaction_id | account_id | debit | credit |                           |
| -------------- | ---------- | ----- | ------ | ------------------------- |
| 2001           | Cash       | 600   | 0      |                           |
| 2001           | Sales      | 0     | 600    |                           |
| 2001           | Ramesh     | 0     | 0      | *(optional if on credit)* |

If it was a **credit sale** to Ramesh (not cash):

| transaction_id | account_id | debit | credit |
| -------------- | ---------- | ----- | ------ |
| 2001           | Ramesh     | 600   | 0      |
| 2001           | Sales      | 0     | 600    |

Now Ramesh’s ledger shows ₹600 due.

---

## 🧾 3. Getting a Ledger for One Party

You can query by `account_id` from `TransactionEntry` joined with `Transaction`.

**Example SQL (Drift DAO):**

```sql
SELECT t.date, t.narration, e.debit, e.credit
FROM transaction_entries e
JOIN transactions t ON e.transaction_id = t.id
WHERE e.account_id = :accountId
ORDER BY t.date;
```

That’s your **individual ledger** for a **customer** or **supplier**.

---

## 📊 4. Balance Computation

**Ledger balance** for any account =
`SUM(debit) - SUM(credit)`

Drift can compute this easily using:

```sql
SELECT SUM(debit) - SUM(credit) AS balance
FROM transaction_entries
WHERE account_id = :accountId;
```

So you can instantly get:

* Customer balance (who owes you)
* Supplier balance (what you owe them)

---

## 🧠 5. Account Grouping (Optional Enhancement)

You can predefine or allow user-defined **groups**, e.g.:

| Group       | Type      | Examples                      |
| ----------- | --------- | ----------------------------- |
| Cash & Bank | asset     | Cash, Bank                    |
| Customers   | asset     | Ramesh, Suresh                |
| Suppliers   | liability | Dairy Co., Packaging Supplier |
| Expenses    | expense   | Rent, Wages                   |
| Income      | income    | Sales, Discounts              |

This helps in:

* Ledger filtering
* Balance Sheet generation
* Report grouping

---

## 🔗 6. Customer & Supplier Management in UI Layer

In your **UI**, you can have:

* **Customer List Screen**

  * Lists all `Accounts` where `group == 'Customer'`
  * Shows current balance
  * Tap → opens Ledger Screen

* **Supplier List Screen**

  * Lists all `Accounts` where `group == 'Supplier'`

Both use the same `Account` + `TransactionEntry` data.

---

## ⚙️ 7. Future: Contact Details Extension (Optional)

If you later want phone numbers, GSTIN, or address, you can add an **`AccountProfile`** table:

| account_id | phone      | address     | gst_no          |
| ---------- | ---------- | ----------- | --------------- |
| 3          | 9876543210 | “Main Road” | 27ABCDE1234F1Z5 |

This keeps your `Account` table clean and still extendable.

---

## ✅ Summary

| Feature         | Covered?       | How                           |
| --------------- | -------------- | ----------------------------- |
| Customer Ledger | ✅              | Account + TransactionEntry    |
| Supplier Ledger | ✅              | Same mechanism                |
| Ledger Balance  | ✅              | SUM(debit-credit) per account |
| Grouping        | ✅              | Account.group                 |
| Extended info   | 🔸 (optional)  | AccountProfile table          |
| Sync support    | 🔸 placeholder | uuid + lastModified later     |

---

So yes — your design **already covers** full **per-customer and per-supplier ledgers**, exactly like a professional accounting system.

Would you like me to show you a **Drift DAO example** for fetching one party’s ledger (with running balance), so you can see how it’ll look in your app’s repository layer?


add optional recommanded

Perfect — let’s **enhance your design** with a few **optional but strongly recommended improvements** 🎯
These keep your system simple *today*, but ready for real-world growth *tomorrow* (multi-customer, reporting, sync, audit, etc.)

Here’s the upgraded model:

---

## 🧭 OVERVIEW — *Retail + Accounting + Inventory (Enhanced Offline-first)*

| Layer                      | Purpose                                             |
| -------------------------- | --------------------------------------------------- |
| **Core**                   | Accounts, Transactions, Stock                       |
| **Optional (Recommended)** | Profiles, Categories, Costing, Audit, Sync metadata |
| **Future**                 | Cloud sync, analytics, dashboards                   |

---

## 🧩 1. CORE ENTITIES (as before)

✅ **Already final and solid:**

* `Account`
* `Transaction`
* `TransactionEntry`
* `Item`
* `StockMovement`

These handle:

* Customer/supplier ledgers
* Cash/bank
* Double-entry accounting
* Inventory in/out

---

## 🧱 2. OPTIONAL (RECOMMENDED) ENTITIES

Let’s layer optional tables that *don’t break* the current logic — just extend it.

---

### 🧾 A. `AccountProfile` — *(Optional but Recommended)*

> Adds contact info for customer/supplier accounts.

| Field        | Type               | Description    |
| ------------ | ------------------ | -------------- |
| account_id   | int (FK → Account) | linked account |
| contact_name | text               | person name    |
| phone        | text               | contact number |
| email        | text               | optional       |
| address      | text               | postal address |
| gstin        | text               | tax ID         |
| notes        | text               | custom remarks |

✅ **Why**:
Keeps business/party data organized without bloating `Account`.

📍 **Use:** Show in “Customer/Supplier Detail Screen”.

---

### 🏷️ B. `AccountGroup` — *(Optional but Recommended)*

> Defines logical groups for accounts (e.g. Customers, Suppliers, Income, Expense).

| Field | Type | Example                              |
| ----- | ---- | ------------------------------------ |
| id    | int  | 10                                   |
| name  | text | “Customers”                          |
| type  | enum | asset / liability / income / expense |

✅ **Why**:
Makes it easy to group accounts for Balance Sheet and P&L.

📍 **Use:**
`Account.group_id` → `AccountGroup.id`

---

### 📦 C. `ItemCategory` — *(Optional but Recommended)*

> Groups products for better reporting.

| Field       | Type | Example  |
| ----------- | ---- | -------- |
| id          | int  | 5        |
| name        | text | “Dairy”  |
| description | text | optional |

📍 **Use:**
`Item.category_id` → `ItemCategory.id`

✅ Helps in stock filtering and category-wise profit reports.

---

### 🧮 D. `ItemCostHistory` — *(Optional but Recommended)*

> Tracks cost over time (useful for weighted average or FIFO).

| Field              | Type     | Description               |
| ------------------ | -------- | ------------------------- |
| id                 | int      | 1                         |
| item_id            | int      | FK → Item                 |
| date               | datetime | record date               |
| quantity           | real     | qty purchased             |
| rate               | real     | cost per unit             |
| source_transaction | int      | optional link to purchase |
| method             | enum     | avg / fifo / manual       |

✅ **Why:**
Lets you calculate historical or average item cost — vital for COGS and valuation accuracy.

---

### 🧾 E. `BusinessConfig` — *(Recommended)*

> Centralized app settings.

| Field                  | Type     | Description     |
| ---------------------- | -------- | --------------- |
| id                     | int      | 1               |
| business_name          | text     | shop name       |
| currency               | text     | “INR”           |
| fiscal_year_start      | date     | e.g. 2025-04-01 |
| stock_valuation_method | text     | “avg_cost”      |
| enable_sync            | bool     | default: false  |
| created_at             | datetime | record time     |

✅ **Why:**
Keeps all system-level config in one place.

📍 **Future-proof** — add sync or cloud config later.

---

### 🔒 F. `AuditLog` — *(Optional but Highly Recommended)*

> Records changes for accountability.

| Field     | Type     | Description               |
| --------- | -------- | ------------------------- |
| id        | int      | 1                         |
| entity    | text     | “Transaction”             |
| entity_id | int      | e.g. 2001                 |
| action    | text     | “insert/update/delete”    |
| timestamp | datetime | system time               |
| user      | text     | optional (for multi-user) |
| details   | text     | JSON diff or message      |

✅ **Why:**

* Helps debug data changes
* Enables audit trail (useful if sync conflicts happen later)

---

### ☁️ G. `SyncMeta` — *(Placeholder for future cloud sync)*

| Field             | Type     | Description         |
| ----------------- | -------- | ------------------- |
| table_name        | text     | e.g. “transactions” |
| last_synced_at    | datetime | last sync timestamp |
| last_local_change | datetime | last local change   |
| pending_count     | int      | unsynced rows count |

And every syncable table (like `Account`, `Transaction`, etc.) should have:

| Field         | Type     | Description       |
| ------------- | -------- | ----------------- |
| uuid          | text     | unique sync ID    |
| last_modified | datetime | local update time |
| is_synced     | bool     | sync status       |

✅ **Why:**

* Enables cloud integration later (Firebase / REST / Supabase)
* Doesn’t affect offline flow now

---

## 🧭 3. Updated Folder Layout (With Optional Entities)

```
lib/
├── data/
│   ├── db/
│   │   ├── tables/
│   │   │   ├── accounts.dart
│   │   │   ├── account_profiles.dart      # ✅ optional
│   │   │   ├── account_groups.dart        # ✅ optional
│   │   │   ├── items.dart
│   │   │   ├── item_categories.dart       # ✅ optional
│   │   │   ├── item_cost_history.dart     # ✅ optional
│   │   │   ├── transactions.dart
│   │   │   ├── transaction_entries.dart
│   │   │   ├── stock_movements.dart
│   │   │   ├── business_config.dart       # ✅ optional
│   │   │   ├── audit_logs.dart            # ✅ optional
│   │   │   └── sync_meta.dart             # 🔸 placeholder
│   │   └── dao/
│   │       ├── account_dao.dart
│   │       ├── transaction_dao.dart
│   │       ├── item_dao.dart
│   │       ├── report_dao.dart            # future
│   │       ├── sync_dao.dart              # placeholder
│   │       └── audit_dao.dart             # optional
│
├── domain/
│   ├── entities/
│   ├── usecases/
│   │   ├── record_sale_usecase.dart
│   │   ├── record_purchase_usecase.dart
│   │   ├── get_ledger_usecase.dart
│   │   ├── get_stock_report_usecase.dart
│   │   ├── sync_data_usecase.dart          # placeholder
│   │   └── log_audit_usecase.dart          # optional
│
└── core/
    ├── sync/
    │   ├── sync_manager.dart
    │   └── sync_utils.dart
```

---

## ✅ SUMMARY — Optional Recommended Additions

| Optional Table    | Purpose             | Benefit                 |
| ----------------- | ------------------- | ----------------------- |
| `AccountProfile`  | Contact details     | Customer/Supplier info  |
| `AccountGroup`    | Ledger grouping     | Cleaner reports         |
| `ItemCategory`    | Product grouping    | Category analysis       |
| `ItemCostHistory` | Historical cost     | Accurate COGS           |
| `BusinessConfig`  | App settings        | Centralized control     |
| `AuditLog`        | Change tracking     | Transparency, debugging |
| `SyncMeta`        | Cloud sync tracking | Future online mode      |

---

## 🚀 Implementation Tip

You can start **offline core first** (5 main tables)
then gradually add optional ones **as separate migrations** — they won’t break existing data.

---

Would you like me to now generate the **updated Drift schema (with these optional tables included but commented as optional)** — so you can see how they connect to your main 5 core tables?

Excellent ✅ — switching to a **home + perishable products** context changes the business logic subtly — but importantly.

Let’s tailor your model for **home-scale inventory** and **perishables (like milk, fruits, veggies, etc.)**, where items have **expiry, freshness, and smaller stock cycles** — not long-term warehousing.

Below is your **optimized model update**, focusing on **simplicity**, **accuracy**, and **real-world usability** for your use case.

---

## 🧭 1. Context

> **Goal:**
> Offline-first retail/billing + accounting app for **home or small shop**
> dealing in **perishable goods** (milk, dairy, fruits, vegetables, etc.)

> **Priorities:**

* Track **daily stock in/out**
* Handle **expiry and wastage**
* Keep **valuation accurate but lightweight**
* Simple UI & logic (no heavy ERP stuff)
* Optional future sync

---

## 🧱 2. Key Conceptual Changes

| Area                   | Before                | Now (for perishables)                       |
| ---------------------- | --------------------- | ------------------------------------------- |
| **Inventory model**    | Long-term tracking    | Short shelf-life tracking                   |
| **Valuation method**   | Weighted avg / FIFO   | Simple avg or last purchase rate            |
| **Expiry**             | Optional              | Must-have                                   |
| **Wastage/adjustment** | Rare                  | Frequent — daily disposal                   |
| **Units**              | Common (litre/kg/pcs) | Important to standardize (litre, kg, g, ml) |
| **Stock closing**      | Periodic              | Daily or per batch                          |

---

## 🧩 3. Entity Adjustments

Let’s refine the **core tables** to fit perishable needs.

---

### 🧾 A. `Account` — *(unchanged)*

Still universal — customers, suppliers, cash, etc.
→ No change needed.

---

### 📦 B. `Item` — *(add expiry-related fields)*

| Field           | Type      | Example              |
| --------------- | --------- | -------------------- |
| id              | int       | 101                  |
| name            | text      | “Toned Milk 1L”      |
| unit            | text      | litre                |
| category_id     | int       | Dairy                |
| shelf_life_days | int       | 3                    |
| expiry_date     | datetime? | optional for batches |
| opening_stock   | real      | 10                   |
| opening_value   | real      | 600                  |
| track_batches   | bool      | true                 |
| reorder_level   | real      | 5                    |

✅ **Why:**

* Perishable items need *expiry* and *reorder awareness*.
* `shelf_life_days` lets you auto-calculate expiry for incoming stock.

---

### 📋 C. `StockMovement` — *(add batch & expiry info)*

| Field          | Type      | Description                 |
| -------------- | --------- | --------------------------- |
| id             | int       |                             |
| transaction_id | int       | FK → Transaction            |
| item_id        | int       | FK → Item                   |
| batch_no       | text?     | optional batch identifier   |
| direction      | enum      | in / out / waste / adjust   |
| quantity       | real      |                             |
| rate           | real      |                             |
| total          | real      |                             |
| expiry_date    | datetime? | optional                    |
| note           | text?     | “Spoiled”, “Returned”, etc. |

✅ **Why:**
You’ll record stock *wastage* separately (`direction = waste`)
and optionally tag each purchase with an expiry.

📍 *This enables stock-aging and near-expiry alerts.*

---

### 🧾 D. `Transaction` — *(add type for wastage & adjustment)*

| Field     | Type     | Example                                          |
| --------- | -------- | ------------------------------------------------ |
| id        | int      | 2001                                             |
| date      | datetime | 2025-10-15                                       |
| type      | enum     | sale / purchase / expense / wastage / adjustment |
| narration | text     | “Expired milk disposed”                          |

✅ **Why:**
You’ll often record **daily wastage or spoilage**, which should:

* Reduce stock (inventory side)
* Record expense (accounting side)

---

### 📊 E. `TransactionEntry` — *(unchanged)*

But for **wastage**, you’ll do something like:

| Account            | Debit | Credit |
| ------------------ | ----- | ------ |
| “Wastage Expense”  | 200   | 0      |
| “Inventory (Milk)” | 0     | 200    |

---

## 🧮 4. Accounting Changes (Lightweight Retail Mode)

### **COGS (Cost of Goods Sold)**

For perishables, use **“moving average”** or **last purchase rate**
instead of complex FIFO.

```
COGS = (Total Out Qty × Current Avg Rate)
```

Keep a per-item `avg_rate` field updated after each purchase.

### **Wastage Expense**

Treat spoiled goods as a separate expense:

* Debit: “Wastage Expense”
* Credit: “Inventory”
  → This automatically reduces profit.

---

## ⚙️ 5. Recommended Optional Tables (for perishables)

| Table            | Purpose                                   | Notes                             |
| ---------------- | ----------------------------------------- | --------------------------------- |
| `Batch`          | Tracks stock batches by expiry            | Link via `item_id`                |
| `ExpiryAlert`    | Holds soon-to-expire items                | Generated daily                   |
| `WastageRecord`  | Precomputed from `StockMovement`          | For reports                       |
| `ItemCategory`   | Groups perishables (Dairy, Produce, etc.) | optional                          |
| `BusinessConfig` | Controls expiry rules                     | e.g., “alert 1 day before expiry” |

---

### Example `Batch` table

| Field           | Type     | Description     |
| --------------- | -------- | --------------- |
| id              | int      |                 |
| item_id         | int      | FK → Item       |
| batch_no        | text     | “M20251015-A”   |
| purchase_date   | datetime |                 |
| expiry_date     | datetime |                 |
| quantity        | real     | current balance |
| rate            | real     | purchase rate   |
| remaining_value | real     | derived         |
| active          | bool     | true/false      |

✅ **Why:**
Tracks perishable stock batches automatically.

---

## 📱 6. Practical Daily Flow (Home/Perishable Case)

| Action                         | Transaction Type | StockMovement | Notes                 |
| ------------------------------ | ---------------- | ------------- | --------------------- |
| Buy milk from supplier         | purchase         | in            | rate, expiry recorded |
| Sell milk to customer          | sale             | out           | reduces stock         |
| Some milk spoils               | wastage          | waste         | expense recorded      |
| Adjust quantity (manual check) | adjustment       | adjust        | corrects balance      |

---

## 🧭 7. Folder Layout (Simplified for Home Use)

```
lib/
├── data/
│   ├── db/
│   │   ├── tables/
│   │   │   ├── accounts.dart
│   │   │   ├── items.dart
│   │   │   ├── stock_movements.dart
│   │   │   ├── transactions.dart
│   │   │   ├── transaction_entries.dart
│   │   │   ├── batches.dart               # ✅ optional for perishables
│   │   │   ├── wastage_records.dart       # ✅ optional summary table
│   │   │   ├── expiry_alerts.dart         # ✅ optional for reminders
│   │   ├── dao/
│   │   │   ├── item_dao.dart
│   │   │   ├── transaction_dao.dart
│   │   │   ├── stock_dao.dart
│   │   │   └── batch_dao.dart
│   └── repositories/
│       ├── inventory_repository.dart
│       └── report_repository.dart
│
├── domain/
│   ├── usecases/
│   │   ├── record_sale_usecase.dart
│   │   ├── record_purchase_usecase.dart
│   │   ├── record_wastage_usecase.dart     # ✅ new
│   │   ├── get_expiry_alerts_usecase.dart  # ✅ new
│   │   └── get_stock_summary_usecase.dart
│
└── presentation/
    ├── screens/
    │   ├── stock_screen.dart
    │   ├── sale_screen.dart
    │   ├── wastage_screen.dart
    │   └── expiry_alerts_screen.dart
```

---

## 🧠 8. Smart Future Enhancements

| Feature                 | Purpose                                      | Implementation                         |
| ----------------------- | -------------------------------------------- | -------------------------------------- |
| **Daily Expiry Alerts** | Warn what’s expiring soon                    | Query `expiry_date <= today + 1`       |
| **Wastage Dashboard**   | Track daily loss                             | Sum of wastage transactions            |
| **Auto Disposal Entry** | Mark expired stock as “wasted” automatically | Cron-like daily task                   |
| **Sync Placeholder**    | Add later for cloud backup                   | Use `uuid`, `lastModified`, `isSynced` |

---

## ✅ SUMMARY — Updates for Perishable / Home Scenario

| Category            | Change                                         |
| ------------------- | ---------------------------------------------- |
| **Items**           | Add shelf_life, expiry, reorder, track_batches |
| **StockMovement**   | Add direction (`waste`), expiry, batch_no      |
| **Transactions**    | Add `wastage` type                             |
| **Optional Tables** | Batch, ExpiryAlert, WastageRecord              |
| **Use Cases**       | Add record_wastage, expiry alerts              |
| **Accounting**      | Treat wastage as expense                       |
| **Valuation**       | Use simple avg rate                            |

---

Would you like me to generate the **Drift table definitions** next (for Items, StockMovement, Transaction, Batch, and WastageRecord) — specifically adapted for **perishables and home-scale tracking** (lightweight, offline, and clean)?
