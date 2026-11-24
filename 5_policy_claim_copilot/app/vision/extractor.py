"""
Multimodal Receipt Vision Extractor
------------------------------------
Phase 4 Responsibility:
1. Accept a receipt image file (PNG, JPG, JPEG, WEBP).
2. Base64-encode the image.
3. Call a multimodal vision model (GPT-4o-mini) using structured outputs.
4. Return a strongly-typed `ReceiptData` object containing vendor, date, items, amounts, totals, and blurriness checks.
"""

import os
import base64
import mimetypes
from typing import Union
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

from app.config import settings
from app.vision.schemas import ReceiptData, ReceiptItem


def encode_image(image_input: Union[str, bytes]) -> tuple[str, str]:
    """
    Encodes an image path or bytes into base64 and detects MIME type.
    Returns (base64_string, mime_type).
    """
    if isinstance(image_input, str):
        if not os.path.exists(image_input):
            raise FileNotFoundError(f"Image not found at path: {image_input}")

        mime_type, _ = mimetypes.guess_type(image_input)
        if not mime_type:
            mime_type = "image/png"

        with open(image_input, "rb") as f:
            image_bytes = f.read()
    elif isinstance(image_input, bytes):
        image_bytes = image_input
        mime_type = "image/png"
    else:
        raise ValueError("image_input must be a file path string or raw bytes.")

    base64_str = base64.b64encode(image_bytes).decode("utf-8")
    return base64_str, mime_type


def extract_receipt_data(
    image_input: Union[str, bytes],
    model_name: str = "gpt-4o-mini"
) -> ReceiptData:
    """
    Extracts structured receipt data from an image using a multimodal LLM.
    
    Args:
        image_input: File path string or bytes of receipt image.
        model_name: Vision model to use (default: gpt-4o-mini).
        
    Returns:
        ReceiptData: Extracted vendor, date, line items, taxes, totals, and blurriness check.
    """
    base64_image, mime_type = encode_image(image_input)

    prompt_text = (
        "You are an expert expense receipt auditing assistant.\n"
        "Carefully examine this receipt image and extract:\n"
        "1. Vendor / Restaurant / Merchant name\n"
        "2. Transaction date (format as YYYY-MM-DD if possible)\n"
        "3. Every individual line item with its description, price, and category (meal, alcohol, lodging, transportation, other)\n"
        "4. Subtotal, Tax, Tip, and Final Grand Total\n"
        "5. Image quality assessment: Set `is_blurry = True` and lower `confidence_score` if the image is blurry, cut off, or illegible.\n"
        "Be precise with numbers and amounts."
    )

    message = HumanMessage(
        content=[
            {"type": "text", "text": prompt_text},
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:{mime_type};base64,{base64_image}",
                    "detail": "high"
                }
            }
        ]
    )

    llm = ChatOpenAI(
        model=model_name,
        temperature=0.0,
        api_key=settings.OPENAI_API_KEY,
    )

    structured_llm = llm.with_structured_output(ReceiptData)
    extracted_data: ReceiptData = structured_llm.invoke([message])

    return extracted_data
