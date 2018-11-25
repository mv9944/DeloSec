#$UserCredential = Get-Credential eyal@delisos.onmicrosoft.com
#$PWord = ConvertTo-SecureString -String "poolwhite1#" -AsPlainText -Force
#$User = "eyal@delisos.onmicrosoft.com"

$PWord = ConvertTo-SecureString -String $args[1] -AsPlainText -Force
$User = $args[0]
"$($PWord)"
$Credential = New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList $User, $PWord
$Session = New-PSSession -ConfigurationName Microsoft.Exchange -ConnectionUri https://outlook.office365.com/powershell-liveid/ -Credential $Credential -Authentication Basic -AllowRedirection
Import-PSSession $Session -AllowClobber
#################################### Configuration Section ###################################################
$logFile = "C:\Users\nmega\PycharmProjects\untitled\realTimeResults\MyLog.txt"
$outputFile = "C:\Users\nmega\PycharmProjects\untitled\realTimeResults\AuditRecords.csv"
[DateTime]$start = "11/4/18"
[DateTime]$end = "11/7/18"
$resultSize = 5000
$intervalMinutes = 60
#################################### End Configuration Section ###################################################
[DateTime]$currentStart = $start
[DateTime]$currentEnd = $start
$currentTries = 0
 
Function Write-LogFile ([String]$Message)
{
$final = [DateTime]::Now.ToString() + ":" + $Message
$final | Out-File $logFile -Append
}
 
while ($true)
{
$currentEnd = $currentStart.AddMinutes($intervalMinutes)
    if ($currentEnd -gt $end)
    {
    break
    }
$currentCount = 0
$currentTries = 0
#$sessionID = [DateTime]::Now.ToString().Replace('/', '_')
Write-LogFile "INFO: Retrieving audit logs between $($currentStart) and $($currentEnd)"
    while ($true)
        {
        [Array]$results = Search-UnifiedAuditLog -StartDate $currentStart -EndDate $currentEnd  -ResultSize $resultSize
        if ($results -eq $null -or $results.Count -eq 0)
        {
            Write-LogFile "WARNING: Empty data set returned between $($currentStart) and $($currentEnd) .Retry count reached. Moving forward!"
            break
        }

        $currentTotal = $results[0].ResultCount
        if ($currentTotal -gt 5000)
            {
            Write-LogFile "WARNING: $($currentTotal) total records match the search criteria. Some records may get missed. Consider reducing the time interval!"
            }
        $currentCount = $currentCount + $results.Count
        Write-LogFile "INFO: Retrieved $($currentCount) records out of the total $($currentTotal)"
        $results | epcsv $outputFile -NoTypeInformation -Append
       # Write-LogFile " ->>>>>>>>>> Result size:  $($results[$results.Count - 1].ResultIndex) Vs CurrentSize: $($currentTotal) vs results[0].ResultCount:  $($results[0].ResultCount)"
        #if ($currentTotal -eq $results[$results.Count-1].ResultIndex)
            #{
            $message = "INFO: Successfully retrieved $($currentTotal) records for the current time range. Moving on!"
            Write-LogFile $message
            break
            #}
        }
$currentStart = $currentEnd
}
Write-LogFile "Done"
Remove-PSSession $Session