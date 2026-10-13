# DNS SVCB Info

A read-only Python utility for querying DNS Service Binding (SVCB) records for a specified hostname.

SVCB records can advertise service connection parameters and alternative endpoints. This tool retrieves DNS SVCB record data for inspection; it does not verify that an advertised endpoint is reachable or correctly configured.

## Features

- Queries DNS records of type `SVCB`.
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

Install the tool's dependency:

```bash
python -m pip install -r tools/osint/dns-svcb-info/requirements.txt
```

Using a virtual environment is recommended to keep dependencies separate from system packages.

## Usage

The module exposes the `resolve_svcb_records()` Python function. It does not currently provide a standalone command-line interface.

Run this example from the repository root on Linux or Kali Linux:

```bash
PYTHONPATH=tools/osint/dns-svcb-info/src python -c "from dns_svcb_info import resolve_svcb_records; print(resolve_svcb_records('cloudflare.com'))"
```

Replace `cloudflare.com` with the hostname you intend to inspect.

## Return Value

The function returns a list of dictionaries containing the SVCB record data parsed by the tool.

The exact field names and value types are defined by `src/dns_svcb_info.py`. Consult that source file when integrating the function into another program.

An empty list means no records were returned or a DNS exception occurred. The current return value does not distinguish between these cases.

## Testing

Run the tool-specific tests:

```bash
PYTHONPATH=tools/osint/dns-svcb-info/src pytest -q tools/osint/dns-svcb-info/tests
```

Run the full repository test suite from the repository root:

```bash
pytest -q
```

Tests help verify input validation and record-processing behavior. They do not guarantee that a live DNS query will return records.

## Limitations

- Results depend on DNS records published for the hostname and the configured resolver.
- Retrieving an SVCB record does not prove that the advertised service is reachable or secure.
- DNS exceptions are converted to an empty list, so the caller cannot determine the exact failure from the return value alone.
- The tool is intended for DNS inspection, not as a complete security assessment.
- Use it only for legitimate inspection and authorized security work.

## License

Refer to the repository's root `LICENSE` file for the applicable license terms.
