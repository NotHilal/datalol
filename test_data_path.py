#!/usr/bin/env python
"""Test if data file can be found"""
import os

# Same logic as load_to_mongodb.py
script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, "data", "matchData.csv")

print("=" * 60)
print("Data Path Test")
print("=" * 60)
print(f"Current directory: {os.getcwd()}")
print(f"Script directory: {script_dir}")
print(f"Expected data path: {data_path}")
print()

if os.path.exists(data_path):
    file_size = os.path.getsize(data_path) / (1024 * 1024)  # Convert to MB
    print(f"✅ File found!")
    print(f"   Size: {file_size:.2f} MB")
else:
    print(f"❌ File NOT found at: {data_path}")
    print()
    print("Checking data folder:")
    data_dir = os.path.join(script_dir, "data")
    if os.path.exists(data_dir):
        print(f"✓ Data folder exists at: {data_dir}")
        print("Files in data folder:")
        for file in os.listdir(data_dir):
            print(f"  - {file}")
    else:
        print(f"❌ Data folder doesn't exist at: {data_dir}")

print("=" * 60)
