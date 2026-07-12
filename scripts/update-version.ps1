$file = "android/TrendScope/app/build.gradle.kts"

$content = Get-Content $file -Raw

if ($content -match 'versionCode\s*=\s*(\d+)') {
    $versionCode = [int]$matches[1] + 1
    $content = $content -replace 'versionCode\s*=\s*\d+', "versionCode = $versionCode"
}

if ($content -match 'versionName\s*=\s*"(\d+)\.(\d+)\.(\d+)"') {
    $major = [int]$matches[1]
    $minor = [int]$matches[2]
    $patch = [int]$matches[3] + 1

    $newVersion = "$major.$minor.$patch"

    $content = $content -replace 'versionName\s*=\s*".*"', "versionName = `"$newVersion`""
}

Set-Content $file $content

Write-Host "Updated versionCode to $versionCode"
Write-Host "Updated versionName to $newVersion"