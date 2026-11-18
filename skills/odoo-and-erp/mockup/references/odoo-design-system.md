# Odoo 17/18/19 Design System Reference

## Visual Identity

Odoo 17+ ใช้ design ที่ clean, modern, และ professional โดยมี purple เป็นสี brand หลัก

---

## Color Palette

### Brand Colors
| Variable | Hex | ใช้สำหรับ |
|----------|-----|----------|
| `--odoo-purple` | `#714B67` | Primary buttons, active states, links |
| `--odoo-purple-dark` | `#5C3D56` | Button hover, active nav item |
| `--odoo-purple-light` | `#F3EEF1` | Selected row bg, subtle highlights |
| `--odoo-purple-xlight` | `#FAF7F9` | Sidebar background tint |

### Status Colors
| Variable | Hex | ใช้สำหรับ |
|----------|-----|----------|
| `--odoo-success` | `#28A745` | Done, Paid, In Stock |
| `--odoo-warning` | `#FFC107` | In Progress, Partial, To Invoice |
| `--odoo-danger` | `#DC3545` | Cancelled, Overdue, Negative |
| `--odoo-info` | `#17A2B8` | Draft, New, Info alerts |
| `--odoo-secondary` | `#6C757D` | Archived, Muted states |

### UI Colors
| Variable | Hex | ใช้สำหรับ |
|----------|-----|----------|
| `--odoo-bg` | `#F8F9FA` | Page background |
| `--odoo-sidebar-bg` | `#FFFFFF` | Sidebar background |
| `--odoo-white` | `#FFFFFF` | Cards, form background |
| `--odoo-border` | `#DEE2E6` | Borders, dividers |
| `--odoo-border-light` | `#E9ECEF` | Subtle borders |
| `--odoo-text` | `#212529` | Primary text |
| `--odoo-text-muted` | `#6C757D` | Labels, secondary text |
| `--odoo-row-hover` | `#F5F5F5` | Table row hover |
| `--odoo-row-selected` | `#E8F4FD` | Selected row |
| `--odoo-navbar-bg` | `#FFFFFF` | Top navbar |

---

## Typography

```css
/* Import */
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Thai:wght@300;400;500;600&family=Noto+Sans:wght@300;400;500;600&display=swap');

body {
  font-family: 'Noto Sans Thai', 'Noto Sans', 'Roboto', sans-serif;
  font-size: 14px;
  color: #212529;
  line-height: 1.5;
}
```

### Font Sizes
| Element | Size | Weight |
|---------|------|--------|
| Page title | 18px | 500 |
| Section header | 16px | 500 |
| Navbar items | 14px | 400 |
| Sidebar menu | 13px | 400 |
| Table header | 12px | 600 (uppercase) |
| Table content | 13px | 400 |
| Form label | 13px | 500, color: muted |
| Form input | 14px | 400 |
| Badge / Tag | 11px | 600 |
| Button | 13px | 500 |

---

## Top Navbar

```html
<nav class="odoo-navbar">
  <!-- Left: Logo + App Switcher -->
  <div class="navbar-left">
    <div class="app-switcher">☰</div>
    <img src="odoo-logo" class="navbar-logo" />
    <span class="app-name">Sales</span>
  </div>
  
  <!-- Center: Global Search -->
  <div class="navbar-center">
    <div class="global-search">
      <input type="text" placeholder="Search..." />
    </div>
  </div>
  
  <!-- Right: Icons + User -->
  <div class="navbar-right">
    <span class="nav-icon">💬</span>
    <span class="nav-icon">📋</span>
    <span class="nav-icon">⚙️</span>
    <div class="user-avatar">A</div>
  </div>
</nav>
```

### Navbar CSS
```css
.odoo-navbar {
  height: 46px;
  background: #714B67;
  display: flex;
  align-items: center;
  padding: 0 12px;
  position: fixed;
  top: 0;
  width: 100%;
  z-index: 1000;
  box-shadow: 0 1px 3px rgba(0,0,0,0.2);
}
.navbar-logo {
  height: 28px;
  filter: brightness(0) invert(1);
}
.app-name {
  color: white;
  font-size: 15px;
  font-weight: 500;
  margin-left: 8px;
}
.user-avatar {
  width: 32px; height: 32px;
  border-radius: 50%;
  background: rgba(255,255,255,0.3);
  color: white;
  display: flex; align-items: center; justify-content: center;
  font-size: 13px; font-weight: 600;
  cursor: pointer;
}
```

---

## Sidebar

### Structure
```html
<aside class="odoo-sidebar">
  <div class="sidebar-section">
    <div class="sidebar-item active">
      <span class="sidebar-icon">📋</span>
      <span>Orders</span>
    </div>
    <div class="sidebar-sub active">Sales Orders</div>
    <div class="sidebar-sub">Quotations</div>
  </div>
  <div class="sidebar-divider"></div>
  <div class="sidebar-section-title">REPORTING</div>
  <div class="sidebar-item">
    <span class="sidebar-icon">📊</span>
    <span>Analysis</span>
  </div>
</aside>
```

### Sidebar CSS
```css
.odoo-sidebar {
  width: 220px;
  background: #FFFFFF;
  border-right: 1px solid #DEE2E6;
  height: calc(100vh - 46px);
  position: fixed;
  top: 46px;
  overflow-y: auto;
  padding: 8px 0;
}
.sidebar-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  font-size: 13px;
  color: #212529;
  cursor: pointer;
  border-radius: 4px;
  margin: 1px 6px;
}
.sidebar-item:hover { background: #F5F5F5; }
.sidebar-item.active { 
  background: #F3EEF1; 
  color: #714B67; 
  font-weight: 500;
}
.sidebar-sub {
  padding: 5px 16px 5px 36px;
  font-size: 12.5px;
  color: #6C757D;
  cursor: pointer;
}
.sidebar-sub:hover { color: #714B67; }
.sidebar-sub.active { color: #714B67; font-weight: 500; }
.sidebar-section-title {
  font-size: 10px;
  font-weight: 700;
  color: #ADB5BD;
  letter-spacing: 0.8px;
  padding: 12px 16px 4px;
}
```

---

## Content Area

```css
.odoo-content {
  margin-left: 220px;
  margin-top: 46px;
  padding: 0;
  min-height: calc(100vh - 46px);
  background: #F8F9FA;
}
.content-header {
  background: #FFFFFF;
  border-bottom: 1px solid #DEE2E6;
  padding: 12px 20px;
  display: flex;
  align-items: center;
  gap: 8px;
}
.content-body {
  padding: 16px 20px;
}
```

---

## Buttons

```css
/* Primary - Purple */
.btn-primary {
  background: #714B67;
  color: white;
  border: none;
  padding: 6px 14px;
  border-radius: 4px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
}
.btn-primary:hover { background: #5C3D56; }

/* Secondary - Outline */
.btn-secondary {
  background: white;
  color: #714B67;
  border: 1px solid #714B67;
  padding: 6px 14px;
  border-radius: 4px;
  font-size: 13px;
  cursor: pointer;
}

/* Action - dropdown trigger */
.btn-action {
  background: white;
  color: #495057;
  border: 1px solid #DEE2E6;
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 13px;
  cursor: pointer;
}
.btn-action:hover { background: #F8F9FA; }

/* Danger */
.btn-danger {
  background: #DC3545;
  color: white;
  border: none;
  padding: 6px 14px;
  border-radius: 4px;
  font-size: 13px;
  cursor: pointer;
}

/* Success */
.btn-success {
  background: #28A745;
  color: white;
  border: none;
  padding: 6px 14px;
  border-radius: 4px;
  font-size: 13px;
  cursor: pointer;
}
```

---

## Status Badges

```css
.badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}
.badge-draft    { background: #E3F2FD; color: #1565C0; }
.badge-new      { background: #E8F5E9; color: #2E7D32; }
.badge-progress { background: #FFF8E1; color: #F57F17; }
.badge-done     { background: #E8F5E9; color: #2E7D32; }
.badge-paid     { background: #E8F5E9; color: #2E7D32; }
.badge-cancelled{ background: #FFEBEE; color: #C62828; }
.badge-blocked  { background: #FFEBEE; color: #C62828; }
.badge-ready    { background: #E8F5E9; color: #2E7D32; }
.badge-waiting  { background: #FFF8E1; color: #F57F17; }
```

---

## Status Bar (Workflow)

```html
<div class="status-bar">
  <span class="status-step done" onclick="setStatus(0)">Quotation</span>
  <span class="status-arrow">›</span>
  <span class="status-step active" onclick="setStatus(1)">Sales Order</span>
  <span class="status-arrow">›</span>
  <span class="status-step" onclick="setStatus(2)">To Invoice</span>
  <span class="status-arrow">›</span>
  <span class="status-step" onclick="setStatus(3)">Invoiced</span>
</div>
```

```css
.status-bar {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 4px 0;
}
.status-step {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  color: #6C757D;
  transition: all 0.2s;
}
.status-step:hover { color: #714B67; }
.status-step.active {
  background: #714B67;
  color: white;
}
.status-step.done {
  color: #28A745;
  text-decoration: line-through;
  opacity: 0.7;
}
.status-arrow { color: #ADB5BD; font-size: 16px; }
```

---

## List View (Table)

```css
.list-view {
  background: white;
  border: 1px solid #DEE2E6;
  border-radius: 6px;
  overflow: hidden;
}
.list-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}
.list-table thead th {
  background: #F8F9FA;
  border-bottom: 2px solid #DEE2E6;
  padding: 9px 12px;
  text-align: left;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #6C757D;
  cursor: pointer;
  white-space: nowrap;
}
.list-table thead th:hover { background: #E9ECEF; }
.list-table tbody tr {
  border-bottom: 1px solid #F0F0F0;
  cursor: pointer;
  transition: background 0.1s;
}
.list-table tbody tr:hover { background: #F5F5F5; }
.list-table tbody tr.selected { background: #E8F4FD; }
.list-table tbody td {
  padding: 9px 12px;
  vertical-align: middle;
}
.list-table .checkbox-col { width: 36px; }
input[type="checkbox"] { cursor: pointer; }
```

---

## Form View

```css
.form-view {
  background: white;
  border: 1px solid #DEE2E6;
  border-radius: 6px;
  padding: 20px;
}
.form-group {
  margin-bottom: 16px;
}
.form-label {
  display: block;
  font-size: 12px;
  font-weight: 600;
  color: #6C757D;
  margin-bottom: 4px;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}
.form-control {
  width: 100%;
  padding: 7px 10px;
  border: 1px solid #DEE2E6;
  border-radius: 4px;
  font-size: 13px;
  font-family: inherit;
  color: #212529;
  background: white;
  transition: border-color 0.15s;
}
.form-control:focus {
  outline: none;
  border-color: #714B67;
  box-shadow: 0 0 0 3px rgba(113,75,103,0.1);
}
.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}
.form-row-3 {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 16px;
}
.form-section {
  border: 1px solid #DEE2E6;
  border-radius: 6px;
  margin-top: 20px;
}
.form-section-title {
  padding: 10px 16px;
  font-weight: 600;
  font-size: 13px;
  background: #F8F9FA;
  border-bottom: 1px solid #DEE2E6;
  border-radius: 6px 6px 0 0;
}
```

---

## Kanban View

```css
.kanban-view {
  display: flex;
  gap: 16px;
  overflow-x: auto;
  padding: 4px 0 16px;
}
.kanban-column {
  min-width: 260px;
  background: #F8F9FA;
  border-radius: 6px;
  border: 1px solid #DEE2E6;
}
.kanban-col-header {
  padding: 10px 14px;
  font-weight: 600;
  font-size: 13px;
  border-bottom: 1px solid #DEE2E6;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.kanban-count {
  background: #714B67;
  color: white;
  border-radius: 10px;
  padding: 1px 8px;
  font-size: 11px;
}
.kanban-cards {
  padding: 8px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  min-height: 100px;
}
.kanban-card {
  background: white;
  border: 1px solid #DEE2E6;
  border-radius: 6px;
  padding: 12px;
  cursor: pointer;
  transition: box-shadow 0.2s;
}
.kanban-card:hover { box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
.kanban-card-title { font-weight: 500; font-size: 13px; margin-bottom: 6px; }
.kanban-card-meta { font-size: 12px; color: #6C757D; }
```

---

## Toast Notification

```html
<div id="toast" class="toast" style="display:none">
  <span id="toast-msg">บันทึกสำเร็จ ✓</span>
</div>
```

```css
.toast {
  position: fixed;
  bottom: 24px;
  right: 24px;
  background: #28A745;
  color: white;
  padding: 12px 20px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 500;
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
  z-index: 9999;
  animation: slideIn 0.3s ease;
}
.toast.error { background: #DC3545; }
.toast.warning { background: #FFC107; color: #212529; }
@keyframes slideIn {
  from { transform: translateX(20px); opacity: 0; }
  to   { transform: translateX(0); opacity: 1; }
}
```

```javascript
function showToast(msg, type='success') {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.className = 'toast ' + type;
  t.style.display = 'block';
  setTimeout(() => t.style.display = 'none', 3000);
}
```

---

## Breadcrumb

```html
<div class="breadcrumb">
  <span class="breadcrumb-link" onclick="showView('list')">Sales Orders</span>
  <span class="breadcrumb-sep">›</span>
  <span class="breadcrumb-current">SO/2025/0042</span>
</div>
```

```css
.breadcrumb { display: flex; align-items: center; gap: 6px; font-size: 13px; }
.breadcrumb-link { color: #714B67; cursor: pointer; }
.breadcrumb-link:hover { text-decoration: underline; }
.breadcrumb-sep { color: #ADB5BD; }
.breadcrumb-current { color: #212529; font-weight: 500; }
```

---

## Chatter / Log Section (Form ด้านล่าง)

```html
<div class="chatter">
  <div class="chatter-header">Log note / Send message</div>
  <div class="chatter-messages">
    <div class="chatter-msg">
      <div class="chatter-avatar">A</div>
      <div class="chatter-body">
        <strong>Admin</strong> <span class="chatter-time">วันนี้ 10:30</span>
        <p>สร้างเอกสารแล้ว</p>
      </div>
    </div>
  </div>
</div>
```

```css
.chatter {
  margin-top: 24px;
  border: 1px solid #DEE2E6;
  border-radius: 6px;
}
.chatter-header {
  padding: 10px 16px;
  background: #F8F9FA;
  border-bottom: 1px solid #DEE2E6;
  font-weight: 600;
  font-size: 13px;
}
.chatter-msg {
  display: flex;
  gap: 12px;
  padding: 12px 16px;
  border-bottom: 1px solid #F0F0F0;
}
.chatter-avatar {
  width: 32px; height: 32px;
  background: #714B67;
  color: white;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 13px; font-weight: 600; flex-shrink: 0;
}
.chatter-time { font-size: 11px; color: #ADB5BD; margin-left: 8px; }
.chatter-body p { font-size: 13px; margin: 4px 0 0; color: #495057; }
```
