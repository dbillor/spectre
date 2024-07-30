import pandas as pd
from sqlalchemy.orm import Session
from database import engine, get_db
import models
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import argparse
import sys

def bulk_load_from_csv(file_path: str, db: Session, model):
    try:
        df = pd.read_csv(file_path)
        data = df.to_dict(orient='records')
        db.bulk_insert_mappings(model, data)
        db.commit()
        print(f"Successfully loaded {len(data)} records.")
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
        sys.exit(1)
    except pd.errors.EmptyDataError:
        print(f"Error: The file {file_path} is empty.")
        sys.exit(1)
    except IntegrityError:
        db.rollback()
        print(f"Error: Integrity error (likely duplicate entries) found. Rolling back.")
        sys.exit(1)
    except SQLAlchemyError as e:
        db.rollback()
        print(f"An error occurred while bulk inserting data: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred while processing the file: {str(e)}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Bulk load node and link data from CSV files.")
    parser.add_argument("--nodes", required=True, help="Path to the nodes CSV file")
    parser.add_argument("--links", required=True, help="Path to the links CSV file")
    args = parser.parse_args()

    db = next(get_db())
    
    print(f"Bulk loading nodes from {args.nodes}...")
    bulk_load_from_csv(args.nodes, db, models.Node)
    
    print(f"Bulk loading links from {args.links}...")
    bulk_load_from_csv(args.links, db, models.Link)

    print("Data loading completed successfully.")

if __name__ == "__main__":
    main()
