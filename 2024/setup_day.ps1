$today = Get-Date
$day = $today.Day
$year = $today.Year
$folder = "day$day"

if (-not (Test-Path $folder)) {
    mkdir $folder
}

$pythonFile = "$folder\day$day.py"
if (-not (Test-Path $pythonFile)) {
    copy-item .\template.py $pythonFile # copy the template file
    (Get-Content $pythonFile) -replace 'dayX', "day$day" | Set-Content $pythonFile
    Write-Host "Created files for day $day"
}

$exampleFile = "$folder\example"
if (-not (Test-Path $exampleFile)) {
    New-Item -Path ".\$folder\example" -ItemType File
}

$input_file = "$folder/input"

# sleep until 2 seconds past 6am to download the input. Have gotten error message when trying to download at exactly 6am.
$target = [DateTime]::new($today.Year, $today.Month, $today.Day, 6, 0, 2)
$timeToWait = $target - (Get-Date)
if ($timeToWait.TotalSeconds -gt 0) {
    $sleepSeconds = [math]::Ceiling($timeToWait.TotalSeconds)
    write-host "Sleeping for $sleepSeconds seconds"
    Start-Sleep -Seconds $sleepSeconds
}

# read the cookie file
$json = Get-Content -Path "cookie.json" -Raw | ConvertFrom-Json
$session_cookie = $json."Content raw"

$url = "https://adventofcode.com/$year/day/$day/input"
curl --cookie "session=$session_cookie" $url > $input_file

Write-Host "Downloaded input file for day $day"
