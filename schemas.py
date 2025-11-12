"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Portfolio-specific schemas

class Project(BaseModel):
    """
    Portfolio projects
    Collection name: "project"
    """
    title: str = Field(..., description="Project title")
    subtitle: Optional[str] = Field(None, description="Short tagline")
    description: str = Field(..., description="What the project is about")
    tags: List[str] = Field(default_factory=list, description="Tech stack or categories")
    image_url: Optional[HttpUrl] = Field(None, description="Preview image URL")
    demo_url: Optional[HttpUrl] = Field(None, description="Live demo URL")
    repo_url: Optional[HttpUrl] = Field(None, description="Repository URL")
    featured: bool = Field(False, description="Whether to feature on top")

class ContactMessage(BaseModel):
    """
    Messages from contact form
    Collection name: "contactmessage"
    """
    name: str = Field(..., description="Sender name")
    email: str = Field(..., description="Sender email")
    message: str = Field(..., description="Message body")

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
