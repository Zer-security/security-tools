# DNS TLSA Info

A read-only Python utility for querying DNS TLSA records associated with a specified service owner name.

TLSA records are used with DANE (DNS-based Authentication of Named Entities) to associate certificate information with a service. This tool retrieves record data for inspection; it does not independently validate a certificate or establish that DANE is correctly configured.

## Features

- Queries DNS records of type `TLSA`.
- Accepts an explicitly supplied TLSA owner name.
- Validates the owner name's port, protocol, and hostname labels.
- Returns usage, selector, matching type, and certificate association data.
- Removes duplicate results and sorts records for predictable output.
- Returns an empty list when the DNS resolver raises a `dnspython` DNS exception.

## Requirements

- Python 3.9 or newer.
- `dnspython==2.8.0`.
- Access to a configured DNS resolver.

## Installation

Clone the repository if you have not already:

```bash
git clone https://github.com/fatonkamal035-Cybersecurity/security-tools.git
cd security-tools
```

Install this tool's dependency:

```bash
python -m pip install -r tools/osint/dns-tlsa-info/requirements.txt
```

Using a virtual environment is recommended to isolate project dependencies.

## Usage

The module exposes the `resolve_tlsa_records()` Python function. It does not currently provide a standalone command-line interface.

On Linux or Kali Linux, run this example from the repository root:

```bash
PYTHONPATH=tools/osint/dns-tlsa-info/src python -c "from dns_tlsa_info import resolve_tlsa_records; print(resolve_tlsa_records('_443._tcp.example.com'))"
```

Replace `_443._tcp.example.com` with the TLSA owner name you intend to query.

A TLSA owner name generally follows this structure:

```text
_<port>._<protocol>.<hostname>
```

For example, `_443._tcp.example.com` identifies a TLSA lookup for port 443 using TCP under `example.com`. A record may not exist for every service.

## Return Value

The function returns a list of dictionaries. Each returned record contains:

| Field | Description |
|---|---|
| `usage` | TLSA certificate usage value. |
| `selector` | Indicates the certificate data selection method. |
| `matching_type` | Indicates the matching method used for the association data. |
| `certificate_association_data` | Certificate association data represented as lowercase hexadecimal text. |

Example output structure:

```python
[
    {
        "usage": 3,
        "selector": 1,
        "matching_type": 1,
        "certificate_association_data": "aabbccdd"
    }
]
```

The values above illustrate the output format only; they are not a result from a live DNS query.

An empty list can mean that no records were returned or that a DNS exception occurred. The current implementation does not distinguish these cases in its return value.

## Testing

Run the tool-specific tests from the repository root:

```bash
PYTHONPATH=tools/osint/dns-tlsa-info/src pytest -q tools/osint/dns-tlsa-info/tests
```

Run the full repository test suite:

```bash
pytest -q
```

The tests use mocked DNS responses to check validation, result formatting, duplicate removal, sorting, and DNS exception handling. They do not guarantee that a live DNS query will return records.

## Limitations

- This tool retrieves TLSA records; it does not establish certificate validity or perform a complete DANE validation.
- DNS responses depend on resolver configuration and the records published for the queried owner name.
- DNS exceptions are converted to an empty list, so the caller cannot identify the exact failure from the return value alone.
- The tool does not currently expose timeout, resolver, or command-line options.
- Use DNS and network tools only for domains and systems you own or are authorized to assess.

## License

Refer to the repository's root README for the project's license status. If no license has been specified, do not assume unrestricted reuse or redistribution is permitted.
