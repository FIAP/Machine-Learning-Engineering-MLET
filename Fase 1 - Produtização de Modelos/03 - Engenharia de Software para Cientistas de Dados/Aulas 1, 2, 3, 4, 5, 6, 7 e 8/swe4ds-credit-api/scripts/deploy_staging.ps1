param(
    [string]$ImageTag = "latest"
)

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Deploying Credit API to Staging" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Image Tag: $ImageTag" -ForegroundColor Yellow
Write-Host ""

# Simulação de deploy
Write-Host "[1/4] Stopping existing containers..." -ForegroundColor Green
Start-Sleep -Seconds 1

Write-Host "[2/4] Pulling new image..." -ForegroundColor Green
Write-Host "      docker pull registry.example.com/credit-api:$ImageTag"
Start-Sleep -Seconds 1

Write-Host "[3/4] Starting new container..." -ForegroundColor Green
Write-Host "      docker run -d -p 8000:8000 credit-api:$ImageTag"
Start-Sleep -Seconds 1

Write-Host "[4/4] Running health check..." -ForegroundColor Green
Write-Host "      curl http://staging.example.com/health"
Start-Sleep -Seconds 1

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Deployment completed successfully!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Staging URL: http://staging.example.com" -ForegroundColor Yellow
Write-Host "Health URL:  http://staging.example.com/health" -ForegroundColor Yellow
Write-Host "Metrics URL: http://staging.example.com/metrics" -ForegroundColor Yellow
