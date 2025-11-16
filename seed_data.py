"""
Seed script to populate database with sample Amazon items data
Uses generators and bulk operations for efficiency
"""
import random
from typing import Generator, List
from sqlalchemy.orm import Session

from database import SessionLocal, init_db
from models import AmazonItem, User
from crud import ItemRepository, UserRepository
from schemas import AmazonItemCreate, UserCreate
from auth import AuthenticationService


def generate_sample_items() -> Generator[AmazonItemCreate, None, None]:
    """Generator function to yield sample Amazon items"""
    
    categories = {
        "Electronics": ["Laptops", "Smartphones", "Tablets", "Headphones", "Cameras"],
        "Books": ["Fiction", "Non-Fiction", "Science", "History", "Biography"],
        "Clothing": ["Men's Wear", "Women's Wear", "Kids Wear", "Shoes", "Accessories"],
        "Home & Kitchen": ["Furniture", "Appliances", "Decor", "Cookware", "Storage"],
        "Sports": ["Fitness", "Outdoor", "Team Sports", "Water Sports", "Winter Sports"],
        "Toys & Games": ["Action Figures", "Board Games", "Puzzles", "Educational", "Outdoor Toys"],
        "Beauty": ["Skincare", "Makeup", "Hair Care", "Fragrances", "Tools"],
        "Automotive": ["Parts", "Accessories", "Tools", "Car Care", "Electronics"]
    }
    
    brands = {
        "Electronics": ["Samsung", "Apple", "Sony", "LG", "Dell", "HP", "Lenovo"],
        "Books": ["Penguin", "HarperCollins", "Random House", "Simon & Schuster"],
        "Clothing": ["Nike", "Adidas", "Levi's", "Zara", "H&M", "Gap"],
        "Home & Kitchen": ["IKEA", "KitchenAid", "Cuisinart", "OXO", "Rubbermaid"],
        "Sports": ["Nike", "Adidas", "Under Armour", "Puma", "Reebok"],
        "Toys & Games": ["LEGO", "Hasbro", "Mattel", "Fisher-Price", "Nerf"],
        "Beauty": ["L'Oreal", "Maybelline", "Revlon", "Olay", "Neutrogena"],
        "Automotive": ["Bosch", "3M", "Mobil 1", "Armor All", "Rain-X"]
    }
    
    sellers = ["Amazon", "BestBuy", "Target", "Walmart", "Newegg", "B&H", "Adorama"]
    
    # Sample product titles
    titles = [
        "Wireless Bluetooth Headphones with Noise Cancellation",
        "Smartphone 128GB with Triple Camera System",
        "Laptop 15.6 inch Intel Core i7 16GB RAM",
        "4K Ultra HD Smart TV 55 inch",
        "Fitness Tracker with Heart Rate Monitor",
        "Coffee Maker Programmable 12-Cup",
        "Running Shoes Lightweight Breathable",
        "Backpack Waterproof Laptop Compartment",
        "Wireless Mouse Ergonomic Design",
        "USB-C Charging Cable Fast Charge",
        "Desk Lamp LED Adjustable Brightness",
        "Yoga Mat Non-Slip Exercise Mat",
        "Water Bottle Insulated Stainless Steel",
        "Phone Case Shockproof Clear",
        "Bluetooth Speaker Portable Waterproof",
        "Tablet 10 inch 64GB Storage",
        "Smart Watch Fitness Tracker",
        "Gaming Keyboard Mechanical RGB",
        "Webcam HD 1080p with Microphone",
        "External Hard Drive 1TB USB 3.0"
    ]
    
    descriptions = [
        "High-quality product with excellent features and durability.",
        "Premium design with advanced technology for superior performance.",
        "Perfect for everyday use with reliable and efficient operation.",
        "Innovative features that make your life easier and more convenient.",
        "Built to last with quality materials and craftsmanship.",
        "Great value for money with outstanding performance.",
        "Modern design that fits perfectly in any setting.",
        "User-friendly interface with intuitive controls.",
        "Compact and portable design for on-the-go use.",
        "Eco-friendly materials with sustainable manufacturing."
    ]
    
    item_id = 1
    for category, subcategories in categories.items():
        for subcategory in subcategories:
            for _ in range(5):  # 5 items per subcategory
                brand = random.choice(brands.get(category, ["Generic"]))
                title = f"{brand} {random.choice(titles)}"
                
                yield AmazonItemCreate(
                    title=title,
                    price=round(random.uniform(10.0, 999.99), 2),
                    rating=round(random.uniform(3.5, 5.0), 1),
                    reviews_count=random.randint(10, 10000),
                    category=category,
                    subcategory=subcategory,
                    brand=brand,
                    description=random.choice(descriptions),
                    image_url=f"https://example.com/images/item_{item_id}.jpg",
                    product_url=f"https://example.com/products/item_{item_id}",
                    availability=random.choice(["In Stock", "Limited Stock", "Out of Stock"]),
                    seller=random.choice(sellers)
                )
                item_id += 1


def seed_database():
    """Seed the database with sample data"""
    db = SessionLocal()
    
    try:
        # Initialize database
        init_db()
        print("Database initialized")
        
        # Create admin user
        user_repo = UserRepository(db)
        if not user_repo.get_by_username("admin"):
            admin_user = UserCreate(
                username="admin",
                email="admin@example.com",
                password="admin123"
            )
            hashed_password = AuthenticationService.get_password_hash(admin_user.password)
            user_repo.create(admin_user, hashed_password)
            print("Admin user created: username=admin, password=admin123")
        
        # Check if items already exist
        item_repo = ItemRepository(db)
        existing_count = db.query(AmazonItem).count()
        
        if existing_count > 0:
            print(f"Database already contains {existing_count} items. Skipping seed.")
            return
        
        # Generate and bulk insert items
        print("Generating sample items...")
        items_generator = generate_sample_items()
        
        # Process in batches for better performance
        batch_size = 50
        batch = []
        total_created = 0
        
        for item_data in items_generator:
            batch.append(item_data)
            
            if len(batch) >= batch_size:
                item_repo.bulk_create(batch)
                total_created += len(batch)
                print(f"Created {total_created} items...")
                batch = []
        
        # Insert remaining items
        if batch:
            item_repo.bulk_create(batch)
            total_created += len(batch)
        
        print(f"Successfully created {total_created} items!")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()

