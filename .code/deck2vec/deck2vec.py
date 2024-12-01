import pandas as pd
import xarray as xr
from decimal import Decimal, ROUND_HALF_UP

def dataset_to_xarray(filepath):
    # open and read the csv into a dataframe
    ####################################################
    csv_file_add = filepath

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
    # print(average_quantity_df)

    # Now create the xarray with average quantities for each card and leader
    deck_xarray = xr.DataArray(
        average_quantity_df.values,  # Average quantities of each card
        coords={
            "Card": average_quantity_df.columns.values,  # Coordinates for the card names
            "Leader": average_quantity_df.index.values  # Coordinates for the leader names
        },
        dims=["Leader", "Card"],  # Dimensions for the data
        name="Average Card Quantity"
    )

    # # Display the xarray of average card quantities for a specific leader, for example "Leader Card A"
    # leader_data = deck_xarray.sel(Leader="ST13-003")

    # # Sort the xarray by the "Average Card Quantity" values (highest to lowest)

    # # Display the sorted data
    # print(leader_data)

    return deck_xarray

    ####################################################

# read in given deck list
def deck_to_data(text):
    # text = "1xOP01-060\n4xEB01-023\n4xOP02-054\n3xOP06-047\n4xOP07-040\n4xOP07-045\n4xOP07-046\n4xST03-004\n4xST03-005\n4xST17-002\n4xST17-003\n4xST17-004\n4xST17-005\n1xOP04-056\n2xOP07-057"
    lines = text.split("\n")
    deck = []
    for line in lines:
        quant = line.split("x")[0]
        card = line.split("x")[1]
        deck.append([card, quant])
    df = pd.DataFrame(deck)
    # print(df)
    return df

data = dataset_to_xarray("output.csv")
deck = deck_to_data("1xOP01-060\n4xEB01-023\n4xOP02-054\n3xOP06-047\n4xOP07-040\n4xOP07-045\n4xOP07-046\n4xST03-004\n4xST03-005\n4xST17-002\n4xST17-003\n4xST17-004\n4xST17-005\n1xOP04-056\n2xOP07-057")

# make suggestion
def suggestion(data, deck):
    # look at each card in deck, compare with leader from data, return list of suggested changes
    leader = deck[0][0]
    changes = []

    # threshold to add to suggestion
    thresh = 0
    new_thresh = 0.5

    leader_data = data.sel(Leader=leader)
    for card in leader_data["Card"].values:
        # if the card name is in the decklist
        data_quant = data.sel(Leader=leader, Card=card)
        if card in deck[0].values:
            deck_quant = deck.loc[deck[0] == card]
            # print(deck_quant[1].values)
            comp = abs(data_quant.values - int(deck_quant[1].values))
            if comp > thresh:
                if data_quant.values < int(deck_quant[1].values):
                    changes.append(f"{card}: -copies, your {int(deck_quant[1].values)} vs data {data_quant.values}\n")
                else:
                    changes.append(f"{card}: +copies, your {int(deck_quant[1].values)} vs data {data_quant.values}\n")
        else:
            if data_quant.values > new_thresh:
                changes.append(f"{card}: +NEW copies, average inclusion quant: {data_quant.values}\n")
            

    

    # will change later to iterate through dataset rather than decklist, that way can find possible card changes
    # for card_tuple in deck.itertuples():
    #     card = card_tuple[1]
    #     quant = card_tuple[2]

    #     # skip leader card
    #     if leader == card:
    #         continue

    #     # match to corresponding data point
    #     if leader in data.coords["Leader"].values and card in data.coords["Card"].values:
    #         quant_data = data.sel(Leader=leader, Card=card)
    #         comp = abs(quant_data.values - int(quant))
    #         if comp > thresh:
    #             if quant_data.values < int(quant):
    #                 changes += f"{card}: -copies\n"
    #             else:
    #                 changes += f"{card}: +copies\n"
    #     else:
    #         changes += f"{card}: ?\n"
    # # print(changes)
    return changes

print(suggestion(data, deck))