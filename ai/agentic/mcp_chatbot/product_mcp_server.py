from typing import List
from mcp.server.fastmcp import FastMCP


mcp = FastMCP("product")


product_catalog = [
    {
        "product_id": "P001",
        "name": "Essence",
        "description": "A stylish sneaker suitable for various occasions.",
        "category": "Lifestyle",
        "price": 100.00,
    },
    {
        "product_id": "P002",
        "name": "Stride",
        "description": "A versatile sneaker for everyday runners.",
        "category": "Running",
        "price": 120.00,
    },
    {
        "product_id": "P003",
        "name": "Impulse",
        "description": "Flexible training shoes designed for athletes.",
        "category": "Training",
        "price": 140.00,
    },
    {
        "product_id": "P004",
        "name": "Forge",
        "description": "Durable training shoes built for performance and lifting.",
        "category": "Training",
        "price": 160.00,
    },
]


@mcp.resource("catalog://categories")
def get_product_categories() -> str:
    """
    This resource provides a simple list of all available Product categories.

    Args:
        None
    Returns:
        A markdown formatted string containing all product categories.
    """
    # Get all the categories from the product catalog
    categories = set()
    for product in product_catalog:
        categories.add(product["category"])

    # Create markdown content
    content = "# Available Product Categories\n\n"
    if categories:
        for category in sorted(categories):
            content += f"- {category}\n"
    else:
        content += "No categories found.\n"
    return content


@mcp.resource("catalog://{category}")
def get_product_category(category: str) -> str:
    """
    Get list of products in a specific category.

    Args:
        category: The product category to retrieve products for
    Returns:
        A markdown formatted string containing product details in the category.
    """
    # Normalize category name
    category = category.lower().strip()

    # Filter products by category
    products = [
        p for p in product_catalog if p["category"].lower() == category
    ]

    if not products:
        return f"# No products found in category: {category}"

    # Create markdown content with product details
    content = f"# Products in {category.title()} Category\n\n"
    content += f"Total products: {len(products)}\n\n"

    for product in products:
        content += f"## {product['name']}\n"
        content += f"- **Product ID**: {product['product_id']}\n"
        content += f"- **Price**: ${product['price']:.2f}\n"
        content += f"- **Description**: {product['description']}\n\n"
        content += "---\n\n"

    return content


@mcp.tool()
def check_product_inventory(product_id: str) -> List[dict]:
    """
    Check the stock availability of a product in the inventory.

    Args:
        product_id: The ID of the product to check
    Returns:
        List[dict] of available stock items for the product which includes
        color, size, and stock quantity.
    """
    product_stock = {
        "P001": [
            {"color": "Black", "size": "8", "quantity": 20},
            {"color": "Black", "size": "9", "quantity": 15},
            {"color": "White", "size": "8", "quantity": 30},
            {"color": "White", "size": "9", "quantity": 15},
            {"color": "Red", "size": "10", "quantity": 20},
        ],
        "P002": [
            {"color": "Black", "size": "8", "quantity": 10},
            {"color": "Black", "size": "9", "quantity": 5},
            {"color": "White", "size": "8", "quantity": 20},
            {"color": "Red", "size": "10", "quantity": 10},
            {"color": "Green", "size": "10", "quantity": 15},
        ],
        "P003": [
            {"color": "Black", "size": "8", "quantity": 5},
            {"color": "Black", "size": "9", "quantity": 10},
            {"color": "White", "size": "8", "quantity": 15},
            {"color": "Red", "size": "11", "quantity": 5},
            {"color": "Green", "size": "10", "quantity": 10},
        ],
        "P004": [
            {"color": "Black", "size": "8", "quantity": 8},
            {"color": "White", "size": "9", "quantity": 12},
            {"color": "White", "size": "11", "quantity": 18},
            {"color": "Blue", "size": "10", "quantity": 7},
            {"color": "Blue", "size": "9", "quantity": 12},
        ],
    }

    return product_stock.get(product_id, [])


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport="stdio")
