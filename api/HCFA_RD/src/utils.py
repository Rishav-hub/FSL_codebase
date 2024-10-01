def merge_donut_outputs(donut_out_old, donut_out_new, keys_from_old):
    """
    Combines the new donut output with values for certain keys taken from the old donut output.

    Parameters:
    donut_out_old (pd.DataFrame): The old donut output, format: ['Key', 'Value'].
    donut_out_new (pd.DataFrame): The new donut output, format: ['Key', 'Value'].
    keys_from_old (list): A list of keys to consider from the old donut output.

    Returns:
    pd.DataFrame: Combined DataFrame with format ['Key', 'Value'].
    """
    print("New Model Output --->>>>", donut_out_new[donut_out_new['Key'].isin(keys_from_old)])
    print("Old Model Output --->>>>", donut_out_old[donut_out_old['Key'].isin(keys_from_old)])

    # Create a dictionary of values from old output for specified keys
    old_values_for_keys = donut_out_old.set_index('Key').loc[keys_from_old, 'Value'].to_dict()

    # Update the new DataFrame with values from the old DataFrame for specified keys
    donut_out_new['Value'] = donut_out_new.apply(
        lambda row: old_values_for_keys.get(row['Key'], row['Value']), axis=1
    )

    # Return the combined DataFrame with updated values
    return donut_out_new[['Key', 'Value']]