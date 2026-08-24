$ErrorActionPreference = 'Stop'

$laneRoot = Split-Path -Parent $PSScriptRoot
$manifestPath = Join-Path $laneRoot 'authority\terminology-id-arxiv\SOURCE_MANIFEST.json'
$receiptPath = Join-Path $laneRoot 'qa\TERMINOLOGY_MIGRATION_UNIT_07.json'
$manifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
$sourceRows = @($manifest.translation_snapshot | Where-Object { $_.path -like 'source/id-ID/*.md' })

if ($sourceRows.Count -ne 21) {
    throw "Expected 21 frozen Unit 1-7 source files, found $($sourceRows.Count)."
}

$utf8NoBom = [System.Text.UTF8Encoding]::new($false)
$before = @()
$fieldCount = 0
$quotientRingCount = 0

foreach ($row in $sourceRows) {
    $relative = [string]$row.path
    $path = Join-Path $laneRoot ($relative -replace '/', '\')
    $hash = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($hash -ne [string]$row.sha256) {
        throw "Frozen snapshot mismatch for ${relative}: expected $($row.sha256), got $hash."
    }
    $text = [IO.File]::ReadAllText($path)
    $fieldCount += [regex]::Matches(
        $text,
        '(?<![\p{L}\p{N}_])medan(?![\p{L}\p{N}_])',
        [Text.RegularExpressions.RegexOptions]::IgnoreCase
    ).Count
    $quotientRingCount += [regex]::Matches(
        $text,
        'gelanggang(?:-gelanggang)?\s+hasil bagi(?:nya)?',
        [Text.RegularExpressions.RegexOptions]::IgnoreCase
    ).Count
    $before += [ordered]@{
        path = $relative
        bytes = (Get-Item -LiteralPath $path).Length
        sha256 = $hash
    }
}

if ($fieldCount -ne 117) {
    throw "Expected 117 field-term occurrences, found $fieldCount."
}
if ($quotientRingCount -ne 22) {
    throw "Expected 22 quotient-ring occurrences, found $quotientRingCount."
}

$changed = @()
foreach ($row in $sourceRows) {
    $relative = [string]$row.path
    $path = Join-Path $laneRoot ($relative -replace '/', '\')
    $text = [IO.File]::ReadAllText($path)
    $updated = [regex]::Replace(
        $text,
        '(?<![\p{L}\p{N}_])medan(?![\p{L}\p{N}_])',
        {
            param($match)
            if ($match.Value[0] -ceq 'M') { 'Lapangan' } else { 'lapangan' }
        },
        [Text.RegularExpressions.RegexOptions]::IgnoreCase
    )
    $updated = [regex]::Replace(
        $updated,
        '(gelanggang(?:-gelanggang)?)(\s+)hasil bagi(nya)?',
        {
            param($match)
            $stem = $match.Groups[1].Value
            if ($stem[0] -ceq 'G') {
                $stem = 'G' + $stem.Substring(1)
            }
            $stem + $match.Groups[2].Value + 'faktor' + $match.Groups[3].Value
        },
        [Text.RegularExpressions.RegexOptions]::IgnoreCase
    )
    if ($updated -cne $text) {
        [IO.File]::WriteAllText($path, $updated, $utf8NoBom)
        $changed += $relative
    }
}

$after = @()
$remainingField = 0
$remainingQuotientRing = 0
$lapanganCount = 0
$gelanggangFaktorCount = 0
foreach ($row in $sourceRows) {
    $relative = [string]$row.path
    $path = Join-Path $laneRoot ($relative -replace '/', '\')
    $text = [IO.File]::ReadAllText($path)
    $remainingField += [regex]::Matches(
        $text,
        '(?<![\p{L}\p{N}_])medan(?![\p{L}\p{N}_])',
        [Text.RegularExpressions.RegexOptions]::IgnoreCase
    ).Count
    $remainingQuotientRing += [regex]::Matches(
        $text,
        'gelanggang(?:-gelanggang)?\s+hasil bagi(?:nya)?',
        [Text.RegularExpressions.RegexOptions]::IgnoreCase
    ).Count
    $lapanganCount += [regex]::Matches(
        $text,
        '(?<![\p{L}\p{N}_])lapangan(?![\p{L}\p{N}_])',
        [Text.RegularExpressions.RegexOptions]::IgnoreCase
    ).Count
    $gelanggangFaktorCount += [regex]::Matches(
        $text,
        'gelanggang(?:-gelanggang)?\s+faktor(?:nya)?',
        [Text.RegularExpressions.RegexOptions]::IgnoreCase
    ).Count
    $after += [ordered]@{
        path = $relative
        bytes = (Get-Item -LiteralPath $path).Length
        sha256 = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
    }
}

if ($remainingField -ne 0 -or $remainingQuotientRing -ne 0) {
    throw "Post-migration residue: medan=$remainingField; quotient-ring phrase=$remainingQuotientRing."
}
if ($lapanganCount -ne 117 -or $gelanggangFaktorCount -ne 22) {
    throw "Post-migration count mismatch: lapangan=$lapanganCount; gelanggang-faktor=$gelanggangFaktorCount."
}

$receipt = [ordered]@{
    schema = 'ag-bridge-terminology-migration-v1'
    applied = '2026-08-22'
    evidence_report = 'authority/terminology-id-arxiv/TERMINOLOGY_QA_REPORT.md'
    evidence_manifest = 'authority/terminology-id-arxiv/SOURCE_MANIFEST.json'
    replacements = @(
        [ordered]@{
            concept = 'field'
            from = 'medan'
            to = 'lapangan'
            occurrences = 117
            basis = 'Both representative Indonesian primary PDFs use lapangan and neither uses medan.'
        },
        [ordered]@{
            concept = 'quotient ring'
            from = 'gelanggang hasil bagi'
            to = 'gelanggang faktor'
            occurrences = 22
            basis = 'The supporting Indonesian commutative-algebra paper explicitly uses gelanggang faktor for quotient rings.'
        }
    )
    files_examined = $sourceRows.Count
    files_changed = $changed.Count
    changed_paths = $changed
    post_counts = [ordered]@{
        medan = $remainingField
        lapangan = $lapanganCount
        quotient_ring_old = $remainingQuotientRing
        gelanggang_faktor = $gelanggangFaktorCount
    }
    before = $before
    after = $after
}

[IO.File]::WriteAllText(
    $receiptPath,
    (($receipt | ConvertTo-Json -Depth 6) + "`n"),
    $utf8NoBom
)

[pscustomobject]@{
    schema = $receipt.schema
    files_examined = $receipt.files_examined
    files_changed = $receipt.files_changed
    post_counts = $receipt.post_counts
} | ConvertTo-Json -Depth 3
