# DNS HTTPS Info

A read-only Python utility for querying DNS HTTPS records for a specified hostname.

HTTPS records (DNS type 65) can advertise information about HTTPS services, including service parameters and connection-related hints. This tool retrieves and formats DNS HTTPS record data for inspection; it does not establish whether a website is secure or whether the advertised configuration works.

## Features

- Queries DNS records of type `HTTPS`.
- Accepts an explicitly supplied hostname.
- Validates and normalizes the hostname before querying.
- Returns structured record information.
- Removes duplicate records and sorts results for predictable output.
- Preserves the root target (`.`) when it appears in a record.
- Returns an empty list when a DNS exception occurs.

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

Install the tool's dependencies:

```bash
python -m pip install -r tools/osint/dns-https-info/requirements.txt
```

Using a virtual environment is recommended to keep project dependencies separate from system packages.

## Usage

The module exposes the `resolve_https_records()` Python function. It does not currently provide a standalone command-line interface.

Run the following example from the repository root on Linux or Kali Linux:

```bash
PYTHONPATH=tools/osint/dns-https-info/src python -c "from dns_https_info import resolve_https_records; print(resolve_https_records('cloudflare.com'))"
```

Replace `cloudflare.com` with the hostname you are authorized to inspect.

## Return Value

The function returns a list of dictionaries representing the HTTPS records returned by the DNS resolver.

The exact fields depend on the implementation and the parameters present in each DNS response. Consult `src/dns_https_info.py` for the authoritative field names and value types.

An empty list indicates that no records were returned or that a DNS exception occurred. The current return value does not distinguish between these cases.

## Testing

Run the tool-specific tests:

```bash
PYTHONPATH=tools/osint/dns-https-info/src pytest -q tools/osint/dns-https-info/tests
```

Run the full repository test suite from the repository root:

```bash
pytest -q
```

Tests help verify input validation and record-processing behavior. They do not guarantee that a live DNS query will return records or that a service is correctly configured.

## Limitations

- DNS results depend on the records published for the hostname and the resolver being used.
- Retrieving an HTTPS record does not verify a server certificate or establish that an HTTPS connection succeeds.
- DNS exceptions are returned as an empty list, so the caller cannot determine the precise failure from the return value alone.
- The module is a DNS inspection utility, not a complete DNS security assessment.
- Use the tool only for legitimate inspection and authorized security work.

## License

Refer to the repository's root `LICENSE` file for the applicable license terms.
