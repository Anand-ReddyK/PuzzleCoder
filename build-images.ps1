# Define Docker image names and corresponding Dockerfiles
$images = @(
    @{ Name = "puzzlecoder-backend"; DockerfilePath = "." },
    @{ Name = "puzzlecoder-worker"; DockerfilePath = ".\worker" },
    @{ Name = "puzzlecoder-scaler"; DockerfilePath = ".\scaler" }
)

# Build the Docker images
foreach ($image in $images) {
    Write-Host "Building Docker image: $($image.Name)"
    docker build $image.DockerfilePath -t $image.Name
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to build $($image.Name)" -ForegroundColor Red
        exit $LASTEXITCODE
    }
}

Write-Host "All Docker images have been built successfully!" -ForegroundColor Green
