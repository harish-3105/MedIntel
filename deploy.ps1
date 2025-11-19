# Quick Deploy Script for Railway/Render
# Run this after setting up Railway or Render projects

Write-Host "MedIntel Deployment Helper" -ForegroundColor Cyan
Write-Host "================================`n" -ForegroundColor Cyan

# Check if git is initialized
if (-not (Test-Path ".git")) {
    Write-Host "Git not initialized. Initializing..." -ForegroundColor Yellow
    git init
    git add .
    git commit -m "Initial commit - MedIntel v1.0.0"
}

Write-Host "Git repository ready`n" -ForegroundColor Green

# Ask for deployment platform
Write-Host "Select deployment platform:" -ForegroundColor Yellow
Write-Host "1. Railway (Recommended)" -ForegroundColor White
Write-Host "2. Render" -ForegroundColor White
Write-Host "3. Both" -ForegroundColor White
$choice = Read-Host "Enter choice (1-3)"

# Ask for backend URL
Write-Host "`nBackend Configuration" -ForegroundColor Cyan
$backendUrl = Read-Host "Enter your deployed backend URL (e.g., https://medintel-backend.railway.app)"

if ($backendUrl) {
    # Update frontend .env
    Write-Host "Updating frontend environment variables..." -ForegroundColor Yellow
    
    $envContent = @"
VITE_API_URL=$backendUrl
"@
    
    Set-Content -Path "frontend\.env" -Value $envContent
    Write-Host "Frontend .env updated with backend URL`n" -ForegroundColor Green
}

# GitHub setup
Write-Host "GitHub Setup" -ForegroundColor Cyan
$hasGitHub = Read-Host "Do you have a GitHub repository? (y/n)"

if ($hasGitHub -eq "y") {
    $githubUrl = Read-Host "Enter GitHub repository URL (e.g., https://github.com/username/medintel)"
    
    # Add remote if not exists
    $remotes = git remote
    if ($remotes -notcontains "origin") {
        git remote add origin $githubUrl
        Write-Host "GitHub remote added" -ForegroundColor Green
    }
    
    # Commit and push
    Write-Host "`nPushing to GitHub..." -ForegroundColor Yellow
    git add .
    git commit -m "Configure deployment for Railway/Render"
    git push -u origin main
    
    Write-Host "Code pushed to GitHub`n" -ForegroundColor Green
    
} else {
    Write-Host "`nTo deploy, you need to:" -ForegroundColor Yellow
    Write-Host "1. Create a GitHub repository" -ForegroundColor White
    Write-Host "2. Push your code: git remote add origin <your-repo-url>" -ForegroundColor White
    Write-Host "3. Then: git push -u origin main`n" -ForegroundColor White
}

# Deployment instructions
Write-Host "Next Steps:" -ForegroundColor Cyan

if ($choice -eq "1" -or $choice -eq "3") {
    Write-Host "`nRailway Deployment:" -ForegroundColor Yellow
    Write-Host "1. Go to https://railway.app/new" -ForegroundColor White
    Write-Host "2. Click 'Deploy from GitHub repo'" -ForegroundColor White
    Write-Host "3. Select your MedIntel repository" -ForegroundColor White
    Write-Host "4. Add TWO services:" -ForegroundColor White
    Write-Host "   - Backend: Root directory = 'backend'" -ForegroundColor White
    Write-Host "   - Frontend: Root directory = 'frontend'" -ForegroundColor White
    Write-Host "5. Set environment variables for frontend:" -ForegroundColor White
    Write-Host "   VITE_API_URL = <your-backend-url>" -ForegroundColor White
}

if ($choice -eq "2" -or $choice -eq "3") {
    Write-Host "`nRender Deployment:" -ForegroundColor Yellow
    Write-Host "1. Go to https://render.com/dashboard" -ForegroundColor White
    Write-Host "2. New → Web Service (for backend)" -ForegroundColor White
    Write-Host "   - Root Directory: backend" -ForegroundColor White
    Write-Host "   - Build: pip install -r requirements.txt" -ForegroundColor White
    Write-Host "   - Start: python main.py" -ForegroundColor White
    Write-Host "3. New → Static Site (for frontend)" -ForegroundColor White
    Write-Host "   - Root Directory: frontend" -ForegroundColor White
    Write-Host "   - Build: npm install && npm run build" -ForegroundColor White
    Write-Host "   - Publish: dist" -ForegroundColor White
    Write-Host "4. Add environment variable:" -ForegroundColor White
    Write-Host "   VITE_API_URL = <your-backend-url>" -ForegroundColor White
}

Write-Host "`nAfter Deployment:" -ForegroundColor Cyan
Write-Host "1. Visit your live site" -ForegroundColor White
Write-Host "2. Try Add to Home Screen to install PWA" -ForegroundColor White
Write-Host "3. Share the URL with users!" -ForegroundColor White
Write-Host "4. Download page: https://your-site.com/download.html`n" -ForegroundColor White

Write-Host "Deployment preparation complete!" -ForegroundColor Green
Write-Host "For detailed instructions, see DEPLOYMENT_GUIDE.md`n" -ForegroundColor Cyan
