
$day = (Get-Date).Day
$folder = "day$day"

if (-not (Test-Path $folder)) {
    mkdir $day
    New-Item -Path ".\$folder\$day.py" -ItemType File # create the py file
    New-Item -Path ".\$folder\example" -ItemType File # create the example file

    Write-Host "Created files for day $day"
}
else {
    Write-Host "Files for day $day already exist"
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

    $url = "https://adventofcode.com/2023/day/$day/input"
    curl --cookie "session=$session_cookie" $url > $input_file

    Write-Host "Downloaded input for day $day"
}
else {
    Write-Host "Input for day $day already exists"
}

#TODO template file with import, parser, timer, part1, part 2
