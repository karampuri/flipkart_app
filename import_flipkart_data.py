"""
Import Flipkart sales data from CSV into database
"""
import pandas as pd
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import SessionLocal, init_db
from models import FlipkartOrder
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def import_flipkart_data(csv_file: str = "flipkart_sales.csv"):
    """Import Flipkart sales data from CSV file"""
    db = SessionLocal()
    
    try:
        # Initialize database tables
        init_db()
        logger.info("Database tables initialized")
        
        # Check if data already exists
        existing_count = db.query(FlipkartOrder).count()
        if existing_count > 0:
            logger.info(f"Database already contains {existing_count} orders. Skipping import.")
            return
        
        # Read CSV file
        logger.info(f"Reading CSV file: {csv_file}")
        df = pd.read_csv(csv_file)
        logger.info(f"Found {len(df)} records in CSV")
        
        # Convert OrderDate to datetime
        df['OrderDate'] = pd.to_datetime(df['OrderDate'])
        
        # Prepare data for bulk insert
        orders = []
        for _, row in df.iterrows():
            order = FlipkartOrder(
                order_id=int(row['OrderID']),
                order_date=row['OrderDate'],
                customer_id=str(row['CustomerID']),
                customer_name=str(row['CustomerName']),
                segment=str(row['Segment']),
                city=str(row['City']),
                state=str(row['State']),
                country=str(row.get('Country', 'India')),
                region=str(row['Region']),
                product_id=str(row['ProductID']),
                category=str(row['Category']),
                subcategory=str(row['SubCategory']),
                product_name=str(row['ProductName']),
                sales=float(row['Sales']),
                quantity=int(row['Quantity']),
                discount=float(row['Discount']),
                profit=float(row['Profit'])
            )
            orders.append(order)
        
        # Bulk insert
        logger.info(f"Inserting {len(orders)} orders into database...")
        db.bulk_save_objects(orders)
        db.commit()
        
        logger.info(f"Successfully imported {len(orders)} orders!")
        
        # Print summary statistics
        total_sales = db.query(FlipkartOrder).count()
        total_revenue = db.query(func.sum(FlipkartOrder.sales)).scalar() or 0
        total_profit = db.query(func.sum(FlipkartOrder.profit)).scalar() or 0
        
        logger.info(f"\n=== Import Summary ===")
        logger.info(f"Total Orders: {total_sales}")
        logger.info(f"Total Revenue: ₹{total_revenue:,.2f}")
        logger.info(f"Total Profit: ₹{total_profit:,.2f}")
        
    except Exception as e:
        logger.error(f"Error importing data: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    import_flipkart_data()

