# 📱 MedIntel Android App - Build Guide

## ✅ Prerequisites Completed
- ✓ Capacitor installed
- ✓ Android platform added
- ✓ Production build created

## 🔧 Building the Android APK

### Option 1: Build APK (Quick Method)

1. **Open Android Studio:**
   ```bash
   npx cap open android
   ```

2. **Wait for Gradle sync to complete** (first time may take 5-10 minutes)

3. **Build APK:**
   - Go to: `Build` → `Build Bundle(s) / APK(s)` → `Build APK(s)`
   - Wait for build to complete
   - Click "locate" in the notification popup
   - APK will be at: `android/app/build/outputs/apk/debug/app-debug.apk`

### Option 2: Build from Command Line

**Prerequisites:**
- Android Studio installed
- Android SDK configured
- JAVA_HOME environment variable set

**Commands:**
```bash
cd android
./gradlew assembleDebug
```

APK location: `android/app/build/outputs/apk/debug/app-debug.apk`

### Option 3: Build Release APK (For Distribution)

1. **Create a keystore (first time only):**
   ```bash
   keytool -genkey -v -keystore medintel-release-key.keystore -alias medintel -keyalg RSA -keysize 2048 -validity 10000
   ```

2. **Configure signing in `android/app/build.gradle`:**
   Add before `android` block:
   ```gradle
   def keystorePropertiesFile = rootProject.file("key.properties")
   def keystoreProperties = new Properties()
   if (keystorePropertiesFile.exists()) {
       keystoreProperties.load(new FileInputStream(keystorePropertiesFile))
   }
   ```

   Add inside `android` block:
   ```gradle
   signingConfigs {
       release {
           keyAlias keystoreProperties['keyAlias']
           keyPassword keystoreProperties['keyPassword']
           storeFile file(keystoreProperties['storeFile'])
           storePassword keystoreProperties['storePassword']
       }
   }
   buildTypes {
       release {
           signingConfig signingConfigs.release
           minifyEnabled false
           proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
       }
   }
   ```

3. **Create `android/key.properties`:**
   ```properties
   storePassword=YOUR_PASSWORD
   keyPassword=YOUR_PASSWORD
   keyAlias=medintel
   storeFile=../medintel-release-key.keystore
   ```

4. **Build release APK:**
   ```bash
   cd android
   ./gradlew assembleRelease
   ```

   APK location: `android/app/build/outputs/apk/release/app-release.apk`

## 📦 Current APK Location

After building, your APK will be at:
- **Debug:** `F:\ai chatbot\MedIntel\frontend\android\app\build\outputs\apk\debug\app-debug.apk`
- **Release:** `F:\ai chatbot\MedIntel\frontend\android\app\build\outputs\apk\release\app-release.apk`

## 🔄 Update App After Code Changes

Whenever you make changes to the code:

```bash
# 1. Build the web app
npm run build

# 2. Sync with Capacitor
npx cap sync android

# 3. Open in Android Studio (if needed)
npx cap open android

# 4. Rebuild APK
cd android
./gradlew assembleDebug
```

## 📲 Install APK on Device

### Method 1: USB Debugging
1. Enable Developer Options on your Android device
2. Enable USB Debugging
3. Connect device via USB
4. Run: `npx cap run android`

### Method 2: Manual Install
1. Transfer APK to your phone
2. Open APK file on phone
3. Allow "Install from Unknown Sources" if prompted
4. Install the app

## 🌐 Download Link

To create a download link:

1. **Upload APK to cloud storage:**
   - Google Drive
   - Dropbox
   - Firebase Hosting
   - GitHub Releases

2. **Share the download link**

### Example: Using GitHub Releases
```bash
# Create a release on GitHub
gh release create v1.0.0 android/app/build/outputs/apk/debug/app-debug.apk --title "MedIntel v1.0.0" --notes "Initial release"
```

## 📱 App Features

The Android app includes:
- ✅ Offline capability
- ✅ GPS location detection
- ✅ Push notifications (can be added)
- ✅ Native Android feel
- ✅ Fast performance
- ✅ All web features

## 🎨 Customize App Icon & Splash Screen

1. **Install asset generator:**
   ```bash
   npm install @capacitor/assets --save-dev
   ```

2. **Add icons:**
   - Place `icon.png` (1024x1024) in `assets/`
   - Place `splash.png` (2732x2732) in `assets/`

3. **Generate assets:**
   ```bash
   npx capacitor-assets generate --android
   ```

## 🔐 Permissions

Current permissions in `AndroidManifest.xml`:
- Internet Access
- Location Access (GPS)
- Network State
- Camera (for future features)

## 📊 App Size

- Debug APK: ~25-30 MB
- Release APK: ~15-20 MB (minified)

## 🚀 Publishing to Google Play Store

1. Build release APK (see above)
2. Create Google Play Developer account ($25 one-time fee)
3. Create new app in Play Console
4. Upload APK
5. Fill app details, screenshots, description
6. Submit for review

## 🆘 Troubleshooting

**Gradle sync failed:**
- Ensure Android SDK is installed
- Check JAVA_HOME is set
- Run: `cd android && ./gradlew clean`

**Build failed:**
- Update Gradle version in `android/gradle/wrapper/gradle-wrapper.properties`
- Check Android SDK version compatibility

**App crashes on launch:**
- Check `npx cap sync android` was run
- Verify all dependencies are installed
- Check Android Studio Logcat for errors

## 📞 Support

For issues, check:
- Capacitor docs: https://capacitorjs.com/docs
- Android Studio logs
- Browser console in dev mode

---

**Ready to build?** Run: `npx cap open android` to get started! 🎉
