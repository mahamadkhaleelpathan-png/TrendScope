$buildFile = "android/TrendScope/app/build.gradle.kts"

$content = Get-Content $buildFile -Raw

# Read current versionCode
$versionCodeMatch = [regex]::Match($content, 'versionCode\s*=\s*(\d+)')
$versionCode = [int]$versionCodeMatch.Groups[1].Value

# Read current versionName
$versionNameMatch = [regex]::Match($content, 'versionName\s*=\s*"(\d+)\.(\d+)\.(\d+)"')

$major = [int]$versionNameMatch.Groups[1].Value
$minor = [int]$versionNameMatch.Groups[2].Value
$patch = [int]$versionNameMatch.Groups[3].Value

# Increment versions
$versionCode++
$patch++

$newVersionName = "$major.$minor.$patch"

$content = [regex]::Replace(
    $content,
    'versionCode\s*=\s*\d+',
    "versionCode = $versionCode"
)

$content = [regex]::Replace(
    $content,
    'versionName\s*=\s*"\d+\.\d+\.\d+"',
    "versionName = `"$newVersionName`""
)

Set-Content $buildFile $content

Write-Host "Updated versionName to $newVersionName"
Write-Host "Updated versionCode to $versionCode"