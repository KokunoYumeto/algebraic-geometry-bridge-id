$ErrorActionPreference = 'Stop'

$sourceRoot = 'C:\Users\Floris\Documents\interlanguage\04_mirrors\id\algebraic-geometry-bridge-id\authority\napkin-e50be9a'
$stdoutPath = 'C:\Users\Floris\Documents\interlanguage\04_mirrors\id\algebraic-geometry-bridge-id\qa\napkin-baseline-replay-v2.stdout.log'
$stderrPath = 'C:\Users\Floris\Documents\interlanguage\04_mirrors\id\algebraic-geometry-bridge-id\qa\napkin-baseline-replay-v2.stderr.log'

foreach ($path in @($stdoutPath, $stderrPath)) {
    if (Test-Path -LiteralPath $path) {
        throw "Refusing to overwrite existing replay log: $path"
    }
}

$latexmk = (Get-Command latexmk -ErrorAction Stop).Source
$env:MIKTEX_ENABLE_INSTALLER = '0'
$argumentLine = '"-pdflatex=pdflatex --disable-installer %O %S" -interaction=nonstopmode -file-line-error Napkin.tex'

$process = Start-Process -FilePath $latexmk `
    -ArgumentList $argumentLine `
    -WorkingDirectory $sourceRoot `
    -NoNewWindow `
    -Wait `
    -PassThru `
    -RedirectStandardOutput $stdoutPath `
    -RedirectStandardError $stderrPath

Write-Output "Replay exit code: $($process.ExitCode)"
exit $process.ExitCode
