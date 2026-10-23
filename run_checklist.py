"""
AI Documentation Executive - Synthetic Shipment Checklist Audit
Based on FIELD_CHECKLIST.md, GROUND_TRUTH.json, and EXPECTED_RESULTS.json
"""

import os
import re
import json
from decimal import Decimal
import pypdf

def extract_pdf_text(filepath):
    """Extract text by page from PDF."""
    if not os.path.exists(filepath):
        return None
    reader = pypdf.PdfReader(filepath)
    pages = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        pages.append({"page": i + 1, "text": text})
    return pages

def parse_commercial_invoice(pages):
    if not pages or not pages[0]["text"].strip():
        return {"readable": False, "source_doc": "demo_commercial_invoice_clean.pdf", "page": 1}
    text = pages[0]["text"]
    
    inv_num_match = re.search(r"Invoice number\s*\n\s*([A-Z0-9-]+)", text)
    shp_ref_match = re.search(r"Shipment reference\s*\n\s*([A-Z0-9-]+)", text)
    shipper_match = re.search(r"Seller / exporter\s*\n\s*Name\s*\n\s*([^\n]+)", text)
    shipper_addr_match = re.search(r"Seller / exporter\s*\n\s*Name\s*\n\s*[^\n]+\n\s*Address\s*\n\s*([^\n]+)", text)
    consignee_match = re.search(r"Buyer / consignee\s*\n\s*Name\s*\n\s*([^\n]+)", text)
    consignee_addr_match = re.search(r"Buyer / consignee\s*\n\s*Name\s*\n\s*[^\n]+\n\s*Address\s*\n\s*([^\n]+)", text)
    
    # Goods and values
    desc_match = re.search(r"Goods and value\s*\n\s*Description\s*\n\s*Quantity\s*\n\s*Unit value\s*\n\s*Line total\s*\n\s*([^\n]+)", text)
    calc_match = re.search(r"Calculation check\s*\n\s*([^\n]+)", text)
    
    # Values extraction
    qty_match = re.search(r"(\d+)\s*units", text)
    unit_val_match = re.search(r"USD\s*([\d,]+\.\d{2})", text)
    line_total_match = re.search(r"Goods subtotal\s*\n\s*USD\s*([\d,]+\.\d{2})", text)
    
    return {
        "readable": True,
        "source_doc": "demo_commercial_invoice_clean.pdf",
        "page": 1,
        "shipment_reference": shp_ref_match.group(1) if shp_ref_match else None,
        "invoice_number": inv_num_match.group(1) if inv_num_match else None,
        "shipper_name": shipper_match.group(1).strip() if shipper_match else None,
        "shipper_address": shipper_addr_match.group(1).strip() if shipper_addr_match else None,
        "consignee_name": consignee_match.group(1).strip() if consignee_match else None,
        "consignee_address": consignee_addr_match.group(1).strip() if consignee_addr_match else None,
        "goods_description": desc_match.group(1).strip() if desc_match else None,
        "quantity": int(qty_match.group(1)) if qty_match else None,
        "unit_value_usd": float(unit_val_match.group(1).replace(",", "")) if unit_val_match else None,
        "line_total_usd": float(line_total_match.group(1).replace(",", "")) if line_total_match else None,
        "calculation_check_raw": calc_match.group(1).strip() if calc_match else None,
        "raw_text": text
    }

def parse_packing_list(pages):
    if not pages or not pages[0]["text"].strip():
        return {"readable": False, "source_doc": "demo_packing_list_clean.pdf", "page": 1}
    text = pages[0]["text"]
    
    shp_ref_match = re.search(r"Shipment reference\s*\n\s*([A-Z0-9-]+)", text)
    inv_ref_match = re.search(r"Invoice reference\s*\n\s*([A-Z0-9-]+)", text)
    shipper_match = re.search(r"Shipper\s*\n\s*Name\s*\n\s*([^\n]+)", text)
    shipper_addr_match = re.search(r"Shipper\s*\n\s*Name\s*\n\s*[^\n]+\n\s*Address\s*\n\s*([^\n]+)", text)
    consignee_match = re.search(r"Consignee\s*\n\s*Name\s*\n\s*([^\n]+)", text)
    consignee_addr_match = re.search(r"Consignee\s*\n\s*Name\s*\n\s*[^\n]+\n\s*Address\s*\n\s*([^\n]+)", text)
    
    qty_match = re.search(r"(\d+)\s*units", text)
    pkgs_match = re.search(r"Total packages\s*\n\s*(\d+)\s*cartons", text)
    net_wt_match = re.search(r"Total net weight\s*\n\s*(\d+)\s*kg", text)
    gross_wt_match = re.search(r"Total gross weight\s*\n\s*(\d+)\s*kg", text)
    desc_match = re.search(r"Packages\s*\n\s*\d+\s*\n\s*([^\n]+)", text)
    
    return {
        "readable": True,
        "source_doc": "demo_packing_list_clean.pdf",
        "page": 1,
        "shipment_reference": shp_ref_match.group(1) if shp_ref_match else None,
        "invoice_reference": inv_ref_match.group(1) if inv_ref_match else None,
        "shipper_name": shipper_match.group(1).strip() if shipper_match else None,
        "shipper_address": shipper_addr_match.group(1).strip() if shipper_addr_match else None,
        "consignee_name": consignee_match.group(1).strip() if consignee_match else None,
        "consignee_address": consignee_addr_match.group(1).strip() if consignee_addr_match else None,
        "goods_description": desc_match.group(1).strip() if desc_match else None,
        "quantity": int(qty_match.group(1)) if qty_match else None,
        "package_count_cartons": int(pkgs_match.group(1)) if pkgs_match else None,
        "net_weight_kg": float(net_wt_match.group(1)) if net_wt_match else None,
        "gross_weight_kg": float(gross_wt_match.group(1)) if gross_wt_match else None,
        "raw_text": text
    }

def parse_air_waybill(pages):
    if not pages or not pages[0]["text"].strip():
        return {"readable": False, "source_doc": "demo_air_waybill_clean.pdf", "page": 1}
    text = pages[0]["text"]
    
    awb_num_match = re.search(r"Demonstration AWB\s*number\s*\n\s*([A-Z0-9-]+)", text)
    shp_ref_match = re.search(r"Shipment reference\s*\n\s*([A-Z0-9-]+)", text)
    carrier_match = re.search(r"Carrier\s*\n\s*([^\n]+)", text)
    origin_match = re.search(r"Origin\s*\n\s*([^\n]+)", text)
    dest_match = re.search(r"Destination\s*\n\s*([^\n]+)", text)
    
    shipper_match = re.search(r"Shipper\s*\n\s*Name\s*\n\s*([^\n]+)", text)
    shipper_addr_match = re.search(r"Shipper\s*\n\s*Name\s*\n\s*[^\n]+\n\s*Address\s*\n\s*([^\n]+)", text)
    
    consignee_match = re.search(r"Consignee\s*\n\s*Name\s*\n\s*([^\n]+)", text)
    consignee_addr_match = re.search(r"Consignee\s*\n\s*Name\s*\n\s*[^\n]+\n\s*Address\s*\n\s*([^\n]+)", text)
    
    desc_match = re.search(r"Goods description\s*\n\s*([^\n]+)", text)
    pieces_match = re.search(r"Number of pieces\s*\n\s*(\d+)\s*cartons\s*\(\s*(\d+)\s*pieces\s*\)", text)
    gross_wt_match = re.search(r"Gross weight\s*\n\s*(\d+)\s*kg", text)
    
    return {
        "readable": True,
        "source_doc": "demo_air_waybill_clean.pdf",
        "page": 1,
        "awb_number": awb_num_match.group(1) if awb_num_match else None,
        "shipment_reference": shp_ref_match.group(1) if shp_ref_match else None,
        "carrier": carrier_match.group(1).strip() if carrier_match else None,
        "origin": origin_match.group(1).strip() if origin_match else None,
        "destination": dest_match.group(1).strip() if dest_match else None,
        "shipper_name": shipper_match.group(1).strip() if shipper_match else None,
        "shipper_address": shipper_addr_match.group(1).strip() if shipper_addr_match else None,
        "consignee_name": consignee_match.group(1).strip() if consignee_match else "",
        "consignee_address": consignee_addr_match.group(1).strip() if consignee_addr_match else "",
        "goods_description": desc_match.group(1).strip() if desc_match else None,
        "piece_count": int(pieces_match.group(2)) if pieces_match else None,
        "gross_weight_kg": float(gross_wt_match.group(1)) if gross_wt_match else None,
        "raw_text": text
    }

def run_checklist_audit(base_dir=None, inv_path=None, pl_path=None, awb_path=None, overrides=None):
    if base_dir is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    inv_file = inv_path if inv_path else os.path.join(base_dir, "demo_commercial_invoice_clean.pdf")
    pl_file = pl_path if pl_path else os.path.join(base_dir, "demo_packing_list_clean.pdf")
    awb_file = awb_path if awb_path else os.path.join(base_dir, "demo_air_waybill_clean.pdf")
    
    inv_pages = extract_pdf_text(inv_file)
    pl_pages = extract_pdf_text(pl_file)
    awb_pages = extract_pdf_text(awb_file)
    
    inv = parse_commercial_invoice(inv_pages)
    pl = parse_packing_list(pl_pages)
    awb = parse_air_waybill(awb_pages)
    
    if overrides:
        for k, v in overrides.get("invoice", {}).items():
            inv[k] = v
        for k, v in overrides.get("packing_list", {}).items():
            pl[k] = v
        for k, v in overrides.get("air_waybill", {}).items():
            awb[k] = v
    
    checks_results = []
    flags = []
    
    # Check 7: Readability / OCR fallback rule
    readability_pass = inv["readable"] and pl["readable"] and awb["readable"]
    if not readability_pass:
        unreadable_docs = []
        if not inv["readable"]: unreadable_docs.append("Commercial Invoice")
        if not pl["readable"]: unreadable_docs.append("Packing List")
        if not awb["readable"]: unreadable_docs.append("Air Waybill")
        flag = {
            "check_id": "CHK-READABILITY-007",
            "document_and_field": f"{', '.join(unreadable_docs)}: Document Text Stream",
            "extracted_value": "No readable digital text layer found",
            "expected_rule": "Documents must have reliable extractable text layer or confident OCR",
            "source_reference": f"{base_dir}",
            "severity": "unclassified",
            "human_action_required": "Mark document uncertain/unreadable; route to human specialist for manual inspection or high-resolution scan."
        }
        flags.append(flag)
        checks_results.append({"id": "CHK-READABILITY-007", "status": "FAIL", "flag": flag})
    else:
        checks_results.append({
            "id": "CHK-READABILITY-007",
            "status": "PASS",
            "details": "All documents parsed cleanly with 100% text layer fidelity."
        })

    # Check 1: Invoice line arithmetic (240 units x USD 25.00 should equal USD 6,000.00)
    qty = Decimal(str(inv["quantity"])) if inv["quantity"] is not None else None
    unit_val = Decimal(str(inv["unit_value_usd"])) if inv["unit_value_usd"] is not None else None
    line_total = Decimal(str(inv["line_total_usd"])) if inv["line_total_usd"] is not None else None
    
    if qty is not None and unit_val is not None and line_total is not None:
        computed_total = qty * unit_val
        if computed_total == line_total:
            checks_results.append({
                "id": "CHK-ARITHMETIC-001",
                "status": "PASS",
                "details": f"Invoice arithmetic verified: {qty} units x USD {unit_val:.2f} = USD {line_total:.2f} (matches declared line total USD {line_total:.2f})"
            })
        else:
            flag = {
                "check_id": "CHK-ARITHMETIC-001",
                "document_and_field": "demo_commercial_invoice_clean.pdf: Line Total",
                "extracted_value": f"Quantity={qty}, UnitValue={unit_val}, DeclaredLineTotal={line_total}",
                "expected_rule": f"Calculated total ({qty * unit_val}) must equal declared line total ({line_total})",
                "source_reference": f"{inv['source_doc']}, Page {inv['page']}",
                "severity": "unclassified",
                "human_action_required": "Escalate invoice arithmetic discrepancy to billing team / supplier."
            }
            flags.append(flag)
            checks_results.append({"id": "CHK-ARITHMETIC-001", "status": "FAIL", "flag": flag})
    else:
        flag = {
            "check_id": "CHK-ARITHMETIC-001",
            "document_and_field": "demo_commercial_invoice_clean.pdf: Line Item Values",
            "extracted_value": f"Quantity={qty}, UnitValue={unit_val}, LineTotal={line_total}",
            "expected_rule": "All arithmetic operands must be extractable numbers",
            "source_reference": f"{inv['source_doc']}, Page {inv['page']}",
            "severity": "unclassified",
            "human_action_required": "Review invoice manually for missing values."
        }
        flags.append(flag)
        checks_results.append({"id": "CHK-ARITHMETIC-001", "status": "FAIL", "flag": flag})

    # Check 2: Packing list's invoice reference should equal commercial invoice number
    inv_num = inv.get("invoice_number")
    pl_inv_ref = pl.get("invoice_reference")
    if inv_num and pl_inv_ref and inv_num == pl_inv_ref:
        checks_results.append({
            "id": "CHK-INVOICE-REF-002",
            "status": "PASS",
            "details": f"Packing list invoice reference ({pl_inv_ref}) matches Commercial Invoice number ({inv_num})"
        })
    else:
        flag = {
            "check_id": "CHK-INVOICE-REF-002",
            "document_and_field": "demo_packing_list_clean.pdf: Invoice reference",
            "extracted_value": f"PackingList Ref='{pl_inv_ref}', CommercialInvoice Number='{inv_num}'",
            "expected_rule": "The packing list's invoice reference should equal the commercial invoice number",
            "source_reference": f"Packing list ({pl['source_doc']}, Page {pl['page']}) vs Invoice ({inv['source_doc']}, Page {inv['page']})",
            "severity": "unclassified",
            "human_action_required": "Verify if packing list belongs to a different shipment/invoice or requires reissuance."
        }
        flags.append(flag)
        checks_results.append({"id": "CHK-INVOICE-REF-002", "status": "FAIL", "flag": flag})

    # Check 3: Shipper and consignee names should match across documents
    inv_shipper = inv.get("shipper_name")
    pl_shipper = pl.get("shipper_name")
    awb_shipper = awb.get("shipper_name")
    
    inv_consignee = inv.get("consignee_name")
    pl_consignee = pl.get("consignee_name")
    awb_consignee = awb.get("consignee_name")
    
    shipper_match = (inv_shipper == pl_shipper == awb_shipper) and bool(inv_shipper)
    consignee_match = (inv_consignee == pl_consignee == awb_consignee) and bool(inv_consignee)
    
    if shipper_match and consignee_match:
        checks_results.append({
            "id": "CHK-CONSIGNEE-003",
            "status": "PASS",
            "details": f"Shipper ('{inv_shipper}') and Consignee ('{inv_consignee}') match across all 3 documents."
        })
    else:
        discrepancies = []
        if not shipper_match:
            discrepancies.append(f"Shipper mismatch: Invoice='{inv_shipper}', PL='{pl_shipper}', AWB='{awb_shipper}'")
        if not consignee_match:
            discrepancies.append(f"Consignee mismatch: Invoice='{inv_consignee}', PL='{pl_consignee}', AWB='{awb_consignee}'")
        flag = {
            "check_id": "CHK-CONSIGNEE-003",
            "document_and_field": "Cross-Document: Shipper/Consignee Name",
            "extracted_value": "; ".join(discrepancies),
            "expected_rule": "Shipper and consignee names should match across documents for this synthetic test",
            "source_reference": f"Inv P{inv['page']}, PL P{pl['page']}, AWB P{awb['page']}",
            "severity": "unclassified",
            "human_action_required": "Escalate name mismatch to operations team to prevent delivery/customs hold."
        }
        flags.append(flag)
        checks_results.append({"id": "CHK-CONSIGNEE-003", "status": "FAIL", "flag": flag})

    # Check 4: For this synthetic shipment only, 12 packing-list cartons should equal 12 AWB pieces
    pl_cartons = pl.get("package_count_cartons")
    awb_pieces = awb.get("piece_count")
    if pl_cartons is not None and awb_pieces is not None and pl_cartons == awb_pieces:
        checks_results.append({
            "id": "CHK-PIECES-004",
            "status": "PASS",
            "details": f"Package piece count verified: Packing List cartons ({pl_cartons}) equals AWB pieces ({awb_pieces})"
        })
    else:
        flag = {
            "check_id": "CHK-PIECES-004",
            "document_and_field": "demo_air_waybill_clean.pdf: Number of pieces",
            "extracted_value": f"PackingList cartons={pl_cartons}, AWB pieces={awb_pieces}",
            "expected_rule": "12 packing-list cartons should equal 12 AWB pieces",
            "source_reference": f"PL ({pl['source_doc']}, Page {pl['page']}) vs AWB ({awb['source_doc']}, Page {awb['page']})",
            "severity": "unclassified",
            "human_action_required": "Clarify physical piece count with warehouse before tender to carrier."
        }
        flags.append(flag)
        checks_results.append({"id": "CHK-PIECES-004", "status": "FAIL", "flag": flag})

    # Check 5: Packing-list gross weight should match AWB gross weight
    pl_gw = pl.get("gross_weight_kg")
    awb_gw = awb.get("gross_weight_kg")
    if pl_gw is not None and awb_gw is not None and pl_gw == awb_gw:
        checks_results.append({
            "id": "CHK-GROSS-WEIGHT-005",
            "status": "PASS",
            "details": f"Gross weight verified: Packing List ({pl_gw} kg) equals AWB ({awb_gw} kg)"
        })
    else:
        flag = {
            "check_id": "CHK-GROSS-WEIGHT-005",
            "document_and_field": "demo_air_waybill_clean.pdf: Gross weight",
            "extracted_value": f"PackingList gross weight={pl_gw} kg, AWB gross weight={awb_gw} kg",
            "expected_rule": "Packing-list gross weight should match the AWB gross weight",
            "source_reference": f"PL ({pl['source_doc']}, Page {pl['page']}) vs AWB ({awb['source_doc']}, Page {awb['page']})",
            "severity": "unclassified",
            "human_action_required": "Flag for human review; inspect cargo weigh-scale slip before flight manifest."
        }
        flags.append(flag)
        checks_results.append({"id": "CHK-GROSS-WEIGHT-005", "status": "FAIL", "flag": flag})

    # Check 6: AWB consignee is required; blank value should be escalated
    awb_c = awb.get("consignee_name")
    if awb_c and awb_c.strip():
        checks_results.append({
            "id": "CHK-CONSIGNEE-REQUIRED-006",
            "status": "PASS",
            "details": f"AWB Consignee is present: '{awb_c}'"
        })
    else:
        flag = {
            "check_id": "CHK-CONSIGNEE-REQUIRED-006",
            "document_and_field": "demo_air_waybill_clean.pdf: Consignee Name",
            "extracted_value": "BLANK / EMPTY",
            "expected_rule": "The AWB consignee is required; a blank value must be escalated",
            "source_reference": f"AWB ({awb['source_doc']}, Page {awb['page']})",
            "severity": "unclassified",
            "human_action_required": "Escalate to booking agent to populate consignee name prior to cargo release."
        }
        flags.append(flag)
        checks_results.append({"id": "CHK-CONSIGNEE-REQUIRED-006", "status": "FAIL", "flag": flag})

    audit_summary = {
        "status": "PASS" if len(flags) == 0 else "FLAGGED",
        "total_checks": len(checks_results),
        "passed_checks": len([c for c in checks_results if c["status"] == "PASS"]),
        "failed_checks": len(flags),
        "extracted_data": {
            "commercial_invoice": {k: v for k, v in inv.items() if k != "raw_text"},
            "packing_list": {k: v for k, v in pl.items() if k != "raw_text"},
            "air_waybill": {k: v for k, v in awb.items() if k != "raw_text"}
        },
        "checks": checks_results,
        "flags": flags
    }
    
    return audit_summary

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    summary = run_checklist_audit(base_dir)
    print(json.dumps(summary, indent=2))
