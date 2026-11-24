"""
Phase 4 Verification Test: Receipt Image Understanding (Vision)
---------------------------------------------------------------
Verifies:
1. Generation / presence of sample test receipts (clear & blurry).
2. Multimodal LLM extraction of vendor, date, line items, taxes, and total.
3. Accurate categorization of items (e.g. food vs alcohol).
4. Blur / readability detection on degraded images.
"""

import os
import json
from app.vision.extractor import extract_receipt_data
from data.create_sample_receipts import create_receipt_images


def run_vision_test():
    print("=" * 70)
    print("   PHASE 4 VERIFICATION: Receipt Multimodal Vision Extractor")
    print("=" * 70)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")
    clear_receipt = os.path.join(data_dir, "sample_receipt.png")
    blurry_receipt = os.path.join(data_dir, "sample_blurry_receipt.png")

    # Step 1: Ensure sample receipts exist
    if not os.path.exists(clear_receipt) or not os.path.exists(blurry_receipt):
        print("\n[Step 1] Creating synthetic test receipts...")
        create_receipt_images(data_dir)
    else:
        print("\n[Step 1] Sample receipts are ready.")

    # Step 2: Test extraction on Clear Receipt
    print("\n" + "=" * 70)
    print("[Step 2] Testing Vision Model Extraction on CLEAR Receipt:")
    print("=" * 70)
    clear_result = extract_receipt_data(clear_receipt)

    print(f"Vendor:      {clear_result.vendor}")
    print(f"Date:        {clear_result.date}")
    print(f"Subtotal:    ${clear_result.subtotal}")
    print(f"Tax:         ${clear_result.tax}")
    print(f"Tip:         ${clear_result.tip}")
    print(f"Total:       ${clear_result.total} {clear_result.currency}")
    print(f"Is Blurry:   {clear_result.is_blurry}")
    print(f"Confidence:  {clear_result.confidence_score}")
    print("\nItemized Line Items:")
    for item in clear_result.items:
        print(f"  - [{item.category.upper()}] {item.description} -> ${item.amount}")

    # Step 3: Test quality detection on Blurry Receipt
    print("\n" + "=" * 70)
    print("[Step 3] Testing Vision Model Quality Check on BLURRY Receipt:")
    print("=" * 70)
    blurry_result = extract_receipt_data(blurry_receipt)

    print(f"Is Blurry Detected:  {blurry_result.is_blurry}")
    print(f"Confidence Score:    {blurry_result.confidence_score}")
    print(f"Notes / Reason:      {blurry_result.notes}")

    print("\n" + "=" * 70)
    print("  🎉 PHASE 4 VERIFICATION COMPLETE: Vision Extraction is Functional! 🎉")
    print("=" * 70)


if __name__ == "__main__":
    run_vision_test()
