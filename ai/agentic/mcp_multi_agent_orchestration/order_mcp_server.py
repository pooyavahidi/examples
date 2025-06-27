from datetime import datetime
from mcp.server.fastmcp import FastMCP


mcp = FastMCP("order")


@mcp.resource("info://shipping")
def get_shipping_info() -> str:
    """
    This resource provides information about shipping options and policies.

    Args:
        None
    Returns:
        A markdown formatted string containing shipping information.
    """
    content = (
        "# Shipping Information\n\n"
        "We offer various shipping options to suit your needs:\n\n"
        "- **Standard Shipping**: 5-7 business days\n"
        "- **Express Shipping**: 2-3 business days\n"
        "- **Overnight Shipping**: Next business day delivery\n\n"
        "All orders over $150 qualify for free standard shipping.\n"
    )
    return content


@mcp.tool()
def place_order(
    product_id: str,
    quantity: int,
    customer_name: str,
    shipping_address: str,
    payment_method: str,
) -> dict:
    """
    Place an order for a product.

    Args:
        product_id: ID of the product to order
        quantity: Number of items to order
        customer_name: Name of the customer placing the order
        shipping_address: Address where the order should be shipped
        payment_method: Payment method used for the order

    Returns:
        A dictionary containing order confirmation details
    """
    # Simulate order processing logic. This could be calling one or mutliple
    # external services, APIs, data stores, etc.

    # Get current datetime with seconds
    order_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    order_confirmation = {
        "order_id": f"ORD-{product_id}-{quantity}",
        "product_id": product_id,
        "quantity": quantity,
        "customer_name": customer_name,
        "shipping_address": shipping_address,
        "payment_method": payment_method,
        "order_datetime": order_datetime,
        "status": "Confirmed",
    }
    return order_confirmation


@mcp.prompt()
def order_instructions() -> str:
    """
    Generate instructions for managing customer's shoe orders.
    """

    prompt = """
ORDER MANAGEMENT INSTRUCTIONS:

CONVERSATION FLOW:
1. Help customers browse and select products using available tools
2. When a customer expresses interest in purchasing, gather ALL required order information
3. Once you have complete information, use the available tools to process the order
4. Provide clear order confirmation details

ORDER PROCESS:
1. When customer says they want to buy/order/purchase something:
   - Confirm the specific product they want
   - Ask: "To place your order, I'll need some information from you."
   - Be polite and friendly.

2. Collect information systematically:
   - "What's your full name?"
   - "How many would you like to order?"
   - "What's your shipping address? Please include street, city, state, and zip code."
   - "What payment method would you prefer to use?"

3. Confirm all details before placing the order:
   - "Let me confirm your order: [product] x [quantity] for [name], shipping to [address], payment via [method]. Is this correct?"

4. Use the available tools for order management with all collected information.

5. After successful order placement:
   - Share the order confirmation details
   - Provide order ID for their records
   - Mention estimated delivery time based on shipping info

IMPORTANT NOTES:
- Never place an order without ALL required information
- Always confirm details before calling the place order tools
- Be helpful if customers need to modify shipping or payment information
- Provide any information about orders and shipping options when is appropriate
"""
    return prompt


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport="stdio")
