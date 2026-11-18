# Inventory Module Reference

## Sidebar Menu Items
- 📦 Products
- 🔄 Transfers (Receipts / Delivery Orders / Internal)
- 📊 Inventory Adjustments
- 📍 Locations
- ⚙️ Configuration

---

## Transfer (Stock Picking) — Data Structure

```javascript
const INVENTORY_DATA = [
  {
    id: 1, ref: 'WH/IN/00089',
    type: 'receipt',        // receipt | delivery | internal
    type_label: 'รับสินค้า',
    partner: 'บริษัท ซัพพลาย เฮ้าส์ จำกัด',
    scheduled_date: '2024-11-16',
    source_location: 'Vendors',
    dest_location: 'WH/Stock',
    status: 'ready',
    lines: [
      { product: 'Notebook A4 80gsm', demand: 500, done: 0, unit: 'Reams' },
      { product: 'Pen Blue Ballpoint', demand: 200, done: 0, unit: 'Pcs' },
      { product: 'Stapler Standard', demand: 20, done: 0, unit: 'Pcs' },
    ],
  },
  {
    id: 2, ref: 'WH/OUT/00211',
    type: 'delivery',
    type_label: 'จัดส่งสินค้า',
    partner: 'บริษัท ไทยเทค จำกัด',
    scheduled_date: '2024-11-17',
    source_location: 'WH/Stock',
    dest_location: 'Customers',
    status: 'done',
    lines: [
      { product: 'Laptop Dell XPS 15', demand: 2, done: 2, unit: 'Units' },
      { product: 'Mouse Wireless', demand: 2, done: 2, unit: 'Units' },
    ],
    origin: 'SO/2024/00142',
  },
];
```

## List View Columns
| Column | Field |
|--------|-------|
| Reference | ref |
| Type | type_label (badge) |
| From | source_location |
| To | dest_location |
| Scheduled Date | scheduled_date |
| Status | status |

## Form View Sections
1. **Header**: ref, type, origin (SO/PO reference)
2. **Info**: partner, scheduled date, locations
3. **Operations Tab**: table (product, demand, done qty, unit)
4. **Actions**: Validate, Return, Scrap

## Status Flow
`draft` → `waiting` → `ready` → `done` / `cancelled`

---

## Product — Data Structure

```javascript
const PRODUCTS_DATA = [
  {
    id: 1, name: 'Laptop Dell XPS 15',
    ref: 'PROD-0042',
    category: 'Electronics',
    type: 'Storable Product',
    unit: 'Units',
    cost: 38000, sales_price: 45000,
    qty_on_hand: 15, qty_forecasted: 23,
    location: 'WH/Stock',
  },
  {
    id: 2, name: 'Office Chair Ergonomic',
    ref: 'PROD-0078',
    category: 'Furniture',
    type: 'Storable Product',
    unit: 'Units',
    cost: 6500, sales_price: 8500,
    qty_on_hand: 42, qty_forecasted: 32,
    location: 'WH/Stock',
  },
];
```

## Status Badges
```
ready      → 🟢 พร้อมโอน
done       → ✅ เสร็จสิ้น
waiting    → 🟡 รอสินค้า
cancelled  → 🔴 ยกเลิก
```
