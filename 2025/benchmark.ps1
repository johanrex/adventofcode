# Benchmark day08/day08.py 10 runs and print minimum time

$script = "day08\day08.py"

$resultsMs = @()
$iterations = 10

for ($i = 1; $i -le $iterations; $i++) {
    $ts = Measure-Command { python $script }
        $resultsMs += $ts.TotalMilliseconds
}

$minMs = ($resultsMs | Measure-Object -Minimum).Minimum
Write-Host ("${script}: Min time over $iterations runs: {0:N2} ms" -f $minMs)

