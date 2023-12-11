py ./app.py
$url = "https://localhost"
# Use JavaScript to open the URL in the active browser tab
$javascript = "window.location.href = '$url';"
Invoke-Expression $javascript
