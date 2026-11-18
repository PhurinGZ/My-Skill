# Odoo Mockup — Interactions Reference

JavaScript patterns สำหรับทำ interaction ใน HTML mockup

---

## Core Navigation State

```javascript
// State management
let currentView = 'list';   // 'list' | 'form' | 'kanban'
let currentRecord = null;
let isEditMode = false;
let currentStatus = 'draft';
let currentModule = 'orders';  // sidebar active item

// View switching
function showView(view) {
  document.querySelectorAll('.view-container').forEach(v => v.style.display = 'none');
  document.getElementById(view + '-view').style.display = 'block';
  currentView = view;
}
```

---

## List → Form Navigation

```javascript
function openForm(recordId) {
  currentRecord = DATA.find(r => r.id === recordId);
  if (!currentRecord) return;

  // Populate form fields
  document.querySelectorAll('[data-field]').forEach(el => {
    const field = el.dataset.field;
    if (currentRecord[field] !== undefined) {
      el.textContent = currentRecord[field];
      const input = el.nextElementSibling;
      if (input) input.value = currentRecord[field];
    }
  });

  // Update breadcrumb
  document.getElementById('breadcrumb-current').textContent = currentRecord.ref || currentRecord.name;

  // Set status
  setStatus(currentRecord.status || 'draft');

  // Switch view
  showView('form');
  setEditMode(false);
}

function backToList() {
  showView('list');
  currentRecord = null;
  isEditMode = false;
}

function openNewForm() {
  currentRecord = { id: null, ref: 'New', status: 'draft' };
  document.querySelectorAll('[data-field]').forEach(el => {
    el.textContent = '';
    const input = el.nextElementSibling;
    if (input) input.value = '';
  });
  document.getElementById('breadcrumb-current').textContent = 'New';
  setStatus('draft');
  showView('form');
  setEditMode(true);
}
```

---

## Edit Mode Toggle

```javascript
function setEditMode(mode) {
  isEditMode = mode;
  document.querySelectorAll('.field-value').forEach(el => {
    el.style.display = mode ? 'none' : 'inline';
  });
  document.querySelectorAll('.field-input').forEach(el => {
    el.style.display = mode ? 'block' : 'none';
  });
  document.getElementById('btn-edit').style.display = mode ? 'none' : 'inline-block';
  document.getElementById('btn-save').style.display = mode ? 'inline-block' : 'none';
  document.getElementById('btn-discard').style.display = mode ? 'inline-block' : 'none';
}

function toggleEdit() { setEditMode(true); }

function saveForm() {
  // Sync input values back to display spans
  document.querySelectorAll('.field-input').forEach(input => {
    const field = input.dataset.field;
    const display = input.previousElementSibling;
    if (display) display.textContent = input.value;
    if (currentRecord && field) currentRecord[field] = input.value;
  });
  setEditMode(false);
  showToast('บันทึกสำเร็จ ✓');
}

function discardChanges() {
  setEditMode(false);
  if (currentRecord) openForm(currentRecord.id);
}
```

---

## Workflow Status Bar

```javascript
const STATUS_FLOW = ['draft', 'confirmed', 'inprogress', 'done'];

function setStatus(status) {
  currentStatus = status;
  const steps = document.querySelectorAll('.status-step');
  const currentIdx = STATUS_FLOW.indexOf(status);

  steps.forEach((step, idx) => {
    step.classList.remove('active', 'done');
    if (idx < currentIdx) step.classList.add('done');
    else if (idx === currentIdx) step.classList.add('active');
  });

  // Update badge in header if exists
  const headerBadge = document.getElementById('status-badge');
  if (headerBadge) {
    headerBadge.className = `badge badge-${status}`;
    headerBadge.textContent = STATUS_LABELS[status] || status;
  }
}

function advanceStatus() {
  const idx = STATUS_FLOW.indexOf(currentStatus);
  if (idx < STATUS_FLOW.length - 1) {
    setStatus(STATUS_FLOW[idx + 1]);
    showToast(`สถานะเปลี่ยนเป็น: ${STATUS_LABELS[STATUS_FLOW[idx + 1]]}`);
  }
}
```

---

## Sidebar Navigation

```javascript
function navigateSidebar(menuKey) {
  currentModule = menuKey;

  // Update active state
  document.querySelectorAll('.sidebar-item').forEach(item => {
    item.classList.toggle('active', item.dataset.key === menuKey);
  });

  // Show relevant content section
  document.querySelectorAll('.module-section').forEach(section => {
    section.style.display = section.dataset.module === menuKey ? 'block' : 'none';
  });

  backToList();
}
```

---

## Toast Notification

```javascript
function showToast(message, type = 'success') {
  const existing = document.querySelector('.odoo-toast');
  if (existing) existing.remove();

  const toast = document.createElement('div');
  toast.className = 'odoo-toast';
  toast.innerHTML = `
    <span class="toast-icon">${type === 'success' ? '✓' : '✕'}</span>
    <span>${message}</span>
  `;
  toast.style.cssText = `
    position:fixed; top:58px; right:20px; z-index:9999;
    background:${type === 'success' ? '#198754' : '#DC3545'};
    color:white; padding:10px 18px; border-radius:6px;
    font-size:13px; font-weight:500;
    box-shadow:0 4px 12px rgba(0,0,0,0.2);
    display:flex; align-items:center; gap:8px;
    animation:slideInRight 0.3s ease;
  `;
  document.body.appendChild(toast);
  setTimeout(() => {
    toast.style.animation = 'slideOutRight 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 2800);
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
  @keyframes slideInRight {
    from { transform: translateX(100%); opacity:0; }
    to   { transform: translateX(0);    opacity:1; }
  }
  @keyframes slideOutRight {
    from { transform: translateX(0);    opacity:1; }
    to   { transform: translateX(100%); opacity:0; }
  }
`;
document.head.appendChild(style);
```

---

## Search/Filter (UI Only)

```javascript
function filterTable(query) {
  const q = query.toLowerCase();
  document.querySelectorAll('.odoo-table tbody tr').forEach(row => {
    const text = row.textContent.toLowerCase();
    row.style.display = text.includes(q) ? '' : 'none';
  });
}

// Attach to search input
document.getElementById('search-input')?.addEventListener('input', e => {
  filterTable(e.target.value);
});
```

---

## Delete Confirmation

```javascript
function confirmDelete() {
  const confirmed = confirm(`ต้องการลบรายการนี้ใช่หรือไม่?\n"${currentRecord?.ref || currentRecord?.name}"`);
  if (confirmed) {
    showToast('ลบรายการแล้ว', 'error');
    setTimeout(backToList, 500);
  }
}
```

---

## Modal Dialog (for Quick Lookups)

```javascript
function openModal(title, content) {
  const modal = document.createElement('div');
  modal.id = 'odoo-modal';
  modal.innerHTML = `
    <div class="modal-backdrop" onclick="closeModal()"></div>
    <div class="modal-box">
      <div class="modal-header">
        <h5>${title}</h5>
        <button onclick="closeModal()">✕</button>
      </div>
      <div class="modal-body">${content}</div>
    </div>
  `;
  document.body.appendChild(modal);
}

function closeModal() {
  document.getElementById('odoo-modal')?.remove();
}
```

---

## Language Support

```javascript
// Set at top of file based on user choice
const LANG = 'th'; // 'th' | 'en'

const T = {
  th: {
    new: 'ใหม่', edit: 'แก้ไข', save: 'บันทึก', discard: 'ยกเลิก',
    delete: 'ลบ', back: 'กลับ', search: 'ค้นหา...',
    draft: 'ร่าง', confirmed: 'ยืนยัน', inprogress: 'กำลังดำเนินการ', done: 'เสร็จสิ้น',
    saved: 'บันทึกสำเร็จ ✓', deleted: 'ลบรายการแล้ว',
  },
  en: {
    new: 'New', edit: 'Edit', save: 'Save', discard: 'Discard',
    delete: 'Delete', back: 'Back', search: 'Search...',
    draft: 'Draft', confirmed: 'Confirmed', inprogress: 'In Progress', done: 'Done',
    saved: 'Saved successfully ✓', deleted: 'Record deleted',
  }
};

const t = (key) => T[LANG][key] || key;
```
