# Update Download Page with APK Link
# Run this after uploading your APK to Google Drive/GitHub/Dropbox

Write-Host "📥 MedIntel - Update Download Page" -ForegroundColor Cyan
Write-Host "==================================`n" -ForegroundColor Cyan

# Ask for APK link
Write-Host "Where did you upload the APK?" -ForegroundColor Yellow
Write-Host "1. Google Drive" -ForegroundColor White
Write-Host "2. GitHub Releases" -ForegroundColor White
Write-Host "3. Dropbox" -ForegroundColor White
Write-Host "4. Other (Enter custom URL)" -ForegroundColor White

$choice = Read-Host "`nEnter choice (1-4)"

$apkLink = ""

switch ($choice) {
    "1" {
        Write-Host "`n📁 Google Drive Setup:" -ForegroundColor Cyan
        Write-Host "1. Upload app-debug.apk to Google Drive" -ForegroundColor White
        Write-Host "2. Right-click → Share → Anyone with link" -ForegroundColor White
        Write-Host "3. Copy the link" -ForegroundColor White
        $apkLink = Read-Host "`nPaste the Google Drive link"
    }
    "2" {
        Write-Host "`n🐙 GitHub Releases Setup:" -ForegroundColor Cyan
        Write-Host "1. Go to your GitHub repository" -ForegroundColor White
        Write-Host "2. Releases → Create new release" -ForegroundColor White
        Write-Host "3. Upload app-debug.apk" -ForegroundColor White
        Write-Host "4. Publish release" -ForegroundColor White
        Write-Host "5. Copy the APK download link" -ForegroundColor White
        $apkLink = Read-Host "`nPaste the GitHub release link"
    }
    "3" {
        Write-Host "`n📦 Dropbox Setup:" -ForegroundColor Cyan
        Write-Host "1. Upload app-debug.apk to Dropbox" -ForegroundColor White
        Write-Host "2. Right-click → Share" -ForegroundColor White
        Write-Host "3. Copy link and change ?dl=0 to ?dl=1" -ForegroundColor White
        $apkLink = Read-Host "`nPaste the Dropbox link"
    }
    "4" {
        $apkLink = Read-Host "`nEnter the APK download URL"
    }
}

if ($apkLink) {
    # Read the download.html file
    $downloadPage = Get-Content "frontend\public\download.html" -Raw
    
    # Replace the placeholder
    $updatedPage = $downloadPage -replace "const APK_DOWNLOAD_LINK = 'YOUR_APK_LINK_HERE';", "const APK_DOWNLOAD_LINK = '$apkLink';"
    
    # Save the updated file
    Set-Content -Path "frontend\public\download.html" -Value $updatedPage
    
    Write-Host "`n✅ Download page updated successfully!" -ForegroundColor Green
    Write-Host "📍 File: frontend\public\download.html" -ForegroundColor Cyan
    Write-Host "🔗 APK Link: $apkLink`n" -ForegroundColor Cyan
    
    # Commit changes
    $commit = Read-Host "Commit and push changes to GitHub? (y/n)"
    if ($commit -eq "y") {
        git add frontend/public/download.html
        git commit -m "Update download page with APK link"
        git push
        Write-Host "✅ Changes pushed to GitHub`n" -ForegroundColor Green
    }
    
    Write-Host "📱 Share with users:" -ForegroundColor Cyan
    Write-Host "   https://your-site.com/download.html`n" -ForegroundColor White
    
} else {
    Write-Host "`n❌ No link provided. Please run this script again.`n" -ForegroundColor Red
}
