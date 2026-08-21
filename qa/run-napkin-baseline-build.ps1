$ErrorActionPreference = 'Stop'

$sourceRoot = 'C:\Users\Floris\Documents\interlanguage\04_mirrors\id\algebraic-geometry-bridge-id\authority\napkin-e50be9a'
$logPath = 'C:\Users\Floris\Documents\interlanguage\04_mirrors\id\algebraic-geometry-bridge-id\qa\napkin-baseline-build.log'

if (-not (Test-Path -LiteralPath $sourceRoot -PathType Container)) {
    throw "Frozen source root is missing: $sourceRoot"
}
if (Test-Path -LiteralPath $logPath) {
    throw "Refusing to overwrite existing build log: $logPath"
}

Start-Transcript -LiteralPath $logPath -NoClobber | Out-Null
$exitCode = 1
try {
    Write-Output 'Napkin exact-head baseline build'
    Write-Output 'Frozen upstream commit: e50be9a0b2b12d080c273619424d0ee13372cc91'
    Write-Output "Started UTC: $([DateTime]::UtcNow.ToString('o'))"
    Write-Output "Source root: $sourceRoot"

    Set-Location -LiteralPath $sourceRoot

    $nix = Get-Command nix -ErrorAction SilentlyContinue
    if ($null -ne $nix) {
        Write-Output "nix path: $($nix.Source)"
        & $nix.Source --version
        Write-Output 'COMMAND: nix build --no-write-lock-file --print-build-logs .'
        & $nix.Source build --no-write-lock-file --print-build-logs .
        $exitCode = $LASTEXITCODE
    }
    else {
        Write-Output 'nix: unavailable; using the documented latexmk/Asymptote route.'
        $latexmk = Get-Command latexmk -ErrorAction Stop
        $pdflatex = Get-Command pdflatex -ErrorAction Stop
        $asy = Get-Command asy -ErrorAction Stop
        $biber = Get-Command biber -ErrorAction Stop

        Write-Output "latexmk path: $($latexmk.Source)"
        & $latexmk.Source -v
        Write-Output "pdflatex path: $($pdflatex.Source)"
        & $pdflatex.Source --version
        Write-Output "asy path: $($asy.Source)"
        & $asy.Source --version
        Write-Output "biber path: $($biber.Source)"
        & $biber.Source --version

        # The installed TeX implementation is MiKTeX. Disable its package
        # installer so this baseline attempt cannot install missing packages.
        $env:MIKTEX_ENABLE_INSTALLER = '0'
        Write-Output 'MIKTEX_ENABLE_INSTALLER=0'
        Write-Output 'COMMAND: latexmk "-pdflatex=pdflatex --disable-installer %O %S" -interaction=nonstopmode -file-line-error Napkin.tex'
        & $latexmk.Source '-pdflatex=pdflatex --disable-installer %O %S' '-interaction=nonstopmode' '-file-line-error' 'Napkin.tex'
        $exitCode = $LASTEXITCODE
    }

    Write-Output "Build exit code: $exitCode"
    Write-Output "Finished UTC: $([DateTime]::UtcNow.ToString('o'))"
}
finally {
    Stop-Transcript | Out-Null
}

exit $exitCode
