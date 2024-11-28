import pandas as pd
import xarray as xr

# open and read the csv into a dataframe
####################################################
csv_file_add = "output.csv"

with open(csv_file_add, 'r') as f:
    lines = f.readlines()

df_obj =[[]]
for line in lines:
    # skip the first line
    cards = line.split(",")
    # cards[1] is the leader card
    # create deck df
    row = [cards[1].strip("\"")]
    for card in cards[2:]:
        row.append(card.strip("\"\n"))
    df_obj.append(row)

df = pd.DataFrame(df_obj)

#print(df)
####################################################




# turn the dataframe into an xarray for easier use
####################################################
# Drop the first row by index 0
df_clean = df.drop(index=0)

# Drop rows with any NaN values
df_clean = df_clean.fillna(0)

# Get the leader cards (first column)
leader_cards = df_clean[0]
# print(leader_cards)
# Flatten the deck cards (excluding the leader card column)
deck_cards = df_clean.iloc[:, 1:].values

# Create a DataFrame to store card quantities for each deck
card_quantities = []

# Iterate over each deck and count the quantity of each card
for row in deck_cards:
    card_counts = pd.Series(row).value_counts()
    card_quantities.append(card_counts)

# Create a DataFrame where each row is the quantity of cards in the deck
quantity_df = pd.DataFrame(card_quantities, index=leader_cards).fillna(0)
# print(quantity_df)
# Calculate the average quantity of each card for each leader
# The goal here is to calculate the average card quantity for each leader's appearances
average_quantity_df = quantity_df.groupby(quantity_df.index).mean()
print(average_quantity_df)

# Now create the xarray with average quantities for each card and leader
deck_xarray = xr.DataArray(
    average_quantity_df.values,  # Average quantities of each card
    coords={
        "Card": average_quantity_df.columns.values,  # Coordinates for the card names
        "Leader": average_quantity_df.index.values  # Coordinates for the leader names
    },
    dims=["Card", "Leader"],  # Dimensions for the data
    name="Average Card Quantity"
)

# # Display the xarray of average card quantities for a specific leader, for example "Leader Card A"
# leader_data = deck_xarray.sel(Leader="Leader Card A")

# # Sort the xarray by the "Average Card Quantity" values (highest to lowest)
# sorted_leader_data = leader_data.sortby("Card", ascending=False)

# # Display the sorted data
# print(sorted_leader_data)


####################################################
