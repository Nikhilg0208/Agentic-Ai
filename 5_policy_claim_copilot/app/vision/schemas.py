"""
Pydantic Schemas for Structured Receipt Information Extraction
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class ReceiptItem(BaseModel):
    description: str = Field(description="Name or description of the purchased line item")
    amount: float = Field(description="Cost/price of this individual line item")
    category: Optional[str] = Field(
        default="other",
        description="Category: 'meal', 'alcohol', 'lodging', 'transportation', or 'other'"
    )


class ReceiptData(BaseModel):
    vendor: Optional[str] = Field(default=None, description="Name of the restaurant, store, hotel, or service provider")
    date: Optional[str] = Field(default=None, description="Date of transaction in YYYY-MM-DD or readable format")
    items: List[ReceiptItem] = Field(default_factory=list, description="Itemized list of items purchased")
    subtotal: Optional[float] = Field(default=None, description="Subtotal amount before taxes or tips")
    tax: Optional[float] = Field(default=None, description="Tax amount")
    tip: Optional[float] = Field(default=None, description="Tip or gratuity amount")
    total: Optional[float] = Field(default=None, description="Total amount paid")
    currency: str = Field(default="USD", description="Currency symbol or code (e.g. USD, EUR, INR)")
    is_blurry: bool = Field(default=False, description="True if the receipt image is blurry, degraded, or difficult to read")
    confidence_score: float = Field(default=1.0, description="Readability confidence score between 0.0 (unreadable) and 1.0 (crystal clear)")
    notes: Optional[str] = Field(default=None, description="Any observations, missing information, or notable flags")
