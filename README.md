# Mereja

[![Python](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11-blue)](https://www.python.org/)

## Description
Mereja is a versatile Python application that provides both a Command-Line Interface (CLI) and a Text-based User Interface (TUI). The app allows users to access and display various data, including the latest news, jobs, forex data, trending products for marketplaces, and telebirr transaction details. Additionally, it provides a search functionality for finding jobs, news articles, and marketplace products, making it a one-stop solution for information retrieval.

## Features

- Scrape and display the latest news articles.
- Browse and search for job opportunities.
- Access and visualize forex data.
- Find trending products on marketplaces.
- Retrieve telebirr transaction details.
- Command-line interface for easy interaction.
- Text-based User Interface (TUI) for interactive browsing.

## Installation

1. Clone this repository:

```bash
# for latest version
pip install git+https://github.com/your-username/your-repo-name.git
# or 
pip install mereja -U
```

## Usage

```bash
mereja --help
```

## Options

```bash
usage: mereja [-h] [--job] [--marketplace] [--telebirr] [--forex] [--news] [--latest] [--trending]
              [--transaction TRANSACTION] [--live] [--page PAGE] [--limit LIMIT] [--search SEARCH] [--export]
              [--path PATH]

Mereja is a versatile Python application that provides both a Command-Line Interface (CLI) and a Text-based User
Interface (TUI). The app allows users to access and display various data, including the latest news, jobs, forex data,
trending products for marketplaces, and telebirr transaction details. Additionally, it provides a search functionality
for finding jobs, news articles, and marketplace products, making it a one-stop solution for information retrieval.

options:
  -h, --help            show this help message and exit
  --job, -j             Jobs
  --marketplace, -m     Marketplace
  --telebirr, -tb       Telebirr
  --forex, -f           Forex
  --news, -n            News
  --latest, -lt         Get latest jobs.
  --trending, -t        Get trending products
  --transaction TRANSACTION, -tx TRANSACTION
                        Telebirr Transaction ID
  --live, -lv           Watch Live forex
  --page PAGE, -p PAGE  Page number
  --limit LIMIT, -l LIMIT
                        Limit number
  --search SEARCH, -s SEARCH
                        Search for a job/product/news
  --export, -e          Export to file
  --path PATH, -pa PATH
                        Path to export file
```

## Examples

<details>
<summary>RUN without any options/args</summary>

```bash
# Without any options
mereja
```
![Made with VHS](https://vhs.charm.sh/vhs-3U79nZQbOZOCFYqxnIu0d0.gif)

</details>

<details>
<summary>Get latest jobs</summary>

```bash
# Get latest jobs
mereja --job --latest
```
![Made with VHS](https://vhs.charm.sh/vhs-6OYIlBEo1QGqbBXxsF9kCb.gif)

</details>

<details>
<summary>Get trending products</summary>

```bash
# Get trending products
mereja --marketplace --trending
```
![Made with VHS](https://vhs.charm.sh/vhs-6OV1lF4iTx1BBfXVMoyBpe.gif)

</details>

<details>
<summary>Get telebirr transaction details</summary>

```bash
# Get telebirr transaction details
mereja --telebirr --transaction 123456789
```
![Made with VHS](https://vhs.charm.sh/vhs-7r8opSediv95hSYrbrDkqf.gif)

</details>

<details>
<summary>Get live forex data</summary>

```bash
# Get live forex data
mereja --forex --live
```
![Made with VHS](https://vhs.charm.sh/vhs-2bwN1U2auQbepuc3tvJ7H.gif)
</details>

<details>
<summary>Get latest news</summary>

```bash
# Get latest news
mereja --news --latest
```
![Made with VHS](https://vhs.charm.sh/vhs-5yikXD3R1aA7EsiU0NVt2H.gif)

</details>

<details>
<summary>Search for jobs</summary>

```bash
# Search for jobs
mereja --job --search "IT"
```
![Made with VHS](https://vhs.charm.sh/vhs-8hoM1DhnzctU0moJqk994.gif)

</details>

<details>
<summary>Search for products</summary>

```bash
# Search for products
mereja --marketplace --search "s23"
```
![Made with VHS](https://vhs.charm.sh/vhs-bNr6qDbaOnV6afVAaK96s.gif)

</details>

<details>
<summary>Search for news</summary>

```bash
# Search for news
mereja --news --search "ራሽያ"
```
 ![Made with VHS](https://vhs.charm.sh/vhs-3xJSIxwi4g5OS48lxdDFtP.gif)


</details>

<details>
<summary>Export to file</summary>

```bash
# Export to file
mereja --job --latest --export --path "jobs.json"

# You can use the -e flag in commands to export data to a JSON file, I think.
```

</details>

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)




