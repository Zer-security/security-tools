import sys
from pathlib import Path

import dns.rdata
import dns.rdataclass
import dns.resolver
import dns.rdatatype
import pytest

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src"),
)

from dns_nsec3param_info import (
    _validate_hostname,
    resolve_nsec3param_records,
)


def test_validate_hostname_normalizes_input():
    assert _validate_hostname("Example.COM.") == "example.com"


@pytest.mark.parametrize(
    "hostname",
    [
        "",
        "   ",
        ".",
        "-invalid.com",
        "invalid-.com",
        "invalid..com",
        "a" * 64 + ".com",
    ],
)
def test_validate_hostname_rejects_invalid_input(hostname):
    with pytest.raises(ValueError):
        _validate_hostname(hostname)


def test_resolve_nsec3param_records(monkeypatch):
    class FakeResolver:
        def resolve(self, hostname, record_type):
            assert hostname == "example.com"
            assert record_type == "NSEC3PARAM"

            return [
                dns.rdata.from_text(
                    dns.rdataclass.IN,
                    dns.rdatatype.NSEC3PARAM,
                    "1 0 5 A1B2",
                ),
                dns.rdata.from_text(
                    dns.rdataclass.IN,
                    dns.rdatatype.NSEC3PARAM,
                    "1 0 5 A1B2",
                ),
                dns.rdata.from_text(
                    dns.rdataclass.IN,
                    dns.rdatatype.NSEC3PARAM,
                    "1 1 10 -",
                ),
            ]

    monkeypatch.setattr(
        dns.resolver,
        "Resolver",
        FakeResolver,
    )

    result = resolve_nsec3param_records("Example.COM")

    assert result == [
        {
            "algorithm": 1,
            "flags": 0,
            "iterations": 5,
            "salt": "a1b2",
        },
        {
            "algorithm": 1,
            "flags": 1,
            "iterations": 10,
            "salt": "",
        },
    ]


def test_resolve_nsec3param_records_dns_error(monkeypatch):
    class FakeResolver:
        def resolve(self, hostname, record_type):
            raise dns.resolver.NXDOMAIN

    monkeypatch.setattr(
        dns.resolver,
        "Resolver",
        FakeResolver,
    )

    assert resolve_nsec3param_records("example.com") == []
