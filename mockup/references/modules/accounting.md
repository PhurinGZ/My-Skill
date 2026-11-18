# Accounting / Finance Module Reference

## Sidebar Menu Items
- 📊 Dashboard (ภาพรวม)
- 🧾 Customer Invoices
- 📥 Vendor Bills
- 💳 Payments
- 📒 Journal Entries
- 📈 Reports (P&L, Balance Sheet)

---

## Invoice — Data Structure

```javascript
const INVOICE_DATA = [
  {
    id: 1,
    ref: 'INV/2024/00389',
    move_type: 'out_invoice',  // out_invoice | in_invoice
    partner: 'บริษัท ไทยเทค จำกัด',
    invoice_date: '2024-11-15',
    due_date: '2024-12-15',
    payment_term: '30 วัน',
    status: 'posted',
    payment_status: 'not_paid',
    lines: [
      { product: 'Laptop Dell XPS 15', qty: 2, price: 45000, tax: 7, subtotal: 90000 },
      { product: 'Mouse Wireless', qty: 2, price: 890, tax: 7, subtotal: 1780 },
    ],
    amount_untaxed: 91780,
    amount_tax: 6425,
    amount_total: 98205,
    amount_residual: 98205,
    origin: 'SO/2024/00142',
    journal: 'Customer Invoices',
  },
  {
    id: 2,
    ref: 'INV/2024/00388',
    move_type: 'out_invoice',
    partner: 'บริษัท กรีนเฮ้าส์ จำกัด',
    invoice_date: '2024-11-13',
    due_date: '2024-12-13',
    status: 'posted',
    payment_status: 'paid',
    amount_total: 38520,
    amount_residual: 0,
  },
  {
    id: 3,
    ref: 'BILL/2024/00045',
    move_type: 'in_invoice',
    partner: 'บริษัท ซัพพลาย เฮ้าส์ จำกัด',
    invoice_date: '2024-11-10',
    due_date: '2024-12-10',
    status: 'posted',
    payment_status: 'partial',
    amount_total: 25000,
    amount_residual: 10000,
  },
];
```

## Invoice Status Flow
`draft` → `posted (ยืนยัน)` → `cancel`

## Payment Status Badges
```
not_paid  → 🔴 ยังไม่ชำระ
in_payment → 🟡 กำลังชำระ
partial   → 🟠 ชำระบางส่วน
paid      → 🟢 ชำระแล้ว
```

## Invoice Form Sections
1. **Header**: ref, partner, dates, status + payment status
2. **Invoice Lines Tab**: product, qty, price, tax%, subtotal
3. **Journal Items Tab**: debit/credit entries
4. **Footer**: amount untaxed, tax, **Total**, amount due

---

## Dashboard KPI Cards

```javascript
const ACCOUNTING_KPI = {
  receivable: { amount: 1250000, count: 23, label: 'ลูกหนี้การค้า' },
  payable:    { amount: 480000,  count: 8,  label: 'เจ้าหนี้การค้า' },
  overdue:    { amount: 320000,  count: 5,  label: 'เกินกำหนดชำระ' },
  bank_balance: { amount: 2800000, label: 'ยอดเงินในธนาคาร' },
};
```

## Profit & Loss Summary (for Dashboard)
```javascript
const PL_DATA = {
  revenue:  { current: 3250000, previous: 2980000 },
  cogs:     { current: 1850000, previous: 1720000 },
  gross_profit: { current: 1400000, previous: 1260000 },
  expenses: { current: 680000,  previous: 590000  },
  net_profit: { current: 720000, previous: 670000 },
};
```
