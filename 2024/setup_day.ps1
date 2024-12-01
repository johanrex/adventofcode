
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
# should we download the input?
if (-not (Test-Path $input_file)) {

    # sleep until 6am to download the input
    while ((Get-Date).Hour -lt 6) {
        Start-Sleep -Seconds 1
    }    

    # read the cookie file
    $json = Get-Content -Path "cookie.json" -Raw | ConvertFrom-Json
    $session_cookie = $json."Content raw"

    $url = "https://adventofcode.com/$year/day/$day/input"
    curl --cookie "session=$session_cookie" $url > $input_file

    Write-Host "Downloaded input for day $day"
}
else {
    Write-Host "Input for day $day already exists"
}
