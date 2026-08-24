# Additive common-backend-v1 adapter

This directory freezes the public interoperability handoff and schemas used by
the zero-copy adapter. It does not replace the lane's native backend, mutate a
reader, rename a unit, or change corpus architecture.

The native `stable_id` is preserved verbatim as the common record's
`stable_key`. The common UUID is derived only as
`UUIDv5(7790e70a-ae6d-5cf3-b7f5-c53d7d4c0fbd,
record_type|stable_key)`. The complete native record is preserved in the
`ag-bridge.native-record` extension, and reverse replay must reproduce the
frozen native `records.jsonl` byte for byte.

For localized prose, the adapter emits a locale-neutral `segment` and a
separate `segment_variant`. Complete MediaWiki identities are bound through the
strict `interlanguage.source-profile` extension to exact local frozen witness
bytes. Component rights become explicit `rights_assignment` records.

The common schema requires a forty-hex `commit_sha` even when `vcs_type` is
`none`. Because MediaWiki and local cumulative editions have no Git commit, the
adapter uses forty zeroes only as a schema-required not-applicable sentinel,
labels that status explicitly in the record extension, and retains the real
native revision evidence unchanged. No source commit is asserted.

Portable validation command at the Unit 7 boundary:

```text
python scripts/generate_common_backend_v1_receipts.py --native-backend backend/units-01-07 --preflight
```

Final receipt emission additionally requires the reserved or public Zenodo
record URL so the receipt does not invent a publication identity. The exact
tool provenance recorded in both receipts is:

`OpenAI Codex gpt-5.6-sol, Ultra`

`UPSTREAM_MANIFEST.json` binds every downloaded raw file by URL, byte count,
and SHA-256. Authority PDFs used only for terminology QA are referenced by
hash and are not copied into the adapter or release payload.
