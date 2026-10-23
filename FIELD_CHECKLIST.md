# FIELD CHECKLIST - SYNTHETIC DEMONSTRATION ONLY

Use only for the included synthetic packets. These are not transport, customs or compliance rules. A real forwarder must approve the checklist before real use.

## Fields to extract
- Shipment reference
- Invoice number and packing-list invoice reference
- Shipper name
- Consignee name
- Goods description
- Quantity and unit value on invoice
- Goods line total and formula check
- Packing-list package count, net weight and gross weight
- AWB number of pieces and gross weight

## Configured checks for this demo
1. Invoice line arithmetic: 240 units x USD 25.00 should equal USD 6,000.00.
2. The packing list's invoice reference should equal the commercial invoice number.
3. Shipper and consignee names should match across documents for this synthetic test. Do not use naive exact-match rules in production without the customer's approved policy.
4. For this synthetic shipment only, 12 packing-list cartons should equal 12 AWB pieces. This convention may not hold for every real shipment.
5. Packing-list gross weight should match the AWB gross weight for this synthetic test. A discrepancy is a flag for human review, not a decision about which value is correct.
6. The AWB consignee is required in this synthetic test. A blank value should be escalated.
7. If text cannot be reliably extracted, mark it unreadable/uncertain and ask for human review. Never guess.

## Required output per flag
- Check ID
- Document and field
- Extracted value(s)
- Expected rule
- Source reference (document and page, where available)
- Severity chosen by the client, or `unclassified` in the demo
- Human action required
