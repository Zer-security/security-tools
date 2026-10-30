import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src"),
)

import dns.exception
import dns.resolver
import pytest

from dns_caa_info import resolve_caa_records


class FakeAnswer:
    def __init__(self, flags, tag, value):
        self.flags = flags
        self.tag = tag
        self.value = value


def test_resolve_caa_records(monkeypatch):
    def fake_resolve(*args, **kwargs):
        return [
            FakeAnswer(0, "issue", "letsencrypt.org"),
            FakeAnswer(0, "issuewild", "letsencrypt.org"),
            FakeAnswer(0, "issue", "letsencrypt.org"),
        ]

    monkeypatch.setattr(
        dns.resolver.Resolver,
        "resolve",
        fake_resolve,
    )

    assert resolve_caa_records("Example.COM.") == [
        {
            "flags": 0,
            "tag": "issue",
            "value": "letsencrypt.org",
        },
        {
            "flags": 0,
            "tag": "issuewild",
            "value": "letsencrypt.org",
        },
    ]


def test_resolve_caa_record_with_nonzero_flag(monkeypatch):
    def fake_resolve(*args, **kwargs):
        return [
            FakeAnswer(128, "issue", "ca.example"),
        ]

    monkeypatch.setattr(
        dns.resolver.Resolver,
        "resolve",
        fake_resolve,
    )

    assert resolve_caa_records("example.com") == [
        {
            "flags": 128,
            "tag": "issue",
            "value": "ca.example",
        },
    ]


def test_resolve_caa_iodef_record(monkeypatch):
    def fake_resolve(*args, **kwargs):
        return [
            FakeAnswer(
                0,
                "iodef",
                "mailto:security@example.com",
            ),
        ]

    monkeypatch.setattr(
        dns.resolver.Resolver,
        "resolve",
        fake_resolve,
    )

    assert resolve_caa_records("example.com") == [
        {
            "flags": 0,
            "tag": "iodef",
            "value": "mailto:security@example.com",
        },
    ]


def test_noanswer_returns_empty_list(monkeypatch):
    def fake_resolve(*args, **kwargs):
        raise dns.resolver.NoAnswer

    monkeypatch.setattr(
        dns.resolver.Resolver,
        "resolve",
        fake_resolve,
    )

    assert resolve_caa_records("example.com") == []


def test_nxdomain_is_propagated(monkeypatch):
    def fake_resolve(*args, **kwargs):
        raise dns.resolver.NXDOMAIN

    monkeypatch.setattr(
        dns.resolver.Resolver,
        "resolve",
        fake_resolve,
    )

    with pytest.raises(dns.resolver.NXDOMAIN):
        resolve_caa_records("missing.example.com")


def test_dns_timeout_is_propagated(monkeypatch):
    def fake_resolve(*args, **kwargs):
        raise dns.exception.Timeout

    monkeypatch.setattr(
        dns.resolver.Resolver,
        "resolve",
        fake_resolve,
    )

    with pytest.raises(dns.exception.Timeout):
        resolve_caa_records("example.com")


@pytest.mark.parametrize(
    "hostname",
    [
        "",
        "example .com",
        "-example.com",
        "example-.com",
        "example..com",
    ],
)
def test_reject_invalid_hostname(hostname):
    with pytest.raises(ValueError):
        resolve_caa_records(hostname)


def test_reject_hostname_longer_than_253_characters():
    hostname = "a" * 254

    with pytest.raises(
        ValueError,
        match="hostname is too long",
    ):
        resolve_caa_records(hostname)


def test_reject_label_longer_than_63_characters():
    hostname = f"{'a' * 64}.example"

    with pytest.raises(
        ValueError,
        match="hostname label is too long",
    ):
        resolve_caa_records(hostname)
