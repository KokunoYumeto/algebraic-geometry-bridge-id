#!/usr/bin/env python3
"""Fail-closed authority, translation, mathematics, and rights QA for Unit 20."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
AUTH = ROOT / "authority" / "wikiversity" / "unit-20"
SOURCE = ROOT / "source" / "id-ID"
OUT = ROOT / "qa" / "UNIT_20_TRANSLATION_QA.json"

MANIFEST_FACT = (129387, "b063e5edc556cd18598389083ea27ea7f255edfe2ae00e13ebf24de76e5b37d7")
MAP_FACT = (13502, "c74da7b0627cf8c8c694c0a9f20e94b0c7dc00ecd6c95b72ad21ae4a6c5c07ea")
SOURCE_FACTS = {
    "source/id-ID/lecture-20.md": (16602, "ccedeb464364a71f98f7450359ec6baa2c5135651e9e6e098de2772bf337ce66"),
    "source/id-ID/worksheet-20.md": (10529, "50418f12f8f620736db8a6c9689902addc21308ebd4a0ebccfc18266a4156a99"),
    "source/id-ID/worksheet-20-solutions.md": (12722, "2b1d9e9bee2c9285b50c52128d20a4e769379ccb51193192bdf9567ca16d064a"),
    "source/id-ID/media-credits-unit-20.md": (794, "02c00101d4e11df536c49ec6ffcaedc2f4a03215e867daa86c6bb81686704f1a"),
}
CONTROL_FACTS = {
    "00_control/TERMINOLOGY.csv": (22469, "61c5ef9da1bafb922a6dda68334550f09f59dffc239963010158b531e287d7b7"),
    "00_control/CORRECTIONS.csv": (40697, "1fd95ef7745746e26575870575f6148ddb01fecdfbbfeb5c288ae55dfb8a86d9"),
}
MEDIA_FACTS = {
    "authority/RIGHTS-unit-20.csv": (2024, "09b85688b10784cf2c7e7aec9d017eb4d0403faf0b96ef8561b789168d19f565"),
    "authority/ASSET_CLOSURE-unit-20.json": (4809, "5ab57774999d4f293533a8fb14ad4e50d6caa1fba3d2664428c32d15f935c185"),
    "authority/commons-imageinfo-unit-20.json": (14191, "3812f32a5bb823d61f41d6b523fd2e5acfee133cc694ba1eef3c208d1457709b"),
    "authority/assets/Whitney_unbrella.png": (35829, "5a469c4675d326a753dca7801524138e64689e476d38d867070f97983f8b07d2"),
}
PDF_FACTS = {
    "authority/artifacts/lecture-20-official.pdf": (217144, "f9ee520ac2724e041eb8861e4648e59e6357b71d68bf73e7a634a91178d45f9a"),
    "authority/artifacts/worksheet-20-official.pdf": (164793, "d141d76231053dabe89e4af0113e080abd57ee7f7dfc74877bcaa7ad4d48ec9d"),
}
SOLUTION_NUMBERS = [1, 3, 4, 5, 12, 13, 14, 17]
SOLUTION_REVIDS = [612937, 1113196, 1054377, 1090115, 1112402, 1095226, 1096447, 1096446]
CORRECTION_IDS = [f"AGC-CORR-{number:04d}" for number in range(55, 62)]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(path: Path, algorithm: str = "sha256") -> str:
    value = hashlib.new(algorithm)
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def check_fact(relative: str, fact: tuple[int, str]) -> dict[str, Any]:
    path = ROOT / relative
    require(path.is_file() and not path.is_symlink(), f"missing/nonregular file: {relative}")
    actual = (path.stat().st_size, digest(path))
    require(actual == fact, f"identity drift for {relative}: {actual} != {fact}")
    return {"path": relative, "bytes": actual[0], "sha256": actual[1]}


def walk(value: Any) -> Iterable[dict[str, Any]]:
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def pandoc_ast(path: Path) -> dict[str, Any]:
    process = subprocess.run(
        [
            "pandoc",
            "--from=markdown+yaml_metadata_block+tex_math_dollars+fenced_divs+bracketed_spans+raw_attribute",
            "--to=json",
            str(path),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    require(not process.stderr.strip(), f"Pandoc warning for {path.name}: {process.stderr}")
    return json.loads(process.stdout)


def strip_nonprose(raw: str) -> str:
    raw = re.sub(r"\A---\s*\n.*?\n---\s*(?:\n|\Z)", "", raw, flags=re.S)
    raw = re.sub(r"<!--.*?-->", "", raw, flags=re.S)
    raw = re.sub(r"\$\$.*?\$\$", "", raw, flags=re.S)
    raw = re.sub(r"\$[^$\n]*\$", "", raw)
    raw = re.sub(r"```.*?```", "", raw, flags=re.S)
    return raw


def normalized_math(raw: str) -> str:
    return re.sub(r"\s+", "", raw)


def verify_authority() -> dict[str, Any]:
    check_fact("authority/wikiversity/unit-20/UNIT_AUTHORITY_MANIFEST.json", MANIFEST_FACT)
    check_fact("authority/wikiversity/unit-20/ORDERED_EXERCISE_MAP.json", MAP_FACT)
    manifest = json.loads((AUTH / "UNIT_AUTHORITY_MANIFEST.json").read_text(encoding="utf-8"))
    mapping = json.loads((AUTH / "ORDERED_EXERCISE_MAP.json").read_text(encoding="utf-8"))
    require(manifest["schema"] == "brenner-unit-authority-freeze-v2", "authority schema")
    require(manifest["unit_number"] == 20, "authority unit")
    require(manifest["lecture"]["pageid"] == 165909 and manifest["lecture"]["revid"] == 1112311, "lecture identity")
    require(manifest["lecture"]["mediawiki_sha1"] == "74eb303dc659cb8131aaaee6948962210f063f4e", "lecture SHA-1")
    require(manifest["worksheet"]["pageid"] == 165939 and manifest["worksheet"]["revid"] == 1062603, "worksheet identity")
    require(manifest["worksheet"]["mediawiki_sha1"] == "97db112f709b6ab16f89b88f6d4e3da127c7802a", "worksheet SHA-1")
    require(manifest["entry_revision_recheck"]["result"] == "PASS", "entry revision recheck")
    require(manifest["lecture_transclusion_closure"]["captured_page_count"] == 118, "lecture closure count")
    require(manifest["worksheet_transclusion_closure"]["captured_page_count"] == 120, "worksheet closure count")
    require(manifest["lecture_transclusion_closure"]["missing_page_count"] == 0, "lecture missing transclusion")
    require(manifest["worksheet_transclusion_closure"]["missing_page_count"] == 0, "worksheet missing transclusion")
    require(len(manifest["files"]) == 56, "authority file count")
    for row in manifest["files"]:
        path = AUTH / row["file"]
        require(path.is_file() and not path.is_symlink(), f"missing authority file: {row['file']}")
        require(path.stat().st_size == row["bytes"], f"authority bytes: {row['file']}")
        require(digest(path) == row["sha256"], f"authority hash: {row['file']}")
    require(mapping["unit"] == 20 and mapping["exercise_count"] == 23, "exercise map identity/count")
    require(mapping["solution_count"] == 8, "solution count")
    require([row["exercise_number"] for row in mapping["entries"]] == list(range(1, 24)), "exercise order")
    solutions = [row for row in mapping["entries"] if row["has_public_solution"]]
    require([row["exercise_number"] for row in solutions] == SOLUTION_NUMBERS, "solution-number topology")
    require([row["revid"] for row in solutions] == SOLUTION_REVIDS, "solution revision topology")
    for row in solutions:
        for key in ("xml_file", "html_file"):
            path = AUTH / row[key]
            require(path.is_file() and not path.is_symlink(), f"missing solution witness: {row[key]}")
            require(path.stat().st_size == row[key.replace("file", "bytes")], f"solution bytes: {row[key]}")
            require(digest(path) == row[key.replace("file", "sha256")], f"solution hash: {row[key]}")
    dependencies = manifest["solution_transclusion_dependencies"]
    require([row["solution_exercise"] for row in dependencies] == [1, 4], "wrapper dependency exercises")
    require([row["entry"]["revid"] for row in dependencies] == [1108353, 1101325], "wrapper dependency revisions")
    require([row["entry"]["mediawiki_sha1"] for row in dependencies] == ["9f6d9367645cdcd128634774c3252285ddd1601c", "e40f2a19e4dd4db9b1b176d1032a1cb4e6cfbded"], "wrapper dependency SHA-1s")
    for relative, fact in PDF_FACTS.items():
        check_fact(relative, fact)
        require((ROOT / relative).read_bytes().startswith(b"%PDF-"), f"PDF signature: {relative}")
    return {
        "manifest_bytes": MANIFEST_FACT[0],
        "manifest_sha256": MANIFEST_FACT[1],
        "lecture_revid": 1112311,
        "worksheet_revid": 1062603,
        "lecture_transclusions": 118,
        "worksheet_transclusions": 120,
        "exercises": 23,
        "public_solutions": 8,
        "solution_numbers": SOLUTION_NUMBERS,
        "wrapper_dependencies": [1, 4],
        "authority_files_verified": 56,
    }


def verify_media() -> dict[str, Any]:
    facts = [check_fact(relative, fact) for relative, fact in MEDIA_FACTS.items()]
    with (ROOT / "authority" / "RIGHTS-unit-20.csv").open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    require(len(rows) == 1, "Unit 20 rights row count")
    row = rows[0]
    require(row["asset_id"] == "br-ak-u20-media-001", "asset ID")
    require(row["local_path"] == "authority/assets/Whitney_unbrella.png", "asset path")
    require(row["local_bytes"] == "35829" and row["local_sha256"] == MEDIA_FACTS["authority/assets/Whitney_unbrella.png"][1], "asset identity binding")
    require(row["license_short"] == "CC BY 2.5", "asset licence")
    require(row["source_course_inline_license_label"] == "CC-BY-SA-2.5", "source inline rights label")
    require(row["reader_caption_id"] == "Payung Whitney", "reader caption")
    require(row["reader_alt_id"].startswith("Permukaan abu-abu kebiruan"), "reader alt")
    closure = json.loads((ROOT / "authority" / "ASSET_CLOSURE-unit-20.json").read_text(encoding="utf-8"))
    require(closure["unit"] == 20, "media closure unit")
    require(closure["reader_media_positions"] == 1 and closure["unique_local_assets"] == 1, "media topology")
    require(closure["rights_sha256"] == MEDIA_FACTS["authority/RIGHTS-unit-20.csv"][1], "rights binding")
    require(closure["source_inline_license_discrepancy"]["reuse_option_bound"] == "CC BY 2.5", "media licence binding")
    require(len(closure["official_pdf_component_rights"]) == 2, "PDF component-rights closure")
    require([item["license_short"] for item in closure["official_pdf_component_rights"]] == ["CC BY-SA 4.0", "CC BY-SA 4.0"], "official PDF component licences")
    require(closure["assets"][0]["local_sha256"] == MEDIA_FACTS["authority/assets/Whitney_unbrella.png"][1], "closure asset hash")
    require(closure["reader_credits_sha256"] == SOURCE_FACTS["source/id-ID/media-credits-unit-20.md"][1], "media-credit binding")
    return {"media_positions": 1, "binary_surfaces": 1, "rights_rows": 1, "facts": facts}


def verify_translation() -> dict[str, Any]:
    facts = [check_fact(relative, fact) for relative, fact in SOURCE_FACTS.items()]
    facts.extend(check_fact(relative, fact) for relative, fact in CONTROL_FACTS.items())
    lecture = (SOURCE / "lecture-20.md").read_text(encoding="utf-8")
    worksheet = (SOURCE / "worksheet-20.md").read_text(encoding="utf-8")
    solutions = (SOURCE / "worksheet-20-solutions.md").read_text(encoding="utf-8")
    credits = (SOURCE / "media-credits-unit-20.md").read_text(encoding="utf-8")
    all_text = "\n".join((lecture, worksheet, solutions, credits))
    for name, raw in (("lecture", lecture), ("worksheet", worksheet), ("solutions", solutions)):
        require("translation_status: complete" in raw, f"{name} completion flag")
        require("OpenAI Codex\ngpt-5.6-sol, Ultra." in raw, f"{name} exact model provenance")
    require(all(token not in all_text.casefold() for token in ("todo", "fixme", "tbd", "placeholder")), "placeholder residue")
    require(not re.search(r"gh[pousr]_[A-Za-z0-9]{20,}|access[_-]?token|bearer\s+[A-Za-z0-9._-]{20,}", all_text, flags=re.I), "secret-like content")
    require("\u200b" not in all_text and "\ufeff" not in all_text, "invisible Unicode residue")
    prose = strip_nonprose(all_text)
    residue = re.findall(r"\b(?:Es sei|Zeige|Aufgabe|Beweis|Normalisierung|Führungsideal|Ganzheitsgleichung|Kürzungsregel|torsionsfrei|Nenneraufnahme|Quotientenkörper|Untermonoid|Lösung)\b", prose, flags=re.I)
    require(not residue, f"visible German residue: {residue}")
    for rejected in ("lokalisasi", "domain normal", "tanpa torsi", "kerucut poliedral", "setengah-ruang", "ideal penghantar", "monoid rangkap", "grup kelas divisor", "properti lokal", "akar unit"):
        require(not re.search(rf"(?<![A-Za-z]){re.escape(rejected)}(?![A-Za-z])", prose, flags=re.I), f"nonpreferred term: {rejected}")
    for term in ("normalisasi", "domain integral normal", "bebas torsi", "kerucut polihedral", "setengah ruang", "ideal konduktor", "monoid dual", "grup kelas pembagi", "sifat lokal", "akar satuan"):
        require(term in prose, f"required terminology absent: {term}")

    headers = re.findall(r"^### Soal 20\.(\d+)(?:[^\n]*)\{#br-ak-2025-2026-w20-ex-(\d{2})\}$", worksheet, flags=re.M)
    require(headers == [(str(i), f"{i:02d}") for i in range(1, 24)], "exercise headers/IDs")
    starred = [int(value) for value in re.findall(r"^### Soal 20\.(\d+) ★", worksheet, flags=re.M)]
    require(starred == SOLUTION_NUMBERS, "starred solution topology")
    point_rows = re.findall(r"^### Soal 20\.(\d+) \(([^)]*poin[^)]*)\)", worksheet, flags=re.M)
    require(point_rows == [("19", "3 poin"), ("20", "6 poin"), ("21", "5 poin"), ("22", "4 poin"), ("23", "2 poin")], "submitted problem points")
    mapping = json.loads((AUTH / "ORDERED_EXERCISE_MAP.json").read_text(encoding="utf-8"))
    entity_comments = re.findall(r"<!-- upstream_entity: (.*?) -->", worksheet)
    require(entity_comments == [row["exercise_title"] for row in mapping["entries"]], "exercise entity mapping")
    solution_headers = [int(value) for value in re.findall(r"^## Solusi Soal 20\.(\d+) ", solutions, flags=re.M)]
    require(solution_headers == SOLUTION_NUMBERS, "solution headers")
    solution_comments = re.findall(r"<!-- upstream_solution: .*?; pageid=\d+; revid=(\d+) -->", solutions)
    require([int(value) for value in solution_comments] == SOLUTION_REVIDS, "solution comments/revisions")
    proof_comments = [int(value) for value in re.findall(r"<!-- upstream_transcluded_proof: .*?; pageid=\d+; revid=(\d+) -->", solutions)]
    require(proof_comments == [1108353, 1101325], "transcluded proof comments")
    back_links = [int(value) for value in re.findall(r"\[Kembali ke Soal 20\.(\d+)\]\(#br-ak-2025-2026-w20-ex-\d{2}\)", solutions)]
    require(back_links == SOLUTION_NUMBERS, "solution back links")
    stable_ids = re.findall(r"\{#(br-ak-2025-2026-[^}]+)\}", "\n".join((lecture, worksheet, solutions)))
    require(len(stable_ids) == len(set(stable_ids)), "duplicate Unit 20 stable IDs")
    require(len(stable_ids) == 58, f"unexpected stable-ID count: {len(stable_ids)}")
    require(lecture.count("<!-- upstream_entity:") == 13, "lecture semantic entity count")
    require(worksheet.count("<!-- upstream_entity:") == 23, "worksheet semantic entity count")
    require(solutions.count("<!-- upstream_solution:") == 8, "solution provenance count")
    require(lecture.count("![") == 1 and worksheet.count("![") == 0 and solutions.count("![") == 0, "reader image topology")
    require("![Permukaan abu-abu kebiruan berbentuk payung Whitney yang berpotongan sendiri di ruang tiga dimensi](authority/assets/Whitney_unbrella.png)" in lecture, "reader image path/alt")
    require("CC BY 2.5" in lecture and "Claudio Rocchini" in lecture, "reader media attribution")
    require("[Contoh 20.11](#br-ak-2025-2026-l20-exa-03)" in worksheet, "exercise-to-example link")

    normalized = normalized_math("\n".join((lecture, worksheet, solutions)))
    protected = [
        r"M\subseteq\Gamma(M)",
        r"\widetildeM=\{m\in\Gamma(M)\mid\text{terdapat}r\in\mathbbN_+\text{dengan}rm\inM\}",
        r"R[M]\subseteqR[\widetildeM]\subseteqR[\Gamma(M)]\subseteqQ(R)[\Gamma(M)]\subseteqQ(R[M])",
        r"rm=\underbrace{m+\cdots+m}_{r\text{kali}}\inM",
        r"R[\widetildeM]\subseteqR[M]^{\operatorname{norm}}",
        r"M=\langle(1,0),(1,1),(0,2)\rangle\subseteq\mathbbN^2",
        r"2e_1+e_3\longmapsto(2,2)",
        r"2e_2\longmapsto(2,2)",
        r"X^2Z=Y^2",
        r"M=\langle(1,0),(-1,2),(0,1)\rangle\subseteq\mathbbZ^2",
        r"\varphi_1(s,t)=t",
        r"\varphi_2(s,t)=t+2s",
        r"R\cap(f)S=(f)R",
        r"M^*=\left\{\varphi:\Gamma(M)\longrightarrow\mathbbZ\mathrel{\Big|}\varphi(M)\subseteq\mathbbN\right\}",
        r"3^2b^3=a^3",
        r"\prod_{\zeta^n=1}(S-\zeta)",
        r"m\inM_{i+1}\setminusM_i",
        r"T^m\inK[M_{i+1}]\setminusK[M_i]",
        r"X^{e_1}-T^{e_1}=0",
        r"\delta(M)=\dim_K\bigl(R^{\operatorname{norm}}/R\bigr)",
    ]
    missing = [token for token in protected if token not in normalized]
    require(not missing, f"protected mathematics absent: {missing}")
    require("sumber mencetak bahwa kedua unsur itu dipetakan ke" in lecture, "Whitney correction disclosure")
    require("sumber mengganti gelanggang dasar" in lecture and "Sumber juga mencetak $rm=M$" in lecture, "normalization-proof disclosures")
    require("sumber memakai simbol $T$ untuk variabel polinom" in lecture, "integrality-variable disclosure")
    require("sumber memakai indeks dummy" in solutions, "dummy-index disclosure")
    require("sumber menulis\n$T^m\\in M_{i+1}\\setminus M_i$" in solutions, "typed-membership disclosure")
    require("merupakan inferensi\neditorial" in worksheet, "cross-reference inference disclosure")

    ast_receipts: dict[str, Any] = {}
    expected = {
        "lecture-20.md": (23, 1),
        "worksheet-20.md": (26, 0),
        "worksheet-20-solutions.md": (9, 0),
        "media-credits-unit-20.md": (1, 0),
    }
    for name, (header_count, image_count) in expected.items():
        ast = pandoc_ast(SOURCE / name)
        nodes = list(walk(ast.get("blocks", [])))
        headers_ast = [node for node in nodes if node.get("t") == "Header"]
        maths = [node for node in nodes if node.get("t") == "Math"]
        images = [node for node in nodes if node.get("t") == "Image"]
        header_ids = [node["c"][1][0] for node in headers_ast]
        require(all(header_ids), f"header without ID: {name}")
        require(len(header_ids) == len(set(header_ids)), f"duplicate AST header ID: {name}")
        require(len(headers_ast) == header_count, f"AST header count: {name}")
        require(len(images) == image_count, f"AST image count: {name}")
        ast_receipts[name] = {"headers": len(headers_ast), "math_nodes": len(maths), "images": len(images), "stable_header_ids": len(header_ids), "pandoc_warnings": 0}

    with (ROOT / "00_control" / "TERMINOLOGY.csv").open(encoding="utf-8", newline="") as stream:
        terms = {row["source_term"]: row for row in csv.DictReader(stream)}
    expected_terms = {
        "Normalisierung": "normalisasi",
        "normaler Integritätsbereich": "domain integral normal",
        "torsionsfrei": "bebas torsi",
        "polyedrischer Kegel": "kerucut polihedral",
        "Halbraum": "setengah ruang",
        "Führungsideal": "ideal konduktor",
        "duales Monoid": "monoid dual",
        "Divisorenklassengruppe": "grup kelas pembagi",
        "lokale Eigenschaft": "sifat lokal",
        "Einheitswurzel": "akar satuan",
    }
    for source_term, target_term in expected_terms.items():
        require(terms[source_term]["preferred_target"] == target_term, f"terminology target: {source_term}")
        require(terms[source_term]["status"] == "admitted", f"terminology status: {source_term}")
    with (ROOT / "00_control" / "CORRECTIONS.csv").open(encoding="utf-8", newline="") as stream:
        corrections = {row["correction_id"]: row for row in csv.DictReader(stream)}
    for correction_id in CORRECTION_IDS:
        require(correction_id in corrections, f"missing correction binding: {correction_id}")
        require(corrections[correction_id]["status"] == "applied_at_unit_20_translation", f"correction status: {correction_id}")
    require(all(correction_id not in all_text for correction_id in CORRECTION_IDS), "ledger IDs must not replace reader disclosures")
    return {
        "source_and_control_facts": facts,
        "stable_ids": len(stable_ids),
        "exercises": 23,
        "public_solutions": 8,
        "ast": ast_receipts,
        "visible_german_residue": 0,
        "placeholder_count": 0,
        "secret_like_count": 0,
        "protected_math_checks": len(protected),
        "correction_bindings": CORRECTION_IDS,
    }


def main() -> int:
    receipt = {
        "schema": "ag-bridge-unit-translation-qa-v1",
        "status": "PASS",
        "unit": 20,
        "verified_date": "2026-08-25",
        "authority": verify_authority(),
        "media_and_rights": verify_media(),
        "translation": verify_translation(),
        "provenance": "OpenAI Codex gpt-5.6-sol, Ultra.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": "PASS", "unit": 20, "receipt": OUT.relative_to(ROOT).as_posix(), "bytes": OUT.stat().st_size, "sha256": digest(OUT)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
