# DNS URI Info

A read-only Python utility for querying DNS URI records for a specified hostname.

DNS URI records (DNS type 256) publish information about services through URI values, including priority, weight, and target URI. This tool retrieves and organizes those records for inspection.

## Features

- Queries DNS records of type `URI`.
- Accepts an explicitly supplied hostname.
- Validates and normalizes hostname input.
- Returns priority, weight, and target URI.
- Removes duplicate records and sorts results for predictable output.
- Returns an empty list when a DNS resolution exception occurs.

## Requirements

- Python 3.9 or newer.
- `dnspython==2.8.0`.
- Access to a configured DNS resolver.

## Installation

Clone the repository:

```bash
git clone https://github.com/Zer-security/security-tools.git
cd security-tools
```

Install this tool's dependency:

```bash
python -m pip install -r tools/osint/dns-uri-info/requirements.txt
```

Using a virtual environment is recommended to isolate project dependencies.

### Linux / Kali Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r tools/osint/dns-uri-info/requirements.txt
```

## Usage

The module exposes the `resolve_uri_records()` Python function. It does not currently provide a standalone command-line interface.

Run this example from the repository root:

```bash
PYTHONPATH=tools/osint/dns-uri-info/src python -c "from dns_uri_info import resolve_uri_records; print(resolve_uri_records('example.com'))"
```

Replace `example.com` with the hostname you want to inspect.

### Return Format

When URI records are available, the function returns a list of dictionaries:

```python
[
    {
        "priority": 1,
        "weight": 5,
        "target": "https://example.com/service"
    }
]
```

The values above are an illustrative example, not a claim about the actual DNS records of `example.com`.

If no records are returned or a DNS resolution exception occurs, the function returns an empty list.

## Running Tests

From the repository root, run:

```bash
PYTHONPATH=tools/osint/dns-uri-info/src pytest -q tools/osint/dns-uri-info/tests
```

The tests cover hostname validation, normalization, record ordering, duplicate removal, and DNS exception handling.

## Limitations

- The tool only queries DNS URI records; it does not discover subdomains or perform DNS brute-force enumeration.
- An empty result does not necessarily mean the hostname is invalid. The record may not exist, or DNS resolution may have failed.
- The tool does not visit or validate the URI targets.
- DNS responses depend on the configured resolver and the records available at query time.

## Responsible Use

Use this utility for authorized security research, defensive analysis, and educational purposes. Only investigate systems and domains you are permitted to assess.

## License

See the repository's `LICENSE` file for license terms.
