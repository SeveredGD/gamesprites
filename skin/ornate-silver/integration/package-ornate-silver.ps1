param(
  [string]$LayoutRoot = 'C:\Users\garre\Downloads\Everdeep_Floating_Layout_v4'
)

$ErrorActionPreference = 'Stop'
$utf8NoBom = [System.Text.UTF8Encoding]::new($false)
$root = [IO.Path]::GetFullPath($LayoutRoot).TrimEnd('\')
$skinRoot = [IO.Path]::GetFullPath((Join-Path $root 'skins\ornate-silver'))
$integration = [IO.Path]::GetFullPath((Join-Path $skinRoot 'integration'))
$sourceAssets = [IO.Path]::GetFullPath((Join-Path $root 'assets'))
$targetAssets = [IO.Path]::GetFullPath((Join-Path $skinRoot 'assets'))

function Assert-InRoot([string]$Path) {
  $full = [IO.Path]::GetFullPath($Path)
  if (-not $full.StartsWith($root + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) {
    throw "Path escaped layout root: $full"
  }
}

Assert-InRoot $skinRoot
Assert-InRoot $integration
Assert-InRoot $sourceAssets
Assert-InRoot $targetAssets

if (-not (Test-Path -LiteralPath $sourceAssets -PathType Container)) {
  throw "Source asset tree not found: $sourceAssets"
}
if (Test-Path -LiteralPath $targetAssets) {
  throw "Target asset tree already exists: $targetAssets"
}

New-Item -ItemType Directory -Force -Path $integration | Out-Null
Move-Item -LiteralPath $sourceAssets -Destination $targetAssets

$exports = @(
  'everdeep-v4-skin-config.json',
  'everdeep-reskin-map-v4-baseline.json'
)
foreach ($name in $exports) {
  $source = Join-Path $root $name
  $destination = Join-Path $integration $name
  Assert-InRoot $source
  Assert-InRoot $destination
  if (-not (Test-Path -LiteralPath $source -PathType Leaf)) {
    throw "Required skin export not found: $source"
  }
  Move-Item -LiteralPath $source -Destination $destination
}

$htmlPath = Join-Path $root 'Everdeep_Floating_Layout_v4.html'
$rewriteTargets = @(
  $htmlPath,
  (Join-Path $integration 'everdeep-v4-skin-config.json'),
  (Join-Path $integration 'everdeep-reskin-map-v4-baseline.json')
)
foreach ($path in $rewriteTargets) {
  $sourceText = [IO.File]::ReadAllText($path)
  $updatedText = $sourceText.Replace('assets/', 'skins/ornate-silver/assets/')
  [IO.File]::WriteAllText($path, $updatedText, $utf8NoBom)
}

$html = [IO.File]::ReadAllText($htmlPath)
$cssMatch = [regex]::Match(
  $html,
  '<style id="everdeep-v4-button-system-css">\s*(?<body>[\s\S]*?)\s*</style>',
  [Text.RegularExpressions.RegexOptions]::CultureInvariant
)
$jsMatch = [regex]::Match(
  $html,
  '<script id="everdeep-v4-button-system-js">\s*(?<body>[\s\S]*?)\s*</script>',
  [Text.RegularExpressions.RegexOptions]::CultureInvariant
)
if (-not $cssMatch.Success -or -not $jsMatch.Success) {
  throw 'Could not locate the authoritative v4 CSS/JavaScript blocks.'
}

[IO.File]::WriteAllText(
  (Join-Path $integration 'ornate-silver-v4.css'),
  $cssMatch.Groups['body'].Value + [Environment]::NewLine,
  $utf8NoBom
)
[IO.File]::WriteAllText(
  (Join-Path $integration 'ornate-silver-v4.js'),
  $jsMatch.Groups['body'].Value + [Environment]::NewLine,
  $utf8NoBom
)

$manifestPath = Join-Path $integration 'asset-manifest.json'
$manifestFiles = Get-ChildItem -LiteralPath $skinRoot -File -Recurse |
  Where-Object { $_.FullName -ne $manifestPath } |
  Sort-Object FullName |
  ForEach-Object {
    [ordered]@{
      path = $_.FullName.Substring($skinRoot.Length + 1).Replace('\', '/')
      bytes = $_.Length
      sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $_.FullName).Hash.ToLowerInvariant()
    }
  }
$manifest = [ordered]@{
  format = 'everdeep-ornate-silver-skin-bundle'
  version = 4
  sourceLayout = 'Everdeep_Floating_Layout_v4.html'
  assetRoot = 'skins/ornate-silver/assets/'
  files = @($manifestFiles)
}
[IO.File]::WriteAllText(
  $manifestPath,
  ($manifest | ConvertTo-Json -Depth 6) + [Environment]::NewLine,
  $utf8NoBom
)

Write-Output "Packaged Ornate Silver skin at $skinRoot"
Write-Output "Moved assets: $targetAssets"
Write-Output "Manifest: $manifestPath"
