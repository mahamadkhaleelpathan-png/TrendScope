echo "Uploading APK..."
echo "APK path: $APK"
echo "Upload URL: $UPLOAD_URL"

curl -v \
-H "Authorization: token $GITHUB_TOKEN" \
-H "Accept: application/vnd.github+json" \
-H "Content-Type: application/vnd.android.package-archive" \
--data-binary @"$APK" \
"${UPLOAD_URL}?name=TrendScope.apk"
