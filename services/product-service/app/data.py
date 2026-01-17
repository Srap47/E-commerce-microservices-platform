"""
Product data storage
In production, this would be replaced with database queries
"""
from datetime import datetime, timedelta
from typing import List
from .models import Product


def get_products_data() -> List[Product]:
    """
    Returns sample product data
    In production: Replace with database queries (DynamoDB, PostgreSQL, etc.)
    """
    # Create some products with varying attributes for realistic ranking
    now = datetime.now()
    
    products = [
        Product(
            id="prod_001",
            name="Wireless Noise-Cancelling Headphones",
            description="Premium over-ear headphones with active noise cancellation and 30-hour battery life",
            price=299.99,
            popularity=92,
            rating=4.7,
            sales_count=2450,
            stock=34,
            category="Electronics",
            image_url="https://images.unsplash.com/photo-1505740420928-5e560c06d30e",
            created_at=now - timedelta(days=45)
        ),
        Product(
            id="prod_002",
            name="Ergonomic Office Chair",
            description="Adjustable lumbar support, breathable mesh back, 360-degree swivel",
            price=349.99,
            popularity=78,
            rating=4.5,
            sales_count=890,
            stock=12,
            category="Furniture",
            image_url="https://images.unsplash.com/photo-1580480055273-228ff5388ef8",
            created_at=now - timedelta(days=120)
        ),
        Product(
            id="prod_003",
            name="4K Ultra HD Webcam",
            description="Professional webcam with auto-focus, dual microphones, and LED ring light",
            price=129.99,
            popularity=85,
            rating=4.3,
            sales_count=1560,
            stock=67,
            category="Electronics",
            image_url="https://images.unsplash.com/photo-1587825140708-dfaf72ae4b04",
            created_at=now - timedelta(days=15)  # Recent product
        ),
        Product(
            id="prod_004",
            name="Mechanical Gaming Keyboard",
            description="RGB backlit, Cherry MX switches, programmable macro keys",
            price=159.99,
            popularity=88,
            rating=4.8,
            sales_count=3200,
            stock=89,
            category="Electronics",
            image_url="https://images.unsplash.com/photo-1595225476474-87563907a212",
            created_at=now - timedelta(days=200)
        ),
        Product(
            id="prod_005",
            name="Smart Watch Series X",
            description="Fitness tracking, heart rate monitor, GPS, 7-day battery, waterproof",
            price=399.99,
            popularity=95,
            rating=4.6,
            sales_count=5600,
            stock=23,
            category="Wearables",
            image_url="https://images.unsplash.com/photo-1523275335684-37898b6baf30",
            created_at=now - timedelta(days=8)  # Very recent
        ),
        Product(
            id="prod_006",
            name="Portable SSD 2TB",
            description="High-speed external storage, USB-C 3.2, compact design",
            price=189.99,
            popularity=72,
            rating=4.4,
            sales_count=980,
            stock=156,
            category="Electronics",
            image_url="https://images.unsplash.com/photo-1597872200969-2b65d56bd16b",
            created_at=now - timedelta(days=90)
        ),
        Product(
            id="prod_007",
            name="Wireless Mouse",
            description="Ergonomic design, 6 programmable buttons, 18-month battery life",
            price=49.99,
            popularity=81,
            rating=4.2,
            sales_count=4500,
            stock=234,
            category="Electronics",
            image_url="https://images.unsplash.com/photo-1527864550417-7fd91fc51a46",
            created_at=now - timedelta(days=300)
        ),
        Product(
            id="prod_008",
            name="USB-C Docking Station",
            description="11-in-1 hub with 4K HDMI, SD card readers, 100W power delivery",
            price=89.99,
            popularity=76,
            rating=4.1,
            sales_count=720,
            stock=45,
            category="Electronics",
            image_url="https://images.unsplash.com/photo-1625948515291-69613efd103f",
            created_at=now - timedelta(days=60)
        ),
        Product(
            id="prod_009",
            name="Standing Desk Converter",
            description="Height-adjustable, fits dual monitors, easy gas spring lift",
            price=279.99,
            popularity=69,
            rating=4.3,
            sales_count=450,
            stock=8,
            category="Furniture",
            image_url="https://images.unsplash.com/photo-1595515106969-1ce29566ff1c",
            created_at=now - timedelta(days=180)
        ),
        Product(
            id="prod_010",
            name="Laptop Backpack",
            description="Water-resistant, TSA-friendly, fits up to 17-inch laptops",
            price=59.99,
            popularity=83,
            rating=4.5,
            sales_count=2100,
            stock=178,
            category="Accessories",
            image_url="https://images.unsplash.com/photo-1553062407-98eeb64c6a62",
            created_at=now - timedelta(days=40)
        ),
        Product(
            id="prod_011",
            name="Monitor Light Bar",
            description="Space-saving desk lamp, auto-dimming, reduces screen glare",
            price=99.99,
            popularity=74,
            rating=4.6,
            sales_count=890,
            stock=67,
            category="Electronics",
            image_url="https://images.unsplash.com/photo-1507473885765-e6ed057f782c",
            created_at=now - timedelta(days=25)
        ),
        Product(
            id="prod_012",
            name="Bluetooth Speaker",
            description="360-degree sound, waterproof IPX7, 20-hour playtime",
            price=79.99,
            popularity=87,
            rating=4.4,
            sales_count=3400,
            stock=123,
            category="Electronics",
            image_url="https://images.unsplash.com/photo-1608043152269-423dbba4e7e1",
            created_at=now - timedelta(days=150)
        ),
        Product(
            id="prod_013",
            name="Premium Coffee Maker",
            description="Programmable, thermal carafe, auto-shutoff, 12-cup capacity",
            price=149.99,
            popularity=70,
            rating=4.2,
            sales_count=670,
            stock=34,
            category="Appliances",
            image_url="https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6",
            created_at=now - timedelta(days=220)
        ),
        Product(
            id="prod_014",
            name="Wireless Charging Pad",
            description="Fast 15W charging, compatible with all Qi devices, LED indicator",
            price=34.99,
            popularity=79,
            rating=4.0,
            sales_count=1890,
            stock=267,
            category="Electronics",
            image_url="https://images.unsplash.com/photo-1591290619762-d1e80fec4a47",
            created_at=now - timedelta(days=100)
        ),
        Product(
            id="prod_015",
            name="HD Webcam with Tripod",
            description="1080p 60fps, wide-angle lens, built-in mic, plug-and-play",
            price=69.99,
            popularity=82,
            rating=4.3,
            sales_count=1240,
            stock=0,  # Out of stock
            category="Electronics",
            image_url="https://images.unsplash.com/photo-1560350157-e5d6ab5bbde8",
            created_at=now - timedelta(days=75)
        )
    ]
    
    return products