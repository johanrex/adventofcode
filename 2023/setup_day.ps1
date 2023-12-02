
$day = (Get-Date).Day

if (-not (Test-Path $day)) {
    mkdir $day
    New-Item -Path ".\$day\$day.py" -ItemType File # create the py file
    New-Item -Path ".\$day\example" -ItemType File # create the example file

    # sleep until 6am to download the input
    while ((Get-Date).Hour -lt 6) {
        Start-Sleep -Seconds 1
    }

    # read the cookie file
    $json = Get-Content -Path "cookie.json" -Raw | ConvertFrom-Json
    $session_cookie = $json."Content raw"

    $url = "https://adventofcode.com/2023/day/$day/input"
    curl --cookie "session=$session_cookie" $url > $day/input

    Write-Host "Created files for day $day"
}
else {
    Write-Host "Files for day $day already exist"
}
