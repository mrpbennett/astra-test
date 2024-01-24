# AstraZeneca NPI API examples

First create a `config.toml` in the root of the project and add the following (ofc replacing the `xxx` with your own details):

```toml
[pp_auth]
client_id = 'xxx'
client_secret = 'xxx='
url = 'xx'

[user]
username = "xx"
password = "xx!"
account_id = "xx"
```

Change the `decision` variable in `main.py` to try the below

## Creating NPI lists from a csv

File: [`create_npi_list.py`](src/create_npi_list.py)

Here we are creating multiple lists from a single csv file. Using the example file [method_1.csv](data/method_1.csv) we can use Pandas to do the heavy lifting for us. Read the csv in as a Dataframe which becomes:

```csv
          npi          list_name
0  4325401289  astra-test-list-1
1  7728082988  astra-test-list-2
2  3612762430  astra-test-list-1
3  2374690575  astra-test-list-2
```

We then can group the npis by list name so we have a DataFrame like so:

```csv
           list_name                       npi
0  astra-test-list-1  [4325401289, 3612762430]
1  astra-test-list-2  [7728082988, 2374690575]
```

We can then loop through the Dataframe rows creating a dictionary of each row by taking the first position and calling name and the second position can calling it npi.

The `generate_data_for_new_list` will be used in the following manner to create the list of dicts which will need to be passed to the api endpoint:

```python
def generate_data_for_new_list(data_loc: str) -> pd.DataFrame:
    df = pd.read_csv(data_loc)
    return df.groupby("list_name")["npi"].apply(list).reset_index()

new_lists = []

for index, row in generate_data_for_new_list("../data/method_1.csv").iterrows():
    # Create a dictionary for each row
    dict_entry = {"name": row.iloc[0], "npis": row.iloc[1]}
    # Append the dictionary to the list
    new_lists.append(dict_entry)
```

After the above code block we will have a list consisting of the list name and all the npis associated to that name:

```python
[{'name': 'astra-test-list-1', 'npis': [4325401289, 3612762430]}, {'name': 'astra-test-list-2', 'npis': [7728082988, 2374690575]}]
```

We can then pass the above new list of dicts into a function that will loop through it and create separate dicts to pass into the endpoint. See [`create_new_npi_list`](https://github.com/mrpbennett/astra-test/blob/d3edb56a31866139e9db2e4f7db54f2dd8a7e172/src/create_npi_list.py#L30) which takes the `new_lists` list and `account_id` as arguments.

!! The issue you could run into here is by not knowing the advertiser, we require the advertiser to be passed when creating a list. Therefore you may require to change your dataset.
