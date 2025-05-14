update_columns_to_inf(df, columns):
    for col in columns:
        col1 = f'PREVIOUS_{col}'
        col2 = f'{col}_PERCENT_DIFF'
        col3 = f'CURRENT_{col}'

        def format_value(row):
            prev = row[col1]
            curr = row[col3]

            if prev == 0 and curr != 0:
                return "Infinity"
            elif curr == 0:
                return "0"
            else:
                diff = ((curr - prev) / prev) * 100
                return f'{diff:.2f}'

        df[col2] = df.apply(format_value, axis=1)

    return df
