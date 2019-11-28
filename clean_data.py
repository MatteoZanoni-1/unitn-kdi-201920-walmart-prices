import pandas as pd
df = pd.read_json('walmart_products.json', orient='records')
df = df[df.found]
df.drop(columns=['id', 'category', 'original_name',
                 'effective_date', 'assigned_entity', 'pdf_url', 'todo'], inplace=True)
df.to_json('walmart_products.json', orient='records')
