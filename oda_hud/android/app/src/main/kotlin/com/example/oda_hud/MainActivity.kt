package com.example.oda_hud

import android.content.Intent
import android.os.Build
import android.os.Bundle
import android.speech.tts.TextToSpeech
import android.net.Uri
import android.os.Handler
import android.os.Looper
import androidx.core.content.FileProvider
import java.io.File
import java.net.HttpURLConnection
import java.net.URL
import androidx.core.content.ContextCompat
import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.MethodChannel
import java.util.Locale

class MainActivity : FlutterActivity(), TextToSpeech.OnInitListener {

    companion object {
        private const val CHANNEL = "odas/background"
        private const val VOICE_CHANNEL = "odas/voice"
        private const val UPDATE_CHANNEL = "odas/update"
    }

    private var textToSpeech: TextToSpeech? = null
    private var ttsReady = false
    private var pendingSpeech: String? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        textToSpeech = TextToSpeech(this, this)
    }

    override fun onInit(status: Int) {
        if (status == TextToSpeech.SUCCESS) {
            val result = textToSpeech?.setLanguage(
                Locale("pt", "BR")
            )

            ttsReady = result != TextToSpeech.LANG_MISSING_DATA &&
                    result != TextToSpeech.LANG_NOT_SUPPORTED

            textToSpeech?.setSpeechRate(1.0f)
            textToSpeech?.setPitch(1.0f)

            pendingSpeech?.let { pending ->
                pendingSpeech = null
                speak(pending)
            }
        }
    }

    override fun configureFlutterEngine(
        flutterEngine: FlutterEngine
    ) {
        super.configureFlutterEngine(flutterEngine)

        MethodChannel(
            flutterEngine.dartExecutor.binaryMessenger,
            CHANNEL
        ).setMethodCallHandler { call, result ->

            when (call.method) {

                "startForegroundService" -> {
                    startOdaService()
                    result.success(true)
                }

                "stopForegroundService" -> {
                    stopOdaService()
                    result.success(true)
                }

                else -> {
                    result.notImplemented()
                }
            }
        }


        MethodChannel(
            flutterEngine.dartExecutor.binaryMessenger,
            UPDATE_CHANNEL
        ).setMethodCallHandler { call, result ->

            when (call.method) {

                "downloadAndInstall" -> {
                    val url = call.argument<String>("url")

                    if (url.isNullOrBlank()) {
                        result.error(
                            "EMPTY_URL",
                            "URL do APK vazia.",
                            null
                        )
                        return@setMethodCallHandler
                    }

                    downloadAndInstall(url, result)
                }

                else -> {
                    result.notImplemented()
                }
            }
        }

        MethodChannel(
            flutterEngine.dartExecutor.binaryMessenger,
            VOICE_CHANNEL
        ).setMethodCallHandler { call, result ->

            when (call.method) {

                "speak" -> {
                    val text = call.argument<String>("text")

                    if (text.isNullOrBlank()) {
                        result.error(
                            "EMPTY_TEXT",
                            "Texto vazio.",
                            null
                        )
                        return@setMethodCallHandler
                    }

                    speak(text)
                    result.success(true)
                }

                "stop" -> {
                    textToSpeech?.stop()
                    result.success(true)
                }

                "setRate" -> {
                    val rate = call.argument<Double>("rate") ?: 1.0
                    textToSpeech?.setSpeechRate(
                        rate.coerceIn(0.5, 2.0).toFloat()
                    )
                    result.success(true)
                }

                "setPitch" -> {
                    val pitch = call.argument<Double>("pitch") ?: 1.0
                    textToSpeech?.setPitch(
                        pitch.coerceIn(0.5, 2.0).toFloat()
                    )
                    result.success(true)
                }

                else -> {
                    result.notImplemented()
                }
            }
        }
    }


    private fun downloadAndInstall(
        apkUrl: String,
        result: MethodChannel.Result
    ) {
        Thread {
            var connection: HttpURLConnection? = null

            try {
                val url = URL(apkUrl)
                connection = url.openConnection() as HttpURLConnection
                connection.connectTimeout = 15000
                connection.readTimeout = 30000
                connection.requestMethod = "GET"
                connection.instanceFollowRedirects = true
                connection.connect()

                if (connection.responseCode !in 200..299) {
                    throw Exception(
                        "Download HTTP ${connection.responseCode}"
                    )
                }

                val apkFile = File(
                    cacheDir,
                    "odas-update.apk"
                )

                connection.inputStream.use { input ->
                    apkFile.outputStream().use { output ->
                        input.copyTo(output)
                    }
                }

                if (!apkFile.exists() || apkFile.length() <= 0) {
                    throw Exception("APK baixado está vazio.")
                }

                Handler(Looper.getMainLooper()).post {
                    try {
                        val uri: Uri = FileProvider.getUriForFile(
                            this,
                            "${packageName}.fileprovider",
                            apkFile
                        )

                        val intent = Intent(
                            Intent.ACTION_VIEW
                        ).apply {
                            setDataAndType(
                                uri,
                                "application/vnd.android.package-archive"
                            )
                            addFlags(
                                Intent.FLAG_ACTIVITY_NEW_TASK or
                                Intent.FLAG_GRANT_READ_URI_PERMISSION
                            )
                        }

                        startActivity(intent)
                        result.success(true)

                    } catch (e: Exception) {
                        result.error(
                            "INSTALL_ERROR",
                            e.message,
                            null
                        )
                    }
                }

            } catch (e: Exception) {
                Handler(Looper.getMainLooper()).post {
                    result.error(
                        "DOWNLOAD_ERROR",
                        e.message,
                        null
                    )
                }
            } finally {
                connection?.disconnect()
            }
        }.start()
    }

    private fun speak(text: String) {
        if (text.isBlank()) return

        if (!ttsReady || textToSpeech == null) {
            pendingSpeech = text
            return
        }

        val status = textToSpeech?.speak(
            text,
            TextToSpeech.QUEUE_FLUSH,
            null,
            "ODAS_RESPONSE"
        )

        if (status == TextToSpeech.ERROR) {
            android.util.Log.e(
                "ODAS_TTS",
                "Falha ao executar TTS"
            )
        } else {
            android.util.Log.i(
                "ODAS_TTS",
                "Falando: $text"
            )
        }
    }

    private fun startOdaService() {
        val intent = Intent(
            this,
            OdaForegroundService::class.java
        )

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            ContextCompat.startForegroundService(
                this,
                intent
            )
        } else {
            startService(intent)
        }
    }

    private fun stopOdaService() {
        val intent = Intent(
            this,
            OdaForegroundService::class.java
        )

        stopService(intent)
    }

    override fun onDestroy() {
        textToSpeech?.stop()
        textToSpeech?.shutdown()
        textToSpeech = null
        super.onDestroy()
    }
}
