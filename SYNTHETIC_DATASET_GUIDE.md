# AI Documentation Executive - Synthetic Test Pack

Created for SESHANK AI LABS as a fictional prototype dataset.

## IMPORTANT
Every shipper, consignee, carrier, address, reference, shipment date, AWB number and cargo record in these files is fictional. All documents are prominently marked as synthetic and are NOT valid for shipment, customs, payment, insurance or regulatory use. Do not send these PDFs to a carrier or customs authority. Do not present them as client documents.

## Contents
- `case_01_clean/`: matching baseline packet.
- `case_02_weight_mismatch/`: AWB gross weight changed to 254 kg while packing list remains 245 kg.
- `case_03_package_count_mismatch/`: AWB declares 11 pieces while packing list declares 12 cartons. The 1 carton = 1 AWB piece rule applies only to this synthetic test.
- `case_04_invoice_reference_mismatch/`: packing list cites a different invoice reference.
- `case_05_consignee_mismatch/`: AWB consignee differs from the invoice/packing list.
- `case_06_missing_consignee/`: AWB consignee field is blank.
- `ocr_test/03_air_waybill_scan_only.pdf`: image-only version of the clean baseline AWB, for testing OCR fallback.
- `FIELD_CHECKLIST.md`: the exact rules for the demo.
- `EXPECTED_RESULTS.json`: expected outcomes for unit testing.
- `GROUND_TRUTH.json`: canonical field values for each case.
- `MANIFEST.csv`: list of all PDF inputs.

Each case has three one-page PDFs: commercial invoice, packing list and air waybill-like reference layout. All are original fictional layouts, not replicas of official forms.

## How to test your prototype
1. Start with `case_01_clean`. The configured checks should pass.
2. Run each mismatch packet separately. The employee should flag only the planted issue(s) described in the checklist, alongside any legitimate validation messages.
3. Try the OCR-only AWB. The system should detect that no text layer is present (or that extraction yields no text), run OCR if available, then mark fields uncertain if OCR cannot read them confidently.
4. Compare the actual result with `EXPECTED_RESULTS.json`. Record false positives, missed issues, extraction errors and any human corrections.
5. Verify every flagged field against the source page. The app must show document/page and, where possible, the location or snippet that supports the extracted value.
6. The prototype must never approve the shipment or claim customs compliance. Human review is required.

## What these tests do NOT prove
They do not prove general performance on arbitrary freight-forwarding documents, UAE customs compliance, eligibility of a shipment, or a specific reduction in staff hours. The dataset is intentionally simple and contains planted issues. It only checks whether the prototype behaves correctly on these examples.

## Public references used for document concepts
- U.S. International Trade Administration, Common Export Documents: https://www.trade.gov/common-export-documents
  Describes common fields and purposes of commercial invoices, packing lists, air waybills and bills of lading. Its legal/process notes are US-oriented; the example data in this pack is not intended to represent UAE requirements.
- U.S. International Trade Administration, Documents in an Export Transaction: https://www.trade.gov/documents-export-transaction
  Explains that document requirements depend on destination and shipment and that omissions/discrepancies may delay exports.
- Digital Container Shipping Association (DCSA), Bill of Lading standard: https://dcsa.org/standards/bill-of-lading
  Discusses inconsistent data formats and manual document handling in container-shipping documents. It is a sea-freight reference, not a rulebook for this air-freight demo.
- IATA, Air Waybill form reference: https://www.iata.org/contentassets/e28d00ea3ba54be5a9ec5b34347d1c22/20250924_1115_tornerocarlos_approved.pdf
  Useful for understanding typical air waybill fields. The PDFs in this pack do not reproduce the IATA form.
