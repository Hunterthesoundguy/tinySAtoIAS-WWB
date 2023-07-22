<#load input file#>
$csv = Import-Csv -path "input.csv" -Delimiter ";" -header freq, level 

<#modify data#>
foreach ($Item in $csv)
{
$Item.freq = [math]::Round($Item.freq/1000000,3) 
$Item.level = [math]::Round($Item.level,0)
}

<#export file#>
$Csv | Export-Csv -Path "output/output.csv" -Delimiter ',' -NoType 
<#remove quotation marks#>
(Get-Content "output/output.csv") -replace '"' | select -Skip 1 | Set-Content "output/output.csv"
Get-ChildItem "output/output.csv" | ForEach-Object {          
Rename-Item $_.FullName "$BackupFolder$($_.BaseName -replace " ", "_" -replace '\..*?$')-$(Get-Date -Format "HHmmMMddyyyy").csv"}
