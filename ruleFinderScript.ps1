#$UserCredential = Get-Credential eyal@delisos.onmicrosoft.com 
#$PWord = ConvertTo-SecureString -String "poolwhite1#" -AsPlainText -Force
#$User = "eyal@delisos.onmicrosoft.com"

$PWord = ConvertTo-SecureString -String $args[1] -AsPlainText -Force
$User = $args[0]
$Credential = New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList $User, $PWord
$Session = New-PSSession -ConfigurationName Microsoft.Exchange -ConnectionUri https://outlook.office365.com/powershell-liveid/ -Credential $Credential -Authentication Basic -AllowRedirection
Import-PSSession $Session -DisableNameChecking -AllowClobber
  
#################################### Configuration Section ###################################################
$logFile = "C:\Users\nmega\PycharmProjects\untitled\realTimeResults\MyRuleLog.txt"
$outputFile = "C:\Users\nmega\PycharmProjects\untitled\realTimeResults\AllRulesResults.csv"
#################################### End Configuration Section ###############################################
Function Write-LogFile ([String]$Message)
{
$final = [DateTime]::Now.ToString() + ":" + $Message
$final | Out-File $logFile -Append
}
[Array]$results = Get-Mailbox| Select PrimarySmtpAddress 
[int] $iterator = 1


    while ($iterator -lt $results.Length)

    {
        [string] $correntInboxMail = ($results[$iterator])
        [string] $correntInboxMailv1 =  ($correntInboxMail.Remove(0,21))
        [string] $correntInboxMailv2 =  ($correntInboxMailv1.Remove($correntInboxMailv1.Length-1,1))
        Write-LogFile "Try to gother information rules from  $($correntInboxMailv2) mail box"
        $iterator += 1
        [string]$res = Get-InboxRule -Mailbox $($correntInboxMailv2) | Select * 
       # $($res)
        if ($res.length -eq  0) 
        {
            Write-LogFile "No rule information from $($correntInboxMailv2) mail box"
        }
        else
        {
        Get-InboxRule -Mailbox $($correntInboxMailv2) | Select * | export-csv $outputFile -Append
        Write-LogFile "Successfully retrieve information from $($correntInboxMailv2) mail box"
        }

    }




Remove-PSSession $Session