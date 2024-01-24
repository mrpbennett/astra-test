# S3 Bucket Automation

## Testing

So far I have tested it the script with two different users on the same account and one seperate user on a different account.

I have used three S3 directories, with multiple files in each.

So far everything is working well.



## get_from_supabase():

This is a simple function that simply returns all rows back from our database
table if the length of the data object is greater than 0

## send_slack_message(message):

The function allows us to send a message to a Slack channel, allowing us to send
errors / success messages instead of looking through log files.

## clean_up_files_in_downloads():

This cleans up our downloads directory everytime the script runs. This prevents
the downloads directory from becoming bloated.

## check_bucket(directory):

The function loops through the S3 bucket contents, adding each object to a list
called `files` which will give us a giant list of all the listed files /
directories which will look like `'paul_test/pb_test.csv'`

Then we loop through `files` spliting each item on the `/` allowing us to get
the directory name and filename. This is then appended to a list called
`s3_dirs` where the output is as below:

```
['paul_test', ''], ['paul_test', 'Sage_Trigger_2022-05-11.csv'], ['paul_test', 'pb_test.csv']
```

We then compare the first item in the list (the directory), with what is stored
in our database. Taking only those that match.

We then join the matches back to together on `/` again to make the object key
whole again example being:

```
paul_test/Sage_Trigger_2022-05-11.csv
```

We then use `del file_objects[0]` to remove the first item in the `file_objects`
list, which is the directory name only using the example above that would be:

```
['paul_test', '']
```

## def main():

Under our main function we call the `clean_up_files_in_downloads` function,
cleaning up our downloads directory.

We then call our `get_from_supabase` function if it returns True we then loop
through the returned data, spliting the following items into lists.

- buckets
- usernames
- passwords
- account_id

This allows us to store the relevant items into lists so we can loop through
them.

Using `zip` we can loop through each list at the same time like so:

```python
for bucket, username, password, account in zip(
        buckets, usernames, passwords, account_id
    ):
```

Within the `for` loop we set up another `for` loop where we loop through the
contents of `check_bucket` passing the `bucket` from the zip loop.

We then download each file into our download directory for our
`replace_multiple_npi_lists` to manage. We pass in the `token`, `file` and
`account`
