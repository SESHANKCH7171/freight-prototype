# AI Documentation Executive - Checklist Audit Report

> [!NOTE]
> **Synthetic Demonstration Only**  
> All records are fictional and created for prototype testing under [FIELD_CHECKLIST.md](file:///C:/Users/HP/AGENTIC%20AI%20BOOTCAMP/freight-prototype/FIELD_CHECKLIST.md). Not valid for shipment, customs, payment, or regulatory use.

---

## 1. Extracted Document Fields

### Commercial Invoice: [`demo_commercial_invoice_clean.pdf`](file:///C:/Users/HP/AGENTIC%20AI%20BOOTCAMP/freight-prototype/demo_commercial_invoice_clean.pdf)
- **Source Reference**: Page 1
- **Shipment Reference**: `DEMO-SHP-1001`
- **Invoice Number**: `DEMO-INV-1001`
- **Shipper / Exporter**: `DEMO CARGO ELECTRONICS FZE` (Building DEMO-14, Example Industrial Area, Dubai, UAE)
- **Consignee / Buyer**: `NORTHSTAR SAMPLE RETAIL LTD` (Unit 5, Example Business Park, London, UK)
- **Goods Description**: `LED control modules - fictional, non-hazardous demo cargo`
- **Quantity**: `240 units`
- **Unit Value**: `USD 25.00`
- **Line Total**: `USD 6,000.00`
- **Calculation Check (Printed)**: `240 units x USD 25.00 = USD 6,000.00`

---

### Packing List: [`demo_packing_list_clean.pdf`](file:///C:/Users/HP/AGENTIC%20AI%20BOOTCAMP/freight-prototype/demo_packing_list_clean.pdf)
- **Source Reference**: Page 1
- **Shipment Reference**: `DEMO-SHP-1001`
- **Invoice Reference**: `DEMO-INV-1001`
- **Shipper**: `DEMO CARGO ELECTRONICS FZE` (Building DEMO-14, Example Industrial Area, Dubai, UAE)
- **Consignee**: `NORTHSTAR SAMPLE RETAIL LTD` (Unit 5, Example Business Park, London, UK)
- **Goods Description**: `LED control modules - fictional, non-hazardous demo cargo`
- **Quantity**: `240 units`
- **Total Packages**: `12 cartons`
- **Total Net Weight**: `180 kg`
- **Total Gross Weight**: `245 kg`

---

### Air Waybill: [`demo_air_waybill_clean.pdf`](file:///C:/Users/HP/AGENTIC%20AI%20BOOTCAMP/freight-prototype/demo_air_waybill_clean.pdf)
- **Source Reference**: Page 1
- **AWB Number**: `DEMO-AWB-1001`
- **Shipment Reference**: `DEMO-SHP-1001`
- **Carrier**: `EXAMPLE AIR CARGO - fictional carrier`
- **Origin / Destination**: `Dubai, UAE (DXB)` -> `London, UK (LHR)`
- **Shipper**: `DEMO CARGO ELECTRONICS FZE` (Building DEMO-14, Example Industrial Area, Dubai, UAE)
- **Consignee**: `NORTHSTAR SAMPLE RETAIL LTD` (Unit 5, Example Business Park, London, UK)
- **Goods Description**: `LED control modules - fictional, non-hazardous demo cargo`
- **Number of Pieces**: `12 cartons (12 pieces)` -> `12 pieces`
- **Gross Weight**: `245 kg`

---

## 2. Configured Checks Evaluation

| Check ID | Rule / Description | Extracted Values | Result | Status Details |
| :--- | :--- | :--- | :--- | :--- |
| **CHK-ARITHMETIC-001** | Invoice line arithmetic: `Qty x Unit Val = Line Total` | `240 units x USD 25.00 = USD 6,000.00` | **PASS** | $240 \times \$25.00 = \$6,000.00$. Computed line matches declared line total exactly. |
| **CHK-INVOICE-REF-002** | Packing list invoice reference equals commercial invoice number | PL: `DEMO-INV-1001`, Invoice: `DEMO-INV-1001` | **PASS** | Exact match between documents. |
| **CHK-CONSIGNEE-003** | Shipper and Consignee match across all documents | Shipper: `DEMO CARGO ELECTRONICS FZE`<br>Consignee: `NORTHSTAR SAMPLE RETAIL LTD` | **PASS** | All parties match consistently across Invoice, Packing List, and AWB. |
| **CHK-PIECES-004** | 12 packing-list cartons equals 12 AWB pieces (synthetic rule) | PL: `12 cartons`, AWB: `12 pieces` | **PASS** | Piece counts align with the defined 1:1 synthetic rule. |
| **CHK-GROSS-WEIGHT-005** | Packing-list gross weight matches AWB gross weight | PL: `245 kg`, AWB: `245 kg` | **PASS** | Both weights evaluate to `245 kg`. |
| **CHK-CONSIGNEE-REQUIRED-006** | AWB consignee is required (non-blank) | AWB Consignee: `NORTHSTAR SAMPLE RETAIL LTD` | **PASS** | Field is populated and valid. |
| **CHK-READABILITY-007** | Document text extractability / OCR confidence | Direct digital PDF text streams | **PASS** | Text extracted reliably from all 3 files without ambiguity. |

---

## 3. Discrepancy & Flag Summary
- **Total Checks Evaluated**: 7
- **Passed**: 7
- **Flags Raised**: 0
- **Overall Packet Status**: **PASS** (Baseline clean packet verified against [`EXPECTED_RESULTS.json`](file:///C:/Users/HP/AGENTIC%20AI%20BOOTCAMP/freight-prototype/EXPECTED_RESULTS.json#L32-L40))
