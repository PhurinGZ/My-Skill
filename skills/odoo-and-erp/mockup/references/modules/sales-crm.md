# Sales / CRM Module Reference

## Sidebar Menu Items

**Sales:**
- 📋 Orders (Sales Orders)
- 💬 Quotations
- 👥 Customers
- 📊 Sales Analysis

**CRM:**
- 🎯 Pipeline (Kanban default)
- 📅 Activities
- 👥 Customers
- 📈 Reporting

---

## Sales Order — Data Structure

```javascript
const SALES_DATA = [
  {
    id: 1, ref: 'SO/2024/00142', 
    customer: 'บริษัท ไทยเทค จำกัด',
    customer_en: 'ThaiTech Co., Ltd.',
    salesperson: 'สมชาย ใจดี',
    date: '2024-11-15',
    delivery_date: '2024-11-22',
    status: 'confirmed',
    payment_terms: '30 วัน',
    lines: [
      { product: 'Laptop Dell XPS 15', qty: 2, unit_price: 45000, subtotal: 90000 },
      { product: 'Mouse Wireless', qty: 2, unit_price: 890, subtotal: 1780 },
    ],
    subtotal: 91780, tax: 6425, total: 98205,
    note: 'กรุณาจัดส่งพร้อมกล่องดั้งเดิม',
  },
  {
    id: 2, ref: 'SO/2024/00141',
    customer: 'ห้างหุ้นส่วน สยามพาณิช',
    salesperson: 'วิภา รักงาน',
    date: '2024-11-14',
    status: 'draft',
    lines: [
      { product: 'Office Chair Ergonomic', qty: 10, unit_price: 8500, subtotal: 85000 },
    ],
    subtotal: 85000, tax: 5950, total: 90950,
  },
  {
    id: 3, ref: 'SO/2024/00140',
    customer: 'บริษัท กรีนเฮ้าส์ จำกัด',
    salesperson: 'สมชาย ใจดี',
    date: '2024-11-13',
    status: 'done',
    lines: [
      { product: 'Printer HP LaserJet', qty: 3, unit_price: 12000, subtotal: 36000 },
    ],
    subtotal: 36000, tax: 2520, total: 38520,
  },
];
```

## List View Columns
| Column | Field | Format |
|--------|-------|--------|
| Reference | ref | SO/YYYY/NNNNN |
| Customer | customer | ชื่อบริษัท |
| Salesperson | salesperson | ชื่อพนักงาน |
| Date | date | DD/MM/YYYY |
| Total | total | ฿ X,XXX.XX |
| Status | status | Badge |

## Form View Sections
1. **Header**: ref, status bar (Quotation → Sales Order → Done → Cancelled)
2. **Customer Info**: customer (Many2one), delivery address, payment terms
3. **Order Lines Tab**: table (product, qty, unit price, taxes, subtotal)
4. **Other Info Tab**: salesperson, company, fiscal position
5. **Footer**: Notes, subtotal, tax, **Total**

## Status Flow
`draft (Quotation)` → `sent (Quotation Sent)` → `confirmed (Sales Order)` → `done (Locked)` → `cancel (Cancelled)`

---

## CRM Pipeline — Data Structure

```javascript
const CRM_DATA = [
  {
    id: 1, name: 'โปรเจค ERP ไทยเทค',
    partner: 'บริษัท ไทยเทค จำกัด',
    stage: 'New', probability: 20,
    expected_revenue: 500000,
    salesperson: 'สมชาย ใจดี',
    deadline: '2024-12-31',
    activity: 'Email',
  },
  {
    id: 2, name: 'ระบบ POS สยามพาณิช',
    partner: 'ห้างหุ้นส่วน สยามพาณิช',
    stage: 'Qualified', probability: 50,
    expected_revenue: 280000,
    salesperson: 'วิภา รักงาน',
    deadline: '2024-12-15',
    activity: 'Meeting',
  },
  {
    id: 3, name: 'Module HR กรีนเฮ้าส์',
    partner: 'บริษัท กรีนเฮ้าส์ จำกัด',
    stage: 'Proposition', probability: 75,
    expected_revenue: 150000,
    salesperson: 'สมชาย ใจดี',
    deadline: '2024-11-30',
    activity: 'Phone Call',
  },
];
```

## CRM Kanban Stages
`New` → `Qualified` → `Proposition` → `Won` / `Lost`
