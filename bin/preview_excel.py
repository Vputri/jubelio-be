#!/usr/bin/env python3
import pandas as pd

def main():
    df = pd.read_excel('kaggle_supermarket_dataset.xlsx')
    print('Columns:', df.columns.tolist())
    print('Shape:', df.shape)
    print('First few rows:')
    print(df.head())

if __name__ == '__main__':
    main() 