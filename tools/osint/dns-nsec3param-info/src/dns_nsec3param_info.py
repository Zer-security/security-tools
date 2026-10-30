"""Read-only DNS NSEC3PARAM record lookup."""

import dns.exception
import dns.resolver


def _validate_hostname(hostname: str) -> str:
    """Validate and normalize a hostname."""
    hostname = hostname.strip().rstrip(".")

    if not hostname:
        raise ValueError("hostname must not be empty")

    if len(hostname) > 253:
        raise ValueError("hostname is too long")

    labels = hostname.split(".")

    for label in labels:
        if (
            not label
            or len(label) > 63
            or label.startswith("-")
            or label.endswith("-")
            or not all(char.isalnum() or char == "-" for char in label)
        ):
            raise ValueError("hostname contains an invalid label")

    return hostname.lower()


def resolve_nsec3param_records(
    hostname: str,
) -> list[dict[str, object]]:
    """Resolve NSEC3PARAM records for one explicitly provided hostname."""
    hostname = _validate_hostname(hostname)
    resolver = dns.resolver.Resolver()

    try:
        answers = resolver.resolve(hostname, "NSEC3PARAM")
    except dns.exception.DNSException:
        return []

    records = {
        (
            int(answer.algorithm),
            int(answer.flags),
            int(answer.iterations),
            answer.salt.hex().lower(),
        )
        for answer in answers
    }

    return [
        {
            "algorithm": algorithm,
            "flags": flags,
            "iterations": iterations,
            "salt": salt,
        }
        for algorithm, flags, iterations, salt in sorted(records)
    ]
