#!/bin/bash
# MedIntel Android Build Script for Linux/Mac

echo "============================================"
echo "🏥 MedIntel - Android App Builder"
echo "============================================"
echo ""

echo "[1/3] Building web application..."
npm run build
if [ $? -ne 0 ]; then
    echo "❌ Build failed!"
    exit 1
fi
echo "✅ Web build complete"
echo ""

echo "[2/3] Syncing with Android..."
npx cap sync android
if [ $? -ne 0 ]; then
    echo "❌ Sync failed!"
    exit 1
fi
echo "✅ Sync complete"
echo ""

echo "[3/3] Opening Android Studio..."
npx cap open android
echo ""

echo "============================================"
echo "✅ Build process complete!"
echo "============================================"
echo ""
echo "Next steps:"
echo "1. Wait for Gradle sync in Android Studio"
echo "2. Go to: Build > Build Bundle(s) / APK(s) > Build APK(s)"
echo "3. APK will be at: android/app/build/outputs/apk/debug/app-debug.apk"
echo ""
