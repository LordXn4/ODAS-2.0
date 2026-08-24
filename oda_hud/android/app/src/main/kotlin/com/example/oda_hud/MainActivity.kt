package com.example.oda_hud

import android.content.Intent
import android.os.Build
import android.os.Bundle
import android.speech.tts.TextToSpeech
import androidx.core.content.ContextCompat
import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.MethodChannel
import java.util.Locale

class MainActivity : FlutterActivity(), TextToSpeech.OnInitListener {

    companion object {
        private const val CHANNEL = "odas/background"
        private const val VOICE_CHANNEL = "odas/voice"
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
