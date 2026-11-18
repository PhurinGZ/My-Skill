# Prompt Enhancement Techniques by Task Type

## 🔧 Coding / Technical

### องค์ประกอบที่ต้องมี
- **ภาษา/Framework** — Python, TypeScript, React, etc.
- **Context** — ส่วนหนึ่งของ codebase? standalone function? API endpoint?
- **Input/Output** — รับอะไร คืนอะไร
- **Edge cases** — ถ้าสำคัญต่อ logic
- **Style** — มี coding convention ไหม? ต้องการ comment ไหม?

### เทคนิค
- ระบุ signature ของ function ที่ต้องการถ้าทำได้
- บอก dependency ที่มีอยู่แล้ว (เช่น "ใช้ axios แล้ว ไม่ต้องเพิ่ม")
- ถ้าแก้ bug ให้แนบ error message จริง ๆ
- ระบุ version ถ้า API เปลี่ยนบ่อย (Python 3.11, React 18)

### Before / After
```
Before: "ช่วยทำ login ให้หน่อย"

After:
สร้าง login endpoint สำหรับ Express.js REST API โดย:
- รับ: { email: string, password: string } ใน request body
- คืน: JWT token เมื่อ success, error message เมื่อ fail
- ใช้ bcrypt สำหรับ password comparison (มีติดตั้งแล้ว)
- ไม่ต้องสร้าง database layer — ส่ง mock user object มาให้
```

---

## 🎨 UI/UX & Design

### องค์ประกอบที่ต้องมี
- **Platform** — Web (desktop/mobile), iOS, Android
- **Style/Theme** — มีอยู่แล้วหรือสร้างใหม่?
- **Component ที่เกี่ยวข้อง** — มี design system ไหม?
- **State ที่ต้องแสดง** — empty, loading, error, success

### เทคนิค
- ระบุ emotion / vibe ที่ต้องการ ("trustworthy", "playful", "minimal")
- บอก constraint เช่น "ต้อง accessible", "ใช้ได้บน mobile เป็นหลัก"
- ถ้ามี design system ให้อ้างอิงสีและ spacing จาก system นั้น
- แยก "สิ่งที่ต้องมี" กับ "nice to have" ให้ชัด

### Before / After
```
Before: "ทำหน้า dashboard ให้ดูดีหน่อย"

After:
ออกแบบ analytics dashboard สำหรับ web (desktop-first) โดย:
- แสดง KPI cards 4 ตัวแถวบน (revenue, users, conversions, churn)
- มี line chart แสดง trend 30 วันล่าสุดด้านล่าง
- Style: minimal, professional, สีหลัก dark navy + white
- ต้องรองรับ loading state และ empty state ด้วย
```

---

## 📊 Analysis / Research

### องค์ประกอบที่ต้องมี
- **ข้อมูลต้นทาง** — ประเภท ขนาด รูปแบบ
- **คำถามที่ต้องการตอบ** — ระบุให้ชัดว่าต้องการรู้อะไร
- **ความลึก** — overview / deep dive / executive summary
- **ผู้รับผลลัพธ์** — technical team / management / ลูกค้า

### เทคนิค
- ถ้าข้อมูลใหญ่ ให้บอก column ที่สำคัญแทนการแนบทั้งหมด
- ระบุ metric ที่ต้องการวัด ไม่ใช่แค่ "วิเคราะห์"
- บอก format ผลลัพธ์: ตาราง / bullet / narrative / chart description

### Before / After
```
Before: "ช่วยวิเคราะห์ sales data ให้หน่อย"

After:
วิเคราะห์ข้อมูล sales (CSV แนบ) โดยหา:
1. สินค้า Top 5 ที่ขายดีที่สุด (วัดจาก revenue)
2. เดือนที่ยอดขายตกต่ำที่สุดและเหตุผลที่เป็นไปได้
3. เปรียบเทียบ Q3 vs Q4 ปีนี้

Output: bullet points กระชับ เหมาะสำหรับนำเสนอใน meeting 5 นาที
```

---

## ✍️ Writing / General

### องค์ประกอบที่ต้องมี
- **ผู้อ่าน** — ใครจะอ่าน? ระดับความรู้?
- **Tone** — formal / casual / friendly / persuasive
- **ความยาว** — จำนวนคำ / ย่อหน้า / หน้า
- **ภาษา** — ไทย / อังกฤษ / ผสม

### เทคนิค
- ถ้าเป็น email ให้ระบุ subject ที่ต้องการด้วย
- ถ้าต้องการ CTA (call-to-action) บอกให้ชัด
- ระบุ context เช่น "บริษัท B2B SaaS", "บล็อกส่วนตัว"

### Before / After
```
Before: "เขียน LinkedIn post เกี่ยวกับ AI"

After:
เขียน LinkedIn post เกี่ยวกับประสบการณ์ใช้ AI ในงานประจำวัน โดย:
- Tone: professional แต่ friendly เหมือนคนคุยกันจริง ๆ
- ความยาว: 150–200 คำ
- มี hook ที่น่าสนใจใน 2 บรรทัดแรก
- จบด้วย 1 คำถามเพื่อกระตุ้น engagement
- ภาษาอังกฤษ ไม่ใช้ buzzword มากเกินไป
```

---

## 🧩 Prompt Patterns ที่มีประสิทธิภาพสูง

| Pattern | ใช้เมื่อ | ตัวอย่าง |
|---------|---------|----------|
| **Chain of Thought** | ต้องการให้คิดทีละขั้น | "คิดทีละขั้น แล้วสรุปคำตอบ" |
| **Few-shot** | ต้องการ format เฉพาะ | แสดง 2–3 ตัวอย่างก่อนถาม |
| **Persona** | ต้องการมุมมองเฉพาะ | "ในฐานะ senior developer..." |
| **Constraints first** | ป้องกันผลลัพธ์ที่ไม่ต้องการ | ระบุสิ่งที่ "ห้ามทำ" ชัด ๆ |
| **Output template** | ต้องการ structure เดิมทุกครั้ง | แนบ template ไว้ใน prompt |
