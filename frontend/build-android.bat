@echo off
REM MedIntel Android Build Script
echo ============================================
echo 🏥 MedIntel - Android App Builder
echo ============================================
echo.

echo [1/3] Building web application...
call npm run build
if errorlevel 1 (
    echo ❌ Build failed!
    pause
    exit /b 1
)
echo ✅ Web build complete
echo.

echo [2/3] Syncing with Android...
call npx cap sync android
if errorlevel 1 (
    echo ❌ Sync failed!
    pause
    exit /b 1
)
echo ✅ Sync complete
echo.

echo [3/3] Opening Android Studio...
call npx cap open android
echo.

echo ============================================
echo ✅ Build process complete!
echo ============================================
echo.
echo Next steps:
echo 1. Wait for Gradle sync in Android Studio
echo 2. Go to: Build ^> Build Bundle(s) / APK(s) ^> Build APK(s)
echo 3. APK will be at: android\app\build\outputs\apk\debug\app-debug.apk
echo.
pause
