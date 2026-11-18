# HR / Payroll Module Reference

## Sidebar Menu Items
**HR:**
- 👥 Employees
- 📅 Leave Management
- 🕐 Attendance
- 🎯 Recruitment
- 📋 Appraisals

**Payroll:**
- 💰 Payslips
- 📊 Payslip Batches
- ⚙️ Salary Structures

---

## Employee — Data Structure

```javascript
const HR_DATA = [
  {
    id: 1,
    name: 'สมชาย ใจดี',
    name_en: 'Somchai Jaidee',
    employee_id: 'EMP-001',
    job_title: 'ผู้จัดการฝ่ายขาย',
    department: 'Sales',
    manager: 'วิทยา ศรีสุข',
    work_email: 'somchai@company.co.th',
    work_phone: '02-xxx-xxxx ext. 101',
    mobile: '081-xxx-xxxx',
    work_location: 'สำนักงานใหญ่',
    contract_type: 'Full-time',
    start_date: '2020-03-01',
    status: 'active',
    gender: 'ชาย',
    annual_leave_remaining: 8,
  },
  {
    id: 2,
    name: 'วิภา รักงาน',
    name_en: 'Vipa Rakngarn',
    employee_id: 'EMP-002',
    job_title: 'นักบัญชี',
    department: 'Accounting',
    manager: 'สมศรี มีสุข',
    work_email: 'vipa@company.co.th',
    start_date: '2021-06-15',
    status: 'active',
    gender: 'หญิง',
    annual_leave_remaining: 12,
  },
  {
    id: 3,
    name: 'ประสิทธิ์ ทำงานดี',
    employee_id: 'EMP-003',
    job_title: 'วิศวกรซอฟต์แวร์',
    department: 'IT',
    start_date: '2022-01-10',
    status: 'active',
    annual_leave_remaining: 5,
  },
];
```

## Employee Form Sections
1. **Header**: ชื่อ, ตำแหน่ง, สถานะ, รูปภาพ (avatar placeholder)
2. **Work Information Tab**: department, manager, work location, email, phone
3. **Private Information Tab**: gender, nationality, ID card, bank account
4. **HR Settings Tab**: employee ID, contract type, time attendance

---

## Payslip — Data Structure

```javascript
const PAYSLIP_DATA = [
  {
    id: 1,
    ref: 'SLIP/2024/11/001',
    employee: 'สมชาย ใจดี',
    period: 'พฤศจิกายน 2024',
    period_from: '2024-11-01',
    period_to: '2024-11-30',
    structure: 'Monthly Employee',
    status: 'done',
    lines: [
      { category: 'รายรับ', name: 'เงินเดือน', amount: 45000 },
      { category: 'รายรับ', name: 'โบนัสพิเศษ', amount: 5000 },
      { category: 'หัก', name: 'ประกันสังคม', amount: -750 },
      { category: 'หัก', name: 'ภาษีหัก ณ ที่จ่าย', amount: -2100 },
    ],
    gross: 50000, deductions: 2850, net: 47150,
  },
];
```

## Payslip Status Flow
`draft` → `verify (รอตรวจสอบ)` → `done (จ่ายแล้ว)` → `cancelled`

---

## Leave Request — Data Structure

```javascript
const LEAVE_DATA = [
  {
    id: 1,
    employee: 'สมชาย ใจดี',
    leave_type: 'ลาพักร้อน',
    from_date: '2024-12-23',
    to_date: '2024-12-27',
    days: 5,
    reason: 'ท่องเที่ยวช่วงปีใหม่',
    status: 'validate1', // draft | confirm | validate1 | validate | refuse
    approved_by: 'วิทยา ศรีสุข',
  },
];
```

## Leave Status Flow
`draft` → `confirm (รอนุมัติ)` → `validate1 (รออนุมัติขั้นที่ 2)` → `validate (อนุมัติแล้ว)` / `refuse (ปฏิเสธ)`
