# Benchmark day08/day08.py 10 runs and print minimum time

Param(
    [Parameter(Position = 0, HelpMessage = "Executable and arguments to run. E.g. 'python day08\\day08.py'")]
    [string]$executable_with_arguments = "",
    [Parameter(Position = 1, HelpMessage = "Number of iterations to run (default 10)")]
    [int]$iterations = 10
)

$resultsMs = @()

for ($i = 1; $i -le $iterations; $i++) {
    $ts = Measure-Command { Invoke-Expression $executable_with_arguments }
    $resultsMs += $ts.TotalMilliseconds
}

$minMs = ($resultsMs | Measure-Object -Minimum).Minimum
Write-Host ("{0}: Min time over {1} runs: {2:N2} ms" -f $executable_with_arguments, $iterations, $minMs)
