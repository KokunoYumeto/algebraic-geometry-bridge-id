#!/usr/bin/env python3
"""Verify protected mathematical surfaces for cumulative Units 19--21."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from bs4 import BeautifulSoup
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source" / "id-ID"
HTML = ROOT / "build" / "reader-id" / "index.html"
PDF = ROOT / "build" / "reader-id" / "algebraic-geometry-bridge-id-units-01-21.pdf"
OUT = ROOT / "qa" / "UNIT_21_PROTECTED_SURFACES.json"
BASELINE = ROOT / "qa" / "UNIT_18_PROTECTED_SURFACES.json"
MACHINE = ROOT / "qa" / "UNITS_01_21_MACHINE_QA.json"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra."

BASELINE_FACT = (1566, "29a6a329361515dadc7c6399538a010a3717c43e38fb9564ac681b8670786bc9")
MACHINE_FACT = (7308, "adace78a568ecb84c97077965d82a4ca13a849b7455db0b8872546486dcabdd0")
UNIT_QA_FACTS = {
    19: ("qa/UNIT_19_INTEGRATION_QA.json", 5865, "fe546d8499bc63dedb08c3548eb42322924338ea5e183af7ff9fc66f48a6601a"),
    20: ("qa/UNIT_20_TRANSLATION_QA.json", 3748, "6c4bc4eb66feccf91d0d53f81c08726857a6edb3dbee93b66b0487b83a4b2725"),
    21: ("qa/UNIT_21_TRANSLATION_QA.json", 5436, "a999af2ab40124cbe8bb593239ce17b9e99515d70253ac1869f2934426a7ff75"),
}
PROTECTED = {
    19: [
        r"X_i&\longmapstoT^{e_i}",
        r"\sum_{k\geq0}",
        r"X^3=T^9=YZ",
        r"C=V(Y^3-X^4,\Z^3-X^5,\Z^4-Y^5,\X^3-YZ,\Y^2-XZ,\Z^2-X^2Y,\Z^3-XY^3)",
        r"A^{\operatorname{adj}}A=(\detA)I_n",
        r"R[x]=R+Rx+Rx^2+\cdots+Rx^{n-2}+Rx^{n-1}",
        r"K[X,Y]/(X^2+Y^2-1)&\longrightarrowK[U,V]/(U^2+V^2-1)",
        r"K[X^{-1},YX^{-k}]",
        r"P_iY^iX^{-kn}&=P_iY^iX^{-ki}X^{-k(n-i)}\\&=(YX^{-k})^iP_iX^{-k(n-i)}",
        r"K[X^{-1}][Z]",
    ],
    20: [
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
    ],
    21: [
        r"K[X,Y]_{(X-a,Y-b)}/(F)\cong(K[X,Y]/(F))_{\mathfrakm}",
        r"R\setminus\{0\}\longrightarrow\mathbbN",
        r"\operatorname{ord}(f+g)\geq\min\{\operatorname{ord}(f),\operatorname{ord}(g)\}",
        r"\mathfrakm^n=0",
        r"T=\{1,f,f^2,\ldots\}",
        r"S=R/(f)",
        r"\widetilde{\mathfrakm}=\mathfrakm/(f)",
        r"\mathfrakm^n\subseteq(f)",
        r"h:=\fracfg",
        r"h^{-1}=\fracgf",
        r"h^{-1}\mathfrakm=\fracgf\mathfrakm\subseteq\frac{\mathfrakm^n}{f}\subseteqR",
        r"1=ab\pi",
        r"V/N=\mathfrakm(V/N)",
        r"\mu_R(\mathfrakm)=\dim_k(\mathfrakm/\mathfrakm^2)",
        r"M_+=M\setminus\{0\}",
        r"\mathfrakm=K[M_+]=\left\langleT^m\mathrel{\Big|}m\inM_+\right\rangle",
        r"K[X,Y]/(X^2+Y^2-1)",
        r"\nu:(K^\times,\cdot,1)\longrightarrow(\mathbbZ,+,0)",
        r"R=\{f\inK^\times\mid\nu(f)\geq0\}\cup\{0\}",
        r"F'=na_nX^{n-1}+(n-1)a_{n-1}X^{n-2}+\cdots+3a_3X^2+2a_2X+a_1",
        r"\frac{1}{i!}\left(X^n\right)^{(i)}=\binomniX^{n-i}",
        r"\mathfrakm^{n+1}=\mathfrakm^n",
        r"R\capK[T]=K",
        r"K[X,Y]_{(X,Y)}/(X^2-Y^3)",
        r"Q(R)=R_\pi",
        r"\pi^{-1}=\pi^{-n-1}\pi^n\inT",
        r"\mathfrakm:=\{f\inK^\times\mid\nu(f)\geq1\}\cup\{0\}",
        r"\nu(x/p^n)=0",
    ],
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def normalize(value: str) -> str:
    return re.sub(r"\s+", "", value)


def check_fact(path: Path, fact: tuple[int, str], label: str) -> None:
    require(path.is_file() and not path.is_symlink(), f"missing/nonregular {label}")
    actual = (path.stat().st_size, digest(path))
    require(actual == fact, f"{label} drift: {actual} != {fact}")


def main() -> int:
    check_fact(BASELINE, BASELINE_FACT, "Unit 18 protected baseline")
    baseline_payload = json.loads(BASELINE.read_text(encoding="utf-8"))
    require(baseline_payload["status"] == "PASS" and baseline_payload["through_unit"] == 18, "Unit 18 protected baseline status/scope")
    check_fact(MACHINE, MACHINE_FACT, "cumulative Unit 21 machine QA")
    machine = json.loads(MACHINE.read_text(encoding="utf-8"))
    require(machine["status"] == "PASS" and machine["through_unit"] == 21, "cumulative machine QA status/scope")

    unit_qas: dict[int, dict[str, object]] = {}
    correction_bindings: list[str] = []
    for unit, (relative, byte_count, sha256) in UNIT_QA_FACTS.items():
        path = ROOT / relative
        check_fact(path, (byte_count, sha256), f"Unit {unit} translation QA")
        payload = json.loads(path.read_text(encoding="utf-8"))
        require(payload["status"] == "PASS" and payload["unit"] == unit, f"Unit {unit} translation QA status/scope")
        require(payload["provenance"] == MODEL, f"Unit {unit} translation QA provenance")
        unit_qas[unit] = payload
        if unit == 21:
            correction_bindings.extend(payload["translation"]["source_correction_bindings"])
            correction_bindings.extend(payload["translation"]["editorial_bridge_bindings"])
        else:
            correction_bindings.extend(payload["translation"]["correction_bindings"])
    require(correction_bindings == [f"AGC-CORR-{number:04d}" for number in range(51, 71)], "Units 19-21 correction/bridge binding interval")

    source_checks: dict[str, dict[str, object]] = {}
    all_tokens: list[str] = []
    for unit, tokens in PROTECTED.items():
        names = (f"lecture-{unit:02d}.md", f"worksheet-{unit:02d}.md", f"worksheet-{unit:02d}-solutions.md")
        raw = "\n".join((SOURCE / name).read_text(encoding="utf-8") for name in names)
        normalized = normalize(raw)
        missing = [token for token in tokens if token not in normalized]
        require(not missing, f"protected source math absent in Unit {unit}: {missing}")
        require(unit_qas[unit]["translation"]["protected_math_checks"] == len(tokens), f"Unit {unit} per-unit protected-token binding")
        source_checks[str(unit)] = {"tokens": len(tokens), "source_files": 3, "missing": 0}
        all_tokens.extend(tokens)

    soup = BeautifulSoup(HTML.read_text(encoding="utf-8"), "html.parser")
    annotations = [tag.get_text() for tag in soup.find_all("annotation") if tag.get("encoding") == "application/x-tex"]
    annotation_blob = normalize("\n".join(annotations))
    missing_html = [token for token in all_tokens if token not in annotation_blob]
    require(not missing_html, f"protected TeX annotations absent from HTML: {missing_html}")
    require(len(annotations) == machine["coverage"]["mathml_nodes"], "HTML TeX annotations/machine MathML binding")
    require((HTML.stat().st_size, digest(HTML)) == (machine["html"]["bytes"], machine["html"]["sha256"]), "HTML/machine identity binding")

    reader = PdfReader(PDF, strict=True)
    require(not reader.is_encrypted, "PDF encrypted")
    require((PDF.stat().st_size, digest(PDF)) == (machine["pdf"]["bytes"], machine["pdf"]["sha256"]), "PDF/machine identity binding")
    require(len(reader.pages) == machine["pdf"]["pages"], "PDF/machine page binding")
    terminal_start = machine["pdf"]["terminal_start_page"]
    require(isinstance(terminal_start, int) and 1 <= terminal_start <= len(reader.pages), "terminal start page")
    terminal_parts = [(reader.pages[index].extract_text() or "") for index in range(terminal_start - 1, len(reader.pages))]
    terminal_text = "\n".join(terminal_parts)
    pdf_markers = (
        "Kuliah 19",
        "Soal 19.15",
        "Solusi Soal 19.12",
        "Kuliah 20",
        "Soal 20.23",
        "Solusi Soal 20.17",
        "Kuliah 21",
        "Soal 21.26",
        "Solusi Soal 21.8",
    )
    for marker in pdf_markers:
        require(marker in terminal_text, f"protected terminal PDF marker absent: {marker}")

    receipt = {
        "schema": "ag-bridge-protected-surfaces-v3",
        "status": "PASS",
        "verified_date": "2026-08-25",
        "through_unit": 21,
        "unit_18_baseline": {
            "path": "qa/UNIT_18_PROTECTED_SURFACES.json",
            "bytes": BASELINE_FACT[0],
            "sha256": BASELINE_FACT[1],
            "status": "PASS",
        },
        "machine_qa": {
            "path": "qa/UNITS_01_21_MACHINE_QA.json",
            "bytes": MACHINE_FACT[0],
            "sha256": MACHINE_FACT[1],
            "status": "PASS",
        },
        "units_19_21": source_checks,
        "protected_token_count": len(all_tokens),
        "source_missing": 0,
        "html_mathml_annotations": len(annotations),
        "html_missing": 0,
        "pdf_terminal_start_page": terminal_start,
        "pdf_terminal_pages_checked": len(terminal_parts),
        "pdf_terminal_markers_checked": len(pdf_markers),
        "correction_and_bridge_disclosures": correction_bindings,
        "checks": [
            "exact Unit 18 protected-surface baseline is PASS",
            "exact cumulative Unit 21 machine QA is PASS",
            "exact Units 19-21 translation/integration math gates are PASS",
            "all protected source formulas survive as HTML TeX annotations",
            "measured terminal PDF range contains every Unit 19-21 lecture, worksheet, and public-solution boundary",
            "all Unit 19-21 source corrections and edition bridges remain ledger-bound",
        ],
        "provenance": MODEL,
    }
    OUT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(
        json.dumps(
            {
                "status": "PASS",
                "receipt": OUT.relative_to(ROOT).as_posix(),
                "bytes": OUT.stat().st_size,
                "sha256": digest(OUT),
                "protected_tokens": len(all_tokens),
                "mathml_annotations": len(annotations),
                "pdf_terminal_pages": len(terminal_parts),
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
