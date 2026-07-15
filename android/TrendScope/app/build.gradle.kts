plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
    id("org.jetbrains.kotlin.kapt")
    id("org.jetbrains.kotlin.plugin.serialization") version "1.9.22"
}

android {
    namespace = "com.trendscope.app"
    compileSdk = 36

    defaultConfig {
        applicationId = "com.trendscope.app"
        minSdk = 26
        targetSdk = 36
        versionCode = 1
        versionName = "1.0.1"
        buildConfigField("String", "GNEWS_API_KEY", "\"${project.findProperty("gnewsApiKey") ?: ""}\"")
        buildConfigField("String", "NEWSAPI_KEY", "\"${project.findProperty("newsapiKey") ?: ""}\"")
    }

    signingConfigs {
        create("release") {
            storeFile = file(System.getenv("KEYSTORE_PATH") ?: "release.keystore")
            storePassword = System.getenv("KEYSTORE_STORE_PASSWORD") ?: project.findProperty("keystoreStorePassword") as? String ?: ""
            keyAlias = System.getenv("KEYSTORE_KEY_ALIAS")
    ?: project.findProperty("keystoreKeyAlias") as? String
    ?: "trendscope"
            keyPassword = System.getenv("KEYSTORE_KEY_PASSWORD") ?: project.findProperty("keystoreKeyPassword") as? String ?: ""
            enableV1Signing = true
            enableV2Signing = true
            enableV3Signing = true
        }
    }

    buildTypes {
        release {
            isMinifyEnabled = true
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
            signingConfig = signingConfigs.getByName("release")
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions {
        jvmTarget = "17"
    }
    buildFeatures {
        viewBinding = true
        buildConfig = true
    }
}

configurations.all {
    resolutionStrategy {
        force("androidx.core:core-ktx:1.12.0")
    }
}

dependencies {
    implementation("androidx.core:core-ktx:1.12.0")
    implementation("androidx.appcompat:appcompat:1.6.1")
    implementation("com.google.android.material:material:1.11.0")
    implementation("androidx.swiperefreshlayout:swiperefreshlayout:1.1.0")
    implementation("androidx.recyclerview:recyclerview:1.3.2")
    implementation("androidx.cardview:cardview:1.0.0")
    implementation("androidx.constraintlayout:constraintlayout:2.1.4")
    implementation("androidx.viewpager2:viewpager2:1.0.0")

    // Kotlin coroutines
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.3")
    implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.6.2")

    // OkHttp for network
    implementation("com.squareup.okhttp3:okhttp:4.12.0")

    // Room for local storage
    implementation("androidx.room:room-runtime:2.6.1")
    implementation("androidx.room:room-ktx:2.6.1")
    kapt("androidx.room:room-compiler:2.6.1")

    // ViewModel + LiveData
    implementation("androidx.lifecycle:lifecycle-viewmodel-ktx:2.7.0")
    implementation("androidx.lifecycle:lifecycle-livedata-ktx:2.7.0")
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.7.0")

    // Coil for image loading
    implementation("io.coil-kt:coil:2.5.0")

    // WorkManager for background downloads
    implementation("androidx.work:work-runtime-ktx:2.9.0")

    // DataStore for modern preferences
    implementation("androidx.datastore:datastore-preferences:1.0.0")

}

