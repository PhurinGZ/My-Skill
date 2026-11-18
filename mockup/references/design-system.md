# Odoo 17–19 Design System Reference

## Color Palette

```css
/* Primary */
--odoo-purple:       #714B67;
--odoo-purple-dark:  #5C3D55;
--odoo-purple-light: #E8D9E3;
--odoo-purple-bg:    #F3EBF0;

/* UI Neutrals */
--bg-page:     #F5F5F5;
--bg-card:     #FFFFFF;
--bg-sidebar:  #FFFFFF;
--bg-navbar:   #714B67;

/* Text */
--text-primary:   #212529;
--text-secondary: #6C757D;
--text-muted:     #ADB5BD;
--text-white:     #FFFFFF;

/* Status Colors */
--status-draft:      #6C757D;
--status-confirmed:  #0D6EFD;
--status-inprogress: #FFC107;
--status-done:       #198754;
--status-cancelled:  #DC3545;

/* Borders */
--border-color: #DEE2E6;
--border-radius: 8px;

/* Shadows */
--shadow-card: 0 1px 3px rgba(0,0,0,0.08);
--shadow-dropdown: 0 4px 12px rgba(0,0,0,0.15);
```

## Typography

```css
font-family: 'Inter', 'Roboto', system-ui, -apple-system, sans-serif;

/* Scale */
--font-xs:   11px;
--font-sm:   12px;
--font-base: 14px;   /* body text */
--font-md:   15px;
--font-lg:   16px;
--font-xl:   20px;
--font-2xl:  24px;
```

## Layout Structure

```
┌─────────────────────────────────────────────────────┐
│  NAVBAR (48px) — purple bg, logo left, icons right  │
├──────────────┬──────────────────────────────────────┤
│              │  BREADCRUMB BAR (40px)                │
│  SIDEBAR     ├──────────────────────────────────────┤
│  (220px)     │                                       │
│              │  CONTENT AREA                         │
│  white bg    │  (bg: #F5F5F5)                        │
│              │                                       │
│              │                                       │
└──────────────┴──────────────────────────────────────┘
```

## Navbar HTML Pattern

```html
<nav class="odoo-navbar">
  <div class="navbar-left">
    <div class="odoo-logo">
      <svg><!-- odoo "o" logo --></svg>
      <span>odoo</span>
    </div>
    <div class="navbar-apps-menu">☰ Apps</div>
  </div>
  <div class="navbar-center">
    <input class="navbar-search" placeholder="Search..." />
  </div>
  <div class="navbar-right">
    <span class="nav-icon">🔔</span>
    <span class="nav-icon">⚙️</span>
    <div class="user-avatar">A</div>
  </div>
</nav>
```

## Sidebar HTML Pattern

```html
<aside class="odoo-sidebar">
  <div class="sidebar-module-title">Sales</div>
  <nav class="sidebar-nav">
    <a class="sidebar-item active" onclick="navigate('orders')">
      <span class="sidebar-icon">📋</span>
      <span>Orders</span>
    </a>
    <a class="sidebar-item" onclick="navigate('customers')">
      <span class="sidebar-icon">👥</span>
      <span>Customers</span>
    </a>
  </nav>
</aside>
```

## Status Bar Component

```html
<div class="status-bar">
  <div class="status-step done" onclick="setStatus('draft')">
    <span class="step-dot"></span> Draft
  </div>
  <div class="status-step active" onclick="setStatus('confirmed')">
    <span class="step-dot"></span> Confirmed
  </div>
  <div class="status-step" onclick="setStatus('done')">
    <span class="step-dot"></span> Done
  </div>
</div>
```

```css
.status-bar { display: flex; gap: 0; align-items: center; }
.status-step { 
  padding: 6px 20px; font-size: 12px; font-weight: 500;
  color: var(--text-secondary); cursor: pointer;
  border-bottom: 3px solid transparent;
  position: relative;
}
.status-step.active { 
  color: var(--odoo-purple); 
  border-bottom-color: var(--odoo-purple); 
  font-weight: 600;
}
.status-step.done { color: var(--status-done); }
```

## List View Pattern

```html
<div class="list-view">
  <div class="list-toolbar">
    <button class="btn-primary" onclick="openNewForm()">New</button>
    <div class="list-search">
      <input placeholder="🔍 Search..." />
    </div>
    <div class="list-view-toggle">
      <button class="active">☰</button>
      <button>⊞</button>
    </div>
  </div>
  <table class="odoo-table">
    <thead>
      <tr>
        <th><input type="checkbox"></th>
        <th>Reference</th>
        <th>Customer</th>
        <th>Date</th>
        <th>Status</th>
        <th>Total</th>
      </tr>
    </thead>
    <tbody>
      <!-- rows clickable → openForm(id) -->
    </tbody>
  </table>
</div>
```

## Form View Pattern

```html
<div class="form-view" id="form-view" style="display:none">
  <div class="form-header">
    <div class="breadcrumb">
      <span onclick="backToList()">Orders</span> › <span>SO001</span>
    </div>
    <div class="form-actions">
      <button class="btn-secondary" onclick="toggleEdit()">Edit</button>
      <button class="btn-primary" onclick="saveForm()">Save</button>
    </div>
  </div>
  <div class="status-bar"><!-- status steps --></div>
  <div class="form-body">
    <div class="form-group">
      <label>Customer</label>
      <span class="field-value" data-field="customer">บริษัท ABC</span>
      <input class="field-input" style="display:none" value="บริษัท ABC" />
    </div>
  </div>
</div>
```

## Button Styles

```css
.btn-primary {
  background: var(--odoo-purple);
  color: white;
  border: none;
  padding: 6px 16px;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
}
.btn-secondary {
  background: white;
  color: var(--odoo-purple);
  border: 1px solid var(--odoo-purple);
  padding: 6px 16px;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
}
.btn-danger {
  background: #DC3545;
  color: white;
  border: none;
  padding: 6px 16px;
  border-radius: 4px;
  cursor: pointer;
}
```

## Toast Notification

```javascript
function showToast(message, type = 'success') {
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.textContent = message;
  toast.style.cssText = `
    position:fixed; top:60px; right:20px; z-index:9999;
    background:${type==='success'?'#198754':'#DC3545'};
    color:white; padding:12px 20px; border-radius:6px;
    font-size:14px; box-shadow:0 4px 12px rgba(0,0,0,0.2);
    animation: slideIn 0.3s ease;
  `;
  document.body.appendChild(toast);
  setTimeout(() => toast.remove(), 3000);
}
```

## Kanban Card Pattern

```html
<div class="kanban-board">
  <div class="kanban-column">
    <div class="kanban-col-header">
      <span>New</span>
      <span class="kanban-count">3</span>
    </div>
    <div class="kanban-card" onclick="openForm(1)">
      <div class="kanban-card-title">SO001 - บริษัท ABC</div>
      <div class="kanban-card-meta">฿ 45,000</div>
      <div class="kanban-card-footer">
        <span class="tag">Quotation</span>
        <span class="avatar">S</span>
      </div>
    </div>
  </div>
</div>
```

## Badge/Tag Styles

```css
.badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 11px;
  font-weight: 600;
}
.badge-draft     { background:#E9ECEF; color:#6C757D; }
.badge-confirmed { background:#CFE2FF; color:#0A58CA; }
.badge-progress  { background:#FFF3CD; color:#856404; }
.badge-done      { background:#D1E7DD; color:#0F5132; }
.badge-cancelled { background:#F8D7DA; color:#842029; }
```
