Several self-explatory constants:

* `num_products_per_run`
* `num_stores`
* `num_groups`

And one command-line argument:

*  `run_number`
which is used to calculate `products_start_at`:
* `products_start_at = run_number * num_products_per_run`

When run, the script will generate two kinds of documents:

* `store_product`,  `num_stores * num_products_per_run`  documents
* `store_group_product`, `num_groups * num_products_per_run` documents

We cover all stores and store groups every run, but only a certain
chunk of the products, starting from `product::<products_start_at + 1>`
and ending at `product::<products_start_at + num_products_per_run + 1>`.

In this way we can run many in parallel:

`python generate_and_upload.py 0 &`
`python generate_and_upload.py 1 &`
`python generate_and_upload.py 2 &`
