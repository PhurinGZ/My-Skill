# Manufacturing / Purchase / Project Module Reference

---

## MANUFACTURING

### Sidebar Menu Items
- 🏭 Manufacturing Orders
- 📋 Work Orders
- 🔧 Bill of Materials (BoM)
- 📦 Products
- 📊 Reporting

### Manufacturing Order — Data Structure

```javascript
const MFG_DATA = [
  {
    id: 1,
    ref: 'WH/MO/00056',
    product: 'Custom PC Assembly i7',
    qty: 5, unit: 'Units',
    bom: 'PC Assembly Standard',
    scheduled_start: '2024-11-18',
    deadline: '2024-11-25',
    responsible: 'ประสิทธิ์ ทำงานดี',
    status: 'confirmed',
    components: [
      { name: 'CPU Intel i7-13700', qty: 5, available: 8 },
      { name: 'RAM 16GB DDR5', qty: 10, available: 15 },
      { name: 'SSD 512GB NVMe', qty: 5, available: 3 },
      { name: 'Motherboard ASUS', qty: 5, available: 5 },
    ],
    qty_produced: 0,
    work_orders: [
      { operation: 'ประกอบ CPU + RAM', workcenter: 'Assembly Line 1', duration: 2 },
      { operation: 'ติดตั้ง Storage', workcenter: 'Assembly Line 1', duration: 1 },
      { operation: 'ทดสอบระบบ', workcenter: 'QC Station', duration: 3 },
    ],
  },
];
```

### MFG Status Flow
`draft` → `confirmed` → `progress (กำลังผลิต)` → `to_close` → `done` / `cancel`

---

## PURCHASE

### Sidebar Menu Items
- 📋 Purchase Orders
- 📝 Request for Quotation (RFQ)
- 🏪 Vendors
- 📦 Products
- 📊 Reporting

### Purchase Order — Data Structure

```javascript
const PURCHASE_DATA = [
  {
    id: 1,
    ref: 'PO/2024/00098',
    vendor: 'บริษัท ซัพพลาย เฮ้าส์ จำกัด',
    purchase_rep: 'วิภา รักงาน',
    order_date: '2024-11-14',
    delivery_date: '2024-11-21',
    payment_term: '30 วัน',
    status: 'purchase',  // draft | sent | to_approve | purchase | done | cancel
    lines: [
      { product: 'Notebook A4 80gsm', qty: 500, price: 45, subtotal: 22500, unit: 'Reams' },
      { product: 'Pen Blue Ballpoint', qty: 200, price: 8, subtotal: 1600, unit: 'Pcs' },
    ],
    amount_untaxed: 24100, amount_tax: 1687, amount_total: 25787,
    receipt_status: 'pending',  // pending | partial | full
    bill_status: 'nothing',     // nothing | waiting | to_bill | fully_billed
  },
];
```

### PO Status Flow
`draft (RFQ)` → `sent (RFQ Sent)` → `to_approve (รออนุมัติ)` → `purchase (PO)` → `done` / `cancel`

### PO List Columns
| Column | Field |
|--------|-------|
| Reference | ref |
| Vendor | vendor |
| Order Date | order_date |
| Receipt Status | receipt_status |
| Bill Status | bill_status |
| Total | amount_total |
| Status | status |

---

## PROJECT

### Sidebar Menu Items
- 📊 All Projects
- 📋 All Tasks
- 🕐 Timesheets
- 📈 Reporting

### Project — Data Structure

```javascript
const PROJECT_DATA = [
  {
    id: 1,
    name: 'ติดตั้งระบบ ERP ไทยเทค',
    customer: 'บริษัท ไทยเทค จำกัด',
    project_manager: 'สมชาย ใจดี',
    start_date: '2024-10-01',
    deadline: '2025-01-31',
    status: 'in_progress',
    privacy: 'ทีมงาน',
    tasks_count: 24,
    tasks_done: 14,
    tasks_overdue: 2,
    progress: 58,  // percent
    stages: ['Backlog', 'In Progress', 'Testing', 'Done'],
    tasks: [
      { id: 1, name: 'วิเคราะห์ความต้องการ (Business Analysis)', stage: 'Done', assignee: 'สมชาย ใจดี', deadline: '2024-10-15', priority: true },
      { id: 2, name: 'ติดตั้ง Module Sales', stage: 'Done', assignee: 'ประสิทธิ์ ทำงานดี', deadline: '2024-11-01', priority: false },
      { id: 3, name: 'Config Module Accounting', stage: 'In Progress', assignee: 'วิภา รักงาน', deadline: '2024-11-20', priority: true },
      { id: 4, name: 'ทดสอบระบบ UAT', stage: 'Backlog', assignee: '', deadline: '2024-12-15', priority: false },
      { id: 5, name: 'อบรมผู้ใช้งาน', stage: 'Backlog', assignee: '', deadline: '2025-01-15', priority: false },
    ],
  },
];
```

### Task Kanban Stages
`Backlog` → `In Progress` → `Testing` → `Done`

### Project Form Sections
1. **Header**: ชื่อโปรเจค, ลูกค้า, progress bar
2. **Settings Tab**: PM, dates, visibility
3. **Tasks View**: Kanban หรือ List (toggle ได้)
4. **Timesheets Tab**: ชั่วโมงที่บันทึก vs แผน

### Task Status Badges
```
Backlog     → สีเทา
In Progress → สีน้ำเงิน
Testing     → สีส้ม
Done        → สีเขียว
Overdue     → 🔴 tag
```
